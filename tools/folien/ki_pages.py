"""KI für Arztpraxen / Pflegedienste / Handwerker (Generator: gen_folien.build_f).
Leistungen laut Inhaber (03.11.2026): Chat- und WhatsApp-Assistent, Online-Terminbuchung mit Erinnerungen,
Vorsortieren von E-Mails und Dokumenten, dazu Marketing und Entwicklung. KEINE Telefon-/Sprach-KI, keine Preise.
Recht (Recherche 03.11.2026, privat: tools/angebot/privat/marketing/KI_Recht_Memo_2026-11-03.md): KI-Hinweis (Art. 50 KI-VO),
keine medizinische Beratung, AV-Vertrag, § 203 StGB, EU-Hosting, Datensparsamkeit, WhatsApp nur Business-Plattform + Einwilligung.
Keine Zahlen zu Zeitersparnis, nicht „rechtssicher“/„zertifiziert“.
"""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'gen_folien.py'), encoding='utf-8').read()
exec(src[:src.index("\nif __name__")])


def demo(art, text):
    """Weitere Bausteine (Online-Termin, Postfach, Wissens-Assistent) – der Chat-Assistent steht oben im Hero."""
    return ('Weitere Bausteine', 'Noch mehr <em>zum Ausprobieren</em>',
            'Online-Termine, ein vorsortiertes Postfach und ein Assistent für Ihre eigenen Unterlagen – so arbeiten die Bausteine für ' + text + '.',
            f'    <div data-ki-bausteine="{art}" class="reveal"></div>')


EIGEN = '''<section class="section" id="eigenes-system">
  <div class="container">
    <div class="sec-head center reveal">
      <span class="eyebrow">Selbst im Einsatz</span>
      <h2 class="sec-title">Unser eigenes System – <em>jeden Tag in Betrieb</em></h2>
      <p class="sec-sub">Was wir Ihnen anbieten, nutzen wir selbst. Die Bausteine laufen auf masar-werbeagentur.de – Sie können sie gleich ausprobieren.</p>
    </div>
    <figure class="reveal" style="max-width:340px;margin:0 auto 2.2rem;text-align:center">
      <video controls muted playsinline preload="none" poster="/videos/anfrage-assistent-demo.webp" width="390" height="760" aria-label="Bildschirmaufnahme: Eine Anfrage wird im Anfrage-Assistenten auf masar-werbeagentur.de Schritt für Schritt aufgenommen" style="display:block;width:100%;height:auto;border-radius:18px;border:1px solid var(--border);background:#132e50"><source src="/videos/anfrage-assistent-demo.mp4" type="video/mp4"></video>
      <figcaption style="font-size:14px;color:var(--muted);margin-top:.7rem">Bildschirmaufnahme unseres Anfrage-Assistenten auf dieser Website, mit Beispielangaben.</figcaption>
    </figure>
    <div class="why-grid">
      <div class="why-item"><div class="why-num">1</div><div><h3>Anfrage-Assistent</h3><p>Führt Kunden Schritt für Schritt zu einer vollständigen Anfrage – mit Anfragenummer statt loser Nachricht. <a href="/#kontakt">Ausprobieren →</a></p></div></div>
      <div class="why-item"><div class="why-num">2</div><div><h3>Online-Terminbuchung</h3><p>Freie Zeiten, Feiertage gesperrt, Bestätigung sofort und Erinnerung etwa 24 Stunden vorher per E-Mail. <a href="/termin.html">Termin ansehen →</a></p></div></div>
      <div class="why-item"><div class="why-num">3</div><div><h3>Status-Seite</h3><p>Kunden sehen mit Nummer und Telefon den Stand ihrer Anfrage und können einen Termin verschieben oder absagen lassen. <a href="/status.html">Status-Seite →</a></p></div></div>
      <div class="why-item"><div class="why-num">4</div><div><h3>Digitaler Sekretär</h3><p>Neue Anfragen, Erinnerung vor jedem Termin und ein Tagesbericht kommen als Nachricht aufs Handy – ohne personenbezogene Daten in der Nachricht.</p></div></div>
    </div>
  </div>
</section>
'''

GENERATOR = '''<section class="section bg-alt" id="generator" hidden>
  <div class="container">
    <div class="sec-head center reveal">
      <span class="eyebrow">Kostenlos ausprobieren</span>
      <h2 class="sec-title">Ein Assistent für <em>Ihre Website – in einer Minute</em></h2>
      <p class="sec-sub">Geben Sie die Adresse Ihrer Website ein. Der Assistent liest Ihre öffentlichen Seiten und beantwortet Fragen so, wie es Ihre Kunden erleben würden. Eine Vorführung – nichts wird auf Ihrer Website verändert.</p>
    </div>
    <div data-ki-generator class="reveal"></div>
  </div>
</section>
'''

