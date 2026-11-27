"""Vorschau-Rechte für Suche und KI-Antworten: alle indexierbaren Seiten erlauben volle Textauszüge
und große Vorschaubilder (max-snippet:-1, max-image-preview:large, max-video-preview:-1).

Das sind die von Google dokumentierten Steuerungen dafür, wie viel einer Seite in Suchergebnissen
und KI-Funktionen (AI Overviews, AI Mode) gezeigt werden darf. Seiten mit noindex bleiben unberührt.
Idempotent. Aufruf: python3 tools/seo/vorschau.py   (--dry zeigt nur, was sich ändern würde)
"""
import os, re, sys, glob

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
ZIEL = '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">'
TAG = re.compile(r'<meta name="robots" content="([^"]*)">')


def main():
    dry = '--dry' in sys.argv
    n = 0
    for pfad in sorted(glob.glob(os.path.join(ROOT, '*.html')) + glob.glob(os.path.join(ROOT, 'blog', '*.html'))):
        s = open(pfad, encoding='utf-8').read()
        kopf = s[:s.find('</head>')] if '</head>' in s else ''
        if not kopf or 'rel="canonical"' not in kopf: continue          # Fehler-/Systemseiten
        m = TAG.search(kopf)
        if m:
            if 'noindex' in m.group(1) or m.group(0) == ZIEL: continue
            neu = s.replace(m.group(0), ZIEL, 1)
        else:
            if re.search(r'<meta[^>]+noindex', kopf): continue
            c = re.search(r'[ \t]*<link rel="canonical"[^>]*>', kopf)
            einzug = re.match(r'[ \t]*', c.group(0)).group(0)
            neu = s[:c.start()] + einzug + ZIEL + '\n' + s[c.start():]
        n += 1
        if not dry: open(pfad, 'w', encoding='utf-8').write(neu)
    print(f'{n} Seiten ' + ('würden geändert' if dry else 'geändert'))


if __name__ == '__main__':
    main()
