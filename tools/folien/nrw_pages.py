"""NRW-Leistungsseiten: Leuchtreklame, Schilder, Schaufenster, Fensterfolie, Webdesign (Generator: gen_folien.build_f)."""
import os, re
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'gen_folien.py'), encoding='utf-8').read()
exec(src[:src.index("\nif __name__")])

CITIES = ['Düsseldorf', 'Köln', 'Dortmund', 'Essen', 'Bochum', 'Duisburg', 'Wuppertal', 'Bonn']
AREA = [{"@type": "State", "name": "Nordrhein-Westfalen"}] + [{"@type": "City", "name": c} for c in CITIES]
CITY_LINKS = [('/werbeagentur-nrw.html', 'Werbeagentur NRW'), ('/werbeagentur-duesseldorf.html', 'Düsseldorf'), ('/werbeagentur-koeln.html', 'Köln'),
              ('/werbeagentur-dortmund.html', 'Dortmund'), ('/werbeagentur-essen.html', 'Essen'), ('/werbeagentur-bochum.html', 'Bochum')]
BERLIN_NOTE = 'Die Fotos zeigen Arbeiten aus unserem Firmensitz in Berlin – in NRW arbeiten wir mit denselben Materialien und Abläufen. <a href="/referenzen.html">Alle Referenzen ansehen →</a>'

def ref(name, alt, cap, top=False):
    f = f'referenzen/{name}.webp'
    w, h = Image.open(ROOT + f).size
    return ('/' + f, w, h, alt, cap, top)

BAUO = '''<p><strong>Genehmigung in NRW:</strong> Werbeanlagen mit einer Ansichtsfläche bis 1&nbsp;m² sind nach § 62 Abs. 1 Nr. 12 BauO NRW in der Regel verfahrensfrei; mehrere gleichzeitig sichtbare Anlagen werden dabei zusammengerechnet. Größere Anlagen brauchen meist eine Baugenehmigung. Verfahrensfrei heißt aber nicht regelfrei: Örtliche Werbeanlagensatzungen, Bebauungspläne und Denkmalschutz gelten trotzdem – in vielen Innenstädten, etwa in Altstadtbereichen, sind Größe, Farbe oder Leuchtwirkung vorgeschrieben.</p>
<p><strong>Wir klären das vorher:</strong> Bevor Sie ein Angebot unterschreiben, prüfen wir, was an Ihrer Fassade erlaubt ist, und sagen Ihnen, ob ein Antrag nötig ist. Ragt ein Schild in den Gehweg (Ausleger), kann zusätzlich eine Sondernutzungserlaubnis der Stadt nötig sein.</p>
<p style="font-size:13px;">Quelle: <a href="https://www.dortmund.de/dortmund/projekte/rathaus/verwaltung/stadtplanungs-und-bauordnungsamt/downloads/bauordnung/infoblaetter/infoblatt_werbeanlagen.pdf" target="_blank" rel="noopener noreferrer">Stadt Dortmund – Infoblatt Werbeanlagen</a>. Allgemeine Hinweise, keine Rechtsberatung; maßgeblich ist die Auskunft der örtlichen Bauaufsicht.</p>'''


def price_top(h2, sub, rows, note):
    t = table('Preise NRW', ['Leistung', 'Ausführung', 'Preis NRW'], [[r[0], r[1], f'<strong>{r[2]}</strong>'] for r in rows])
    return ('Preise auf einen Blick', h2, sub, t + f'''
    <p class="price-note">{note}</p>
    <div style="text-align:center;margin-top:1.4rem;display:flex;gap:.8rem;justify-content:center;flex-wrap:wrap"><a href="#kontakt" class="btn btn-teal">Festpreis anfragen</a></div>''')

PRICE_NOTE = 'Alle Preise netto zzgl. 19&nbsp;% MwSt., Startpreise für einfache Ausführungen. Ihren verbindlichen Festpreis inklusive Montage durch unser Team in NRW bekommen Sie nach Foto und Maßen – in der Regel innerhalb von 24 Stunden.'
ROWS_L = [('LED-Leuchtbuchstaben', 'einzeln montiert, LED, Front- oder Rückleuchter', 'ab 229&nbsp;€ / Buchstabe'),
          ('Leuchtkasten', 'ein- oder zweiseitig, bedruckte oder gefräste Front', 'nach Größe – Festpreis'),
          ('Ausleger (Nasenschild)', 'beidseitig sichtbar, quer zur Fassade', 'nach Größe – Festpreis'),
          ('Umbau auf LED', 'vorhandene Reklame mit neuer Technik oder Front', 'nach Foto – Festpreis')]
ROWS_S = [('Hinweis- / Sicherheitsschild', 'Alu oder Kunststoff, A4/A5', 'ab 59&nbsp;€'),
          ('Tür- / Klingelschild', 'Acryl oder Alu, Druck oder Gravur', 'ab 85&nbsp;€'),
          ('Firmenschild', 'Alu-Dibond 3 mm, bis 1 m², laminiert', 'ab 179&nbsp;€'),
          ('Einzelbuchstaben (unbeleuchtet)', 'Acryl, Alu oder Edelstahl, pro Buchstabe', 'ab 139&nbsp;€'),
          ('Acrylglasschild', 'rückseitig bedruckt, mit Abstandshaltern', 'ab 289&nbsp;€'),
          ('Praxis- / Kanzleischild', 'hochwertige Ausführung inkl. Gestaltung', 'ab 459&nbsp;€')]
ROWS_W = [('Schaufensterbeschriftung', 'Logo, Öffnungszeiten, Kontakt als Plottfolie', 'ab 179&nbsp;€'),
          ('Milchglas- / Sichtschutzfolie', 'Teilfläche oder ganze Scheibe, mit Logo oder Muster', 'ab 229&nbsp;€'),
          ('Aktions- / Eröffnungsfolie', '„Bald hier“, Sale, Saison – rückstandslos entfernbar', 'ab 229&nbsp;€'),
          ('Lochfolie (One Way Vision)', 'außen Motiv, innen Durchsicht, inkl. Druck', 'ab 55&nbsp;€ / m²'),
          ('Vollflächige Gestaltung', 'ganze Ladenfront mit Druck- und Milchglasfolie', 'nach Fläche – Festpreis')]
ROWS_F = [('Sichtschutzfolie', 'eine Fensterfläche, Milchglas-Optik', 'ab 229&nbsp;€'),
          ('Milchglas- / Sandstrahlfolie nach Maß', 'Streifen, Logo, Muster oder ganze Scheibe', 'ab 289&nbsp;€'),
          ('Sonnenschutzfolie', 'gegen Hitze und Blendung, nach Glasprüfung', 'nach Fläche – Festpreis'),
          ('Spiegelfolie', 'einseitiger Sichtschutz am Tag', 'nach Fläche – Festpreis'),
          ('Sicherheitsfolie', 'Splitterschutz bzw. durchwurfhemmend nach DIN EN 12600 / 356', 'nach Fläche – Festpreis')]

COMMON = dict(finder_strip=False, hero_mobile=True, area=AREA, parent=('Werbeagentur NRW', 'werbeagentur-nrw.html'),
              faq_h2=None, svc_sub='Alles aus einer Hand – Gestaltung, Produktion und Montage durch unser Team in NRW.')

