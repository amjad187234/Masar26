"""<lastmod> in sitemap.xml ehrlich halten: Datum der letzten Änderung am *Inhalt* einer Seite.

Google nutzt lastmod nur, wenn es „durchgehend und nachprüfbar stimmt“. Seitenweite Technik-Änderungen
(Farben, Skripte, Fußzeile, Kopfbereich) zählen deshalb nicht – verglichen wird nur der sichtbare Haupttext
(Überschriften, Absätze, Listen, Tabellen, Bildunterschriften, Bild-alt; ohne nav/footer/script/style/form).

    python3 tools/seo/sitemap_lastmod.py          lastmod aktualisieren (Inhalt geändert → heute)
    python3 tools/seo/sitemap_lastmod.py --dry    nur anzeigen
    python3 tools/seo/sitemap_lastmod.py --git    Startwerte aus der Git-Historie neu berechnen

Speicher: tools/seo/inhalt_hashes.json (Seite → [Hash, Datum]). Fehlt eine Seite dort, wird ihr Datum
aus der Git-Historie bestimmt (letzter Commit, der den Haupttext verändert hat). Ein späteres, von Hand
gesetztes lastmod bleibt erhalten. Am Ende der Pipeline ausführen (nach umbruch.py).
"""
import os, re, sys, json, hashlib, subprocess, datetime
from html.parser import HTMLParser

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
SITE = 'https://masar-werbeagentur.de/'
SPEICHER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inhalt_hashes.json')
SKIP = {'nav', 'footer', 'script', 'style', 'template', 'noscript', 'form', 'dialog', 'svg', 'head', 'button'}
INHALT = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'td', 'th', 'dt', 'dd', 'figcaption', 'blockquote', 'summary'}
LEER = {'br', 'img', 'hr', 'meta', 'link', 'input', 'source', 'wbr'}


class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []; self.teile = []; self.skip = 0; self.inhalt = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'img' and not self.skip and a.get('alt'): self.teile.append('[' + a['alt'] + ']')
        if tag in LEER: return
        sk = tag in SKIP or 'as-classic' in (a.get('class') or '') or a.get('aria-hidden') == 'true'
        self.stack.append((tag, sk, tag in INHALT))
        if sk: self.skip += 1
        if tag in INHALT: self.inhalt += 1

    def handle_endtag(self, tag):
        if tag in LEER: return
        while self.stack:
            t, sk, inh = self.stack.pop()
            if sk: self.skip -= 1
            if inh: self.inhalt -= 1
            if t == tag: break

    def handle_data(self, d):
        if not self.skip and self.inhalt: self.teile.append(d)


def inhalt_hash(s):
    # sitzenweite Technik-Blöcke vorher entfernen
    s = re.sub(r'<!-- (\w+):start -->.*?<!-- \1:ende -->', '', s, flags=re.S)
    p = Text()
    try: p.feed(s)
    except Exception: pass
    # ohne Leerraum und weiche Trennstriche: <span class="nw"> oder entfernte &shy; sind keine Inhaltsänderung
    t = re.sub(r'\s+', '', ''.join(p.teile)).replace('­', '')
    return hashlib.sha1(t.encode('utf-8')).hexdigest()[:16]


def git(*a):
    return subprocess.run(['git', '-C', ROOT] + list(a), capture_output=True, text=True).stdout


def aus_git(rel):
    """Datum des letzten Commits, der den Haupttext von rel verändert hat."""
    log = [l.split() for l in git('log', '--format=%H %cs', '--', rel).splitlines() if l.strip()]
    log.reverse()  # alt → neu
    vorher, datum, erster = None, None, True
    for sha, d in log:
        s = git('show', f'{sha}:{rel}')
        if not s: continue
        h = inhalt_hash(s)
        if h != vorher:
            # erster Stand = Aufnahme ins Repository, nicht unbedingt Veröffentlichung → kein Datum ableiten
            datum = None if erster else d
            vorher = h
        erster = False
    return datum


def rel_von(loc):
    r = loc.replace(SITE, '', 1)
    return r + 'index.html' if r == '' or r.endswith('/') else r


def main():
    dry = '--dry' in sys.argv
    neu_git = '--git' in sys.argv
    heute = datetime.date.today().isoformat()
    sp = {} if neu_git or not os.path.exists(SPEICHER) else json.load(open(SPEICHER, encoding='utf-8'))
    sm_pfad = os.path.join(ROOT, 'sitemap.xml')
    x = open(sm_pfad, encoding='utf-8').read()
    geaendert = 0

    def ersetze(m):
        nonlocal geaendert
        loc, alt = m.group(2), m.group(4)
        rel = rel_von(loc)
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p): return m.group(0)
        h = inhalt_hash(open(p, encoding='utf-8').read())
        if rel not in sp:
            d = aus_git(rel) or (alt[:10] if alt else heute)
            # Arbeitskopie weicht vom letzten Commit ab → heute
            kopf = git('show', f'HEAD:{rel}')
            if kopf and inhalt_hash(kopf) != h: d = heute
            sp[rel] = [h, d]
        elif sp[rel][0] != h:
            sp[rel] = [h, heute]
        d = sp[rel][1]
        if alt and alt[:10] > d: d = alt[:10]   # späteres Handdatum behalten
        if d == (alt or '')[:10]: return m.group(0)
        geaendert += 1
        print(f'{rel:55} {alt} → {d}')
        if m.group(3): return m.group(1) + m.group(3).replace(alt, d)
        return m.group(1) + f'\n    <lastmod>{d}</lastmod>'

    x2 = re.sub(r'(<loc>([^<]+)</loc>)(\s*<lastmod>([^<]+)</lastmod>)?', ersetze, x)
    print(geaendert, 'lastmod', 'würden geändert' if dry else 'geändert')
    if not dry:
        open(sm_pfad, 'w', encoding='utf-8').write(x2)
        zeilen = [f'{json.dumps(k, ensure_ascii=False)}: {json.dumps(v)}' for k, v in sorted(sp.items())]
        open(SPEICHER, 'w', encoding='utf-8').write('{\n' + ',\n'.join(zeilen) + '\n}\n')


if __name__ == '__main__':
    main()
