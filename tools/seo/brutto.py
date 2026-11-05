"""Bruttopreise neben die Netto-Preise setzen (Inhaber, 05.11.2026 – seit Privatkunden dazugehören, PAngV § 3: Gesamtpreis nennen).
Aus „ab 45 € netto“ wird „ab 45 € netto <span class="brutto">(53,55 € brutto)</span>“.
Erfasst: Preise mit „ab“ oder mit „netto“ (inkl. Einheiten wie /m², je Buchstabe, pro Monat, für 10 Stück) im sichtbaren Text.
Nicht erfasst: <head>, Skripte, Styles, Attribute, Spannen ohne „ab“/„netto“, „statt …“-Preise, Preise mit „inkl.“ oder „/h“.
Idempotent: vorhandene Brutto-Angaben werden entfernt und neu berechnet. Aufruf: python3 tools/seo/brutto.py [--dry]
"""
import os, re, sys
from decimal import Decimal, ROUND_HALF_UP
ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))).rstrip('/')
OHNE = ('.git', '.claude', 'node_modules', 'tools', 'admin', 'docs', 'data', 'uploads')
MWST = Decimal('1.19')
SP = r'(?:\s|&nbsp;| |&#8239;| )'
NUM = r'\d{1,3}(?:\.\d{3})*(?:,\d{2})?'
EINH = (rf'(?:{SP}?/{SP}?(?:m²|Monat|Buchstabe|Buchst\.|Stück|Fahrzeug)'
        rf'|{SP}(?:pro|je){SP}(?:m²|Monat|Buchstabe|Stück|Fahrzeug|Motiv|Seite)'
        rf'|{SP}für{SP}\d+{SP}Stück)?')
TOK = re.compile(rf'(?<![\d.,])(?:(?P<ab>[Aa]b){SP})?(?P<n>{NUM}){SP}?€(?P<e>{EINH})(?P<net>,?{SP}netto)?(?P<z>{SP}?zzgl\.{SP}?(?:19{SP}?%{SP}?)?(?:MwSt\.?|Umsatzsteuer))?'
                 rf'(?!{SP}?(?:/{SP}?(?:h\b|Std)|inkl|brutto|Brutto|einzeln))')
SPAN = re.compile(r' ?<span class="brutto">\([^<]*\)</span>')
CSS = ('<style id="brutto-css">.brutto{font-size:.8em;font-weight:600;white-space:nowrap}'
       '.price-val .brutto,.ph-stat-num .brutto,.stat-num .brutto,.pkg-price .brutto,.price .brutto{display:block;font-size:clamp(13px,.4em,17px);margin-top:.15rem}</style>')


def euro(d):
    d = d.quantize(Decimal('0.01'), ROUND_HALF_UP)
    ganz, cent = f'{d:.2f}'.split('.')
    ganz = f'{int(ganz):,}'.replace(',', '.')
    return ganz if cent == '00' else f'{ganz},{cent}'


def text_ersetzen(t, davor):
    def f(m):
        if not (m.group('ab') or m.group('net')): return m.group(0)
        if re.search(r'statt\s*$', davor + t[:m.start()][-12:]): return m.group(0)
        n = Decimal(m.group('n').replace('.', '').replace(',', '.'))
        return m.group(0) + f' <span class="brutto">({euro(n * MWST)}&nbsp;€ brutto)</span>'
    return TOK.sub(f, t)


def bearbeiten(s):
    s = SPAN.sub('', s)
    schutz = []
    def weg(m): schutz.append(m.group(0)); return f'\x00{len(schutz) - 1}\x00'
    s = re.sub(r'<head\b.*?</head>|<(script|style|textarea|title|noscript|option)\b.*?</\1>|<!--.*?-->', weg, s, flags=re.S | re.I)
    teile = re.split(r'(<[^>]+>)', s)
    out = []; davor = ''
    for t in teile:
        if t.startswith('<') or '€' not in t:
            out.append(t)
            if not t.startswith('<') and t.strip(): davor = t[-20:]
            continue
        out.append(text_ersetzen(t, davor)); davor = t[-20:]
    s = ''.join(out)
    s = re.sub(r'\x00(\d+)\x00', lambda m: schutz[int(m.group(1))], s)
    if 'class="brutto"' in s:
        if 'id="brutto-css"' in s: s = re.sub(r'<style id="brutto-css">.*?</style>', lambda m: CSS, s, count=1, flags=re.S)
        else: s = s.replace('</head>', CSS + '\n</head>', 1)
    return s


def main():
    dry = '--dry' in sys.argv; n = 0; z = 0
    for d, ds, fs in os.walk(ROOT):
        rel = os.path.relpath(d, ROOT)
        if rel != '.' and rel.split(os.sep)[0] in OHNE: ds[:] = []; continue
        for f in fs:
            if not f.endswith('.html'): continue
            p = os.path.join(d, f); s = open(p, encoding='utf-8').read()
            neu = bearbeiten(s)
            if neu != s:
                n += 1; z += neu.count('class="brutto"')
                if not dry: open(p, 'w', encoding='utf-8').write(neu)
    print(n, 'Seiten mit Bruttopreisen', f'({z} Angaben)' if n else '', '(Probelauf)' if dry else '')


if __name__ == '__main__':
    main()