# ---------------------------------------------------------------- Leuchtreklame
L = dict(COMMON)
L.update(file='leuchtreklame-nrw.html', crumb='Leuchtreklame NRW', img='leuchtreklamen', tab_ey='Bauarten',
 img_alt='Beispiel-Visualisierung: Leuchtreklame mit beleuchteten Buchstaben an einer Ladenfassade',
 title='Leuchtreklame NRW: Leuchtbuchstaben & Leuchtkästen | Masar',
 desc='Leuchtreklame in NRW: Leuchtbuchstaben, Leuchtkästen und LED-Neon für Düsseldorf, Köln und das Ruhrgebiet – Genehmigung geprüft, Montage vor Ort.',
 service_type='Leuchtreklame', schema_name='Leuchtreklame in NRW',
 badge='Leuchtreklame · NRW', h1='Leuchtreklame <em>NRW</em>',
 sub='Leuchtbuchstaben, Leuchtkästen und LED-Neon für Läden, Praxen, Restaurants und Betriebe zwischen Rhein und Ruhr. Wir gestalten, produzieren und klären vorab, was an Ihrer Fassade erlaubt ist – unser Team in NRW misst auf und montiert bei Ihnen vor Ort.',
 trust='Düsseldorf · Köln · Dortmund · Essen · Bochum',
 usp=['Team vor Ort in NRW', 'Genehmigung geprüft', 'Gestaltung bis Montage', 'Angebot in 24 h'],
 wa='Hallo, ich interessiere mich für eine Leuchtreklame in NRW. Ich schicke Ihnen ein Foto der Fassade.',
 angles_ey='Warum Leuchtreklame', angles_h2='Gesehen werden – <em>auch nach 16 Uhr</em>',
 angles_sub='Im Winter ist es in NRW schon am Nachmittag dunkel. Ein unbeleuchtetes Schild verschwindet dann.',
 angles=[
  ('Sichtbar am Abend', 'Gerade in der dunklen Jahreszeit fällt ein beleuchteter Schriftzug in der Einkaufsstraße sofort auf – während unbeleuchtete Schilder kaum noch zu lesen sind.'),
  ('Passend zur Fassade', 'Altbau in Düsseldorf-Flingern, Ladenzeile in der Dortmunder City oder Gewerbehalle in Duisburg: Wir wählen Bauart und Größe so, dass die Reklame zum Gebäude passt.'),
  ('Sparsame LED-Technik', 'Moderne LED verbraucht wenig Strom und hält lange. Auf Wunsch mit Zeitschaltuhr, damit die Reklame nur leuchtet, wenn sie gesehen wird.'),
  ('Ein Ansprechpartner', 'Gestaltung, Genehmigungsfrage, Produktion, Elektroanschluss-Vorbereitung und Montage – Sie müssen nicht mehrere Firmen koordinieren.'),
 ],
 gallery=dict(h2='Leuchtreklame <em>aus unserer Werkstatt</em>', sub='So sehen Arbeiten aus, die wir gebaut und montiert haben.', note=BERLIN_NOTE, items=[
  ref('leuchtreklame-berlin-07', 'Blau leuchtende Profilbuchstaben für einen Barbershop, aufgebaut in der Werkstatt', 'Profilbuchstaben mit LED – vor der Montage in der Werkstatt aufgebaut und geprüft.'),
  ref('leuchtreklame-berlin-02', 'Leuchtkasten für einen Friseursalon mit hinterleuchteten Buchstaben in der Werkstatt', 'Leuchtkasten mit hinterleuchteten Buchstaben für einen Friseursalon.'),
  ref('leuchtreklame-berlin-06', 'Runder Ausleger eines Barbershops wird über dem Eingang montiert', 'Montage eines runden Auslegers über dem Eingang.'),
 ]),
 tab_h2='Welche Leuchtreklame <em>passt zu Ihnen?</em>', tab_sub='Die Bauart richtet sich nach Fassade, Budget und gewünschter Wirkung.',
 tab_cols=['Bauart', 'Wirkung', 'Gut für'],
 tab_rows=[
  ['3D-Leuchtbuchstaben', 'Einzelne Buchstaben, die von vorn oder nach hinten leuchten', 'Ladenfront, Praxis, Restaurant'],
  ['Leuchtkasten', 'Flächiges Leuchtschild, Motiv auf der Front', 'günstiger Einstieg, viel Inhalt'],
  ['Leuchtkasten mit durchgesteckter Schrift', 'Nur Schrift und Logo leuchten, die Front bleibt dunkel', 'edle Wirkung bei Leuchtkasten-Preis'],
  ['Ausleger (Nasenschild)', 'Steht quer zur Fassade, von beiden Seiten sichtbar', 'Fußgängerzone, Seitenstraße'],
  ['LED-Neon', 'Leuchtende Linie wie klassisches Neon', 'Schaufenster innen, Logo, Wand im Laden'],
 ],
 tab_note='Mehr zu Bauarten und Beispielen auf unserer Seite <a href="/leuchtreklame-berlin.html">Leuchtreklame</a>. Schilder ohne Beleuchtung: <a href="/schilder-nrw.html">Schilder NRW</a>.',
 svc_h2='Leuchtreklame <em>in NRW</em>',
 services=[
  ('licht', 'Leuchtbuchstaben', 'Profil- oder Acrylbuchstaben mit LED, einzeln an der Fassade montiert.', '#kontakt'),
  ('schild', 'Leuchtkästen', 'Ein- oder zweiseitig, mit bedruckter oder gefräster Front.', '#kontakt'),
  ('neon', 'LED-Neon', 'Logo oder Schriftzug als Neon-Optik – für das Schaufenster oder innen.', '#kontakt'),
  ('stern', 'Ausleger', 'Nasenschilder quer zur Fassade, gut sichtbar aus beiden Richtungen.', '#kontakt'),
  ('web', 'Gestaltung', 'Wir entwickeln den Entwurf passend zu Ihrem Logo und Ihrer Fassade.', '/grafikdesign-berlin.html'),
  ('schild', 'Schilder ohne Licht', 'Firmen-, Praxis- und Türschilder aus Alu-Dibond, Acryl oder Edelstahl.', '/schilder-nrw.html'),
 ],
 preis_h2='Was kostet <em>Leuchtreklame in NRW?</em>',
 preis_html='''<p>Leuchtbuchstaben berechnen wir in NRW ab 229&nbsp;€ pro Buchstabe netto zzgl. 19&nbsp;% MwSt. Leuchtkästen und größere Fassadenanlagen kalkulieren wir nach Größe, Bauart und Montageaufwand.</p>
<p>Für Ihr Projekt bekommen Sie ein <strong>Festpreis-Angebot</strong> nach einem Foto der Fassade und den ungefähren Maßen – kostenlos und in der Regel innerhalb von 24 Stunden. Vor der Produktion misst unser Team in NRW vor Ort nach.</p>''',
 recht_ey='Gut zu wissen', recht_h2='Genehmigung <em>in NRW</em>', recht_sub=None,
 recht_html=BAUO + '<p><strong>Strom:</strong> Für die Leuchtreklame braucht es einen Stromanschluss in der Nähe. Den Anschluss an das Hausnetz übernimmt eine Elektrofachkraft; wir sagen Ihnen vorher genau, was vorbereitet sein muss.</p>',
 ablauf=[
  ('Foto & Wunsch', 'Sie schicken uns ein Foto der Fassade, Ihr Logo und ungefähre Maße – per WhatsApp oder E-Mail.'),
  ('Entwurf & Prüfung', 'Wir zeigen Ihnen die Reklame als Fotomontage an Ihrer Fassade und prüfen, ob eine Genehmigung nötig ist.'),
  ('Aufmaß & Festpreis', 'Unser Team in NRW misst vor Ort nach. Sie bekommen ein schriftliches Festpreis-Angebot.'),
  ('Produktion & Montage', 'Nach Ihrer Freigabe produzieren wir und montieren am vereinbarten Termin bei Ihnen.'),
 ],
 faq=[
  ('In welchen Städten in NRW montieren Sie Leuchtreklame?', 'Schwerpunkt sind Düsseldorf, Köln, Dortmund, Essen und Bochum, dazu Duisburg, Wuppertal, Bonn und die Städte dazwischen. Unser Team in NRW kommt für Aufmaß und Montage zu Ihnen. Unser Firmensitz ist in Berlin.'),
  ('Brauche ich eine Genehmigung für meine Leuchtreklame?', 'Bis 1 m² Ansichtsfläche ist eine Werbeanlage in NRW in der Regel verfahrensfrei, größere Anlagen brauchen meist eine Baugenehmigung. Örtliche Satzungen und Denkmalschutz können weitere Vorgaben machen. Wir prüfen das für Ihre Adresse, bevor Sie bestellen.'),
  ('Wie lange dauert es bis zur Montage?', 'Das hängt von Bauart und Genehmigung ab. Den Zeitplan nennen wir Ihnen im Angebot. Ist eine Baugenehmigung nötig, richtet sich der Termin nach der Bearbeitungszeit der Stadt.'),
  ('Wie viel Strom verbraucht eine LED-Leuchtreklame?', 'LED-Technik ist sparsam. Den Verbrauch Ihrer Anlage nennen wir Ihnen im Angebot. Mit einer Zeitschaltuhr leuchtet die Reklame nur, wann Sie es möchten.'),
  ('Können Sie meine alte Reklame umbauen?', 'Oft ja. Ein alter Leuchtkasten bekommt zum Beispiel eine neue Front oder LED statt Leuchtstoffröhren. Schicken Sie uns ein Foto, dann sagen wir, ob sich das lohnt.'),
  ('Brauche ich ein fertiges Design?', 'Nein, Ihr Logo reicht. Daraus entwickeln wir den Entwurf und zeigen Ihnen vorher, wie die Reklame an Ihrer Fassade aussieht.'),
 ],
 links=[('/leuchtreklame-berlin.html', 'Leuchtreklame: Bauarten & Beispiele'), ('/schilder-nrw.html', 'Schilder NRW')] + [('/leuchtreklame-koeln.html', 'Leuchtreklame Köln'), ('/leuchtreklame-duesseldorf.html', 'Leuchtreklame Düsseldorf'), ('/leuchtreklame-dortmund.html', 'Leuchtreklame Dortmund'), ('/leuchtreklame-essen.html', 'Leuchtreklame Essen'), ('/leuchtreklame-bochum.html', 'Leuchtreklame Bochum')] + CITY_LINKS[:1],
 form_opts=['3D-Leuchtbuchstaben', 'Leuchtkasten', 'Ausleger / Nasenschild', 'LED-Neon', 'Umbau einer vorhandenen Reklame'],
 form_labels=('Welche Leuchtreklame?', 'Fassade &amp; Wunsch', 'Foto der Fassade (optional)', 'Ein Foto der Fassade von vorn und ungefähre Maße reichen für ein erstes Angebot. Ihr Logo können Sie gleich mitschicken.'),
 form_sub='Schicken Sie uns ein Foto der Fassade und Ihr Logo – Sie bekommen innerhalb von 24 Stunden ein Angebot. Unser Team in NRW misst auf und montiert bei Ihnen vor Ort.',
 subject='Anfrage Leuchtreklame NRW (Website)', msg_ph='z. B. Leuchtbuchstaben „Café Rhein“ über dem Eingang, Fassade ca. 5 m breit, Altbau in Köln-Ehrenfeld',
 sticky=('Leuchtreklame NRW', 'Team vor Ort, Genehmigung geprüft'))
