"""Zusätzliche Wissens-Abschnitte auf Leistungsseiten (04.11.2026, aus dem Wettbewerbsvergleich docs/wettbewerb-2026-11.md).

Setzt vor den FAQ-Abschnitt jeweils einen Abschnitt mit belegten Hinweisen (Strom & Licht bei Leuchtreklame,
Scheiben bei Fahrzeugen, Befestigung & Genehmigung bei Bannern, Arbeitskleidung beim Textildruck, Logo-Dateien
beim Grafikdesign) und verlinkt den passenden Ratgeber aus tools/blog/werbetechnik_ratgeber.py.
Idempotent (Marker <!-- wissen:start --> … <!-- wissen:end -->); setzt außerdem einen Link-Chip in „Passend dazu“,
wo es die Leiste gibt. Nach dem Neu-Erzeugen der Seiten erneut ausführen (Reihenfolge: nach stadt_lokal.py).

Aufruf: python3 tools/seo/wissen_abschnitte.py [--dry]
"""
import os, re, sys

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
START, ENDE = '<!-- wissen:start -->', '<!-- wissen:end -->'
ICON = ('<svg class="i-inline" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="10"/>'
        '<path d="M12 16v-4"/><path d="M12 8h.01"/></svg>')
LINK = 'style="color:var(--teal-ink);font-weight:700;"'


def quellen(liste, zusatz='Allgemeine Hinweise, keine Rechtsberatung.'):
    q = ' · '.join(f'<a href="{h}" target="_blank" rel="noopener noreferrer">{t}</a>' for h, t in liste)
    return f'<p style="font-size:13px;">Quellen: {q}. {zusatz}</p>'


Q_LICHT = [('https://www.gesetze-im-internet.de/bimschg/__22.html', '§ 22 BImSchG'),
           ('https://www.lai-immissionsschutz.de/documents/lichthinweise-2015-11-03mit-formelkorrektur_aus_03_2018_1520588339.pdf', 'LAI-Hinweise Lichtimmissionen'),
           ('https://www.gesetze-im-internet.de/bnatschg_2009/__41a.html', '§ 41a BNatSchG')]
LICHT = ('Betrieb', 'Strom, Schaltzeiten <em>&amp; Nachbarn</em>', f'''
<p><strong>Stromkosten selbst ausrechnen:</strong> Leistung laut Datenblatt (Watt) × Betriebsstunden ÷ 1.000 ergibt die Kilowattstunden – mal Ihrem Strompreis sind das die Kosten. Der größte Hebel sind die Stunden: Eine Anlage, die nur von der Dämmerung bis Ladenschluss leuchtet, verbraucht einen Bruchteil einer Anlage im Dauerbetrieb.</p>
<p><strong>Steuerung gleich mitplanen:</strong> Ein Dämmerungsschalter schaltet ein, wenn es dunkel wird; eine Zeitschaltuhr schaltet zu einer festen Uhrzeit aus. Viele LED-Anlagen lassen sich außerdem dimmen – das hilft, wenn Wohnungen in der Nähe sind.</p>
<p><strong>Muss die Reklame nachts aus?</strong> Eine allgemeine Abschaltpflicht gibt es derzeit nicht; die Regel der Energiesparverordnung (22 bis 6 Uhr) ist im April 2023 ausgelaufen. Betriebszeiten können aber als Auflage in der Genehmigung oder in einer örtlichen Satzung stehen. Licht gilt außerdem als Immission: Stört es Nachbarn erheblich, beurteilen Behörden das nach den LAI-Hinweisen. Wir richten die Anlage deshalb zur Straße aus und planen die Helligkeit passend zur Umgebung.</p>
<p>Ausführlich mit Rechenbeispiel: <a href="/blog/leuchtreklame-strom-betriebszeiten.html" {LINK}>Leuchtreklame: Strom, Schaltzeiten, Nachbarn →</a></p>
{quellen(Q_LICHT)}''', ('/blog/leuchtreklame-strom-betriebszeiten.html', 'Ratgeber: Strom &amp; Schaltzeiten'))

Q_SCHEIBE = [('https://www.gesetze-im-internet.de/stvzo_2012/__22a.html', '§ 22a StVZO'),
             ('https://www.gesetze-im-internet.de/stvzo_2012/__35b.html', '§ 35b StVZO'),
             ('https://www.gesetze-im-internet.de/stvzo_2012/__56.html', '§ 56 StVZO')]
