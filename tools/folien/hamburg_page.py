"""Erzeugt werbeagentur-hamburg.html aus werbeagentur-nrw.html (gleiches Layout, Texte für Hamburg).

Hamburg: eigenes Team vor Ort (keine Adresse/Filiale), NRW-Preise, Leistungen wie NRW
(ohne Foto/Video, Messebau, Express). Genehmigung nach Hamburgischer Bauordnung (HBauO).
Aufruf: python3 tools/folien/hamburg_page.py
"""
import os, re

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
src = open(os.path.join(ROOT, 'werbeagentur-nrw.html'), encoding='utf-8').read()
s = src


def ersetze(alt, neu, anzahl=1):
    global s
    n = s.count(alt)
    assert n == anzahl, f'{n}× statt {anzahl}×: {alt[:70]}'
    s = s.replace(alt, neu)


def block(start, ende, neu):
    """Ersetzt den Bereich von start (inkl.) bis ende (exkl.)."""
    global s
    a = s.index(start); b = s.index(ende, a)
    s = s[:a] + neu + s[b:]


WA_NRW = 'Hallo%2C%20ich%20habe%20eine%20Anfrage%20f%C3%BCr%20Werbetechnik%20in%20NRW.'
WA_HH = 'Hallo%2C%20ich%20habe%20eine%20Anfrage%20f%C3%BCr%20Werbetechnik%20in%20Hamburg.'
s = s.replace(WA_NRW, WA_HH)

BESCHR = 'Werbeagentur in Hamburg mit eigenem Team vor Ort: Schilder, Leuchtreklame, Fahrzeug- und Schaufensterbeschriftung, Druck, Grafik- und Webdesign.'
s = s.replace('Werbeagentur in NRW mit eigenem Team vor Ort: Schilder, Leuchtreklame, Fahrzeug- und Schaufensterbeschriftung, Druck, Grafik- und Webdesign.', BESCHR)
s = s.replace('Werbeagentur NRW: Werbetechnik, Druck &amp; Design | Masar', 'Werbeagentur Hamburg: Werbetechnik, Druck &amp; Design | Masar')
s = s.replace('https://masar-werbeagentur.de/werbeagentur-nrw.html', 'https://masar-werbeagentur.de/werbeagentur-hamburg.html')
s = s.replace('https://masar-werbeagentur.de/og/werbeagentur-nrw.jpg', 'https://masar-werbeagentur.de/og/werbeagentur-hamburg.jpg')
ersetze('content="Werbeagentur NRW – Masar Werbeagentur"', 'content="Werbeagentur Hamburg – Masar Werbeagentur"')

# JSON-LD: Einsatzgebiet
a = s.index('"areaServed": ['); b = s.index('],', a) + 2
BEZIRKE = ['Hamburg-Mitte', 'Altona', 'Eimsbüttel', 'Hamburg-Nord', 'Wandsbek', 'Bergedorf', 'Harburg']
area = '"areaServed": [\n    {\n      "@type": "City",\n      "name": "Hamburg"\n    }' + ''.join(
    f',\n    {{\n      "@type": "Place",\n      "name": "{b_}"\n    }}' for b_ in BEZIRKE) + '\n  ],'
s = s[:a] + area + s[b:]
ersetze('"name": "Werbeagentur NRW",\n  "description"', '"name": "Werbeagentur Hamburg",\n  "description"')
ersetze('"name": "Werbeagentur NRW",\n      "item"', '"name": "Werbeagentur Hamburg",\n      "item"')

