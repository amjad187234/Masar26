"""Barrierefreiheit (axe/WCAG) – seitenweite Korrekturen, idempotent:
1. Seiten, deren Hero role="main" trägt: echtes <main id="main-content"> von Hero bis vor den Footer.
2. Schwebender WhatsApp-Knopf in <aside aria-label>, Sticky-Leiste als role="complementary".
3. Footer-Überschriften h5 → h2 und .why-item h4 → h3 (gleiche Optik), damit die Überschriftenfolge stimmt.
Aufruf: python3 tools/seo/a11y.py  (nach Generatoren ausführen)
"""
import os, re, glob

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
FOOT_CSS = '<style id="a11y-fix">.foot-col h2.foot-h{font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#fff;margin:0 0 1rem;font-family:inherit;line-height:1.4}</style>'


def fix(s):
    # 1) main-Landmark
    if '<main' not in s:
        m = re.search(r'<(section|div)([^>]*?) id="main-content" role="main" tabindex="-1"([^>]*)>', s)
        if m:
            f = s.find('<footer', m.end())
            if f > 0:
                neu = f'<main id="main-content" tabindex="-1">\n<{m.group(1)}{m.group(2)}{m.group(3)}>'
                s = s[:f] + '</main>\n' + s[f:]
                s = s[:m.start()] + neu + s[m.end():]
    # 2) schwebende Elemente
    s = re.sub(r'(?<!<aside aria-label="WhatsApp">)(<a [^>]*class="wa"[^>]*>.*?</a>)', r'<aside aria-label="WhatsApp">\1</aside>', s, count=1, flags=re.S)
    s = re.sub(r'<div([^>]*) id="stickyCta"(?![^>]*role=)', r'<div\1 id="stickyCta" role="complementary" aria-label="Schnellkontakt"', s, count=1)
    # 3) Footer-Überschriften
    f = s.find('<footer')
    if f > 0 and ('<h5' in s[f:] or 'class="foot-h"' in s[f:]):
        s = s[:f] + re.sub(r'<h5(\s[^>]*)?>', lambda m: '<h2 class="foot-h"' + (m.group(1) or '') + '>', s[f:]).replace('</h5>', '</h2>')
        if 'id="a11y-fix"' not in s:
            s = s.replace('</head>', FOOT_CSS + '\n</head>', 1)
    # 4) why-item: h4 direkt unter h2 → h3 (gleiche Optik)
    if 'class="why-item' in s:
        s = re.sub(r'\.why-item h4(?!,\.why-item h3)', '.why-item h4,.why-item h3', s)
        s = re.sub(r'(<div class="why-item[^"]*">(?:(?!</div>\s*</div>).)*?)<h4([^>]*)>(.*?)</h4>', r'\1<h3\2>\3</h3>', s, flags=re.S)
    # 5) Ratgeber: verwandte Artikel h4 → h3 (unter h2 „Weitere Artikel“)
    if 'class="related-card"' in s:
        s = re.sub(r'\.related-card h4(?!,\.related-card h3)', '.related-card h4,.related-card h3', s)
        s = re.sub(r'(<(?:div|a)[^>]*class="related-card"[^>]*>\s*)<h4([^>]*)>(.*?)</h4>', r'\1<h3\2>\3</h3>', s, flags=re.S)
    # 6) Schritt-Listen (Umland-Seiten, Prozess): h4 → h3 (gleiche Optik)
    for box, sel in (('ua-steps', '.ua-steps'), ('process-steps', '.pstep')):
        if f'class="{box}' in s:
            s = re.sub(re.escape(sel) + r' h4(?!,' + re.escape(sel) + r' h3)', f'{sel} h4,{sel} h3', s)
            i = s.find(f'class="{box}')
            j = s.find('</section>', i)
            if j > i:
                s = s[:i] + re.sub(r'<h4([^>]*)>(.*?)</h4>', r'<h3\1>\2</h3>', s[i:j]) + s[j:]
    return s


def main():
    n = 0
    for p in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
        rel = os.path.relpath(p, ROOT)
        if rel.startswith(('tools/', 'admin/', 'node_modules/', 'data/')): continue
        s = open(p, encoding='utf-8').read(); t = fix(s)
        if t != s: open(p, 'w', encoding='utf-8').write(t); n += 1
    print(n, 'Seiten angepasst')


if __name__ == '__main__':
    main()
