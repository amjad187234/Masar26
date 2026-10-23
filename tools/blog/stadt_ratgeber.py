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


def artikel(c):
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
        {''.join(f'<div class="related-card"><h4>{I["pin"]}{e(o["stadt"])}</h4><p>{e(o["desc"][:90].rsplit(" ", 1)[0])} …</p><a href="/blog/werbeanlage-{o["slug"]}.html">Artikel lesen →</a></div>' for o in STAEDTE if o is not c)}
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