# FAQ (JSON-LD und sichtbar)
FAQ_ORT_F = 'Wo genau sind Sie in Hamburg tätig?'
FAQ_ORT_A = 'In allen sieben Bezirken: Hamburg-Mitte, Altona, Eimsbüttel, Hamburg-Nord, Wandsbek, Bergedorf und Harburg. Liegt Ihr Standort im Umland, fragen Sie einfach – wir sagen Ihnen ehrlich, wann ein Termin möglich ist.'
FAQ_STO_F = 'Haben Sie einen Standort in Hamburg?'
FAQ_STO_A = 'Unser Firmensitz mit Studio ist in Berlin-Wedding. In Hamburg arbeitet ein eigenes Team für uns, das Aufmaß, Montage und Beschriftung vor Ort übernimmt. Anfragen laufen über dieselbe Nummer, dieselbe E-Mail und dasselbe Formular.'
FAQ_GEN_A = 'Das hängt von Größe, Anbringung und Lage ab. In Hamburg gilt die Hamburgische Bauordnung (HBauO): Werbeanlagen mit einer Ansichtsfläche bis 1 m² brauchen nach Anlage 2 zur HBauO keine Genehmigung, größere in der Regel eine Baugenehmigung. Zusätzlich können Erhaltungsverordnungen und Vorgaben des Bezirks gelten, und Werbeanlagen auf öffentlichem Grund brauchen immer eine Sondernutzungserlaubnis. Wir klären das vor dem Angebot und bereiten den Antrag mit Ihnen vor.'
FAQ_MESSE_F = 'Bieten Sie in Hamburg auch Messebau an?'
FAQ_MESSE_A = 'Nein – Messebau machen wir nur in Berlin. Für Hamburg übernehmen wir Schilder, Leuchtreklame, Fahrzeug- und Schaufensterbeschriftung, Folien, Banner, Druck, Textildruck, Grafik- und Webdesign.'
alt_faq = re.findall(r'"text": "(Schwerpunkt sind Düsseldorf.*?)"', s)[0]
s = s.replace(alt_faq, FAQ_ORT_A)
s = s.replace('Wo genau sind Sie in NRW tätig?', FAQ_ORT_F)
s = s.replace('Haben Sie einen Standort in NRW?', FAQ_STO_F)
s = s.replace('Unser Firmensitz mit Studio ist in Berlin-Wedding. In NRW arbeitet ein eigenes Team für uns, das Aufmaß, Montage und Beschriftung vor Ort übernimmt. Anfragen laufen über dieselbe Nummer, dieselbe E-Mail und dasselbe Formular.', FAQ_STO_A)
gen_alt = 'Das hängt von Größe, Beleuchtung, Anbringung und Lage ab. In NRW gilt die Landesbauordnung NRW: Werbeanlagen bis 1 m² Ansichtsfläche sind verfahrensfrei, größere oder auskragende Anlagen meist nicht – und alles, was in den Gehweg ragt, braucht eine Sondernutzungserlaubnis. Wir klären das vor dem Angebot und bereiten den Antrag mit Ihnen vor.'
assert s.count(gen_alt) == 2
s = s.replace(gen_alt, FAQ_GEN_A)
s = s.replace('Bieten Sie in NRW auch Messebau an?', FAQ_MESSE_F)
s = s.replace('Nein – Messebau machen wir nur in Berlin. Für NRW übernehmen wir Schilder, Leuchtreklame, Fahrzeug- und Schaufensterbeschriftung, Folien, Banner, Druck, Textildruck, Grafik- und Webdesign.', FAQ_MESSE_A)

# Termin-Link und Assistent
s = s.replace('/termin.html?region=nrw', '/termin.html?region=hamburg')
ersetze('data-region="nrw"', 'data-region="hamburg" data-ort="Hamburg"')

# Hero
ersetze('<div class="hero-badge">✦ Werbeagentur · Nordrhein-Westfalen</div>', '<div class="hero-badge">✦ Werbeagentur · Hamburg</div>')
ersetze('<h1>Werbeagentur<em>für ganz</em>NRW.</h1>', '<h1>Werbeagentur<em>für</em>Hamburg.</h1>')
ersetze('Düsseldorf, Köln, Dortmund, Essen und die Städte dazwischen: Unser Team in NRW misst bei Ihnen auf, produziert und montiert – von der Schaufensterfolie bis zur Leuchtreklame, vom einzelnen Transporter bis zur Website.',
        'Von Altona bis Wandsbek, von Eimsbüttel bis Harburg: Unser Team in Hamburg misst bei Ihnen auf, produziert und montiert – von der Schaufensterfolie bis zur Leuchtreklame, vom einzelnen Transporter bis zur Website.')
