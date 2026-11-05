"""Ratgeber Werbetechnik (04.11.2026): Themen, zu denen Wettbewerber ranken und wir noch keine Seite hatten
(siehe docs/wettbewerb-2026-11.md). Vorlage: blog/fotowand-firmenfeier.html (wie tools/blog/ki_artikel.py).

Regeln: Preise nur aus CLAUDE.md, keine erfundenen Zahlen (Rechenbeispiele sind als Annahme gekennzeichnet),
Rechtliches nur mit Quelle, kein „rechtssicher“, keine Lieferzeit-Zusagen außer bei Schildern/Leuchtreklame.

Aufruf: python3 tools/blog/werbetechnik_ratgeber.py
Erzeugt die Artikel und trägt sie (idempotent) in blog/index.html, sitemap.xml und llms.txt ein.
Vorschaubilder einmalig: python3 tools/og/og_cards.py add blog/<datei> <og[0]> "<og[1]>" "<og[2]>" "<og[3]>"
(Werte im Feld og je Artikel); bei erneutem Aufruf bleibt die Karte erhalten.
Danach: blog_kurzbox.py → schnell.py → a11y.py → marke.py → umbruch.py (siehe tools/README.md).
"""
import os, re, json
from urllib.parse import quote

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
BASE = 'https://masar-werbeagentur.de/'
DATUM = '2026-11-04'
WA = 'https://wa.me/491785143918?text='

HINWEIS_RECHT = 'Hinweis: Dieser Artikel gibt einen allgemeinen Überblick und ist keine Rechtsberatung. Verbindlich ist die Auskunft der zuständigen Behörde.'
HINWEIS_PRAXIS = 'Hinweis: Allgemeine Hinweise aus der Praxis. Maßgeblich sind die Angaben des jeweiligen Herstellers zu Material und Pflege.'

