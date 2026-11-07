"""Preisanpassung nach Wettbewerbsvergleich (Inhaber, 07.11.2026: „عدل الأسعار مثل المنافسين … اعمل المناسب“).
Leuchtbuchstaben je Buchstabe: Berlin 199 → 149 €, NRW/Hamburg 229 → 179 €
Praxis-/Kanzleischild:         Berlin 390 → 290 €, NRW/Hamburg 459 → 339 €
Erkennt das Produkt am nächstgelegenen Produktwort vor (oder direkt nach) dem Preis. Bruttowerte setzt danach tools/seo/brutto.py neu.
Einmalig. Aufruf: python3 tools/seo/preise_2026_11.py [--dry]
"""
import os, re, sys, glob
ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
DRY = '--dry' in sys.argv
NEU = {'leucht': {199: 149, 229: 179}, 'praxis': {390: 290, 459: 339}}
# Produktwörter – das letzte vor dem Preis entscheidet
WORTE = [('leucht', r'buchstab|buchst\.'), ('praxis', r'praxis|kanzlei'),
         ('x', r'vorlage|template|social|teilbeschriftung|pkw|schriftzug|fahrzeug|milchglas|sichtschutz|aktionsfolie|druckaufl|'
               r'firmenschild|acrylglas|einzelbuchstaben unbeleuchtet|neon|leuchtkast|logo|banner|folie|(?<![a-zäöü-])schild(?!er)')]
PREIS = re.compile(r'(?<![\d.,–\-])(199|229|390|459)(?=(?:,00)?(?:&nbsp;|\s| )?(?:€|EUR))')


def produkt(vor, nach):
    if re.match(r'(?:,00)?(?:&nbsp;|\s| )?€\s?(?:/|je|pro)\s?Buchst', nach): return 'leucht'
    t = re.sub(r'<[^>]+>', ' ', vor).lower()
    best, pos = None, -1
    for name, rx in WORTE:
        for m in re.finditer(rx, t):
            if m.start() > pos: best, pos = name, m.start()
    return best


def bearbeiten(s):
    log = []
    def rep(mo):
        n = int(mo.group(1)); vor = s[max(0, mo.start() - 300):mo.start()]; nach = s[mo.end():mo.end() + 25]
        if re.search(r'brutto\)?\s*$', vor[-20:]) or re.search(r'\(\s*$', vor[-3:]): return mo.group(0)
        p = produkt(vor, nach)
        neu = NEU.get(p, {}).get(n)
        if not neu: return mo.group(0)
        kurz = re.sub(r'<[^>]+>|\s+', ' ', vor)[-60:]
        log.append(f'{p} {n}→{neu}: …{kurz}')
        return str(neu)
    return PREIS.sub(rep, s), log


def main():
    claude = open(os.path.join(ROOT, 'CLAUDE.md'), encoding='utf-8').read()
    if '| Leuchtbuchstaben (je Buchstabe) | 149 € |' in claude and not DRY:
        print('Schon umgestellt – nichts zu tun.'); return
    dateien = [p for p in glob.glob(os.path.join(ROOT, '**', '*'), recursive=True)
               if os.path.isfile(p) and p.endswith(('.html', '.py', '.js', '.txt', '.md', '.php'))
               and not os.path.relpath(p, ROOT).startswith(('tools/angebot', 'node_modules', 'data', '.git', '.claude', 'docs'))
               and not p.endswith('preise_2026_11.py')]
    gesamt = 0
    for p in dateien:
        s = open(p, encoding='utf-8').read(); neu, log = bearbeiten(s)
        if neu != s:
            gesamt += len(log)
            for l in log: print(os.path.relpath(p, ROOT), '|', l)
            if not DRY: open(p, 'w', encoding='utf-8').write(neu)
    print(gesamt, 'Preise', '(Probelauf)' if DRY else 'geändert')


if __name__ == '__main__':
    main()