# Bild im Hero (auch mobil sichtbar)
block('<div class="hero-logo-frame">', '      </div>\n    </div>\n  </div>\n</section>',
      '<img class="hero-shot-hh" src="/leuchtreklamen-720.webp" srcset="/leuchtreklamen-360.webp 360w, /leuchtreklamen-540.webp 540w, /leuchtreklamen-720.webp 720w, /leuchtreklamen.webp 1080w" sizes="(max-width: 900px) 80vw, 400px" alt="Leuchtreklame und Außenwerbung in Hamburg – Masar Werbeagentur" loading="eager" fetchpriority="high" width="1080" height="1350">\n')
ersetze('</head>', '<style id="hero-mobile">.hero-shot-hh{display:block;border-radius:16px;box-shadow:0 22px 60px rgba(0,0,0,.4);width:100%;max-width:400px;height:auto;margin:0 auto}@media(max-width:900px){.hero-visual{display:block!important;margin-top:1.6rem}.hero-shot-hh{max-width:340px;width:100%;margin:0 auto}}</style>\n</head>')

# Breadcrumb, Laufband
ersetze('    <span>Werbeagentur NRW</span>', '    <span>Werbeagentur Hamburg</span>')
s = s.replace('<span class="hi">Werbeagentur NRW</span>', '<span class="hi">Werbeagentur Hamburg</span>')

# Abschnitt „Was wir machen“
ersetze('<span class="eyebrow">Was wir in NRW machen</span>', '<span class="eyebrow">Was wir in Hamburg machen</span>')
ersetze('mit einem Team, das in NRW unterwegs ist.', 'mit einem Team, das in Hamburg unterwegs ist.')
ersetze('Aufmaß, Montage und Beschriftung übernimmt unser Team in NRW. Sie müssen nichts selbst anbringen',
        'Aufmaß, Montage und Beschriftung übernimmt unser Team in Hamburg. Sie müssen nichts selbst anbringen')
ersetze('<div class="why-title">Landesbauordnung NRW im Blick</div><div class="why-desc">In NRW gelten andere Schwellen als in Berlin. Ob Ihr Schild genehmigungsfrei ist, ob der Bebauungsplan etwas vorschreibt oder ob ein Nasenschild eine Sondernutzungserlaubnis braucht, klären wir, bevor Sie ein Angebot unterschreiben.</div>',
        '<div class="why-title">Hamburgische Bauordnung im Blick</div><div class="why-desc">In Hamburg gelten die Hamburgische Bauordnung und die Vorgaben der Bezirke. Ob Ihr Schild genehmigungsfrei ist, ob eine Erhaltungsverordnung gilt oder ob ein Ausleger eine Sondernutzungserlaubnis braucht, klären wir, bevor Sie ein Angebot unterschreiben.</div>')
ersetze('Messebau bieten wir nur in Berlin an, Foto und Video ebenfalls. Für NRW konzentrieren wir uns',
        'Messebau bieten wir nur in Berlin an, Foto und Video ebenfalls. In Hamburg konzentrieren wir uns')