RECHT = '''<p><strong>Klarer KI-Hinweis:</strong> Wer mit dem Assistenten schreibt, erfährt gleich zu Beginn, dass es ein digitaler Assistent ist – so verlangt es die EU-KI-Verordnung (Art.&nbsp;50) seit dem 2.&nbsp;August&nbsp;2026.</p>
<p><strong>Keine medizinische Beratung:</strong> Der Assistent stellt keine Diagnose, bewertet keine Beschwerden und fragt nicht nach Symptomen. Bei Notfall-Wörtern verweist er sofort an 112{bereit}.</p>
<p><strong>So wenig Daten wie möglich:</strong> Terminart per Auswahl statt Freitext, feste Löschfristen, Hosting und KI-Modell in der EU. Was nicht gebraucht wird, wird nicht erfasst.</p>
<p><strong>Vertraglich sauber:</strong> Wir arbeiten als Auftragsverarbeiter mit AV-Vertrag nach Art.&nbsp;28 DSGVO und unterschreiben eine Verschwiegenheitsverpflichtung nach §&nbsp;203 StGB. Sie bekommen dazu die Liste der technischen Maßnahmen, der Unterauftragnehmer und eine Vorlage für die Datenschutz-Folgenabschätzung.</p>
<p><strong>WhatsApp nur richtig angebunden:</strong> Nicht über die normale App auf dem Praxis-Handy, sondern über die WhatsApp Business Platform mit EU-Anbieter, nur nach Einwilligung und ohne Gesundheitsangaben in der Nachricht. Ein anderer Weg (E-Mail oder SMS) bleibt immer möglich.</p>
<p><strong>Ihr Team entscheidet:</strong> Antwortentwürfe und Terminvorschläge gibt ein Mensch frei. Der Assistent ergänzt Ihre {software} – er ersetzt sie nicht.</p>
<p style="font-size:13px;">Allgemeine Hinweise, keine Rechtsberatung. Grundlagen: <a href="https://eur-lex.europa.eu/eli/reg/2024/1689/oj" target="_blank" rel="noopener noreferrer">KI-Verordnung (EU) 2024/1689</a>, <a href="https://eur-lex.europa.eu/eli/reg/2016/679/oj" target="_blank" rel="noopener noreferrer">DSGVO</a>, <a href="https://www.gesetze-im-internet.de/stgb/__203.html" target="_blank" rel="noopener noreferrer">§ 203 StGB</a>.</p>'''

LEISTUNGEN = lambda wer: [
  ('web', 'Chat-Assistent auf der Website', f'Beantwortet die immer gleichen Fragen und nimmt Anliegen vollständig auf – rund um die Uhr, in mehreren Sprachen.', '#demo'),
  ('phone', 'WhatsApp-Assistent', 'Für alle, die lieber schreiben: über die WhatsApp Business Platform, mit Einwilligung und EU-Anbieter.', '#datenschutz'),
  ('karte', 'Online-Termine & Erinnerungen', f'{wer} wählen freie Zeiten selbst, bekommen eine Bestätigung und eine Erinnerung vor dem Termin.', '#bausteine'),
  ('druck', 'E-Mails vorsortieren', 'Eingehende Nachrichten werden gelesen, eingeordnet und mit einem Antwortentwurf versehen, den Ihr Team freigibt.', '#bausteine'),
  ('auge', 'Assistent für Ihre Unterlagen', 'Beantwortet interne Fragen aus Ihren eigenen Dokumenten – Abläufe, Richtlinien, Checklisten – und nennt die Quelle.', '#bausteine'),
  ('stern', 'Website & Marketing', 'Auf Wunsch die passende Website, Praxis- oder Firmenschild und Social Media dazu – alles aus einer Hand.', '/webdesign-berlin.html'),
]

