"""Banner-Preise B2B (Freigabe Inhaber 03.11.2026) auf Website, Generatoren und Assistent setzen.
Berlin/Brandenburg: PVC 29 · Mesh 34 · Blockout 42 €/m² · Mindestpreis 79 €
NRW/Hamburg:        PVC 34 · Mesh 39 · Blockout 48 €/m² · Mindestpreis 89 €  (gleiche Staffel wie bisher, nach Marktrecherche)
Erkennt das Produkt am Wort davor (Mesh/Blockout, sonst PVC). Idempotent. Aufruf: python3 tools/seo/bannerpreise.py [--dry]
"""
import os, re, sys, glob

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
MAP = {'pvc': {19: 29, 22: 34}, 'mesh': {22: 34, 25: 39}, 'blockout': {29: 42, 33: 48}}
MIND = {39: 79, 49: 89}
QM = re.compile(r'(?<![\d,.])(19|22|25|29|33)((?:,00)?(?:&nbsp;|\s)?(?:€|EUR)\s?(?:/\s?m²|pro m²))')
DRY = '--dry' in sys.argv


def produkt(vor):
    v = vor.lower(); m, b, p = v.rfind('mesh'), v.rfind('blockout'), v.rfind('pvc')
    if max(m, b) > p and max(m, b) >= 0:
        return 'mesh' if m > b else 'blockout'
    return 'pvc'


def bearbeiten(s, datei):
    aenderungen = []
    def qm(mo):
        wert = int(mo.group(1)); vor = s[max(0, mo.start() - 200):mo.start()]
        if 'banner' not in vor.lower() and 'mesh' not in vor.lower() and 'pvc' not in vor.lower() and 'kopf-preis' not in vor and 'data-label' not in vor and "'ab " not in vor[-6:]:
            return mo.group(0)          # kein Banner-Zusammenhang (z. B. Lochfolie)
        pr = produkt(vor); neu = MAP[pr].get(wert) or MAP['pvc'].get(wert)
        if not neu: return mo.group(0)
        aenderungen.append(f'{pr} {wert}→{neu}: …{vor[-45:]}')
        return f'{neu}{mo.group(2)}'
    s = QM.sub(qm, s)
    def mind(mo):
        neu = MIND[int(mo.group(2))]; aenderungen.append(f'Mindestpreis {mo.group(2)}→{neu}')
        return f'{mo.group(1)}{neu}'
    s = re.sub(r'(Mindestpreis(?: je Banner(?: liegt bei)?)? )(39|49)(?= ?€)', mind, s)
    s = re.sub(r'(Mindestpreis je Banner</td><td[^>]*>[^<]*</td><td[^>]*><strong>ab )(39|49)(?=&nbsp;€)', mind, s)
    # Generatoren / Assistent
    for alt, neu in [('rows(19, 22, 29, 39)', 'rows(29, 34, 42, 79)'), ('rows(22, 25, 33, 49)', 'rows(34, 39, 48, 89)'),
                     ("'PVC-Banner', '/pvc-banner-berlin.html', 19,", "'PVC-Banner', '/pvc-banner-berlin.html', 29,"),
                     ("'PVC-Banner', 22, ' / m²'", "'PVC-Banner', 34, ' / m²'"),
                     ('| PVC-Banner (m²) | 19 € | 22 € |', '| PVC-Banner (m²) | 29 € | 34 € |'), ('| Mesh-Banner (m²) | 22 € | 25 € |', '| Mesh-Banner (m²) | 34 € | 39 € |'),
                     ('| Blockout-Banner (m²) | 29 € | 33 € |', '| Blockout-Banner (m²) | 42 € | 48 € |'), ('| Banner-Mindestpreis | 39 € | 49 € |', '| Banner-Mindestpreis | 79 € | 89 € |')]:
        if alt in s: s = s.replace(alt, neu); aenderungen.append(f'{alt} → {neu}')
    return s, aenderungen


def main():
    if '| PVC-Banner (m²) | 29 € | 34 € |' in open(os.path.join(ROOT, 'CLAUDE.md'), encoding='utf-8').read() and not DRY:
        print('Neue Preise sind schon gesetzt – nichts zu tun (Skript nur einmal ausführen).'); return
    dateien = [p for p in glob.glob(os.path.join(ROOT, '**', '*'), recursive=True)
               if os.path.isfile(p) and p.endswith(('.html', '.py', '.js', '.txt', '.md'))
               and not os.path.relpath(p, ROOT).startswith(('tools/angebot', 'node_modules', 'data', '.git'))
               and not p.endswith('bannerpreise.py')]
    gesamt = 0
    for p in dateien:
        s = open(p, encoding='utf-8').read()
        neu, ae = bearbeiten(s, p)
        if neu != s:
            gesamt += len(ae)
            if DRY:
                print('##', os.path.relpath(p, ROOT)); [print('  ', a) for a in ae]
            else:
                open(p, 'w', encoding='utf-8').write(neu)
    print(gesamt, 'Preisstellen', '(Probelauf)' if DRY else 'geändert')


if __name__ == '__main__':
    main()
