"""Stadt-Ratgeber für den Blog: „Werbeanlage in <Stadt> – Genehmigung, Satzungen, Kosten“.

Jeder Artikel hat eigene, belegte Inhalte (lokale Satzungen, Behörden, Quellen) – keine Kopien mit
nur anderem Ortsnamen. Layout und Kopf/Fuß kommen aus blog/aussenwerbung-berlin-ratgeber.html.
Aufruf: python3 tools/blog/stadt_ratgeber.py
"""
import os, re, html, json

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
VORLAGE = open(os.path.join(ROOT, 'blog', 'aussenwerbung-berlin-ratgeber.html'), encoding='utf-8').read()
DATUM, MONAT = '2026-10-23', 'Oktober 2026'
WA = '491785143918'
e = html.escape

I = {
    'tip': '<svg class="i-inline" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></svg>',
    'warn': '<svg class="i-inline" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>',
    'pin': '<svg class="i-inline" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/></svg>',
    'cal': '<svg class="i-inline" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/></svg>',
    'clock': '<svg class="i-inline" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><line x1="10" x2="14" y1="2" y2="2"/><line x1="12" x2="15" y1="14" y2="11"/><circle cx="12" cy="14" r="8"/></svg>',
    'pen': '<svg class="i-inline" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 20h9"/><path d="M16.376 3.622a1 1 0 0 1 3.002 3.002L7.368 18.635a2 2 0 0 1-.855.506l-2.872.838a.5.5 0 0 1-.62-.62l.838-2.872a2 2 0 0 1 .506-.854z"/></svg>',
    'wa': '<svg class="i-inline" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/></svg>',
}

NRW_PREISE = [('Firmenschild', 'ab 179 €'), ('Leuchtbuchstaben', 'ab 229 € je Buchstabe'), ('Schaufensterbeschriftung', 'ab 179 €'),
              ('Milchglas / Sichtschutz', 'ab 229 €'), ('Fahrzeug-Teilbeschriftung', 'ab 340 €')]
BER_PREISE = [('Firmenschild', 'ab 149 €'), ('Leuchtbuchstaben', 'ab 199 € je Buchstabe'), ('Schaufensterbeschriftung', 'ab 149 €'),
              ('Milchglas / Sichtschutz', 'ab 190 €'), ('Fahrzeug-Teilbeschriftung', 'ab 290 €')]
NRW_GEB = ('Die Baugenehmigungsgebühr richtet sich in NRW nach dem Allgemeinen Gebührentarif (AVerwGebO NRW): '
           'für Werbeanlagen 10 % der Herstellungssumme, mindestens 100 €. Bei einer Leuchtreklame für 3.000 € sind das also rund 300 €.')
NRW_RECHT = ('In ganz Nordrhein-Westfalen gilt die Landesbauordnung (BauO NRW). Werbeanlagen mit einer Ansichtsfläche bis 1 m² sind nach '
             '§ 62 BauO NRW verfahrensfrei; mehrere Flächen nebeneinander werden zusammengerechnet. Städte dürfen aber nach § 89 BauO NRW '
             'eigene Gestaltungs- und Werbesatzungen erlassen – und genau dort wird es in {stadt} interessant.')

