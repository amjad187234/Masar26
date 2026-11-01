"""Rechenbeispiele für gängige Bannergrößen auf den Banner-Seiten (Berlin/NRW), berechnet nur aus den
Listenpreisen (m²-Preis, Mindestpreis). Idempotent (Marker), nach banner_pages.py ausführen.
Aufruf: python3 tools/seo/banner_beispiele.py
"""
import os, re

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
A, Z = '<!-- banner-beispiele:start -->', '<!-- banner-beispiele:ende -->'
SEITEN = {'pvc-banner-berlin.html': (19, 22, 39), 'pvc-banner-nrw.html': (22, 25, 49)}
GROESSEN = [('PVC-Banner', '200 × 100 cm', 2.0, 'pvc'), ('PVC-Banner', '300 × 100 cm', 3.0, 'pvc'),
            ('PVC-Banner', '500 × 100 cm', 5.0, 'pvc'), ('Mesh-Banner (Bauzaun)', '340 × 173 cm', 3.4 * 1.73, 'mesh')]


def eur(v):
    return f'{v:,.0f}'.replace(',', '.') + '&nbsp;€'


def block(pvc, mesh, mind):
    karten = ''
    for art, mass, m2, typ in GROESSEN:
        preis = max(round(m2 * (pvc if typ == 'pvc' else mesh)), mind)
        karten += (f'<div style="background:#fff;border:1px solid var(--border,#e0eaea);border-radius:10px;padding:.8rem 1rem">'
                   f'<div style="font-size:13px;color:var(--muted,#5a7070)">{art}</div><div style="font-weight:700;color:var(--navy,#132e50)">{mass}</div>'
                   f'<div style="font-family:\'Barlow Condensed\',sans-serif;font-weight:800;font-size:1.35rem;color:var(--teal-ink,#177567)">ab {eur(preis)}</div></div>')
    return (f'{A}<h3 style="margin-top:2rem">Rechenbeispiele</h3>'
            f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:.7rem;margin:.8rem 0">{karten}</div>'
            f'<p class="price-note">Netto, berechnet aus dem m²-Preis inklusive Saum und Ösen, ohne Gestaltung und Montage. Mindestpreis je Banner {eur(mind)}.</p>{Z}')


def main():
    n = 0
    for f, (pvc, mesh, mind) in SEITEN.items():
        p = os.path.join(ROOT, f)
        if not os.path.exists(p): continue
        s = open(p, encoding='utf-8').read()
        s = re.sub(re.escape(A) + r'.*?' + re.escape(Z), '', s, flags=re.S)
        m = re.search(r'<p class="price-note">.*?</p>', s, re.S)
        if not m: print('kein price-note:', f); continue
        s = s[:m.end()] + block(pvc, mesh, mind) + s[m.end():]
        open(p, 'w', encoding='utf-8').write(s); n += 1
    print(n, 'Banner-Seiten mit Rechenbeispielen')


if __name__ == '__main__':
    main()
