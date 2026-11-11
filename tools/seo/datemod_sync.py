"""JSON-LD "dateModified" jeder Seite an das <lastmod> in sitemap.xml angleichen.

sitemap_lastmod.py bestimmt das Datum der letzten *inhaltlichen* Änderung (ehrlich, inhaltbasiert).
Dieses Skript trägt genau dieses Datum in das "dateModified" der Seite (Article/BlogPosting-JSON-LD) ein,
damit Seite und Sitemap übereinstimmen. "datePublished" bleibt unangetastet. Nur wenn beide Werte
abweichen wird geschrieben; "dateModified" wird nie vor "datePublished" gesetzt.

Am Ende der Pipeline ausführen (nach sitemap_lastmod.py). Aufruf: python3 tools/seo/datemod_sync.py [--dry]
"""
import os, re, sys

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
SITE = 'https://masar-werbeagentur.de/'
DM = re.compile(r'("dateModified"\s*:\s*")(\d{4}-\d{2}-\d{2})(")')
DP = re.compile(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})"')


def sitemap_lastmod():
    p = os.path.join(ROOT, 'sitemap.xml')
    s = open(p, encoding='utf-8').read()
    out = {}
    for m in re.finditer(r'<loc>\s*([^<]+?)\s*</loc>\s*(?:<lastmod>\s*([^<]+?)\s*</lastmod>)?', s, re.S):
        loc, lm = m.group(1), m.group(2)
        if not lm: continue
        rel = loc.replace(SITE, '').lstrip('/')
        if rel in ('', '/'): rel = 'index.html'
        out[rel] = lm[:10]
    return out


def main():
    dry = '--dry' in sys.argv
    lm = sitemap_lastmod()
    n = 0
    for rel, datum in lm.items():
        p = os.path.join(ROOT, rel)
        if not p.endswith('.html') or not os.path.isfile(p): continue
        s = open(p, encoding='utf-8').read()
        if '"dateModified"' not in s: continue
        dp = DP.search(s)
        ziel = datum
        if dp and ziel < dp.group(1): ziel = dp.group(1)  # nie vor Veröffentlichung
        neu, k = DM.subn(lambda m: m.group(1) + ziel + m.group(3) if m.group(2) != ziel else m.group(0), s)
        if neu != s:
            n += 1
            if not dry: open(p, 'w', encoding='utf-8').write(neu)
    print(n, 'Seiten: dateModified an sitemap.xml angeglichen', '(Probelauf)' if dry else '')


if __name__ == '__main__':
    main()