L['faq_h2'] = 'Leuchtreklame NRW – <em>Fragen &amp; Antworten</em>'

# ---------------------------------------------------------------- Schilder
S = dict(COMMON)
S.update(file='schilder-nrw.html', crumb='Schilder NRW', img='schilder', tab_ey='Materialien',
 img_alt='Beispiel-Visualisierung: Firmenschild aus Acryl mit Abstandshaltern an einer Wand',
 title='Schilder NRW: Firmen-, Praxis- & Türschilder | Masar',
 desc='Schilder in NRW: Firmen-, Praxis- und Türschilder aus Alu-Dibond, Acryl und Edelstahl – gefertigt und montiert in Düsseldorf, Köln und im Ruhrgebiet.',
 service_type='Schilderherstellung', schema_name='Schilder in NRW',
 badge='Schilder · NRW', h1='Schilder <em>NRW</em>',
 sub='Firmenschild am Eingang, Praxisschild neben der Klingel oder Wegweiser im Treppenhaus: Wir gestalten und fertigen Schilder aus Alu-Dibond, Acrylglas und Edelstahl. Unser Team in NRW bringt sie bei Ihnen an – gerade, sauber und dauerhaft.',
 trust='Firmenschilder · Praxisschilder · Türschilder · Wegweiser',
 usp=['Team vor Ort in NRW', 'Montage inklusive möglich', 'Einzelschild bis Leitsystem', 'Angebot in 24 h'],
 wa='Hallo, ich brauche ein Schild in NRW. Ich schicke Ihnen ein Foto der Stelle.',
 angles_ey='Warum ein gutes Schild', angles_h2='Der erste Eindruck <em>hängt an der Wand</em>',
 angles_sub='Bevor ein Kunde Ihr Büro betritt, sieht er Ihr Schild.',
 angles=[
  ('Gefunden werden', 'In großen Bürohäusern in Düsseldorf oder Köln und in Hinterhöfen im Ruhrgebiet suchen Kunden oft den Eingang. Ein klares Schild am richtigen Platz erspart Anrufe.'),
  ('Vertrauen schaffen', 'Ein hochwertiges Praxis- oder Kanzleischild wirkt seriös. Ein ausgeblichener Ausdruck hinter Folie wirkt das Gegenteil.'),
  ('Alles im selben Design', 'Fassade, Eingang, Türen und Etagen: Mit einem einheitlichen Schildersystem passt alles zusammen.'),
  ('Langlebig', 'Alu-Dibond, Acryl und Edelstahl sind wetterfest. Für außen verwenden wir UV-beständigen Druck oder Gravur.'),
 ],
 gallery=dict(h2='Schilder &amp; Beschriftung <em>aus unserer Arbeit</em>', sub='Beispiele für Schilder und Fassadenbeschriftungen, die wir gefertigt und montiert haben.', note=BERLIN_NOTE, items=[
  ref('leuchtreklame-berlin-05', 'Hinterleuchtetes Logoschild eines Barbershops an einer Innenwand', 'Logoschild mit Abstandshaltern an der Innenwand eines Barbershops.'),
  ref('leuchtreklame-berlin-09', 'Goldfarbene Fassadenbeschriftung eines Juweliers', 'Goldfarbene Fassadenbeschriftung für einen Juwelier.'),
  ref('schaufensterbeschriftung-pflegedienst-berlin-01', 'Weiße Fensterbeschriftung eines ambulanten Pflegedienstes mit Logo, Firmenname und Öffnungszeiten an der Tür', 'Beschriftung für einen Pflegedienst: Logo, Name und Öffnungszeiten an Tür und Fenster.'),
 ]),
 tab_h2='Welches Material <em>für Ihr Schild?</em>', tab_sub='Die Wahl hängt davon ab, wo das Schild hängt und wie es wirken soll.',
 tab_cols=['Material', 'Eigenschaften', 'Gut für'],
 tab_rows=[
  ['Alu-Dibond', 'leicht, stabil, wetterfest, bedruckt', 'Firmenschild außen, Bauschild, Hinweisschild'],
  ['Acrylglas', 'edle Glasoptik, mit Abstandshaltern', 'Praxis, Kanzlei, Empfang'],
  ['Edelstahl', 'graviert oder geätzt, sehr langlebig', 'Klingel- und Türschilder, repräsentative Eingänge'],
  ['Profil- oder Acrylbuchstaben', 'einzelne 3D-Buchstaben, ohne oder mit Licht', 'Logo an Fassade oder Empfangswand'],
  ['Folienbeschriftung', 'direkt auf Glas, Tür oder Wand', 'Öffnungszeiten, Glastüren, Innenräume'],
 ],
 tab_note='Formate, Beispiele und Preise im Detail: <a href="/schilder-berlin.html">Schilder</a> und <a href="/praxisbeschilderung-berlin.html">Praxisbeschilderung</a>. Beleuchtete Schilder: <a href="/leuchtreklame-nrw.html">Leuchtreklame NRW</a>.',
 svc_h2='Schilder <em>in NRW</em>',
 services=[
  ('schild', 'Firmenschilder', 'Am Eingang, an der Fassade oder auf dem Firmengelände.', '#kontakt'),
  ('tuer', 'Praxis- & Kanzleischilder', 'Mit Name, Fachrichtung und Sprechzeiten – passend zu Ihrem Auftritt.', '/praxisbeschilderung-berlin.html'),
  ('karte', 'Tür- & Klingelschilder', 'Für Büros, Etagen und Gemeinschaftseingänge.', '#kontakt'),
  ('weg', 'Leitsysteme', 'Wegweiser und Etagenschilder für Bürohäuser, Praxen und Hallen.', '#kontakt'),
  ('licht', 'Beleuchtete Schilder', 'Leuchtkästen und Leuchtbuchstaben für mehr Wirkung am Abend.', '/leuchtreklame-nrw.html'),
  ('web', 'Gestaltung', 'Wir gestalten das Schild passend zu Ihrem Logo – oder entwickeln ein neues.', '/grafikdesign-berlin.html'),
 ],
 preis_h2='Was kostet <em>ein Schild in NRW?</em>',
 preis_html='''<p>Einfache Schilder im Format A4/A5 gibt es in NRW ab 59&nbsp;€ netto zzgl. 19&nbsp;% MwSt., Firmenschilder aus Alu-Dibond ab 179&nbsp;€ netto, Acrylglasschilder ab 289&nbsp;€ netto. Größe, Material, Druck oder Gravur und die Montage bestimmen den Endpreis.</p>
<p>Schicken Sie uns ein Foto der Stelle, an der das Schild hängen soll, und Ihr Logo. Sie bekommen ein <strong>Festpreis-Angebot</strong> – auf Wunsch mit Montage durch unser Team in NRW.</p>''',
 recht_ey='Gut zu wissen', recht_h2='Was bei Schildern <em>in NRW gilt</em>', recht_sub=None,
 recht_html=BAUO + '<p><strong>Mietobjekt:</strong> Im Mietobjekt sollten Sie vor der Montage mit dem Vermieter oder der Hausverwaltung klären, wo und wie gebohrt werden darf. Wir richten uns nach diesen Vorgaben.</p>',
 ablauf=[
  ('Foto & Logo', 'Sie schicken uns ein Foto der Stelle, ungefähre Maße und Ihr Logo – per WhatsApp oder E-Mail.'),
  ('Entwurf', 'Wir zeigen Ihnen das Schild als Fotomontage am geplanten Platz.'),
  ('Festpreis', 'Sie bekommen ein schriftliches Angebot mit Material, Größe und Montage.'),
  ('Fertigung & Montage', 'Wir fertigen das Schild, unser Team in NRW montiert es am vereinbarten Termin.'),
 ],
 faq=[
  ('Montieren Sie die Schilder auch?', 'Ja. Unser Team in NRW bringt die Schilder bei Ihnen an – in Düsseldorf, Köln, Dortmund, Essen, Bochum und den Städten dazwischen. Unser Firmensitz ist in Berlin.'),
  ('Kann ich das Schild auch nur bestellen und selbst anbringen?', 'Ja. Kleine Schilder liefern wir auf Wunsch mit Klebeband oder Bohrlöchern und passendem Befestigungsmaterial zum Selbstmontieren.'),
  ('Welches Material hält draußen am längsten?', 'Alu-Dibond mit UV-beständigem Druck und Edelstahl mit Gravur sind sehr wetterfest. Acrylglas eignet sich ebenfalls für außen, wirkt aber besonders edel an geschützten Stellen wie im Eingangsbereich.'),
  ('Brauche ich eine Genehmigung für mein Firmenschild?', 'Bis 1 m² Ansichtsfläche ist ein Schild in NRW in der Regel verfahrensfrei. Örtliche Satzungen oder Denkmalschutz können trotzdem Vorgaben machen. Wir prüfen das für Ihre Adresse.'),
  ('Machen Sie auch mehrere Schilder für ein ganzes Gebäude?', 'Ja. Für Bürohäuser, Praxen und Firmengelände planen wir ein einheitliches Schildersystem – vom Eingang bis zur Etagentür.'),
  ('Brauche ich ein fertiges Design?', 'Nein, Ihr Logo reicht. Daraus gestalten wir das Schild und zeigen es Ihnen vorher am geplanten Platz.'),
 ],
 links=[('/schilder-berlin.html', 'Schilder: Formate & Preise'), ('/blog/praxisschild-regeln-kosten.html', 'Praxisschild: Regeln & Kosten'), ('/leuchtreklame-nrw.html', 'Leuchtreklame NRW')] + [('/schilder-koeln.html', 'Schilder Köln'), ('/schilder-duesseldorf.html', 'Schilder Düsseldorf'), ('/schilder-dortmund.html', 'Schilder Dortmund'), ('/schilder-essen.html', 'Schilder Essen'), ('/schilder-bochum.html', 'Schilder Bochum')] + CITY_LINKS[:1],
 form_opts=['Firmenschild', 'Praxis- oder Kanzleischild', 'Tür- / Klingelschild', 'Leitsystem / mehrere Schilder', 'Profil- oder Acrylbuchstaben'],
 form_labels=('Welches Schild?', 'Ort &amp; Wunsch', 'Foto der Stelle (optional)', 'Ein Foto der Wand oder des Eingangs und ungefähre Maße reichen für ein erstes Angebot. Ihr Logo können Sie gleich mitschicken.'),
 form_sub='Schicken Sie uns ein Foto der Stelle und Ihr Logo – Sie bekommen innerhalb von 24 Stunden ein Angebot. Unser Team in NRW montiert bei Ihnen vor Ort.',
 subject='Anfrage Schilder NRW (Website)', msg_ph='z. B. Praxisschild aus Acryl, ca. 60 × 40 cm, neben dem Hauseingang in Essen-Rüttenscheid, Montage gewünscht',
 sticky=('Schilder NRW', 'Gestaltet, gefertigt, montiert'))
