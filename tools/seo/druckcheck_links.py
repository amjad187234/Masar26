"""Verlinkt die kostenlosen Werkzeuge von passenden Seiten aus: Druckdaten-Check (druckdaten-check.html)
und Leuchtbuchstaben-Konfigurator (leuchtbuchstaben-konfigurator.html, Marker konfig-hinweis).
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


KA, KZ = '<!-- konfig-hinweis -->', '<!-- /konfig-hinweis -->'
K_SEITEN = ['leuchtreklame-berlin.html', 'leuchtreklame-nrw.html', 'schilder-berlin.html', 'schilder-nrw.html', 'schaufensterbeschriftung-berlin.html',
            'aussenwerbung-berlin.html', 'werbetechnik.html', 'praxisbeschilderung-berlin.html', 'kanzleischild-berlin.html',
            'leuchtreklame-koeln.html', 'leuchtreklame-duesseldorf.html', 'leuchtreklame-dortmund.html', 'leuchtreklame-essen.html', 'leuchtreklame-bochum.html']
K_BLOG = ['blog/leuchtreklame-strom-betriebszeiten.html', 'blog/aussenwerbung-berlin-ratgeber.html']
K_ICON = ('<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
          'stroke-linejoin="round" aria-hidden="true" focusable="false" style="flex:none;color:#177567"><path d="M4 20 9 4h2l5 16"/><path d="M6.2 13h7.6"/><path d="M17 8h3v12"/></svg>')


def kbox(wrap):
    inner = (f'<p style="margin:0;display:flex;gap:.8rem;align-items:flex-start;background:#f4f7f7;border:1px solid #e0eaea;border-left:4px solid #58d0bd;'
             f'border-radius:10px;padding:1rem 1.2rem;font-size:15.5px;line-height:1.6;color:#1a2a2a">{K_ICON}<span><strong>Wie wirkt Ihr Schild an der Fassade?</strong> '
             f'Planen Sie es im <a href="/leuchtbuchstaben-konfigurator.html" style="color:#177567;font-weight:700">kostenlosen Konfigurator</a> – '
             f'Schrift, Farben, Größe und Lesbarkeit, mit Vorschau bei Tag und Nacht, auch auf Ihrem eigenen Foto.</span></p>')
    if wrap:
        return f'{KA}\n<div class="konfig-hinweis" style="max-width:1100px;margin:2rem auto;padding:0 16px;box-sizing:border-box">{inner}</div>\n{KZ}\n'
    return f'{KA}\n    <div class="konfig-hinweis" style="margin:2rem 0">{inner}</div>\n    {KZ}\n    '


def einsetzen(paare, A, Z, boxf):
    n = 0
    for f, wrap, ziel in paare:
        p = os.path.join(ROOT, f)
        if not os.path.exists(p): continue
        s = open(p, encoding='utf-8').read(); alt = s
        b = boxf(wrap)
        s, k = re.subn(re.escape(A) + r'.*?' + re.escape(Z) + r'\n(?:    )?', lambda m: b, s, count=1, flags=re.S)
        if not k:
            i = s.find(ziel)
            if i < 0 and wrap: i = s.find('<section class="mk-contact" id="kontakt"')
            if i < 0 and wrap:
                m = re.search(r'<(section|div)[^>]*id="kontakt"', s); i = m.start() if m else -1
            if i < 0: print('kein Ziel:', f); continue
            s = s[:i] + b + s[i:]
        if s != alt: open(p, 'w', encoding='utf-8').write(s); n += 1
    return n


def main_konfig():
    n = einsetzen([(f, True, '<section class="section" id="kontakt"') for f in K_SEITEN] + [(f, False, '<div class="article-cta"') for f in K_BLOG], KA, KZ, kbox)
    print(n, 'Seiten verlinken den Konfigurator')


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
    main_konfig()


if __name__ == '__main__':
    main()
