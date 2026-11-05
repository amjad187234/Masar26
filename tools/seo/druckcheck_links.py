"""Verlinkt den kostenlosen Druckdaten-Check (druckdaten-check.html) von passenden Seiten aus.
Leistungsseiten: Hinweis-Kasten vor dem Kontaktbereich. Ratgeber: Kasten vor der Angebotsbox (.article-cta).
Idempotent (Marker), ersetzt den Block an seiner Stelle. Aufruf: python3 tools/seo/druckcheck_links.py
"""
import os, re
ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))).rstrip('/')
A, Z = '<!-- druckcheck-hinweis -->', '<!-- /druckcheck-hinweis -->'
SEITEN = ['print.html', 'pvc-banner-berlin.html', 'pvc-banner-nrw.html', 'foliendruck-berlin.html', 'grafikdesign-berlin.html',
          'textildruck-berlin.html', 'leistungen.html']
BLOG = ['blog/logo-dateien-werbetechnik.html', 'blog/bauzaunbanner-ratgeber.html', 'blog/arbeitskleidung-bedrucken.html']
ICON = ('<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
        'stroke-linejoin="round" aria-hidden="true" focusable="false" style="flex:none;color:#177567"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8Z"/>'
        '<path d="M14 3v5h5"/><path d="m9 15 2 2 4-4"/></svg>')


def box(wrap):
    inner = (f'<p style="margin:0;display:flex;gap:.8rem;align-items:flex-start;background:#f4f7f7;border:1px solid #e0eaea;border-left:4px solid #58d0bd;'
             f'border-radius:10px;padding:1rem 1.2rem;font-size:15.5px;line-height:1.6;color:#1a2a2a">{ICON}<span><strong>Druckdatei fertig?</strong> '
             f'Prüfen Sie sie vorher mit unserem <a href="/druckdaten-check.html" style="color:#177567;font-weight:700">kostenlosen Druckdaten-Check</a> – '
             f'Auflösung, Beschnitt, Schriften und Farben in Sekunden, ohne Upload.</span></p>')
    if wrap:
        return f'{A}\n<div class="druckcheck-hinweis" style="max-width:1100px;margin:2rem auto;padding:0 16px;box-sizing:border-box">{inner}</div>\n{Z}\n'
    return f'{A}\n    <div class="druckcheck-hinweis" style="margin:2rem 0">{inner}</div>\n    {Z}\n    '


def main():
    n = 0
    for f, wrap, ziel in [(f, True, '<section class="section" id="kontakt"') for f in SEITEN] + [(f, False, '<div class="article-cta"') for f in BLOG]:
        p = os.path.join(ROOT, f)
        if not os.path.exists(p): continue
        s = open(p, encoding='utf-8').read(); alt = s
        b = box(wrap)
        s, k = re.subn(re.escape(A) + r'.*?' + re.escape(Z) + r'\n(?:    )?', lambda m: b, s, count=1, flags=re.S)
        if not k:
            i = s.find(ziel)
            if i < 0 and wrap: i = s.find('<section class="mk-contact" id="kontakt"')
            if i < 0: print('kein Ziel:', f); continue
            s = s[:i] + b + s[i:]
        if s != alt: open(p, 'w', encoding='utf-8').write(s); n += 1
    print(n, 'Seiten verlinken den Druckdaten-Check')


if __name__ == '__main__':
    main()
