"""KI für Arztpraxen / KI für Pflegedienste (Generator: gen_folien.build_f).
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
    <div class="why-grid">
      <div class="why-item"><div class="why-num">1</div><div><h3>Anfrage-Assistent</h3><p>Führt Kunden Schritt für Schritt zu einer vollständigen Anfrage – mit Anfragenummer statt loser Nachricht. <a href="/#kontakt">Ausprobieren →</a></p></div></div>
      <div class="why-item"><div class="why-num">2</div><div><h3>Online-Terminbuchung</h3><p>Freie Zeiten, Feiertage gesperrt, Bestätigung sofort und Erinnerung etwa 24 Stunden vorher per E-Mail. <a href="/termin.html">Termin ansehen →</a></p></div></div>
      <div class="why-item"><div class="why-num">3</div><div><h3>Status-Seite</h3><p>Kunden sehen mit Nummer und Telefon den Stand ihrer Anfrage und können einen Termin verschieben oder absagen lassen. <a href="/status.html">Status-Seite →</a></p></div></div>
      <div class="why-item"><div class="why-num">4</div><div><h3>Digitaler Sekretär</h3><p>Neue Anfragen, Erinnerung vor jedem Termin und ein Tagesbericht kommen als Nachricht aufs Handy – ohne personenbezogene Daten in der Nachricht.</p></div></div>
    </div>
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
 badge='KI für Arztpraxen · Berlin', h1='Weniger Anrufe. <em>Mehr Zeit am Tresen.</em>',
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
 links=[('/ki-loesungen/', 'KI-Lösungen'), ('/ki-fuer-pflegedienste-berlin.html', 'KI für Pflegedienste'), ('/blog/ki-arztpraxis-datenschutz.html', 'Ratgeber: KI in der Arztpraxis'), ('/blog/online-terminbuchung-arztpraxis.html', 'Online-Terminbuchung'), ('/blog/whatsapp-arztpraxis-datenschutz.html', 'WhatsApp in der Praxis'), ('/blog/mehrsprachige-patienten-praxis.html', 'Mehrsprachige Patienten'), ('/blog/ki-verordnung-praxis-pflege.html', 'KI-Verordnung'),
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
 badge='KI für Pflegedienste · Berlin', h1='Die Stunde vor der ersten Tour <em>gehört wieder Ihnen.</em>',
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
 links=[('/ki-loesungen/', 'KI-Lösungen'), ('/ki-fuer-arztpraxen-berlin.html', 'KI für Arztpraxen'), ('/blog/krankmeldung-pflegedienst-digital.html', 'Ratgeber: Krankmeldungen digital aufnehmen'), ('/blog/ki-pflegedienst-dokumentation.html', 'Ratgeber: KI in der Pflegedokumentation'), ('/blog/angehoerige-kommunikation-pflegedienst.html', 'Angehörige im Pflegedienst'), ('/blog/postfach-pflegedienst-ordnen.html', 'Postfach ordnen'), ('/blog/ki-verordnung-praxis-pflege.html', 'KI-Verordnung'),
        ('/werbung-pflegedienst-berlin.html', 'Werbung für Pflegedienste'), ('/webdesign-berlin.html', 'Webdesign')],
 form_opts=['Krankmeldungen', 'Fragen von Angehörigen', 'Neuanfragen', 'E-Mails & Postfach', 'Interne Unterlagen'],
 form_labels=('Was bindet Ihr Büro am meisten?', 'Ihr Dienst &amp; Ihr Wunsch', 'Datei (optional)', 'Zum Beispiel ein Ablauf oder Aushang – bitte keine Patientendaten.'),
 form_sub='Schreiben Sie uns, was Ihr Büro am meisten bindet – wir melden uns innerhalb von 24 Stunden für ein kostenloses Gespräch.',
 subject='Anfrage KI für Pflegedienste (Website)', msg_ph='z. B. ambulanter Pflegedienst in Berlin-Reinickendorf, 25 Mitarbeiter, Krankmeldungen morgens per Telefon',
 sticky=('KI für Pflegedienste', 'Kostenloses Erstgespräch'))
PFLEGE['extra'] = demo('pflege', 'Angehörigen und Ihr Team')


def nachbearbeiten(p):
    f = ROOT + p['file']; h = open(f, encoding='utf-8').read()
    # Demo-Abschnitt mit Anker, eigenes System vor „Passend dazu“, Recht-Abschnitt mit Anker, Skript
    for text, sid in (('Weitere Bausteine</span>', 'bausteine'), ('Datenschutz &amp; Schweigepflicht</span>', 'datenschutz')):
        i = h.find(text)
        if i > 0 and f'id="{sid}"' not in h:
            j = h.rfind('<section ', 0, i); k = h.index('>', j)
            tag = h[j:k]
            tag = re.sub(r' id="[^"]*"', '', tag) + f' id="{sid}"'
            h = h[:j] + tag + h[k:]
    anker = '<section class="section bg-alt" style="padding:2.5rem 0;">'
    if 'id="eigenes-system"' not in h and anker in h:
        h = h.replace(anker, EIGEN + anker, 1)
    # Hero: Live-Demo statt Standbild
    art = 'pflege' if 'pflege' in p['file'] else 'praxis'
    h = re.sub(r'(<div class="hero-visual">)\s*<img class="hero-shot"[^>]*>', lambda m: m.group(1) + f'\n        <div class="hero-demo" id="demo" data-ki-demo="{art}"></div>', h, count=1)
    if '<style id="ki-hero">' not in h:
        h = h.replace('</head>', '<style id="ki-hero">.hero-demo{color:rgba(255,255,255,.85)}.hero-visual .hero-demo .kd{max-width:380px}.hero-visual>.hero-demo{max-width:380px!important}@media(max-width:900px){.hero-visual .kd-in{height:500px}}@media(max-width:420px){.hero-visual .kd-in{height:470px}.kd-w{max-height:104px}}</style>\n</head>', 1)
    h = h.replace('Foto per WhatsApp schicken', 'Per WhatsApp schreiben').replace('<a href="#kontakt" class="btn btn-teal">Angebot anfordern</a>', '<a href="#kontakt" class="btn btn-teal">Erstgespräch anfragen</a>', 1)
    if '/ki-demo.js' not in h:
        h = h.replace('</body>', '<script src="/ki-demo.js?v=3" defer></script>\n</body>', 1)
    open(f, 'w', encoding='utf-8').write(h)


if __name__ == '__main__':
    for p in (PRAXIS, PFLEGE):
        print(build_f(p)); nachbearbeiten(p)
