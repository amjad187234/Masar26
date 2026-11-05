"""Leistungserbringung offenlegen (Wunsch des Inhabers, 05.11.2026).

Masar plant, gestaltet, koordiniert und steuert Projekte. Arbeiten, für die eine Eintragung in die
Handwerksrolle oder eine besondere Qualifikation nötig ist (Bau/Montage beleuchteter Werbeanlagen –
Schilder- und Lichtreklamehersteller ist seit 14.02.2020 wieder zulassungspflichtig –, elektrische
Anschlüsse durch einen eingetragenen Elektrofachbetrieb, Montagen mit Hubarbeitsbühne, Messestandbau,
Fahrzeug-Vollfolierung), führen qualifizierte Partnerbetriebe aus. Rechtsprechung (z. B. OLG Koblenz
9 U 1015/25, 02.06.2026; OLG Rostock 2 U 11/20): Der Hinweis auf Partner/Subunternehmer muss sich aus der
Werbung selbst ergeben – deshalb steht er im Footer jeder Seite und als Kasten auf den Leistungsseiten.

Das Skript (idempotent, Marker `partner-hinweis` / `foot-partner`):
1. setzt im Footer aller öffentlichen Seiten eine Zeile mit Link auf impressum.html#leistungserbringung,
2. setzt auf Leuchtreklame-, Messe-, Fahrzeug-, Schilder- und Regionsseiten einen kurzen Hinweis vor das Kontaktformular,
3. ersetzt auf den Leuchtreklame-Seiten Formulierungen, die eigene Herstellung/Montage beleuchteter Anlagen behaupten
   (dieselben Texte stehen in tools/folien/nrw_pages.py, nrw_staedte.py und tools/seo/referenzen_einbau.py).

Reihenfolge: nach den Generatoren und referenzen_einbau.py, vor a11y.py / marke.py / umbruch.py.
Aufruf: python3 tools/seo/partner_hinweis.py   (--dry zeigt nur, was sich ändern würde)
"""
import os, re, sys, glob

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
AUSNAHMEN = ('admin/', 'tools/', 'node_modules/', 'data/', 'docs/', 'angebote/')

FOOT = ('<p class="foot-partner" style="margin:1.1rem 0 0;font-size:13px;line-height:1.6;color:rgba(255,255,255,.75);max-width:100%">'
        'Masar Werbeagentur plant, gestaltet und koordiniert Ihr Projekt. Arbeiten, für die eine Eintragung in die Handwerksrolle '
        'oder eine Elektrofachkraft nötig ist – etwa Bau und Montage beleuchteter Werbeanlagen und elektrische Anschlüsse –, '
        'führen eingetragene Partnerbetriebe in unserem Auftrag aus. '
        '<a href="/impressum.html#leistungserbringung" style="color:#58d0bd">Mehr zur Leistungserbringung</a></p>')

TEXT = {
    'licht': ('<strong>So arbeiten wir bei Leuchtreklame:</strong> Wir gestalten, planen und koordinieren Ihr Projekt und klären die Genehmigung. '
              'Gebaut und montiert wird die beleuchtete Anlage von einem in die Handwerksrolle eingetragenen Partnerbetrieb; '
              'den elektrischen Anschluss übernimmt ein eingetragener Elektrofachbetrieb aus unserem Partnernetz. '
              'Ihr Vertragspartner und Ansprechpartner bleiben wir.'),
    'messe': ('<strong>So arbeiten wir beim Messestand:</strong> Planung, 3D-Entwurf, Grafik und die Koordination von Auf- und Abbau liegen bei uns. '
              'Elektroarbeiten am Stand und individuell gefertigte Bauteile, für die eine besondere Qualifikation nötig ist, '
              'übernehmen qualifizierte Partnerbetriebe in unserem Auftrag. Ihr Vertragspartner und Ansprechpartner bleiben wir.'),
    'fahrzeug': ('<strong>So arbeiten wir bei Fahrzeugen:</strong> Gestaltung, Druckdaten und die Steuerung des Projekts liegen bei uns. '
                 'Vollfolierungen und Arbeiten, die eine besondere Ausrüstung oder Qualifikation erfordern, setzen wir mit spezialisierten '
                 'Partnerbetrieben aus unserem Netzwerk um. Ihr Vertragspartner und Ansprechpartner bleiben wir.'),
    'allg': ('<strong>Wer was ausführt:</strong> Wir planen, gestalten und koordinieren Ihr Projekt. Arbeiten, für die eine Eintragung in die '
             'Handwerksrolle oder eine besondere Qualifikation nötig ist – etwa Bau und Montage beleuchteter Anlagen, elektrische Anschlüsse '
             'oder Montagen mit Hubarbeitsbühne –, führen qualifizierte Partnerbetriebe in unserem Auftrag aus. '
             'Ihr Vertragspartner und Ansprechpartner bleiben wir.'),
}
LINK = ' <a href="/impressum.html#leistungserbringung" style="color:#177567;font-weight:600">Mehr dazu</a>'


def box(art):
    return ('<!-- partner-hinweis -->\n<div class="partner-hinweis" role="note" style="max-width:1100px;margin:2rem auto;padding:0 16px;box-sizing:border-box">'
            '<p style="margin:0;background:#f4f7f7;border-left:4px solid #58d0bd;border-radius:10px;padding:1rem 1.2rem;'
            f'font-size:15px;line-height:1.6;color:#1a2a2a">{TEXT[art]}{LINK}</p></div>\n')