STAEDTE = [
 dict(slug='koeln', stadt='Köln', region='nrw', seite='/werbeagentur-koeln.html', bild='leuchtreklamen',
  title='Werbeanlage in Köln: Werbesatzungen, Genehmigung & Kosten (2026)',
  desc='Köln hat für viele Veedel eigene Werbesatzungen – dort ist oft schon ab 0,5 m² ein Antrag nötig. Was gilt, wo es gilt und wie Sie es klären.',
  h1='Werbeanlage in Köln:<br><em>Werbesatzungen</em><br>&amp; Genehmigung',
  kurz='In Köln sind Werbeanlagen bis 1 m² nach Landesrecht grundsätzlich frei. <strong>Aber:</strong> Liegt Ihr Laden im Bereich einer Kölner Werbesatzung, entfällt dieser Vorteil – die Stadt weist darauf hin, dass dort meist schon ab 0,5 m² ein Antrag nötig ist.',
  lokal_h='Kölner Werbesatzungen: Veedel für Veedel geregelt',
  lokal=[
   'Köln regelt Werbung nicht mit einer einzigen Satzung, sondern quartiersweise. Es gibt eigene Satzungen „über Anbringungsort, Abmessungen und Ausgestaltung von Werbeanlagen“, zum Beispiel für die <strong>Altstadt-Nord</strong>, die <strong>Venloer Straße</strong> in Ehrenfeld und die <strong>Neusser Straße</strong>. In den Jahren 2023 und 2024 hat die Stadt weitere Werbesatzungen für die Ringe und die Neustadt bekannt gemacht.',
   'Die Satzungen stützen sich auf die Landesbauordnung und führen ausdrücklich eine <strong>Genehmigungspflicht auch für sonst genehmigungsfreie Werbeanlagen</strong> ein. Inhaltlich verlangen sie, dass sich Werbung in die Gliederung der Fassade einfügt und das Ortsbild nicht beeinträchtigt.',
   'Ein konkretes Beispiel aus der Satzung Altstadt-Nord: Flach auf der Fassade angebrachte Werbeanlagen dürfen höchstens <strong>0,25 m</strong> vor die Bauflucht auskragen. Die Satzung für die Venloer Straße enthält eine eigene Regelung für größere Anlagen an Brandwänden.'],
  warn='An Baudenkmälern oder in ihrer Nähe wird Werbung zusätzlich mit dem Amt für Denkmalschutz abgestimmt. Den Bauantrag reichen Sie in NRW digital über das Bauportal.NRW ein.',
  raum='Ragt ein Schild über den Gehweg – etwa ein Nasenschild –, kommt zur Baugenehmigung eine straßenrechtliche Erlaubnis der Stadt hinzu. Welche Stelle in Köln dafür zuständig ist und welche Vorsprünge erlaubnisfrei sind, klären wir vor dem Angebot.',
  tipps=['Prüfen Sie zuerst, ob Ihre Adresse im Geltungsbereich einer Werbesatzung liegt – die Karten stehen in den Satzungen der Stadt Köln.',
         'Planen Sie in Satzungsgebieten auch für kleine Schilder einen Antrag ein. Das spart Ärger, wenn die Bauaufsicht nachfragt.',
         'Leuchtreklame an der Venloer oder Neusser Straße? Vorab Maße und Lage mit der Satzung abgleichen – das ist schneller als ein abgelehnter Antrag.'],
  faq=[('Brauche ich in Köln für ein kleines Schild eine Genehmigung?', 'Außerhalb von Satzungsgebieten sind Werbeanlagen bis 1 m² verfahrensfrei. In Gebieten mit Kölner Werbesatzung ist laut Stadt meist schon ab 0,5 m² ein Antrag nötig.'),
       ('Welche Kölner Straßen haben eine Werbesatzung?', 'Unter anderem Altstadt-Nord, Venloer Straße und Neusser Straße; 2023/2024 kamen Satzungen für die Ringe und die Neustadt hinzu. Maßgeblich ist der Geltungsbereich in der jeweiligen Satzung.'),
       ('Wie reiche ich den Antrag ein?', 'Digital über das Bauportal.NRW. Zeichnung, Fotomontage und technische Angaben bereiten wir für Sie vor.')],
  quellen=[('Stadt Köln – Baugenehmigungsfreie Werbeanlagen', 'https://www.stadt-koeln.de/artikel/74042/index.html'),
           ('Stadt Köln – Werbeanlagen (Dienstleistung)', 'https://www.stadt-koeln.de/service/produkte/00139/index.html'),
           ('Werbesatzung Altstadt-Nord', 'https://www.stadt-koeln.de/mediaasset/content/satzungen/werbesatzung-altstadt-nord20060113.pdf'),
           ('Werbesatzung Venloer Straße', 'https://www.stadt-koeln.de/mediaasset/content/satzungen/werbesatzung-venloer-strasse20140205.pdf')]),

 dict(slug='duesseldorf', stadt='Düsseldorf', region='nrw', seite='/werbeagentur-duesseldorf.html', bild='aussenwerbung',
  title='Werbeanlage in Düsseldorf: Altstadt-Satzung, Genehmigung & Kosten (2026)',
  desc='In der Düsseldorfer Altstadt braucht schon ein Schild unter 0,5 m² eine Baugenehmigung. Was die Satzung regelt und was sonst in Düsseldorf gilt.',
  h1='Werbeanlage in Düsseldorf:<br><em>Altstadt-Satzung</em><br>&amp; Genehmigung',
  kurz='Außerhalb besonderer Gebiete sind Werbeanlagen bis 1 m² in Düsseldorf verfahrensfrei. <strong>In der Altstadt</strong> gilt dagegen eine eigene Satzung: Dort ist eine Baugenehmigung auch für Werbeanlagen bis 0,5 m² und für zeitlich begrenzte Werbung erforderlich.',
  lokal_h='Die Düsseldorfer Altstadt-Satzung',
  lokal=[
   'Für den Altstadtbereich hat Düsseldorf eine eigene <strong>„Satzung über Werbeanlagen und Warenautomaten“</strong> (Stadtrecht Nr. 63.202). Sie gilt in einem fest umgrenzten Gebiet, das in einer Karte dargestellt ist – unter anderem rund um Altestadt, Stiftsplatz und Lambertusstraße.',
   'Der wichtigste Punkt für Ladeninhaber: In diesem Gebiet ist für das Errichten und Ändern von Werbeanlagen eine <strong>Baugenehmigung nötig – auch für Anlagen bis 0,5 m²</strong> und auch für zeitlich begrenzte Werbung. Ausgenommen ist Werbung für Schluss-, Räumungs- und Jubiläumsverkäufe an der Stätte der Leistung.',
   'Daneben gibt es eine stadtweite Satzung über Werbeanlagen mit <strong>wechselndem und bewegtem Licht</strong> (Nr. 63.201). Wer an Laufschrift oder animierte LED-Werbung denkt, sollte diese Satzung vorher kennen.'],
  warn='Die Königsallee grenzt an die Altstadt, steht aber nach unserer Recherche nicht ausdrücklich im Geltungsbereich der Altstadt-Satzung. Entscheidend ist die Karte der Stadt – wir prüfen das für Ihre Adresse.',
  raum='Für Ausleger über dem Gehweg, Aufsteller oder Werbung auf öffentlichen Flächen braucht es zusätzlich eine Sondernutzungserlaubnis der Stadt (Straßen- und Wegegesetz NRW).',
  tipps=['Ladenlokal in der Altstadt? Rechnen Sie auch für ein kleines Schild mit einem Bauantrag und planen Sie die Zeit ein.',
         'Eröffnungs- oder Aktionsbanner in der Altstadt sind keine Ausnahme – nur Schluss-, Räumungs- und Jubiläumsverkäufe sind ausgenommen.',
         'Für bewegte oder wechselnde Lichtwerbung zuerst die Satzung 63.201 prüfen – statische Leuchtbuchstaben sind meist der einfachere Weg.'],
  faq=[('Brauche ich in der Düsseldorfer Altstadt für ein kleines Schild eine Genehmigung?', 'Ja. Die Altstadt-Satzung verlangt eine Baugenehmigung auch für Werbeanlagen bis 0,5 m².'),
       ('Gilt die Altstadt-Satzung auch auf der Kö?', 'Nach unserer Recherche gehört die Königsallee nicht ausdrücklich zum Geltungsbereich. Maßgeblich ist die Karte der Stadt Düsseldorf.'),
       ('Ist animierte LED-Werbung erlaubt?', 'Dafür gibt es eine eigene Satzung über Werbeanlagen mit wechselndem und bewegtem Licht. Wir prüfen vor dem Angebot, was an Ihrem Standort zulässig ist.')],
  quellen=[('Düsseldorf – Satzung über Werbeanlagen und Warenautomaten für den Altstadtbereich (63.202)', 'https://www.duesseldorf.de/stadtrecht/6/63/63-202/'),
           ('Düsseldorfer Stadtrecht A bis Z', 'https://www.duesseldorf.de/stadtrecht/abisz/')]),

 dict(slug='dortmund', stadt='Dortmund', region='nrw', seite='/werbeagentur-dortmund.html', bild='schilder',
  title='Werbeanlage in Dortmund: Westenhellweg, Genehmigung & Kosten (2026)',
  desc='Am Westen- und Ostenhellweg ist jede Werbeanlage genehmigungspflichtig. Was die Dortmunder Gestaltungssatzungen regeln und wer zuständig ist.',
  h1='Werbeanlage in Dortmund:<br><em>Gestaltungssatzungen</em><br>&amp; Genehmigung',
  kurz='Dortmund ist eindeutig: Werbeanlagen im Bereich von Gestaltungssatzungen – zum Beispiel am <strong>Westenhellweg</strong> – sind laut Stadt <strong>immer baugenehmigungspflichtig</strong>, auch wenn sie anderswo nach § 62 BauO NRW frei wären.',
  lokal_h='Westenhellweg, Ostenhellweg & Co.',
  lokal=[
   'Zuständig ist das <strong>Stadtplanungs- und Bauordnungsamt</strong>. Für die wichtigste Einkaufsachse gibt es seit 2004 die „Satzung über Werbeanlagen, Vordächer und Sonnenschutzdächer zum Schutz der Gestalt des Westenhellweges / Ostenhellweges“. Sie regelt die Zulässigkeit von Werbeanlagen nach <strong>Anzahl, Lage, Größe und Ausführung</strong>.',
   'Weitere Gestaltungssatzungen und -leitlinien listet die Stadt auf ihrer Seite zu baurechtlichen Satzungen. Für das Zentrum von <strong>Hörde</strong> gibt es aus dem Stadtumbau eine Gestaltungsbroschüre, die Zahl und Größe von Werbeanlagen begrenzt.',
   'An <strong>Baudenkmälern</strong> oder in ihrer Nähe brauchen Werbeanlagen – genehmigungsfrei oder nicht – zusätzlich eine denkmalrechtliche Erlaubnis der Unteren Denkmalbehörde.'],
  warn='Werbung auf Straßen und Gehwegen (öffentlicher Grund) regelt in Dortmund ein Gestattungsvertrag mit dem Tiefbauamt – das ist eine eigene Stelle neben der Bauaufsicht.',
  raum='Für Aufsteller, Ausleger und Werbung im Straßenraum gilt die städtische Satzung über Sondernutzungen; je nach Fall schließt das Tiefbauamt einen Gestattungsvertrag.',
  tipps=['Laden am Westen- oder Ostenhellweg? Planen Sie für jede Werbeanlage einen Bauantrag ein – auch für kleine.',
         'Vordächer und Markisen fallen am Hellweg unter dieselbe Satzung – am besten gemeinsam mit dem Schild planen.',
         'Vor dem Design die Satzung lesen: Anzahl und Lage sind dort festgelegt, nicht nur die Größe.'],
  faq=[('Ist ein kleines Schild am Westenhellweg genehmigungsfrei?', 'Nein. Laut Stadt Dortmund sind Werbeanlagen im Bereich von Gestaltungssatzungen wie am Westenhellweg immer baugenehmigungspflichtig.'),
       ('Wer ist in Dortmund zuständig?', 'Das Stadtplanungs- und Bauordnungsamt; bei Denkmälern zusätzlich die Untere Denkmalbehörde, für Werbung auf öffentlichem Grund das Tiefbauamt.'),
       ('Was regelt die Hellweg-Satzung?', 'Anzahl, Lage, Größe und Ausführung von Werbeanlagen sowie Vordächer und Sonnenschutzdächer.')],
  quellen=[('Stadt Dortmund – Infoblatt Werbeanlagen (PDF)', 'https://www.dortmund.de/dortmund/projekte/rathaus/verwaltung/stadtplanungs-und-bauordnungsamt/downloads/bauordnung/infoblaetter/informationsblatt-werbeanlagen.pdf'),
           ('Stadt Dortmund – Bauantrag Werbeanlagen', 'https://www.dortmund.de/services/bauantrag-werbeanlagen.html'),
           ('Stadt Dortmund – Gestaltungssatzungen', 'https://www.dortmund.de/themen/planen-und-bauen/stadtplanung/baurechtliche-satzungen/gestaltungssatzungen/')]),

 dict(slug='essen', stadt='Essen', region='nrw', seite='/werbeagentur-essen.html', bild='leuchtreklamen',
  title='Werbeanlage in Essen: Reklameaufsicht, neue Gestaltungssatzung & Kosten (2026)',
  desc='Wer genehmigt Werbung in Essen, was kostet der Antrag und was bedeutet die geplante Gestaltungssatzung Innenstadt für Ihr Schild?',
  h1='Werbeanlage in Essen:<br><em>Reklameaufsicht</em><br>&amp; neue Satzung',
  kurz='In Essen ist die <strong>Reklameaufsicht</strong> der Stadt Ihr Ansprechpartner. Bis 1 m² sind Werbeanlagen nach Landesrecht verfahrensfrei. Für die Innenstadt arbeitet die Stadt an einer <strong>Gestaltungssatzung</strong>, die auch Werbeanlagen regeln soll.',
  lokal_h='Essen: Was sich in der Innenstadt ändert',
  lokal=[
   'Die Stadt Essen stellt eine <strong>Gestaltungssatzung für die Innenstadt</strong> auf (Grundlage: § 89 BauO NRW). Sie soll Fassaden, Werbeanlagen und Außengastronomie regeln – mit einem Rahmen, der Spielraum für individuelle Gestaltung lässt. Als Ziel nennt die Stadt unter anderem, überladene Werbeanlagen anzugehen.',
   'Im Frühjahr 2026 gab es Workshops mit Eigentümern, Händlern und Gastronomen und eine Online-Beteiligung. Einen Ratsbeschluss mit konkreten Regeln für Werbeanlagen haben wir bis zur Veröffentlichung dieses Artikels nicht gefunden.',
   'Für Sie heißt das: Wer jetzt eine Leuchtreklame in der Innenstadt plant, sollte zurückhaltend und hochwertig gestalten – das passt erfahrungsgemäß am ehesten zu dem, was eine Gestaltungssatzung später verlangt.'],
  warn='Kontakt: Stadt Essen, Reklameaufsicht, Lindenallee 10 (Deutschlandhaus), 45127 Essen · Tel. 0201 88-61114 · bauordnungsamt@essen.de. Fragen Sie vorab an – das ist kostenlos und spart Zeit.',
  raum='Für Ausleger über dem Gehweg, Aufsteller und Werbung auf öffentlichen Flächen ist zusätzlich eine Sondernutzungserlaubnis der Stadt nötig (Straßen- und Wegegesetz NRW).',
  tipps=['Vor dem Antrag kurz bei der Reklameaufsicht anrufen und das Vorhaben schildern.',
         'Antrag mit Ansichtszeichnung, Fassadenfoto mit Position, Material- und Lichtbeschreibung, Lageplan und Zustimmung des Eigentümers.',
         'Innenstadt: Den Stand der Gestaltungssatzung vor der Produktion prüfen – wir halten das für Sie im Blick.'],
  faq=[('Wer genehmigt in Essen eine Leuchtreklame?', 'Die Reklameaufsicht der Stadt Essen (Bauordnungsamt), Lindenallee 10, 45127 Essen.'),
       ('Was kostet die Genehmigung in Essen?', 'Nach Gebührentarif NRW 10 % der Herstellungssumme, mindestens 100 €.'),
       ('Gibt es in Essen schon eine Gestaltungssatzung für die Innenstadt?', 'Sie wird gerade aufgestellt; Beteiligungen liefen im Frühjahr 2026. Einen beschlossenen Satzungstext haben wir bis Oktober 2026 nicht gefunden.')],
  quellen=[('Stadt Essen – Gestaltungssatzung Innenstadt', 'https://www.essen.de/leben/planen_bauen_und_wohnen/innenstadt/innenstadt___gestaltung.de.html'),
           ('Stadt Essen – Pressemeldung zur Gestaltungssatzung', 'https://www.essen.de/meldungen/pressemeldung_1569220.de.html')]),

 dict(slug='bochum', stadt='Bochum', region='nrw', seite='/werbeagentur-bochum.html', bild='schaufenster',
  title='Werbeanlage in Bochum: Gestaltungssatzung Innenstadt, Genehmigung & Kosten (2026)',
  desc='Seit April 2024 gilt in der Bochumer Innenstadt die Gestaltungssatzung Nr. 1000 Gb – auch für Werbeanlagen. Was das für Ihr Schild bedeutet.',
  h1='Werbeanlage in Bochum:<br><em>Gestaltungssatzung</em><br>&amp; Genehmigung',
  kurz='Für die Bochumer Innenstadt gilt seit dem <strong>9. April 2024</strong> die überarbeitete <strong>Gestaltungssatzung Nr. 1000 Gb</strong>. Sie macht Vorgaben für Fassaden, <strong>Werbeanlagen</strong> und Außengastronomie. Außerhalb davon gilt die Landesbauordnung NRW.',
  lokal_h='Bochum: Satzung plus Gestaltungshandbuch',
  lokal=[
   'Der Rat hat die überarbeitete Satzung im März 2024 beschlossen. Satzungstext, Karte des Geltungsbereichs und Begründung stellt die Stadt auf ihrer Seite zum Bebauungsplan Nr. 1000 Gb bereit.',
   'Ergänzend gibt es ein <strong>Gestaltungshandbuch</strong> mit Beispielen. Es richtet sich an Eigentümer, Bauherren und Planer – und ist für Ladeninhaber die praktischste Hilfe, um ein Schild von Anfang an passend zu planen.',
   'Die Stadt berichtet, dass die Satzung bereits sichtbar wirkt, etwa rund um den Husemannplatz und die Massenbergstraße.'],
  warn='Liegt Ihr Geschäft im Geltungsbereich, gleichen Sie Größe, Lage und Beleuchtung Ihrer Werbeanlage vor der Produktion mit Satzung und Handbuch ab. Nachträgliche Änderungen sind teurer als eine kurze Prüfung.',
  raum='Für Werbung, die in den öffentlichen Raum ragt, oder Aufsteller vor dem Geschäft braucht es zusätzlich eine Sondernutzungserlaubnis der Stadt (Straßen- und Wegegesetz NRW).',
  tipps=['Zuerst prüfen, ob die Adresse im Geltungsbereich der Satzung 1000 Gb liegt.',
         'Das Gestaltungshandbuch als Vorlage nutzen – wir setzen die Vorgaben direkt im Entwurf um.',
         'Außerhalb der Innenstadt: bis 1 m² verfahrensfrei, darüber in der Regel Bauantrag.'],
  faq=[('Seit wann gilt die Gestaltungssatzung in Bochum?', 'Die überarbeitete Satzung Nr. 1000 Gb gilt seit dem 9. April 2024.'),
       ('Regelt die Satzung auch Schilder und Leuchtreklame?', 'Ja, Werbeanlagen gehören ausdrücklich dazu – neben Fassaden und Außengastronomie.'),
       ('Wo finde ich die Regeln?', 'Satzungstext, Karte und Gestaltungshandbuch stellt die Stadt Bochum online bereit.')],
  quellen=[('Stadt Bochum – Gestaltungshandbuch und Gestaltungssatzung Innenstadt', 'https://www.bochum.de/amt-fuer-stadtplanung-und-wohnen/Dienstleistungen-und-Infos/Stadterneuerung/ISEK-Innenstadt/Gestaltungshandbuch-und-Gestaltungssatzung-Innenstadt'),
           ('IHK Mittleres Ruhrgebiet – Gestaltungssatzung Innenstadt Bochum', 'https://www.ihk.de/bochum/hauptnavigation/branchenbetreuung/stadtentwicklung/stadt-und-quartiersentwicklung/gestaltungssatzung-bochum-6656476')]),

 dict(slug='hamburg', stadt='Hamburg', region='hamburg', seite='/werbeagentur-hamburg.html', bild='aussenwerbung',
  title='Werbeanlage in Hamburg: Bezirksamt, Sondernutzung & Kosten (2026)',
  desc='In Hamburg braucht Werbung oft zwei Erlaubnisse: Baurecht beim Bezirksamt und Sondernutzung für alles über dem Gehweg. So läuft es ab.',
  h1='Werbeanlage in Hamburg:<br><em>Bezirksamt</em><br>&amp; Sondernutzung',
  kurz='In Hamburg sind Werbeanlagen bis 1 m² nach der Hamburgischen Bauordnung genehmigungsfrei. <strong>Zwei Fallen:</strong> Erhaltungsverordnungen und Vorgaben der Bezirke können strenger sein – und alles, was in den öffentlichen Raum ragt, braucht <strong>immer</strong> eine Sondernutzungserlaubnis.',
  lokal_h='Hamburg: Baurecht und Wegerecht getrennt',
  lokal=[
   '<strong>Baurecht:</strong> Zuständig ist die Bauprüfabteilung des Bezirksamts, in dessen Bezirk Ihr Standort liegt. Werbeanlagen bis 1 m² Ansichtsfläche brauchen nach Anlage 2 zur HBauO keine Genehmigung; größere Anlagen auf privaten Grundstücken in der Regel eine Baugenehmigung. Jede Werbeanlage muss dabei die Anforderungen des § 13 HBauO erfüllen.',
   '<strong>Erhaltungsgebiete:</strong> In Gebieten mit städtebaulicher Erhaltungsverordnung und nach bezirklichen Vorgaben gelten oft strengere Regeln als in der Bauordnung – etwa zur Größe von Fassadenschildern oder dazu, bis zu welchem Geschoss Werbung reichen darf.',
   '<strong>Wegerecht:</strong> Werbung auf öffentlichem Grund braucht eine Sondernutzungserlaubnis nach dem Hamburgischen Wegegesetz. Das gilt auch für Schilder auf privatem Grund, die in den Luftraum über dem Gehweg ragen – etwa Ausleger. Die Erlaubnis erteilt das Bezirksamt, befristet und mit Auflagen.'],
  warn='Ein häufiger Fehler: Das Schild braucht keine Baugenehmigung – und trotzdem fehlt die Sondernutzungserlaubnis, weil es über den Gehweg ragt. Beides getrennt prüfen.',
  raum='Frei aufgestellte Werbetafeln auf dem Gehweg sind in Hamburg nach Angaben der Handelskammer grundsätzlich nicht erlaubt; Werbung auf öffentlichen Wegen ist zudem weitgehend an große Außenwerber vergeben. Für Ladeninhaber bleibt vor allem die Werbung an der eigenen Fassade – und die planen wir mit Ihnen.',
  tipps=['Zuerst klären: Liegt Ihr Laden in einem Erhaltungsgebiet? Dann gelten oft strengere Regeln als 1 m².',
         'Ausleger oder Nasenschild? Sondernutzungserlaubnis beim Bezirksamt von Anfang an einplanen.',
         'Antrag immer beim Bezirksamt des Standorts stellen – nicht beim Bezirk Ihres Firmensitzes.'],
  faq=[('Brauche ich in Hamburg für ein kleines Schild eine Genehmigung?', 'Bis 1 m² Ansichtsfläche ist keine Baugenehmigung nötig (Anlage 2 HBauO). In Erhaltungsgebieten können strengere Regeln gelten, und Schilder über dem Gehweg brauchen eine Sondernutzungserlaubnis.'),
       ('Wer ist zuständig?', 'Das Bezirksamt, in dessen Bezirk die Werbeanlage hängt – für die Baugenehmigung wie für die Sondernutzung.'),
       ('Darf ich einen Aufsteller vor meinen Laden stellen?', 'Nach Angaben der Handelskammer Hamburg sind frei aufgestellte Werbetafeln auf öffentlichen Wegen grundsätzlich nicht erlaubt.')],
  quellen=[('hamburg.de – Sondernutzungserlaubnis für Werbung im öffentlichen Raum', 'https://www.hamburg.de/service/info/111073031/n0/'),
           ('Handelskammer Hamburg – Außenwerbung', 'https://www.ihk.de/hamburg/produktmarken/beratung-service/recht-und-steuern/wirtschaftsrecht/gewerberecht/aussenwerbung-1156810'),
           ('Hamburg – Bauprüfdienst Werbeanlagen (PDF)', 'https://dokumente.hamburg.de/resource/blob/190466/267e443ff2b54e7ceb473a937b58a180/bpd-werbeanlagen-data.pdf')]),

 dict(slug='potsdam', stadt='Potsdam', region='berlin', seite='/werbetechnik-potsdam.html', bild='schilder',
  title='Werbeanlage in Potsdam: Werbesatzung Innenstadt, Genehmigung & Kosten (2026)',
  desc='Die Potsdamer Innenstadt hat eine eigene Werbesatzung – im Dezember 2025 neu gefasst. Was sie verlangt und wie Sie Ihre Werbeanlage beantragen.',
  h1='Werbeanlage in Potsdam:<br><em>Werbesatzung</em><br>Innenstadt',
  kurz='In der Potsdamer Innenstadt gilt eine eigene <strong>Werbesatzung</strong>. Ihr Grundprinzip ist <strong>Zurückhaltung</strong>: Werbung soll die Gestaltung der Straßen und Plätze nicht stören. Die 2. Änderung wurde am <strong>5. Dezember 2025</strong> beschlossen.',
  lokal_h='Potsdam: Werbesatzung und Gestaltungssatzungen',
  lokal=[
   'Die <strong>Werbesatzung, Teilbereich Innenstadt</strong>, soll die gestalterischen Qualitäten der öffentlichen Straßen und Plätze dauerhaft sichern. Rechtsgrundlage ist § 81 der Brandenburgischen Bauordnung (BbgBO), der Städten örtliche Bauvorschriften erlaubt.',
   'Nach der ersten Änderung von 2014 hat die Stadt die Satzung erneut überarbeitet; der Satzungsbeschluss zur 2. Änderung fiel am 5. Dezember 2025. Satzungstext, Karte und Begründung veröffentlicht die Stadt auf potsdam.de.',
   'Für einzelne Stadtteile gibt es zusätzlich Gestaltungssatzungen, zum Beispiel für die <strong>Berliner Vorstadt</strong>. Viele Gebäude in Potsdam stehen zudem unter Denkmalschutz – dann ist auch die Denkmalbehörde beteiligt.'],
  warn='Kleine Werbeanlagen können nach der Brandenburgischen Bauordnung verfahrensfrei sein. In der Innenstadt und in Gestaltungssatzungsgebieten gelten aber die strengeren örtlichen Regeln – prüfen Sie Ihren Standort vor der Bestellung.',
  raum='Für Werbung, die in den öffentlichen Straßenraum ragt, oder Aufsteller vor dem Geschäft ist zusätzlich eine straßenrechtliche Erlaubnis der Stadt nötig.',
  tipps=['Den Antrag auf Errichtung einer Werbeanlage stellen Sie bei der Landeshauptstadt Potsdam; die Unterlagen bereiten wir mit Ihnen vor.',
         'In der Innenstadt lieber kleine, hochwertige Einzelbuchstaben oder ein edles Schild als großflächige Leuchtkästen.',
         'Denkmal? Frühzeitig abstimmen – das verhindert Umplanungen.'],
  faq=[('Gibt es in Potsdam eine Werbesatzung?', 'Ja, für den Teilbereich Innenstadt. Die 2. Änderung wurde am 5. Dezember 2025 beschlossen.'),
       ('Was ist das Ziel der Satzung?', 'Die gestalterischen Qualitäten der Straßen und Plätze zu sichern – mit dem Grundprinzip der Zurückhaltung.'),
       ('Kommen Sie für Potsdam vor Ort?', 'Ja. Potsdam betreuen wir aus Berlin – mit Aufmaß und Montage vor Ort.')],
  quellen=[('Landeshauptstadt Potsdam – Werbesatzung Teilbereich Innenstadt', 'https://www.potsdam.de/de/werbesatzung-teilbereich-innenstadt'),
           ('Landeshauptstadt Potsdam – Satzungen aus dem Bau- und Planungsbereich', 'https://www.potsdam.de/de/satzungen-aus-dem-bau-und-planungsbereich'),
           ('Landeshauptstadt Potsdam – Werbeanlagen, Antrag auf Errichtung', 'https://vv.potsdam.de/vv/produkte/173010100000009433.php')]),
]