S['faq_h2'] = 'Schilder NRW – <em>Fragen &amp; Antworten</em>'

# ---------------------------------------------------------------- Schaufenster
W = dict(COMMON)
W.update(file='schaufensterbeschriftung-nrw.html', crumb='Schaufensterbeschriftung NRW', img='schaufenster', tab_ey='Folienarten',
 img_alt='Beispiel-Visualisierung: Schaufenster mit Folienbeschriftung, Logo und Öffnungszeiten',
 title='Schaufensterbeschriftung NRW: Folie, Milchglas & Druck | Masar',
 desc='Schaufensterbeschriftung in NRW: Logo, Öffnungszeiten, Milchglas und Druckfolie für Läden und Praxen in Düsseldorf, Köln und im Ruhrgebiet – vor Ort montiert.',
 service_type='Schaufensterbeschriftung', schema_name='Schaufensterbeschriftung in NRW',
 badge='Schaufenster · NRW', h1='Schaufenster&shy;beschriftung <em>NRW</em>',
 sub='Ihr Schaufenster ist die Werbefläche, an der jeden Tag Menschen vorbeigehen. Wir gestalten und produzieren Folien für Logo, Öffnungszeiten, Sichtschutz und große Motive – unser Team in NRW klebt sie blasenfrei bei Ihnen vor Ort.',
 trust='Läden · Praxen · Gastronomie · Büros · Neueröffnungen',
 usp=['Team vor Ort in NRW', 'Blasenfreie Montage', 'Auch zur Eröffnung', 'Angebot in 24 h'],
 wa='Hallo, ich interessiere mich für eine Schaufensterbeschriftung in NRW. Ich schicke Ihnen ein Foto der Fenster.',
 angles_ey='Warum Schaufenster', angles_h2='Ihre Fensterfläche <em>arbeitet für Sie</em>',
 angles_sub='Eine Beschriftung kostet einmal und wirbt jeden Tag – ohne Miete für eine Werbefläche.',
 angles=[
  ('Sofort erkennbar', 'Wer durch die Einkaufsstraße geht, sieht in Sekunden, was Sie anbieten. Logo, Leistungen und Öffnungszeiten auf dem Glas sagen das ohne Worte.'),
  ('Sichtschutz inklusive', 'Milchglas- oder Lochfolie schützt Behandlungsräume, Büros und Lager vor Blicken – und trägt zugleich Ihre Werbung.'),
  ('Für die Eröffnung', 'Vor der Neueröffnung macht eine „Bald hier“-Folie neugierig. Nach der Eröffnung ersetzen wir sie durch die dauerhafte Beschriftung.'),
  ('Schnell geändert', 'Neue Öffnungszeiten oder Aktion? Folie lässt sich austauschen, ohne dass das Glas Schaden nimmt.'),
 ],
 gallery=dict(h2='Schaufenster <em>aus unserer Arbeit</em>', sub='Zum Beispiel diese Praxis: Eröffnungsfolie außen, Milchglas innen – in zwei Terminen montiert.', note=BERLIN_NOTE, items=[
  ref('praxis-schaufenster-berlin-02', 'Fertig beklebte Schaufensterfront einer neuen Physiotherapiepraxis: bedruckte Folien, Logo-Blenden und Milchglas', 'Fertige Front einer neuen Physiotherapiepraxis: Druckfolie, Logo-Blenden und Milchglas.'),
  ref('praxis-schaufenster-berlin-01', 'Schaufenster einer Physiotherapiepraxis während der Montage, zwei Monteure kleben Folie', 'Während der Montage: Unser Team verklebt die Folie vor Ort.'),
  ref('schaufensterbeschriftung-berlin-01', 'Vollflächig bedruckte Front eines Imbiss-Kiosks', 'Vollflächig bedruckte Front für einen Imbiss-Kiosk.'),
 ]),
 tab_h2='Welche Folie <em>für Ihr Fenster?</em>', tab_sub='Je nach Ziel kombinieren wir verschiedene Folien auf einer Scheibe.',
 tab_cols=['Folie', 'Wirkung', 'Gut für'],
 tab_rows=[
  ['Geplottete Schrift', 'einzelne Buchstaben und Logo, Glas bleibt frei', 'Name, Leistungen, Öffnungszeiten'],
  ['Milchglasfolie', 'Sichtschutz, Licht kommt trotzdem durch', 'Praxen, Büros, Kosmetik'],
  ['Lochfolie', 'außen Motiv, innen Durchsicht', 'große Werbemotive auf ganzer Scheibe'],
  ['Druckfolie', 'vollflächiges Motiv in Fotoqualität', 'Eröffnung, Aktionen, Kampagnen'],
  ['Folie für Glastüren', 'Markierung gegen Anlaufen', 'Ganzglastüren und große Glasflächen'],
 ],
 tab_note='Mehr Beispiele und Folienarten: <a href="/schaufensterbeschriftung-berlin.html">Schaufensterbeschriftung</a>. Für Hitze- und Sichtschutz: <a href="/fensterfolie-nrw.html">Fensterfolie NRW</a>.',
 svc_h2='Schaufenster <em>in NRW</em>',
 services=[
  ('glas', 'Schaufensterbeschriftung', 'Logo, Name und Leistungen als Folie auf dem Glas.', '#kontakt'),
  ('auge', 'Sichtschutz', 'Milchglas, Streifen oder Motiv – für Praxen, Büros und Kosmetikstudios.', '/fensterfolie-nrw.html'),
  ('druck', 'Druck- & Lochfolie', 'Große Motive, die außen wirken und innen Durchsicht lassen.', '#kontakt'),
  ('stern', 'Eröffnungsfolie', '„Bald hier“ oder „Neueröffnung“ – zum Wechseln nach der Eröffnung.', '#kontakt'),
  ('karte', 'Öffnungszeiten', 'Türbeschriftung mit Zeiten, Telefon und Website.', '#kontakt'),
  ('web', 'Gestaltung', 'Wir planen die Gestaltung passend zu Ihren Fenstern und Ihrem Logo.', '/grafikdesign-berlin.html'),
 ],
 preis_h2='Was kostet <em>eine Schaufensterbeschriftung in NRW?</em>',
 preis_html='''<p>Eine Schaufensterbeschriftung gibt es in NRW ab 179&nbsp;€ netto zzgl. 19&nbsp;% MwSt., Milchglas-Sichtschutz ab 229&nbsp;€ netto. Der Endpreis hängt von Fläche, Folienart, Gestaltung und der Zahl der Scheiben ab.</p>
<p>Schicken Sie uns ein Foto der Fenster und ungefähre Maße. Sie bekommen ein <strong>Festpreis-Angebot</strong> inklusive Montage durch unser Team in NRW – kostenlos und in der Regel innerhalb von 24 Stunden.</p>''',
 recht_ey='Gut zu wissen', recht_h2='Was Sie vorher <em>wissen sollten</em>', recht_sub=None,
 recht_html='''<p><strong>Werbung auf dem Glas:</strong> Auch eine Schaufensterbeschriftung kann als Werbeanlage gelten. Beschriftungen innerhalb der eigenen Schaufenster sind in der Regel unproblematisch; in Altstadtbereichen oder bei Denkmalschutz kann eine örtliche Satzung aber Vorgaben machen, etwa zum Anteil der beklebten Fläche. Wir fragen das vorher ab.</p>
<p><strong>Mietobjekt:</strong> Folie lässt sich rückstandsfrei entfernen. Trotzdem lohnt eine kurze Abstimmung mit dem Vermieter, besonders bei großflächigen Motiven.</p>
<p><strong>Innen oder außen:</strong> Folie innen ist vor Wetter geschützt und hält länger. Außen wirkt sie brillanter, weil keine Spiegelung des Glases dazwischen liegt. Wir empfehlen je nach Fenster die bessere Lösung.</p>''',
 ablauf=[
  ('Foto & Maße', 'Sie schicken uns ein Foto der Fenster von außen und ungefähre Maße – per WhatsApp oder E-Mail.'),
  ('Entwurf', 'Wir zeigen Ihnen die Beschriftung als Fotomontage auf Ihren Fenstern.'),
  ('Festpreis & Termin', 'Sie bekommen ein schriftliches Angebot, wir vereinbaren den Montagetermin in NRW.'),
  ('Montage vor Ort', 'Unser Team reinigt das Glas und verklebt die Folie blasenfrei – meist an einem Termin.'),
 ],
 faq=[
  ('Kommen Sie für die Montage zu uns?', 'Ja. Unser Team in NRW montiert bei Ihnen vor Ort – in Düsseldorf, Köln, Dortmund, Essen, Bochum und den Städten dazwischen. Unser Firmensitz ist in Berlin.'),
  ('Wie lange dauert die Montage?', 'Eine normale Ladenfront ist meist an einem Termin erledigt. Bei großen Flächen oder mehreren Folienarten sagen wir Ihnen die Dauer vorher.'),
  ('Lässt sich die Folie wieder entfernen?', 'Ja. Folie lässt sich später ablösen, ohne das Glas zu beschädigen. Bei kurzfristigen Aktionen verwenden wir eine leicht ablösbare Folie.'),
  ('Kann man von innen noch hinaussehen?', 'Bei geplotteter Schrift und Lochfolie ja. Milchglas lässt Licht durch, aber keine klare Sicht. Wir beraten Sie, was zu Ihrem Raum passt.'),
  ('Machen Sie auch eine Folie zur Eröffnung?', 'Ja. Eine „Bald hier“-Folie vor der Eröffnung und danach die dauerhafte Beschriftung – auf Wunsch planen wir beides zusammen.'),
  ('Brauche ich ein fertiges Design?', 'Nein, Ihr Logo reicht. Daraus gestalten wir die Beschriftung passend zu Ihren Fenstern.'),
 ],
 links=[('/schaufensterbeschriftung-berlin.html', 'Schaufensterbeschriftung: Beispiele'), ('/fensterfolie-nrw.html', 'Fensterfolie NRW'), ('/blog/sichtschutz-praxis-fenster.html', 'Sichtschutz für Praxisfenster')] + [('/schaufensterbeschriftung-koeln.html', 'Schaufenster Köln'), ('/schaufensterbeschriftung-duesseldorf.html', 'Schaufenster Düsseldorf'), ('/schaufensterbeschriftung-dortmund.html', 'Schaufenster Dortmund'), ('/schaufensterbeschriftung-essen.html', 'Schaufenster Essen'), ('/schaufensterbeschriftung-bochum.html', 'Schaufenster Bochum')] + CITY_LINKS[:1],
 form_opts=['Schaufensterbeschriftung', 'Milchglas / Sichtschutz', 'Druck- oder Lochfolie', 'Eröffnungsfolie', 'Öffnungszeiten an der Tür'],
 form_labels=('Was soll aufs Fenster?', 'Fenster &amp; Wunsch', 'Foto der Fenster (optional)', 'Ein Foto der Fenster von außen und ungefähre Maße reichen für ein erstes Angebot. Ihr Logo können Sie gleich mitschicken.'),
 form_sub='Schicken Sie uns ein Foto der Fenster und Ihr Logo – Sie bekommen innerhalb von 24 Stunden ein Angebot. Unser Team in NRW montiert bei Ihnen vor Ort.',
 subject='Anfrage Schaufensterbeschriftung NRW (Website)', msg_ph='z. B. 3 Schaufenster je ca. 1,2 × 2 m, Logo und Leistungen, Milchglas unten, Laden in Düsseldorf-Bilk',
 sticky=('Schaufensterbeschriftung NRW', 'Team vor Ort, blasenfreie Montage'))
