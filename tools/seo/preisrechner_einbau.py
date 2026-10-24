"""Baut den Preisrechner (preisrechner.js) in passende Leistungsseiten ein – vor dem Kontaktbereich.
Idempotent (Marker <!-- preisrechner:start/ende -->). Aufruf: python3 tools/seo/preisrechner_einbau.py
"""
import os, re, glob

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
A, Z = '<!-- preisrechner:start -->', '<!-- preisrechner:ende -->'
SKRIPT = '<script src="/preisrechner.js?v=1" defer></script>'

SEITEN = {'pvc-banner-berlin.html': ('banner', ''), 'pvc-banner-nrw.html': ('banner', 'nrw'),
          'leuchtreklame-berlin.html': ('leuchtbuchstaben', ''), 'leuchtreklame-nrw.html': ('leuchtbuchstaben', 'nrw'),
          'schaufensterbeschriftung-berlin.html': ('lochfolie', ''), 'schaufensterbeschriftung-nrw.html': ('lochfolie', 'nrw'),
          'aussenwerbung-berlin.html': ('leuchtbuchstaben', ''), 'werbeagentur-hamburg.html': ('leuchtbuchstaben', 'hamburg'),
          'werbeagentur-nrw.html': ('leuchtbuchstaben', 'nrw'), 'preisrechner.html': ('banner', '')}
for c in ['koeln', 'duesseldorf', 'dortmund', 'essen', 'bochum']:
    SEITEN[f'leuchtreklame-{c}.html'] = ('leuchtbuchstaben', 'nrw')
    SEITEN[f'schaufensterbeschriftung-{c}.html'] = ('lochfolie', 'nrw')
    SEITEN[f'werbeagentur-{c}.html'] = ('leuchtbuchstaben', 'nrw')


def block(produkt, region):
    reg = f' data-region="{region}"' if region else ''
    return (f'{A}\n<section class="section" id="preisrechner" style="padding:3rem 0">\n  <div class="container">\n'
            f'    <div data-preisrechner data-produkt="{produkt}"{reg}></div>\n'
            f'    <noscript><p style="text-align:center">Preise und Festpreis-Angebot per WhatsApp: 0178 514 3918</p></noscript>\n'
            f'  </div>\n</section>\n{Z}\n')


def main():
    n = 0
    for f, (produkt, region) in SEITEN.items():
        p = os.path.join(ROOT, f)
        if not os.path.exists(p) or f == 'preisrechner.html': continue
        s = open(p, encoding='utf-8').read()
        s = re.sub(re.escape(A) + r'.*?' + re.escape(Z) + r'\n?', '', s, flags=re.S)
        for anker in ['<!-- lokal:start -->', '<!-- CONTACT -->', '<section class="section" id="kontakt">', '<div class="cta-strip" id="kontakt">']:
            if anker in s:
                i = s.index(anker); s = s[:i] + block(produkt, region) + s[i:]; break
        else:
            m = re.search(r'<(section|div)[^>]*id="kontakt"', s)
            if not m: print('kein Anker:', f); continue
            s = s[:m.start()] + block(produkt, region) + s[m.start():]
        if SKRIPT not in s:
            s = s.replace('</body>', SKRIPT + '\n</body>', 1)
        open(p, 'w', encoding='utf-8').write(s); n += 1
    print(n, 'Seiten mit Preisrechner')


if __name__ == '__main__':
    main()
