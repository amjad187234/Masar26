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
           f'sizes="(max-width:600px) 92vw, 420px" width="720" height="900" alt="{alt}" loading="eager">\n      <figcaption>{cap}</figcaption>\n    </figure>\n')
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