W['faq_h2'] = 'Schaufenster NRW – <em>Fragen &amp; Antworten</em>'

# ---------------------------------------------------------------- Fensterfolie
F = dict(COMMON)
F.update(file='fensterfolie-nrw.html', crumb='Fensterfolie NRW', img='fensterfolie', img_q='?v=2', tab_ey='Folienarten',
 img_alt='Beispiel-Visualisierung: Bürofenster mit Sonnenschutz- und Sichtschutzfolie',
 title='Fensterfolie NRW: Sonnenschutz, Sichtschutz & Sicherheit | Masar',
 desc='Fensterfolie in NRW: Sonnenschutz gegen Hitze, Sichtschutz für Praxis und Büro, Sicherheitsfolie – mit Glasprüfung und Montage vor Ort in ganz NRW.',
 service_type='Montage von Fensterfolien', schema_name='Fensterfolie in NRW',
 badge='Fensterfolie · NRW', h1='Fensterfolie <em>NRW</em>',
 sub='Zu heiß im Büro, zu viel Einblick in die Praxis oder Sorge um Glasbruch? Die passende Folie löst das, ohne neue Fenster. Wir prüfen Ihr Glas, beraten zur richtigen Folie und unser Team in NRW montiert sie bei Ihnen vor Ort.',
 trust='Sonnenschutz · Sichtschutz · Spiegelfolie · Sicherheitsfolie',
 usp=['Team vor Ort in NRW', 'Glas wird geprüft', 'Für Büro, Praxis, Laden', 'Angebot in 24 h'],
 wa='Hallo, ich interessiere mich für Fensterfolie in NRW. Ich schicke Ihnen ein Foto der Fenster.',
 angles_ey='Wofür Fensterfolie', angles_h2='Ein Problem am Fenster – <em>eine passende Folie</em>',
 angles_sub='Fensterfolie ist eine schnelle Lösung für Glas, das zu heiß, zu durchsichtig oder zu unsicher ist.',
 angles=[
  ('Hitze & Blendung', 'Große Glasflächen in Büros und Läden heizen sich im Sommer stark auf. Sonnenschutzfolie hält einen Teil der Sonnenenergie draußen und reduziert Blendung am Bildschirm.'),
  ('Blicke von außen', 'Im Erdgeschoss an einer belebten Straße sieht jeder hinein. Milchglas- oder Spiegelfolie schützt Praxis, Büro und Wohnung.'),
  ('Splitterschutz', 'Sicherheitsfolie hält Glassplitter bei Bruch zusammen und erschwert einen schnellen Durchgriff.'),
  ('Ohne Umbau', 'Keine neuen Fenster, keine Baustelle. Die Montage ist meist an einem Termin erledigt.'),
 ],
 gallery=dict(h2='Folien <em>aus unserer Arbeit</em>', sub='Milchglas und Druckfolie an einer Praxisfront – innen und außen verklebt.', note=BERLIN_NOTE, items=[
  ref('praxis-schaufenster-berlin-02', 'Fertige Praxisfront mit Milchglasfolie an Tür und Mittelfenstern und bedruckten Folien', 'Milchglas an Tür und Mittelfenstern: Licht kommt herein, Einblicke nicht.'),
  ref('praxis-schaufenster-berlin-01', 'Monteure verkleben Folie an der Schaufensterfront einer Praxis', 'Montage vor Ort: Glas reinigen, Folie zuschneiden, blasenfrei verkleben.'),
  ref('schaufensterbeschriftung-pflegedienst-berlin-01', 'Fensterbeschriftung eines Pflegedienstes mit Logo und Öffnungszeiten an der Tür', 'Kombination aus Sichtschutz und Beschriftung an Fenster und Tür.'),
 ]),
 tab_h2='Welche Folie <em>passt zu Ihrem Fenster?</em>', tab_sub='Nicht jede Folie passt auf jedes Glas – deshalb prüfen wir vorher.',
 tab_cols=['Folie', 'Wirkung', 'Gut zu wissen'],
 tab_rows=[
  ['Sonnenschutzfolie', 'weniger Hitze und Blendung', 'Innen- oder Außenfolie je nach Glas – wir prüfen das vorher'],
  ['Milchglasfolie', 'Sichtschutz, Licht bleibt', 'auch als Streifen, mit Logo oder Muster'],
  ['Spiegelfolie', 'tagsüber kaum Einblick', 'nachts dreht sich der Effekt um, wenn innen Licht brennt'],
  ['Sicherheitsfolie', 'Splitterschutz, mehr Widerstand', 'geprüft nach DIN EN 12600 bzw. DIN EN 356'],
  ['Dekorfolie', 'Gestaltung und Sichtschutz zugleich', 'Motive, Logos, Farbverläufe'],
 ],
 tab_note='Ausführliche Infos zu jeder Folie: <a href="/sonnenschutzfolie-berlin.html">Sonnenschutzfolie</a>, <a href="/sichtschutzfolie-berlin.html">Sichtschutzfolie</a>, <a href="/sicherheitsfolie-berlin.html">Sicherheitsfolie</a>. Werbung auf dem Glas: <a href="/schaufensterbeschriftung-nrw.html">Schaufensterbeschriftung NRW</a>.',
 svc_h2='Fensterfolie <em>in NRW</em>',
 services=[
  ('sonne', 'Sonnenschutzfolie', 'Gegen Hitze und Blendung in Büro, Laden und Wintergarten.', '/sonnenschutzfolie-berlin.html'),
  ('auge', 'Sichtschutzfolie', 'Milchglas, Streifen oder Dekor für Praxis, Büro und Bad.', '/sichtschutzfolie-berlin.html'),
  ('spiegel', 'Spiegelfolie', 'Einseitiger Sichtschutz am Tag für Büro und Erdgeschoss.', '/blog/spiegelfolie-nachts.html'),
  ('schutz', 'Sicherheitsfolie', 'Splitterschutz und durchwurfhemmende Folie nach DIN-Norm.', '/sicherheitsfolie-berlin.html'),
  ('glas', 'Glastür-Markierung', 'Markierung für Ganzglastüren nach Arbeitsstättenregel.', '/blog/glastueren-kennzeichnen.html'),
  ('thermo', 'Glasprüfung', 'Wir prüfen Glasart und Lage, bevor wir eine Folie empfehlen.', '#kontakt'),
 ],
 preis_h2='Was kostet <em>Fensterfolie in NRW?</em>',
 preis_html='''<p>Sichtschutzfolie gibt es in NRW ab 229&nbsp;€ netto zzgl. 19&nbsp;% MwSt. Bei Sonnenschutz- und Sicherheitsfolie hängt der Preis stark von Folientyp, Fläche und Zugänglichkeit der Fenster ab – deshalb kalkulieren wir nach Fotos und Maßen.</p>
<p>Sie bekommen ein <strong>Festpreis-Angebot</strong> inklusive Montage durch unser Team in NRW – kostenlos und in der Regel innerhalb von 24 Stunden. Was die Kosten bestimmt, erklären wir im Ratgeber <a href="/blog/sonnenschutzfolie-kosten.html">Sonnenschutzfolie: Kosten</a>.</p>''',
 recht_ey='Gut zu wissen', recht_h2='Vor der Montage <em>prüfen wir das Glas</em>', recht_sub=None,
 recht_html='''<p><strong>Glasprüfung:</strong> Eine innen geklebte Sonnenschutzfolie kann das Glas zusätzlich erwärmen. Bei manchen Gläsern – etwa großen, teils verschatteten Scheiben oder bestimmten Isoliergläsern – steigt dadurch das Risiko eines Hitzesprungs. Deshalb prüfen wir Glasart und Lage und empfehlen dann Innen- oder Außenfolie.</p>
<p><strong>Mietobjekt:</strong> Im Mietobjekt sollten Sie die Folie mit dem Vermieter abstimmen. Folien lassen sich später wieder entfernen.</p>
<p><strong>Sicherheitsfolie:</strong> Für eine geprüfte Schutzwirkung kommt es auf Folie und Montage an. Wir nennen Ihnen im Angebot, nach welcher Norm die Folie geprüft ist.</p>''',
 ablauf=[
  ('Fotos & Problem', 'Sie schicken uns Fotos der Fenster und sagen, was stört – Hitze, Einblicke oder Sicherheit.'),
  ('Glas & Beratung', 'Wir prüfen anhand der Angaben Glasart und Lage und empfehlen die passende Folie.'),
  ('Festpreis & Termin', 'Sie bekommen ein schriftliches Angebot, wir vereinbaren den Montagetermin in NRW.'),
  ('Montage vor Ort', 'Unser Team reinigt die Scheiben und verklebt die Folie sauber und blasenfrei.'),
 ],
 faq=[
  ('In welchen Städten montieren Sie Fensterfolie?', 'In ganz NRW, mit Schwerpunkt Düsseldorf, Köln, Dortmund, Essen und Bochum, dazu Duisburg, Wuppertal, Bonn und die Städte dazwischen. Unser Firmensitz ist in Berlin.'),
  ('Innen oder außen – was ist besser?', 'Das hängt vom Glas ab. Außenfolie hält mehr Hitze draußen, Innenfolie ist vor Wetter geschützt. Bei manchen Gläsern ist Innenfolie wegen der Hitzesprung-Gefahr nicht geeignet. Mehr dazu im Ratgeber <a href="/blog/sonnenschutzfolie-innen-oder-aussen.html">Sonnenschutzfolie innen oder außen</a>.'),
  ('Sieht man nachts durch Spiegelfolie hinein?', 'Ja, wenn es innen heller ist als außen. Für Sichtschutz rund um die Uhr ist Milchglasfolie besser.'),
  ('Wird es mit Sonnenschutzfolie dunkler?', 'Etwas, je nach Folie. Es gibt helle Folien, die viel Licht durchlassen und trotzdem Hitze reduzieren. Wir zeigen Ihnen die Unterschiede.'),
  ('Lässt sich die Folie wieder entfernen?', 'Ja. Fensterfolien lassen sich später ablösen. Wie leicht das geht, hängt von Folie und Alter ab.'),
  ('Wie lange dauert die Montage?', 'Für ein Büro oder eine Ladenfront meist ein Termin. Bei großen Glasfassaden nennen wir die Dauer im Angebot.'),
 ],
 links=[('/fensterfolie-berlin.html', 'Fensterfolien: Übersicht'), ('/blog/sonnenschutzfolie-glasfassade-buero.html', 'Sonnenschutz für Glasfassade & Büro'), ('/schaufensterbeschriftung-nrw.html', 'Schaufensterbeschriftung NRW')] + CITY_LINKS[:1],
 form_opts=['Sonnenschutzfolie', 'Sichtschutz / Milchglas', 'Spiegelfolie', 'Sicherheitsfolie', 'Glastür-Markierung'],
 form_sub='Schicken Sie uns Fotos der Fenster und sagen Sie uns, was stört – Sie bekommen innerhalb von 24 Stunden ein Angebot. Unser Team in NRW montiert bei Ihnen vor Ort.',
 subject='Anfrage Fensterfolie NRW (Website)', msg_ph='z. B. Büro mit 6 Fenstern nach Süden, je ca. 1,5 × 2 m, zu heiß im Sommer, 2. OG in Dortmund',
 sticky=('Fensterfolie NRW', 'Glas geprüft, Montage vor Ort'))