# Leistungskarten: keine NRW-Unterseiten verlinken
for alt, thema in [('/leuchtreklame-nrw.html" class="svc-link">Leuchtreklame in NRW →', 'Leuchtreklame in Hamburg'),
                   ('/fahrzeugbeschriftung-nrw.html" class="svc-link">Fahrzeugbeschriftung in NRW →', 'Fahrzeugbeschriftung in Hamburg'),
                   ('/schilder-nrw.html" class="svc-link">Schilder in NRW →', 'Schilder in Hamburg'),
                   ('/schaufensterbeschriftung-nrw.html" class="svc-link">Schaufenster in NRW →', 'Schaufenster in Hamburg'),
                   ('/pvc-banner-nrw.html" class="svc-link">PVC-Banner in NRW →', 'PVC-Banner in Hamburg')]:
    ersetze('<a href="' + alt + '</a>', f'<a href="#kontakt" class="svc-link" data-betreff="{thema}">Angebot anfragen →</a>')
ersetze('Mobile Werbung, die täglich tausende Menschen erreicht.', 'Mobile Werbung, die bei jeder Fahrt durch die Stadt mitwirbt.')
s = s.replace(' in NRW">', ' in Hamburg">').replace(' in NRW ">', ' in Hamburg">')
s = re.sub(r'alt="([^"]*?) NRW([ "–])', r'alt="\1 Hamburg\2', s)
s = s.replace('für Betriebe in NRW – Aufmaß und Montage vor Ort.', 'für Betriebe in Hamburg – Aufmaß und Montage vor Ort.')
s = s.replace('Aufmaß und Montage übernimmt unser Team in NRW – Firmensitz und Studio sind in Berlin-Wedding.', 'Aufmaß und Montage übernimmt unser Team in Hamburg – Firmensitz und Studio sind in Berlin-Wedding.')
s = s.replace('für Unternehmen in NRW – Design immer inklusive.', 'für Unternehmen in Hamburg – Design immer inklusive.')
ersetze('<p style="margin-top:.9rem;font-size:14.5px;"><a href="/webdesign-nrw.html" style="color:var(--teal-ink);font-weight:700;">Mehr zu Webdesign in NRW →</a></p>', '')

# Genehmigung Hamburg
block('<section class="section bg-off">\n  <div class="container">\n    <div class="sec-head center reveal">\n      <span class="eyebrow">Genehmigung</span>',
      '<section class="section">\n  <div class="container">\n    <div class="sec-head center reveal">\n      <span class="eyebrow">Einsatzgebiet</span>',
      '''<section class="section bg-off">
  <div class="container">
    <div class="sec-head center reveal">
      <span class="eyebrow">Genehmigung</span>
      <h2 class="sec-title">Was die <em>Hamburgische Bauordnung</em> sagt</h2>
      <p class="sec-sub">In Hamburg gilt die Hamburgische Bauordnung (HBauO), nicht die Berliner Bauordnung. Die wichtigsten Punkte für Schilder und Leuchtreklame:</p>
    </div>
    <div class="prozess-grid">
      <div class="prozess-step reveal">
        <div class="prozess-num">1</div>
        <div class="prozess-title">Bis 1 m² ohne Genehmigung</div>
        <div class="prozess-desc">Werbeanlagen mit einer Ansichtsfläche bis 1 m² brauchen nach Anlage 2 zur Hamburgischen Bauordnung keine Baugenehmigung. Für ein kleines Schild am Eingang ist das oft der einfachste Weg.</div>
      </div>
      <div class="prozess-step reveal">
        <div class="prozess-num">2</div>
        <div class="prozess-title">Größer: meist Baugenehmigung</div>
        <div class="prozess-desc">Größere Werbeanlagen auf privaten Grundstücken brauchen in der Regel eine Baugenehmigung. Zeichnung, Maße und technische Angaben für den Antrag bereiten wir mit Ihnen vor.</div>
      </div>
      <div class="prozess-step reveal">
        <div class="prozess-num">3</div>
        <div class="prozess-title">Bezirk und Erhaltungsgebiet</div>
        <div class="prozess-desc">In manchen Straßen gelten städtebauliche Erhaltungsverordnungen oder Vorgaben des Bezirks, die strenger sind als die Bauordnung. Ob das bei Ihnen der Fall ist, prüfen wir vor dem Angebot.</div>
      </div>
      <div class="prozess-step reveal">
        <div class="prozess-num">4</div>
        <div class="prozess-title">Genehmigungsfrei heißt nicht regelfrei</div>
        <div class="prozess-desc">Auch ohne Genehmigung muss jede Werbeanlage die Anforderungen der Bauordnung erfüllen (§ 13 HBauO). Werbeanlagen auf öffentlichem Grund – etwa ein Ausleger über dem Gehweg – brauchen immer eine Sondernutzungserlaubnis.</div>
      </div>
    </div>
    <div class="reveal" style="max-width:760px;margin:2rem auto 0;font-size:15px;line-height:1.75;color:var(--muted);text-align:center;"><p>Zuständig ist das Bezirksamt, in dessen Bezirk Ihr Standort liegt. Diese Übersicht ersetzt keine Prüfung im Einzelfall – die übernehmen wir vor dem Angebot.</p></div>
  </div>
</section>

''')