# ---------------------------------------------------------------------------
ARTIKEL = [
 dict(file='leuchtreklame-strom-betriebszeiten.html', og=('leuchtreklamen.webp', 'Ratgeber Leuchtreklame', 'Strom, Schaltzeiten, Nachbarn', 'Verbrauch ausrechnen, Zeitschaltuhr und was bei Licht gilt'), crumb='Leuchtreklame Strom & Betriebszeiten',
  title='Leuchtreklame: Stromkosten, Schaltzeiten, Nachbarn',
  desc='Was eine LED-Leuchtreklame im Betrieb verbraucht, wie Zeitschaltuhr und Dämmerungsschalter helfen und was bei Licht in der Nachbarschaft rechtlich gilt.',
  tag='Ratgeber · Leuchtreklame', h1='Leuchtreklame im Betrieb:<br><em>Strom, Schaltzeiten, Nachbarn.</em>', minuten=6,
  bild=('/leuchtreklamen', 'Grafik mit mehreren leuchtenden Schildern in Neon-Optik und dem Schriftzug Leuchtreklame', 'Leuchtreklame wirkt vor allem in der Dämmerung – und genau dann lohnt sich eine gute Steuerung.'),
  intro='<p>Die Anlage hängt, das Licht ist an – und dann kommen die Fragen: Was kostet der Strom? Muss die Reklame nachts aus? Und was, wenn sich die Nachbarn über das Licht beschweren? Hier die Antworten, die wir in Beratungen am häufigsten geben – mit Rechenweg und den Regeln, die tatsächlich gelten.</p>',
  body='''
    <h2>So rechnen Sie den Stromverbrauch aus</h2>
    <p>Die Leistung Ihrer Anlage steht im Datenblatt der LED-Module oder auf dem Netzteil, angegeben in Watt. Damit ist die Rechnung einfach:</p>
    <ul>
      <li><strong>Leistung (Watt) × Betriebsstunden ÷ 1.000 = Verbrauch in kWh</strong></li>
      <li><strong>Verbrauch in kWh × Ihr Strompreis = Kosten</strong></li>
    </ul>
    <p>Kennen Sie nur die Leistung des Netzteils, rechnen Sie damit: Das Netzteil ist auf die Anlage ausgelegt, die tatsächliche Aufnahme liegt meist darunter. Genau messen kann es Ihr Elektriker.</p>
    <div class="tip-box">
      <p><strong>Rechenbeispiel (nur Annahmen):</strong> Eine Anlage mit 100&nbsp;Watt leuchtet jeden Abend 6&nbsp;Stunden. Das sind 100 × 6 ÷ 1.000 = 0,6&nbsp;kWh am Tag und rund 219&nbsp;kWh im Jahr. Bei angenommenen 0,30&nbsp;€ je kWh wären das etwa 66&nbsp;€ im Jahr. Setzen Sie die Werte Ihrer Anlage und Ihren Stromtarif ein.</p>
    </div>
    <p>Der größte Hebel sind die <strong>Betriebsstunden</strong>, nicht die Technik: Eine Anlage, die nur von der Dämmerung bis Ladenschluss leuchtet, braucht einen Bruchteil dessen, was dieselbe Anlage rund um die Uhr verbraucht.</p>

    <h2>Zeitschaltuhr, Dämmerungsschalter, Dimmen</h2>
    <ul>
      <li><strong>Dämmerungsschalter:</strong> schaltet ein, wenn es dunkel wird. Damit leuchtet die Reklame nicht unnötig bei Tageslicht, wo sie ohnehin kaum wirkt.</li>
      <li><strong>Zeitschaltuhr:</strong> schaltet zu einer festen Uhrzeit aus, etwa nach Ladenschluss oder zu einer Nachtzeit, die Sie festlegen.</li>
      <li><strong>Astro-Zeitschaltuhr:</strong> verbindet beides – sie kennt die Sonnenauf- und -untergangszeiten für Ihren Ort und braucht keinen Lichtsensor.</li>
      <li><strong>Dimmen:</strong> Viele LED-Anlagen lassen sich dimmen. Das spart Strom und ist die einfachste Lösung, wenn die Reklame in einer Wohnstraße zu hell wirkt.</li>
    </ul>
    <p>Weniger Betriebsstunden schonen außerdem Netzteil und LEDs. Planen Sie die Steuerung deshalb gleich mit ein – nachträglich ist sie meist aufwendiger.</p>

    <h2>Muss die Reklame nachts aus?</h2>
    <p>Eine allgemeine, bundesweite Abschaltpflicht für Leuchtreklame gibt es derzeit nicht. Viele erinnern sich an die Energiesparverordnung (EnSikuMaV): Von September 2022 bis April 2023 mussten beleuchtete Werbeanlagen von 22 bis 6 Uhr ausgeschaltet sein – mit Ausnahmen, etwa für Hinweise auf das eigene Geschäft während der Öffnungszeit. Diese Regel ist ausgelaufen.</p>
    <p>Im Bundesnaturschutzgesetz steht seit 2021 eine Vorschrift zum Schutz von Insekten vor Beleuchtung (§&nbsp;41a BNatSchG), die auch neue Werbeanlagen betrifft. Sie gilt aber erst, wenn die dazugehörige Rechtsverordnung erlassen ist – das ist nach unserem Stand (November 2026) noch nicht geschehen.</p>
    <p>Betriebszeiten können trotzdem vorgeschrieben sein: als <strong>Auflage in der Baugenehmigung</strong>, durch eine örtliche Gestaltungssatzung oder in Schutzgebieten. Was für Ihre Anlage gilt, steht im Bescheid – lesen Sie ihn genau.</p>

    <h2>Licht und Nachbarn</h2>
    <p>Licht zählt nach dem Bundes-Immissionsschutzgesetz zu den Immissionen (§&nbsp;3 Abs.&nbsp;2 BImSchG). Wer eine Anlage betreibt, muss vermeidbare schädliche Umwelteinwirkungen verhindern (§&nbsp;22 BImSchG). Ob Licht erheblich stört, beurteilen Behörden in der Regel nach den <strong>Hinweisen der Bund/Länder-Arbeitsgemeinschaft Immissionsschutz (LAI)</strong>: Sie unterscheiden die Aufhellung von Wohnräumen und die Blendung – je nach Art des Gebiets und mit strengeren Werten in der Nacht. Zivilrechtlich können sich Nachbarn auf §&nbsp;906 BGB berufen, wenn die Beeinträchtigung wesentlich ist.</p>
    <p>In der Praxis lassen sich die meisten Konflikte schon bei der Planung vermeiden:</p>
    <ul>
      <li>Die Reklame zur Straße ausrichten, nicht auf Fenster gegenüber oder darüber.</li>
      <li>Hinterleuchtete Buchstaben wirken weicher als ein heller Leuchtkasten.</li>
      <li>In Wohnstraßen auf Lauf- und Blinkeffekte verzichten.</li>
      <li>Dimmbar planen und nachts früher abschalten.</li>
      <li>In der Nähe von Ampeln keine roten oder grünen Dauerlichter, die verwechselt werden können.</li>
    </ul>

    <h2>Checkliste für den Betrieb</h2>
    <ol>
      <li>Leistung der Anlage aus dem Datenblatt notieren und die Kosten einmal durchrechnen.</li>
      <li>Betriebszeit festlegen, zum Beispiel von der Dämmerung bis Ladenschluss.</li>
      <li>Dämmerungsschalter oder Astro-Zeitschaltuhr gleich mit einbauen lassen.</li>
      <li>Bei Wohnnachbarn: Helligkeit prüfen und die Anlage dimmbar planen.</li>
      <li>Auflagen aus der Genehmigung (Betriebszeiten, Helligkeit) beachten.</li>
      <li>Einmal im Jahr Gehäuse reinigen und auf Dichtigkeit prüfen lassen.</li>
    </ol>''',
  cta=('Leuchtreklame aus Berlin', 'Wir planen Ihre Leuchtreklame mit Steuerung und passender Helligkeit – in Berlin und mit unserem Team in NRW und Hamburg. Festpreis nach Fotos.', '/leuchtreklame-berlin.html', 'Leuchtreklame ansehen', 'Hallo, ich plane eine Leuchtreklame und habe eine Frage zu Strom und Schaltzeiten.', 'Leuchtreklame'),
  weiter=[('/leuchtreklame-berlin.html', 'Leuchtreklame Berlin'), ('/leuchtreklame-nrw.html', 'Leuchtreklame NRW'), ('/blog/aussenwerbung-berlin-ratgeber.html', 'Genehmigung in Berlin')],
  quellen=[('https://www.gesetze-im-internet.de/bimschg/__3.html', '§ 3 BImSchG – Begriffsbestimmungen (Licht als Immission)'),
           ('https://www.gesetze-im-internet.de/bimschg/__22.html', '§ 22 BImSchG – Pflichten der Betreiber nicht genehmigungsbedürftiger Anlagen'),
           ('https://www.lai-immissionsschutz.de/documents/lichthinweise-2015-11-03mit-formelkorrektur_aus_03_2018_1520588339.pdf', 'LAI – Hinweise zur Messung, Beurteilung und Minderung von Lichtimmissionen'),
           ('https://www.gesetze-im-internet.de/bnatschg_2009/__41a.html', '§ 41a BNatSchG – Schutz vor nachteiligen Auswirkungen von Beleuchtungen'),
           ('https://www.buzer.de/11_EnSikuMaV.htm', '§ 11 EnSikuMaV (bis 15.04.2023) – Beleuchtung von Werbeanlagen'),
           ('https://www.gesetze-im-internet.de/bgb/__906.html', '§ 906 BGB – Zuführung unwägbarer Stoffe')],
  hinweis=HINWEIS_RECHT,
  related=[('/blog/werbetechnik-trends-2026.html', 'LED, Neon oder Folie?', 'Was sich für Ladenlokale wirklich rechnet.'),
           ('/blog/aussenwerbung-berlin-ratgeber.html', 'Außenwerbung Berlin', 'Genehmigung, Kosten und Materialien im Überblick.')],
  index=('Leuchtreklame', 'Leuchtreklame: Strom, Schaltzeiten, Nachbarn', 'Verbrauch selbst ausrechnen, Zeitschaltuhr und Dämmerungsschalter, Abschaltpflicht und Licht in der Nachbarschaft.'),
  llms='Leuchtreklame: Stromkosten, Schaltzeiten, Nachbarn'),

 dict(file='werbung-autoscheiben-erlaubt.html', og=('fahrzeug.webp', 'Ratgeber Fahrzeug', 'Werbung auf Autoscheiben', 'Was am Firmenwagen erlaubt ist'), crumb='Werbung auf Autoscheiben',
  title='Werbung auf Autoscheiben: Was ist erlaubt?',
  desc='Heckscheibe, Seitenscheiben, Frontscheibe: Wo Lochfolie und Schriftzüge am Firmenwagen erlaubt sind und was Bauartgenehmigung und Außenspiegel damit zu tun haben.',
  tag='Ratgeber · Fahrzeug', h1='Werbung auf Autoscheiben:<br><em>Was erlaubt ist.</em>', minuten=5,
  bild=('/fahrzeug', 'Grafik eines weißen Transporters mit Logo-Beschriftung an Seite und Front', 'Die Karosserie ist die beste Werbefläche – bei den Scheiben gelten eigene Regeln.'),
  intro='<p>Die Telefonnummer groß auf der Heckscheibe, das Logo auf der Seitenscheibe: Viele Betriebe möchten die Glasflächen ihres Firmenwagens mitnutzen. Das geht – aber nicht überall. Scheiben gehören zur Verkehrssicherheit, und dafür gibt es klare Regeln.</p>',
  body='''
    <h2>Die Grundregel: Der Fahrer muss genug sehen</h2>
    <p>Wer ein Fahrzeug führt, ist dafür verantwortlich, dass seine Sicht nicht beeinträchtigt wird (§&nbsp;23 Abs.&nbsp;1 StVO). Das Fahrzeug selbst muss dem Fahrer ein ausreichendes Sichtfeld bieten – bei jedem Wetter (§&nbsp;35b Abs.&nbsp;2 StVZO). Alles, was auf Scheiben geklebt wird, muss sich daran messen lassen.</p>

    <h2>Frontscheibe und vordere Seitenscheiben: keine Werbung</h2>
    <p>Auf die Frontscheibe und die Scheiben von Fahrer- und Beifahrertür gehört keine Werbefolie. Dort braucht der Fahrer freie Sicht nach vorn und zur Seite, auch auf die Außenspiegel. Erlaubt ist nur, was vorgeschrieben oder ausdrücklich zugelassen ist – etwa Plaketten.</p>

    <h2>Heckscheibe und hintere Seitenscheiben</h2>
    <p>Hier ist Werbung möglich, meist mit <strong>Lochfolie</strong> (One-Way-Vision): Von außen sieht man das Motiv, von innen schaut man durch die Löcher hindurch. Zwei Voraussetzungen sind wichtig:</p>
    <ul>
      <li><strong>Zugelassene Folie:</strong> Folien für Fahrzeugscheiben brauchen eine Allgemeine Bauartgenehmigung des Kraftfahrt-Bundesamts (§&nbsp;22a StVZO). Achten Sie auf das Prüfzeichen und fragen Sie, ob der Nachweis im Fahrzeug mitgeführt werden muss – das steht häufig in der Genehmigung.</li>
      <li><strong>Zwei Außenspiegel:</strong> Ist die Sicht nach hinten durch die Heckscheibe eingeschränkt, braucht das Fahrzeug Außenspiegel auf beiden Seiten (§&nbsp;56 StVZO). Bei Transportern ist das ohnehin Standard, bei Pkw prüfen.</li>
    </ul>
    <p>Gut zu wissen: Bei Dunkelheit und Regen sieht man durch Lochfolie schlechter als durch klares Glas. Für Fahrzeuge, die viel im Dunkeln rückwärts rangieren, ist eine Rückfahrkamera eine sinnvolle Ergänzung.</p>

    <h2>Was immer frei bleibt</h2>
    <ul>
      <li>Kennzeichen, Leuchten, Blinker und Rückstrahler – nichts davon wird überklebt.</li>
      <li>Der Wischbereich der Heckscheibe, wenn dort klare Sicht nötig ist.</li>
      <li>Hinweise und Plaketten, die vorgeschrieben sind.</li>
    </ul>

    <h2>Oft die bessere Lösung: die Karosserie</h2>
    <p>Telefonnummer und Website wirken auf der lackierten Heckklappe oder unter der Scheibe genauso gut – ohne Zulassungsfragen und ohne Einschränkung der Sicht. Auf der Scheibe lohnt sich Werbung vor allem, wenn das Heck sonst kaum Fläche bietet, etwa beim Kombi mit großer Heckscheibe.</p>
    <div class="tip-box">
      <p><strong>Tipp:</strong> Kontrast schlägt Größe. Weiße Schrift auf dunkler Lochfolie oder dunkle Schrift auf hellem Lack – Hauptsache, die Nummer ist im Vorbeifahren lesbar.</p>
    </div>

    <h2>Checkliste</h2>
    <ol>
      <li>Front und vordere Seitenscheiben frei lassen.</li>
      <li>Für Heck und hintere Seitenscheiben Lochfolie mit Bauartgenehmigung wählen.</li>
      <li>Zwei Außenspiegel prüfen, bei Bedarf Rückfahrkamera.</li>
      <li>Kennzeichen, Leuchten und Plaketten frei lassen.</li>
      <li>Bei Leasing: Rückgabebedingungen vorher lesen.</li>
      <li>Im Zweifel bei einer Prüforganisation oder der Zulassungsstelle nachfragen.</li>
    </ol>''',
  cta=('Fahrzeugbeschriftung aus Berlin', 'Wir planen Ihre Beschriftung so, dass sie wirkt und zugelassen bleibt – Festpreis nach Fotos, Montage in Berlin und mit unserem Team in NRW.', '/fahrzeugbeschriftung-berlin.html', 'Fahrzeugbeschriftung ansehen', 'Hallo, ich möchte unseren Firmenwagen beschriften lassen, auch die Heckscheibe.', 'Fahrzeugbeschriftung'),
  weiter=[('/fahrzeugbeschriftung-berlin.html', 'Fahrzeugbeschriftung Berlin'), ('/fahrzeugbeschriftung-nrw.html', 'Fahrzeugbeschriftung NRW'), ('/lkw-beschriftung-berlin.html', 'LKW-Beschriftung')],
  quellen=[('https://www.gesetze-im-internet.de/stvo_2013/__23.html', '§ 23 StVO – Sonstige Pflichten von Fahrzeugführenden'),
           ('https://www.gesetze-im-internet.de/stvzo_2012/__35b.html', '§ 35b StVZO – Einrichtungen zum sicheren Führen der Fahrzeuge'),
           ('https://www.gesetze-im-internet.de/stvzo_2012/__22a.html', '§ 22a StVZO – Bauartgenehmigung für Fahrzeugteile'),
           ('https://www.gesetze-im-internet.de/stvzo_2012/__56.html', '§ 56 StVZO – Spiegel und andere Einrichtungen für indirekte Sicht')],
  hinweis=HINWEIS_RECHT + ' Für Ihr Fahrzeug fragen Sie im Zweifel eine Prüforganisation (z.&nbsp;B. TÜV, DEKRA) oder die Zulassungsstelle.',
  related=[('/blog/fahrzeugbeschriftung-tipps.html', 'Fahrzeugbeschriftung: 7 Tipps', 'Folie, Schriftgröße und Montage.'),
           ('/blog/leasingrueckgabe-fahrzeugbeschriftung-entfernen.html', 'Leasingrückgabe', 'Fahrzeugbeschriftung lackschonend entfernen.')],
  index=('Fahrzeug', 'Werbung auf Autoscheiben: Was ist erlaubt?', 'Heckscheibe, Seitenscheiben, Front: Lochfolie, Bauartgenehmigung und Außenspiegel am Firmenwagen.'),
  llms='Werbung auf Autoscheiben: Was ist erlaubt?'),

 dict(file='bauzaunbanner-ratgeber.html', og=('pvc-banner.webp', 'Ratgeber Banner', 'Bauzaunbanner', 'Material, Befestigung, Genehmigung'), crumb='Bauzaunbanner',
  title='Bauzaunbanner: Material, Befestigung, Genehmigung',
  desc='Bauzaunbanner richtig planen: Mesh oder PVC, Ösen, Kabelbinder oder Spanngummi, Wind, Brandschutz – und wann Werbung am Bauzaun eine Genehmigung braucht.',
  tag='Ratgeber · Banner', h1='Bauzaunbanner:<br><em>Material, Befestigung, Genehmigung.</em>', minuten=6,
  bild=('/pvc-banner', 'Grafik zweier PVC-Banner, eines mit Metallösen und eines ohne Ösen', 'Ösen oder Saum: Die Befestigung entscheidet mit, wie lange ein Banner am Zaun hält.'),
  intro='<p>Ein Banner am Bauzaun ist die günstigste große Werbefläche, die es gibt: für die Baufirma, den Bauträger, das neue Geschäft, das hier bald eröffnet. Damit es auch nach dem ersten Sturm noch gerade hängt – und keinen Ärger mit dem Amt gibt –, kommt es auf ein paar Punkte an.</p>',
  body='''
    <h2>Mesh oder PVC?</h2>
    <p><strong>Mesh-Banner</strong> sind gelocht und lassen einen Teil des Windes durch. Für Bauzäune im Freien ist das meist die richtige Wahl, denn ein geschlossenes Banner wirkt wie ein Segel – und die Kraft geht auf Ösen, Zaun und Zaunfüße. Das Druckbild ist durch die Löcher etwas weniger satt, aus der Entfernung fällt das kaum auf.</p>
    <p><strong>PVC-Banner</strong> sind geschlossen und blickdicht. Sie passen für geschützte Lagen, kleinere Flächen oder wenn der Zaun auch Sichtschutz sein soll – dann aber mit besonders guter Befestigung.</p>

    <h2>Richtig messen</h2>
    <p>Bauzaunelemente sind nicht alle gleich groß. Messen Sie das Feld innerhalb des Rahmens aus und planen Sie das Banner etwas kleiner, damit es sich ringsum spannen lässt. Wichtige Inhalte gehören nicht an den Rand, wo Zaunschellen oder Stützen sitzen.</p>

    <h2>Ösen und Befestigung</h2>
    <ul>
      <li><strong>Ösen ringsum:</strong> Standard ist etwa alle 50&nbsp;cm. An windigen Standorten setzen wir die Ösen enger und verstärken die Ecken.</li>
      <li><strong>Alle Ösen nutzen:</strong> Nur so verteilt sich die Zugkraft. Werden nur die Ecken befestigt, reißen sie zuerst aus.</li>
      <li><strong>Kabelbinder</strong> sind schnell und günstig, aber starr und im Sonnenlicht nicht ewig haltbar – gut für kurze Einsätze.</li>
      <li><strong>Spanngummis</strong> federn Windstöße ab und schonen die Ösen – die bessere Wahl für längere Standzeiten.</li>
      <li><strong>Kontrolle:</strong> Befestigung regelmäßig prüfen und das Banner vor angekündigtem Sturm im Zweifel abnehmen.</li>
    </ul>
    <p>Wichtig: Ein Banner erhöht die Windlast auf den Bauzaun. Ob der Zaun dafür ausreichend beschwert oder abgestützt ist, klären Sie mit dem Verleiher oder Bauleiter.</p>

    <h2>Was draufgehört</h2>
    <p>Ein Bauzaun wird im Vorbeigehen und Vorbeifahren gelesen. Drei Dinge reichen: wer Sie sind, was Sie machen und wie man Sie erreicht. Große Schrift, starker Kontrast, wenig Text. Ein QR-Code funktioniert nur, wenn er groß genug ist und man davor stehen bleiben kann.</p>

    <h2>Brandschutz</h2>
    <p>Draußen am Bauzaun spielt er selten eine Rolle. Hängt das Banner aber in einer Halle, an einem Gerüst im Innenhof oder bei einer Veranstaltung, wird oft schwer entflammbares Material (B1 nach DIN&nbsp;4102) verlangt. Sagen Sie uns vorher, wo das Banner hängt.</p>

    <h2>Braucht Werbung am Bauzaun eine Genehmigung?</h2>
    <p>Ein Banner kann eine <strong>Werbeanlage</strong> im Sinne der Bauordnung sein. Ob eine Genehmigung nötig ist, hängt vom Bundesland, der Größe, der Dauer und dem Ort ab:</p>
    <ul>
      <li><strong>NRW:</strong> Werbeanlagen bis 1&nbsp;m² und Werbeanlagen, die erkennbar nur vorübergehend für höchstens zwei Monate angebracht werden, sind verfahrensfrei – nicht im Außenbereich (§&nbsp;62 Abs.&nbsp;1 Nr.&nbsp;12 BauO NRW).</li>
      <li><strong>Brandenburg:</strong> Auch hier sind vorübergehende Werbeanlagen für höchstens zwei Monate verfahrensfrei, außer im Außenbereich (§&nbsp;61 BbgBO).</li>
      <li><strong>Berlin:</strong> Verfahrensfrei sind Werbeanlagen bis 1&nbsp;m² Ansichtsfläche, an der Stätte der Leistung bis 2,5&nbsp;m² (§&nbsp;61 Abs.&nbsp;1 BauO Bln). Für größere Banner oder Fremdwerbung fragen Sie vorher beim Bezirksamt nach.</li>
      <li><strong>Hamburg:</strong> Bis 1&nbsp;m² genehmigungsfrei, darüber meist Baugenehmigung; zuständig ist das Bezirksamt.</li>
    </ul>
    <p>Verfahrensfrei heißt nicht, dass alles erlaubt ist: Örtliche Satzungen, Denkmalschutz und die Verkehrssicherheit gelten weiter. Ein Banner darf zum Beispiel nicht die Sicht an Ausfahrten oder Kreuzungen verdecken. Steht der Bauzaun auf dem Gehweg oder der Straße, braucht er ohnehin eine Erlaubnis zur Sondernutzung – klären Sie mit dem Straßenamt, ob Werbung daran erlaubt ist.</p>
    <p>Nicht verwechseln: Das <strong>Bauschild</strong> mit Angaben zum Bauvorhaben ist bei genehmigungspflichtigen Bauvorhaben vorgeschrieben – es ist keine Werbung, kann aber im selben Layout gestaltet werden.</p>

    <h2>Checkliste für Ihr Bauzaunbanner</h2>
    <ol>
      <li>Standort prüfen: windig oder geschützt? Dann Mesh oder PVC wählen.</li>
      <li>Feld innerhalb des Zaunrahmens ausmessen.</li>
      <li>Ösen ringsum, bei Wind enger und mit verstärkten Ecken.</li>
      <li>Spanngummis für längere Standzeit, alle Ösen nutzen.</li>
      <li>Standsicherheit des Zauns mit Verleiher oder Bauleitung klären.</li>
      <li>Genehmigung und Sondernutzung vorher klären – je nach Land, Größe und Dauer.</li>
    </ol>''',
  cta=('Banner aus Berlin', 'PVC-, Mesh- und Blockout-Banner mit Gestaltung und auf Wunsch Montage – PVC-Banner ab 29 € pro m² netto in Berlin, ab 34 € in NRW.', '/pvc-banner-berlin.html', 'PVC-Banner ansehen', 'Hallo, ich brauche Bauzaunbanner. Anzahl und Größe: ', 'PVC-Banner'),
  weiter=[('/pvc-banner-berlin.html', 'PVC-Banner Berlin'), ('/pvc-banner-nrw.html', 'PVC-Banner NRW'), ('/werbung-handwerker-berlin.html', 'Werbung für Handwerker')],
  quellen=[('https://bauportal.nrw/werbeanlagen-bauen-nordrhein-westfalen', 'Bauportal.NRW – Werbeanlagen bauen in Nordrhein-Westfalen'),
           ('https://www.duisburg.de/vv/produkte/pro_du/dez_vii/errichtung_von_werbeanlagen.php', 'Stadt Duisburg – Errichtung von Werbeanlagen'),
           ('https://www.anwalt24.de/gesetze/bbgbo-1/61', '§ 61 BbgBO – Verfahrensfreie Vorhaben'),
           ('https://www.anwalt24.de/gesetze/bauo_bln/61', '§ 61 BauO Bln – Verfahrensfreie Bauvorhaben'),
           ('https://dokumente.hamburg.de/resource/blob/190466/267e443ff2b54e7ceb473a937b58a180/bpd-werbeanlagen-data.pdf', 'Hamburg – Bauprüfdienst Werbeanlagen'),
           ('https://www.ihk.de/hamburg/produktmarken/beratung-service/recht-und-steuern/wirtschaftsrecht/gewerberecht/aussenwerbung-1156810', 'Handelskammer Hamburg – Außenwerbung')],
  hinweis=HINWEIS_RECHT,
  related=[('/blog/werbung-handwerker.html', 'Werbung für Handwerker', '7 Ideen mit Kosten – vom Fahrzeug bis zum Bauzaun.'),
           ('/blog/fotowand-firmenfeier.html', 'Fotowand für die Firmenfeier', 'Größe, Material und Brandschutz.')],
  index=('Banner', 'Bauzaunbanner: Material, Befestigung, Genehmigung', 'Mesh oder PVC, Ösen und Spanngummis, Wind, Brandschutz und wann das Amt mitredet.'),
  llms='Bauzaunbanner: Material, Befestigung, Genehmigung'),

 dict(file='arbeitskleidung-bedrucken.html', og=('textildruck.webp', 'Ratgeber Textildruck', 'Arbeitskleidung bedrucken', 'Verfahren, Wäsche, Teambestellung'), crumb='Arbeitskleidung bedrucken',
  title='Arbeitskleidung bedrucken: Verfahren, Wäsche, Bestellung',
  desc='Logo auf Arbeitskleidung: Flex, Flock oder DTF, was die Wäsche aushält, wo das Logo sitzen sollte und wie eine Teambestellung ohne Durcheinander klappt.',
  tag='Ratgeber · Textildruck', h1='Arbeitskleidung bedrucken:<br><em>Verfahren, Wäsche, Bestellung.</em>', minuten=5,
  bild=('/textildruck', 'T-Shirt, zwei Hoodies, Tasche und Cap mit aufgedrucktem Schriftzug', 'Shirt, Hoodie, Tasche: Ein einheitliches Logo macht aus Kleidung einen Auftritt.'),
  intro='<p>Ein Logo auf der Arbeitskleidung zeigt sofort, wer zum Team gehört – beim Kunden, auf der Baustelle, im Laden. Damit der Druck nicht nach ein paar Wäschen aufgibt, sollten Sie vor der Bestellung drei Dinge klären: wie gewaschen wird, welches Verfahren zum Logo passt und wo das Logo sitzen soll.</p>',
  body='''
    <h2>Zuerst: Wie wird die Kleidung gewaschen?</h2>
    <p>Das ist die wichtigste Frage – und die, die am häufigsten vergessen wird. Shirts, die zu Hause gewaschen werden, stellen andere Ansprüche als Kleidung, die regelmäßig in eine gewerbliche Wäscherei geht, wo heißer und mit stärkeren Mitteln gewaschen wird. Schauen Sie aufs Pflegeetikett und sagen Sie uns, wie bei Ihnen gewaschen wird. Dann wählen wir das Verfahren danach – oder sagen Ihnen ehrlich, wenn ein anderes Verfahren besser passt.</p>

    <h2>Flex, Flock oder DTF?</h2>
    <ul>
      <li><strong>Flex:</strong> Das Logo wird aus farbiger Folie geschnitten und aufgepresst. Sehr scharfe Kanten, ideal für Schriftzüge und Logos in ein bis zwei Farben, Namen und Nummern.</li>
      <li><strong>Flock:</strong> wie Flex, aber mit samtiger, leicht erhabener Oberfläche – wirkt hochwertig auf Hoodies und Jacken.</li>
      <li><strong>DTF (Direct to Film):</strong> Das Motiv wird auf eine Folie gedruckt und übertragen. Alle Farben in einem Arbeitsgang, auch Verläufe, Fotos und feine Details.</li>
    </ul>
    <p>Stickerei bieten wir nicht an. Wenn Ihr Logo oder Ihre Wäsche eher nach Stick verlangt, sagen wir Ihnen das vorher.</p>

    <h2>Schutz- und Warnkleidung</h2>
    <p>Bei Warnschutz- und anderer Schutzkleidung gilt besondere Vorsicht: Reflexstreifen und Leuchtflächen dürfen nicht überdruckt werden, und bedruckt wird nur dort, wo der Hersteller es zulässt. Sonst kann die Schutzwirkung leiden. Fragen Sie im Zweifel beim Hersteller der Kleidung nach, bevor Sie bestellen.</p>

    <h2>Wo das Logo sitzen sollte</h2>
    <ul>
      <li><strong>Brust links:</strong> der Klassiker – im Gespräch auf Augenhöhe sichtbar.</li>
      <li><strong>Rücken groß:</strong> wirkt auf Distanz, etwa auf der Baustelle, beim Umzug oder in der Werkstatt. Hier passen auch Website oder Telefonnummer.</li>
      <li><strong>Ärmel:</strong> als Ergänzung, zum Beispiel für ein kleines Symbol oder einen Slogan.</li>
    </ul>
    <p>Wir zeigen Ihnen vor der Produktion, wie Größe und Position auf dem Textil aussehen – so gibt es keine Überraschung.</p>

    <h2>Teambestellung ohne Durcheinander</h2>
    <ol>
      <li><strong>Größenliste:</strong> Wir schicken Ihnen eine einfache Liste – jede Person trägt ihre Größe ein.</li>
      <li><strong>Reserve einplanen:</strong> Für neue Mitarbeitende ein paar Teile mehr bestellen. Textilfarben und Modelle können später ausverkauft sein.</li>
      <li><strong>Eigene Textilien?</strong> Geht auch. Schicken Sie uns ein Foto vom Pflegeetikett, damit wir das Material kennen.</li>
      <li><strong>Mindestmenge:</strong> bei uns 5 Stück.</li>
    </ol>
    <div class="tip-box">
      <p><strong>Preise bei uns (netto, ab 5 Stück):</strong> T-Shirt mit Logo ab 15&nbsp;€, Poloshirt ab 22&nbsp;€, Hoodie ab 35&nbsp;€, eigene Textilien ab 7&nbsp;€ je Motiv – inklusive Gestaltung und Aufbereitung Ihres Logos.</p>
    </div>

    <h2>Damit der Druck lange hält</h2>
    <ul>
      <li>Auf links drehen und nicht heißer waschen als auf dem Etikett angegeben – bei bedruckten Teilen höchstens 40&nbsp;°C.</li>
      <li>Nicht direkt auf dem Motiv bügeln.</li>
      <li>Auf Weichspüler verzichten und den Trockner sparsam nutzen.</li>
    </ul>''',
  cta=('Textildruck aus Berlin', 'Flex, Flock und DTF ab 5 Stück – Abholung in Berlin oder Versand in ganz Deutschland.', '/textildruck-berlin.html', 'Textildruck ansehen', 'Hallo, ich möchte Arbeitskleidung mit unserem Logo bedrucken lassen. Anzahl: ', 'Textildruck'),
  weiter=[('/textildruck-berlin.html', 'Textildruck Berlin'), ('/grafikdesign-berlin.html', 'Logo & Grafikdesign'), ('/werbung-handwerker-berlin.html', 'Werbung für Handwerker')],
  quellen=[('https://www.ginetex.net/', 'GINETEX – Internationale Pflegekennzeichnung für Textilien')],
  hinweis=HINWEIS_PRAXIS,
  related=[('/blog/logo-dateien-werbetechnik.html', 'Logo-Dateien für Druck & Folie', 'Welche Datei Werkstatt und Druckerei brauchen.'),
           ('/blog/werbung-handwerker.html', 'Werbung für Handwerker', '7 Ideen mit Kosten.')],
  index=('Textildruck', 'Arbeitskleidung bedrucken: Verfahren, Wäsche, Bestellung', 'Flex, Flock oder DTF, Wäsche, Schutzkleidung, Logo-Position und Teambestellung.'),
  llms='Arbeitskleidung bedrucken: Verfahren, Wäsche, Bestellung'),

 dict(file='logo-dateien-werbetechnik.html', og=('grafikdesign.webp', 'Ratgeber Gestaltung', 'Logo-Dateien', 'Was Werkstatt und Druckerei brauchen'), crumb='Logo-Dateien',
  title='Logo-Dateien für Schild, Folie und Druck',
  desc='Vektor oder Pixel, PDF, SVG oder PNG: Welche Logo-Datei Werkstatt und Druckerei brauchen, wie Sie eine gute Datei erkennen und was hilft, wenn keine da ist.',
  tag='Ratgeber · Gestaltung', h1='Logo-Dateien für Schild, Folie und Druck:<br><em>Was wir wirklich brauchen.</em>', minuten=5,
  bild=('/grafikdesign', 'Grafik eines Laptops mit Gestaltungsprogramm und gedruckten Entwürfen', 'Gute Druckdaten sparen Zeit – und sorgen dafür, dass das Logo auch groß scharf bleibt.'),
  intro='<p>„Schicken Sie uns bitte Ihr Logo als Vektordatei.“ Diesen Satz hören viele Betriebe zum ersten Mal, wenn sie ein Schild, eine Fahrzeugbeschriftung oder ein Banner bestellen. Was damit gemeint ist, woran Sie eine gute Datei erkennen und was Sie tun, wenn Sie keine haben – hier in Ruhe erklärt.</p>',
  body='''
    <h2>Vektor oder Pixel – der Unterschied</h2>
    <p>Eine <strong>Pixeldatei</strong> (JPG, PNG) besteht aus vielen kleinen Farbpunkten. Für eine Website oder Visitenkarte reicht das oft. Vergrößert man sie auf ein Schild oder einen Transporter, werden die Kanten unscharf und treppig.</p>
    <p>Eine <strong>Vektordatei</strong> beschreibt das Logo mit Linien und Flächen. Sie lässt sich beliebig vergrößern und bleibt scharf. Für Folienschriften ist sie sogar Pflicht: Der Schneideplotter fährt genau diese Linien ab.</p>

    <h2>Welche Formate passen?</h2>
    <ul>
      <li><strong>PDF, SVG, AI, EPS:</strong> meist Vektor – ideal. Aber Vorsicht: Ein PDF kann auch nur ein eingebettetes Foto enthalten.</li>
      <li><strong>PNG mit transparentem Hintergrund:</strong> gut für Bildschirm und kleine Drucke, für große Flächen nur in sehr hoher Auflösung.</li>
      <li><strong>JPG:</strong> für Logos die schwächste Wahl – kein transparenter Hintergrund, oft unscharfe Kanten.</li>
      <li><strong>Word, PowerPoint, Screenshot:</strong> als Vorlage, damit wir sehen, wie es aussehen soll – zum Drucken nicht geeignet.</li>
    </ul>

    <h2>So prüfen Sie Ihre Datei in einer Minute</h2>
    <ol>
      <li>Datei in einem PDF-Programm oder Browser öffnen.</li>
      <li>Stark hineinzoomen, auf 800&nbsp;% oder mehr.</li>
      <li>Bleiben die Kanten glatt und scharf, ist es sehr wahrscheinlich Vektor. Sehen Sie Treppchen oder Unschärfe, sind es Pixel.</li>
    </ol>

    <h2>Farben: was auf dem Bildschirm anders aussieht</h2>
    <p>Bildschirme zeigen Farben in RGB, gedruckt wird in CMYK – deshalb wirkt ein leuchtendes Blau auf Papier oft etwas ruhiger. Für eine genaue Hausfarbe helfen festgelegte Farbwerte, zum Beispiel aus Ihrem Corporate Design. Folien gibt es in festen Farbtönen der Hersteller: Wir wählen den Ton, der Ihrer Farbe am nächsten kommt, und zeigen Ihnen bei Bedarf vorher ein Muster.</p>

    <h2>Schriften und feine Details</h2>
    <p>Schriften im Logo sollten in Pfade (Kurven) umgewandelt sein – sonst ersetzt der Computer sie womöglich durch eine andere Schrift. Sehr feine Linien und winzige Schrift sehen am Bildschirm gut aus, gehen aber auf Folie oder aus der Entfernung verloren. Für Schild und Fahrzeug lohnt sich oft eine vereinfachte Version des Logos.</p>

    <h2>Keine gute Datei vorhanden?</h2>
    <p>Fragen Sie zuerst bei der Agentur oder Person nach, die das Logo gestaltet hat – dort liegt meist die offene Datei. Gibt es sie nicht mehr, bauen wir das Logo als Vektordatei nach. Den Aufwand nennen wir Ihnen vorher im Angebot.</p>
    <p>Ein Punkt, der oft vergessen wird: Wer ein Logo gestalten lässt, braucht die <strong>Nutzungsrechte</strong> daran (§&nbsp;31 UrhG). Halten Sie im Auftrag fest, dass Sie das Logo uneingeschränkt nutzen dürfen und die offenen Dateien bekommen. Bevor Sie ein neues Logo festlegen, lohnt außerdem ein Blick ins Markenregister des DPMA.</p>

    <h2>Checkliste für Ihre Druckdaten</h2>
    <ol>
      <li>Logo als PDF, SVG, AI oder EPS – Zoomtest bestanden.</li>
      <li>Schriften in Pfade umgewandelt.</li>
      <li>Hausfarben als Farbwerte notiert.</li>
      <li>Bei Bedarf eine vereinfachte Version für Schild und Fahrzeug.</li>
      <li>Nutzungsrechte und offene Dateien beim Gestalter gesichert.</li>
    </ol>''',
  cta=('Logo & Gestaltung aus Berlin', 'Schicken Sie uns Ihre Datei: Wir prüfen sie vor dem Druck, bauen das Logo bei Bedarf nach oder gestalten ein neues – Logo-Design ab 490 € netto.', '/grafikdesign-berlin.html', 'Grafikdesign ansehen', 'Hallo, ich habe eine Frage zu unserer Logo-Datei.', 'Grafikdesign'),
  weiter=[('/grafikdesign-berlin.html', 'Grafikdesign Berlin'), ('/schilder-berlin.html', 'Schilder'), ('/pvc-banner-berlin.html', 'PVC-Banner')],
  quellen=[('https://www.gesetze-im-internet.de/urhg/__31.html', '§ 31 UrhG – Einräumung von Nutzungsrechten'),
           ('https://www.dpma.de/marken/', 'Deutsches Patent- und Markenamt – Marken')],
  hinweis='Hinweis: Allgemeine Hinweise aus der Praxis, keine Rechtsberatung. Bei Fragen zu Marken- und Urheberrecht hilft eine fachkundige Beratung.',
  related=[('/blog/arbeitskleidung-bedrucken.html', 'Arbeitskleidung bedrucken', 'Verfahren, Wäsche und Teambestellung.'),
           ('/blog/fahrzeugbeschriftung-tipps.html', 'Fahrzeugbeschriftung: 7 Tipps', 'Folie, Schriftgröße und Montage.')],
  index=('Gestaltung', 'Logo-Dateien für Schild, Folie und Druck', 'Vektor oder Pixel, die richtigen Formate, der Zoomtest und was hilft, wenn keine Datei da ist.'),
  llms='Logo-Dateien für Schild, Folie und Druck'),
]