F['faq_h2'] = 'Fensterfolie NRW – <em>Fragen &amp; Antworten</em>'

# ---------------------------------------------------------------- Webdesign
D = dict(COMMON)
D.update(file='webdesign-nrw.html', crumb='Webdesign NRW', img='webdesign', tab_ey='Pakete',
 img_alt='Beispiel-Visualisierung: moderne Website auf Laptop und Smartphone',
 title='Webdesign NRW: Websites für Unternehmen | Masar',
 desc='Webdesign für Unternehmen in NRW: schnelle, mobile Websites und Landingpages für Düsseldorf, Köln und das Ruhrgebiet – mit Texten und SEO-Grundlagen.',
 service_type='Webdesign', schema_name='Webdesign in NRW', svc_sub='Von der ersten Idee bis zur fertigen Website – alles aus einer Hand.',
 badge='Webdesign · NRW', h1='Webdesign <em>NRW</em>',
 sub='Eine Website, die auf dem Handy schnell lädt, bei Google gefunden wird und aus Besuchern Anfragen macht. Wir planen, gestalten und programmieren Websites und Landingpages für Betriebe in ganz NRW – abgestimmt per Video-Call, Telefon oder WhatsApp.',
 trust='Websites · Landingpages · Relaunch · SEO-Grundlagen',
 usp=['Mobil zuerst', 'Schnelle Ladezeit', 'SEO-Grundlagen inklusive', 'Abstimmung online'],
 wa='Hallo, ich interessiere mich für eine neue Website. Mein Unternehmen ist in NRW.',
 angles_ey='Warum eine neue Website', angles_h2='Ihre Website <em>ist Ihr bester Verkäufer</em>',
 angles_sub='Die meisten Kunden suchen zuerst online – auch für den Handwerker um die Ecke.',
 angles=[
  ('Gefunden werden', 'Wer in Köln „Elektriker in der Nähe“ sucht, landet bei Google. Eine saubere technische Grundlage und klare Seiten pro Leistung helfen, dort sichtbar zu werden.'),
  ('Schnell auf dem Handy', 'Die meisten Besucher kommen vom Smartphone. Lädt die Seite langsam oder ist schwer zu bedienen, sind sie weg.'),
  ('Anfragen statt Besucher', 'Klare Texte, sichtbare Preise oder Beispiele und ein einfaches Formular oder WhatsApp-Kontakt machen aus Besuchern Kunden.'),
  ('Passend zum Auftritt', 'Website, Schild, Fahrzeug und Flyer im selben Design – weil alles aus einer Hand kommt.'),
 ],
 gallery=dict(h2='Webdesign <em>von uns</em>', sub='Unsere eigene Website haben wir selbst gestaltet und programmiert – inklusive interaktivem Anfrage-Assistenten.', note='Die Website, auf der Sie gerade sind, ist von uns. <a href="/webdesign-berlin.html">Mehr zu unserem Webdesign →</a>', items=[
  ref('webdesign-masar-desktop', 'Startseite der Website masar-werbeagentur.de am Desktop', 'Startseite am Desktop: klare Botschaft, direkte Wege zu Leistungen und Anfrage.', True),
  ref('webdesign-masar-mobil', 'Startseite der Website masar-werbeagentur.de auf dem Smartphone', 'Dieselbe Seite auf dem Smartphone – für Daumen und kleine Bildschirme gebaut.', True),
  ref('webdesign-masar-assistent', 'Interaktiver Folien-Finder auf masar-werbeagentur.de mit Auswahlfeldern', 'Interaktiver Assistent: In zwei Schritten zur passenden Lösung und Anfrage.', True),
 ]),
 tab_h2='Was Ihre Website <em>bekommt</em>', tab_sub='Jede Website ist anders – diese Grundlagen sind bei uns immer dabei.',
 tab_cols=['Bereich', 'Was wir machen', 'Ihr Vorteil'],
 tab_rows=[
  ['Gestaltung', 'eigenes Design passend zu Logo und Branche', 'kein Baukasten-Look'],
  ['Mobil & schnell', 'für Smartphone optimiert, schlanke Technik', 'Besucher bleiben, Google wertet es positiv'],
  ['Texte & Struktur', 'Seiten pro Leistung, klare Wege zur Anfrage', 'mehr Anfragen aus denselben Besuchern'],
  ['SEO-Grundlagen', 'Titel, Beschreibungen, strukturierte Daten, Sitemap', 'solide Basis für Google'],
  ['Recht & Technik', 'Impressum, Datenschutz-Struktur, SSL, Formular', 'sicher und vollständig online'],
 ],
 tab_note='Mehr zu Leistungen und Ablauf: <a href="/webdesign-berlin.html">Webdesign</a>. Rechtliche Texte erstellen wir nicht als Rechtsberatung – wir bauen die Struktur, die Inhalte stimmen Sie mit Ihrem Berater ab.',
 svc_h2='Webdesign <em>für NRW</em>',
 services=[
  ('web', 'Neue Website', 'Firmenwebsite mit allen Leistungen, Referenzen und Kontakt.', '#kontakt'),
  ('stern', 'Landingpage', 'Eine Seite für ein Angebot oder eine Kampagne – auf Anfragen ausgerichtet.', '#kontakt'),
  ('druck', 'Relaunch', 'Ihre alte Website modern, schnell und mobil – Inhalte übernehmen wir.', '#kontakt'),
  ('auge', 'SEO-Grundlagen', 'Technik und Struktur, damit Google Ihre Seiten versteht.', '#kontakt'),
  ('phone', 'Kontakt & WhatsApp', 'Formulare, Anruf- und WhatsApp-Buttons, die funktionieren.', '#kontakt'),
  ('karte', 'Alles im Design', 'Passend dazu Logo, Flyer, Schilder und Fahrzeug.', '/werbeagentur-nrw.html'),
 ],
 preis_h2='Was kostet <em>eine Website?</em>',
 preis_html='''<p>Der Preis hängt vom Umfang ab: Eine Landingpage ist schneller umgesetzt als eine Website mit vielen Leistungsseiten, Mehrsprachigkeit oder Shop. Auch, ob wir Texte und Bilder erstellen oder Sie diese liefern, macht einen Unterschied.</p>
<p>Nach einem kurzen Gespräch bekommen Sie ein <strong>Festpreis-Angebot</strong> mit allen Seiten und Funktionen – kostenlos und unverbindlich.</p>''',
 recht_ey='So arbeiten wir', recht_h2='Zusammenarbeit <em>über die Entfernung</em>', recht_sub=None,
 recht_html='''<p><strong>Online statt Anfahrt:</strong> Für eine Website müssen wir nicht bei Ihnen vor Ort sein. Wir stimmen uns per Video-Call, Telefon, E-Mail oder WhatsApp ab – das spart Ihnen Zeit.</p>
<p><strong>Sie sehen alles vorher:</strong> Vor dem Livegang bekommen Sie einen Vorschau-Link und können jede Seite prüfen. Änderungswünsche setzen wir um, bevor die Seite online geht.</p>
<p><strong>Fotos vor Ort:</strong> Für Werbetechnik ist unser Team in NRW bei Ihnen vor Ort. Foto- und Videoaufnahmen bieten wir in NRW allerdings nicht an – dafür nutzen wir Ihre Bilder oder lizenzierte Fotos.</p>''',
 ablauf=[
  ('Gespräch', 'Kurzer Call: Was bieten Sie an, wer sind Ihre Kunden, was soll die Website erreichen?'),
  ('Konzept & Angebot', 'Wir planen Seiten und Inhalte und schicken Ihnen ein Festpreis-Angebot.'),
  ('Design & Umsetzung', 'Wir gestalten und programmieren die Website. Sie prüfen alles über einen Vorschau-Link.'),
  ('Livegang', 'Nach Ihrer Freigabe geht die Seite online – mit Sitemap und Anmeldung bei Google.'),
 ],
 faq=[
  ('Arbeiten Sie auch für Unternehmen in NRW?', 'Ja. Webdesign stimmen wir online ab – per Video-Call, Telefon oder WhatsApp. Für Werbetechnik wie Schilder oder Fahrzeugbeschriftung ist zusätzlich unser Team in NRW vor Ort. Unser Firmensitz ist in Berlin.'),
  ('Wie lange dauert eine neue Website?', 'Das hängt vom Umfang und davon ab, wie schnell Inhalte vorliegen. Den Zeitplan nennen wir im Angebot.'),
  ('Muss ich die Texte selbst schreiben?', 'Nein. Wir schreiben die Texte auf Wunsch nach einem Gespräch mit Ihnen. Sie prüfen und geben frei.'),
  ('Kann ich die Website später selbst ändern?', 'Kleine Änderungen übernehmen wir schnell für Sie. Wenn Sie selbst regelmäßig Inhalte pflegen möchten, planen wir das von Anfang an mit ein.'),
  ('Kümmern Sie sich um Google?', 'Wir legen die technischen SEO-Grundlagen und melden die Seite bei Google an. Platzierungen kann niemand garantieren – eine saubere Grundlage ist aber die Voraussetzung.'),
  ('Was ist mit Domain und Hosting?', 'Wir beraten Sie dazu und richten alles ein. Die Domain läuft auf Ihren Namen, damit sie Ihnen gehört.'),
 ],
 links=[('/webdesign-berlin.html', 'Webdesign: Leistungen'), ('/grafikdesign-berlin.html', 'Grafikdesign & Logo'), ('/blog/bfsg-website-barrierefreiheit.html', 'Barrierefreiheit (BFSG)'), ('/werbeagentur-nrw.html', 'Werbeagentur NRW')] + CITY_LINKS[1:],
 form_opts=['Neue Website', 'Landingpage', 'Relaunch der bestehenden Website', 'Website + Logo / Design', 'SEO / Sichtbarkeit'],
 form_labels=('Was brauchen Sie?', 'Unternehmen &amp; Wunsch', 'Datei (optional)', 'Zum Beispiel Ihr Logo oder eine Liste Ihrer Leistungen. Den Rest besprechen wir im Gespräch.'),
 form_sub='Erzählen Sie uns kurz von Ihrem Unternehmen – wir melden uns innerhalb von 24 Stunden und vereinbaren ein kurzes Gespräch.',
 subject='Anfrage Webdesign NRW (Website)', msg_ph='z. B. Malerbetrieb in Bochum, 5 Mitarbeiter, alte Website von 2015, möchten mehr Anfragen über Google',
 sticky=('Webdesign NRW', 'Abstimmung online, Festpreis'))
