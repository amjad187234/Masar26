"""Ratgeber Krankmeldungen im Pflegedienst (Praxis-Thema steht schon in blog/ki-arztpraxis-datenschutz.html) (03.11.2026). Vorlage: blog/fotowand-firmenfeier.html.
Rechtliche Aussagen aus der Recherche vom 03.11.2026 (privat: tools/angebot/privat/marketing/KI_Recht_Memo_2026-11-03.md),
ohne Zeitersparnis-Zahlen, ohne „rechtssicher“. Aufruf: python3 tools/blog/ki_artikel.py
"""
import os, re, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
VORLAGE = open(os.path.join(ROOT, 'blog', 'fotowand-firmenfeier.html'), encoding='utf-8').read()
BASE = 'https://masar-werbeagentur.de/'

QUELLEN_RECHT = [
    ('https://eur-lex.europa.eu/eli/reg/2024/1689/oj', 'Verordnung (EU) 2024/1689 (KI-Verordnung), Art. 50'),
    ('https://eur-lex.europa.eu/eli/reg/2016/679/oj', 'Verordnung (EU) 2016/679 (DSGVO), Art. 9, 28, 35'),
    ('https://www.gesetze-im-internet.de/stgb/__203.html', '§ 203 StGB – Verletzung von Privatgeheimnissen'),
    ('https://www.gesetze-im-internet.de/bdsg_2018/__22.html', '§ 22 BDSG – Verarbeitung besonderer Kategorien'),
]

ARTIKEL = [
 dict(file='krankmeldung-pflegedienst-digital.html', crumb='Krankmeldung Pflegedienst',
  title='Krankmeldungen im Pflegedienst digital aufnehmen',
  desc='Krankmeldung um sechs Uhr, Tour um sieben: Wie ambulante Pflegedienste Krankmeldungen per Chat oder WhatsApp aufnehmen – schnell, vollständig und datenschutzgerecht.',
  tag='Ratgeber · KI &amp; Pflege', h1='Krankmeldungen im Pflegedienst:<br><em>schneller bei der Einsatzleitung.</em>', minuten=5,
  bild=('/ki-pflegedienst', 'Bildschirmfoto eines Pflegedienst-Assistenten: Krankmeldung wird aufgenommen und an die Einsatzleitung gegeben', 'Eine Krankmeldung im Chat: Mitarbeiter schreiben, die Einsatzleitung bekommt alle Angaben auf einen Blick.'),
  intro='<p>In vielen ambulanten Diensten beginnt der Tag mit dem Telefon: Jemand ist krank, die erste Tour startet bald, und die Einsatzleitung muss umplanen. Das Problem ist selten die Krankmeldung selbst – sondern dass sie unvollständig, spät oder auf dem falschen Weg ankommt. So lässt sich das digital ordnen.</p>',
  body='''
    <h2>Was eine gute Krankmeldung enthält</h2>
    <p>Für die Umplanung braucht die Einsatzleitung nur wenige Angaben – aber alle auf einmal:</p>
    <ul>
      <li>wer ausfällt und ab wann,</li>
      <li>voraussichtlich bis wann,</li>
      <li>welche Tour oder welche Einsätze betroffen sind,</li>
      <li>ob die Krankmeldung (AU) nachgereicht wird.</li>
    </ul>
    <p>Eine Diagnose gehört <strong>nicht</strong> dazu. Je weniger Gesundheitsangaben ein System erfasst, desto besser.</p>

    <h2>Warum per Chat statt Anruf?</h2>
    <p>Ein Anruf um 5:45 Uhr erreicht oft niemanden, eine Sprachnachricht wird überhört, ein Zettel liegt im falschen Fach. Ein digitaler Assistent nimmt die Meldung jederzeit auf, fragt die fehlenden Angaben nach und informiert sofort die Einsatzleitung. Die Entscheidung, wer übernimmt, trifft weiterhin ein Mensch.</p>

    <h2>WhatsApp für Mitarbeiter – aber nicht privat</h2>
    <p>Viele Teams melden sich ohnehin per WhatsApp. Aus Datenschutzsicht sollte das nicht über private Handys und die normale App laufen. Besser ist die <strong>WhatsApp Business Platform</strong> über einen Anbieter mit EU-Hosting und Auftragsverarbeitungsvertrag – mit Einwilligung der Mitarbeiter und ohne Gesundheitsangaben in der Nachricht.</p>

    <h2>Auch für Angehörige und Neuanfragen</h2>
    <p>Dieselbe Technik hilft im Büro: Fragen von Angehörigen werden aufgenommen und sortiert, Neuanfragen kommen mit Bezirk und Pflegegrad-Status an. Wichtig ist der klare Hinweis, dass ein digitaler Assistent antwortet – das verlangt die EU-KI-Verordnung seit August 2026 – und dass er im Notfall sofort auf <strong>112</strong> verweist.</p>

    <h2>Was der Pflegedienst vertraglich braucht</h2>
    <p>Pflegekräfte unterliegen der Schweigepflicht nach <strong>§&nbsp;203 StGB</strong>. Ein externer Dienstleister muss deshalb eine Verschwiegenheitsverpflichtung unterschreiben – zusätzlich zum <strong>Auftragsverarbeitungsvertrag</strong> nach Art.&nbsp;28 DSGVO. Der Assistent ergänzt Pflegesoftware und Telematikinfrastruktur, er ersetzt sie nicht.</p>

    <h2>So fangen Sie an</h2>
    <ol>
      <li>Festlegen, welche Angaben eine Krankmeldung braucht – und wer sie bekommt.</li>
      <li>Einen Weg wählen: Chat auf der Website, WhatsApp Business Platform oder beides.</li>
      <li>AV-Vertrag und Verschwiegenheitsverpflichtung mit dem Dienstleister abschließen.</li>
      <li>Team informieren: Die offizielle Krankmeldung bleibt wie gewohnt.</li>
      <li>Nach vier Wochen gemeinsam prüfen, was gut läuft und was fehlt.</li>
    </ol>''',
  cta=('Digitaler Assistent für Ihren Pflegedienst', 'Probieren Sie unsere Demo aus oder schreiben Sie uns, was Ihr Büro am meisten bindet.', '/ki-fuer-pflegedienste-berlin.html#demo', 'Demo ansehen', 'Hallo, ich interessiere mich für einen digitalen Assistenten für unseren Pflegedienst.', 'KI für den Pflegedienst'),
  weiter=[('/ki-fuer-pflegedienste-berlin.html', 'KI für Pflegedienste'), ('/werbung-pflegedienst-berlin.html', 'Werbung für Pflegedienste'), ('/ki-loesungen/', 'KI-Lösungen')],
  quellen=QUELLEN_RECHT,
  related=[('/blog/ki-pflegedienst-dokumentation.html', 'KI in der Pflegedokumentation', 'Wer haftet und was ein System sinnvoll übernehmen kann.'),
           ('/blog/ki-arztpraxis-datenschutz.html', 'KI in der Arztpraxis', 'Was rechtlich geht – Datenschutz, Schweigepflicht, KI-Verordnung.')]),
]


