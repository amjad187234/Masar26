"""Baut den Anfrage-Assistenten (assistent.js) in den Kontaktbereich von Leistungsseiten ein.
Das bisherige Formular bleibt erhalten – eingeklappt unter „Lieber das klassische Formular?“.
Idempotent (Marker data-as-inject). Aufruf: python3 add_assistent.py [--dry]"""
import re, sys, os, html
import os as _os
ROOT = _os.environ.get('MASAR_ROOT', _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))).rstrip('/') + '/'
CITY = {'koeln': 'Köln', 'duesseldorf': 'Düsseldorf', 'dortmund': 'Dortmund', 'essen': 'Essen', 'bochum': 'Bochum'}

# Datei → (data-start, nrw?, ort)
M = {
 'schilder-berlin.html': ('schild:0', 0, ''), 'leuchtreklame-berlin.html': ('schild:1', 0, ''),
 'praxisbeschilderung-berlin.html': ('schild:3', 0, ''), 'kanzleischild-berlin.html': ('schild:3', 0, ''),
 'aussenwerbung-berlin.html': ('schild', 0, ''), 'werbetechnik.html': ('', 0, ''),
 'schaufensterbeschriftung-berlin.html': ('schaufenster', 0, ''), 'fahrzeugbeschriftung-berlin.html': ('fahrzeug', 0, ''),
 'lkw-beschriftung-berlin.html': ('fahrzeug:2', 0, ''), 'sonnenschutzfolie-berlin.html': ('fensterfolie:0', 0, ''),
 'sichtschutzfolie-berlin.html': ('fensterfolie:1', 0, ''), 'sicherheitsfolie-berlin.html': ('fensterfolie:2', 0, ''),
 'pvc-banner-berlin.html': ('druck:1', 0, ''), 'foliendruck-berlin.html': ('druck:2', 0, ''), 'print.html': ('druck:0', 0, ''),
 'express-druck-berlin.html': ('druck:4', 0, ''), 'messebeschriftung-berlin.html': ('messe:1', 0, ''),
 'grafikdesign-berlin.html': ('design:0', 0, ''), 'digital-signage-berlin.html': ('design:2', 0, ''),
 'webdesign-berlin.html': ('web:0', 0, ''), 'digital.html': ('web:3', 0, ''),
 'werbetechnik-potsdam.html': ('', 0, 'Potsdam'), 'werbetechnik-brandenburg.html': ('', 0, ''), 'werbetechnik-berlin-wedding.html': ('', 0, 'Berlin-Wedding'),
 # NRW
 'werbeagentur-nrw.html': ('', 1, ''), 'leuchtreklame-nrw.html': ('schild:1', 1, ''), 'schilder-nrw.html': ('schild:0', 1, ''),
 'schaufensterbeschriftung-nrw.html': ('schaufenster', 1, ''), 'fensterfolie-nrw.html': ('fensterfolie', 1, ''),
 'webdesign-nrw.html': ('web:0', 1, ''), 'fahrzeugbeschriftung-nrw.html': ('fahrzeug', 1, ''), 'lkw-beschriftung-nrw.html': ('fahrzeug:2', 1, ''),
 'pvc-banner-nrw.html': ('druck:1', 1, ''),
}
for k, v in CITY.items():
    M[f'werbeagentur-{k}.html'] = ('', 1, v)
    for svc, st in [('leuchtreklame', 'schild:1'), ('schilder', 'schild:0'), ('schaufensterbeschriftung', 'schaufenster'), ('fensterfolie', 'fensterfolie')]:
        M[f'{svc}-{k}.html'] = (st, 1, v)

def inject(f, start, nrw, ort, dry=False):
    p = ROOT + f
    if not os.path.exists(p): return 'fehlt'
    s = open(p, encoding='utf-8').read()
    if 'data-as-inject' in s: return 'schon'
    m = re.search(r'<(?:section|div)[^>]*id="kontakt"[^>]*>', s)
    if not m: return 'kein #kontakt'
    fm = re.search(r'<form[^>]*action="/kontakt\.php".*?</form>', s[m.end():], re.S)
    if not fm: return 'kein Formular'
    fs, fe = m.end() + fm.start(), m.end() + fm.end()
    # Behälter des Formulars (form-wrap / ähnliches) – Assistent davor setzen
    before = s[m.end():fs]
    wrap = None
    for wm in re.finditer(r'<div class="(form-wrap|contact-form|cf-wrap|form-card|cform)[^"]*"[^>]*>', before):
        wrap = wm
    attrs = ' data-assistent data-as-inject="1"' + (f' data-start="{start}"' if start else '') + (' data-region="nrw"' if nrw else '') + (f' data-ort="{html.escape(ort)}"' if ort else '')
    box = f'<div{attrs} style="margin-bottom:1.4rem"></div>\n'
    det_a = '<details class="as-classic" style="margin-top:.4rem"><summary style="cursor:pointer;font-weight:700;color:var(--teal-ink,#177567);padding:.6rem 0">Lieber das klassische Formular?</summary>\n'
    det_b = '\n</details>'
    ins_at = m.end() + wrap.start() if wrap else fs
    s2 = s[:ins_at] + box + s[ins_at:fs] + det_a + s[fs:fe] + det_b + s[fe:]
    if 'assistent.js' not in s2:
        s2 = s2.replace('</body>', '<script src="/assistent.js?v=7" defer></script>\n</body>', 1)
    if not dry: open(p, 'w', encoding='utf-8').write(s2)
    return 'ok' + (' (wrap)' if wrap else ' (direkt)')

if __name__ == '__main__':
    dry = '--dry' in sys.argv
    for f, (st, n, o) in M.items():
        print(f.ljust(42), inject(f, st, n, o, dry))
