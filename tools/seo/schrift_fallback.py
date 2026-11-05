"""Ausweichschriften mit angepassten Maßen gegen Layout-Sprünge beim Laden der Webfonts (CLS).
Bis Barlow/Barlow Condensed geladen sind, zeigt der Browser Arial mit size-adjust/ascent-override – Zeilen und
Umbrüche bleiben fast gleich. Werte berechnet mit fontTools (Breite eines deutschen Mustertextes, hhea-Metriken)
gegen Liberation Sans (metrisch gleich Arial): Barlow 400 → 94,4 %, Barlow Condensed 900 → 76,9 % (05.11.2026).
1. @font-face 'Barlow Fallback' und 'Barlow Condensed Fallback' in fonts.css (Marker).
2. In allen HTML/CSS-Dateien die Fallback-Familie direkt hinter 'Barlow' bzw. 'Barlow Condensed' einsetzen. Idempotent.
Aufruf: python3 tools/seo/schrift_fallback.py
"""
import os, re
ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))).rstrip('/')
OHNE = ('.git', '.claude', 'node_modules', 'tools', 'admin', 'data', 'uploads')
A, Z = '/* fallback:start */', '/* fallback:ende */'
FACES = (A + "\n@font-face{font-family:'Barlow Fallback';src:local('Arial'),local('ArialMT'),local('Liberation Sans'),local('Helvetica');"
         "size-adjust:94.4%;ascent-override:105.9%;descent-override:21.2%;line-gap-override:0%}\n"
         "@font-face{font-family:'Barlow Condensed Fallback';src:local('Arial Bold'),local('Arial-BoldMT'),local('Liberation Sans Bold'),local('Arial');"
         "font-weight:100 900;size-adjust:76.9%;ascent-override:130%;descent-override:26%;line-gap-override:0%}\n" + Z)
FB = {'barlow': "'Barlow Fallback'", 'barlow condensed': "'Barlow Condensed Fallback'"}


def liste(v):
    """Fallback hinter Barlow/Barlow Condensed in einer font-family-Liste einsetzen (einzelne Namen = @font-face, bleiben)."""
    teile = [t for t in v.split(',')]
    namen = [t.strip().strip('\'"').lower() for t in teile]
    if len(teile) < 2: return v
    out = []
    for i, t in enumerate(teile):
        out.append(t)
        n = namen[i]
        if n in FB:
            nxt = namen[i + 1] if i + 1 < len(namen) else ''
            if nxt != n + ' fallback': out.append(FB[n])
    return ','.join(out)


def css(s):
    return re.sub(r"(font-family\s*:\s*)([^;}<>]*)", lambda m: m.group(1) + liste(m.group(2)), s)


def html(s):
    s = re.sub(r'(<style\b[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + css(m.group(2)) + m.group(3), s, flags=re.S)
    return re.sub(r'(style=")([^"]*)(")', lambda m: m.group(1) + css(m.group(2)) + m.group(3), s)


def main():
    n = 0
    f = os.path.join(ROOT, 'fonts.css'); s = open(f, encoding='utf-8').read()
    neu = re.sub(re.escape(A) + r'.*?' + re.escape(Z), lambda m: FACES, s, flags=re.S) if A in s else s.rstrip('\n') + '\n\n' + FACES + '\n'
    if neu != s: open(f, 'w', encoding='utf-8').write(neu); n += 1
    for d, ds, fs in os.walk(ROOT):
        rel = os.path.relpath(d, ROOT)
        if rel != '.' and rel.split(os.sep)[0] in OHNE: ds[:] = []; continue
        for name in fs:
            if not name.endswith(('.html', '.css')) or name == 'fonts.css': continue
            p = os.path.join(d, name); s = open(p, encoding='utf-8').read()
            neu = css(s) if name.endswith('.css') else html(s)
            if neu != s: open(p, 'w', encoding='utf-8').write(neu); n += 1
    print(n, 'Dateien mit Ausweichschrift')


if __name__ == '__main__':
    main()