NRW_SEITE = '/werbeagentur-nrw.html'
STAEDTE += [
 dict(slug='duisburg', stadt='Duisburg', region='nrw', seite=NRW_SEITE, bild='aussenwerbung',
  title='Werbeanlage in Duisburg: Was genehmigungsfrei ist, Antrag & Kosten (2026)',
  desc='Duisburg listet genau auf, welche Werbeanlagen ohne Genehmigung gehen – bis 1 m², befristete Werbung bis zwei Monate. Was darüber gilt.',
  h1='Werbeanlage in Duisburg:<br><em>genehmigungsfrei</em><br>oder Antrag?',
  kurz='Die Bauaufsicht Duisburg nennt als genehmigungsfrei unter anderem <strong>Werbeanlagen bis 1 m²</strong> und <strong>befristete Werbung bis zu zwei Monate</strong>. Größere Anlagen brauchen einen Bauantrag – und in Gebieten mit Gestaltungssatzung gelten eigene Regeln.',
  lokal_h='Duisburg: Die Liste der Bauaufsicht',
  lokal=[
   'Auf ihrer Seite „Errichtung von Werbeanlagen“ fasst die Stadt Duisburg zusammen, welche Werbeanlagen nach der BauO NRW ohne Genehmigung errichtet werden dürfen: Werbeanlagen und Hinweiszeichen bis 1 m², vorübergehende Werbung (zum Beispiel für eine Eröffnung) bis zu zwei Monate und weitere Sonderfälle.',
   'Für einzelne Quartiere hat Duisburg Gestaltungssatzungen. Ein Beispiel ist die <strong>Margarethensiedlung</strong> in Rheinhausen: Die Satzung schützt das Erscheinungsbild der denkmalgeschützten Siedlung – dort sind auch kleine Schilder an die Vorgaben gebunden.',
   'Eine eigene Werbesatzung für die Duisburger Innenstadt haben wir bei unserer Recherche nicht gefunden. Wir prüfen trotzdem für jede Adresse, ob ein Bebauungsplan oder eine Satzung etwas regelt.'],
  warn='Die 1-m²-Grenze gilt für die Ansichtsfläche; mehrere Schilder nebeneinander werden zusammengerechnet. Drei Schilder à 0,4 m² sind also bereits genehmigungspflichtig.',
  raum='Für Ausleger über dem Gehweg, Aufsteller und Werbung auf öffentlichen Flächen braucht es eine Sondernutzungserlaubnis der Stadt (Straßen- und Wegegesetz NRW).',
  tipps=['Eröffnung geplant? Ein Banner für bis zu zwei Monate ist meist der schnellste Weg – danach kommt das dauerhafte Schild.',
         'Mehrere kleine Schilder an einer Fassade immer zusammenrechnen.',
         'Denkmal oder Siedlung mit Gestaltungssatzung? Vor dem Entwurf prüfen.'],
  faq=[('Welche Werbung ist in Duisburg genehmigungsfrei?', 'Nach der Übersicht der Stadt unter anderem Werbeanlagen bis 1 m² und vorübergehende Werbung bis zu zwei Monate.'),
       ('Gibt es in Duisburg Gestaltungssatzungen?', 'Ja, für einzelne Gebiete – zum Beispiel die Margarethensiedlung in Rheinhausen.'),
       ('Was kostet die Baugenehmigung?', 'Nach Gebührentarif NRW 10 % der Herstellungssumme, mindestens 100 €.')],
  quellen=[('Stadt Duisburg – Errichtung von Werbeanlagen', 'https://www.duisburg.de/vv/produkte/pro_du/dez_vii/errichtung_von_werbeanlagen.php'),
           ('Stadt Duisburg – Gestaltungssatzung Margarethensiedlung (PDF)', 'https://geoportal2.duisburg.de/scripts/pbv/showFile.php?id=3488')]),

 dict(slug='wuppertal', stadt='Wuppertal', region='nrw', seite=NRW_SEITE, bild='schaufenster',
  title='Werbeanlage in Wuppertal: Gestaltungssatzungen Elberfeld & Döppersberg (2026)',
  desc='Wuppertal regelt Werbung über mehrere Gestaltungssatzungen – etwa für Alte Freiheit/Poststraße und den Döppersberg. Was das für Ihr Schild heißt.',
  h1='Werbeanlage in Wuppertal:<br><em>Gestaltungssatzungen</em><br>&amp; Genehmigung',
  kurz='Wuppertal hat keine einzige stadtweite Werbesatzung, sondern <strong>mehrere Gestaltungssatzungen</strong> für bestimmte Gebiete – zum Beispiel für die Elberfelder City rund um <strong>Alte Freiheit / Poststraße</strong> und für den <strong>Döppersberg</strong>. Dort gelten eigene Regeln für Werbeanlagen.',
  lokal_h='Wuppertal: Satzungen nach Gebiet',
  lokal=[
   'Die Satzung für den Bereich <strong>Alte Freiheit – Poststraße</strong> in Elberfeld stammt von 1993 und wurde später geändert. Sie regelt ausdrücklich das Errichten und Ändern von Werbeanlagen; ein Anlass war, dass Werbung nach dem Bau der Fußgängerzone das Straßenbild zu dominieren begann.',
   'Für den <strong>Döppersberg</strong> rund um den Hauptbahnhof gibt es seit 2010 eine eigene Gestaltungssatzung mit Regeln für Fassaden- und Fensterwerbung.',
   'Daneben gibt es Erhaltungs- und Gestaltungssatzungen für Quartiere wie <strong>Robert-Koch-Platz</strong> oder <strong>Sedansberg</strong>. Dort gilt typischerweise: Werbung muss zum Charakter von Straße und Gebäude passen und ist nur im Erdgeschoss zulässig.'],
  warn='Welche Satzung gilt, hängt von der genauen Adresse ab. Wir prüfen den Geltungsbereich, bevor wir gestalten.',
  raum='Werbung, die in den öffentlichen Raum ragt, fällt unter die Wuppertaler Sondernutzungssatzung. Sie enthält auch Gebühren je m² für Werbeanlagen an Gebäuden in den Fußgängerzonen von Elberfeld und Barmen.',
  tipps=['Laden in der Elberfelder Fußgängerzone? Satzung Alte Freiheit/Poststraße vor dem Entwurf lesen.',
         'In Erhaltungsgebieten Werbung im Erdgeschoss planen – Obergeschosse sind meist tabu.',
         'Ausleger in Fußgängerzonen: Sondernutzungsgebühr in die Kalkulation einrechnen.'],
  faq=[('Hat Wuppertal eine Werbesatzung?', 'Es gibt mehrere gebietsbezogene Gestaltungssatzungen, unter anderem für Alte Freiheit/Poststraße und den Döppersberg.'),
       ('Darf ich in Wuppertal im Obergeschoss werben?', 'In Gebieten wie Robert-Koch-Platz oder Sedansberg ist Werbung nur im Erdgeschoss zulässig. Andernorts hängt es von Satzung und Bauordnung ab.'),
       ('Kostet ein Ausleger in der Fußgängerzone extra?', 'Ja, die Sondernutzungssatzung sieht Gebühren je m² für Werbeanlagen in den Fußgängerzonen von Elberfeld und Barmen vor.')],
  quellen=[('Wuppertal – Satzung Alte Freiheit / Poststraße (PDF)', 'https://www.wuppertal.de/rathaus-buergerservice/verwaltung/politik/stadtrecht-dokumente/alte-freiheit.pdf'),
           ('Wuppertal – Gestaltungssatzung Döppersberg (PDF)', 'https://www.wuppertal.de/rathaus-buergerservice/verwaltung/politik/stadtrecht-dokumente/doeppersberg.pdf'),
           ('Wuppertal – Sondernutzungssatzung (PDF)', 'https://www.wuppertal.de/rathaus-buergerservice/verwaltung/politik/stadtrecht-dokumente/6-00.pdf')]),

 dict(slug='bonn', stadt='Bonn', region='nrw', seite=NRW_SEITE, bild='schilder',
  title='Werbeanlage in Bonn: Gestaltungs- und Werbesatzungen Innenstadt & Bad Godesberg (2026)',
  desc='Bonn hat zwei Gestaltungs- und Werbesatzungen: für die Innenstadt und für Bad Godesberg. Was sie regeln und wie Sie Ihr Schild genehmigt bekommen.',
  h1='Werbeanlage in Bonn:<br><em>Innenstadt</em><br>&amp; Bad Godesberg',
  kurz='In Bonn gelten zwei eigene Satzungen: die <strong>Gestaltungs- und Werbesatzung Bonner Innenstadt</strong> (61-23) und die <strong>Gestaltungs- und Werbesatzung Bad Godesberg</strong> (61-26). Wer dort ein Schild plant, muss sich an deren Vorgaben halten.',
  lokal_h='Bonn: Zwei Zentren, zwei Satzungen',
  lokal=[
   'Die Satzung für die <strong>Bonner Innenstadt</strong> (vom 23. Juni 2015) soll das charakteristische Stadtbild mit seiner historischen Baustruktur wahren und den Kernbereich aufwerten.',
   'Die Satzung für <strong>Bad Godesberg</strong> schützt das Erscheinungsbild des Bezirkszentrums. Sie regelt Gestaltung und Größe von Werbeanlagen und auch Sondernutzungen wie Außengastronomie und Warenständer – mit dem Ziel einheitlicher, nachvollziehbarer Kriterien. Seit 2018 gilt sie unbefristet.',
   'Den Geltungsbereich und die Texte veröffentlicht die Stadt Bonn im Ortsrecht unter „Bauen und Stadtgestaltung“.'],
  warn='Liegt Ihr Laden in der Fußgängerzone oder im Zentrum von Bad Godesberg, passen wir Größe und Gestaltung direkt an die Satzung an – das spart Rückfragen im Verfahren.',
  raum='Warenständer, Aufsteller und Ausleger auf öffentlichen Flächen sind in Bonn Sondernutzungen; der Gebührentarif der Stadt nennt die Gebiete der Gestaltungs- und Werbesatzung ausdrücklich.',
  tipps=['Zuerst klären: Innenstadt, Bad Godesberg oder außerhalb beider Satzungen?',
         'In Bad Godesberg Werbeanlage und Außenmöblierung zusammen planen – beide stehen in derselben Satzung.',
         'Hochwertige, zurückhaltende Lösungen (Einzelbuchstaben, edles Schild) passen meist am besten.'],
  faq=[('Welche Werbesatzungen gibt es in Bonn?', 'Die Gestaltungs- und Werbesatzung Bonner Innenstadt (61-23) und die Gestaltungs- und Werbesatzung Bad Godesberg (61-26).'),
       ('Gilt die Bad Godesberger Satzung noch?', 'Ja, der Rat hat 2018 die Entfristung beschlossen.'),
       ('Was regelt die Satzung in Bad Godesberg?', 'Gestaltung und Größe von Werbeanlagen sowie Sondernutzungen wie Außengastronomie und Warenständer.')],
  quellen=[('Bonn – Gestaltungs- und Werbesatzung Bonner Innenstadt (61-23)', 'https://www.bonn.de/service-bieten/stadtpolitik-ortsrecht/ortsrecht/bauen-stadtgestaltung/gestaltungs-und-werbesatzung-bonner-innenstadt.php'),
           ('Bonn – Gestaltungs- und Werbesatzung Bad Godesberg (61-26)', 'https://www.bonn.de/service-bieten/stadtpolitik-ortsrecht/ortsrecht/bauen-stadtgestaltung/gestaltungs-und-werbesatzung-bad-godesberg.php')]),

 dict(slug='moenchengladbach', stadt='Mönchengladbach', region='nrw', seite=NRW_SEITE, bild='leuchtreklamen',
  title='Werbeanlage in Mönchengladbach: Werbeanlagensatzungen City & Rheydt (2026)',
  desc='In den Innenstädten von Mönchengladbach und Rheydt gelten Werbeanlagensatzungen – dort braucht jede Werbeanlage eine Genehmigung.',
  h1='Werbeanlage in Mönchengladbach:<br><em>City</em><br>&amp; Rheydt',
  kurz='Mönchengladbach hat <strong>zwei Werbeanlagensatzungen</strong>: für die Innenstadt Mönchengladbach (seit 1. November 2017) und für den Innenstadtkern Rheydt (seit 2016, 2018 überarbeitet). Laut Stadt sind Werbeanlagen in einem Satzungsgebiet <strong>nicht genehmigungsfrei</strong>.',
  lokal_h='Mönchengladbach: Satzungen und Handbücher',
  lokal=[
   'Die Satzung „Gestaltung von Werbeanlagen und Warenautomaten im Innenstadtkern <strong>Rheydt</strong>“ gilt seit dem 1. Januar 2016. Nach einer Evaluierung hat der Rat sie im Mai 2018 mit Anpassungen erneut beschlossen.',
   'Für die <strong>Innenstadt Mönchengladbach</strong> gilt eine entsprechende Satzung seit dem 1. November 2017. Zu beiden Satzungen gibt die Stadt Handbücher heraus, die die Regeln mit Beispielen erklären.',
   'Bestehende, genehmigte Werbeflächen haben Bestandsschutz. Neue Schilder und Änderungen an bestehenden müssen vorher genehmigt werden.'],
  warn='Ein Teil der Rheydter Innenstadt steht zusätzlich als Denkmalbereich unter Schutz – dann brauchen auch viele Änderungen an der Fassade eine Erlaubnis der Stadt.',
  raum='Für Waren- und Werbeständer im öffentlichen Raum hat Mönchengladbach eine eigene Richtlinie; Ausleger über dem Gehweg brauchen eine Sondernutzungserlaubnis.',
  tipps=['Laden in der City oder in Rheydt? Für jede neue Werbeanlage einen Antrag einplanen.',
         'Das Handbuch der Stadt als Gestaltungsvorlage nutzen – wir setzen es im Entwurf um.',
         'Bestehendes Schild ändern? Auch das ist genehmigungspflichtig, der Bestandsschutz gilt nur unverändert.'],
  faq=[('Brauche ich in der Mönchengladbacher Innenstadt für jedes Schild eine Genehmigung?', 'Ja. Laut Stadt sind Werbeanlagen im Geltungsbereich einer Werbeanlagensatzung nicht genehmigungsfrei.'),
       ('Seit wann gelten die Satzungen?', 'Rheydt seit 1. Januar 2016 (2018 erneut beschlossen), Innenstadt Mönchengladbach seit 1. November 2017.'),
       ('Was ist mit meinem alten Schild?', 'Genehmigte Bestandsanlagen haben Bestandsschutz; Änderungen brauchen eine neue Genehmigung.')],
  quellen=[('Mönchengladbach – Werbeanlagensatzungen', 'https://www.moenchengladbach.de/rathaus/buergerinfo-a-z/planen-bauen-mobilitaet-umwelt-dezernat-vi/fachbereich-stadtentwicklung-und-planung-61/abteilung-bauleitplanung-und-stadtgestaltung/stadtgestaltung/werbeanlagensatzungen'),
           ('Mönchengladbach – Werbeanlage (Weg zur Baugenehmigung)', 'https://www.moenchengladbach.de/rathaus/buergerinfo-a-z/planen-bauen-mobilitaet-umwelt-dezernat-vi/fachbereich-bauordnung-und-denkmalschutz-63/der-weg-zur-baugenehmigung/werbeanlage'),
           ('Mönchengladbach – Richtlinie Außengastronomie und Waren-/Werbeständer', 'https://www.moenchengladbach.de/rathaus/buergerinfo-a-z/planen-bauen-mobilitaet-umwelt-dezernat-vi/fachbereich-stadtentwicklung-und-planung-61/abteilung-bauleitplanung-und-stadtgestaltung/stadtgestaltung/richtlinie-fuer-aussengastronomie-und-waren-/werbestaender')]),

 dict(slug='krefeld', stadt='Krefeld', region='nrw', seite=NRW_SEITE, bild='schaufenster',
  title='Werbeanlage in Krefeld: Werbeanlagensatzung Innenstadt & Uerdingen (2026)',
  desc='Innerhalb der Krefelder Wälle gilt eine Werbeanlagensatzung: fast jede Werbeanlage braucht eine Genehmigung, grelle Farben sind tabu.',
  h1='Werbeanlage in Krefeld:<br><em>Werbeanlagensatzung</em><br>Innenstadt',
  kurz='In der Krefelder Innenstadt – innerhalb der <strong>vier Wälle</strong> – gilt eine eigene <strong>Werbeanlagensatzung</strong>. Laut Stadt muss dort fast jede Werbeanlage genehmigt werden; Werbung soll sich den Gebäuden unterordnen, <strong>grelle, Leucht- und Signalfarben</strong> sind nicht zulässig.',
  lokal_h='Krefeld: Innenstadt, Uerdingen, Bruchfeld',
  lokal=[
   'Die „Satzung über die Werbeanlagen und Warenautomaten für die Innenstadt Krefeld“ (Ortsrecht 6.10) gilt für den Bereich der Wälle – Westwall, Nordwall, Ostwall und Südwall – samt Bahnhofsumfeld. Sie stammt von 1996 und regelt Zahl, Gestaltung und Größe von Werbeanlagen.',
   'In einem Bericht zur „Gestaltungsoffensive Innenstadt“ werden Beispiele genannt, etwa Schrifthöhen bis <strong>40 cm</strong> oder Werbeflächen bis <strong>0,4 m² je laufendem Meter Schaufenster</strong>. Maßgeblich ist der Satzungstext.',
   'Weitere Werbeanlagensatzungen gibt es für den <strong>historischen Ortskern Uerdingen</strong> (6.26), für <strong>Bruchfeld</strong> (6.08) und für Gewerbe- und Industriegebiete (6.09). Ergänzend hat die Stadt Gestaltungsleitlinien veröffentlicht.'],
  warn='Neueröffnung oder neue Fassade in der Innenstadt? Dann laut Stadt immer einen Antrag stellen – auch für kleine Schilder.',
  raum='Für Werbung, die in den öffentlichen Raum ragt, und Aufsteller vor dem Geschäft braucht es zusätzlich eine Sondernutzungserlaubnis.',
  tipps=['Farbwahl früh klären: Neon- und Signalfarben sind in der Innenstadt nicht erlaubt.',
         'Schrifthöhe und Fläche am Schaufenster ausmessen und mit der Satzung abgleichen.',
         'In Uerdingen gilt eine eigene Satzung für den historischen Ortskern.'],
  faq=[('Brauche ich in der Krefelder Innenstadt eine Genehmigung für mein Schild?', 'Laut Stadt muss fast jede Werbeanlage innerhalb der Wälle genehmigt werden.'),
       ('Sind Leuchtfarben erlaubt?', 'Nein, grelle Farben sowie Leucht- und Signalfarben sind in der Innenstadt nicht zulässig.'),
       ('Gibt es weitere Satzungen in Krefeld?', 'Ja, unter anderem für den historischen Ortskern Uerdingen, für Bruchfeld und für Gewerbegebiete.')],
  quellen=[('Krefeld – Werbeanlagensatzung Innenstadt 6.10 (PDF)', 'https://service.krefeld.de/system/files/2024-05/6.10-satzung_ueber_die_werbeanlagen_und_warenautomaten_fuer_die_innenstadt_krefeld.pdf'),
           ('Krefeld – Gestaltungsoffensive Innenstadt', 'https://www.krefeld.de/de/inhalt/gestaltungsoffensive-innenstadt-stadt-macht-auf-regeln-aufmerksam/&s93=16'),
           ('Krefeld – Werbeanlagensatzung Uerdingen 6.26 (PDF)', 'https://service.krefeld.de/system/files/2024-08/6.26_werbeanlagensatzung_historischer_ortskern_krefeld-uerdingen.pdf')]),

 dict(slug='neuss', stadt='Neuss', region='nrw', seite=NRW_SEITE, bild='schilder',
  title='Werbeanlage in Neuss: Werbeanlagensatzung Innenstadt, Genehmigung & Kosten (2026)',
  desc='Die Neusser Werbeanlagensatzung verlangt, dass sich Werbung in Anzahl, Maßstab und Erscheinungsbild ins Stadtbild einfügt. Was das praktisch heißt.',
  h1='Werbeanlage in Neuss:<br><em>Werbeanlagensatzung</em><br>Innenstadt',
  kurz='Für die Innenstadt Neuss gilt die <strong>Werbeanlagensatzung</strong> (Ortsrecht 61/05). Ihr Grundsatz: Werbeanlagen und Schaukästen sollen sich in <strong>Anzahl, Maßstab und Erscheinungsform</strong> in das Stadtbild einfügen.',
  lokal_h='Neuss: Die Werbeanlagensatzung',
  lokal=[
   'Die „Satzung über die äußere Gestaltung und die besonderen Anforderungen an Werbeanlagen und Schaukästen im Bereich der Innenstadt Neuss“ stammt vom 24. Oktober 2001 und wurde 2005 geändert. Sie gilt für das Errichten und Ändern von Werbeanlagen im Sinne der BauO NRW.',
   'Die Stadt stellt die aktuelle Fassung im Ortsrecht und auf der Seite der Stadtplanung als PDF bereit.',
   'Praktisch heißt das: Schilder, Leuchtreklame und Schaukästen werden auf die Fassade abgestimmt – nicht jede Fläche darf beklebt oder beleuchtet werden.'],
  warn='Ob Ihre Adresse im Geltungsbereich liegt, steht in der Satzung. Wir prüfen das vor dem Entwurf.',
  raum='Für Werbung über dem Gehweg und Aufsteller braucht es zusätzlich eine Sondernutzungserlaubnis der Stadt Neuss.',
  tipps=['Schaukästen fallen ausdrücklich unter die Satzung – auch Speisekarten-Kästen von Restaurants.',
         'Lieber eine klare, gut lesbare Werbeanlage als viele kleine.',
         'Außerhalb der Innenstadt gilt die BauO NRW: bis 1 m² verfahrensfrei.'],
  faq=[('Hat Neuss eine Werbesatzung?', 'Ja, die Werbeanlagensatzung für die Innenstadt (Ortsrecht 61/05).'),
       ('Was verlangt die Satzung?', 'Dass sich Werbeanlagen und Schaukästen in Anzahl, Maßstab und Erscheinungsform ins Stadtbild einfügen.'),
       ('Gilt sie auch für Schaukästen?', 'Ja, Schaukästen sind ausdrücklich genannt.')],
  quellen=[('Neuss – Ortsrecht', 'https://www.neuss.de/rathaus/ortsrecht'),
           ('Neuss – Stadtplanung und -entwicklung', 'https://www.neuss.de/infos/stadtplanung')]),

 dict(slug='muelheim', stadt='Mülheim an der Ruhr', region='nrw', seite='/werbeagentur-muelheim.html', bild='schaufenster',
  title='Werbeanlage in Mülheim an der Ruhr: Gestaltungssatzung Innenstadt (2026)',
  desc='In der Mülheimer Innenstadt brauchen Werbeanlagen über 1 m² eine Baugenehmigung, Schaufensterwerbung bleibt im Erdgeschoss. Die Regeln im Überblick.',
  h1='Werbeanlage in Mülheim:<br><em>Gestaltungssatzung</em><br>Innenstadt',
  kurz='Für die Mülheimer Innenstadt gilt eine <strong>Gestaltungssatzung</strong> (vom 25. März 2011). Seit 2019 brauchen dort Werbeanlagen <strong>über 1 m²</strong> eine Baugenehmigung; Werbung in Fenstern ist auf das <strong>Erdgeschoss</strong> beschränkt.',
  lokal_h='Mülheim: Was die Satzung konkret regelt',
  lokal=[
   'Die Satzung soll den Bezug zwischen Erdgeschoss und Obergeschossen erhalten. Werbeanlagen, die diesen Zusammenhang stören, sind nicht zulässig.',
   '<strong>Fenster:</strong> Werbung in oder hinter Fenstern ist auf die Erdgeschosszone beschränkt; eine dauerhafte großflächige Beklebung der Fenster als Werbung ist nicht erlaubt – Ausnahmen gibt es für zeitlich begrenzte Aktionen.',
   '<strong>Vordächer und Markisen:</strong> Zusätzliche Ausleger, Werbe-Konsolen und Strahler an Vordächern sind nicht zulässig. Werbung auf Stadtmobiliar wie Bänken oder Masten ist ebenfalls ausgeschlossen.'],
  warn='Die Stadt Mülheim stellt Satzung und eine Broschüre „Bauen in Mülheim – Werbeanlagen“ online bereit. Wir richten Entwurf und Antrag danach aus.',
  raum='Die Sondernutzungssatzung (Fassung vom 23. Juni 2023) erlaubt Werbeanlagen an der Stätte der Leistung, die höchstens 0,30 m in den Verkehrsraum ragen, ohne Sondernutzungserlaubnis. Was weiter auskragt, braucht eine Erlaubnis.',
  tipps=['Schaufenster nicht dauerhaft vollflächig bekleben – lieber Logo, Öffnungszeiten und gezielte Akzente.',
         'Nasenschild? Auf maximal 0,30 m Auskragung achten oder Sondernutzung beantragen.',
         'Werbung nur im Erdgeschoss planen.'],
  faq=[('Ab wann brauche ich in der Mülheimer Innenstadt eine Genehmigung?', 'Seit 2019 für Werbeanlagen über 1 m² im Geltungsbereich der Gestaltungssatzung.'),
       ('Darf ich mein Schaufenster komplett bekleben?', 'Dauerhaft großflächig nicht; Ausnahmen gelten für zeitlich begrenzte Aktionen.'),
       ('Wie weit darf ein Schild über den Gehweg ragen?', 'Ohne Sondernutzungserlaubnis höchstens 0,30 m (Werbeanlage an der Stätte der Leistung).')],
  quellen=[('Mülheim – Gestaltungssatzung für die Innenstadt', 'https://cms.muelheim-ruhr.de/gestaltungssatzung-fuer-die-innenstadt'),
           ('Mülheim – Bauen in Mülheim: Werbeanlagen (PDF)', 'https://cms.muelheim-ruhr.de/sites/default/files/2025-10/4%20Werbeanlagen_.pdf'),
           ('Mülheim – Sondernutzungssatzung', 'https://cms.muelheim-ruhr.de/ortsrecht/sondernutzungssatzung')]),

 dict(slug='herne', stadt='Herne', region='nrw', seite='/werbeagentur-herne.html', bild='leuchtreklamen',
  title='Werbeanlage in Herne: Gestaltungssatzungen Herne-Mitte & Wanne (2026)',
  desc='Herne hat Gestaltungssatzungen für die Innenstädte Herne-Mitte und Wanne. Blinkende und bewegte Werbung ist dort nicht zulässig.',
  h1='Werbeanlage in Herne:<br><em>Herne-Mitte</em><br>&amp; Wanne',
  kurz='In Herne gelten <strong>Gestaltungssatzungen</strong> für die Innenstadt <strong>Herne-Mitte</strong> (rund um die Bahnhofstraße) und für die Innenstadt <strong>Wanne</strong>, beide vom 26. Oktober 2021. Sie regeln auch Werbeanlagen – <strong>animierte, blinkende oder bewegte Werbung</strong> ist nicht zulässig.',
  lokal_h='Herne: Was die Satzungen regeln',
  lokal=[
   'Die Satzung für <strong>Herne-Mitte</strong> beschreibt die Bahnhofstraße und ihr Umfeld als Zentrum der Innenstadt. Sie schließt bestimmte Anbringungsorte für Werbung aus und verbietet animierte Werbeanlagen, Lichtprojektionen sowie bewegliche oder veränderliche Werbung – also etwa Blinkwerbung, Wechsellicht und Laufschriften.',
   'Ziel ist laut Amtsblatt, Veränderungen zu vermeiden, die das Bild der Innenstadt beeinträchtigen, und die Identität der Innenstadt durch gute Gestaltung zu stärken.',
   'Für <strong>Wanne</strong> gab es schon 2016 eine erste Gestaltungssatzung zur Werbung. Die Stadt arbeitet an einer Neufassung und hat dazu Bürgerinnen und Bürger beteiligt – unter anderem bei einem Stadtspaziergang, bei dem Werbeanlagen Thema waren.'],
  warn='Laufschrift oder animiertes LED-Display geplant? In den Innenstädten von Herne nicht zulässig – statische Leuchtbuchstaben sind die passende Alternative.',
  raum='Für Werbung, die in den öffentlichen Raum ragt, und Aufsteller braucht es eine Sondernutzungserlaubnis der Stadt Herne.',
  tipps=['Bahnhofstraße oder Wanne-Mitte? Satzung vor dem Entwurf prüfen.',
         'Statische Leuchtreklame statt Blink- oder Wechsellicht.',
         'Für Wanne den Stand der Neufassung im Blick behalten.'],
  faq=[('Gibt es in Herne Gestaltungssatzungen?', 'Ja, für die Innenstädte Herne-Mitte und Wanne, jeweils vom 26. Oktober 2021.'),
       ('Ist Blinkwerbung erlaubt?', 'Nein, animierte, bewegliche und veränderliche Werbung ist in den Satzungsgebieten nicht zulässig.'),
       ('Kommen Sie für Herne vor Ort?', 'Ja, unser Team in NRW übernimmt Aufmaß und Montage.')],
  quellen=[('Herne – Gestaltungssatzung Innenstadt Herne-Mitte (PDF)', 'https://www.herne.de/PDF/Ortsrecht/6-Bauverwaltung/6_11.pdf'),
           ('Herne – Gestaltungssatzung Innenstadt Wanne (PDF)', 'https://www.herne.de/PDF/Ortsrecht/6-Bauverwaltung/6_08.pdf'),
           ('Herne – Beteiligung zur neuen Gestaltungssatzung Wanne', 'https://www.herne.de/Meldungen/News-Detailansicht_294209.html')]),

 dict(slug='gelsenkirchen', stadt='Gelsenkirchen', region='nrw', seite=NRW_SEITE, bild='aussenwerbung',
  title='Werbeanlage in Gelsenkirchen: Gestaltungssatzung City/Altstadt (2026)',
  desc='Für die Gelsenkirchener City/Altstadt gibt es seit 2006 eine Gestaltungssatzung mit einem eigenen Kapitel zur Außenwerbung. Was Sie wissen sollten.',
  h1='Werbeanlage in Gelsenkirchen:<br><em>City</em><br>&amp; Altstadt',
  kurz='Für die <strong>City/Altstadt</strong> von Gelsenkirchen gibt es eine <strong>Gestaltungssatzung</strong> (2006 verabschiedet) mit einem eigenen Kapitel zur <strong>Außenwerbung</strong> sowie Regeln zu Markisen und Vordächern. Außerhalb gilt die BauO NRW.',
  lokal_h='Gelsenkirchen: Satzung, Fibel und Beratung',
  lokal=[
   'Die Gestaltungssatzung für die Hauptgeschäftslage der City ist Teil eines Pakets: verbindliche Festsetzungen, Empfehlungen, eine <strong>Gestaltungsfibel</strong> und eine Bau- und Gestaltungsberatung.',
   'Inhaltlich enthält die Satzung einen Abschnitt zur Außenwerbung, Regeln zu Markisen und Vordächern und zu Werbung an einzelnen Gebäudeteilen sowie eine Regelung für Ausnahmen.',
   'Eine eigene Satzung für Buer haben wir bei unserer Recherche nicht gefunden. Wir prüfen für jede Adresse, ob Bebauungsplan oder Satzung etwas vorschreiben.'],
  warn='Gerade bei Markisen und Vordächern lohnt sich der Blick in die Satzung – sie werden in der City zusammen mit der Werbung geregelt.',
  raum='Für Ausleger über dem Gehweg und Aufsteller braucht es eine Sondernutzungserlaubnis der Stadt (Straßen- und Wegegesetz NRW).',
  tipps=['Laden in der City/Altstadt? Gestaltungsfibel als Vorlage nutzen.',
         'Werbung, Markise und Vordach gemeinsam planen.',
         'Für Abweichungen gibt es eine Ausnahmeregelung – mit gut begründetem Entwurf.'],
  faq=[('Gibt es in Gelsenkirchen eine Gestaltungssatzung?', 'Ja, für die City/Altstadt; sie wurde 2006 verabschiedet.'),
       ('Regelt sie auch Werbung?', 'Ja, mit einem eigenen Kapitel zur Außenwerbung sowie Regeln zu Markisen und Vordächern.'),
       ('Was kostet die Genehmigung?', 'Nach Gebührentarif NRW 10 % der Herstellungssumme, mindestens 100 €.')],
  quellen=[('Nationale Stadtentwicklungspolitik – Gelsenkirchen „City“', 'https://www.nationale-stadtentwicklungspolitik.de/NSP/SharedDocs/Projekte/WSProjekte_DE/Gelsenkirchen_City.html')]),

 dict(slug='oberhausen', stadt='Oberhausen', region='nrw', seite=NRW_SEITE, bild='schaufenster',
  title='Werbeanlage in Oberhausen: Genehmigung, Innenstadt & Sterkrade (2026)',
  desc='Ab welcher Größe Werbung in Oberhausen genehmigt werden muss, was in Alt-Oberhausen und Sterkrade gilt und wie Sie den Antrag stellen.',
  h1='Werbeanlage in Oberhausen:<br><em>Innenstadt</em><br>&amp; Sterkrade',
  kurz='Die Bauordnung der Stadt Oberhausen weist darauf hin, dass Werbeanlagen ab einer bestimmten Größe genehmigt werden müssen – nach BauO NRW in der Regel über 1 m². Für die Innenstadt von <strong>Alt-Oberhausen</strong> gibt es eine <strong>Gestaltungssatzung</strong> mit Schwerpunkt Werbeanlagen, Fassaden und Außengastronomie.',
  lokal_h='Oberhausen: Innenstadt und Sterkrade',
  lokal=[
   'Für die Innenstadt von Alt-Oberhausen nennt das Stadtmagazin eine Gestaltungssatzung, die Werbeanlagen, Fassaden und Außengastronomie regelt. Für die Umgestaltung der Marktstraße liegt zudem ein Nutzungs- und Gestaltungskonzept vor.',
   'In <strong>Sterkrade</strong> fördert die Stadt mit einem <strong>Fassaden- und Hofprogramm</strong> unter anderem das Entfernen veralteter Werbeanlagen und Vordächer. Das ist keine Satzung, sondern eine Förderung – für Eigentümer kann sich eine Modernisierung dadurch lohnen.',
   'Den aktuellen Satzungstext für Alt-Oberhausen prüfen wir für Ihre Adresse vor dem Entwurf.'],
  warn='Sie modernisieren in Sterkrade? Fragen Sie bei der Stadt nach dem Fassaden- und Hofprogramm, bevor Sie alte Werbeanlagen entfernen lassen.',
  raum='Für Ausleger über dem Gehweg und Aufsteller braucht es eine Sondernutzungserlaubnis der Stadt (Straßen- und Wegegesetz NRW).',
  tipps=['Alt-Oberhausen: Werbung, Fassade und Außengastronomie zusammen planen.',
         'Sterkrade: Förderprogramm für Fassaden prüfen.',
         'Mehrere Schilder an einer Fassade zusammenrechnen (1-m²-Grenze).'],
  faq=[('Ab wann brauche ich in Oberhausen eine Genehmigung?', 'Nach BauO NRW in der Regel für Werbeanlagen über 1 m²; in Satzungsgebieten können strengere Regeln gelten.'),
       ('Gibt es eine Gestaltungssatzung?', 'Für die Innenstadt von Alt-Oberhausen, mit Schwerpunkt Werbeanlagen, Fassaden und Außengastronomie.'),
       ('Gibt es Förderung für neue Fassaden?', 'In Sterkrade gibt es ein Fassaden- und Hofprogramm der Stadt.')],
  quellen=[('Stadt Oberhausen – Werbeanlagen (Bauordnung)', 'https://www.oberhausen.de/de/index/rathaus/verwaltung/stadtplanung-bauen-mobilitat-umwelt/bauordnung/werbeanlagen.php'),
           ('Stadt Oberhausen – Fassaden- und Hofprogramm Sterkrade', 'https://www.oberhausen.de/de/index/rathaus/aktuelle-pressemeldungen/meldungen-2018/fassaden_und_hofprogramm_fuer_sterkrade.php?pagePresse=8')]),

 dict(slug='bottrop', stadt='Bottrop', region='nrw', seite='/werbeagentur-bottrop.html', bild='schilder',
  title='Werbeanlage in Bottrop: Genehmigung, Straßenbenutzung & Kosten (2026)',
  desc='In Bottrop dürfen Werbeanlagen am Geschäft bis 0,30 m in die Straße ragen, wenn 1,50 m Gehweg frei bleiben. Was sonst gilt.',
  h1='Werbeanlage in Bottrop:<br><em>Genehmigung</em><br>&amp; Gehweg',
  kurz='In Bottrop gilt für Werbeanlagen die BauO NRW (bis 1 m² verfahrensfrei). Für den Gehweg regelt die <strong>Straßenbenutzungs-Satzung</strong>: Werbung an der Stätte der Leistung darf ohne Erlaubnis bis <strong>0,30 m</strong> in die Straße ragen, wenn mindestens <strong>1,50 m</strong> Gehweg frei bleiben.',
  lokal_h='Bottrop: Innenstadt im Umbau',
  lokal=[
   'Für die Bottroper Innenstadt hat der Rat im Dezember 2023 ein integriertes Entwicklungskonzept beschlossen und das Rathausviertel zum Stadtumbaugebiet erklärt.',
   'Für den Bebauungsplan „Trapez“ in der Innenstadt sind gestalterische Vorschriften für Werbeanlagen vorgesehen. Eine eigenständige Werbesatzung für die gesamte Innenstadt haben wir bei unserer Recherche nicht gefunden.',
   'Für einzelne Siedlungen – etwa die Siedlung Kleiststraße – gibt es Erhaltungs- und Gestaltungssatzungen, die auch das Anbringen von Werbeanlagen erfassen.'],
  warn='In Fußgängerzonen und verkehrsberuhigten Bereichen muss laut Straßenbenutzungs-Satzung zusätzlich ein 1,50 m breiter Streifen für Feuerwehr, Rettung und Lieferverkehr frei bleiben.',
  raum='Was über 0,30 m hinausragt oder den freien Gehweg einschränkt, braucht eine Erlaubnis nach der Straßenbenutzungs-Satzung der Stadt Bottrop.',
  tipps=['Nasenschild: Auskragung und Restbreite des Gehwegs vorher messen.',
         'Im Bereich Bebauungsplan „Trapez“ die Gestaltungsvorgaben prüfen.',
         'Siedlung mit Gestaltungssatzung? Auch kleine Schilder abstimmen.'],
  faq=[('Wie weit darf mein Schild in Bottrop in den Gehweg ragen?', 'Ohne Erlaubnis bis 0,30 m, wenn mindestens 1,50 m Gehweg frei bleiben.'),
       ('Gibt es eine Werbesatzung für die Innenstadt?', 'Eine eigenständige haben wir nicht gefunden; für den Bebauungsplan „Trapez“ sind gestalterische Vorgaben vorgesehen.'),
       ('Kommen Sie für Bottrop vor Ort?', 'Ja, unser Team in NRW übernimmt Aufmaß und Montage.')],
  quellen=[('Stadt Bottrop – Straßenbenutzungs-Satzung', 'https://www.bottrop.de/rathaus/ortsrecht/ordnung/Strassenbenutzungs-Satzung-2019.php'),
           ('Stadt Bottrop – Bebauungsplan „Trapez“ (PDF)', 'https://www.o-sp.de/download/bottrop/142851'),
           ('Stadt Bottrop – Satzung „Kleiststraße“', 'https://www.bottrop.de/rathaus/bekanntmachungen/2020/2020-032.php')]),

 dict(slug='leverkusen', stadt='Leverkusen', region='nrw', seite=NRW_SEITE, bild='aussenwerbung',
  title='Werbeanlage in Leverkusen: Gestaltungsregeln Wiesdorf, Genehmigung & Kosten (2026)',
  desc='Für die Wiesdorfer City gibt es neue Gestaltungsregeln und eine Fibel für Händler. Was für Schilder und Leuchtreklame in Leverkusen gilt.',
  h1='Werbeanlage in Leverkusen:<br><em>Wiesdorf</em><br>&amp; Genehmigung',
  kurz='In Leverkusen gilt für Werbeanlagen die BauO NRW (bis 1 m² verfahrensfrei). Für die <strong>Wiesdorfer City</strong> hat der Rat ein <strong>Gestaltungshandbuch</strong> für den öffentlichen Raum beschlossen; dazu kommt eine <strong>Gestaltungsfibel für Händler und Gastronomen</strong>.',
  lokal_h='Leverkusen: Neue Gestaltungsregeln für Wiesdorf',
  lokal=[
   'Das Gestaltungshandbuch für den öffentlichen Raum in Wiesdorf ist eine verbindliche Leitlinie für Materialien, Möblierung und Beleuchtung. Es soll auch privaten Investoren und Geschäftsleuten als Orientierung dienen.',
   'Ergänzend hat die Stadt eine Gestaltungsfibel für Gewerbetreibende und Gastronomen vorgestellt. Sie zeigt, wie Ladenfronten und Außenbereiche zum neuen Stadtbild passen.',
   'Eine eigene Werbeanlagensatzung für Leverkusen haben wir bei unserer Recherche nicht gefunden. Wir prüfen für Ihre Adresse Bebauungsplan und örtliche Vorschriften.'],
  warn='Ob das Handbuch für Werbeanlagen rechtlich bindend ist, geht aus den Quellen nicht hervor. Wer in Wiesdorf ein Schild plant, fährt aber gut damit, sich an der Fibel zu orientieren.',
  raum='Für Ausleger über dem Gehweg und Aufsteller braucht es eine Sondernutzungserlaubnis der Stadt (Straßen- und Wegegesetz NRW).',
  tipps=['Laden in Wiesdorf? Gestaltungsfibel für Händler als Vorlage nutzen.',
         'Mehrere Schilder an einer Fassade zusammenrechnen (1-m²-Grenze).',
         'Leuchtreklame über 1 m²: Bauantrag einplanen.'],
  faq=[('Gibt es in Leverkusen eine Werbesatzung?', 'Eine eigene Werbeanlagensatzung haben wir nicht gefunden; für Wiesdorf gibt es ein Gestaltungshandbuch und eine Fibel für Händler.'),
       ('Ab wann brauche ich eine Genehmigung?', 'Nach BauO NRW in der Regel für Werbeanlagen über 1 m².'),
       ('Was kostet die Genehmigung?', 'Nach Gebührentarif NRW 10 % der Herstellungssumme, mindestens 100 €.')],
  quellen=[('Radio Leverkusen – Neue Gestaltungsregeln für die Wiesdorfer City', 'https://www.radioleverkusen.de/artikel/leverkusen-neue-gestaltungsregeln-fuer-wiesdorfer-city-2653953'),
           ('Leverkusen – Neues Gestaltungshandbuch für Wiesdorf', 'https://www.leverkusen.com/presse/neues-gestaltungshandbuch-soll-leverkusen-wiesdorf-ein-einheitliches-stadtbild-geben-00050365.html')]),
]