# Einsatzgebiet: sieben Bezirke statt NRW-Städte
PIN = '<div class="why-icon"><svg class="i-svg" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/></svg></div>'
BEZ = [('Hamburg-Mitte', 'Altstadt, Neustadt, St. Pauli, St. Georg, HafenCity und Hamm.'),
       ('Altona', 'Altona-Altstadt, Ottensen, Bahrenfeld, Blankenese und Lurup.'),
       ('Eimsbüttel', 'Eimsbüttel, Rotherbaum, Harvestehude, Stellingen und Niendorf.'),
       ('Hamburg-Nord', 'Eppendorf, Winterhude, Barmbek, Uhlenhorst und Fuhlsbüttel.'),
       ('Wandsbek', 'Wandsbek, Bramfeld, Rahlstedt, Volksdorf und Poppenbüttel.'),
       ('Bergedorf', 'Bergedorf, Lohbrügge und die Vier- und Marschlande.'),
       ('Harburg', 'Harburg, Heimfeld, Wilhelmsburg-Süd, Neugraben und Hausbruch.')]
karten = ''.join(f'      <div class="why-card reveal">{PIN}<div class="why-title">{n}</div><div class="why-desc">{d}</div></div>\n' for n, d in BEZ)
block('      <h2 class="sec-title">Wo wir in NRW <em>unterwegs sind</em></h2>', '<!-- WHY US -->',
      f'''      <h2 class="sec-title">Wo wir in Hamburg <em>unterwegs sind</em></h2>
      <p class="sec-sub">Unser Team ist in allen sieben Bezirken im Einsatz:</p>
    </div>
    <div class="why-grid">
{karten}    </div>
    <div class="reveal" style="max-width:760px;margin:2rem auto 0;font-size:15px;line-height:1.75;color:var(--muted);text-align:center;"><p>Ihr Standort liegt im Hamburger Umland? Fragen Sie einfach – wir sagen Ihnen ehrlich, wann ein Termin möglich ist.</p></div>
  </div>
</section>

''')

ersetze('<div class="why-title">Team vor Ort in NRW</div><div class="why-desc">Aufmaß, Montage und Beschriftung übernimmt unser Team in NRW.', '<div class="why-title">Team vor Ort in Hamburg</div><div class="why-desc">Aufmaß, Montage und Beschriftung übernimmt unser Team in Hamburg.')
ersetze('Wir liefern und montieren direkt vor Ort – in NRW.', 'Wir liefern und montieren direkt vor Ort – in Hamburg.')
ersetze('Was Betriebe in NRW <em>vorher fragen</em>', 'Was Betriebe in Hamburg <em>vorher fragen</em>')
s = s.replace('data-betreff="Social Media für mein Unternehmen in NRW"', 'data-betreff="Social Media für mein Unternehmen in Hamburg"')
s = s.replace('data-betreff="Angebot in NRW"', 'data-betreff="Angebot in Hamburg"')