PRAXIS = dict(file='ki-fuer-arztpraxen-berlin.html', crumb='KI für Arztpraxen', img='ki-arztpraxis',
 parent=('KI-Lösungen', 'ki-loesungen/'), finder_strip=False, tab_ey='Anliegen', hero_mobile=True,
 img_alt='Bildschirmfoto unseres Praxis-Assistenten: Ein Patient schreibt auf Türkisch, das Praxisteam bekommt das Anliegen auf Deutsch',
 title='KI für Arztpraxen Berlin: Chat-Assistent & Online-Termine | Masar',
 desc='Digitaler Assistent für Berliner Arztpraxen: Fragen beantworten, Termine und Rezeptwünsche online aufnehmen, Erinnerungen, E-Mails vorsortieren – mit KI-Hinweis, AV-Vertrag und EU-Hosting.',
 service_type='KI-Assistent für Arztpraxen', schema_name='Digitaler Assistent für Arztpraxen in Berlin',
 badge='KI für Arztpraxen · Berlin', h1='KI-Assistent für Arztpraxen: <em>weniger Anrufe, mehr Zeit am Tresen.</em>',
 sub='Viele Anrufe brauchen keine Entscheidung – nur eine Antwort oder eine vollständige Anfrage. Unser digitaler Assistent erledigt das im Chat, per WhatsApp und über die Online-Terminbuchung, rund um die Uhr und in mehreren Sprachen. Ihr Team bekommt alles sortiert und entscheidet selbst.',
 trust='Chat · WhatsApp · Online-Termine · E-Mails · Keine medizinische Beratung',
 usp=['Mehrsprachig', 'Team gibt frei', 'AV-Vertrag & § 203', 'EU-Hosting'],
 wa='Hallo, ich interessiere mich für einen digitalen Assistenten für unsere Praxis.',
 angles_ey='Worum es geht', angles_h2='Nicht die Menge – <em>die Unterbrechung</em>',
 angles_sub='Das Telefon klingelt, während jemand am Tresen steht. Ein großer Teil davon ließe sich auch schriftlich erledigen.',
 angles=[
  ('Weniger Unterbrechungen', 'Terminverschiebung, Öffnungszeiten, Folgerezept: Wer schreiben kann, muss nicht anrufen – und Ihr Team telefoniert seltener mitten in der Arbeit.'),
  ('Rund um die Uhr erreichbar', 'Viele Patienten erledigen so etwas lieber abends. Der Assistent nimmt das Anliegen auf, die Praxis bearbeitet es am nächsten Morgen.'),
  ('In der Sprache Ihrer Patienten', 'Anliegen auf Türkisch, Arabisch, Englisch oder anderen Sprachen werden aufgenommen und für Ihr Team auf Deutsch zusammengefasst.'),
  ('Vollständig statt Rückrufzettel', 'Jedes Anliegen kommt mit allen nötigen Angaben an – sortiert in einer Liste, nicht verteilt auf Zettel und Mailbox.'),
 ],
 tab_h2='Was der Assistent <em>übernimmt – und was nicht</em>', tab_sub='Klein anfangen: meist mit dem Anliegen, das am häufigsten kommt.',
 tab_cols=['Anliegen', 'Was passiert', 'Wer entscheidet'],
 tab_rows=[
  ['Termin verschieben oder absagen', 'Wunsch wird aufgenommen, freie Zeiten werden vorgeschlagen', 'Ihr Team bestätigt'],
  ['Folgerezept oder Überweisung', 'Anfrage vollständig aufgenommen, ohne Angaben zu Beschwerden', 'Ärztin oder Arzt'],
  ['Öffnungszeiten, Urlaub, Anfahrt', 'Antwort direkt aus Ihren hinterlegten Informationen', 'steht vorher fest'],
  ['Anliegen in anderer Sprache', 'aufgenommen in der Sprache des Patienten, auf Deutsch übergeben', 'Ihr Team'],
  ['Beschwerden, Notfall', '<strong>keine Bewertung</strong> – sofortiger Hinweis auf 112 bzw. 116&nbsp;117', 'nicht der Assistent'],
 ],
 tab_note='Der Assistent ergänzt Ihre Praxissoftware und Ihre bestehenden Wege – Telefon und Tresen bleiben.',
 svc_h2='Was wir <em>für Ihre Praxis bauen</em>', svc_sub='Jeder Baustein einzeln – und nach Bedarf zusammen.',
 services=LEISTUNGEN('Patienten'),
 preis_h2='Was kostet <em>ein Praxis-Assistent?</em>',
 preis_html='''<p>Das hängt davon ab, welche Anliegen der Assistent übernehmen soll, über welche Wege (Website, WhatsApp, Online-Termine) und ob er an Ihre vorhandene Software angebunden wird. Deshalb nennen wir keinen Pauschalpreis.</p>
<p>Wir beginnen mit einem <strong>kostenlosen Erstgespräch</strong> und dem einen Anliegen, das bei Ihnen am häufigsten kommt. Danach bekommen Sie ein <strong>Festpreis-Angebot</strong> für Einrichtung und Betreuung.</p>''',
 recht_ey='Datenschutz &amp; Schweigepflicht', recht_h2='Patientendaten sind <em>keine Nebensache</em>', recht_sub=None,
 recht_html=RECHT.replace('{bereit}', ', außerhalb der Sprechzeiten an den ärztlichen Bereitschaftsdienst 116&nbsp;117').replace('{software}', 'Praxissoftware'),
 ablauf=[
  ('Erstgespräch', 'Wir klären, welches Anliegen bei Ihnen am häufigsten kommt und über welchen Weg Ihre Patienten am liebsten schreiben.'),
  ('Vorschau mit Ihren Texten', 'Sie sehen den Assistenten mit Ihren Öffnungszeiten, Abläufen und Formulierungen, bevor er live geht.'),
  ('Unterlagen & Einrichtung', 'AV-Vertrag, Verschwiegenheitsverpflichtung und Datenschutztexte – danach richten wir alles ein und weisen Ihr Team ein.'),
  ('Start & Betreuung', 'Wir begleiten die ersten Wochen, passen Antworten an und erweitern auf weitere Anliegen, wenn Sie möchten.'),
 ],
 faq_h2='KI in der Praxis – <em>Fragen &amp; Antworten</em>',
 faq=[
  ('Gibt der Assistent medizinische Auskünfte?', 'Nein. Er beantwortet organisatorische Fragen und nimmt Anliegen auf. Er stellt keine Diagnose, bewertet keine Beschwerden und verweist bei Notfällen sofort an 112 bzw. 116&nbsp;117.'),
  ('Wissen Patienten, dass sie mit einer KI schreiben?', 'Ja. Der Hinweis steht gleich zu Beginn des Gesprächs – so verlangt es die EU-KI-Verordnung seit August 2026.'),
  ('Ist das datenschutzgerecht?', 'Wir bauen es so: EU-Hosting, so wenig Daten wie möglich, AV-Vertrag und Verschwiegenheitsverpflichtung nach § 203 StGB. Die Datenschutz-Folgenabschätzung führt die Praxis durch – wir liefern die Vorlage und alle Angaben dazu.'),
  ('Geht das mit WhatsApp?', 'Ja, aber nicht über die normale App auf dem Praxis-Handy. Wir binden die WhatsApp Business Platform über einen EU-Anbieter an, nur nach Einwilligung und ohne Gesundheitsangaben in den Nachrichten.'),
  ('Ersetzt das unsere Praxissoftware?', 'Nein. Der Assistent ergänzt sie. Wo eine Schnittstelle vorhanden ist, prüfen wir die Anbindung – sonst landen die Anliegen sortiert in einer Liste für Ihr Team.'),
  ('Wie fangen wir an?', 'Mit einem kostenlosen Gespräch und einem einzigen Anliegen. Sie sehen eine Vorschau mit Ihren Texten, bevor etwas live geht.'),
 ],
 links=[('/ki-loesungen/', 'KI-Lösungen'), ('/ki-fuer-pflegedienste-berlin.html', 'KI für Pflegedienste'), ('/ki-fuer-handwerker-berlin.html', 'KI für Handwerker'), ('/blog/ki-arztpraxis-datenschutz.html', 'Ratgeber: KI in der Arztpraxis'), ('/blog/online-terminbuchung-arztpraxis.html', 'Online-Terminbuchung'), ('/blog/whatsapp-arztpraxis-datenschutz.html', 'WhatsApp in der Praxis'), ('/blog/mehrsprachige-patienten-praxis.html', 'Mehrsprachige Patienten'), ('/blog/ki-verordnung-praxis-pflege.html', 'KI-Verordnung'),
        ('/praxisbeschilderung-berlin.html', 'Praxisschild'), ('/webdesign-berlin.html', 'Webdesign')],
 form_opts=['Termine verschieben/absagen', 'Folgerezepte & Überweisungen', 'Fragen zu Öffnungszeiten', 'Mehrsprachige Patienten', 'E-Mails & Kontaktformular', 'Online-Terminbuchung'],
 form_labels=('Welches Anliegen kommt am häufigsten?', 'Ihre Praxis &amp; Ihr Wunsch', 'Datei (optional)', 'Zum Beispiel Ihre aktuellen Öffnungszeiten oder ein Aushang – bitte keine Patientendaten.'),
 form_sub='Schreiben Sie uns, welches Anliegen bei Ihnen am häufigsten kommt – wir melden uns innerhalb von 24 Stunden für ein kostenloses Gespräch.',
 subject='Anfrage KI für Arztpraxen (Website)', msg_ph='z. B. Hausarztpraxis in Berlin-Wedding, viele Anrufe wegen Folgerezepten, Patienten oft türkisch- oder arabischsprachig',
 sticky=('KI für Arztpraxen', 'Kostenloses Erstgespräch'))
