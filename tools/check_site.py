"""Prüft die statische Website (nur lesen, ändert nichts). Exit-Code 1, wenn etwas gefunden wird.

  python3 tools/check_site.py                  alle Prüfungen
  python3 tools/check_site.py --nur links,ids  nur bestimmte Prüfungen
  python3 tools/check_site.py --max 20         höchstens 20 Meldungen je Prüfung anzeigen (Standard 40)
  python3 tools/check_site.py --list           Prüfungen anzeigen

Prüfungen:
  links      interne Links (href) auf vorhandene Dateien; Links auf 301-Weiterleitungen aus .htaccess
  anker      #anker auf derselben oder einer anderen Seite (id/name muss existieren)
  dateien    Bilder (src, srcset, poster, og:image, url(...)), Skripte, Stylesheets, Icons, Manifest
  ids        doppelte id-Attribute auf einer Seite
  alt        <img> ohne alt-Attribut (alt="" für reine Schmuckbilder ist erlaubt)
  main       genau ein <main> mit Ende-Tag
  sitemap    öffentliche Seiten fehlen in sitemap.xml / Einträge ohne Datei / noindex-Seiten in der Sitemap
  versionen  dieselbe JS/CSS-Datei mit verschiedenen ?v=-Versionen auf verschiedenen Seiten
  bloecke    Seiten ohne Footer-Claim (marke.py), ohne umbruch- oder schnell-Block
Öffentliche Seiten = alle .html außer tools/, admin/, data/, node_modules/, uploads/.
"""
import argparse, collections, html.parser, os, re, sys, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(HERE, '..'))).rstrip('/')
BASE = 'https://masar-werbeagentur.de'
OHNE = ('tools/', 'admin/', 'data/', 'node_modules/', 'uploads/', '.git/', '.claude/', 'destadsmuur/')  # destadsmuur: eigenständige Kundenseite
PRUEFUNGEN = ['links', 'anker', 'dateien', 'ids', 'alt', 'main', 'sitemap', 'versionen', 'bloecke']
# QR-Landingpages (noindex) mit eigener Mini-Fußzeile: ohne Claim und ohne <main> erlaubt
SONDERSEITEN = {'qr.html', 'qr/index.html'}
# Anker, die erst Skripte erzeugen oder die der Browser kennt
ANKER_OK = {'', 'top', 'main-content'}


class Seite(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = collections.Counter(); self.namen = set()
        self.links = []      # (attr, url, zeile)
        self.dateien = []    # (tag, url, zeile)
        self.ohne_alt = []   # zeile
        self.main_auf = self.main_zu = 0
        self.meta = {}
        self.styles = []
        self._in_style = False
        self._in_script = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs); z = self.getpos()[0]
        if 'id' in a and a['id']: self.ids[a['id']] += 1
        if tag == 'a' and a.get('name'): self.namen.add(a['name'])
        if tag == 'main': self.main_auf += 1
        if tag in ('a', 'area') and a.get('href') is not None: self.links.append(('href', a['href'], z))
        if tag == 'form' and a.get('action'): self.links.append(('action', a['action'], z))
        if tag in ('img', 'source', 'video', 'audio', 'iframe', 'script', 'track', 'embed', 'input'):
            if a.get('src'): self.dateien.append((tag, a['src'], z))
            for k in ('srcset', 'data-srcset'):
                if a.get(k):
                    for teil in a[k].split(','):
                        u = teil.strip().split(' ')[0]
                        if u: self.dateien.append((tag, u, z))
            if a.get('poster'): self.dateien.append((tag, a['poster'], z))
        if tag == 'img' and 'alt' not in a: self.ohne_alt.append(z)
        if tag == 'link' and a.get('href'):
            rel = (a.get('rel') or '').lower()
            if any(r in rel for r in ('stylesheet', 'icon', 'manifest', 'preload', 'apple-touch-icon')):
                self.dateien.append(('link', a['href'], z))
        if tag == 'meta':
            k = a.get('property') or a.get('name')
            if k: self.meta[k.lower()] = a.get('content', '')
            if k in ('og:image', 'twitter:image') and a.get('content'): self.dateien.append(('meta', a['content'], z))
        if a.get('style'): self.styles.append((a['style'], z))
        if tag == 'style': self._in_style = True

    def handle_endtag(self, tag):
        if tag == 'main': self.main_zu += 1
        if tag == 'style': self._in_style = False

    def handle_data(self, data):
        if self._in_style: self.styles.append((data, self.getpos()[0]))


def oeffentlich(rel):
    return rel.endswith('.html') and not rel.startswith(OHNE)


