"""Schnelleres Navigieren: Speculation Rules (Vorladen interner Links bei Hover/Touch) + weiche Seitenübergänge
(View Transitions). Nur öffentliche HTML-Seiten; /admin, PHP, /tools und PDFs werden nie vorgeladen.
Außerdem bekommen Galerie-Bilder ohne srcset die vorhandenen kleineren WebP-Varianten (-480/-720), und die
Vorladung des Logos (preload, fetchpriority=high) entfällt, damit Schriften und Hero-Bild Vorrang haben.
Idempotent (Marker). Aufruf: python3 tools/seo/schnell.py
"""
import os, re, glob

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
A, Z = '<!-- schnell:start -->', '<!-- schnell:ende -->'
REGELN = ('{"prefetch":[{"source":"document","where":{"and":[{"href_matches":"/*"},{"not":{"href_matches":["/admin/*","/*.php","/*.php?*","/tools/*","/*.pdf"]}},'
          '{"not":{"selector_matches":"[rel~=nofollow],[target=_blank]"}}]},"eagerness":"moderate"}]}')
BLOCK = (f'{A}\n<script type="speculationrules">{REGELN}</script>\n'
         '<style>@view-transition{navigation:auto}@media (prefers-reduced-motion:reduce){@view-transition{navigation:none}}</style>\n'
         f'{Z}\n')
AUSNAHMEN = ('admin/', 'tools/', 'node_modules/', 'data/')
# Galerie-Bilder („Aus unserer Arbeit“, gen_folien.py) kamen ohne srcset – das Handy lud 1200-px-Originale.
GALERIE = re.compile(r'<img src="(/[^"]+)\.webp" width="(\d+)" height="(\d+)"(?![^>]*srcset)([^>]*style="width:100%;aspect-ratio:4/3)')
GROESSEN = '(max-width: 700px) 100vw, 400px'


def breite(datei):
    try:
        from PIL import Image
        return Image.open(datei).size[0]
    except Exception:
        m = re.search(r'-(\d+)\.webp$', datei)
        return int(m.group(1)) if m else None


def srcset(m):
    stamm, w = m.group(1), m.group(2)
    teile = []
    for v in ('360', '480', '540', '720'):
        f = os.path.join(ROOT, f'{stamm}-{v}.webp'.lstrip('/'))
        if os.path.exists(f):
            b = breite(f)
            if b and b < int(w): teile.append(f'{stamm}-{v}.webp {b}w')
    if not teile: return m.group(0)
    teile.append(f'{stamm}.webp {w}w')
    return (f'<img src="{stamm}.webp" srcset="{", ".join(teile)}" sizes="{GROESSEN}" '
            f'width="{w}" height="{m.group(3)}"{m.group(4)}')


def main():
    n = 0
    for p in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
        rel = os.path.relpath(p, ROOT)
        if rel.startswith(AUSNAHMEN): continue
        s = open(p, encoding='utf-8').read()
        if '</head>' not in s: continue
        if A in s:   # vorhandenen Block an seiner Stelle ersetzen (keine unnötigen Verschiebungen im Kopf)
            neu = re.sub(re.escape(A) + r'.*?' + re.escape(Z) + r'\n?', lambda m: BLOCK, s, count=1, flags=re.S)
        else:
            neu = s.replace('</head>', BLOCK + '</head>', 1)
        neu = GALERIE.sub(srcset, neu)
        # Logo nicht mehr mit hoher Priorität vorladen: es steht ohnehin oben im HTML und ist nie das LCP-Element
        # der Seite – die Vorladung konkurrierte mit Schriften und Hero-Bild (fetchpriority="high").
        neu = neu.replace('<link rel="preload" as="image" href="/logo.webp" fetchpriority="high">\n', '')
        if neu != s:
            open(p, 'w', encoding='utf-8').write(neu); n += 1
    print(n, 'Seiten aktualisiert')


if __name__ == '__main__':
    main()
