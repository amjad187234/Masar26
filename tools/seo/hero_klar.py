"""Klarer Seitenkopf auf den wichtigsten Leistungsseiten: „ab“-Preis + drei Zusagen direkt unter dem Einleitungstext,
bei Fahrzeug und Leuchtreklame (Berlin) ein echtes Projektfoto statt Werbegrafik. Nur Listenpreise.
Idempotent (Marker). Aufruf: python3 tools/seo/hero_klar.py
"""
import os, re

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
A, Z = '<!-- kopf:start -->', '<!-- kopf:ende -->'
A2, Z2 = '<!-- kopf-zusagen:start -->', '<!-- kopf-zusagen:ende -->'
B_MONT = 'Montage durch unser Team in Berlin'
N_MONT = 'Montage durch unser Team vor Ort'
L_MONT = 'Bau und Montage durch eingetragene Partnerbetriebe'  # Leuchtreklame: zulassungspflichtiges Handwerk (HwO), siehe partner_hinweis.py
SEITEN = {
    'fahrzeugbeschriftung-berlin.html': ('ab 290 € netto', 'Teilbeschriftung · Entwurf inklusive', B_MONT),
    'leuchtreklame-berlin.html': ('ab 199 € je Buchstabe', 'LED-Neon innen ab 249 €', L_MONT),
    'schilder-berlin.html': ('ab 45 € netto', 'Firmenschild ab 149 € · Praxisschild ab 390 €', B_MONT),
    'schaufensterbeschriftung-berlin.html': ('ab 149 € netto', 'Sichtschutz ab 190 € · Lochfolie ab 45 €/m²', B_MONT),
    'fensterfolie-berlin.html': ('Sichtschutz ab 190 € netto', 'Glas wird vor der Montage geprüft', B_MONT),
    'sichtschutzfolie-berlin.html': ('ab 190 € netto', 'Milchglas nach Maß ab 240 €', B_MONT),
    'pvc-banner-berlin.html': ('ab 29 €/m² netto', 'Mesh ab 34 €/m² · Blockout ab 42 €/m²', 'Druck in Berlin-Wedding'),
    'aussenwerbung-berlin.html': ('Leuchtbuchstaben ab 199 €', 'Schilder ab 45 € · Banner ab 29 €/m²', L_MONT),
    'leuchtreklame-nrw.html': ('ab 229 € je Buchstabe', 'Werbesatzung Ihrer Stadt geprüft', L_MONT),
    'schilder-nrw.html': ('ab 59 € netto', 'Firmenschild ab 179 € · Praxisschild ab 459 €', N_MONT),
    'fahrzeugbeschriftung-nrw.html': ('ab 340 € netto', 'Teilbeschriftung · Entwurf inklusive', N_MONT),
    'schaufensterbeschriftung-nrw.html': ('ab 179 € netto', 'Sichtschutz ab 229 € · Lochfolie ab 55 €/m²', N_MONT),
    'fensterfolie-nrw.html': ('Sichtschutz ab 229 € netto', 'Glas wird vor der Montage geprüft', N_MONT),
    'pvc-banner-nrw.html': ('ab 34 €/m² netto', 'Mesh ab 39 €/m² · Blockout ab 48 €/m²', N_MONT),
}
FOTO = {
    'fahrzeugbeschriftung-berlin.html': ('fahrzeugbeschriftung-berlin-04', 'Von Masar beschrifteter Transporter mit Logo, Leistungen und Kontakt'),
    'leuchtreklame-berlin.html': ('leuchtreklame-berlin-09', 'Fassadenschrift über einem Ladengeschäft in Berlin – ein Projekt von Masar'),
}
CSS = ('<style id="kopf-klar">.kopf-preis{display:inline-flex;align-items:baseline;gap:.5rem;flex-wrap:wrap;background:rgba(88,208,189,.14);'
       'border:1px solid rgba(88,208,189,.45);border-radius:10px;padding:.55rem .9rem;margin:-.6rem 0 1rem;color:#fff;font-size:14px}'
       '.kopf-preis b{font-family:"Barlow Condensed",sans-serif;font-weight:800;font-size:1.35rem;color:#58d0bd;letter-spacing:.3px}'
       '.kopf-checks{list-style:none;margin:0 0 1.4rem;padding:0;display:grid;gap:.4rem}.hero-btns+.kopf-checks{margin-top:1.3rem}'
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
        s = re.sub(re.escape(A2) + r'.*?' + re.escape(Z2), '', s, flags=re.S)
        m = re.search(r'<p class="hero-sub">.*?</p>', s, re.S)
        if not m: print('kein hero-sub:', f); continue
        preis_blk = f'{A}<div class="kopf-preis"><b>{preis}</b><span>{zusatz}</span></div>{Z}'
        checks = (f'<ul class="kopf-checks"><li>Festpreis nach Fotos – Angebot in der Regel in 24 Stunden</li>'
                  f'<li>Entwurf inklusive, Genehmigung wird geprüft</li><li>{montage}</li></ul>')
        s = s[:m.end()] + preis_blk + s[m.end():]
        # Zusagen unter die Knöpfe (UX 04.11.2026): so liegt „Angebot anfordern“ am Handy im ersten Bildschirm
        b = re.search(r'<div class="hero-btns">.*?</div>', s, re.S)
        if b: s = s[:b.end()] + f'{A2}{checks}{Z2}' + s[b.end():]
        else: s = s.replace(preis_blk, preis_blk + f'{A2}{checks}{Z2}', 1)
        if 'id="kopf-klar"' in s:
            s = re.sub(r'<style id="kopf-klar">.*?</style>', lambda _: CSS, s, count=1, flags=re.S)
        else:
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