PRAXIS_CTA = ('Digitaler Assistent für Ihre Praxis', 'Probieren Sie unsere Demo aus oder schreiben Sie uns, welches Anliegen bei Ihnen am häufigsten kommt.', '/ki-fuer-arztpraxen-berlin.html#demo', 'Demo ansehen', 'Hallo, ich interessiere mich für einen digitalen Assistenten für unsere Praxis.', 'KI für die Arztpraxis')
PFLEGE_CTA = ('Digitaler Assistent für Ihren Pflegedienst', 'Probieren Sie unsere Demo aus oder schreiben Sie uns, was Ihr Büro am meisten bindet.', '/ki-fuer-pflegedienste-berlin.html#demo', 'Demo ansehen', 'Hallo, ich interessiere mich für einen digitalen Assistenten für unseren Pflegedienst.', 'KI für den Pflegedienst')
BILD_P = ('/ki-arztpraxis', 'Bildschirmfoto eines Praxis-Assistenten mit KI-Hinweis und sortiertem Anliegen für das Team', 'So sieht ein Praxis-Assistent aus: KI-Hinweis oben, das Team bekommt das Anliegen sortiert.')
BILD_PF = ('/ki-pflegedienst', 'Bildschirmfoto eines Pflegedienst-Assistenten: Anliegen wird aufgenommen und an die zuständige Person gegeben', 'Ein Assistent für den Pflegedienst: Anliegen kommen vollständig und sortiert im Büro an.')
W_P = [('/ki-fuer-arztpraxen-berlin.html', 'KI für Arztpraxen'), ('/ki-loesungen/', 'KI-Lösungen'), ('/praxisbeschilderung-berlin.html', 'Praxisschild')]
W_PF = [('/ki-fuer-pflegedienste-berlin.html', 'KI für Pflegedienste'), ('/werbung-pflegedienst-berlin.html', 'Werbung für Pflegedienste'), ('/ki-loesungen/', 'KI-Lösungen')]
Q_DSK = ('https://www.datenschutz-bayern.de/dsbk-ent/DSK_101-SN-MessengerKH.pdf', 'Datenschutzkonferenz – Messenger-Dienste im Krankenhausbereich')
Q_116 = ('https://www.116117.de/', '116117.de – Ärztlicher Bereitschaftsdienst')

