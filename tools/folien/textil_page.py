"""Textildruck Berlin – Firmenkleidung mit Logo (Generator: gen_folien.build_f).
Verfahren laut Inhaber (03.11.2026): Flex/Flock (Plotter), DTF, Stick. Preise „ab“ nach Marktrecherche – vor
Veröffentlichung vom Inhaber freigeben. Lieferung: Berlin + Versand deutschlandweit.
"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'gen_folien.py'), encoding='utf-8').read()
exec(src[:src.index("\nif __name__")])

PREISE = [  # Produkt, Ausführung, Preis (netto, ab, inkl. Textil in Standardqualität, ein Motiv)
    ['T-Shirt mit Logo', 'Flex oder DTF, Brust oder Rücken', 'ab 15&nbsp;€'],
    ['Poloshirt mit Stick', 'Logo auf der Brust gestickt', 'ab 25&nbsp;€'],
    ['Hoodie mit Logo', 'Flex oder DTF, Brust und/oder Rücken', 'ab 35&nbsp;€'],
    ['Cap mit Stick', 'Logo vorne gestickt', 'ab 18&nbsp;€'],
    ['Stofftasche', 'bedruckt, ein Motiv', 'ab 8&nbsp;€'],
    ['Ihre eigenen Textilien', 'veredeln, je Motiv', 'ab 7&nbsp;€'],
    ['Stickprogramm', 'einmalig je Logo (Digitalisierung)', 'ab 39&nbsp;€'],
]

P = dict(file='textildruck-berlin.html', crumb='Textildruck', img='textildruck',
 parent=('Druckerei', 'print.html'), finder_strip=False, tab_ey='Verfahren', hero_mobile=True,
 img_alt='Beispiel-Visualisierung: T-Shirt, zwei Hoodies, Stofftasche und Cap mit aufgedrucktem Logo – so kann Ihre Firmenkleidung aussehen',
 title='Textildruck Berlin: T-Shirts & Hoodies mit Logo | Masar',
 desc='Textildruck in Berlin für Firmen: T-Shirts, Hoodies, Polos, Caps und Taschen mit Ihrem Logo – Flex, DTF oder Stick, Gestaltung inklusive, Versand in ganz Deutschland.',
 service_type='Textildruck', schema_name='Textildruck und Stick in Berlin',
 badge='Textildruck · Berlin', h1='Textildruck <em>Berlin</em>',
 sub='Ihr Logo wirbt jeden Tag für Sie – auf dem Shirt im Laden, dem Hoodie im Team und der Tasche beim Kunden. Wir veredeln Firmenkleidung mit Flex, DTF oder Stick, gestalten das Motiv auf Wunsch mit und schicken die fertigen Teile in ganz Deutschland zu Ihnen.',
 trust='Flex · DTF · Stick · Firmenkleidung · Teamwear · Merch',
 usp=['Flex, DTF & Stick', 'Gestaltung inklusive', 'Versand deutschlandweit', 'Angebot in 24 h'],
 wa='Hallo, ich interessiere mich für Textildruck mit unserem Logo. Ich schicke Ihnen das Logo und die Stückzahl.',
 angles_ey='Warum Textildruck', angles_h2='Werbung, die <em>man trägt</em>',
 angles_sub='Ein einheitlicher Auftritt beginnt beim Team – und wirkt überall, wo es unterwegs ist.',
 angles=[
  ('Einheitliches Team', 'Kundinnen und Kunden erkennen sofort, wer zu Ihnen gehört – im Laden, in der Praxis, auf der Baustelle oder am Messestand.'),
  ('Werbung unterwegs', 'Jedes Shirt und jede Tasche trägt Ihr Logo durch die Stadt. Eine Werbefläche, die mitläuft und nichts im Monat kostet.'),
  ('Teamgefühl', 'Gemeinsame Kleidung stärkt das Wir-Gefühl – bei Firmenfeiern, Sportevents, Eröffnungen oder im Alltag.'),
  ('Merch für Kunden', 'Bedruckte Taschen, Shirts oder Caps als Geschenk bleiben in Erinnerung – länger als ein Flyer.'),
 ],
 tab_h2='Welches Verfahren <em>passt zu Ihrem Logo?</em>', tab_sub='Wir wählen das Verfahren nach Motiv, Stoff und Stückzahl – und beraten Sie vorher.',
 tab_cols=['Verfahren', 'Ideal für', 'Gut zu wissen'],
 tab_rows=[
  ['Flex & Flock', 'Logos und Schriftzüge in 1–2 Farben, Namen und Nummern', 'geplottet und aufgepresst, sehr scharfe Kanten; Flock mit samtiger Oberfläche'],
  ['DTF-Druck', 'farbige Logos, Verläufe und Fotos', 'alle Farben in einem Arbeitsgang, auch kleine Details; auf vielen Stoffen'],
  ['Stick', 'Poloshirts, Caps, Jacken, Arbeitskleidung', 'besonders hochwertig und langlebig; einmalig wird ein Stickprogramm erstellt'],
 ],
 tab_note='Sie sind unsicher? Schicken Sie uns Ihr Logo – wir sagen Ihnen, welches Verfahren am besten aussieht und am längsten hält. Für Werbung auf Fenster und Fahrzeug siehe <a href="/foliendruck-berlin.html">Foliendruck</a>.',
 svc_h2='Was wir <em>für Sie veredeln</em>', svc_sub='Vom einzelnen Teamshirt bis zur Kollektion für die ganze Firma.',
 services=[
  ('stern', 'T-Shirts & Polos', 'Für Team, Empfang und Verkauf – mit Logo auf Brust, Rücken oder Ärmel.', '#kontakt'),
  ('schutz', 'Hoodies & Jacken', 'Warm und sichtbar – für Werkstatt, Außendienst und kalte Tage.', '#kontakt'),
  ('karte', 'Arbeitskleidung', 'Logo auf Arbeitshosen, Westen und Jacken – gestickt oder gedruckt.', '#kontakt'),
  ('druck', 'Caps & Taschen', 'Gestickte Caps und bedruckte Stofftaschen als Merch oder Geschenk.', '#kontakt'),
  ('neon', 'Events & Messen', 'Einheitliche Shirts für Messeteam, Eröffnung oder Firmenlauf.', '/messebau-berlin.html'),
  ('web', 'Gestaltung', 'Wir bereiten Ihr Logo für den Druck auf oder entwickeln ein Motiv mit Ihnen.', '/grafikdesign-berlin.html'),
 ],
 preis_h2='Was kostet <em>Textildruck?</em>',
 preis_html=table('Preise Textildruck', ['Produkt', 'Ausführung', 'Preis netto'], [[r[0], r[1], f'<strong>{r[2]}</strong>'] for r in PREISE]) + '''
<p style="margin-top:1.2rem">Alle Preise netto zzgl. 19&nbsp;% MwSt., inklusive Textil in Standardqualität und einem Motiv. Der Endpreis hängt von Textil, Größe und Zahl der Motive sowie der Stückzahl ab – ab 10 Stück gibt es Staffelpreise. Sie bekommen von uns ein <strong>Festpreis-Angebot</strong>, in der Regel innerhalb von 24 Stunden.</p>
<p>Gestaltung und Aufbereitung Ihres Logos sind enthalten. Lieferung: Abholung in Berlin-Wedding oder Versand in ganz Deutschland.</p>''',
 recht_ey='Gut zu wissen', recht_h2='Damit Ihr Druck <em>lange hält</em>', recht_sub=None,
 recht_html='''<p><strong>Druckdaten:</strong> Am besten ist Ihr Logo als Vektordatei (PDF, SVG, AI oder EPS). Ein gutes PNG geht auch – wir prüfen jede Datei und bereiten sie für Flex, DTF oder Stick auf.</p>
<p><strong>Waschen:</strong> Bedruckte Textilien auf links drehen, bei höchstens 40&nbsp;°C waschen und nicht direkt auf dem Motiv bügeln. So bleiben Druck und Stick lange schön.</p>
<p><strong>Größen:</strong> Für Teambestellungen schicken wir Ihnen auf Wunsch eine einfache Größenliste – Sie tragen ein, wer welche Größe braucht.</p>
<p><strong>Rechte am Motiv:</strong> Wir drucken Ihr eigenes Logo oder Motive, an denen Sie die Rechte haben. Fremde Marken, Vereinslogos oder Bilder ohne Erlaubnis drucken wir nicht.</p>
<p><strong>Lieferzeit:</strong> In der Regel etwa 3 Wochen nach Freigabe des Entwurfs und Anzahlung. Brauchen Sie die Teile zu einem festen Termin, sagen Sie es uns bei der Anfrage.</p>''',
 ablauf=[
  ('Logo & Stückzahl', 'Sie schicken uns Ihr Logo, die gewünschten Teile und ungefähr, wie viele Sie brauchen – per WhatsApp oder Formular.'),
  ('Entwurf', 'Wir zeigen Ihnen, wie das Logo auf Shirt, Hoodie oder Cap aussieht – mit Größe und Position.'),
  ('Festpreis & Größen', 'Sie bekommen ein schriftliches Angebot und eine Größenliste für Ihr Team.'),
  ('Produktion & Lieferung', 'Wir veredeln die Textilien in unserer Werkstatt und liefern sie aus – in Berlin oder per Versand.'),
 ],
 faq_h2='Textildruck – <em>Fragen &amp; Antworten</em>',
 faq=[
  ('Ab wie vielen Stück drucken Sie?', 'Kleine Mengen sind möglich. Ab 10 Stück gibt es Staffelpreise, bei größeren Teambestellungen wird der Preis pro Teil deutlich günstiger. Fragen Sie einfach mit Ihrer Stückzahl an.'),
  ('Flex, DTF oder Stick – was ist besser?', 'Das hängt vom Logo ab: Flex für klare Logos in 1–2 Farben, DTF für farbige Motive mit Verläufen, Stick für Polos, Caps und Jacken mit besonders hochwertigem Look. Wir beraten Sie gern.'),
  ('Kann ich eigene Textilien bringen?', 'Ja. Wir veredeln auch Ihre eigenen Shirts, Hoodies oder Jacken. Bitte sagen Sie uns vorher das Material, damit wir das passende Verfahren wählen.'),
  ('Liefern Sie auch außerhalb von Berlin?', 'Ja. Wir verschicken die fertigen Textilien in ganz Deutschland – zum Beispiel an Ihr Team in NRW oder Hamburg.'),
  ('Wie lange dauert es?', 'In der Regel etwa 3 Wochen nach Freigabe des Entwurfs und Anzahlung. Haben Sie einen festen Termin, zum Beispiel eine Messe oder Eröffnung, planen wir danach.'),
  ('Brauchen wir ein fertiges Design?', 'Nein. Ihr Logo reicht. Wir bereiten es für den Druck auf und zeigen Ihnen vorher, wie es auf dem Textil aussieht.'),
 ],
 links=[('/print.html', 'Druckerei Berlin'), ('/foliendruck-berlin.html', 'Foliendruck & Sticker'), ('/messebau-berlin.html', 'Messestand'),
        ('/grafikdesign-berlin.html', 'Grafikdesign'), ('/referenzen.html', 'Referenzen')],
 form_opts=['T-Shirts', 'Poloshirts', 'Hoodies / Jacken', 'Arbeitskleidung', 'Caps', 'Taschen', 'Eigene Textilien veredeln'],
 form_labels=('Was soll veredelt werden?', 'Logo, Teile &amp; Stückzahl', 'Ihr Logo (optional)', 'Am besten als PDF, SVG oder AI. Ein PNG in guter Qualität geht auch.'),
 form_sub='Schicken Sie uns Ihr Logo, die gewünschten Teile und die Stückzahl – Sie bekommen innerhalb von 24 Stunden ein Angebot.',
 subject='Anfrage Textildruck (Website)', msg_ph='z. B. 20 T-Shirts schwarz mit Logo vorne, 10 Hoodies mit Logo vorne und Rücken, Größen gemischt, Lieferung bis Ende des Monats',
 sticky=('Textildruck Berlin', 'Flex, DTF & Stick – Versand deutschlandweit'))

if __name__ == '__main__':
    print(build_f(P))
