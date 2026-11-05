"""Genehmigungs-Check Werbeanlage (genehmigungs-check.html) – Generator auf Basis von gen_folien.build_f.
Werkzeug: /genehmigung.js (Fragen-Assistent, keine Preise, keine Rechtsberatung). Regeln mit Quellen siehe Kopf von genehmigung.js
und Abschnitt „Regeln je Region“. Idee und Belege: docs/markt-2026-11/suchnachfrage-luecken.md (Briefing 8).
Aufruf: python3 tools/folien/genehmigung_page.py
"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'gen_folien.py'), encoding='utf-8').read()
exec(src[:src.index("\nif __name__")])


def frage(key, nr, text, opts, hilfe=''):
    btn = ''.join(f'<button type="button" data-v="{v}" aria-pressed="false">{t}</button>' for v, t in opts)
    h = f'<p class="gc-help">{hilfe}</p>' if hilfe else ''
    return f'''        <fieldset class="gc-q" data-q="{key}"><legend><span>{nr}</span>{text}</legend>{h}<div class="gc-opts">{btn}</div></fieldset>\n'''


WERKZEUG = ('    <div class="gc" id="gcheck">\n      <p class="gc-fort" id="gc-fort" aria-live="polite"></p>\n'
    + frage('region', 1, 'Wo ist Ihr Geschäft?', [('berlin', 'Berlin'), ('nrw', 'NRW'), ('hamburg', 'Hamburg'), ('brandenburg', 'Brandenburg'), ('andere', 'Anderswo')])
    + frage('wo', 2, 'Was planen Sie?', [('fassade', 'Schild oder Schriftzug an der Fassade'), ('fenster', 'Werbung im Schaufenster'), ('ausleger', 'Ausleger über dem Gehweg'),
                                         ('gehweg', 'Kundenstopper auf dem Gehweg'), ('geruest', 'Banner an Bauzaun oder Gerüst'), ('frei', 'Freistehend (Pylon, Mast)')])
    + frage('flaeche', 3, 'Wie groß ist die Ansichtsfläche?', [('k1', 'bis 1 m²'), ('k25', '1 bis 2,5 m²'), ('g', 'über 2,5 m²')],
            'Breite × Höhe der Werbefläche. Mehrere Schilder nebeneinander zählen zusammen.')
    + frage('eigen', 4, 'Wirbt es für Ihr eigenes Geschäft am selben Ort?', [('ja', 'Ja, eigenes Geschäft'), ('nein', 'Nein, Fremdwerbung')])
    + frage('dauer', 5, 'Wie lange hängt es?', [('dauer', 'Dauerhaft'), ('kurz', 'Höchstens 2 Monate')])
    + frage('denkmal', 6, 'Denkmal oder Altstadt-Satzung?', [('nein', 'Nein'), ('ja', 'Ja'), ('unklar', 'Weiß nicht')])
    + frage('miete', 7, 'Ist das Gebäude gemietet?', [('ja', 'Ja, gemietet'), ('nein', 'Nein, eigenes Gebäude')])
    + frage('licht', 8, 'Soll es leuchten?', [('ja', 'Ja, beleuchtet'), ('nein', 'Nein')])
    + '      <div id="gc-out" aria-live="polite" hidden></div>\n    </div>')

CSS = '''<style id="gcheck-css">
.gc{max-width:860px;margin:0 auto;display:grid;gap:.9rem}
.gc [hidden]{display:none!important}
.gc-fort{font-size:14px;color:var(--muted);margin:0;text-align:right}
.gc-q{border:1px solid var(--border);border-radius:14px;background:#fff;padding:1rem 1.1rem 1.1rem;margin:0;min-width:0}
.gc-q legend{font-weight:700;color:var(--navy);font-size:1.05rem;padding:0 .4rem;display:flex;gap:.55rem;align-items:center}
.gc-q legend span{display:inline-flex;width:28px;height:28px;border-radius:50%;background:var(--teal);color:var(--navy);align-items:center;justify-content:center;font-size:.95rem;flex:none}
.gc-help{font-size:13.5px;color:var(--muted);margin:.2rem 0 .5rem}
.gc-opts{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:.5rem}
.gc-opts button{font:inherit;font-size:15px;font-weight:600;padding:.6rem 1rem;min-height:46px;border-radius:10px;border:1.5px solid var(--border);background:#fff;color:var(--navy);cursor:pointer;text-align:left}
.gc-opts button[aria-pressed=true]{border-color:var(--teal-ink);background:#e6f7f4;box-shadow:inset 0 0 0 1px var(--teal-ink)}
.gc-opts button:focus-visible{outline:3px solid var(--navy);outline-offset:2px}
.gc-res{border-radius:16px;padding:1.3rem 1.3rem 1.2rem;border:1px solid}
.gc-res h3{margin:.4rem 0 .6rem;color:var(--navy);font-size:1.35rem}
.gc-res ul{margin:0 0 .8rem 1.1rem;display:grid;gap:.45rem}
.gc-res li{font-size:15.5px;line-height:1.6}
.gc-tag{display:inline-block;font-size:12.5px;font-weight:800;text-transform:uppercase;letter-spacing:.5px;padding:.2rem .6rem;border-radius:20px;color:#fff}
.gc-gruen{background:#e9f7f4;border-color:#9ed9cd}.gc-gruen .gc-tag{background:#177567}
.gc-gelb{background:#fff6e5;border-color:#f0cf8f}.gc-gelb .gc-tag{background:#8a5100}
.gc-rot{background:#fdeceb;border-color:#f0b4ae}.gc-rot .gc-tag{background:#b3261e}
.gc-links{font-size:15px}.gc-links a{color:var(--teal-ink);font-weight:700}
.gc-hinweis{font-size:13.5px;color:var(--muted);margin:.6rem 0 0}
.gc-act{display:flex;flex-wrap:wrap;gap:.6rem;margin-top:1rem}
.gc-act .btn{flex:1 1 220px;justify-content:center;text-align:center}
.gc-btn2{background:var(--navy);color:#fff}
.gc-again{flex:1 1 160px;font:inherit;font-weight:700;padding:.8rem 1rem;border-radius:10px;border:2px solid var(--border);background:#fff;color:var(--navy);cursor:pointer;min-height:48px}
@media(max-width:600px){.gc-q{padding:.85rem}.gc-opts button{flex:1 1 100%}}
</style>'''

P = dict(file='genehmigungs-check.html', crumb='Genehmigungs-Check', img='aussenwerbung',
 parent=('Außenwerbung', 'aussenwerbung-berlin.html'), finder_strip=False, tab_ey='Regeln je Region', hero_mobile=True,
 img_alt='Fassade mit Werbeschildern und Leuchtreklame – Beispiel für Außenwerbung',
 title='Genehmigungs-Check: Braucht mein Schild eine Genehmigung?',
 desc='Acht kurze Fragen zu Ort, Größe und Gebäude: Der Check zeigt, ob Ihr Schild in Berlin, NRW oder Hamburg wohl verfahrensfrei ist oder einen Antrag braucht.',
 service_type='Genehmigungsservice Werbeanlagen', schema_name='Genehmigungs-Check für Werbeanlagen',
 area=[{"@type": "City", "name": "Berlin"}, {"@type": "State", "name": "Nordrhein-Westfalen"}, {"@type": "City", "name": "Hamburg"}, {"@type": "State", "name": "Brandenburg"}],
 badge='Kostenloses Werkzeug · Genehmigung', h1='Genehmigungs- <em>Check</em>',
 sub='Braucht Ihr Schild, Ihre Leuchtreklame oder Ihr Kundenstopper eine Genehmigung? Acht kurze Fragen – und Sie wissen, woran Sie sind: verfahrensfrei, Antrag beim Bauamt oder Erlaubnis für den Gehweg. Kostenlos und ohne Anmeldung.',
 trust='Berlin · NRW · Hamburg · Brandenburg · mit Quellen · keine Anmeldung',
 usp=['8 kurze Fragen', 'Berlin, NRW, Hamburg', 'Mit Paragraf und Quelle', 'Wir klären den Rest'],
 wa='Hallo, ich plane eine Werbeanlage und möchte wissen, ob ich eine Genehmigung brauche.',
 top=('Jetzt prüfen', 'Brauche ich eine <em>Genehmigung?</em>', 'Beantworten Sie die Fragen – das Ergebnis erscheint sofort darunter. Es ist eine erste Einordnung, keine Rechtsberatung.', WERKZEUG),
 angles_ey='Warum vorher prüfen', angles_h2='Teuer wird es <em>nach</em> der Montage',
 angles_sub='Fehlt eine nötige Genehmigung, kann das Amt den Abbau verlangen – dann ist das Schild schon bezahlt.',
 angles=[
  ('Abbau auf eigene Kosten', 'Ohne nötige Genehmigung kann die Bauaufsicht die Beseitigung anordnen. Die Bauordnungen erlauben zusätzlich Bußgelder, in Berlin und NRW bis 500.000 €.'),
  ('Zwei Ämter, zwei Fragen', 'Das Bauamt prüft die Werbeanlage, die Stadt den Gehweg. Ein Ausleger oder Kundenstopper braucht oft beides.'),
  ('Denkmal und Satzung', 'In Altstadt- und Denkmalbereichen gelten strengere Regeln – auch für kleine Schilder.'),
  ('Vermieter nicht vergessen', 'Unabhängig vom Amt braucht es meist die Zustimmung des Eigentümers.'),
 ],
 tab_h2='Die Regeln <em>auf einen Blick</em>', tab_sub='Stand November 2026. Maßgeblich ist immer die Auskunft der zuständigen Behörde.',
 tab_cols=['Region', 'Verfahrensfrei (Bauordnung)', 'Gut zu wissen'],
 tab_rows=[
  ['Berlin', 'bis 1 m² Ansichtsfläche, am eigenen Geschäft bis 2,5 m² (§ 61 Abs. 1 BauO Bln)', 'größer: Antrag beim Bezirksamt, meist vereinfachtes Verfahren; Gerüst- und Bauzaunwerbung nicht verfahrensfrei'],
  ['NRW', 'bis 1 m² (§ 62 Abs. 1 Nr. 12 BauO NRW); vorübergehend bis 2 Monate', 'Flächen nebeneinander werden zusammengerechnet; Gestaltungssatzungen der Städte beachten'],
  ['Hamburg', 'bis 1 m² (Anlage 2 HBauO)', 'sonst meist Baugenehmigung beim Bezirksamt; Kundenstopper grundsätzlich nicht gestattet'],
  ['Brandenburg', 'vorübergehend bis 2 Monate (§ 61 BbgBO)', 'für dauerhafte Anlagen beim Bauamt der Stadt nachfragen'],
  ['Gehweg (überall)', '–', 'Kundenstopper, Warenauslage und Ausleger brauchen eine Sondernutzungserlaubnis der Stadt'],
 ],
 tab_note='Denkmalschutz gilt zusätzlich: Am Denkmal braucht auch eine sonst verfahrensfreie Werbeanlage meist eine denkmalrechtliche Genehmigung. Details in den Ratgebern <a href="/blog/aussenwerbung-berlin-ratgeber.html">Außenwerbung Berlin</a>, <a href="/blog/werbeanlage-hamburg.html">Hamburg</a> und <a href="/blog/kundenstopper-erlaubnis.html">Kundenstopper</a>.',
 svc_h2='Wir kümmern uns <em>um den Rest</em>', svc_sub='Von der Prüfung bis zur Montage – mit einem Ansprechpartner.',
 services=[
  ('stern', 'Schilder', 'Firmen-, Praxis- und Türschilder – mit Prüfung der Genehmigung.', '/schilder-berlin.html'),
  ('neon', 'Leuchtreklame', 'Leuchtbuchstaben und Leuchtkästen, Bau durch eingetragene Partnerbetriebe.', '/leuchtreklame-berlin.html'),
  ('karte', 'Schaufenster', 'Beschriftung und Folien – oft die Alternative zum Kundenstopper.', '/schaufensterbeschriftung-berlin.html'),
  ('druck', 'Bauzaunbanner', 'Banner für Baustelle und Gerüst – mit Hinweis auf die Regeln vor Ort.', '/pvc-banner-berlin.html'),
 ],
 preis_h2='Was kostet <em>die Prüfung?</em>',
 preis_html='''<p>Der Check ist kostenlos. Bei jedem Angebot für ein Schild oder eine Leuchtreklame prüfen wir außerdem, ob an Ihrem Standort eine Genehmigung nötig ist. Auf Wunsch bereiten wir die Antragsunterlagen vor – was das kostet, steht dann im Angebot. Die Gebühren des Amts richten sich nach dessen Gebührenordnung.</p>''',
 recht_ey='Quellen', recht_h2='Worauf der Check <em>beruht</em>', recht_sub=None,
 recht_html='''<p>Der Check ordnet Ihre Angaben nach den Bauordnungen und den Hinweisen der Städte ein (Stand November 2026). Er ersetzt keine Auskunft der Behörde und keine Rechtsberatung: Gestaltungssatzungen, Bebauungspläne oder Besonderheiten am Gebäude kann er nicht kennen.</p>
<ul>
<li><a href="https://gesetze.co/BE/BauO_Bln/61" target="_blank" rel="noopener noreferrer">§ 61 BauO Bln – Verfahrensfreie Bauvorhaben</a></li>
<li><a href="https://www.stadt-koeln.de/artikel/74042/index.html" target="_blank" rel="noopener noreferrer">Stadt Köln – Werbeanlagen (§ 62 BauO NRW)</a></li>
<li><a href="https://www.hamburg.de/service/info/111073031/n0/" target="_blank" rel="noopener noreferrer">hamburg.de – Werbung auf öffentlichen Wegen</a></li>
<li><a href="https://service.berlin.de/dienstleistung/325999/" target="_blank" rel="noopener noreferrer">service.berlin.de – Sondernutzung für Werbeaufsteller</a></li>
<li><a href="https://www.berlin.de/ba-neukoelln/politik-und-verwaltung/aemter/stadtentwicklungsamt/stadtplanung/planungsrechtliche-auskuenfte/260708_merkblatt_werbeanlagen-neukoelln.pdf" target="_blank" rel="noopener noreferrer">Bezirksamt Neukölln – Merkblatt Werbeanlagen (PDF)</a></li>
</ul>''',
 ablauf=[
  ('Fragen beantworten', 'Region, Art, Größe und Gebäude – das Ergebnis erscheint sofort.'),
  ('Ergebnis lesen', 'Verfahrensfrei, Antrag oder Gehweg-Erlaubnis – mit Paragraf und Link zum passenden Ratgeber.'),
  ('Mit uns klären', 'Schicken Sie uns Ihr Ergebnis und ein Foto – wir prüfen den Standort und machen ein Angebot.'),
  ('Umsetzen', 'Nach Freigabe fertigen und montieren wir – bei Bedarf mit Genehmigung.'),
 ],
 faq_h2='Genehmigung – <em>Fragen &amp; Antworten</em>',
 faq=[
  ('Ist der Check verbindlich?', 'Nein. Er ist eine erste Einordnung nach den Bauordnungen und Hinweisen der Städte (Stand November 2026). Verbindlich ist die Auskunft der Bauaufsicht bzw. des Bezirksamts.'),
  ('Was ist die Ansichtsfläche?', 'Die Fläche, die man von vorn sieht – Breite mal Höhe der Werbeanlage. In NRW werden mehrere Flächen nebeneinander zusammengerechnet.'),
  ('Was heißt „an der Stätte der Leistung“?', 'Werbung für das eigene Geschäft am selben Ort, etwa der Schriftzug über Ihrem Laden. In Berlin ist sie bis 2,5 m² verfahrensfrei.'),
  ('Brauche ich für einen Kundenstopper eine Genehmigung?', 'Auf dem öffentlichen Gehweg ja – eine Sondernutzungserlaubnis der Stadt. In Hamburg sind Kundenstopper laut Stadt grundsätzlich nicht gestattet.'),
  ('Was passiert ohne Genehmigung?', 'Die Behörde kann einen nachträglichen Antrag oder den Abbau verlangen; zusätzlich sind Bußgelder möglich. Am teuersten ist meist der Abbau eines bezahlten Schilds.'),
  ('Kümmern Sie sich um den Antrag?', 'Ja, auf Wunsch. Wir prüfen bei jedem Angebot, ob eine Genehmigung nötig ist, und bereiten die Unterlagen vor.'),
 ],
 links=[('/blog/aussenwerbung-berlin-ratgeber.html', 'Außenwerbung Berlin'), ('/blog/kundenstopper-erlaubnis.html', 'Kundenstopper'), ('/blog/werbeschild-mietobjekt-vermieter.html', 'Schild am Mietobjekt'),
        ('/blog/werbeanlage-hamburg.html', 'Werbeanlagen Hamburg'), ('/leuchtbuchstaben-konfigurator.html', 'Konfigurator')],
 form_opts=['Schild', 'Leuchtreklame', 'Schaufenster', 'Ausleger', 'Kundenstopper', 'Bauzaunbanner'],
 form_labels=('Was planen Sie?', 'Standort &amp; Wunsch', 'Foto der Fassade (optional)', 'Ein Foto der Fassade hilft uns, die Lage einzuschätzen.'),
 form_sub='Schicken Sie uns Ihr Ergebnis und ein Foto – wir prüfen die Genehmigung für Ihren Standort und machen Ihnen ein Angebot.',
 subject='Genehmigungs-Check (Website)', msg_ph='z. B. Leuchtreklame 3 × 0,6 m über dem Laden, Berlin-Neukölln, Altbau',
 sticky=('Genehmigungs-Check', 'In 8 Fragen zur ersten Einordnung'))

APP = {"@context": "https://schema.org", "@type": "WebApplication", "name": "Genehmigungs-Check Werbeanlage",
       "url": "https://masar-werbeagentur.de/genehmigungs-check.html", "applicationCategory": "UtilitiesApplication",
       "operatingSystem": "Web-Browser", "inLanguage": "de", "isAccessibleForFree": True, "description": P['desc'],
       "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}, "provider": {"@id": "https://masar-werbeagentur.de/#identity"}}

if __name__ == '__main__':
    f, n = build_f(P)
    path = ROOT + f
    s = open(path, encoding='utf-8').read()
    s = s.replace('<section class="section" id="preise">', '<section class="section" id="check">', 1)
    s = s.replace('<a href="#kontakt" class="btn btn-teal">Angebot anfordern</a>', '<a href="#check" class="btn btn-teal">Jetzt prüfen</a>', 1)
    s = s.replace('Foto per WhatsApp schicken</a>', 'Per WhatsApp fragen</a>', 1)
    s = s.replace('Kostenloses Angebot <em>anfordern</em>', 'Genehmigung <em>mit uns klären</em>', 1)
    s = s.replace('</head>', CSS + '\n<script type="application/ld+json">\n' + json.dumps(APP, ensure_ascii=False, indent=2) + '\n</script>\n</head>', 1)
    s = s.replace('</body>', '<script src="/genehmigung.js?v=1" defer></script>\n</body>', 1)
    open(path, 'w', encoding='utf-8').write(s)
    print(f, len(s))
