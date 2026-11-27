"""Maschinenlesbare Dateien für KI-Assistenten – idempotent, am Ende der Pipeline.

1. preise.md        – Preisliste als reiner Text (aus dem Abschnitt „Preise“ in llms.txt, keine eigenen Zahlen).
2. llms-full.txt    – llms.txt plus der sichtbare Text der wichtigsten Seiten in einer Datei.
3. <link rel="alternate" type="text/markdown"> im <head> von Startseite, Leistungen und Über uns,
   damit Assistenten die Dateien über einen Link finden (nicht über geratene Pfade).
Es werden keine Inhalte erfunden: alles stammt aus llms.txt und den vorhandenen Seiten.
Aufruf: python3 tools/seo/ki_dateien.py
"""
import os, re, html

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
BASE = 'https://masar-werbeagentur.de/'
SEITEN = ['index.html', 'ueber-uns.html', 'leistungen.html', 'einsatzgebiete.html', 'referenzen.html',
          'werbetechnik.html', 'schilder-berlin.html', 'leuchtreklame-berlin.html', 'schaufensterbeschriftung-berlin.html',
          'schaufensterfolie-store-eroeffnung.html', 'fahrzeugbeschriftung-berlin.html', 'lkw-beschriftung-berlin.html',
          'praxisbeschilderung-berlin.html', 'kanzleischild-berlin.html', 'fensterfolie-berlin.html', 'sichtschutzfolie-berlin.html',
          'pvc-banner-berlin.html', 'textildruck-berlin.html', 'express-druck-berlin.html', 'print.html',
          'messebeschriftung-berlin.html', 'grafikdesign-berlin.html', 'webdesign-berlin.html',
          'werbetechnik-berlin-wedding.html', 'werbeagentur-nrw.html', 'werbeagentur-hamburg.html',
          'genehmigungs-check.html', 'impressum.html']
LINKS = ('<link rel="alternate" type="text/markdown" href="/llms.txt" title="Masar Werbeagentur – Überblick für KI-Assistenten">\n'
         '<link rel="alternate" type="text/markdown" href="/preise.md" title="Masar Werbeagentur – Preisliste als Text">\n'
         '<link rel="alternate" type="text/plain" href="/llms-full.txt" title="Masar Werbeagentur – alle Kerninhalte in einer Datei">\n')
KOPF_SEITEN = ['index.html', 'leistungen.html', 'ueber-uns.html']


def lies(p):
    return open(os.path.join(ROOT, p), encoding='utf-8').read()


def schreibe(p, s):
    ziel = os.path.join(ROOT, p)
    alt = open(ziel, encoding='utf-8').read() if os.path.exists(ziel) else None
    if alt != s:
        open(ziel, 'w', encoding='utf-8').write(s)
        print('geschrieben', p)


def text(seite):
    s = lies(seite)
    titel = html.unescape(re.search(r'<title>(.*?)</title>', s, re.S).group(1)).strip()
    m = re.search(r'<main\b.*?</main>', s, re.S)
    b = m.group(0) if m else re.search(r'<body.*?</body>', s, re.S).group(0)
    b = re.sub(r'<!--.*?-->', '', b, flags=re.S)
    for tag in ('script', 'style', 'nav', 'header', 'footer', 'form', 'svg', 'noscript', 'select', 'button', 'picture', 'video', 'details'):
        b = re.sub(rf'<{tag}\b.*?</{tag}>', ' ', b, flags=re.S)
    b = re.sub(r'<h1[^>]*>(.*?)</h1>', lambda m: '\n\n### ' + m.group(1) + '\n\n', b, flags=re.S)
    b = re.sub(r'<h[23][^>]*>(.*?)</h[23]>', lambda m: '\n\n#### ' + m.group(1) + '\n\n', b, flags=re.S)
    b = re.sub(r'<h[456][^>]*>(.*?)</h[456]>', lambda m: '\n\n**' + m.group(1).strip() + '**\n\n', b, flags=re.S)
    b = re.sub(r'<li[^>]*>', '\n- ', b)
    b = re.sub(r'</(p|div|section|tr|ul|ol|table|dd|dt)>', '\n', b)
    b = re.sub(r'<br\s*/?>', '\n', b)
    b = html.unescape(re.sub(r'<[^>]+>', ' ', b)).replace('\xa0', ' ')
    zeilen, aus = [re.sub(r'[ \t]+', ' ', z).strip() for z in b.split('\n')], []
    for z in zeilen:
        if not z:
            if aus and aus[-1] != '': aus.append('')
            continue
        if len(z) < 3 or z in ('→', '✦', '-'): continue
        if aus and z == aus[-1]: continue
        aus.append(z)
    return titel, '\n'.join(aus).strip()


def main():
    llms = lies('llms.txt')
    kopf = llms.split('\n## ', 1)[0].rstrip()
    m = re.search(r'\n(## Preise.*?)(?=\n## )', llms, re.S)
    preise = ('# Preise – Masar Werbeagentur\n\n'
              'Masar Werbeagentur, Bristolstraße 19E, 13349 Berlin · Telefon/WhatsApp 0178 514 3918 · info@masar-werbeagentur.de\n'
              'Quelle und aktuelle Fassung: https://masar-werbeagentur.de/leistungen.html\n\n'
              + m.group(1).strip() + '\n\n'
              '## Hinweise\n\n'
              '- „ab“-Preise sind Einstiegspreise; das verbindliche Angebot ist ein Festpreis nach Fotos oder Aufmaß, Entwurf inklusive.\n'
              '- Anfrage: https://masar-werbeagentur.de/#kontakt · kostenlose Beratung: https://masar-werbeagentur.de/termin.html\n')
    schreibe('preise.md', preise)
    teile = [kopf, '', m.group(1).strip(), '',
             '## Inhalte der wichtigsten Seiten', '',
             'Der folgende Text ist der sichtbare Inhalt der Seiten von masar-werbeagentur.de, zusammengefasst in einer Datei.', '']
    for seite in SEITEN:
        if not os.path.exists(os.path.join(ROOT, seite)): continue
        titel, t = text(seite)
        url = BASE + ('' if seite == 'index.html' else seite)
        teile += ['---', '', f'## {titel}', '', f'URL: {url}', '', t, '']
    schreibe('llms-full.txt', '\n'.join(teile).rstrip() + '\n')
    # Verweis in llms.txt
    hinweis = ('- Maschinenlesbar: Preisliste als Text https://masar-werbeagentur.de/preise.md · '
               'alle Kerninhalte in einer Datei https://masar-werbeagentur.de/llms-full.txt')
    if 'llms-full.txt' not in llms:
        anker = '\n\n## Preise'
        llms = llms.replace(anker, '\n' + hinweis + anker, 1)
        schreibe('llms.txt', llms)
    for seite in KOPF_SEITEN:
        s = lies(seite)
        if 'href="/llms.txt"' in s: continue
        s = s.replace('</head>', LINKS + '</head>', 1)
        schreibe(seite, s)


if __name__ == '__main__':
    main()
