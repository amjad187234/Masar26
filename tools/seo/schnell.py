"""Schnelleres Navigieren: Speculation Rules (Vorladen interner Links bei Hover/Touch) + weiche Seitenübergänge
(View Transitions). Nur öffentliche HTML-Seiten; /admin, PHP, /tools und PDFs werden nie vorgeladen.
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


def main():
    n = 0
    for p in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
        rel = os.path.relpath(p, ROOT)
        if rel.startswith(AUSNAHMEN): continue
        s = open(p, encoding='utf-8').read()
        if '</head>' not in s: continue
        neu = re.sub(re.escape(A) + r'.*?' + re.escape(Z) + r'\n?', '', s, flags=re.S)
        neu = neu.replace('</head>', BLOCK + '</head>', 1)
        if neu != s:
            open(p, 'w', encoding='utf-8').write(neu); n += 1
    print(n, 'Seiten aktualisiert')


if __name__ == '__main__':
    main()