PRAXIS['extra'] = demo('praxis', 'Patienten')

PFLEGE = dict(PRAXIS)
PFLEGE.update(file='ki-fuer-pflegedienste-berlin.html', crumb='KI für Pflegedienste', img='ki-pflegedienst',
 img_alt='Bildschirmfoto unseres Pflegedienst-Assistenten: Eine Krankmeldung wird früh am Morgen aufgenommen und sofort an die Einsatzleitung gegeben',
 title='KI für Pflegedienste Berlin: Krankmeldungen, Anfragen & Termine | Masar',
 desc='Digitaler Assistent für ambulante Pflegedienste in Berlin: Krankmeldungen, Angehörigen-Fragen und Neuanfragen per Chat und WhatsApp aufnehmen, E-Mails vorsortieren – Entscheidungen bleiben bei Ihnen.',
 service_type='KI-Assistent für Pflegedienste', schema_name='Digitaler Assistent für Pflegedienste in Berlin',
 badge='KI für Pflegedienste · Berlin', h1='KI-Assistent für Pflegedienste: <em>die Stunde vor der ersten Tour gehört wieder Ihnen.</em>',
 sub='Krankmeldungen, Angehörige, Neuanfragen – und dazwischen soll die Planung stehen. Unser digitaler Assistent nimmt diese Anliegen per Chat und WhatsApp auf, sortiert sie und gibt Dringendes sofort an die Einsatzleitung. Entscheiden tun weiterhin Sie.',
 trust='Ambulante Pflege · Tagespflege · Betreuungsdienste',
 usp=['Krankmeldung sofort bei der Einsatzleitung', 'Team gibt frei', 'AV-Vertrag & § 203', 'EU-Hosting'],
 wa='Hallo, ich interessiere mich für einen digitalen Assistenten für unseren Pflegedienst.',
 angles_ey='Worum es geht', angles_h2='Der Engpass sitzt <em>im Büro</em>',
 angles_sub='Pflege lässt sich nicht automatisieren. Das Aufnehmen, Einsortieren und Weitergeben drumherum zu großen Teilen schon.',
 angles=[
  ('Krankmeldung um sechs', 'Mitarbeiter melden sich per Chat oder WhatsApp krank – die Einsatzleitung hat sofort alle Angaben, statt eine Stunde zu telefonieren.'),
  ('Angehörige gut informiert', 'Fragen zu Besuchszeiten oder Änderungen werden aufgenommen und sortiert. Die Antwort gibt das Büro – aber ohne ständiges Telefonklingeln.'),
  ('Keine Neuanfrage geht verloren', 'Wer Pflege sucht, kann jederzeit schreiben. Bezirk und Pflegegrad-Status sind erfasst, bevor die PDL zurückruft.'),
  ('Ordnung im Postfach', 'Kassen-Rückfragen, Bewerbungen, Arztpraxen: E-Mails werden vorsortiert und mit Antwortentwurf vorgelegt.'),
 ],
 tab_h2='Was der Assistent <em>übernimmt – und was nicht</em>', tab_sub='Wir starten mit dem Punkt, der Ihr Büro am meisten bindet.',
 tab_rows=[
  ['Krankmeldung von Mitarbeitern', 'Zeitraum und betroffene Tour werden aufgenommen, Einsatzleitung sofort benachrichtigt', 'Einsatzleitung plant um'],
  ['Fragen von Angehörigen', 'Anliegen aufgenommen und sortiert, Rückmeldung zugesagt', 'Büro / PDL antwortet'],
  ['Neuanfrage Pflege', 'Bezirk, für wen, Pflegegrad-Status erfasst', 'PDL prüft Kapazität'],
  ['E-Mails von Kassen und Praxen', 'vorsortiert, Antwortentwurf vorbereitet', 'Ihr Team gibt frei'],
  ['Notfall beim Patienten', '<strong>keine Bewertung</strong> – sofortiger Hinweis auf 112', 'nicht der Assistent'],
 ],
 tab_note='Der Assistent ergänzt Ihre Pflegesoftware und die Telematikinfrastruktur – er ersetzt sie nicht.',
 services=LEISTUNGEN('Angehörige und Interessenten'),
 preis_h2='Was kostet <em>ein Assistent für den Pflegedienst?</em>',
 preis_html=PRAXIS['preis_html'].replace('Website, WhatsApp, Online-Termine', 'Website, WhatsApp, E-Mail').replace('Ihre vorhandene Software', 'Ihre Pflegesoftware').replace('das bei Ihnen am häufigsten kommt', 'das Ihr Büro am meisten bindet'),
 recht_h2='Pflegedaten sind <em>besonders geschützt</em>',
 recht_html=RECHT.replace('{bereit}', '').replace('{software}', 'Pflegesoftware'),
 ablauf=[
  ('Erstgespräch', 'Wir klären, was Ihr Büro am meisten bindet – Krankmeldungen, Angehörige, Neuanfragen oder das Postfach.'),
  ('Vorschau mit Ihren Abläufen', 'Sie sehen den Assistenten mit Ihren Texten und Zuständigkeiten, bevor er live geht.'),
  ('Unterlagen & Einrichtung', 'AV-Vertrag, Verschwiegenheitsverpflichtung und Datenschutztexte – danach richten wir alles ein und weisen Ihr Team ein.'),
  ('Start & Betreuung', 'Wir begleiten die ersten Wochen und erweitern auf weitere Anliegen, wenn Sie möchten.'),
 ],
 faq_h2='KI im Pflegedienst – <em>Fragen &amp; Antworten</em>',
 faq=[
  ('Plant der Assistent die Touren?', 'Nein. Er nimmt Krankmeldungen und Anliegen auf und informiert sofort die richtige Person. Die Umplanung entscheidet weiterhin Ihre Einsatzleitung.'),
  ('Gibt er pflegerische oder medizinische Auskünfte?', 'Nein. Er beantwortet organisatorische Fragen, nimmt Anliegen auf und verweist im Notfall sofort an 112.'),
  ('Wissen Angehörige, dass sie mit einer KI schreiben?', 'Ja. Der Hinweis steht gleich zu Beginn des Gesprächs – so verlangt es die EU-KI-Verordnung seit August 2026.'),
  ('Ist das datenschutzgerecht?', 'Wir bauen es so: EU-Hosting, so wenig Daten wie möglich, AV-Vertrag und Verschwiegenheitsverpflichtung nach § 203 StGB. Die Datenschutz-Folgenabschätzung führt der Pflegedienst durch – wir liefern die Vorlage und alle Angaben.'),
  ('Können Mitarbeiter sich per WhatsApp krankmelden?', 'Ja, über die WhatsApp Business Platform mit EU-Anbieter und Einwilligung – nicht über ein privates Handy. Die offizielle Krankmeldung reichen Mitarbeiter wie gewohnt nach.'),
  ('Ersetzt das unsere Pflegesoftware?', 'Nein. Der Assistent ergänzt sie. Wo eine Schnittstelle vorhanden ist, prüfen wir die Anbindung.'),
 ],
 links=[('/ki-loesungen/', 'KI-Lösungen'), ('/ki-fuer-arztpraxen-berlin.html', 'KI für Arztpraxen'), ('/ki-fuer-handwerker-berlin.html', 'KI für Handwerker'), ('/blog/krankmeldung-pflegedienst-digital.html', 'Ratgeber: Krankmeldungen digital aufnehmen'), ('/blog/ki-pflegedienst-dokumentation.html', 'Ratgeber: KI in der Pflegedokumentation'), ('/blog/angehoerige-kommunikation-pflegedienst.html', 'Angehörige im Pflegedienst'), ('/blog/postfach-pflegedienst-ordnen.html', 'Postfach ordnen'), ('/blog/ki-verordnung-praxis-pflege.html', 'KI-Verordnung'),
        ('/werbung-pflegedienst-berlin.html', 'Werbung für Pflegedienste'), ('/webdesign-berlin.html', 'Webdesign')],
 form_opts=['Krankmeldungen', 'Fragen von Angehörigen', 'Neuanfragen', 'E-Mails & Postfach', 'Interne Unterlagen'],
 form_labels=('Was bindet Ihr Büro am meisten?', 'Ihr Dienst &amp; Ihr Wunsch', 'Datei (optional)', 'Zum Beispiel ein Ablauf oder Aushang – bitte keine Patientendaten.'),
 form_sub='Schreiben Sie uns, was Ihr Büro am meisten bindet – wir melden uns innerhalb von 24 Stunden für ein kostenloses Gespräch.',
 subject='Anfrage KI für Pflegedienste (Website)', msg_ph='z. B. ambulanter Pflegedienst in Berlin-Reinickendorf, 25 Mitarbeiter, Krankmeldungen morgens per Telefon',
 sticky=('KI für Pflegedienste', 'Kostenloses Erstgespräch'))