def art_fuer(rel):
    n = os.path.basename(rel)
    if rel.startswith('blog/'):
        return None
    if n.startswith('leuchtreklame-') or n in ('aussenwerbung-berlin.html', 'werbetechnik.html'):
        return 'licht'
    if n in ('messebau-berlin.html', 'messestand-berlin-2027.html', 'messebeschriftung-berlin.html'):
        return 'messe'
    if n.startswith(('fahrzeugbeschriftung-', 'lkw-beschriftung-')):
        return 'fahrzeug'
    if n.startswith(('schilder-', 'werbeagentur-', 'werbetechnik-')) or n in (
            'index.html', 'leistungen.html', 'kanzleischild-berlin.html', 'praxisbeschilderung-berlin.html'):
        return 'allg'
    return None


# Leuchtreklame-Seiten: eigene Herstellung/Montage beleuchteter Anlagen nicht behaupten
LICHT_ERSETZEN = [
    ('So sehen Arbeiten aus, die wir gebaut und montiert haben.',
     'So sehen Projekte aus, die wir geplant und mit unseren Partnerbetrieben umgesetzt haben.'),
    ('Leuchtreklame <em>aus unserer Werkstatt</em>', 'Leuchtreklame <em>aus unseren Projekten</em>'),
    ('Leuchtreklame aus unserer Werkstatt', 'Leuchtreklame aus unseren Projekten'),
    ('Außenwerbung aus unserer Werkstatt', 'Außenwerbung aus unseren Projekten'),
    ('Alles aus einer Hand – Gestaltung, Produktion und Montage durch unser Team in NRW.',
     'Alles aus einer Hand – Gestaltung und Koordination durch uns, Bau, Montage und Anschluss durch eingetragene Partnerbetriebe.'),
    ('Nach Ihrer Freigabe produzieren wir und montieren am vereinbarten Termin bei Ihnen.',
     'Nach Ihrer Freigabe fertigt ein eingetragener Partnerbetrieb die Anlage und montiert sie am vereinbarten Termin bei Ihnen.'),
    ('Den Anschluss an das Hausnetz übernimmt eine Elektrofachkraft;',
     'Den Anschluss an das Hausnetz übernimmt ein eingetragener Elektrofachbetrieb aus unserem Partnernetz;'),
    ('Ihren verbindlichen Festpreis inklusive Montage durch unser Team in NRW bekommen Sie',
     'Ihren verbindlichen Festpreis inklusive Montage durch eingetragene Partnerbetriebe bekommen Sie'),
    ('Wir gestalten, produzieren und klären vorab, was an Ihrer Fassade erlaubt ist – unser Team in NRW misst auf und montiert bei Ihnen vor Ort.',
     'Wir gestalten, klären vorab, was an Ihrer Fassade erlaubt ist, und koordinieren alles Weitere – unser Team in NRW misst bei Ihnen auf, Bau, Montage und Anschluss übernehmen eingetragene Partnerbetriebe.'),
    ('Unser Team in NRW kommt für Aufmaß und Montage zu Ihnen.',
     'Unser Team in NRW kommt zum Aufmaß zu Ihnen, die Montage übernimmt ein eingetragener Partnerbetrieb.'),
    ('Unser Team in NRW misst auf und montiert bei Ihnen vor Ort.',
     'Unser Team in NRW misst bei Ihnen auf, die Montage übernimmt ein eingetragener Partnerbetrieb.'),
    ('Wir gestalten, klären die Genehmigung und unser Team in NRW montiert bei Ihnen vor Ort.',
     'Wir gestalten, klären die Genehmigung und koordinieren Bau und Montage mit eingetragenen Partnerbetrieben vor Ort.'),
    ('Genehmigung geprüft, Montage durch unser Team vor Ort.', 'Genehmigung geprüft, Montage durch eingetragene Partnerbetriebe.'),
    ('Montage und elektrischer Anschluss durch unsere Fachbetriebe,', 'Montage und elektrischer Anschluss durch eingetragene Partnerbetriebe,'),
]
LICHT_RE = [
    (re.compile(r'Ja\. Unser Team in NRW kommt für Aufmaß und Montage zu Ihnen – '),
     'Ja. Unser Team in NRW kommt zum Aufmaß zu Ihnen, die Montage übernimmt ein eingetragener Partnerbetrieb – '),
    (re.compile(r'Unser Team montiert bei Ihnen in ([A-ZÄÖÜ][\wäöüß-]+)\.'),
     r'Die Montage in \1 übernimmt ein eingetragener Partnerbetrieb.'),
]


def bearbeiten(rel, s):
    neu = s
    art = art_fuer(rel)
    if art == 'licht' and os.path.basename(rel).startswith(('leuchtreklame-', 'aussenwerbung-')):
        for alt, ers in LICHT_ERSETZEN:
            neu = neu.replace(alt, ers)
        for muster, ers in LICHT_RE:
            neu = muster.sub(ers, neu)
    if art and 'partner-hinweis' not in neu:
        m = re.search(r'<section[^>]*\bid="kontakt"', neu)
        pos = m.start() if m else neu.find('</main>')
        if pos > 0:
            neu = neu[:pos] + box(art) + neu[pos:]
    if 'foot-partner' not in neu and '<div class="foot-bottom">' in neu:
        neu = neu.replace('<div class="foot-bottom">', FOOT + '\n    <div class="foot-bottom">', 1)
    return neu


def main():
    dry = '--dry' in sys.argv
    n = 0
    for p in sorted(glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True)):
        rel = os.path.relpath(p, ROOT)
        if rel.startswith(AUSNAHMEN):
            continue
        s = open(p, encoding='utf-8').read()
        neu = bearbeiten(rel, s)
        if neu != s:
            n += 1
            if dry:
                print('würde ändern:', rel)
            else:
                open(p, 'w', encoding='utf-8').write(neu)
    print(n, 'Seiten', 'würden geändert' if dry else 'geändert')


if __name__ == '__main__':
    main()
