"""„Aus unserer Arbeit“: drei echte Projektfotos je Leistungsseite (Vertrauenssignal, wie bei den Marktführern).
Nur Fotos und Bildunterschriften aus referenzen.html. Idempotent (Marker), erzeugt 480-px-Vorschaubilder.
Aufruf: python3 tools/seo/referenzen_einbau.py
"""
import os, re
from PIL import Image

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
A, Z = '<!-- referenzen:start -->', '<!-- referenzen:ende -->'
LR = [('leuchtreklame-berlin-08', 'Leuchtreklame, montiert am Eröffnungstag'), ('leuchtreklame-berlin-09', 'Fassadenschrift über einem Ladengeschäft'), ('leuchtreklame-berlin-04', 'Zweisprachige Anlage, deutsch und arabisch')]
FZ = [('fahrzeugbeschriftung-berlin-04', 'Transporter mit Seitenbeschriftung, fertig'), ('fahrzeugfolierung-berlin-01', 'Vollfolierung eines Imbisswagens'), ('fahrzeugbeschriftung-berlin-01', 'Folie wird auf die Schiebetür aufgezogen')]
MIX = [('leuchtreklame-berlin-08', 'Leuchtreklame am Eröffnungstag'), ('fahrzeugbeschriftung-berlin-04', 'Transporter mit Seitenbeschriftung'), ('schaufensterbeschriftung-showroom-berlin-02', 'Schaufensterbeschriftung für LAUFEN Berlin Gallery')]
SEITEN = {
    'leuchtreklame-berlin.html': ('Leuchtreklame aus unserer Werkstatt', LR),
    'aussenwerbung-berlin.html': ('Außenwerbung aus unserer Werkstatt', LR),
    'fahrzeugbeschriftung-berlin.html': ('Fahrzeugbeschriftung aus unserer Werkstatt', FZ),
    'lkw-beschriftung-berlin.html': ('Fahrzeuge aus unserer Werkstatt', FZ),
    'werbetechnik.html': ('Werbetechnik aus unserer Werkstatt', MIX),
    'werbeagentur-nrw.html': ('Beispiele aus unserer Werkstatt in Berlin', MIX),
    'werbeagentur-hamburg.html': ('Beispiele aus unserer Werkstatt in Berlin', MIX),
    'leuchtreklame-nrw.html': ('Leuchtreklame aus unserer Werkstatt in Berlin', LR),
    'fahrzeugbeschriftung-nrw.html': ('Fahrzeuge aus unserer Werkstatt in Berlin', FZ),
}


def vorschau(name):
    src = os.path.join(ROOT, 'referenzen', name + '.webp'); dst = os.path.join(ROOT, 'referenzen', name + '-480.webp')
    if not os.path.exists(dst):
        im = Image.open(src).convert('RGB'); im.thumbnail((480, 480)); im.save(dst, quality=80, method=6)
    w, h = Image.open(dst).size
    return f'/referenzen/{name}-480.webp', w, h


def block(titel, bilder):
    karten = ''
    for name, cap in bilder:
        url, w, h = vorschau(name)
        karten += (f'<figure style="margin:0;background:#fff;border:1px solid var(--border,#e0eaea);border-radius:12px;overflow:hidden">'
                   f'<a href="/referenzen.html" style="display:block"><img src="{url}" width="{w}" height="{h}" alt="{cap}" loading="lazy" style="width:100%;aspect-ratio:4/3;object-fit:cover;display:block"></a>'
                   f'<figcaption style="padding:.7rem .9rem;font-size:14px;color:var(--muted,#5a7070);line-height:1.5">{cap}</figcaption></figure>')
    return (f'{A}\n<section class="section" id="arbeiten" style="padding:3rem 0">\n  <div class="container">\n'
            f'    <div class="sec-head reveal" style="margin-bottom:1.2rem;text-align:center"><span class="eyebrow">Aus unserer Arbeit</span>'
            f'<h2 class="sec-title" style="font-size:clamp(1.5rem,3vw,2.2rem);">{titel}</h2></div>\n'
            f'    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1rem;max-width:1000px;margin:0 auto">{karten}</div>\n'
            f'    <p style="text-align:center;margin-top:1.2rem"><a href="/referenzen.html" style="color:var(--teal-ink,#177567);font-weight:700">Alle Referenzen ansehen →</a></p>\n'
            f'  </div>\n</section>\n{Z}\n')


def main():
    n = 0
    for f, (titel, bilder) in SEITEN.items():
        p = os.path.join(ROOT, f)
        if not os.path.exists(p): continue
        s = open(p, encoding='utf-8').read()
        s = re.sub(re.escape(A) + r'.*?' + re.escape(Z) + r'\n?', '', s, flags=re.S)
        for anker in ['<!-- lokal:start -->', '<!-- CONTACT -->']:
            if anker in s:
                i = s.index(anker); break
        else:
            m = re.search(r'<(section|div)[^>]*id="kontakt"', s)
            if not m: print('kein Anker:', f); continue
            i = m.start()
        s = s[:i] + block(titel, bilder) + s[i:]
        open(p, 'w', encoding='utf-8').write(s); n += 1
    print(n, 'Seiten mit Referenzen')


if __name__ == '__main__':
    main()