PFLEGE['extra'] = demo('pflege', 'Angehörigen und Ihr Team')


RECHT_FIRMA = '''<p><strong>Klarer KI-Hinweis:</strong> Wer mit dem Assistenten schreibt, erfährt gleich zu Beginn, dass es ein digitaler Assistent ist – so verlangt es die EU-KI-Verordnung (Art.&nbsp;50) seit dem 2.&nbsp;August&nbsp;2026.</p>
<p><strong>Das Angebot schreiben Sie:</strong> Der Assistent nimmt die Anfrage auf und nennt höchstens die Preisrahmen, die Sie ihm vorgeben. Verbindliche Angebote und Zusagen gibt weiterhin Ihr Betrieb.</p>
<p><strong>So wenig Daten wie möglich:</strong> Abgefragt wird nur, was Sie für ein Angebot brauchen. Feste Löschfristen, Hosting und KI-Modell in der EU.</p>
<p><strong>Vertraglich sauber:</strong> Wir arbeiten als Auftragsverarbeiter mit AV-Vertrag nach Art.&nbsp;28 DSGVO und liefern die Texte für Ihre Datenschutzerklärung.</p>
<p><strong>WhatsApp nur richtig angebunden:</strong> Nicht über die normale App auf dem Firmenhandy, sondern über die WhatsApp Business Platform mit EU-Anbieter und nur nach Einwilligung. Ein anderer Weg (E-Mail oder Formular) bleibt immer möglich.</p>
<p style="font-size:13px;">Allgemeine Hinweise, keine Rechtsberatung. Grundlagen: <a href="https://eur-lex.europa.eu/eli/reg/2024/1689/oj" target="_blank" rel="noopener noreferrer">KI-Verordnung (EU) 2024/1689</a>, <a href="https://eur-lex.europa.eu/eli/reg/2016/679/oj" target="_blank" rel="noopener noreferrer">DSGVO</a>.</p>'''