def alle_seiten():
    out = []
    for d, ds, fs in os.walk(ROOT):
        rel_d = os.path.relpath(d, ROOT)
        ds[:] = [x for x in ds if not (os.path.normpath(os.path.join(rel_d, x)) + '/').startswith(OHNE) and x not in ('.git', 'node_modules', '__pycache__')]
        for f in fs:
            rel = os.path.normpath(os.path.join(rel_d, f))
            if oeffentlich(rel): out.append(rel)
    return sorted(out)


def weiterleitungen():
    """Pfade (ohne /), die .htaccess per R=301/302 umleitet: [(regex, ziel)]."""
    out = []
    p = os.path.join(ROOT, '.htaccess')
    if not os.path.exists(p): return out
    for z in open(p, encoding='utf-8', errors='replace'):
        m = re.match(r'\s*RewriteRule\s+(\^\S+)\s+(\S+)\s+\[[^\]]*R=30[12]', z)
        if m and m.group(1) != '^':
            try: out.append((re.compile(m.group(1)), m.group(2)))
            except re.error: pass
    return out


def lokal(url, seite):
    """URL → (relativer Dateipfad oder None für extern/ignoriert, Anker)."""
    url = url.strip()
    if not url or url.startswith(('mailto:', 'tel:', 'javascript:', 'data:', 'sms:', 'whatsapp:', 'blob:')): return None, None
    if url.startswith('//'): return None, None
    if url.startswith(('http://', 'https://')):
        if not url.startswith((BASE + '/', BASE + '?', BASE + '#')) and url != BASE: return None, None
        url = url[len(BASE):] or '/'
    if '${' in url or '{{' in url or "'+" in url: return None, None   # Vorlagen in Skripten
    teile = urllib.parse.urlsplit(url)
    pfad = urllib.parse.unquote(teile.path)
    if not pfad:   # nur ?query oder #anker
        return seite, teile.fragment
    if pfad.startswith('/'):
        rel = pfad.lstrip('/')
    else:
        rel = os.path.normpath(os.path.join(os.path.dirname(seite), pfad))
        if rel == '.': rel = ''
    return rel, teile.fragment


def aufloesen(rel):
    """Dateipfad, den der Server ausliefern würde (Verzeichnis → index.html), oder None."""
    p = os.path.join(ROOT, rel)
    if rel == '' or rel.endswith('/') or os.path.isdir(p):
        q = os.path.join(p, 'index.html')
        return os.path.relpath(q, ROOT) if os.path.isfile(q) else None
    return rel if os.path.isfile(p) else None


