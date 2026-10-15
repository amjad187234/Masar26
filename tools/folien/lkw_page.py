"""LKW-Beschriftung Berlin – eigene Landingpage (Generator: gen_folien.build_f)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'gen_folien.py'), encoding='utf-8').read()
exec(src[:src.index("\nif __name__")])

P = dict(file='lkw-beschriftung-berlin.html', crumb='LKW-Beschriftung', img='lkw-beschriftung',
 parent=('Fahrzeugbeschriftung', 'fahrzeugbeschriftung-berlin.html'), finder_strip=False, tab_ey='Flächen', hero_mobile=True,
 img_alt='Beispiel-Visualisierung: weißer Sattelzug mit Logo auf Fahrerhaus und Plane und blauem Wellendesign – so kann Ihr LKW als Werbefläche aussehen',
 title='LKW-Beschriftung Berlin: Plane, Koffer & Fahrerhaus | Masar',
 desc='LKW-Beschriftung in Berlin für Unternehmen: Fahrerhaus, Kofferaufbau, bedruckte Plane oder Vollfolierung – mit Gestaltung, Produktion und Montage bei Ihnen vor Ort.',
 service_type='LKW-Beschriftung', schema_name='LKW-Beschriftung in Berlin',
 badge='LKW-Beschriftung · Berlin', h1='LKW-Beschriftung <em>Berlin</em>',
 sub='Ein LKW ist jeden Tag auf Autobahn, Stadtstraße und Rampe unterwegs – und damit eine der größten Werbeflächen, die ein Unternehmen haben kann. Wir gestalten, produzieren und montieren die Beschriftung für Fahrerhaus, Kofferaufbau und Plane. Die Montage machen wir bei Ihnen vor Ort in Berlin und Umgebung.',
 trust='Fahrerhaus · Kofferaufbau · Plane · Vollfolierung · Flotten',
 usp=['Montage bei Ihnen vor Ort', 'Gestaltung aus einer Hand', 'Einzelfahrzeug bis Flotte', 'Angebot in 24 h'],
 wa='Hallo, ich interessiere mich für eine LKW-Beschriftung. Ich schicke Ihnen Fotos des Fahrzeugs.',
 angles_ey='Warum LKW', angles_h2='Die größte Werbefläche <em>Ihres Betriebs</em>',
 angles_sub='Ein Firmenschild sieht, wer vorbeikommt. Einen LKW sieht jeder, an dem er vorbeifährt.',
 angles=[
  ('Riesige Fläche', 'Plane und Kofferaufbau bieten Platz für Logo, Leistungen und Kontakt in einer Größe, die man auch aus dem Gegenverkehr oder von der Nachbarspur liest.'),
  ('Jeden Tag unterwegs', 'Die Werbung fährt mit, wohin Ihr Betrieb fährt – auf der Autobahn, in der Innenstadt, beim Kunden auf dem Hof. Ohne Monatsmiete wie bei Plakatflächen.'),
  ('Professioneller Auftritt', 'Ein einheitlich beschrifteter Fuhrpark wirkt zuverlässig. Kunden, Partner und Bewerber erkennen Ihr Unternehmen auf den ersten Blick.'),
  ('Recruiting', 'Fahrer und Fachkräfte werden gesucht. Ein gut lesbarer Hinweis „Wir stellen ein“ mit Website oder QR-Code erreicht genau die Menschen auf der Straße.'),
 ],
 tab_h2='Was wir an Ihrem <em>LKW beschriften</em>', tab_sub='Welche Lösung passt, hängt vom Aufbau ab – Koffer, Plane oder Fahrerhaus.',
 tab_cols=['Fläche', 'Lösung', 'Gut zu wissen'],
 tab_rows=[
  ['Fahrerhaus', 'Logo, Schriftzug, Kontakt als geplottete oder bedruckte Folie', 'Sichtfeld des Fahrers bleibt frei'],
  ['Kofferaufbau', 'Großflächiger Digitaldruck oder Folienschrift', 'glatte Fläche – ideal für große Motive'],
  ['Plane (Curtainsider)', 'Neue bedruckte Plane oder Folie auf der vorhandenen Plane', 'Folie nur auf Planen in gutem Zustand'],
  ['Heck und Türen', 'Kontakt, Website, QR-Code', 'Rückleuchten und Kennzeichen bleiben frei'],
  ['Vollfolierung', 'Fahrerhaus oder ganzes Fahrzeug in neuer Farbe oder mit Motiv', 'Lack wird zugleich geschützt'],
 ],
 tab_note='Auf Wunsch gestalten wir alle Fahrzeuge Ihrer Flotte im selben Design – vom Transporter bis zum Sattelzug. Für PKW und Transporter siehe <a href="/fahrzeugbeschriftung-berlin.html">Fahrzeugbeschriftung</a>. Ihre Fahrzeuge stehen in Nordrhein-Westfalen? <a href="/lkw-beschriftung-nrw.html">LKW-Beschriftung NRW</a>.',
 svc_h2='Unsere Leistungen <em>für LKW</em>', svc_sub='Von der ersten Skizze bis zum fertig beklebten Fahrzeug – aus einer Hand.',
 services=[
  ('karte', 'Fahrerhaus-Beschriftung', 'Logo und Name auf Türen und Front – der schnellste Weg zum beschrifteten LKW.', '#kontakt'),
  ('druck', 'Kofferaufbau', 'Großformatiger Digitaldruck auf Folie für Koffer- und Kühlaufbauten.', '#kontakt'),
  ('schild', 'Planendruck', 'Neue Plane mit Druck oder Folienbeschriftung auf der vorhandenen Plane.', '#kontakt'),
  ('glas', 'Vollfolierung', 'Fahrerhaus oder ganzes Fahrzeug in neuer Farbe oder mit vollflächigem Motiv.', '/fahrzeugbeschriftung-berlin.html'),
  ('stern', 'Flotten', 'Einheitliches Design für alle Fahrzeuge – Transporter, LKW, Anhänger.', '/fahrzeugbeschriftung-berlin.html'),
  ('web', 'Gestaltung', 'Wir entwickeln das Design passend zu Ihrem Corporate Design – oder ein neues.', '/grafikdesign-berlin.html'),
 ],
 preis_h2='Was kostet <em>LKW-Beschriftung?</em>',
 preis_html='''<p>Der Preis hängt stark vom Fahrzeug ab: Ein Logo auf zwei Fahrerhaustüren ist etwas völlig anderes als ein bedruckter Sattelauflieger. Entscheidend sind die Fläche, ob gedruckt oder geplottet wird, ob eine neue Plane nötig ist, der Gestaltungsaufwand und die Zahl der Fahrzeuge.</p>
<p>Deshalb nennen wir keinen Pauschalpreis, sondern machen Ihnen nach Fotos und Maßen ein <strong>Festpreis-Angebot</strong> – kostenlos und in der Regel innerhalb von 24 Stunden. Bei mehreren Fahrzeugen rechnen wir die Flotte gemeinsam.</p>''',
 recht_ey='Gut zu wissen', recht_h2='Was bei LKW <em>frei bleiben muss</em>', recht_sub=None,
 recht_html='''<p><strong>Konturmarkierung:</strong> Für Lkw über 7,5&nbsp;t und Anhänger über 3,5&nbsp;t, die seit Juli 2011 neu zugelassen werden, ist eine retroreflektierende Konturmarkierung vorgeschrieben; sie wird bei der Hauptuntersuchung geprüft. Diese Markierung darf durch Beschriftung nicht verdeckt oder beschädigt werden – wir planen das Design deshalb um sie herum.</p>
<p><strong>Licht, Kennzeichen, Scheiben:</strong> Leuchten, Rückstrahler und Kennzeichen bleiben frei. Auch das Sichtfeld des Fahrers durch Front- und Seitenscheiben bleibt unbeklebt.</p>
<p><strong>Plane:</strong> Folie auf einer vorhandenen Plane hält nur, wenn die Plane in gutem Zustand ist; Folienhersteller geben die volle Gewährleistung oft nur auf neuen Planen. Bei älteren Planen ist eine neue, bedruckte Plane meist die bessere Lösung.</p>
<p><strong>Abgestellte Werbefahrzeuge:</strong> Ein LKW mit Werbung darf ganz normal am Straßenrand parken. Wird ein Fahrzeug oder Anhänger aber vor allem zu Werbezwecken im öffentlichen Straßenraum abgestellt, kann das eine genehmigungspflichtige Sondernutzung sein.</p>
<p><strong>Montage bei Ihnen:</strong> Wir kommen zu Ihnen. Für die Montage brauchen wir einen überdachten, trockenen Platz, an dem das Fahrzeug für die Dauer der Arbeiten stehen kann – zum Beispiel eine Halle oder ein Carport. Folie lässt sich nicht bei Regen und nicht bei großer Kälte verkleben.</p>''',
 ablauf=[
  ('Fotos & Maße', 'Sie schicken uns Fotos des Fahrzeugs von allen Seiten, die Maße des Aufbaus und Ihr Logo – per WhatsApp oder Formular.'),
  ('Entwurf', 'Wir gestalten das Design auf einer Ansicht Ihres Fahrzeugtyps – Sie sehen vorher, wie der LKW aussehen wird.'),
  ('Festpreis & Termin', 'Sie bekommen ein schriftliches Angebot und wir vereinbaren den Montagetermin bei Ihnen vor Ort.'),
  ('Produktion & Montage', 'Wir produzieren Folie oder Plane und montieren am vereinbarten Tag bei Ihnen.'),
 ],
 faq_h2='LKW-Beschriftung – <em>Fragen &amp; Antworten</em>',
 faq=[
  ('Kommen Sie zu uns auf den Hof?', 'Ja. Wir montieren bei Ihnen vor Ort in Berlin und Umgebung. Wichtig ist ein überdachter, trockener Platz, an dem das Fahrzeug während der Montage stehen kann.'),
  ('Wie lange steht der LKW still?', 'Das hängt vom Umfang ab. Eine Fahrerhaus-Beschriftung ist deutlich schneller erledigt als eine Vollfolierung. Die Dauer nennen wir Ihnen im Angebot, damit Sie die Tour planen können.'),
  ('Plane bedrucken oder Folie auf die Plane?', 'Ist die Plane neu oder in gutem Zustand, ist Folie möglich. Bei älteren Planen empfehlen wir eine neue bedruckte Plane – sie hält besser und lässt sich besser falten und öffnen.'),
  ('Lässt sich die Beschriftung wieder entfernen?', 'Ja. Folienbeschriftung lässt sich später wieder entfernen, zum Beispiel beim Verkauf oder Leasing-Rückgabe. Wie leicht das geht, hängt von Folie, Alter und Lackzustand ab.'),
  ('Machen Sie auch mehrere Fahrzeuge?', 'Ja. Für Flotten entwickeln wir ein einheitliches Design, das auf Transporter, LKW und Anhänger passt, und planen die Montage so, dass nicht alle Fahrzeuge gleichzeitig stehen.'),
  ('Brauchen wir ein fertiges Design?', 'Nein. Ihr Logo reicht. Daraus entwickeln wir das Fahrzeugdesign. Haben Sie schon ein Design, prüfen wir es und bereiten es für die Produktion auf.'),
 ],
 links=[('/fahrzeugbeschriftung-berlin.html', 'Fahrzeugbeschriftung PKW & Transporter'), ('/blog/fahrzeugbeschriftung-tipps.html', 'Fahrzeugbeschriftung: 7 Tipps'),
        ('/blog/fahrzeugbeschriftung-kosten-berlin.html', 'Fahrzeugbeschriftung: Kosten'), ('/grafikdesign-berlin.html', 'Grafikdesign'), ('/referenzen.html', 'Referenzen')],
 form_opts=['Fahrerhaus-Beschriftung', 'Kofferaufbau', 'Plane (Curtainsider)', 'Vollfolierung', 'Mehrere Fahrzeuge / Flotte'],
 form_labels=('Was soll beschriftet werden?', 'Fahrzeug &amp; Wunsch', 'Fotos des Fahrzeugs (optional)', 'Fotos von allen Seiten, Fahrzeugtyp und Maße des Aufbaus reichen für ein erstes Angebot. Ihr Logo können Sie gleich mitschicken.'),
 form_sub='Schicken Sie uns Fotos des Fahrzeugs, die Maße des Aufbaus und Ihr Logo – Sie bekommen innerhalb von 24 Stunden ein Angebot.',
 subject='Anfrage LKW-Beschriftung (Website)', msg_ph='z. B. 2 × 7,5-t-Koffer-LKW, Logo und Leistungen auf beiden Seiten und am Heck, Montage auf unserem Hof in Berlin-Spandau',
 sticky=('LKW-Beschriftung Berlin', 'Montage bei Ihnen vor Ort'))


SCHRIFT = ('Lesbarkeit', 'Wie groß muss <em>die Schrift sein?</em>',
 'Was man aus 30 Metern nicht lesen kann, ist auf dem LKW verschenkte Fläche. Diese Richtwerte helfen bei der Planung.',
 """    <div class="price-scroll">
      <table class="price-table rt">
        <caption class="sr-only" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);">Schrifthöhe nach Leseabstand</caption>
        <thead><tr><th scope="col">Leseabstand</th><th scope="col">Typische Situation</th><th scope="col">Mindestens</th><th scope="col">Empfohlen am Fahrzeug</th></tr></thead>
        <tbody>
          <tr><td data-label="Leseabstand">5 m</td><td data-label="Situation">Parkplatz, Laderampe, Kunde steht daneben</td><td data-label="Mindestens">ca. 3 cm</td><td class="pcell" data-label="Empfohlen">ca. 6 cm</td></tr>
          <tr><td data-label="Leseabstand">10 m</td><td data-label="Situation">Gehweg, Ampel, Nachbarfahrzeug</td><td data-label="Mindestens">ca. 6 cm</td><td class="pcell" data-label="Empfohlen">ca. 12 cm</td></tr>
          <tr><td data-label="Leseabstand">20 m</td><td data-label="Situation">Nebenspur, gegenüberliegende Straßenseite</td><td data-label="Mindestens">ca. 12 cm</td><td class="pcell" data-label="Empfohlen">ca. 23 cm</td></tr>
          <tr><td data-label="Leseabstand">30 m</td><td data-label="Situation">Gegenverkehr, Kreuzung</td><td data-label="Mindestens">ca. 17 cm</td><td class="pcell" data-label="Empfohlen">ca. 35 cm</td></tr>
          <tr><td data-label="Leseabstand">50 m</td><td data-label="Situation">Autobahn, Fahrzeug voraus</td><td data-label="Mindestens">ca. 29 cm</td><td class="pcell" data-label="Empfohlen">ca. 58 cm</td></tr>
        </tbody>
      </table>
    </div>
    <div class="blog-prose" style="max-width:820px;margin:1.5rem auto 0;">
      <p><strong>So lesen Sie die Tabelle:</strong> Angegeben ist die Höhe der Großbuchstaben. „Mindestens“ ist die Größe, ab der eine gut lesbare Schrift bei normaler Sehkraft und ruhigem Hinsehen gerade noch entziffert werden kann – berechnet aus dem in der Leserlichkeitsforschung üblichen Mindest-Sehwinkel (rund 2,9&nbsp;mm Versalhöhe auf 50&nbsp;cm Abstand). Am fahrenden LKW bleiben oft nur ein, zwei Sekunden – deshalb empfehlen wir etwa das Doppelte.</p>
      <p><strong>Faustregel für die Planung:</strong> Logo und Firmenname groß für die Ferne, Leistungen mittelgroß, Telefon und Website so groß, dass man sie an der Ampel abschreiben kann. Je weniger Text, desto größer darf er werden – drei Zeilen wirken mehr als zehn.</p>
      <p><strong>Außerdem wichtig:</strong> kräftige, einfache Schrift ohne Schnörkel, starker Kontrast zum Untergrund und Abstand zu Sicken, Türgriffen und Planenschnallen.</p>
      <p style="font-size:13px;">Quelle zur Berechnung: <a href="https://leserlich.info/zeichen/schriftgroesse" target="_blank" rel="noopener noreferrer">leserlich.info – Schriftgröße</a> (Grundlage DIN 1450). Richtwerte für die Planung, keine Norm-Vorgabe für Fahrzeuge.</p>
    </div>""")
P['extra'] = SCHRIFT

CITIES = ['Düsseldorf', 'Köln', 'Dortmund', 'Essen', 'Bochum', 'Duisburg', 'Wuppertal', 'Bonn']
N = dict(P)
N.update(file='lkw-beschriftung-nrw.html', crumb='LKW-Beschriftung NRW',
 parent=('Fahrzeugbeschriftung NRW', 'fahrzeugbeschriftung-nrw.html'),
 area=[{"@type": "State", "name": "Nordrhein-Westfalen"}] + [{"@type": "City", "name": c} for c in CITIES],
 img_alt='Beispiel-Visualisierung: weißer Sattelzug mit Logo auf Fahrerhaus und Plane – LKW-Beschriftung in NRW',
 title='LKW-Beschriftung NRW: Plane, Koffer & Fahrerhaus | Masar',
 desc='LKW-Beschriftung in NRW: Fahrerhaus, Koffer, Planendruck und Vollfolierung für Speditionen in Düsseldorf, Köln und im Ruhrgebiet – Montage vor Ort.',
 service_type='LKW-Beschriftung', schema_name='LKW-Beschriftung in NRW',
 badge='LKW-Beschriftung · NRW', h1='LKW-Beschriftung <em>NRW</em>',
 sub='Zwischen Rhein und Ruhr sind jeden Tag unzählige LKW unterwegs – auf der A1, A2, A3 und A40, in den Häfen und Gewerbegebieten. Machen Sie Ihre Fahrzeuge zur Werbefläche: Wir gestalten und produzieren die Beschriftung für Fahrerhaus, Kofferaufbau und Plane, unser Team in NRW montiert sie bei Ihnen vor Ort.',
 trust='Düsseldorf · Köln · Ruhrgebiet · Bonn · Wuppertal',
 usp=['Team vor Ort in NRW', 'Montage auf Ihrem Hof', 'Einzelfahrzeug bis Flotte', 'Angebot in 24 h'],
 wa='Hallo, ich interessiere mich für eine LKW-Beschriftung in NRW. Ich schicke Ihnen Fotos des Fahrzeugs.',
 angles_ey='Warum LKW', angles_h2='Ihr LKW wirbt <em>auf jeder Tour</em>',
 angles_sub='NRW ist eine der verkehrsreichsten Regionen Deutschlands. Ihr Fahrzeug ist dort jeden Tag sichtbar.',
 angles=[
  ('Sichtbar im dichtesten Verkehr', 'Stau auf der A40, Ladezone in der Kölner Innenstadt, Rampe im Duisburger Gewerbegebiet: Wo viele Fahrzeuge unterwegs sind, wird Ihr LKW von sehr vielen Menschen gesehen.'),
  ('Für Speditionen und Betriebe', 'Ob Spedition, Baustofflieferant, Handwerksbetrieb oder Getränkehandel – ein beschrifteter LKW zeigt, wer Sie sind und wie man Sie erreicht.'),
  ('Einheitliche Flotte', 'Transporter in Köln, LKW in Dortmund, Anhänger in Essen: Mit einem gemeinsamen Design erkennt man Ihren Fuhrpark überall.'),
  ('Fahrer gewinnen', 'Ein gut lesbarer Hinweis „Wir stellen ein: Berufskraftfahrer (m/w/d)“ mit Website oder QR-Code erreicht Fahrer genau dort, wo sie unterwegs sind.'),
 ],
 tab_note='Für Transporter und PKW in NRW siehe <a href="/fahrzeugbeschriftung-nrw.html">Fahrzeugbeschriftung NRW</a>. Für Fahrzeuge in Berlin: <a href="/lkw-beschriftung-berlin.html">LKW-Beschriftung Berlin</a>.',
 services=[s_ for s_ in P['services'] if s_[1] not in ('Vollfolierung', 'Flotten')] + [
  ('glas', 'Vollfolierung', 'Fahrerhaus oder ganzes Fahrzeug in neuer Farbe oder mit vollflächigem Motiv.', '/fahrzeugbeschriftung-nrw.html'),
  ('stern', 'Flotten', 'Einheitliches Design für alle Fahrzeuge – Transporter, LKW, Anhänger.', '/fahrzeugbeschriftung-nrw.html')],
 ablauf=[
  ('Fotos & Maße', 'Sie schicken uns Fotos des Fahrzeugs von allen Seiten, die Maße des Aufbaus und Ihr Logo – per WhatsApp oder E-Mail.'),
  ('Entwurf', 'Wir gestalten das Design auf einer Ansicht Ihres Fahrzeugtyps – Sie sehen vorher, wie der LKW aussehen wird.'),
  ('Festpreis & Termin', 'Sie bekommen ein schriftliches Angebot, und wir vereinbaren den Montagetermin bei Ihnen in NRW.'),
  ('Montage vor Ort', 'Unser Team in NRW montiert am vereinbarten Tag auf Ihrem Hof oder in Ihrer Halle.'),
 ],
 faq=[
  ('In welchen Städten in NRW beschriften Sie LKW?', 'Schwerpunkt sind Düsseldorf, Köln, Dortmund, Essen und Bochum, dazu Duisburg, Wuppertal, Bonn und die Städte dazwischen. Unser Team in NRW kommt für die Montage zu Ihnen. Unser Firmensitz ist in Berlin.'),
  ('Kommen Sie zu uns auf den Hof?', 'Ja. Die Montage erfolgt bei Ihnen vor Ort. Wichtig ist ein überdachter, trockener Platz, an dem das Fahrzeug während der Montage stehen kann – zum Beispiel eine Halle.'),
  ('Wie lange steht der LKW still?', 'Das hängt vom Umfang ab. Eine Fahrerhaus-Beschriftung ist deutlich schneller erledigt als eine Vollfolierung. Die Dauer nennen wir im Angebot, damit Sie die Touren planen können.'),
  ('Plane bedrucken oder Folie auf die Plane?', 'Ist die Plane neu oder in gutem Zustand, ist Folie möglich. Bei älteren Planen empfehlen wir eine neue bedruckte Plane – sie hält besser und lässt sich besser öffnen und falten.'),
  ('Machen Sie auch mehrere Fahrzeuge?', 'Ja. Für Flotten entwickeln wir ein einheitliches Design und planen die Termine so, dass nicht alle Fahrzeuge gleichzeitig stehen.'),
  ('Brauchen wir ein fertiges Design?', 'Nein, Ihr Logo reicht. Daraus entwickeln wir das Fahrzeugdesign. Haben Sie schon ein Design, bereiten wir es für die Produktion auf.'),
 ],
 links=[('/fahrzeugbeschriftung-nrw.html', 'Fahrzeugbeschriftung NRW'), ('/werbeagentur-nrw.html', 'Werbeagentur NRW'), ('/werbeagentur-duesseldorf.html', 'Düsseldorf'),
        ('/werbeagentur-koeln.html', 'Köln'), ('/werbeagentur-dortmund.html', 'Dortmund'), ('/werbeagentur-essen.html', 'Essen'), ('/werbeagentur-bochum.html', 'Bochum'),
        ('/blog/fahrzeugbeschriftung-tipps.html', 'Fahrzeugbeschriftung: 7 Tipps')],
 form_sub='Schicken Sie uns Fotos des Fahrzeugs, die Maße des Aufbaus und Ihr Logo – Sie bekommen innerhalb von 24 Stunden ein Angebot. Unser Team in NRW montiert bei Ihnen vor Ort.',
 subject='Anfrage LKW-Beschriftung NRW (Website)', msg_ph='z. B. 3 Sattelzüge mit Curtainsider, Logo auf Fahrerhaus und Plane, Montage auf unserem Hof in Duisburg',
 sticky=('LKW-Beschriftung NRW', 'Team vor Ort, Montage auf Ihrem Hof'))
N['recht_html'] = P['recht_html'].replace('<p><strong>Montage bei Ihnen:</strong> Wir kommen zu Ihnen.', '<p><strong>Montage bei Ihnen:</strong> Unser Team in NRW kommt zu Ihnen.')

def nrw_kontakt(f):
    """NRW: WhatsApp und E-Mail statt Telefon in Navigation und mobilem Menü (wie fahrzeugbeschriftung-nrw)."""
    import re
    h = open(ROOT + f, encoding='utf-8').read()
    wa_nav = ('<a href="https://wa.me/491785143918?text=Hallo%2C%20ich%20m%C3%B6chte%20ein%20Angebot%20f%C3%BCr%20LKW-Beschriftung%20in%20NRW." target="_blank" rel="noopener noreferrer" class="nav-phone" aria-label="Per WhatsApp schreiben">\n'
              '      <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 3a8.5 8.5 0 0 0-7.4 12.7L3 21l5.4-1.5A8.5 8.5 0 1 0 12 3Zm-3 7.2h6a.8.8 0 0 1 0 1.6H9a.8.8 0 0 1 0-1.6Zm0 3h4a.8.8 0 0 1 0 1.6H9a.8.8 0 0 1 0-1.6Z"/></svg>\n      WhatsApp\n    </a>')
    h, n1 = re.subn(r'<a href="tel:01785143918" class="nav-phone".*?</a>', lambda m: wa_nav, h, count=1, flags=re.S)
    h, n2 = re.subn(r'<a href="tel:01785143918" class="mob-call-btn">.*?</a>', lambda m: '<a href="#kontakt" class="mob-call-btn"><svg class="i-inline" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>E-Mail</a>', h, count=1, flags=re.S)
    h = h.replace('placeholder="z. B. Berlin-Mitte"', 'placeholder="z. B. Duisburg"')
    open(ROOT + f, 'w', encoding='utf-8').write(h)
    return n1, n2

if __name__ == '__main__':
    print(build_f(P))
    print(build_f(N), nrw_kontakt(N['file']))
