"""Eine Firma, ein Datensatz: hält die Firmenangaben im JSON-LD auf allen Seiten widerspruchsfrei.

Hintergrund: Suchmaschinen und KI-Suche ordnen Angaben über die @id einer Firma zu. Steht dieselbe
Firma auf jeder Leistungsseite noch einmal mit eigenen (abweichenden) Öffnungszeiten, Gebieten und
Bildern, entstehen Widersprüche. Die vollständigen Angaben stehen deshalb nur auf der Startseite.

1. Startseite: WebSite-Knoten (#website) mit Verweis auf die Firma; Inhaber als Person mit eigener @id;
   Leistungskatalog um alle Listenpreise aus LISTENPREISE ergänzt (nur Preise, die in CLAUDE.md stehen).
2. Alle Seiten: „provider“ einer Leistung, der auf #identity zeigt, wird auf den Verweis gekürzt
   (Typ, @id, Name, URL, Telefon, Adresse) – abweichende Kopien von Öffnungszeiten, Gebiet usw. entfallen.
3. Über uns: Inhaber verweist auf dieselbe Person-@id.

Es werden keine neuen Tatsachen erfunden. Idempotent; geänderte Blöcke werden mit Einrückung 2 geschrieben.
Aufruf: python3 tools/seo/entitaet.py   (--dry zeigt nur, was sich ändern würde)
"""
import os, re, sys, json, glob

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
BASIS = 'https://masar-werbeagentur.de'
IDENTITY, WEBSITE, INHABER = BASIS + '/#identity', BASIS + '/#website', BASIS + '/#inhaber'
KARTE = 'https://maps.app.goo.gl/kZ53GHfQ9HxUvxHg8'   # Google-Unternehmensprofil (Link vom Inhaber, 27.11.2026)
LD = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)
BEHALTEN = ('@type', '@id', 'name', 'url', 'telephone', 'address')

PERSON = {'@type': 'Person', '@id': INHABER, 'name': 'Amjad Alblili', 'jobTitle': 'Inhaber, Mediengestalter',
          'worksFor': {'@id': IDENTITY}, 'knowsLanguage': ['de', 'en', 'ar', 'tr']}

WEBSITE_KNOTEN = {'@context': 'https://schema.org', '@type': 'WebSite', '@id': WEBSITE, 'url': BASIS + '/',
                  'name': 'Masar Werbeagentur', 'alternateName': 'Masar', 'inLanguage': 'de-DE',
                  'publisher': {'@id': IDENTITY}}

# Name, Seite, Netto-Preis ab (Berlin), Einheit – nur Werte aus der Preistabelle in CLAUDE.md
LISTENPREISE = [
    ('Tür- und Klingelschild', 'schilder-berlin.html', 69, None),
    ('Einzelbuchstaben', 'schilder-berlin.html', 119, None),
    ('Acrylglasschild', 'schilder-berlin.html', 240, None),
    ('Praxis- und Kanzleischild', 'praxisbeschilderung-berlin.html', 290, None),
    ('Milchglasfolie nach Maß', 'sichtschutzfolie-berlin.html', 240, None),
    ('Aktionsfolie', 'schaufenster-weihnachten-black-friday.html', 190, None),
    ('Lochfolie (je m²)', 'schaufensterbeschriftung-berlin.html', 45, 'MTK'),
    ('Mesh-Banner (je m²)', 'pvc-banner-berlin.html', 34, 'MTK'),
    ('Blockout-Banner (je m²)', 'pvc-banner-berlin.html', 42, 'MTK'),
    ('Social-Media-Betreuung (je Monat)', 'digital.html', 490, 'MON'),
    ('Textildruck: T-Shirt (ab 5 Stück)', 'textildruck-berlin.html', 15, 'C62'),
]


def angebot(name, seite, preis, einheit):
    ps = {'@type': 'UnitPriceSpecification' if einheit else 'PriceSpecification', 'minPrice': preis,
          'priceCurrency': 'EUR', 'valueAddedTaxIncluded': False}
    if einheit: ps['unitCode'] = einheit
    return {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': name, 'url': f'{BASIS}/{seite}'},
            'priceSpecification': ps}