NEU = [
 dict(file='online-terminbuchung-arztpraxis.html', crumb='Online-Terminbuchung Praxis',
  title='Online-Terminbuchung für die Arztpraxis: Worauf achten?',
  desc='Online-Terminbuchung in der Arztpraxis: welche Termine online sinnvoll sind, Erinnerungen, Absagen, Notfälle und Datenschutz – mit Checkliste für den Start.',
  tag='Ratgeber · KI &amp; Praxis', h1='Online-Terminbuchung für die Praxis:<br><em>Worauf es ankommt.</em>', minuten=6, bild=BILD_P,
  intro='<p>Viele Patienten möchten ihren Termin lieber abends am Handy buchen als morgens in der Warteschleife. Für die Praxis ist das eine Chance – wenn die Buchung zu den eigenen Abläufen passt. Diese Punkte entscheiden, ob Online-Termine Ihr Team entlasten oder neue Arbeit machen.</p>',
  body='''
    <h2>Nicht jeder Termin gehört online</h2>
    <p>Gut geeignet sind planbare Termine: Kontrolltermine, Impfungen, Vorsorge, Folgetermine, Erstgespräche mit fester Dauer. Akutsprechstunde, Notfälle und Termine, bei denen die Ärztin vorher entscheiden muss, bleiben besser bei Telefon und Tresen. Legen Sie fest, welche Terminarten online freigegeben sind – und wie viele Plätze pro Tag.</p>

    <h2>Terminart per Auswahl, nicht per Freitext</h2>
    <p>Ein Feld „Grund des Besuchs“ lädt dazu ein, Beschwerden ausführlich zu beschreiben. Besser ist eine kurze Auswahl („Kontrolle“, „Impfung“, „Vorsorge“). Das hält die Daten sparsam – schon ein Terminwunsch kann nach der DSGVO ein Gesundheitsdatum sein – und Ihr Team weiß sofort, wie lange der Termin dauert.</p>

    <h2>Erinnerung und einfache Absage</h2>
    <p>Eine Erinnerung vor dem Termin hilft, dass Patienten kommen oder rechtzeitig absagen. Wichtig: Die Absage muss genauso einfach sein wie die Buchung, sonst bleibt der Platz leer. Für Erinnerungen per SMS oder WhatsApp holen Sie die Einwilligung ein; der Text nennt nur Tag und Uhrzeit, nicht die Fachrichtung oder den Grund.</p>

    <h2>Was mit Notfällen passiert</h2>
    <p>Eine Buchungsseite darf Menschen mit akuten Beschwerden nicht in einen Termin in drei Wochen schicken. Ein fester Hinweis gehört dazu: im Notfall <strong>112</strong>, außerhalb der Sprechzeiten der ärztliche Bereitschaftsdienst <strong>116&nbsp;117</strong>.</p>

    <h2>Datenschutz und Vertrag</h2>
    <p>Wer die Buchung technisch betreibt, arbeitet für Ihre Praxis als Auftragsverarbeiter: Sie brauchen einen AV-Vertrag nach Art.&nbsp;28 DSGVO und – wegen der Schweigepflicht – eine Verschwiegenheitsverpflichtung nach §&nbsp;203 StGB. Hosting in der EU und feste Löschfristen gehören dazu.</p>

    <h2>Checkliste für den Start</h2>
    <ol>
      <li>Terminarten und Online-Kontingent pro Tag festlegen.</li>
      <li>Auswahl statt Freitext, keine Fragen zu Beschwerden.</li>
      <li>Bestätigung sofort, Erinnerung vorher, Absage mit einem Klick.</li>
      <li>Notfall-Hinweis mit 112 und 116 117 sichtbar platzieren.</li>
      <li>AV-Vertrag, § 203-Verpflichtung, EU-Hosting, Löschfristen.</li>
      <li>Datenschutzerklärung der Praxis ergänzen, Team einweisen.</li>
    </ol>''',
  cta=PRAXIS_CTA, weiter=W_P, quellen=QUELLEN_RECHT + [Q_116],
  related=[('/blog/whatsapp-arztpraxis-datenschutz.html', 'WhatsApp in der Arztpraxis', 'Was erlaubt ist und wie es richtig angebunden wird.'),
           ('/blog/ki-arztpraxis-datenschutz.html', 'KI in der Arztpraxis', 'Was rechtlich geht – Datenschutz, Schweigepflicht, KI-Verordnung.')]),

 dict(file='whatsapp-arztpraxis-datenschutz.html', crumb='WhatsApp Arztpraxis',
  title='WhatsApp in der Arztpraxis: Was ist erlaubt?',
  desc='WhatsApp für Terminerinnerungen und Patientenfragen: warum die normale App problematisch ist, was die WhatsApp Business Platform ändert und welche Regeln gelten.',
  tag='Ratgeber · KI &amp; Praxis', h1='WhatsApp in der Arztpraxis:<br><em>Was erlaubt ist.</em>', minuten=5, bild=BILD_P,
  intro='<p>Patienten schreiben ohnehin per WhatsApp – also warum nicht auch der Praxis? Die Idee ist verständlich, der Weg dorthin aber nicht beliebig. Hier der Unterschied zwischen der App auf dem Praxis-Handy und einer sauberen Anbindung.</p>',
  body='''
    <h2>Das Problem mit der normalen App</h2>
    <p>Die normale WhatsApp-App (auch die Business-App auf einem Handy) gleicht das Adressbuch ab und überträgt Daten an den Mutterkonzern Meta. In einer Praxis stehen im Adressbuch aber Patienten – und schon die Tatsache, dass jemand Patient ist, ist vertraulich. Datenschutzbehörden sehen das deshalb kritisch.</p>

    <h2>Die WhatsApp Business Platform</h2>
    <p>Für Unternehmen gibt es die <strong>WhatsApp Business Platform</strong> (Cloud API). Sie läuft nicht über ein Handy mit Adressbuch, sondern über eine Schnittstelle – zum Beispiel angebunden an einen digitalen Assistenten oder Ihr Terminsystem. Zusammen mit einem Anbieter mit EU-Hosting und AV-Vertrag wird WhatsApp damit für viele Praxen vertretbar.</p>
    <p>Ehrlich gesagt bleibt ein Restrisiko: Metadaten liegen weiterhin bei Meta, ein Datentransfer in die USA ist über das EU-US-Datenschutzrahmenabkommen abgesichert. Das sollte Ihre Datenschutzinformation offen benennen.</p>

    <h2>Regeln für den Alltag</h2>
    <ul>
      <li><strong>Nur mit Einwilligung:</strong> Patienten entscheiden selbst, ob sie WhatsApp nutzen möchten.</li>
      <li><strong>Keine Gesundheitsangaben in der Nachricht:</strong> „Ihr Termin morgen um 10 Uhr“ – nicht „Ihr Termin in der Kardiologie“.</li>
      <li><strong>Keine Befunde per WhatsApp.</strong> Für den Austausch unter Fachleuten gibt es KIM und den TI-Messenger.</li>
      <li><strong>Immer eine Alternative:</strong> E-Mail, SMS oder Anruf bleiben möglich.</li>
      <li><strong>KI-Hinweis:</strong> Antwortet ein digitaler Assistent, muss das seit August 2026 gleich zu Beginn erkennbar sein.</li>
    </ul>

    <h2>Wofür WhatsApp in der Praxis gut passt</h2>
    <p>Terminerinnerungen, Bestätigung einer Terminverschiebung, Hinweise zu Urlaub und Vertretung, die Frage „Ist mein Rezept fertig?“ mit einer kurzen Antwort. Alles, was eine ärztliche Einschätzung braucht, gehört nicht in den Chat.</p>''',
  cta=PRAXIS_CTA, weiter=W_P, quellen=QUELLEN_RECHT + [Q_DSK],
  related=[('/blog/online-terminbuchung-arztpraxis.html', 'Online-Terminbuchung', 'Welche Termine online sinnvoll sind – mit Checkliste.'),
           ('/blog/mehrsprachige-patienten-praxis.html', 'Mehrsprachige Patienten', 'Wie Verständigung in Berliner Praxen leichter wird.')]),

 dict(file='mehrsprachige-patienten-praxis.html', crumb='Mehrsprachige Patienten',
  title='Mehrsprachige Patienten in der Praxis: So klappt es',
  desc='Patienten mit Türkisch, Arabisch, Englisch oder anderen Sprachen: Wie Berliner Praxen Termine, Aushänge, Website und digitale Assistenten verständlich machen.',
  tag='Ratgeber · KI &amp; Praxis', h1='Mehrsprachige Patienten:<br><em>So wird Verständigung leichter.</em>', minuten=5, bild=BILD_P,
  intro='<p>In vielen Berliner Praxen sprechen Patienten Türkisch, Arabisch, Englisch, Russisch oder Polnisch – und am Telefon wird es schnell kompliziert: Termin verwechselt, Rezept falsch verstanden, Rückruf an die falsche Nummer. Ein paar einfache Mittel helfen schon vor dem ersten Gespräch.</p>',
  body='''
    <h2>Organisatorisches mehrsprachig, Medizinisches persönlich</h2>
    <p>Öffnungszeiten, Anfahrt, was zum Termin mitzubringen ist, wie man einen Termin absagt – das lässt sich gut mehrsprachig erklären. Aufklärung, Befunde und Diagnosen gehören dagegen ins persönliche Gespräch, bei Bedarf mit qualifizierter Sprachmittlung.</p>

    <h2>Aushang und Schaufenster</h2>
    <p>Ein klarer Aushang an Tür oder Fenster in den häufigsten Sprachen Ihrer Patienten wirkt sofort: Sprechzeiten, Telefonzeiten, Hinweis auf Online-Termine. Piktogramme helfen zusätzlich. Wichtig ist eine einfache Sprache auch auf Deutsch.</p>

    <h2>Website in einfacher Sprache</h2>
    <p>Kurze Sätze, klare Überschriften, die wichtigsten Infos oben: Das hilft allen, nicht nur Menschen mit anderer Muttersprache. Eine Übersetzung der Kernseiten (Termine, Anfahrt, Notfall) ist oft wirkungsvoller als eine komplett übersetzte Website.</p>

    <h2>Digitaler Assistent in der Sprache des Patienten</h2>
    <p>Ein digitaler Assistent kann Anliegen wie „Termin verschieben“ oder „Folgerezept“ in der Sprache des Patienten aufnehmen und für Ihr Team auf Deutsch zusammenfassen. Die Antwort an den Patienten kommt wieder in seiner Sprache. So gibt es weniger Missverständnisse – und Ihr Team muss nicht jede Sprache sprechen.</p>
    <p>Dabei gilt: Der Assistent weist darauf hin, dass er eine KI ist, gibt keine medizinischen Auskünfte und verweist im Notfall an 112 bzw. 116&nbsp;117.</p>

    <h2>Kleine Schritte, große Wirkung</h2>
    <ol>
      <li>Die drei häufigsten Sprachen Ihrer Patienten notieren.</li>
      <li>Aushang mit Sprech- und Telefonzeiten in diesen Sprachen.</li>
      <li>Kernseiten der Website in einfacher Sprache, wichtigste Infos übersetzt.</li>
      <li>Terminbestätigungen in der Sprache des Patienten.</li>
      <li>Für Aufklärung und Befunde: qualifizierte Sprachmittlung.</li>
    </ol>''',
  cta=PRAXIS_CTA, weiter=W_P, quellen=QUELLEN_RECHT[:1] + [Q_116],
  related=[('/blog/whatsapp-arztpraxis-datenschutz.html', 'WhatsApp in der Arztpraxis', 'Was erlaubt ist und wie es richtig angebunden wird.'),
           ('/blog/praxisschild-regeln-kosten.html', 'Praxisschild: Regeln & Kosten', 'Was auf das Schild gehört und was es kostet.')]),

 dict(file='ki-verordnung-praxis-pflege.html', crumb='KI-Verordnung Praxis & Pflege',
  title='KI-Verordnung: Was Praxen und Pflegedienste jetzt beachten müssen',
  desc='EU-KI-Verordnung seit August 2026: KI-Hinweis im Chat, keine Triage, Rollen von Anbieter und Betreiber, KI-Kompetenz im Team – verständlich für Praxen und Pflegedienste.',
  tag='Ratgeber · KI &amp; Recht', h1='KI-Verordnung für Praxis und Pflege:<br><em>Was jetzt gilt.</em>', minuten=6, bild=BILD_P,
  intro='<p>Die EU-KI-Verordnung (Verordnung 2024/1689) gilt schrittweise. Für digitale Assistenten in Praxen und Pflegediensten ist vor allem eine Pflicht wichtig, die seit dem 2. August 2026 greift: Menschen müssen wissen, dass sie mit einer KI sprechen. Hier das Wichtigste – ohne Paragrafendschungel.</p>',
  body='''
    <h2>Der KI-Hinweis (Art. 50)</h2>
    <p>Wer mit einem KI-System chattet, muss das <strong>spätestens bei der ersten Nachricht</strong> erfahren – es sei denn, es ist ohnehin offensichtlich. Für einen Chat auf der Praxis-Website oder per WhatsApp heißt das: ein klarer, fester Satz zu Beginn, zum Beispiel „Sie schreiben mit einem digitalen Assistenten (KI). Keine medizinische Beratung – im Notfall 112.“</p>

    <h2>Kein Hochrisiko – solange keine Triage</h2>
    <p>Ein Assistent, der Termine, Rezeptanfragen und organisatorische Fragen übernimmt, zählt nach der Verordnung nicht zu den Hochrisiko-Systemen. Das ändert sich, wenn er Beschwerden einschätzt, Dringlichkeit bewertet oder Patienten sortiert – dann kann er als Medizinprodukt gelten, mit deutlich strengeren Regeln. Deshalb gehört eine solche Funktion nicht in einen Praxis- oder Pflege-Assistenten.</p>

    <h2>Wer ist wofür zuständig?</h2>
    <ul>
      <li><strong>Anbieter</strong> ist, wer das System baut und bereitstellt – er sorgt dafür, dass der KI-Hinweis technisch eingebaut ist.</li>
      <li><strong>Betreiber</strong> ist die Praxis oder der Pflegedienst – er setzt das System ein und achtet darauf, dass es wie vorgesehen genutzt wird.</li>
    </ul>

    <h2>KI-Kompetenz im Team (Art. 4)</h2>
    <p>Wer KI einsetzt, soll dafür sorgen, dass das eigene Personal ausreichend Bescheid weiß. Praktisch heißt das: eine kurze Einweisung, was der Assistent kann, was nicht, und wann ein Mensch übernimmt.</p>

    <h2>Und die DSGVO?</h2>
    <p>Die KI-Verordnung ersetzt die DSGVO nicht. Für Patienten- und Pflegedaten gelten weiterhin Art.&nbsp;9 DSGVO, ein AV-Vertrag nach Art.&nbsp;28 und die Schweigepflicht nach §&nbsp;203 StGB.</p>

    <h2>Kurz-Check</h2>
    <ol>
      <li>Steht der KI-Hinweis gleich zu Beginn jedes Gesprächs?</li>
      <li>Bewertet der Assistent keine Beschwerden und verweist im Notfall an 112?</li>
      <li>Gibt ein Mensch Antwortentwürfe und Terminvorschläge frei?</li>
      <li>Ist das Team eingewiesen?</li>
      <li>Liegen AV-Vertrag und Verschwiegenheitsverpflichtung vor?</li>
    </ol>''',
  cta=PRAXIS_CTA, weiter=W_P + [('/ki-fuer-pflegedienste-berlin.html', 'KI für Pflegedienste')], quellen=QUELLEN_RECHT,
  related=[('/blog/ki-arztpraxis-datenschutz.html', 'KI in der Arztpraxis', 'Was rechtlich geht – Datenschutz, Schweigepflicht, KI-Verordnung.'),
           ('/blog/ki-pflegedienst-dokumentation.html', 'KI in der Pflegedokumentation', 'Wer haftet und was ein System sinnvoll übernehmen kann.')]),

 dict(file='angehoerige-kommunikation-pflegedienst.html', crumb='Angehörige Pflegedienst',
  title='Kommunikation mit Angehörigen im Pflegedienst',
  desc='Angehörige rufen an, das Büro ist voll: Wie ambulante Pflegedienste Fragen von Angehörigen geordnet aufnehmen – mit Schweigepflicht, festen Wegen und digitalem Assistenten.',
  tag='Ratgeber · KI &amp; Pflege', h1='Angehörige im Pflegedienst:<br><em>gut informiert, ohne Dauertelefon.</em>', minuten=5, bild=BILD_PF,
  intro='<p>Angehörige wollen wissen, wann die Pflege kommt, ob sich etwas geändert hat und wen sie ansprechen können. Das ist verständlich – und im Büro oft der Grund, warum das Telefon nicht stillsteht. Mit klaren Wegen wird beides besser: die Information der Angehörigen und die Ruhe im Büro.</p>',
  body='''
    <h2>Erst klären: Wer darf was erfahren?</h2>
    <p>Pflegekräfte unterliegen der Schweigepflicht (§&nbsp;203 StGB). Auskünfte über den Gesundheitszustand gibt es nur, wenn die pflegebedürftige Person einverstanden ist oder eine Vollmacht bzw. Betreuung vorliegt. Halten Sie in der Akte fest, wer Auskunft bekommen darf – das erspart Unsicherheit am Telefon.</p>

    <h2>Feste Wege statt Zufall</h2>
    <ul>
      <li><strong>Organisatorisches</strong> (Besuchszeiten, Terminänderungen, Urlaub): schriftlich per Chat, WhatsApp oder E-Mail.</li>
      <li><strong>Pflegerische Fragen:</strong> persönliches Gespräch mit der Pflegedienstleitung, mit festem Rückrufzeitfenster.</li>
      <li><strong>Notfälle:</strong> 112 – nicht der Chat und nicht die Büronummer.</li>
    </ul>

    <h2>Was ein digitaler Assistent übernimmt</h2>
    <p>Ein Assistent nimmt Fragen von Angehörigen jederzeit auf, fragt nach, worum es geht, und legt das Anliegen sortiert ins Büro: „Besuch morgen später möglich?“, „Rückruf erbeten“, „Änderung der Medikamentenabholung“. Die Antwort gibt das Büro. Der Assistent gibt selbst keine pflegerischen oder medizinischen Auskünfte und sagt gleich zu Beginn, dass er eine KI ist.</p>

    <h2>Datensparsam bleiben</h2>
    <p>Im Chat genügt, wer schreibt, für wen und worum es geht – keine Diagnosen. WhatsApp nur über die WhatsApp Business Platform mit Einwilligung, nicht über private Handys. Mit dem Dienstleister schließen Sie einen AV-Vertrag und eine Verschwiegenheitsverpflichtung ab.</p>

    <h2>So starten Sie</h2>
    <ol>
      <li>Auskunftsberechtigte je Pflegebedürftigem in der Akte vermerken.</li>
      <li>Wege festlegen: Organisatorisches schriftlich, Pflegerisches persönlich.</li>
      <li>Rückrufzeitfenster der PDL bekanntgeben.</li>
      <li>Angehörige mit einem kurzen Infoblatt über die Wege informieren.</li>
    </ol>''',
  cta=PFLEGE_CTA, weiter=W_PF, quellen=QUELLEN_RECHT,
  related=[('/blog/krankmeldung-pflegedienst-digital.html', 'Krankmeldungen im Pflegedienst', 'Schneller bei der Einsatzleitung – per Chat oder WhatsApp.'),
           ('/blog/postfach-pflegedienst-ordnen.html', 'Postfach im Pflegedienst ordnen', 'Kassen, Praxen, Bewerbungen – sortiert statt liegen geblieben.')]),

 dict(file='postfach-pflegedienst-ordnen.html', crumb='Postfach Pflegedienst',
  title='E-Mail-Postfach im Pflegedienst ordnen – mit KI',
  desc='Kassen-Rückfragen, Arztpraxen, Bewerbungen, Angehörige: Wie ambulante Pflegedienste ihr Postfach vorsortieren und Antworten vorbereiten lassen – die Freigabe bleibt beim Team.',
  tag='Ratgeber · KI &amp; Pflege', h1='Das Postfach im Pflegedienst:<br><em>sortiert statt liegen geblieben.</em>', minuten=5, bild=BILD_PF,
  intro='<p>Rückfragen von Kassen, Verordnungen aus Arztpraxen, Bewerbungen, Nachrichten von Angehörigen – im Büro eines Pflegedienstes landet vieles in einem Postfach. Was nicht sofort zugeordnet wird, bleibt liegen. Ein digitaler Assistent kann vorsortieren und Antworten vorbereiten. Entscheiden und abschicken tut weiterhin Ihr Team.</p>',
  body='''
    <h2>Was sich gut vorsortieren lässt</h2>
    <ul>
      <li><strong>Kassen und Kostenträger:</strong> Rückfragen, Genehmigungen, Unterlagen – mit Zuordnung zum richtigen Vorgang.</li>
      <li><strong>Arztpraxen:</strong> Verordnungen und Rückfragen, die schnell bei der PDL ankommen müssen.</li>
      <li><strong>Bewerbungen:</strong> eingeordnet nach Stelle, Eingangsbestätigung als Entwurf.</li>
      <li><strong>Angehörige:</strong> Anliegen erkannt und an die zuständige Person gegeben.</li>
      <li><strong>Werbung und Newsletter:</strong> aussortiert, damit Wichtiges oben steht.</li>
    </ul>

    <h2>Antwortentwurf statt automatischer Antwort</h2>
    <p>Für wiederkehrende Fälle – Eingangsbestätigung, Bitte um fehlende Unterlagen, Terminvorschlag – entsteht ein Entwurf. Eine Mitarbeiterin prüft ihn und schickt ihn ab. So bleibt die Verantwortung beim Team, und die Antwort ist trotzdem schnell da.</p>

    <h2>Was nicht automatisch passieren sollte</h2>
    <p>Pflegerische oder medizinische Einschätzungen, Zusagen zu Kapazitäten, Absagen an Bewerber und alles mit rechtlicher Wirkung gibt ein Mensch frei. Das System ergänzt Ihre Pflegesoftware und KIM, es ersetzt sie nicht.</p>

    <h2>Datenschutz im Postfach</h2>
    <p>Im Postfach stecken Gesundheits- und Bewerberdaten. Deshalb: Verarbeitung in der EU, AV-Vertrag nach Art.&nbsp;28 DSGVO, Verschwiegenheitsverpflichtung nach §&nbsp;203 StGB und feste Löschfristen – auch für Bewerbungen. Der Assistent liest nur, was er für die Sortierung braucht.</p>

    <h2>So fangen Sie an</h2>
    <ol>
      <li>Eine Woche lang notieren, welche Arten von E-Mails am häufigsten kommen.</li>
      <li>Für die drei häufigsten Arten Zuständigkeit und Antwortvorlage festlegen.</li>
      <li>Vorsortierung mit Antwortentwurf für genau diese drei starten.</li>
      <li>Nach vier Wochen prüfen und erweitern.</li>
    </ol>''',
  cta=PFLEGE_CTA, weiter=W_PF, quellen=QUELLEN_RECHT,
  related=[('/blog/angehoerige-kommunikation-pflegedienst.html', 'Angehörige im Pflegedienst', 'Gut informiert, ohne Dauertelefon.'),
           ('/blog/pflegekraefte-finden-werbung.html', 'Pflegekräfte finden', 'Wie Werbung beim Recruiting hilft.')]),
]