def main():
    ap = argparse.ArgumentParser(description='Website-Prüfung (nur lesen)')
    ap.add_argument('--nur', help='Prüfungen, mit Komma getrennt: ' + ', '.join(PRUEFUNGEN))
    ap.add_argument('--max', type=int, default=40, help='höchstens so viele Meldungen je Prüfung anzeigen')
    ap.add_argument('--list', action='store_true')
    a = ap.parse_args()
    if a.list:
        print(__doc__.split('Prüfungen:')[1].split('Öffentliche')[0]); return 0
    aktiv = [x.strip() for x in a.nur.split(',')] if a.nur else PRUEFUNGEN
    for x in aktiv:
        if x not in PRUEFUNGEN: raise SystemExit(f'Unbekannte Prüfung „{x}“ – mögliche: ' + ', '.join(PRUEFUNGEN))

    seiten = alle_seiten()
    daten, quelltext = {}, {}
    for rel in seiten:
        s = open(os.path.join(ROOT, rel), encoding='utf-8', errors='replace').read()
        p = Seite()
        try:
            p.feed(s); p.close()
        except Exception as e:   # sollte nicht vorkommen
            print(f'{rel}: HTML nicht lesbar ({e})'); continue
        daten[rel], quelltext[rel] = p, s

    funde = collections.defaultdict(list)
    wl = weiterleitungen()
    anker_cache = {}

    def anker_von(rel):
        if rel not in anker_cache:
            if rel in daten: anker_cache[rel] = set(daten[rel].ids) | daten[rel].namen
            else:
                p = Seite()
                try: p.feed(open(os.path.join(ROOT, rel), encoding='utf-8', errors='replace').read())
                except Exception: pass
                anker_cache[rel] = set(p.ids) | p.namen
        return anker_cache[rel]

    for rel, p in daten.items():
        s = quelltext[rel]
        # links + anker
        for attr, url, z in p.links:
            ziel, frag = lokal(url, rel)
            if ziel is None: continue
            if ziel == rel and not urllib.parse.urlsplit(url).path:   # #anker auf derselben Seite
                if 'anker' in aktiv and frag and frag not in ANKER_OK and frag not in anker_von(rel):
                    funde['anker'].append(f'{rel}:{z}: #{frag} gibt es auf der Seite nicht')
                continue
            datei = aufloesen(ziel)
            if datei is None:
                umg = next((zz for rx, zz in wl if rx.match(ziel)), None)
                if 'links' in aktiv:
                    if umg: funde['links'].append(f'{rel}:{z}: Link auf Weiterleitung /{ziel} → {umg}')
                    else: funde['links'].append(f'{rel}:{z}: {url} – Datei fehlt')
                continue
            if 'anker' in aktiv and frag and datei.endswith('.html') and frag not in ANKER_OK and frag not in anker_von(datei):
                funde['anker'].append(f'{rel}:{z}: {url} – #{frag} gibt es auf {datei} nicht')
        # dateien
        if 'dateien' in aktiv:
            liste = list(p.dateien)
            for css, z in p.styles:
                for m in re.finditer(r'url\(\s*["\']?([^)"\']+)["\']?\s*\)', css):
                    liste.append(('url()', m.group(1), z))
            for tag, url, z in liste:
                ziel, _ = lokal(url, rel)
                if ziel is None or ziel == rel: continue
                if aufloesen(ziel) is None:
                    funde['dateien'].append(f'{rel}:{z}: <{tag}> {url} – Datei fehlt')
        # ids
        if 'ids' in aktiv:
            for i, n in p.ids.items():
                if n > 1: funde['ids'].append(f'{rel}: id="{i}" kommt {n}× vor')
        # alt
        if 'alt' in aktiv:
            for z in p.ohne_alt: funde['alt'].append(f'{rel}:{z}: <img> ohne alt')
        # main
        if 'main' in aktiv and '<footer' in s and rel not in SONDERSEITEN:
            if p.main_auf != 1 or p.main_zu != 1:
                funde['main'].append(f'{rel}: {p.main_auf}× <main>, {p.main_zu}× </main>')

    # sitemap
    if 'sitemap' in aktiv:
        sm = os.path.join(ROOT, 'sitemap.xml')
        locs = re.findall(r'<loc>\s*([^<\s]+)\s*</loc>', open(sm, encoding='utf-8').read()) if os.path.exists(sm) else []
        in_sm = set()
        for u in locs:
            ziel, _ = lokal(u, '')
            datei = aufloesen(ziel) if ziel is not None else None
            if datei is None: funde['sitemap'].append(f'sitemap.xml: {u} – Datei fehlt')
            else: in_sm.add(datei)
        for rel, p in daten.items():
            noindex = 'noindex' in p.meta.get('robots', '').lower()
            if noindex and rel in in_sm: funde['sitemap'].append(f'{rel}: steht in sitemap.xml, hat aber noindex')
            elif not noindex and rel not in in_sm: funde['sitemap'].append(f'{rel}: fehlt in sitemap.xml (kein noindex)')

    # versionen
    if 'versionen' in aktiv:
        ver = collections.defaultdict(lambda: collections.defaultdict(list))
        for rel, p in daten.items():
            for tag, url, z in p.dateien:
                if tag not in ('script', 'link'): continue
                ziel, _ = lokal(url, rel)
                if not ziel or not ziel.endswith(('.js', '.css')): continue
                q = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query).get('v', [''])[0]
                ver[ziel][q or '(ohne)'].append(rel)
        for datei, vs in sorted(ver.items()):
            if len(vs) > 1:
                haupt = max(vs, key=lambda k: len(vs[k]))
                rest = '; '.join(f'?v={k}: {len(v)} Seiten (z. B. {", ".join(sorted(v)[:3])})' for k, v in sorted(vs.items()) if k != haupt)
                funde['versionen'].append(f'/{datei}: meist ?v={haupt} ({len(vs[haupt])} Seiten), abweichend {rest}')

    # bloecke
    if 'bloecke' in aktiv:
        for rel, s in quelltext.items():
            fehlt = []
            if '<footer' in s and rel not in SONDERSEITEN and 'foot-claim' not in s: fehlt.append('Footer-Claim')
            if '</head>' in s and '<!-- umbruch:start -->' not in s: fehlt.append('umbruch')
            if '</head>' in s and '<!-- schnell:start -->' not in s: fehlt.append('schnell')
            if fehlt: funde['bloecke'].append(f'{rel}: ohne ' + ', '.join(fehlt))

    gesamt = 0
    print(f'{len(daten)} Seiten geprüft ({ROOT})')
    for x in aktiv:
        f = funde.get(x, [])
        gesamt += len(f)
        print(f'\n[{x}] ' + (f'{len(f)} Befund(e)' if f else 'ok'))
        for z in f[:a.max]: print('  ' + z)
        if len(f) > a.max: print(f'  … und {len(f) - a.max} weitere (--max erhöhen)')
    print(f'\n{"Keine Befunde." if not gesamt else f"{gesamt} Befund(e)."}')
    return 1 if gesamt else 0


if __name__ == '__main__':
    sys.exit(main())