def nachbarn(c, n=5):
    """Bis zu n andere Ratgeber: zuerst dieselbe Region, dann der Rest – in fester Reihenfolge."""
    i = [o['slug'] for o in STAEDTE].index(c['slug'])
    ring = STAEDTE[i + 1:] + STAEDTE[:i]
    gleich = [o for o in ring if o['region'] == c['region']]
    rest = [o for o in ring if o['region'] != c['region']]
    return (gleich + rest)[:n]


def artikel(c):
    # Kurzer Suchergebnis-Titel (≤ 60 Zeichen); der lange Titel bleibt für die Überschrift im JSON-LD erhalten
    c = dict(c, title=f"Werbeanlage {c['stadt'].replace(' an der Ruhr', '')}: Satzung, Genehmigung & Kosten")
    s = c['stadt']; url = f"https://masar-werbeagentur.de/blog/werbeanlage-{c['slug']}.html"
    nrw = c['region'] == 'nrw'; preise = BER_PREISE if c['region'] == 'berlin' else NRW_PREISE
    team = {'nrw': 'unser Team in NRW', 'hamburg': 'unser Team in Hamburg', 'berlin': 'unser Team aus Berlin'}[c['region']]
    recht = NRW_RECHT.format(stadt=s) if nrw else ''
    geb = NRW_GEB if nrw else 'Die Gebühr für die Baugenehmigung richtet sich nach der jeweiligen Gebührenordnung; wir nennen sie Ihnen vorab mit dem Angebot.'
    wa = f"https://wa.me/{WA}?text=" + re.sub(' ', '%20', f'Hallo, ich plane eine Werbeanlage in {s}.')
    rows = ''.join(f'<tr><td>{e(a)}</td><td class="pcell">{e(b)} netto</td></tr>' for a, b in preise)
    faq_html = ''.join(f'<h3>{e(q)}</h3><p>{e(a)}</p>' for q, a in c['faq'])
    quellen = ''.join(f'<li><a href="{u}" target="_blank" rel="noopener noreferrer">{e(t)}</a></li>' for t, u in c['quellen'])
    tipps = ''.join(f'<li>{t}</li>' for t in c['tipps'])
    lokal = ''.join(f'<p>{p}</p>' for p in c['lokal'])
    img = c['bild']
    body = f'''
<header class="article-header" id="main-content">
  <div class="container">
    <nav aria-label="Breadcrumb" style="position:static;height:auto;z-index:auto;box-shadow:none;backdrop-filter:none;background:transparent;border-bottom:none;margin-bottom:1.5rem;">
      <ol style="list-style:none;display:flex;flex-wrap:wrap;gap:.3rem .6rem;font-size:13px;color:rgba(255,255,255,.5);">
        <li><a href="/" style="color:var(--teal-ink);">Home</a></li><li style="opacity:.4;">/</li>
        <li><a href="/blog/" style="color:var(--teal-ink);">Blog</a></li><li style="opacity:.4;">/</li>
        <li style="color:#fff;">Werbeanlage {e(s)}</li>
      </ol>
    </nav>
    <div class="art-tag">{I['pin']}Stadt-Ratgeber · {e(s)}</div>
    <h1>{c['h1']}</h1>
    <div class="art-meta"><span>{I['cal']}{MONAT}</span><span>{I['clock']}6 Min. Lesezeit</span><span>{I['pen']}Masar Werbeagentur</span></div>
  </div>
</header>

<main class="article-body">
  <div class="container">
    <figure class="art-hero"><img src="/{img}-720.webp" srcset="/{img}-360.webp 360w, /{img}-540.webp 540w, /{img}-720.webp 720w, /{img}.webp 1080w" sizes="(max-width:800px) 100vw, 752px" width="1080" height="1350" alt="Werbeanlage in {e(s)} – Schild, Leuchtreklame oder Beschriftung planen" loading="eager" fetchpriority="high"></figure>

    <div class="tip-box"><p>{I['tip']}<strong>Kurz gesagt:</strong> {c['kurz']}</p></div>

    <h2>1. Was grundsätzlich gilt</h2>
    {f'<p>{recht}</p>' if recht else ''}
    <p>Wichtig ist immer der <strong>Standort der Werbeanlage</strong>, nicht der Sitz Ihrer Firma. Und „verfahrensfrei“ heißt nicht „regelfrei“: Auch ohne Antrag müssen Größe, Lage und Gestaltung zu den örtlichen Vorschriften passen.</p>

    <h2>2. {e(c['lokal_h'])}</h2>
    {lokal}
    <div class="warning-box"><p>{I['warn']}{c['warn']}</p></div>

    <h2>3. Werbung, die in den öffentlichen Raum ragt</h2>
    <p>{c['raum']}</p>

    <h2>4. So läuft es mit uns ab</h2>
    <ol>
      <li><strong>Fotos und Wünsche</strong> per WhatsApp oder über den Anfrage-Assistenten schicken.</li>
      <li><strong>Standort prüfen:</strong> Wir klären Satzung, Denkmal und Sondernutzung für Ihre Adresse.</li>
      <li><strong>Entwurf und Festpreis</strong> – passend zu den örtlichen Regeln.</li>
      <li><strong>Antragsunterlagen:</strong> Zeichnung, Fotomontage und technische Angaben für den Antrag.</li>
      <li><strong>Produktion und Montage</strong> durch {team}.</li>
    </ol>

    <h2>5. Was kostet eine Werbeanlage in {e(s)}?</h2>
    <p>Startpreise bei Masar Werbeagentur für {e(s)} (netto zzgl. 19 % MwSt.; Festpreis nach Fotos oder Aufmaß):</p>
    <div class="table-wrap"><table class="price-table rt"><thead><tr><th>Leistung</th><th>Preis</th></tr></thead><tbody>{rows}</tbody></table></div>
    <p>{geb}</p>

    <h2>6. Unsere Tipps für {e(s)}</h2>
    <ul>{tipps}</ul>

    <h2>Häufige Fragen</h2>
    {faq_html}

    <div class="quellen" style="margin-top:2rem;font-size:14px;color:var(--muted)"><strong style="color:var(--navy)">Quellen (Stand {MONAT}):</strong><ul style="margin-top:.4rem">{quellen}</ul>
    <p style="margin-top:.6rem">Dieser Ratgeber ersetzt keine Rechtsberatung und keine Auskunft der Behörde. Satzungen ändern sich – vor dem Auftrag prüfen wir den aktuellen Stand für Ihren Standort.</p></div>

    <div class="article-cta">
      <h3>Werbeanlage in {e(s)} planen?</h3>
      <p>Wir prüfen Ihren Standort, gestalten passend zu den örtlichen Regeln und montieren vor Ort. Antwort innerhalb von 24 Stunden.</p>
      <div class="btns">
        <a href="{c['seite']}" class="btn-teal">Werbeagentur für {e(s)} →</a>
        <a href="{wa}" target="_blank" rel="noopener noreferrer" class="btn-wa">{I['wa']} WhatsApp</a>
        <a href="/termin.html{'?region=' + c['region'] if c['region'] != 'berlin' else ''}" data-termin-link class="btn-termin" style="background:#fff;color:var(--navy);padding:13px 24px;border-radius:8px;font-weight:700;font-size:15px">{I['cal']} Kostenlose Beratung</a>
      </div>
    </div>

    <div class="related-posts">
      <h2 style="font-family:'Barlow Condensed',sans-serif;font-weight:900;font-size:1.5rem;color:var(--navy);text-transform:uppercase;">Ratgeber für weitere Städte</h2>
      <div class="related-grid">
        {''.join(f'<div class="related-card"><h4>{I["pin"]}{e(o["stadt"])}</h4><p>{e(o["desc"][:90].rsplit(" ", 1)[0])} …</p><a href="/blog/werbeanlage-{o["slug"]}.html">Artikel lesen →</a></div>' for o in nachbarn(c))}
        <div class="related-card"><h4>{I['pin']}Berlin</h4><p>Außenwerbung in Berlin: Genehmigung, Kosten und Strategien …</p><a href="/blog/aussenwerbung-berlin-ratgeber.html">Artikel lesen →</a></div>
      </div>
    </div>
  </div>
</main>
'''
    kopf = VORLAGE[:VORLAGE.index('<header class="article-header"')]
    fuss = VORLAGE[VORLAGE.index('</main>') + len('</main>'):]
    # Meta
    alt_url = 'https://masar-werbeagentur.de/blog/aussenwerbung-berlin-ratgeber.html'
    kopf = kopf.replace(alt_url, url)
    kopf = re.sub(r'<title>.*?</title>', f'<title>{e(c["title"])}</title>', kopf, count=1)
    for prop in ['og:title', 'twitter:title']:
        kopf = re.sub(rf'(<meta (?:property|name)="{prop}" content=")[^"]*', lambda m: m.group(1) + e(c['title']), kopf)
    for prop in ['description', 'og:description', 'twitter:description']:
        kopf = re.sub(rf'(<meta (?:property|name)="{prop}" content=")[^"]*', lambda m: m.group(1) + e(c['desc']), kopf)
    kopf = kopf.replace('og/blog-aussenwerbung-berlin-ratgeber.jpg', f'og/blog-werbeanlage-{c["slug"]}.jpg')
    kopf = re.sub(r'(<meta property="og:image:alt" content=")[^"]*', lambda m: m.group(1) + e(f'Werbeanlage {s} – Masar Werbeagentur'), kopf)
    # JSON-LD ersetzen
    kopf = re.sub(r'<script type="application/ld\+json">.*?</script>\s*<script type="application/ld\+json">.*?</script>', '', kopf, count=1, flags=re.S)
    ld = [{'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': re.sub('<[^>]+>', ' ', c['h1']).replace('&amp;', '&').replace('  ', ' ').strip(),
           'description': c['desc'], 'url': url, 'datePublished': DATUM, 'dateModified': DATUM, 'inLanguage': 'de-DE',
           'about': {'@type': 'City', 'name': s},
           'author': {'@type': 'Organization', '@id': 'https://masar-werbeagentur.de/#identity', 'name': 'Masar Werbeagentur', 'url': 'https://masar-werbeagentur.de'},
           'publisher': {'@type': 'Organization', '@id': 'https://masar-werbeagentur.de/#identity', 'name': 'Masar Werbeagentur', 'url': 'https://masar-werbeagentur.de', 'logo': {'@type': 'ImageObject', 'url': 'https://masar-werbeagentur.de/logo.png'}},
           'image': f'https://masar-werbeagentur.de/og/blog-werbeanlage-{c["slug"]}.jpg', 'mainEntityOfPage': url},
          {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
              {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': 'https://masar-werbeagentur.de/'},
              {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': 'https://masar-werbeagentur.de/blog/'},
              {'@type': 'ListItem', 'position': 3, 'name': f'Werbeanlage {s}', 'item': url}]},
          {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
              {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in c['faq']]}]
    lds = ''.join(f'<script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False, indent=2)}\n</script>\n' for x in ld)
    css = '<style id="hero-mobile">.art-hero{margin:0 0 1.6rem}.art-hero img{width:100%;height:auto;max-height:420px;object-fit:cover;object-position:center 35%;border-radius:12px;display:block}@media(max-width:700px){.art-hero img{max-height:300px}}</style>\n'
    kopf = kopf.replace('<style>', lds + css + '<style>', 1)
    out = kopf + body.lstrip('\n') + fuss
    f = os.path.join(ROOT, 'blog', f'werbeanlage-{c["slug"]}.html')
    open(f, 'w', encoding='utf-8').write(out)
    return f


if __name__ == '__main__':
    for c in STAEDTE:
        print(artikel(c))
