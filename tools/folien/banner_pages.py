"""PVC-Banner: Berlin, NRW und Städteseiten (Generator: gen_folien.build_f)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'nrw_staedte.py'), encoding='utf-8').read()
exec(src[:src.index("\nif __name__")])

def ptab(h2, rows, col, note):
    t = table('Preise PVC-Banner', ['Produkt', 'Ausführung', col], [[r[0], r[1], f'<strong>{r[2]}</strong>'] for r in rows])
    return ('Preise auf einen Blick', h2, None, t + f'''
    <p class="price-note">{note}</p>
    <div style="text-align:center;margin-top:1.4rem"><a href="#kontakt" class="btn btn-teal">Festpreis anfragen</a></div>''')

def rows(m2, mesh, dbl, mind):
    return [('PVC-Banner (Frontlit, ca. 510 g/m²)', 'einseitig bedruckt, Saum und Ösen ca. alle 50 cm', f'ab {m2}&nbsp;€ / m²'),
            ('Mesh-Banner', 'winddurchlässig – für Gerüst, Bauzaun und Fassade', f'ab {mesh}&nbsp;€ / m²'),
            ('Blockout-Banner', 'beidseitig bedruckt, lichtundurchlässig', f'ab {dbl}&nbsp;€ / m²'),
            ('Mindestpreis je Banner', 'z. B. kleine Banner für Theke, Stand oder Zaun', f'ab {mind}&nbsp;€'),
            ('Gestaltung', 'Layout nach Ihrem Logo, Druckdaten-Check inklusive', 'ab 49&nbsp;€'),
            ('Montage', 'an Gerüst, Zaun oder Fassade', 'nach Aufwand – Festpreis')]
ROWS_B, ROWS_N = rows(29, 34, 42, 79), rows(34, 39, 48, 89)
NOTE_B = 'Alle Preise netto zzgl. 19&nbsp;% MwSt. Ihren Festpreis bekommen wir nach Maß, Stückzahl und Ausführung – in der Regel innerhalb von 24 Stunden.'
NOTE_N = 'Alle Preise netto zzgl. 19&nbsp;% MwSt. Ihren Festpreis inklusive Lieferung oder Montage durch unser Team in NRW bekommen Sie nach Maß und Stückzahl – in der Regel innerhalb von 24 Stunden.'

TIPPS = '''<p><strong>Ösen oder ohne?</strong> Ösen brauchen Sie, wenn das Banner mit Kabelbindern oder Seilen an Zaun, Gerüst oder Geländer befestigt wird – Standard ist etwa alle 50&nbsp;cm. Ohne Ösen, dafür mit Hohlsaum oder Keder, eignet sich das Banner für Stangen, Rahmen und Spannsysteme.</p>
<p><strong>PVC oder Mesh?</strong> Draußen an Gerüst oder Bauzaun drückt der Wind stark auf eine geschlossene Fläche. Mesh-Banner sind gelocht und lassen Wind durch – bei großen Flächen im Freien ist das die sicherere Wahl.</p>
<p><strong>Brandschutz:</strong> Für Messen, Veranstaltungsräume und öffentliche Gebäude wird oft schwer entflammbares Material (B1 nach DIN 4102) verlangt. Sagen Sie uns, wo das Banner hängt – wir wählen das passende Material.</p>
<p><strong>Druckdaten:</strong> Ideal sind Vektordaten oder ein PDF im Endformat. Schicken Sie uns einfach, was Sie haben – wir prüfen die Daten vor dem Druck oder gestalten das Banner für Sie.</p>'''
RECHT_B = '''<p><strong>Werbung im Freien:</strong> Ein Banner an Fassade, Gerüst oder Bauzaun kann als Werbeanlage gelten. Je nach Größe, Dauer und Lage kann eine Genehmigung nötig sein; ragt es in den öffentlichen Straßenraum, kommt eine Sondernutzungserlaubnis dazu. Wir sagen Ihnen vorher, worauf Sie achten müssen.</p>'''
RECHT_N = '''<p><strong>Werbung im Freien in NRW:</strong> Werbeanlagen bis 1&nbsp;m² und Werbung für zeitlich begrenzte Aktionen bis zu zwei Monate sind nach § 62 BauO NRW in der Regel verfahrensfrei (nicht im Außenbereich). Größere oder dauerhafte Banner an der Fassade können genehmigungspflichtig sein; örtliche Satzungen gelten zusätzlich.</p>
<p style="font-size:13px;">Quelle: <a href="https://www.dortmund.de/dortmund/projekte/rathaus/verwaltung/stadtplanungs-und-bauordnungsamt/downloads/bauordnung/infoblaetter/infoblatt_werbeanlagen.pdf" target="_blank" rel="noopener noreferrer">Stadt Dortmund – Infoblatt Werbeanlagen</a>. Allgemeine Hinweise, keine Rechtsberatung.</p>'''

B = dict(finder_strip=False, hero_mobile=True, file='pvc-banner-berlin.html', crumb='PVC-Banner', img='pvc-banner', tab_ey='Einsatz',
 parent=('Werbetechnik', 'werbetechnik.html'), area=[{"@type": "City", "name": "Berlin"}],
 img_alt='PVC-Banner mit und ohne Ösen – robust, wetterfest, in individuellen Größen',
 title='PVC-Banner Berlin: Banner drucken mit Ösen | Masar',
 desc='PVC-Banner in Berlin ab 29 €/m² netto: wetterfest, mit oder ohne Ösen, Mesh-Banner für Gerüst und Bauzaun – Gestaltung und Montage aus einer Hand.',
 service_type='Bannerdruck', schema_name='PVC-Banner in Berlin',
 badge='PVC-Banner · Berlin', h1='PVC-Banner <em>Berlin</em>',
 sub='Wetterfeste Banner für Fassade, Bauzaun, Messestand, Eröffnung oder Event – mit Ösen, Hohlsaum oder ganz ohne. Wir gestalten, drucken und hängen Ihr Banner auf Wunsch bei Ihnen in Berlin auf.',
 trust='PVC-Banner ab 29 € / m² netto · Mesh · Blockout · Gestaltung & Montage',
 usp=['Wetterfest innen & außen', 'Mit oder ohne Ösen', 'Jede Größe', 'Angebot in 24 h'],
 wa='Hallo, ich interessiere mich für ein PVC-Banner. Größe: ',
 angles_ey='Warum ein Banner', angles_h2='Groß, günstig, <em>schnell sichtbar</em>',
 angles_sub='Kaum ein Werbemittel bringt so viel Fläche für so wenig Geld.',
 angles=[
  ('Große Wirkung', 'Ein Banner am Zaun oder an der Fassade ist schon von weitem lesbar – ideal für Neueröffnung, Aktion, Baustelle oder Stellenanzeige.'),
  ('Wetterfest', 'PVC-Banner halten Regen, Wind und Sonne stand und lassen sich mehrfach verwenden – drinnen wie draußen.'),
  ('Flexibel', 'Jede Größe, mit Ösen, Hohlsaum oder Keder, ein- oder beidseitig bedruckt – passend zu Ort und Befestigung.'),
  ('Aus einer Hand', 'Gestaltung, Druck und auf Wunsch Montage – Sie müssen sich um nichts selbst kümmern.'),
 ],
 tab_h2='Wofür eignet sich <em>welches Banner?</em>', tab_sub='Die richtige Wahl hängt vom Ort und von der Befestigung ab.',
 tab_cols=['Einsatz', 'Empfehlung', 'Befestigung'],
 tab_rows=[
  ['Bauzaun, Gerüst', 'Mesh-Banner (winddurchlässig)', 'Ösen + Kabelbinder'],
  ['Fassade, Geländer', 'PVC-Banner oder Mesh, je nach Größe', 'Ösen, Spannseil oder Rahmen'],
  ['Messe, Event, Innenraum', 'PVC-Banner, schwer entflammbar (B1)', 'Ösen, Hohlsaum oder Keder'],
  ['Freistehend, von beiden Seiten sichtbar', 'Blockout-Banner, beidseitig bedruckt', 'Hohlsaum oder Rahmen'],
  ['Eröffnung, Aktion', 'PVC-Banner, einseitig', 'Ösen'],
 ],
 tab_note='Für Messen siehe auch <a href="/messebeschriftung-berlin.html">Messebeschriftung</a> und <a href="/messebau-berlin.html">Messebau</a>. Banner in NRW: <a href="/pvc-banner-nrw.html">PVC-Banner NRW</a>.',
 svc_h2='Banner <em>für jeden Zweck</em>', svc_sub='Druck, Verarbeitung und Montage aus einer Hand.',
 services=[
  ('druck', 'PVC-Banner', 'Frontlit-Banner, einseitig bedruckt, mit Saum und Ösen.', '#kontakt'),
  ('stern', 'Mesh-Banner', 'Gelochtes Material für Gerüst, Bauzaun und große Fassaden.', '#kontakt'),
  ('schild', 'Blockout-Banner', 'Beidseitig bedruckt, lichtundurchlässig.', '#kontakt'),
  ('karte', 'Messe & Event', 'Schwer entflammbare Banner für Stand, Bühne und Innenraum.', '/messebeschriftung-berlin.html'),
  ('web', 'Gestaltung', 'Layout nach Ihrem Logo – gut lesbar aus der Entfernung.', '/grafikdesign-berlin.html'),
  ('weg', 'Montage', 'Wir hängen das Banner bei Ihnen auf – sicher und gerade.', '#kontakt'),
 ],
 preis_h2='Gut zu <em>wissen</em>', preis_html=TIPPS,
 recht_ey='Genehmigung', recht_h2='Banner <em>im Freien</em>', recht_sub=None, recht_html=RECHT_B,
 ablauf=[
  ('Maß & Wunsch', 'Sie sagen uns Größe, Stückzahl, Ort und Befestigung – per WhatsApp, E-Mail oder Formular.'),
  ('Gestaltung', 'Wir gestalten das Banner oder prüfen Ihre Druckdaten und schicken Ihnen eine Vorschau.'),
  ('Festpreis', 'Sie bekommen ein schriftliches Angebot mit Material, Verarbeitung und Lieferzeit.'),
  ('Druck & Montage', 'Nach Freigabe drucken wir; auf Wunsch hängen wir das Banner bei Ihnen auf.'),
 ],
 faq_h2='PVC-Banner – <em>Fragen &amp; Antworten</em>',
 faq=[
  ('Was kostet ein PVC-Banner?', 'PVC-Banner gibt es bei uns ab 29 € pro m² netto zzgl. 19 % MwSt., inklusive Saum und Ösen. Mesh-Banner beginnen bei 34 € pro m², beidseitig bedruckte Blockout-Banner bei 42 € pro m². Der Mindestpreis je Banner liegt bei 79 € netto.'),
  ('Wie weit sind die Ösen auseinander?', 'Standard ist etwa alle 50 cm. Für starke Beanspruchung, etwa an Gerüsten, setzen wir die Ösen enger. Sagen Sie uns, wie das Banner befestigt wird.'),
  ('Brauche ich ein Mesh-Banner?', 'Für große Banner im Freien – an Gerüst, Bauzaun oder Fassade – empfehlen wir Mesh, weil der Wind durch das gelochte Material gehen kann. Für kleinere Banner und innen reicht PVC.'),
  ('Ist das Material schwer entflammbar?', 'Für Messen und Veranstaltungsräume verwenden wir schwer entflammbares Material (B1). Sagen Sie uns, wo das Banner hängt.'),
  ('Können Sie das Banner gestalten?', 'Ja. Ihr Logo reicht. Wir gestalten das Banner so, dass es aus der Entfernung gut lesbar ist, und schicken Ihnen vorher eine Vorschau.'),
  ('Hängen Sie das Banner auch auf?', 'Ja, in Berlin montieren wir auf Wunsch – an Zaun, Gerüst, Geländer oder Fassade. Den Preis nennen wir Ihnen im Angebot.'),
 ],
 links=[('/werbetechnik.html', 'Werbetechnik'), ('/messebeschriftung-berlin.html', 'Messebeschriftung'), ('/print.html', 'Druckerei'), ('/aussenwerbung-berlin.html', 'Außenwerbung'), ('/pvc-banner-nrw.html', 'PVC-Banner NRW')],
 form_opts=['PVC-Banner mit Ösen', 'PVC-Banner ohne Ösen (Hohlsaum/Keder)', 'Mesh-Banner', 'Blockout-Banner (beidseitig)', 'Mehrere Banner'],
 form_labels=('Welches Banner?', 'Größe, Stückzahl &amp; Ort', 'Druckdaten oder Logo (optional)', 'Vektordatei oder PDF im Endformat ist ideal – aber jedes Logo oder Foto reicht für den Anfang.'),
 form_sub='Sagen Sie uns Größe, Stückzahl und wo das Banner hängt – Sie bekommen innerhalb von 24 Stunden ein Angebot.',
 subject='Anfrage PVC-Banner Berlin (Website)', msg_ph='z. B. 2 Banner 3 × 1 m für den Bauzaun, Ösen alle 50 cm, Logo und Telefonnummer, Baustelle in Berlin-Pankow',
 sticky=('PVC-Banner Berlin', 'ab 29 € / m² netto'))
B['top'] = ptab('Was kostet <em>ein PVC-Banner?</em>', ROWS_B, 'Preis', NOTE_B)

N = dict(B)
N.update(file='pvc-banner-nrw.html', crumb='PVC-Banner NRW', parent=('Werbeagentur NRW', 'werbeagentur-nrw.html'), area=AREA,
 title='PVC-Banner NRW: Banner drucken mit Ösen | Masar',
 desc='PVC-Banner in NRW ab 34 €/m² netto: wetterfest, mit oder ohne Ösen, Mesh-Banner für Düsseldorf, Köln und das Ruhrgebiet – Montage vor Ort.',
 schema_name='PVC-Banner in NRW', badge='PVC-Banner · NRW', h1='PVC-Banner <em>NRW</em>',
 sub='Wetterfeste Banner für Fassade, Bauzaun, Eröffnung oder Event in ganz NRW – ob Köln, Düsseldorf, Dortmund, Essen, Bochum oder Duisburg. Mit Ösen, Hohlsaum oder ganz ohne. Wir gestalten und drucken, unser Team in NRW hängt das Banner auf Wunsch bei Ihnen auf.',
 trust='PVC-Banner ab 34 € / m² netto · Düsseldorf · Köln · Ruhrgebiet',
 usp=['Team vor Ort in NRW', 'Mit oder ohne Ösen', 'Jede Größe', 'Angebot in 24 h'],
 wa='Hallo, ich interessiere mich für ein PVC-Banner in NRW. Größe: ',
 tab_note='Für Werbung am Fahrzeug siehe <a href="/fahrzeugbeschriftung-nrw.html">Fahrzeugbeschriftung NRW</a>. Banner in Berlin: <a href="/pvc-banner-berlin.html">PVC-Banner Berlin</a>.',
 services=[s for s in B['services'] if s[1] != 'Messe & Event'] + [('licht', 'Leuchtreklame', 'Für dauerhafte Werbung an der Fassade: Leuchtreklame in NRW.', '/leuchtreklame-nrw.html')],
 recht_html=RECHT_N,
 faq_h2='PVC-Banner NRW – <em>Fragen &amp; Antworten</em>',
 faq=[('In welchen Städten liefern und montieren Sie Banner?', 'In ganz NRW – Schwerpunkt Düsseldorf, Köln, Dortmund, Essen und Bochum, dazu Duisburg, Wuppertal, Bonn und die Städte dazwischen. Unser Team in NRW montiert vor Ort. Unser Firmensitz ist in Berlin.'),
      ('Was kostet ein PVC-Banner in NRW?', 'PVC-Banner gibt es in NRW ab 34 € pro m² netto zzgl. 19 % MwSt., inklusive Saum und Ösen. Mesh-Banner ab 39 € pro m², Blockout-Banner ab 48 € pro m², Mindestpreis je Banner 89 € netto.')] + B['faq'][1:5] + [('Brauche ich für ein Banner eine Genehmigung?', 'Werbung für zeitlich begrenzte Aktionen bis zu zwei Monate und Werbeanlagen bis 1 m² sind in NRW in der Regel verfahrensfrei. Für größere, dauerhafte Banner an der Fassade kann eine Genehmigung nötig sein. Wir sagen Ihnen vorher, worauf Sie achten müssen.')],
 links=[('/werbeagentur-nrw.html', 'Werbeagentur NRW')] + [(f'/werbeagentur-{k}.html', f'Werbeagentur {v["name"]}') for k, v in C.items()] + [('/leuchtreklame-nrw.html', 'Leuchtreklame NRW')],
 form_sub='Sagen Sie uns Größe, Stückzahl und wo das Banner hängt – Sie bekommen innerhalb von 24 Stunden ein Angebot. Unser Team in NRW montiert auf Wunsch vor Ort.',
 subject='Anfrage PVC-Banner NRW (Website)', msg_ph='z. B. 2 Banner 3 × 1 m für den Bauzaun, Ösen alle 50 cm, Baustelle in Duisburg',
 sticky=('PVC-Banner NRW', 'ab 34 € / m² netto'), nrw=True, ph='Duisburg')
N['top'] = ptab('Was kostet <em>ein PVC-Banner in NRW?</em>', ROWS_N, 'Preis NRW', NOTE_N)

# Abschnitt „Banner zur Neueröffnung“ (nur Berlin, Anker #neueroeffnung) – SEO-Chancen 07.11.2026, Maßnahme 6.
# Keine neuen Preise: nur die m²-Preise und der Mindestpreis aus der Preistabelle oben.
NEUER = ('Neueröffnung', 'Banner zur <em>Neueröffnung</em>',
 'Solange umgebaut wird, sieht man von außen nur Papier im Fenster oder einen Bauzaun. Ein Banner sagt schon vorher, was hier bald aufmacht.',
 '''    <div class="blog-prose" style="max-width:820px;margin:0 auto;">
<p><strong>Vorher: „Bald hier“.</strong> Ein Banner mit Name, Logo und „Eröffnung am …“ am Bauzaun, am Gerüst oder innen hinter der Schaufensterscheibe macht Nachbarn und Passanten schon während des Umbaus neugierig. Am Zaun oder Gerüst nehmen wir Mesh mit Ösen, hinter der Scheibe reicht PVC. Soll die Werbung direkt aufs Glas, ist eine <a href="/schaufensterbeschriftung-berlin.html" style="color:var(--teal-ink);font-weight:700;">Schaufensterbeschriftung</a> die bessere Wahl.</p>
<p><strong>Am großen Tag: das Eröffnungsbanner.</strong> Wenig Text, große Schrift: Name, „Neueröffnung“, Datum und höchstens ein Angebot. Mehr liest im Vorbeigehen niemand. Wir gestalten das Banner so, dass es aus der Entfernung lesbar ist, und schicken Ihnen vorher eine Vorschau.</p>
<p><strong>Draußen bei Wind: Mesh.</strong> Ein geschlossenes Banner am Bauzaun oder an der Fassade fängt viel Wind. Mesh ist gelocht und lässt ihn durch – für große Flächen im Freien die sicherere Wahl.</p>
    </div>
    <div class="price-scroll" style="max-width:820px;margin:1.4rem auto 0;">
      <table class="price-table rt">
        <caption class="sr-only" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);">Beispielgrößen für Banner zur Neueröffnung</caption>
        <thead><tr><th scope="col">Einsatz</th><th scope="col">Größe zum Beispiel</th><th scope="col">Material</th></tr></thead>
        <tbody>
          <tr><td data-label="Einsatz">Hinter der Schaufensterscheibe</td><td data-label="Größe">2 × 1 m</td><td data-label="Material">PVC-Banner, einseitig</td></tr>
          <tr><td data-label="Einsatz">Bauzaunfeld</td><td data-label="Größe">3 × 1 m</td><td data-label="Material">Mesh-Banner mit Ösen</td></tr>
          <tr><td data-label="Einsatz">Fassade über dem Eingang</td><td data-label="Größe">4 × 1 m</td><td data-label="Material">PVC oder Mesh, je nach Wind</td></tr>
          <tr><td data-label="Einsatz">Freistehend, von beiden Seiten sichtbar</td><td data-label="Größe">2 × 1 m</td><td data-label="Material">Blockout-Banner, beidseitig</td></tr>
        </tbody>
      </table>
    </div>
    <div class="blog-prose" style="max-width:820px;margin:1.4rem auto 0;">
<p><strong>Was es kostet:</strong> Berechnet wird nach Fläche – PVC-Banner ab 29&nbsp;€ / m² netto, Mesh ab 34&nbsp;€ / m² netto, Blockout ab 42&nbsp;€ / m² netto, mindestens 79&nbsp;€ netto je Banner. Die Größen oben sind nur Beispiele – jedes Maß ist möglich. Ihren Festpreis bekommen Sie mit dem Angebot.</p>
<p><strong>Zeitplan:</strong> Bestellen Sie das „Bald hier“-Banner, sobald Name und Eröffnungstag feststehen – je länger es hängt, desto mehr Menschen sehen es. Das Eröffnungsbanner können Sie gleich mitbestellen, dann passt alles zusammen. Den Liefertermin nennen wir Ihnen im Angebot.</p>
<p><strong>Genehmigung:</strong> Ob ein Banner an Fassade oder Zaun genehmigungsfrei ist, hängt von Größe, Ort und Dauer ab. Prüfen Sie das vorab mit dem <a href="/genehmigungs-check.html" style="color:var(--teal-ink);font-weight:700;">kostenlosen Genehmigungs-Check</a> – oder fragen Sie uns.</p>
<p>Was zur Eröffnung sonst noch dazugehört – Schild, Schaufenster, Flyer: <a href="/blog/ladeneroeffnung-werbung-checkliste.html" style="color:var(--teal-ink);font-weight:700;">Checkliste: Werbung zur Ladeneröffnung →</a></p>
    </div>''')
B['extra'] = NEUER   # nach N = dict(B) gesetzt: gilt nur für Berlin

PAGES_B = [B, N]
# Städteseiten PVC-Banner am 13.10.2026 in pvc-banner-nrw.html zusammengeführt (301 in .htaccess)
for k, c in ({} if True else C).items():
    n = c['name']
    p = dict(N)
    p.update(file=f'pvc-banner-{k}.html', crumb=f'PVC-Banner {n}', parent=(f'Werbeagentur {n}', c['hub']), area=[{"@type": "City", "name": n}],
     title=f'PVC-Banner {n}: Banner drucken mit Ösen | Masar',
     desc=f'PVC-Banner in {n} ab 34 €/m² netto: wetterfest, mit oder ohne Ösen, Mesh für Gerüst und Bauzaun – Druck und Montage vor Ort.',
     schema_name=f'PVC-Banner in {n}', badge=f'PVC-Banner · {n}', h1=f'PVC-Banner <em>{n}</em>',
     sub=f'Wetterfeste Banner für Läden, Baustellen, Events und Vereine in {n} – von {c["lagen"]} bis {c["veedel"]}. Wir gestalten und drucken, unser Team in NRW hängt das Banner auf Wunsch bei Ihnen auf.',
     trust=f'PVC-Banner ab 34 € / m² netto · Montage in {n}',
     wa=f'Hallo, ich interessiere mich für ein PVC-Banner in {n}. Größe: ',
     angles_h2=f'Sichtbar in {n} – <em>groß und günstig</em>',
     angles=[('Große Wirkung', f'Ob Neueröffnung in {c["lagen"].split(" und ")[0]}, Baustelle in {c["veedel"].split(",")[0]} oder Betrieb {c["gewerbe"]}: Ein Banner ist schon von weitem lesbar.')] + B['angles'][1:],
     faq_h2=f'PVC-Banner {n} – <em>Fragen &amp; Antworten</em>',
     faq=[(f'Liefern und montieren Sie Banner in ganz {n}?', f'Ja. Unser Team in NRW kommt zu Ihnen – zum Beispiel nach {c["veedel"]}. Unser Firmensitz ist in Berlin.')] + N['faq'][1:],
     links=[('/pvc-banner-nrw.html', 'PVC-Banner NRW'), ('/' + c['hub'], f'Werbeagentur {n}'), (f'/schaufensterbeschriftung-{k}.html', f'Schaufenster {n}'), (f'/leuchtreklame-{k}.html', f'Leuchtreklame {n}')] + [(f'/pvc-banner-{kk}.html', f'PVC-Banner {vv["name"]}') for kk, vv in C.items() if kk != k],
     form_sub=f'Sagen Sie uns Größe, Stückzahl und wo das Banner hängt – Sie bekommen innerhalb von 24 Stunden ein Angebot. Unser Team montiert bei Ihnen in {n}.',
     subject=f'Anfrage PVC-Banner {n} (Website)', msg_ph=f'z. B. 2 Banner 3 × 1 m für den Bauzaun, Ösen alle 50 cm, Baustelle in {c["ph"]}',
     sticky=(f'PVC-Banner {n}', 'ab 34 € / m² netto'), ph=c['ph'])
    p['top'] = ptab(f'Was kostet <em>ein PVC-Banner in {n}?</em>', ROWS_N, 'Preis NRW', NOTE_N)
    PAGES_B.append(p)

if __name__ == '__main__':
    for p in PAGES_B:
        r = build_f(p)
        if p.get('extra') is NEUER:
            # build_f setzt für „extra“ keine id – Anker #neueroeffnung hier ergänzen
            h = open(ROOT + p['file'], encoding='utf-8').read()
            i = h.rindex('<section class="section"', 0, h.index('Banner zur <em>Neueröffnung</em>'))
            h = h[:i] + '<section id="neueroeffnung" class="section"' + h[i + len('<section class="section"'):]
            open(ROOT + p['file'], 'w', encoding='utf-8').write(h)
        if p.get('nrw'):
            nrw_fix(p)
            h = open(ROOT + p['file'], encoding='utf-8').read().replace('placeholder="z. B. Köln-Ehrenfeld"', f'placeholder="z. B. {p["ph"]}"')
            open(ROOT + p['file'], 'w', encoding='utf-8').write(h)
        print(r)
