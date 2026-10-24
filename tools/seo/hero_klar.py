"""Klarer Seitenkopf auf den wichtigsten Leistungsseiten: „ab“-Preis + drei Zusagen direkt unter dem Einleitungstext,
bei Fahrzeug und Leuchtreklame (Berlin) ein echtes Projektfoto statt Werbegrafik. Nur Listenpreise.
Idempotent (Marker). Aufruf: python3 tools/seo/hero_klar.py
"""
import os, re

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
A, Z = '<!-- kopf:start -->', '<!-- kopf:ende -->'
B_MONT = 'Montage durch unser Team in Berlin'
N_MONT = 'Montage durch unser Team vor Ort'
SEITEN = {
    'fahrzeugbeschriftung-berlin.html': ('ab 290 € netto', 'Teilbeschriftung · Entwurf inklusive', B_MONT),
    'leuchtreklame-berlin.html': ('ab 199 € je Buchstabe', 'LED-Neon innen ab 249 €', B_MONT),
    'schilder-berlin.html': ('ab 45 € netto', 'Firmenschild ab 149 € · Praxisschild ab 390 €', B_MONT),
    'schaufensterbeschriftung-berlin.html': ('ab 149 € netto', 'Sichtschutz ab 190 € · Lochfolie ab 45 €/m²', B_MONT),
    'fensterfolie-berlin.html': ('Sichtschutz ab 190 € netto', 'Glas wird vor der Montage geprüft', B_MONT),
    'sichtschutzfolie-berlin.html': ('ab 190 € netto', 'Milchglas nach Maß ab 240 €', B_MONT),
    'pvc-banner-berlin.html': ('ab 19 €/m² netto', 'Mesh ab 22 €/m² · Blockout ab 29 €/m²', 'Druck in Berlin-Wedding'),
    'aussenwerbung-berlin.html': ('Leuchtbuchstaben ab 199 €', 'Schilder ab 45 € · Banner ab 19 €/m²', B_MONT),
    'leuchtreklame-nrw.html': ('ab 229 € je Buchstabe', 'Werbesatzung Ihrer Stadt geprüft', N_MONT),
    'schilder-nrw.html': ('ab 59 € netto', 'Firmenschild ab 179 € · Praxisschild ab 459 €', N_MONT),
    'fahrzeugbeschriftung-nrw.html': ('ab 340 € netto', 'Teilbeschriftung · Entwurf inklusive', N_MONT),
    'schaufensterbeschriftung-nrw.html': ('ab 179 € netto', 'Sichtschutz ab 229 € · Lochfolie ab 55 €/m²', N_MONT),
    'fensterfolie-nrw.html': ('Sichtschutz ab 229 € netto', 'Glas wird vor der Montage geprüft', N_MONT),
    'pvc-banner-nrw.html': ('ab 22 €/m² netto', 'Mesh ab 25 €/m² · Blockout ab 33 €/m²', N_MONT),
}
FOTO = {
    'fahrzeugbeschriftung-berlin.html': ('fahrzeugbeschriftung-berlin-04', 'Von Masar beschrifteter Transporter mit Logo, Leistungen und Kontakt'),
    'leuchtreklame-berlin.html': ('leuchtreklame-berlin-09', 'Von Masar montierte Fassadenschrift über einem Ladengeschäft in Berlin'),
}
CSS = ('<style id="kopf-klar">.kopf-preis{display:inline-flex;align-items:baseline;gap:.5rem;flex-wrap:wrap;background:rgba(88,208,189,.14);'
       'border:1px solid rgba(88,208,189,.45);border-radius:10px;padding:.55rem .9rem;margin:-.6rem 0 1rem;color:#fff;font-size:14px}'
       '.kopf-preis b{font-family:"Barlow Condensed",sans-serif;font-weight:800;font-size:1.35rem;color:#58d0bd;letter-spacing:.3px}'
       '.kopf-checks{list-style:none;margin:0 0 1.4rem;padding:0;display:grid;gap:.4rem}'
       '.kopf-checks li{position:relative;padding-left:1.6rem;color:rgba(255,255,255,.88);font-size:15px;line-height:1.5}'
       '.kopf-checks li::before{content:"✓";position:absolute;left:0;top:0;width:1.1rem;height:1.1rem;border-radius:50%;background:#58d0bd;color:#132e50;'
       'font-weight:900;font-size:.75rem;display:flex;align-items:center;justify-content:center;margin-top:.2rem}</style>')


def main():
    n = 0
    for f, (preis, zusatz, montage) in SEITEN.items():
        p = os.path.join(ROOT, f)
        if not os.path.exists(p): continue
        s = open(p, encoding='utf-8').read()
        s = re.sub(re.escape(A) + r'.*?' + re.escape(Z), '', s, flags=re.S)
        m = re.search(r'<p class="hero-sub">.*?</p>', s, re.S)
        if not m: print('kein hero-sub:', f); continue
        blk = (f'{A}<div class="kopf-preis"><b>{preis}</b><span>{zusatz}</span></div>'
               f'<ul class="kopf-checks"><li>Festpreis nach Fotos – Angebot in der Regel in 24 Stunden</li>'
               f'<li>Entwurf inklusive, Genehmigung wird geprüft</li><li>{montage}</li></ul>{Z}')
        s = s[:m.end()] + blk + s[m.end():]
        if 'id="kopf-klar"' not in s:
            s = s.replace('</head>', CSS + '\n</head>', 1)
        if f in FOTO:
            name, alt = FOTO[f]
            s = re.sub(r'<img class="hero-shot"[^>]*>',
                       f'<img class="hero-shot" src="/referenzen/{name}.webp" srcset="/referenzen/{name}-480.webp 480w, /referenzen/{name}.webp 1200w" '
                       f'sizes="360px" width="1080" height="1080" alt="{alt}" loading="eager" fetchpriority="high" style="aspect-ratio:1/1;object-fit:cover">', s, count=1)
        open(p, 'w', encoding='utf-8').write(s); n += 1
    print(n, 'Seiten mit klarem Kopf')


if __name__ == '__main__':
    main()