D['faq_h2'] = 'Webdesign NRW – <em>Fragen &amp; Antworten</em>'

L['top'] = price_top('Was kostet <em>Leuchtreklame in NRW?</em>', None, ROWS_L, PRICE_NOTE)
S['top'] = price_top('Was kostet <em>ein Schild in NRW?</em>', None, ROWS_S, PRICE_NOTE)
F['top'] = price_top('Was kostet <em>Fensterfolie in NRW?</em>', None, ROWS_F, PRICE_NOTE)
W['top'] = price_top('Was kostet <em>eine Schaufensterbeschriftung in NRW?</em>', None, ROWS_W, PRICE_NOTE)
PAGES = [L, S, W, F, D]

def nrw_fix(p):
    """NRW: WhatsApp und E-Mail statt Telefon in Navigation und mobilem Menü."""
    import urllib.parse
    h = open(ROOT + p['file'], encoding='utf-8').read()
    txt = urllib.parse.quote(f"Hallo, ich möchte ein Angebot für {p['crumb']}.")
    wa_nav = (f'<a href="https://wa.me/491785143918?text={txt}" target="_blank" rel="noopener noreferrer" class="nav-phone" aria-label="Per WhatsApp schreiben">\n'
              '      <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 3a8.5 8.5 0 0 0-7.4 12.7L3 21l5.4-1.5A8.5 8.5 0 1 0 12 3Zm-3 7.2h6a.8.8 0 0 1 0 1.6H9a.8.8 0 0 1 0-1.6Zm0 3h4a.8.8 0 0 1 0 1.6H9a.8.8 0 0 1 0-1.6Z"/></svg>\n      WhatsApp\n    </a>')
    h, n1 = re.subn(r'<a href="tel:01785143918" class="nav-phone".*?</a>', lambda m: wa_nav, h, count=1, flags=re.S)
    h, n2 = re.subn(r'<a href="tel:01785143918" class="mob-call-btn">.*?</a>', lambda m: '<a href="#kontakt" class="mob-call-btn"><svg class="i-inline" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>E-Mail</a>', h, count=1, flags=re.S)
    h = h.replace('placeholder="z. B. Berlin-Mitte"', 'placeholder="z. B. Köln-Ehrenfeld"')
    open(ROOT + p['file'], 'w', encoding='utf-8').write(h)
    return n1, n2

if __name__ == '__main__':
    for p in PAGES:
        print(build_f(p), nrw_fix(p))