# Weitere Städte und Leistungen
CHIP = 'style="display:inline-flex;align-items:center;gap:.5rem;background:#fff;border:1px solid var(--border);border-radius:999px;padding:11px 20px;font-size:14px;font-weight:600;color:var(--navy);"'
block('      <a href="/werbeagentur-duesseldorf.html" ' + CHIP + '>Düsseldorf</a>', '    </div>\n  </div>\n</section>\n\n<!-- CONTACT -->',
      ''.join(f'      <a href="{h}" {CHIP}>{t}</a>\n' for h, t in [('/', 'Berlin'), ('/werbeagentur-nrw.html', 'NRW'), ('/einsatzgebiete.html', 'Alle Einsatzgebiete'), ('/termin.html?region=hamburg', 'Kostenlose Beratung'), ('/referenzen.html', 'Referenzen')]))
ersetze('Weitere Städte und <em>Leistungen</em>', 'Weitere Regionen und <em>Leistungen</em>')

# Kontakt
ersetze('<div class="cta-title reveal">Ihr Projekt in <em>NRW.</em></div>', '<div class="cta-title reveal">Ihr Projekt in <em>Hamburg.</em></div>')
ersetze('value="Werbeagentur NRW – Anfrage"', 'value="Werbeagentur Hamburg – Anfrage"')
ersetze('placeholder="z. B. Schild und Schaufenster in NRW"', 'placeholder="z. B. Schild und Schaufenster in Hamburg"')
ersetze('Zum Beispiel: Neues Ladenlokal in Bochum, Schaufenster und Schild über dem Eingang, dazu zwei Transporter.', 'Zum Beispiel: Neues Ladenlokal in Ottensen, Schaufenster und Schild über dem Eingang, dazu zwei Transporter.')
ersetze('<strong>Team vor Ort in NRW</strong> · Termin nach Vereinbarung', '<strong>Team vor Ort in Hamburg</strong> · Termin nach Vereinbarung')
ort_input = '<div class="fg"><label for="betreffInput">'
ersetze(ort_input, '<input type="hidden" name="ort" value="Hamburg">\n          ' + ort_input)

# Ruhrgebiet-Block entfernen
block('<section class="section bg-alt" style="padding:2.4rem 0;">', '</main>', '')

# Fußzeile: Hamburg ergänzen (nur auf dieser Seite)
SEP = '<span aria-hidden="true" style="color:rgba(255,255,255,.35);margin:0 .45rem;">·</span>'
FOOT_NRW = '<a href="/werbeagentur-nrw.html" style="color:#58d0bd;">NRW</a>'
i = s.index(FOOT_NRW)
s = s[:i] + '<a href="/werbeagentur-hamburg.html" style="color:#58d0bd;">Hamburg</a>' + SEP + s[i:]

# Navigation: keine NRW-Unterseiten
s = s.replace('<li><a href="/lkw-beschriftung-nrw.html">LKW-Beschriftung</a></li>', '<li><a href="/lkw-beschriftung-berlin.html">LKW-Beschriftung</a></li>')
s = s.replace('  <a href="/fahrzeugbeschriftung-nrw.html">Fahrzeugbeschriftung</a>\n  <a href="/lkw-beschriftung-nrw.html">LKW-Beschriftung</a>', '  <a href="/fahrzeugbeschriftung-berlin.html">Fahrzeugbeschriftung</a>\n  <a href="/lkw-beschriftung-berlin.html">LKW-Beschriftung</a>')

s = s.replace('/assistent.js?v=7', '/assistent.js?v=8')   # Region hamburg braucht die neue Version

assert 'Düsseldorf' not in s.split('<footer')[0], 'NRW-Stadt im Inhalt übrig'
open(os.path.join(ROOT, 'werbeagentur-hamburg.html'), 'w', encoding='utf-8').write(s)
print('werbeagentur-hamburg.html geschrieben,', len(s), 'Zeichen')