ARTIKEL += NEU


def bauen(a):
    s = VORLAGE
    url = BASE + 'blog/' + a['file']
    alt_url = BASE + 'blog/fotowand-firmenfeier.html'
    s = s.replace(alt_url, url)
    s = re.sub(r'<title>.*?</title>', f'<title>{a["title"]}</title>', s, count=1)
    for k in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        s = re.sub(rf'(<meta {k} content=")[^"]*', lambda m: m.group(1) + a['desc'], s, count=1)
    for k in ('property="og:title"', 'name="twitter:title"'):
        s = re.sub(rf'(<meta {k} content=")[^"]*', lambda m: m.group(1) + a['title'], s, count=1)
    img = BASE.rstrip('/') + a['bild'][0] + '.webp'
    s = s.replace('https://masar-werbeagentur.de/messe.webp', img)
    s = re.sub(r'(<meta property="og:image:alt" content=")[^"]*', lambda m: m.group(1) + a['bild'][1], s, count=1)
    s = re.sub(r'"headline": "[^"]*"', '"headline": ' + json.dumps(a['title'], ensure_ascii=False), s, count=1)
    s = re.sub(r'"description": "[^"]*"', '"description": ' + json.dumps(a['desc'], ensure_ascii=False), s, count=1)
    s = s.replace('"datePublished": "2026-11-01"', '"datePublished": "2026-11-03"').replace('"dateModified": "2026-11-01"', '"dateModified": "2026-11-03"')
    s = s.replace('"name": "Fotowand Firmenfeier"', '"name": ' + json.dumps(a['crumb'], ensure_ascii=False))
    s = re.sub(r'(<div class="art-tag"><svg.*?</svg>)[^<]*', lambda m: m.group(1) + a['tag'], s, count=1, flags=re.S)
    s = re.sub(r'<h1>.*?</h1>', f'<h1>{a["h1"]}</h1>', s, count=1, flags=re.S)
    s = re.sub(r'\d+ Min\. Lesezeit', f'{a["minuten"]} Min. Lesezeit', s, count=1)
    b, alt, cap = a['bild']
    fig = (f'\n    <figure class="art-figure">\n      <img src="{b}-720.webp" srcset="{b}-360.webp 360w, {b}-540.webp 540w, {b}-720.webp 720w, {b}.webp 1080w" '
           f'sizes="(max-width:600px) 92vw, 420px" width="720" height="900" alt="{alt}" loading="eager" fetchpriority="high">\n      <figcaption>{cap}</figcaption>\n    </figure>\n')
    t, p, ziel, ziel_txt, wa_txt, thema = a['cta']
    from urllib.parse import quote
    weiter = ' · '.join(f'<a href="{h}" style="color:var(--teal);font-weight:700;">{x}</a>' for h, x in a['weiter'])
    cta = f'''    <div class="article-cta">
      <h3>{t}</h3>
      <p>{p}</p>
      <div class="btns">
        <a href="{ziel}" class="btn-teal">{ziel_txt}</a>
        <a href="https://wa.me/491785143918?text={quote(wa_txt)}" class="btn-wa" target="_blank" rel="noopener noreferrer">WhatsApp</a>
        <a href="/termin.html?thema={quote(thema)}" data-termin-link class="btn-termin" style="background:#fff;color:var(--navy);padding:13px 24px;border-radius:8px;font-weight:700;font-size:15px">Kostenlose Beratung buchen</a>
      </div>
      <p style="margin:1.2rem 0 0;font-size:14px;">Weiter: {weiter}</p>
    </div>

    <div class="sources">
      <h2>Quellen</h2>
      <ul>
{''.join(f'        <li><a href="{h}" target="_blank" rel="noopener noreferrer">{x}</a></li>' + chr(10) for h, x in a['quellen'])}      </ul>
      <p>Hinweis: Dieser Artikel ist keine Rechtsberatung. Für Verträge und Ihre Datenschutz-Folgenabschätzung empfehlen wir eine fachkundige Prüfung.</p>
    </div>

    <div class="related-posts">
      <h2>Weitere Artikel</h2>
      <div class="related-grid">
{''.join(f"""        <div class="related-card">
          <h3>{x}</h3>
          <p>{d}</p>
          <a href="{h}">Artikel lesen →</a>
        </div>
""" for h, x, d in a['related'])}      </div>
    </div>

  </div>
</main>'''
    i = s.index('<main class="article-body">'); j = s.index('</main>', i) + len('</main>')
    s = s[:i] + '<main class="article-body">\n  <div class="container">\n\n    ' + a['intro'] + fig + a['body'] + '\n\n' + cta + s[j:]
    open(os.path.join(ROOT, 'blog', a['file']), 'w', encoding='utf-8').write(s)
    return a['file'], len(s)


if __name__ == '__main__':
    for a in ARTIKEL:
        print(bauen(a))