SCHEIBE = ('Scheiben', 'Werbung auf den <em>Scheiben</em>', f'''
<p><strong>Front und vordere Seitenscheiben bleiben frei.</strong> Dort braucht der Fahrer freie Sicht nach vorn, zur Seite und auf die Außenspiegel (§ 35b StVZO).</p>
<p><strong>Heckscheibe und hintere Seitenscheiben:</strong> Hier ist Werbung mit Lochfolie möglich – von außen sieht man das Motiv, von innen schaut man hindurch. Die Folie braucht eine Bauartgenehmigung des Kraftfahrt-Bundesamts (§ 22a StVZO), und ist die Sicht nach hinten eingeschränkt, muss das Fahrzeug Außenspiegel auf beiden Seiten haben (§ 56 StVZO). Kennzeichen, Leuchten und Plaketten werden nie überklebt.</p>
<p>Oft wirkt die Telefonnummer auf der lackierten Heckklappe genauso gut – ohne Einschränkung der Sicht. Wir sagen Ihnen bei der Planung, was bei Ihrem Fahrzeug sinnvoll ist. Mehr dazu: <a href="/blog/werbung-autoscheiben-erlaubt.html" {LINK}>Werbung auf Autoscheiben: Was ist erlaubt? →</a></p>
{quellen(Q_SCHEIBE, 'Allgemeine Hinweise, keine Rechtsberatung – im Zweifel Prüforganisation oder Zulassungsstelle fragen.')}''', ('/blog/werbung-autoscheiben-erlaubt.html', 'Ratgeber: Werbung auf Autoscheiben'))

BANNER_BEF = f'''
<p><strong>Alle Ösen nutzen:</strong> Nur dann verteilt sich die Zugkraft. Werden nur die Ecken befestigt, reißen sie bei Wind zuerst aus. An windigen Standorten setzen wir die Ösen enger und verstärken die Ecken.</p>
<p><strong>Kabelbinder oder Spanngummi?</strong> Kabelbinder sind schnell und günstig, aber starr und im Sonnenlicht nicht ewig haltbar – gut für kurze Einsätze. Spanngummis federn Windstöße ab und schonen die Ösen, wenn das Banner länger hängt.</p>
<p><strong>Der Zaun muss es tragen:</strong> Ein Banner erhöht die Windlast auf den Bauzaun. Ob der Zaun ausreichend beschwert oder abgestützt ist, klären Sie mit dem Verleiher oder der Bauleitung – vor angekündigtem Sturm das Banner im Zweifel abnehmen.</p>'''
Q_BLN = [('https://www.anwalt24.de/gesetze/bauo_bln/61', '§ 61 BauO Bln')]
BANNER_B = ('Befestigung', 'Am Bauzaun <em>sicher befestigt</em>', BANNER_BEF + f'''
<p><strong>Genehmigung in Berlin:</strong> Werbeanlagen bis 1&nbsp;m² Ansichtsfläche, an der Stätte der Leistung bis 2,5&nbsp;m², sind verfahrensfrei (§ 61 Abs. 1 BauO Bln). Größere Banner oder Fremdwerbung sollten vorher mit dem Bezirksamt geklärt werden; steht der Zaun auf Gehweg oder Straße, ist zusätzlich die Sondernutzung zu beachten.</p>
<p>Alles zu Material, Maß und Genehmigung: <a href="/blog/bauzaunbanner-ratgeber.html" {LINK}>Bauzaunbanner: Material, Befestigung, Genehmigung →</a></p>
{quellen(Q_BLN)}''', ('/blog/bauzaunbanner-ratgeber.html', 'Ratgeber: Bauzaunbanner'))
BANNER_N = ('Befestigung', 'Am Bauzaun <em>sicher befestigt</em>', BANNER_BEF + f'''
<p>Alles zu Material, Maß und Genehmigung in NRW, Berlin, Brandenburg und Hamburg: <a href="/blog/bauzaunbanner-ratgeber.html" {LINK}>Bauzaunbanner: Material, Befestigung, Genehmigung →</a></p>''', ('/blog/bauzaunbanner-ratgeber.html', 'Ratgeber: Bauzaunbanner'))

TEXTIL = ('Arbeitskleidung', 'Arbeitskleidung <em>richtig bedrucken</em>', f'''
<p><strong>Erst die Wäsche klären:</strong> Kleidung, die zu Hause gewaschen wird, stellt andere Ansprüche als Kleidung, die regelmäßig in eine gewerbliche Wäscherei geht. Sagen Sie uns, wie bei Ihnen gewaschen wird – dann wählen wir das Verfahren danach oder sagen Ihnen ehrlich, wenn ein anderes Verfahren besser passt. Stickerei bieten wir nicht an.</p>
<p><strong>Schutz- und Warnkleidung:</strong> Reflexstreifen und Leuchtflächen werden nicht überdruckt, und bedruckt wird nur, wo der Hersteller es zulässt – sonst kann die Schutzwirkung leiden.</p>
<p><strong>Position:</strong> Brust links für den Kontakt auf Augenhöhe, Rücken groß für die Fernwirkung auf Baustelle oder Umzug – dort passen auch Website oder Telefonnummer.</p>
<p>Mehr Tipps zu Verfahren, Pflege und Teambestellung: <a href="/blog/arbeitskleidung-bedrucken.html" {LINK}>Arbeitskleidung bedrucken →</a></p>''', ('/blog/arbeitskleidung-bedrucken.html', 'Ratgeber: Arbeitskleidung bedrucken'))

