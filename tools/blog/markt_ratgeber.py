"""Ratgeber aus der Marktrecherche 11/2026 (docs/markt-2026-11/): Themen, bei denen Kunden Geld verlieren und die
Wettbewerber nicht gut beantworten. Baut mit den Funktionen aus werbetechnik_ratgeber.py (gleiche Vorlage, gleiche Eintragung).

Regeln: Preise nur aus CLAUDE.md, Rechtliches nur mit Quelle (Stand 11/2026, „keine Rechtsberatung“), keine Garantien,
keine Lieferzeit-Zusagen außer bei Schildern/Leuchtreklame. Zahlen aus Behörden-/Gerichtsquellen; Kanzlei-Angaben als solche gekennzeichnet.
Aufruf: python3 tools/blog/markt_ratgeber.py
"""
import os, re, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('wr', os.path.join(HERE, 'werbetechnik_ratgeber.py'))
W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
W.DATUM = '2026-11-05'
BASE = W.BASE

ARTIKEL = [
 dict(file='kundenstopper-erlaubnis.html', og=('rollup.webp', 'Ratgeber Gehweg', 'Kundenstopper & Ausleger', 'Erlaubnis in Berlin, Hamburg und NRW'), crumb='Kundenstopper: Erlaubnis',
  title='Kundenstopper: Erlaubnis in Berlin, Hamburg und NRW',
  desc='Kundenstopper oder Ausleger auf dem Gehweg? Wann Sie eine Sondernutzungserlaubnis brauchen, welche Maße in Berlin gelten und warum es in Hamburg schwierig ist.',
  tag='Ratgeber · Gehweg', h1='Kundenstopper aufstellen:<br><em>Was ist erlaubt?</em>', minuten=6,
  bild=('/rollup', 'Werbeaufsteller und Roll-up als Beispiel für Werbung vor dem Geschäft', 'Ein Aufsteller vor der Tür wirbt – auf dem Gehweg braucht er aber meist eine Erlaubnis.'),
  intro='<p>Ein Kundenstopper vor der Tür ist die günstigste Werbung, die ein Laden haben kann. Viele stellen ihn einfach raus – und wundern sich über Post vom Bezirksamt. Denn der Gehweg gehört der Stadt: Wer dort wirbt, nutzt öffentliches Straßenland. Hier die Regeln für Berlin, Hamburg und NRW, Stand November 2026.</p>',
  body='''
    <h2>Warum der Gehweg eine Erlaubnis braucht</h2>
    <p>Gehwege sind für Fußgänger da. Alles, was darüber hinausgeht – Kundenstopper, Warenauslage, Tische oder ein Ausleger, der über den Gehweg ragt – ist eine <strong>Sondernutzung</strong>. Sie braucht eine Erlaubnis der Stadt und kostet meist eine Gebühr. Auf Ihrem eigenen Grundstück, etwa im Hof oder in der Einfahrt, ist es keine Sondernutzung; dort kann aber das Baurecht für Werbeanlagen gelten.</p>

    <h2>Berlin: Antrag beim Bezirksamt</h2>
    <p>In Berlin ist Werbung auf öffentlichem Straßenland eine Sondernutzung nach § 11 Berliner Straßengesetz. Den Antrag stellen Sie beim Bezirksamt, in dem Ihr Geschäft liegt. Laut der Leistungsbeschreibung auf service.berlin.de gilt für Werbeaufsteller:</p>
    <ul>
      <li>nur <strong>während der Öffnungszeiten</strong> und <strong>direkt vor dem eigenen Geschäft</strong>,</li>
      <li>höchstens <strong>1,50 m von der Hauswand</strong> entfernt,</li>
      <li>der Aufsteller darf höchstens <strong>1,20 m hoch und 0,80 m breit</strong> sein,</li>
      <li>Fußgänger dürfen nicht behindert werden.</li>
    </ul>
    <p>Die Verwaltungsgebühr nennt zum Beispiel das Bezirksamt Pankow mit <strong>40 € für ein Jahr und 60 € für zwei Jahre</strong>. Wer ohne Erlaubnis aufstellt, begeht eine Ordnungswidrigkeit – das Bezirksamt Pankow nennt Geldbußen bis 10.000 €. Stellen Sie den Antrag deshalb rechtzeitig vor der Eröffnung.</p>
    <div class="tip-box">
      <p><strong>Tipp:</strong> Fragen Sie beim Antrag gleich nach, ob an Ihrem Standort Besonderheiten gelten – etwa schmale Gehwege, Haltestellen oder Denkmalschutz. Die Auskunft des Bezirksamts ist verbindlich, nicht dieser Artikel.</p>
    </div>

    <h2>Ausleger: oft zwei Erlaubnisse</h2>
    <p>Ein Ausleger oder Nasenschild hängt an der Fassade und ragt über den Gehweg. Damit ist er meist beides: eine <strong>Werbeanlage</strong> nach der Bauordnung und eine <strong>Sondernutzung</strong>, weil er in den öffentlichen Raum ragt. Klären Sie beides, bevor gebaut wird – wir prüfen das bei jedem Angebot mit. Mehr zur Bauordnung: <a href="/blog/aussenwerbung-berlin-ratgeber.html">Außenwerbung in Berlin</a>.</p>

    <h2>Hamburg: Kundenstopper meist nicht erlaubt</h2>
    <p>In Hamburg regelt § 19 des Hamburgischen Wegegesetzes die Sondernutzung. Die Stadt schreibt dazu, dass Kundenstopper <strong>„bis auf wenige Ausnahmen grundsätzlich nicht gestattet“</strong> sind. Laut Merkblatt der Stadt beträgt die Mindestgebühr 35 €; wer ohne Erlaubnis nutzt, zahlt eine um mindestens 100 € erhöhte Gebühr – dazu kann ein Bußgeld kommen.</p>
    <p>Die Alternative für Hamburger Läden: Werbung <strong>im Schaufenster</strong> – etwa eine Folie mit Angebot, Öffnungszeiten oder Logo. Sie braucht keine Sondernutzung. Siehe <a href="/werbeagentur-hamburg.html">Werbeagentur Hamburg</a> und <a href="/blog/werbeanlage-hamburg.html">Werbeanlagen in Hamburg</a>.</p>

    <h2>NRW: Jede Stadt hat eigene Regeln</h2>
    <p>In NRW gilt das Straßen- und Wegegesetz (§§ 18, 19 StrWG NRW). Die Einzelheiten – Maße, Gebühren, Zeiten – stehen in der <strong>Sondernutzungssatzung Ihrer Stadt</strong>, in Köln etwa in der Satzung vom 10.06.2024. Fragen Sie beim Ordnungs- oder Straßenamt Ihrer Stadt nach, bevor Sie aufstellen.</p>

    <h2>Checkliste vor dem Kauf</h2>
    <ul>
      <li><strong>Wo steht er?</strong> Eigenes Grundstück oder öffentlicher Gehweg?</li>
      <li><strong>Erlaubnis:</strong> Antrag gestellt, Maße und Abstand zur Hauswand passend?</li>
      <li><strong>Standfest:</strong> Bei Wind braucht ein Aufsteller Gewicht – etwa einen Wassertank oder einen schweren Fuß.</li>
      <li><strong>Inhalt:</strong> Stehen Preise für Privatkunden darauf, gehört der Gesamtpreis inklusive Mehrwertsteuer dazu (Preisangabenverordnung).</li>
      <li><strong>Wechselbar:</strong> Ein Kundenstopper mit Klemmrahmen lässt sich mit neuen Plakaten immer wieder aktualisieren.</li>
    </ul>
''',
  cta=('Kundenstopper und Plakate aus Berlin', 'Wir drucken Plakate für Kundenstopper, Aufsteller und Schaufenster – und prüfen auf Wunsch, was an Ihrem Standort erlaubt ist.', '/print.html', 'Druck ansehen', 'Hallo, ich brauche einen Kundenstopper bzw. Plakate dafür und habe eine Frage zur Erlaubnis.', 'Druck'),
  weiter=[('/print.html', 'Druckerei Berlin'), ('/schaufensterbeschriftung-berlin.html', 'Schaufensterbeschriftung'), ('/blog/aussenwerbung-berlin-ratgeber.html', 'Genehmigung in Berlin')],
  quellen=[('https://service.berlin.de/dienstleistung/325999/', 'service.berlin.de – Straßensondernutzung für Werbeaufsteller'),
           ('https://www.berlin.de/ba-pankow/sondernutzung', 'Bezirksamt Pankow – Sondernutzung öffentlichen Straßenlandes'),
           ('https://www.hamburg.de/service/info/111073031/n0/', 'hamburg.de – Werbung auf öffentlichen Wegen'),
           ('https://www.hamburg.de/resource/blob/76694/27be0a4bf862276b10f49b9ebf5155e5/merkblatt-sondernutzung-data.pdf', 'Hamburg – Merkblatt Sondernutzung (PDF)'),
           ('https://www.stadt-koeln.de/mediaasset/content/satzungen/sondernutzungssatzung_10_06_2024.pdf', 'Stadt Köln – Sondernutzungssatzung vom 10.06.2024 (PDF)')],
  hinweis=W.HINWEIS_RECHT,
  related=[('/blog/aussenwerbung-berlin-ratgeber.html', 'Außenwerbung Berlin', 'Genehmigung, Kosten und Materialien im Überblick.'),
           ('/blog/werbung-teure-fehler.html', 'Teure Fehler in der Werbung', 'Bilder, Logos, Preise und Abzocke – so vermeiden Sie Ärger.')],
  index=('Gehweg & Genehmigung', 'Kundenstopper: Erlaubnis in Berlin, Hamburg, NRW', 'Maße, Antrag und Gebühr in Berlin, warum Kundenstopper in Hamburg meist nicht erlaubt sind und was in NRW gilt.'),
  llms='Kundenstopper: Erlaubnis in Berlin, Hamburg und NRW'),

 dict(file='leuchtreklame-kosten-berlin.html', og=('konfigurator.webp', 'Ratgeber Leuchtreklame', 'Was kostet Leuchtreklame?', 'Preise, Preistreiber und 7 Prüfpunkte'), crumb='Leuchtreklame: Kosten',
  title='Leuchtreklame Kosten Berlin: Preise & 7 Prüfpunkte',
  desc='Was kostet Leuchtreklame in Berlin? Startpreise, was den Preis bestimmt und 7 Prüfpunkte, bevor Sie günstig online bestellen – von CE bis Genehmigung.',
  tag='Ratgeber · Leuchtreklame', h1='Was kostet<br><em>Leuchtreklame?</em>', minuten=7,
  bild=('/konfigurator', 'Vorschau einer Leuchtreklame bei Tag und Nacht mit Maßangaben', 'Größe und Ausführung bestimmen den Preis – die Vorschau hilft, vorher zu entscheiden.'),
  intro='<p>„Was kostet so eine Leuchtreklame?“ – die häufigste Frage, die wir hören. Die ehrliche Antwort: Es kommt auf Größe, Ausführung und Montage an. Hier sind unsere Startpreise, die wichtigsten Preistreiber und sieben Punkte, die Sie prüfen sollten, bevor Sie ein billiges Angebot aus dem Internet bestellen.</p>',
  body='''
    <h2>Unsere Startpreise</h2>
    <div class="table-wrap"><table class="rt">
      <thead><tr><th>Leistung</th><th>Berlin</th><th>NRW &amp; Hamburg</th></tr></thead>
      <tbody>
        <tr><td data-label="Leistung">Leuchtbuchstaben (je Buchstabe)</td><td data-label="Berlin">ab 199 € netto</td><td data-label="NRW &amp; Hamburg">ab 229 € netto</td></tr>
        <tr><td data-label="Leistung">Einzelbuchstaben unbeleuchtet (je Buchstabe)</td><td data-label="Berlin">ab 119 € netto</td><td data-label="NRW &amp; Hamburg">ab 139 € netto</td></tr>
        <tr><td data-label="Leistung">LED-Neon für innen</td><td data-label="Berlin">ab 249 € netto</td><td data-label="NRW &amp; Hamburg">ab 249 € netto</td></tr>
        <tr><td data-label="Leistung">Firmenschild (Alu-Dibond)</td><td data-label="Berlin">ab 149 € netto</td><td data-label="NRW &amp; Hamburg">ab 179 € netto</td></tr>
      </tbody>
    </table></div>
    <p>Das sind Startpreise für einfache Ausführungen. Den genauen Preis nennen wir Ihnen als Festpreis, nachdem wir Fotos und Maße gesehen haben.</p>

    <h2>Was den Preis bestimmt</h2>
    <ul>
      <li><strong>Zahl und Höhe der Buchstaben:</strong> Jeder Buchstabe wird einzeln gebaut. Mehr und größere Buchstaben kosten mehr.</li>
      <li><strong>Ausführung:</strong> frontleuchtend, rückleuchtend (Halo) oder unbeleuchtet – und das Material der Front und der Seiten.</li>
      <li><strong>Montage:</strong> In welcher Höhe hängt die Anlage? Braucht es eine Hubarbeitsbühne oder ein Gerüst?</li>
      <li><strong>Strom:</strong> Gibt es einen Anschluss in der Nähe? Den Anschluss übernimmt ein eingetragener Elektrofachbetrieb.</li>
      <li><strong>Genehmigung:</strong> Größere Anlagen brauchen eine Genehmigung – dafür fallen Gebühren beim Amt an.</li>
      <li><strong>Gestaltung:</strong> Liegt Ihr Logo als Vektordatei vor, oder muss es erst aufbereitet werden?</li>
    </ul>
    <div class="tip-box">
      <p><strong>Rechenbeispiel (nur Startpreise):</strong> Ein Schriftzug mit 8 Leuchtbuchstaben beginnt in Berlin bei 8 × 199 € = 1.592 € netto. Wie groß die Buchstaben sein sollten und wie es an Ihrer Fassade wirkt, sehen Sie im <a href="/leuchtbuchstaben-konfigurator.html">Leuchtbuchstaben-Konfigurator</a>.</p>
    </div>

    <h2>Billig online bestellen? 7 Prüfpunkte</h2>
    <p>Im Internet gibt es Leuchtreklame zu sehr niedrigen Preisen, oft direkt aus Fernost. Das kann gut gehen – oft fehlt aber genau das, was später teuer wird. Behörden in Großbritannien und Australien haben bereits LED-Werbeschilder und Netzteile wegen Brand- und Stromschlaggefahr beanstandet. Prüfen Sie vor dem Kauf:</p>
    <ol>
      <li><strong>CE-Kennzeichnung und Hersteller:</strong> Gibt es einen verantwortlichen Hersteller oder Importeur in der EU, eine Bedienungsanleitung auf Deutsch und Angaben zum Netzteil?</li>
      <li><strong>Für außen geeignet?</strong> Außen braucht die Technik Schutz gegen Regen und Feuchtigkeit – fragen Sie nach der Schutzart von Leuchtmitteln und Netzteil.</li>
      <li><strong>Netzteil und Ersatzteile:</strong> Netzteile sind die häufigste Schwachstelle. Lässt es sich später einfach tauschen – und bekommen Sie Ersatz?</li>
      <li><strong>Genehmigung:</strong> Der Händler im Ausland kümmert sich nicht darum. Ohne nötige Genehmigung kann das Amt den Abbau auf Ihre Kosten anordnen.</li>
      <li><strong>Montage:</strong> Wer montiert, und wer haftet, wenn sich etwas löst? Für Schäden durch herabfallende Schilder kann der Betreiber haften.</li>
      <li><strong>Elektroanschluss:</strong> Der feste Anschluss gehört in die Hände einer Elektrofachkraft.</li>
      <li><strong>Ansprechpartner und Gewährleistung:</strong> Wen erreichen Sie, wenn etwas ausfällt? In Deutschland gilt die gesetzliche Gewährleistung – das hilft nur, wenn der Verkäufer erreichbar ist.</li>
    </ol>
    <p>Bei uns kommt alles aus einer Hand: Entwurf und Genehmigung von uns, Bau und Montage durch in die Handwerksrolle eingetragene Partnerbetriebe, der Anschluss durch einen Elektrofachbetrieb – mit einem Ansprechpartner in Berlin.</p>

    <h2>Laufende Kosten</h2>
    <p>LED-Anlagen brauchen wenig Strom, die Betriebsstunden sind der größte Hebel. Wie Sie den Verbrauch selbst ausrechnen und was Zeitschaltuhr und Dämmerungsschalter bringen, steht im Ratgeber <a href="/blog/leuchtreklame-strom-betriebszeiten.html">Leuchtreklame: Strom und Schaltzeiten</a>.</p>
''',
  cta=('Festpreis für Ihre Leuchtreklame', 'Schicken Sie uns ein Foto Ihrer Fassade und den gewünschten Schriftzug – Sie bekommen ein Festpreis-Angebot, in der Regel innerhalb von 24 Stunden.', '/leuchtreklame-berlin.html', 'Leuchtreklame Berlin', 'Hallo, ich möchte wissen, was eine Leuchtreklame für mein Geschäft kostet. Ich schicke ein Foto der Fassade.', 'Leuchtreklame'),
  weiter=[('/leuchtreklame-berlin.html', 'Leuchtreklame Berlin'), ('/leuchtreklame-nrw.html', 'Leuchtreklame NRW'), ('/leuchtbuchstaben-konfigurator.html', 'Konfigurator')],
  quellen=[('https://www.gov.uk/product-safety-alerts-reports-recalls/product-safety-report-led-vape-shop-sign-2312-0076', 'UK Office for Product Safety and Standards – Product Safety Report LED Shop Sign'),
           ('https://www.productsafety.gov.au/node/21234', 'ACCC Product Safety Australia – Rückruf Netzteile für LED-Neon'),
           ('https://www.ra-kotz.de/fahrzeugbeschaedigung-durch-herabfallendes-werbeschild-schadensersatzansprueche.htm', 'Kanzlei Kotz – Haftung bei herabfallendem Werbeschild (LG Meiningen)')],
  hinweis='Hinweis: Preise sind Startpreise der Masar Werbeagentur (netto zzgl. 19 % MwSt.). Rechtliche Hinweise sind allgemein und keine Rechtsberatung.',
  related=[('/blog/leuchtreklame-strom-betriebszeiten.html', 'Leuchtreklame: Strom & Schaltzeiten', 'Verbrauch ausrechnen und Nachbarn schonen.'),
           ('/blog/aussenwerbung-berlin-ratgeber.html', 'Außenwerbung Berlin', 'Genehmigung, Kosten und Materialien im Überblick.')],
  index=('Leuchtreklame', 'Leuchtreklame Kosten Berlin: Preise & 7 Prüfpunkte', 'Startpreise, was den Preis bestimmt und worauf Sie achten sollten, bevor Sie günstig online bestellen.'),
  llms='Leuchtreklame Kosten Berlin: Preise & 7 Prüfpunkte'),

 dict(file='werbung-teure-fehler.html', og=('grafikdesign.webp', 'Ratgeber Recht', 'Teure Fehler in der Werbung', 'Bilder, Logos, Preise und Abzocke'), crumb='Teure Fehler in der Werbung',
  title='Teure Fehler in der Werbung: Bilder, Logos, Preise',
  desc='Bilderklau, fremde Marken, falsche Preisangaben, Branchenbuch-Fallen: die häufigsten teuren Fehler kleiner Betriebe in der Werbung – und wie Sie sie vermeiden.',
  tag='Ratgeber · Recht', h1='Teure Fehler<br><em>in der Werbung.</em>', minuten=7,
  bild=('/grafikdesign', 'Gestaltung von Logo und Werbemitteln am Bildschirm', 'Die meisten teuren Fehler passieren, bevor gedruckt wird.'),
  intro='<p>Ein Flyer mit einem Foto aus dem Internet, ein Logo, das einer bekannten Marke ähnelt, ein Preisschild ohne Mehrwertsteuer: Solche Kleinigkeiten führen bei kleinen Betrieben immer wieder zu Abmahnungen – und die kosten schnell mehr als die ganze Werbung. Hier die häufigsten Fallen und wie Sie sie vermeiden.</p>',
  body='''
    <h2>1. Fotos ohne Lizenz</h2>
    <p>Ein Bild aus der Google-Suche ist nicht frei. Wer fremde Fotos ohne Erlaubnis auf Website, Flyer oder Fahrzeug nutzt, verletzt das Urheberrecht (§ 97 UrhG). Laut Fachkanzleien verlangen Rechteinhaber oft Lizenzgebühr, Anwaltskosten und eine Unterlassungserklärung – Gerichte setzen für einfache Fotos zwar teils deutlich weniger an, der Ärger bleibt aber.</p>
    <ul>
      <li>Eigene Fotos nutzen oder Bilder mit klarer Lizenz (Lizenznachweis aufheben).</li>
      <li>Auf Stockbild-Plattformen die Bedingungen lesen – manche verlangen die Nennung des Fotografen.</li>
      <li>Bei KI-Bildern die Nutzungsbedingungen des Dienstes prüfen.</li>
    </ul>

    <h2>2. Name oder Logo ähnelt einer Marke</h2>
    <p>Ein neuer Firmenname oder ein Logo kann eine eingetragene Marke verletzen – dann müssen Schild, Fahrzeugbeschriftung und Website im schlimmsten Fall neu. Laut Fachkanzleien liegen die Anwaltskosten einer Markenabmahnung häufig im vierstelligen Bereich. Prüfen Sie deshalb vor Logo und Schild die Register beim <a href="https://register.dpma.de/" target="_blank" rel="noopener noreferrer">Deutschen Patent- und Markenamt</a> und beim EUIPO. Auch fremde Logos – etwa von Getränkemarken – gehören nur mit Erlaubnis auf Ihre Werbung.</p>

    <h2>3. Preise ohne Mehrwertsteuer</h2>
    <p>Wer Privatkunden Preise nennt – im Schaufenster, auf dem Aufsteller oder der Website –, muss den <strong>Gesamtpreis inklusive Mehrwertsteuer</strong> angeben (§ 3 Preisangabenverordnung). Ein Nettopreis mit „zzgl. MwSt.“ reicht gegenüber Verbrauchern nicht. Verstöße sind Ordnungswidrigkeiten und werden häufig von Mitbewerbern abgemahnt.</p>

    <h2>4. „Testsieger“, Siegel und Garantien</h2>
    <p>Wer mit einem Testergebnis wirbt, muss angeben, wo der Test zu finden ist – sonst ist die Werbung irreführend (BGH, I ZR 134/20). Wer mit einer Garantie wirbt, muss deren Bedingungen klar nennen (§ 479 BGB). Im Zweifel lieber sachlich beschreiben, was Sie tun.</p>

    <h2>5. Branchenbuch- und Formularfallen</h2>
    <p>„Bitte prüfen Sie Ihren Eintrag“ – solche Schreiben sehen aus wie Behördenpost oder kostenlose Aktualisierungen. Wer unterschreibt, schließt oft einen teuren Vertrag über mehrere Jahre ab. Die IHKs warnen regelmäßig davor und nennen Beträge von mehreren hundert bis über tausend Euro im Jahr. Lesen Sie das Kleingedruckte und unterschreiben Sie nichts, was Sie nicht bestellt haben.</p>

    <h2>6. Werbe-E-Mails ohne Einwilligung</h2>
    <p>Werbung per E-Mail braucht die vorherige ausdrückliche Einwilligung des Empfängers – auch gegenüber anderen Firmen (§ 7 UWG). Für neue Kunden sind Briefe per Post, gute Schaufenster und eine sichtbare Website die sichere Wahl.</p>

    <h2>7. Kein oder falsches Impressum</h2>
    <p>Geschäftliche Websites und Social-Media-Profile brauchen ein Impressum (§ 5 Digitale-Dienste-Gesetz). Ein fehlendes Impressum ist einer der häufigsten Abmahngründe.</p>

    <div class="tip-box">
      <p><strong>So helfen wir:</strong> Wir gestalten Logos, Flyer und Schilder mit eigenen oder lizenzierten Bildern, achten auf Preisangaben auf Ihren Werbemitteln und prüfen Ihre Druckdaten kostenlos mit dem <a href="/druckdaten-check.html">Druckdaten-Check</a>. Die rechtliche Prüfung im Einzelfall übernimmt Ihr Anwalt oder Ihre Kammer.</p>
    </div>
''',
  cta=('Werbung ohne Ärger', 'Logo, Flyer, Schild oder Website – wir gestalten mit eigenen oder lizenzierten Bildern und klaren Preisangaben.', '/grafikdesign-berlin.html', 'Grafikdesign ansehen', 'Hallo, ich möchte Werbung gestalten lassen und habe eine Frage zu Bildern bzw. Logo.', 'Grafikdesign'),
  weiter=[('/grafikdesign-berlin.html', 'Grafikdesign'), ('/webdesign-berlin.html', 'Webdesign'), ('/druckdaten-check.html', 'Druckdaten-Check')],
  quellen=[('https://www.gesetze-im-internet.de/urhg/__97.html', '§ 97 UrhG – Anspruch auf Unterlassung und Schadensersatz'),
           ('https://www.gesetze-im-internet.de/pangv_2022/__3.html', '§ 3 PAngV – Pflicht zur Angabe des Gesamtpreises'),
           ('https://www.gesetze-im-internet.de/uwg_2004/__7.html', '§ 7 UWG – Unzumutbare Belästigungen'),
           ('https://www.gesetze-im-internet.de/bgb/__479.html', '§ 479 BGB – Sonderbestimmungen für Garantien'),
           ('https://www.gesetze-im-internet.de/ddg/__5.html', '§ 5 DDG – Allgemeine Informationspflichten'),
           ('https://www.ihk.de/pfalz/recht/wettbewerb/adressbuchschwindel-1274004', 'IHK Pfalz – Adressbuchschwindel'),
           ('https://www.it-recht-kanzlei.de/markenabmahnungen-kosten-teuer.html', 'IT-Recht Kanzlei – Kosten von Markenabmahnungen')],
  hinweis=W.HINWEIS_RECHT,
  related=[('/blog/logo-dateien-werbetechnik.html', 'Logo-Dateien', 'Welche Datei Werkstatt und Druckerei brauchen.'),
           ('/blog/kundenstopper-erlaubnis.html', 'Kundenstopper: Erlaubnis', 'Was auf dem Gehweg erlaubt ist.')],
  index=('Recht', 'Teure Fehler in der Werbung: Bilder, Logos, Preise', 'Bilderklau, fremde Marken, Preisangaben, Branchenbuch-Fallen, Werbe-E-Mails und Impressum – und wie Sie sie vermeiden.'),
  llms='Teure Fehler in der Werbung: Bilder, Logos, Preise'),
]


def llms():
    p = os.path.join(W.ROOT, 'llms.txt'); s = open(p, encoding='utf-8').read()
    neu = [a for a in ARTIKEL if f'blog/{a["file"]})' not in s]
    if not neu: return
    m = re.search(r'^- Ratgeber Werbetechnik: .*$', s, re.M)
    zus = ', '.join(f'[{a["llms"]}]({BASE}blog/{a["file"]})' for a in neu)
    s = s[:m.end()] + ', ' + zus + s[m.end():] if m else s.rstrip('\n') + '\n- Ratgeber: ' + zus + '\n'
    open(p, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    vorlage = open(W.VORLAGE_DATEI, encoding='utf-8').read()
    for a in ARTIKEL:
        print(W.bauen(a, vorlage))
    W.ARTIKEL = ARTIKEL
    W.eintragen()
    llms()
    print('Blog-Übersicht, Sitemap und llms.txt geprüft')