# ---------------------------------------------------------------------------
VORLAGE_DATEI = os.path.join(ROOT, 'blog', 'fotowand-firmenfeier.html')


def bauen(a, vorlage):
    s = vorlage
    url = BASE + 'blog/' + a['file']
    s = s.replace(BASE + 'blog/fotowand-firmenfeier.html', url)
    s = re.sub(r'<title>.*?</title>', f'<title>{a["title"]}</title>', s, count=1)
    for k in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        s = re.sub(rf'(<meta {k} content=")[^"]*', lambda m: m.group(1) + a['desc'], s, count=1)
    for k in ('property="og:title"', 'name="twitter:title"'):
        s = re.sub(rf'(<meta {k} content=")[^"]*', lambda m: m.group(1) + a['title'], s, count=1)
    b, alt, cap = a['bild']
    img = BASE.rstrip('/') + b + '.webp'
    # Vorschaubild: eigene Karte aus og_cards.py, falls schon erzeugt – sonst das Artikelbild
    karte = 'og/blog-' + a['file'].replace('.html', '.jpg')
    og = BASE + karte if os.path.exists(os.path.join(ROOT, karte)) else img
    s = re.sub(r'(<meta property="og:image" content=")[^"]*', lambda m: m.group(1) + og, s, count=1)
    s = re.sub(r'(<meta name="twitter:image" content=")[^"]*', lambda m: m.group(1) + og, s, count=1)
    if og != img:
        s = re.sub(r'(<meta property="og:image:width" content=")[^"]*', r'\g<1>1200', s, count=1)
        s = re.sub(r'(<meta property="og:image:height" content=")[^"]*', r'\g<1>630', s, count=1)
        s = re.sub(r'(<meta property="og:image:type" content=")[^"]*', r'\g<1>image/jpeg', s, count=1)
    og_alt = a['og'][2] + ' – Masar Werbeagentur' if og != img else alt
    s = re.sub(r'(<meta property="og:image:alt" content=")[^"]*', lambda m: m.group(1) + og_alt, s, count=1)
    s = re.sub(r'"image": "[^"]*"', '"image": ' + json.dumps(img), s, count=1)
    s = re.sub(r'"headline": "[^"]*"', '"headline": ' + json.dumps(a['title'], ensure_ascii=False), s, count=1)
    s = re.sub(r'"description": "[^"]*"', '"description": ' + json.dumps(a['desc'], ensure_ascii=False), s, count=1)
    s = re.sub(r'"datePublished": "[^"]*"', f'"datePublished": "{DATUM}"', s, count=1)
    s = re.sub(r'"dateModified": "[^"]*"', f'"dateModified": "{DATUM}"', s, count=1)
    s = s.replace('"name": "Fotowand Firmenfeier"', '"name": ' + json.dumps(a['crumb'], ensure_ascii=False))
    s = re.sub(r'(<div class="art-tag"><svg.*?</svg>)[^<]*', lambda m: m.group(1) + a['tag'], s, count=1, flags=re.S)
    s = re.sub(r'<h1>.*?</h1>', f'<h1>{a["h1"]}</h1>', s, count=1, flags=re.S)
    s = re.sub(r'\d+ Min\. Lesezeit', f'{a["minuten"]} Min. Lesezeit', s, count=1)
    fig = (f'\n    <figure class="art-figure">\n      <img src="{b}-720.webp" srcset="{b}-360.webp 360w, {b}-540.webp 540w, {b}-720.webp 720w, {b}.webp 1080w" '
           f'sizes="(max-width:600px) 92vw, 420px" width="720" height="900" alt="{alt}" loading="eager">\n      <figcaption>{cap}</figcaption>\n    </figure>\n')
    t, p, ziel, ziel_txt, wa_txt, thema = a['cta']
    weiter = ' · '.join(f'<a href="{h}" style="color:var(--teal);font-weight:700;">{x}</a>' for h, x in a['weiter'])
    quellen = ''
    if a.get('quellen'):
        quellen = ('''
    <div class="sources">
      <h2>Quellen</h2>
      <ul>
''' + ''.join(f'        <li><a href="{h}" target="_blank" rel="noopener noreferrer">{x}</a></li>\n' for h, x in a['quellen']) +
                   f'''      </ul>
      <p>{a['hinweis']} Stand: November 2026.</p>
    </div>
''')
    cta = f'''    <div class="article-cta">
      <h3>{t}</h3>
      <p>{p}</p>
      <div class="btns">
        <a href="{ziel}" class="btn-teal">{ziel_txt}</a>
        <a href="{WA}{quote(wa_txt)}" class="btn-wa" target="_blank" rel="noopener noreferrer">WhatsApp</a>
        <a href="/termin.html?thema={quote(thema)}" data-termin-link class="btn-termin" style="background:#fff;color:var(--navy);padding:13px 24px;border-radius:8px;font-weight:700;font-size:15px">Kostenlose Beratung buchen</a>
      </div>
      <p style="margin:1.2rem 0 0;font-size:14px;">Weiter: {weiter}</p>
    </div>
{quellen}
    <div class="related-posts">
      <h2>Weitere Artikel</h2>
      <div class="related-grid">
''' + ''.join(f"""        <div class="related-card">
          <h3>{x}</h3>
          <p>{d}</p>
          <a href="{h}">Artikel lesen →</a>
        </div>
""" for h, x, d in a['related']) + '''      </div>
    </div>

  </div>
</main>'''
    i = s.index('<main class="article-body">'); j = s.index('</main>', i) + len('</main>')
    s = s[:i] + '<main class="article-body">\n  <div class="container">\n\n    ' + a['intro'] + fig + a['body'] + '\n\n' + cta + s[j:]
    open(os.path.join(ROOT, 'blog', a['file']), 'w', encoding='utf-8').write(s)
    return a['file'], len(s)