HANDWERK = dict(PRAXIS)
HANDWERK.update(file='ki-fuer-handwerker-berlin.html', crumb='KI für Handwerker', img='ki-handwerk',
 img_alt='Bildschirmfoto unseres Anfrage-Assistenten: Eine Anfrage für einen Malerbetrieb wird im Chat vollständig aufgenommen',
 title='KI für Handwerker Berlin: Anfragen & Termine automatisch | Masar',
 desc='Digitaler Assistent für Handwerksbetriebe und kleine Firmen in Berlin: Anfragen vollständig aufnehmen, Besichtigungstermine online buchen, Nachricht aufs Handy – das Angebot schreiben weiterhin Sie.',
 service_type='KI-Assistent für Handwerksbetriebe', schema_name='Digitaler Anfrage-Assistent für Handwerksbetriebe in Berlin',
 badge='KI für Handwerker · Berlin', h1='KI-Assistent für Handwerker: <em>keine Anfrage geht mehr verloren.</em>',
 sub='Sie stehen auf der Baustelle, das Telefon klingelt, und abends fehlen bei jeder Anfrage die halben Angaben. Unser digitaler Assistent nimmt Anfragen auf Ihrer Website und per WhatsApp vollständig auf, bucht Besichtigungstermine und schickt Ihnen eine Nachricht aufs Handy. Das Angebot schreiben weiterhin Sie.',
 trust='Maler · Elektro · Sanitär · Kfz-Werkstatt · Reinigung · Hausverwaltung',
 usp=['Anfragen auch abends', 'Termine ohne Telefon', 'Nachricht aufs Handy', 'EU-Hosting'],
 wa='Hallo, ich interessiere mich für einen digitalen Anfrage-Assistenten für unseren Betrieb.',
 angles_ey='Worum es geht', angles_h2='Die Anfrage kommt, <em>wenn Sie keine Hand frei haben</em>',
 angles_sub='Kunden schreiben abends und am Wochenende. Wer dann nur eine Mailbox erreicht, fragt beim nächsten Betrieb.',
 angles=[
  ('Vollständig statt „Rufen Sie mich an“', 'Leistung, Umfang, Ort, Wunschtermin und Fotos kommen in einer Anfrage an – nicht verteilt auf Mailbox, WhatsApp und Zettel.'),
  ('Auch abends und am Wochenende', 'Der Assistent nimmt die Anfrage auf, wenn der Kunde Zeit hat. Sie bearbeiten sie, wenn Sie Zeit haben.'),
  ('Besichtigung ohne Telefon-Pingpong', 'Kunden wählen einen freien Termin aus Ihrem Kalender und bekommen Bestätigung und Erinnerung.'),
  ('In der Sprache Ihrer Kunden', 'Anfragen auf Türkisch, Arabisch oder Englisch werden aufgenommen und für Sie auf Deutsch zusammengefasst.'),
 ],
 tab_h2='Was der Assistent <em>übernimmt – und was nicht</em>', tab_sub='Klein anfangen: meist mit der Anfrage, die am häufigsten kommt.',
 tab_rows=[
  ['Neue Anfrage', 'Leistung, Umfang, Ort, Zeitraum und Fotos werden abgefragt', 'Sie schreiben das Angebot'],
  ['Besichtigungstermin', 'Kunde wählt eine freie Zeit, Bestätigung und Erinnerung gehen raus', 'Ihr Kalender gibt die Zeiten vor'],
  ['„Was kostet das ungefähr?“', 'nennt nur die Preisrahmen, die Sie hinterlegt haben', 'Sie legen die Rahmen fest'],
  ['Stand der Anfrage', 'Kunde sieht mit Nummer und Telefon den aktuellen Stand', 'Sie setzen den Status'],
  ['Reklamation, Sonderfall', 'wird aufgenommen und <strong>sofort an Sie</strong> weitergegeben', 'nicht der Assistent'],
 ],
 tab_note='Der Assistent ergänzt Telefon und persönlichen Kontakt – er ersetzt sie nicht.',
 svc_h2='Was wir <em>für Ihren Betrieb bauen</em>', svc_sub='Jeder Baustein einzeln – und nach Bedarf zusammen.',
 services=[
  ('web', 'Anfrage-Assistent auf der Website', 'Führt Kunden Schritt für Schritt zu einer vollständigen Anfrage – mit Anfragenummer statt loser Nachricht.', '#demo'),
  ('phone', 'WhatsApp-Assistent', 'Für alle, die lieber schreiben: über die WhatsApp Business Platform, mit Einwilligung und EU-Anbieter.', '#datenschutz'),
  ('karte', 'Online-Termine & Erinnerungen', 'Kunden wählen freie Zeiten selbst, bekommen eine Bestätigung und eine Erinnerung vor dem Termin.', '#bausteine'),
  ('druck', 'E-Mails vorsortieren', 'Eingehende Nachrichten werden gelesen, eingeordnet und mit einem Antwortentwurf versehen, den Sie freigeben.', '#bausteine'),
  ('auge', 'Status-Seite für Kunden', 'Kunden sehen den Stand ihrer Anfrage selbst – weniger Rückfragen am Telefon.', '/status.html'),
  ('stern', 'Website, Schild & Fahrzeug', 'Auf Wunsch die passende Website, das Firmenschild und die Fahrzeugbeschriftung dazu – alles aus einer Hand.', '/fahrzeugbeschriftung-berlin.html'),
 ],
 preis_h2='Was kostet <em>ein Anfrage-Assistent?</em>',
 preis_html='''<p>Das hängt davon ab, welche Anfragen der Assistent aufnehmen soll, über welche Wege (Website, WhatsApp, Online-Termine) und ob Ihre vorhandene Website weiter genutzt wird. Deshalb nennen wir keinen Pauschalpreis.</p>
<p>Wir beginnen mit einem <strong>kostenlosen Erstgespräch</strong> und der einen Anfrage, die bei Ihnen am häufigsten kommt. Danach bekommen Sie ein <strong>Festpreis-Angebot</strong> für Einrichtung und Betreuung.</p>''',
 recht_ey='Datenschutz &amp; KI-Hinweis', recht_h2='Kundendaten <em>bleiben in der EU</em>', recht_sub=None,
 recht_html=RECHT_FIRMA,
 ablauf=[
  ('Erstgespräch', 'Wir klären, welche Anfrage bei Ihnen am häufigsten kommt und welche Angaben Sie für ein Angebot brauchen.'),
  ('Vorschau mit Ihren Leistungen', 'Sie sehen den Assistenten mit Ihren Leistungen, Fragen und Zeiten, bevor er live geht.'),
  ('Einrichtung', 'AV-Vertrag und Datenschutztexte – danach binden wir den Assistenten in Ihre Website ein und richten die Nachrichten aufs Handy ein.'),
  ('Start & Betreuung', 'Wir begleiten die ersten Wochen, passen Fragen an und erweitern auf weitere Leistungen, wenn Sie möchten.'),
 ],
 faq_h2='KI im Handwerk – <em>Fragen &amp; Antworten</em>',
 faq=[
  ('Schreibt der Assistent Angebote?', 'Nein. Er nimmt die Anfrage vollständig auf und nennt höchstens die Preisrahmen, die Sie hinterlegt haben. Das verbindliche Angebot schreiben Sie.'),
  ('Wissen Kunden, dass sie mit einer KI schreiben?', 'Ja. Der Hinweis steht gleich zu Beginn des Gesprächs – so verlangt es die EU-KI-Verordnung seit August 2026.'),
  ('Brauche ich dafür eine neue Website?', 'Nein. Der Assistent lässt sich in eine bestehende Website einbinden. Wenn Sie noch keine haben, bauen wir sie mit.'),
  ('Wie erfahre ich von einer neuen Anfrage?', 'Als Nachricht aufs Handy und in einer Übersicht mit Anfragenummer und Status. In der Handy-Nachricht stehen keine personenbezogenen Daten.'),
  ('Kann der Assistent telefonieren?', 'Nein. Wir bieten Chat, WhatsApp, Online-Termine und das Vorsortieren von E-Mails an – keine Telefon- oder Sprach-KI.'),
  ('Wie fangen wir an?', 'Mit einem kostenlosen Gespräch und einer einzigen Anfrageart. Sie sehen eine Vorschau mit Ihren Leistungen, bevor etwas live geht.'),
 ],
 links=[('/ki-loesungen/', 'KI-Lösungen'), ('/ki-fuer-arztpraxen-berlin.html', 'KI für Arztpraxen'), ('/ki-fuer-pflegedienste-berlin.html', 'KI für Pflegedienste'), ('/blog/werbung-handwerker.html', 'Ratgeber: Werbung für Handwerker'),
        ('/fahrzeugbeschriftung-berlin.html', 'Fahrzeugbeschriftung'), ('/schilder-berlin.html', 'Firmenschild'), ('/webdesign-berlin.html', 'Webdesign')],
 form_opts=['Anfragen auf der Website', 'WhatsApp-Assistent', 'Online-Terminbuchung', 'E-Mails & Postfach', 'Status-Seite für Kunden'],
 form_labels=('Was soll der Assistent übernehmen?', 'Ihr Betrieb &amp; Ihr Wunsch', 'Datei (optional)', 'Zum Beispiel Ihre Leistungsliste oder ein Foto Ihres Anfrageformulars – bitte keine Kundendaten.'),
 form_sub='Schreiben Sie uns, welche Anfrage bei Ihnen am häufigsten kommt – wir melden uns innerhalb von 24 Stunden für ein kostenloses Gespräch.',
 subject='Anfrage KI für Handwerker (Website)', msg_ph='z. B. Malerbetrieb in Berlin-Reinickendorf, 6 Mitarbeiter, Anfragen kommen abends per WhatsApp und Mailbox',
 sticky=('KI für Handwerker', 'Kostenloses Erstgespräch'))
