"""Untere Leiste (#stickyCta): Textzeile wird zum Link „Kostenlose Beratung buchen“ – mit dem Thema der Seite.

  python3 tools/sticky_termin.py            → alle HTML-Seiten
  python3 tools/sticky_termin.py a.html …   → nur diese Seiten
Idempotent (Marker data-termin-link). Nach dem Neu-Erzeugen von Seiten erneut ausführen.
"""
import html, os, re, sys, urllib.parse

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))).rstrip('/') + '/'
BTN = ("text-decoration:none;display:inline-flex;align-items:center;justify-content:center;gap:6px;border:1.5px solid #58d0bd;background:rgba(88,208,189,.16);color:#fff;border-radius:8px;padding:9px 16px;font-weight:700;line-height:1.3")
CAL = ('<svg class="i-inline" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
       '<path d="M4 6h16v14H4zM4 10h16M8 3v4M16 3v4"/></svg>')
ALLGEMEIN = {'Masar Werbeagentur', ''}


def link(thema: str, seite: str) -> str:
    if seite == 'termin.html':
        return '#termin'
    return '/termin.html' + ('?thema=' + urllib.parse.quote(thema) if thema not in ALLGEMEIN else '')


def neu_scta(m, seite):
    inner = m.group(1)
    sp = re.search(r'<span>(.*?)</span>', inner)
    thema = html.unescape(re.sub(r'<[^>]+>', '', sp.group(1))).strip() if sp else ''
    text = f'{CAL}<b style="color:#fff">Kostenlose Beratung buchen →</b>'   # Thema geht über den Link mit
    return (f'<a class="scta-txt" data-termin-link data-btn href="{html.escape(link(thema, seite))}" '
            f'style="{BTN}">{text}</a>')


def blog_cta(s: str) -> str:
    """Blogartikel: dritte Taste „Kostenlose Beratung buchen“ im Kasten am Artikelende (Thema = Kastenüberschrift)."""
    m = re.search(r'<div class="article-cta">\s*<h3>(.*?)</h3>.*?<div class="btns">(.*?)</div>', s, re.S)
    if not m:
        return s
    thema = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()
    taste = (f'\n        <a href="{html.escape(link(thema, ""))}" data-termin-link class="btn-termin" '
             f'style="background:#fff;color:var(--navy);padding:13px 24px;border-radius:8px;font-weight:700;font-size:15px">{CAL} Kostenlose Beratung buchen</a>\n      ')
    return s[:m.end(2)].rstrip() + taste + s[m.end(2):]


def bearbeiten(pfad: str) -> bool:
    seite = os.path.relpath(pfad, ROOT)
    s = open(pfad, encoding='utf-8').read()
    if 'data-termin-link' in s:
        return False
    if 'id="stickyCta"' not in s:
        neu = blog_cta(s)
        if neu != s:
            open(pfad, 'w', encoding='utf-8').write(neu)
            return True
        return False
    alt = s
    # Variante 1: <div class="scta-txt">★<span>Thema</span> – Text</div>
    s = re.sub(r'<div class="scta-txt">(.*?)</div>', lambda m: neu_scta(m, seite), s, count=1, flags=re.S)
    # Variante 2: <div class="sticky-cta-text"><strong>…</strong><span>…</span></div>
    s = re.sub(r'<div class="sticky-cta-text">.*?</div>',
               f'<a class="sticky-cta-text" data-termin-link data-btn href="{link("", seite)}" style="{BTN}">'
               f'<strong style="color:#fff;font-size:14px">{CAL} Kostenlose Beratung buchen →</strong></a>',
               s, count=1, flags=re.S)
    if s != alt:
        open(pfad, 'w', encoding='utf-8').write(s)
        return True
    return False


if __name__ == '__main__':
    dateien = sys.argv[1:] or [os.path.join(d, f) for d, _, fs in os.walk(ROOT) if '/tools' not in d and '/.git' not in d for f in fs if f.endswith('.html')]
    n = sum(bearbeiten(f if os.path.isabs(f) else ROOT + f) for f in dateien)
    print(n, 'Seiten geändert')