# --- Eintragen in Blog-Übersicht, Sitemap, llms.txt (idempotent) ----------
ICON_IMG = '<svg class="i-inline" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/></svg>'
ICON_CAL = '<svg class="i-inline" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/></svg>'
ICON_UHR = '<svg class="i-inline" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><line x1="10" x2="14" y1="2" y2="2"/><line x1="12" x2="15" y1="14" y2="11"/><circle cx="12" cy="14" r="8"/></svg>'


def karte(a):
    tag, h2, txt = a['index']
    return f'''        <article class="blog-card">
          <div class="blog-card-img">{ICON_IMG}</div>
          <div class="blog-card-body">
            <span class="blog-tag">{tag}</span>
            <div class="blog-meta"><span>{ICON_CAL}November 2026</span><span>{ICON_UHR}{a['minuten']} Min. Lesezeit</span></div>
            <h2>{h2}</h2>
            <p>{txt}</p>
            <a href="/blog/{a['file']}" class="blog-read-more">Artikel lesen →</a>
          </div>
        </article>
'''


def eintragen():
    p = os.path.join(ROOT, 'blog', 'index.html')
    s = open(p, encoding='utf-8').read()
    neu = ''.join(karte(a) for a in ARTIKEL if f'/blog/{a["file"]}"' not in s)
    if neu:
        i = s.index('<div class="blog-grid">')
        i = s.index('<article class="blog-card">', i)
        s = s[:i] + neu.lstrip(' ') + '        ' + s[i:]
        open(p, 'w', encoding='utf-8').write(s)
    p = os.path.join(ROOT, 'sitemap.xml')
    s = open(p, encoding='utf-8').read()
    neu = ''.join(f'''  <url>
    <loc>{BASE}blog/{a['file']}</loc>
    <lastmod>{DATUM}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>

''' for a in ARTIKEL if f'{BASE}blog/{a["file"]}<' not in s)
    if neu:
        i = s.index('  <url>\n    <loc>' + BASE + 'blog/fotowand-firmenfeier.html')
        s = s[:i] + neu + s[i:]
        open(p, 'w', encoding='utf-8').write(s)
    p = os.path.join(ROOT, 'llms.txt')
    s = open(p, encoding='utf-8').read()
    if 'Ratgeber Werbetechnik:' not in s:
        zeile = '- Ratgeber Werbetechnik: ' + ', '.join(f'[{a["llms"]}]({BASE}blog/{a["file"]})' for a in ARTIKEL)
        anker = s.index('- Ratgeber KI in Praxis & Pflege:')
        s = s[:anker] + zeile + '\n' + s[anker:]
        open(p, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    vorlage = open(VORLAGE_DATEI, encoding='utf-8').read()
    for a in ARTIKEL:
        print(bauen(a, vorlage))
    eintragen()
    print('Blog-Übersicht, Sitemap und llms.txt geprüft')