def knoten(d):
    if isinstance(d, list): return d
    if isinstance(d, dict) and isinstance(d.get('@graph'), list): return d['@graph']
    return [d]


def kuerzen(o, aend):
    """provider/author/publisher mit #identity: nur die Verweis-Felder behalten."""
    if isinstance(o, list):
        for x in o: kuerzen(x, aend)
        return
    if not isinstance(o, dict): return
    p = o.get('provider')
    if isinstance(p, dict) and p.get('@id') == IDENTITY:
        weg = [k for k in p if k not in BEHALTEN]
        if weg:
            for k in weg: del p[k]
            aend.append('provider gekürzt')
    for v in o.values(): kuerzen(v, aend)


def startseite(d, aend):
    for o in knoten(d):
        if not isinstance(o, dict) or o.get('@id') != IDENTITY or 'hasOfferCatalog' not in o: continue
        if o.get('founder') != {'@id': INHABER} and o.get('founder') != PERSON:
            o['founder'] = PERSON; aend.append('Inhaber mit @id')
        # Dresden wird bedient (Inhaber, 27.11.2026); Kartenprofil vom Inhaber genannt
        if isinstance(o.get('areaServed'), list) and not any(x.get('name') == 'Dresden' for x in o['areaServed']):
            o['areaServed'].append({'@type': 'City', 'name': 'Dresden'}); aend.append('Dresden im Gebiet')
        if o.get('hasMap') != KARTE:
            o['hasMap'] = KARTE; aend.append('Kartenprofil')
        if isinstance(o.get('sameAs'), list) and KARTE not in o['sameAs']:
            o['sameAs'].append(KARTE); aend.append('sameAs Kartenprofil')
        liste = o['hasOfferCatalog']['itemListElement']
        namen = {a['itemOffered']['name'] for a in liste}
        for e in LISTENPREISE:
            if e[0] not in namen and os.path.exists(os.path.join(ROOT, e[1])):
                liste.append(angebot(*e)); aend.append('Katalog + ' + e[0])


def ueber_uns(d, aend):
    for o in knoten(d):
        m = o.get('mainEntity') if isinstance(o, dict) else None
        if isinstance(m, dict) and m.get('@id') == IDENTITY and m.get('founder') != {'@type': 'Person', '@id': INHABER, 'name': 'Amjad Alblili'}:
            m['founder'] = {'@type': 'Person', '@id': INHABER, 'name': 'Amjad Alblili'}; aend.append('Inhaber-Verweis')


def main():
    dry = '--dry' in sys.argv
    n = 0
    for pfad in sorted(glob.glob(os.path.join(ROOT, '*.html')) + glob.glob(os.path.join(ROOT, 'blog', '*.html'))):
        rel = os.path.relpath(pfad, ROOT)
        alt = open(pfad, encoding='utf-8').read()
        alle = []

        def ersetze(m):
            try: d = json.loads(m.group(2))
            except ValueError: return m.group(0)
            aend = []
            kuerzen(d, aend)
            if rel == 'index.html': startseite(d, aend)
            if rel == 'ueber-uns.html': ueber_uns(d, aend)
            if not aend: return m.group(0)
            alle.extend(aend)
            return m.group(1) + '\n' + json.dumps(d, ensure_ascii=False, indent=2) + '\n' + m.group(3)

        neu = LD.sub(ersetze, alt)
        if rel == 'index.html' and WEBSITE not in neu:
            m = LD.search(neu)
            block = '\n<script type="application/ld+json">\n' + json.dumps(WEBSITE_KNOTEN, ensure_ascii=False, indent=2) + '\n</script>'
            neu = neu[:m.end()] + block + neu[m.end():]
            alle.append('WebSite-Knoten')
        if neu != alt:
            n += 1
            print(f'  {rel}: {", ".join(sorted(set(alle)))}')
            if not dry: open(pfad, 'w', encoding='utf-8').write(neu)
    print(f'{n} Seiten ' + ('würden geändert' if dry else 'geändert'))


if __name__ == '__main__':
    main()
