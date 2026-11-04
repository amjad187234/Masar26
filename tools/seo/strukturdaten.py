"""Strukturierte Daten (JSON-LD) vereinheitlichen – idempotent, ändert nur, was fehlt.

1. Artikel (BlogPosting/Article) ohne Bild oder nur mit dem Logo bekommen das Vorschaubild der Seite
   (og:image, 1200×630) – Google empfiehlt für Artikel ein aussagekräftiges Bild.
2. Firmenobjekte „Masar Werbeagentur“ (author/publisher) ohne @id bekommen
   https://masar-werbeagentur.de/#identity, damit Google/KI-Suche alles derselben Firma zuordnen.
Es werden keine Inhalte, Preise oder Bewertungen ergänzt. Geänderte Blöcke werden mit Einrückung 2 neu geschrieben.
Aufruf: python3 tools/seo/strukturdaten.py   (--dry zeigt nur, was sich ändern würde)
Läuft automatisch am Ende von snippets.py.
"""
import os, re, sys, json, glob

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
IDENTITY = 'https://masar-werbeagentur.de/#identity'
LD = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)
ARTIKEL = ('BlogPosting', 'Article', 'NewsArticle')


def typen(o):
    t = o.get('@type', [])
    return t if isinstance(t, list) else [t]


def ist_logo(u):
    if isinstance(u, list): u = u[0] if u else ''
    if isinstance(u, dict): u = u.get('url', '')
    return not u or str(u).endswith(('logo.png', 'logo.webp'))


def bearbeiten(o, og, aend):
    if isinstance(o, list):
        for x in o: bearbeiten(x, og, aend)
        return
    if not isinstance(o, dict): return
    ty = typen(o)
    if any(t in ARTIKEL for t in ty) and og and not ist_logo(og) and ist_logo(o.get('image')):
        o['image'] = og; aend.append('Artikelbild')
    for k in ('author', 'publisher', 'provider', 'brand'):
        v = o.get(k)
        if isinstance(v, dict) and str(v.get('name', '')).startswith('Masar') and not v.get('@id') \
                and any(t in ('Organization', 'LocalBusiness') for t in typen(v)):
            # @id an zweiter Stelle einfügen (nach @type)
            neu = {}
            for kk, vv in v.items():
                neu[kk] = vv
                if kk == '@type': neu['@id'] = IDENTITY
            o[k] = neu; aend.append(f'@id {k}')
    for k, v in list(o.items()):
        if isinstance(v, (dict, list)) and k not in ('author', 'publisher'): bearbeiten(v, og, aend)


def main(dry=False):
    n = 0
    for p in sorted(glob.glob(os.path.join(ROOT, '*.html')) + glob.glob(os.path.join(ROOT, '*', '*.html'))):
        rel = os.path.relpath(p, ROOT)
        if rel.startswith(('tools', 'admin', 'node_modules')): continue
        s = open(p, encoding='utf-8').read()
        if 'noindex' in s.split('</head>', 1)[0]: continue
        m = re.search(r'<meta property="og:image" content="([^"]+)"', s)
        og = m.group(1) if m else None
        alle = []

        def ersetze(mm):
            try: j = json.loads(mm.group(2))
            except ValueError: return mm.group(0)
            aend = []
            bearbeiten(j, og, aend)
            if not aend: return mm.group(0)
            alle.extend(aend)
            return mm.group(1) + '\n' + json.dumps(j, ensure_ascii=False, indent=2) + '\n' + mm.group(3)

        neu = LD.sub(ersetze, s)
        if neu != s:
            n += 1
            print(('würde ändern ' if dry else 'geändert ') + rel + ': ' + ', '.join(sorted(set(alle))))
            if not dry: open(p, 'w', encoding='utf-8').write(neu)
    print(n, 'Seiten', 'zu ändern' if dry else 'geändert')


if __name__ == '__main__':
    main('--dry' in sys.argv)