LOGO = ('Druckdaten', 'Welche Logo-Datei <em>brauchen wir?</em>', f'''
<p><strong>Am besten eine Vektordatei</strong> – PDF, SVG, AI oder EPS. Sie lässt sich beliebig vergrößern und bleibt auf Schild, Fahrzeug und Banner scharf; für Folienschriften braucht der Schneideplotter genau diese Linien. Ein JPG oder PNG reicht für Website und kleine Drucke, wird groß aber unscharf.</p>
<p><strong>Der Zoomtest:</strong> Datei öffnen und stark hineinzoomen. Bleiben die Kanten glatt, ist es sehr wahrscheinlich Vektor; Treppchen bedeuten Pixel.</p>
<p><strong>Keine gute Datei?</strong> Fragen Sie zuerst beim Gestalter nach der offenen Datei. Gibt es sie nicht mehr, bauen wir das Logo als Vektordatei nach – den Aufwand nennen wir vorher. Bei einem neuen Logo halten wir fest, dass Sie die Nutzungsrechte und die offenen Dateien bekommen.</p>
<p>Ausführlich: <a href="/blog/logo-dateien-werbetechnik.html" {LINK}>Logo-Dateien für Schild, Folie und Druck →</a></p>''', ('/blog/logo-dateien-werbetechnik.html', 'Ratgeber: Logo-Dateien'))

SEITEN = {
    'leuchtreklame-berlin.html': LICHT,
    'leuchtreklame-nrw.html': LICHT,
    'fahrzeugbeschriftung-berlin.html': SCHEIBE,
    'fahrzeugbeschriftung-nrw.html': SCHEIBE,
    'pvc-banner-berlin.html': BANNER_B,
    'pvc-banner-nrw.html': BANNER_N,
    'textildruck-berlin.html': TEXTIL,
    'grafikdesign-berlin.html': LOGO,
}
# Nur Link-Chip in „Passend dazu“ (Seite hat schon passende Inhalte)
CHIPS = {
    'schilder-berlin.html': ('/blog/logo-dateien-werbetechnik.html', 'Ratgeber: Logo-Dateien'),
    'schilder-nrw.html': ('/blog/logo-dateien-werbetechnik.html', 'Ratgeber: Logo-Dateien'),
    'print.html': ('/blog/logo-dateien-werbetechnik.html', 'Ratgeber: Logo-Dateien'),
    'lkw-beschriftung-berlin.html': ('/blog/werbung-autoscheiben-erlaubt.html', 'Ratgeber: Werbung auf Autoscheiben'),
}


def abschnitt(ey, h2, html, faq_klasse):
    bg = ' bg-alt' if 'bg-alt' not in faq_klasse else ''
    return f'''{START}
<section class="section{bg}" id="wissen">
  <div class="container">
    <div class="sec-head reveal">
      <span class="eyebrow">{ICON}{ey}</span>
      <h2 class="sec-title">{h2}</h2>
    </div>
    <div class="blog-prose" style="max-width:820px;margin:0 auto;">{html}
    </div>
  </div>
</section>
{ENDE}
'''


def chip(s, href, text):
    if f'href="{href}" class="chip"' in s:
        return s, False
    m = re.search(r'<div class="chip-row">\n', s)
    if not m:
        return s, False
    return s[:m.end()] + f'      <a href="{href}" class="chip">{text}</a>\n' + s[m.end():], True


def main(dry=False):
    n = 0
    for f, (ey, h2, html, (href, text)) in SEITEN.items():
        p = os.path.join(ROOT, f)
        if not os.path.exists(p):
            print('fehlt', f); continue
        s = alt = open(p, encoding='utf-8').read()
        s = re.sub(re.escape(START) + r'.*?' + re.escape(ENDE) + r'\n?', '', s, flags=re.S)
        i = s.find('Häufige Fragen</span>')
        if i < 0:
            print('kein FAQ', f); continue
        j = s.rfind('<section', 0, i)
        faq_klasse = re.match(r'<section class="([^"]*)"', s[j:]).group(1)
        s = s[:j] + abschnitt(ey, h2, html, faq_klasse) + s[j:]
        s, _ = chip(s, href, text)
        if s != alt:
            n += 1
            if not dry:
                open(p, 'w', encoding='utf-8').write(s)
    for f, (href, text) in CHIPS.items():
        p = os.path.join(ROOT, f)
        if not os.path.exists(p):
            continue
        s = open(p, encoding='utf-8').read()
        s, neu = chip(s, href, text)
        if neu:
            n += 1
            if not dry:
                open(p, 'w', encoding='utf-8').write(s)
    print(f'{n} Seiten mit Wissens-Abschnitt/Ratgeber-Link aktualisiert')


if __name__ == '__main__':
    main('--dry' in sys.argv)