HANDWERK['extra'] = demo('firma', 'Kunden und Ihr Büro')


def nachbearbeiten(p):
    f = ROOT + p['file']; h = open(f, encoding='utf-8').read()
    # Demo-Abschnitt mit Anker, eigenes System vor „Passend dazu“, Recht-Abschnitt mit Anker, Skript
    for text, sid in (('Weitere Bausteine</span>', 'bausteine'), ('Datenschutz &amp; Schweigepflicht</span>', 'datenschutz'), ('Datenschutz &amp; KI-Hinweis</span>', 'datenschutz')):
        i = h.find(text)
        if i > 0 and f'id="{sid}"' not in h:
            j = h.rfind('<section ', 0, i); k = h.index('>', j)
            tag = h[j:k]
            tag = re.sub(r' id="[^"]*"', '', tag) + f' id="{sid}"'
            h = h[:j] + tag + h[k:]
    anker = '<section class="section bg-alt" style="padding:2.5rem 0;">'
    if 'id="eigenes-system"' not in h and anker in h:
        h = h.replace(anker, EIGEN + anker, 1)
    # Chatbot-Generator (Versuch): nur auf der Handwerker-Seite; bleibt unsichtbar, bis der Server ihn freigibt
    if 'handwerker' in p['file'] and 'data-ki-generator' not in h:
        h = h.replace('<section class="section" id="eigenes-system">', GENERATOR + '<section class="section" id="eigenes-system">', 1)
        h = h.replace('</body>', '<script src="/ki-generator.js?v=1" defer></script>\n</body>', 1)
    # Hero: Live-Demo statt Standbild
    art = 'pflege' if 'pflege' in p['file'] else 'handwerk' if 'handwerker' in p['file'] else 'praxis'
    h = re.sub(r'(<div class="hero-visual">)\s*<img class="hero-shot"[^>]*>', lambda m: m.group(1) + f'\n        <div class="hero-demo" id="demo" data-ki-demo="{art}"></div>', h, count=1)
    if '<style id="ki-hero">' not in h:
        h = h.replace('</head>', '<style id="ki-hero">.hero-demo{color:rgba(255,255,255,.85)}.hero-visual .hero-demo .kd{max-width:380px}.hero-visual>.hero-demo{max-width:380px!important}@media(max-width:900px){.hero-visual .kd-in{height:500px}}@media(max-width:420px){.hero-visual .kd-in{height:470px}.kd-w{max-height:104px}}</style>\n</head>', 1)
    h = h.replace('Foto per WhatsApp schicken', 'Per WhatsApp schreiben').replace('<a href="#kontakt" class="btn btn-teal">Angebot anfordern</a>', '<a href="#kontakt" class="btn btn-teal">Erstgespräch anfragen</a>', 1)
    if '/ki-demo.js' not in h:
        h = h.replace('</body>', '<script src="/ki-demo.js?v=4" defer></script>\n</body>', 1)
    open(f, 'w', encoding='utf-8').write(h)


if __name__ == '__main__':
    for p in (PRAXIS, PFLEGE, HANDWERK):
        print(build_f(p)); nachbearbeiten(p)
