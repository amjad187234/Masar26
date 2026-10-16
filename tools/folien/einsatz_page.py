"""Zentrale Seite „Einsatzgebiete & Unternehmen“: Standort, Leistungen je Region, alle Stadtseiten, FAQ."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, '..', 'branchen', 'gen_branchen.py'), encoding='utf-8').read()
exec(src[:src.index('\nimport pages')])
us = open(os.path.join(HERE, 'umland_pages.py'), encoding='utf-8').read()
exec(us[us.index('CITIES = ['):us.index('NRW_NEAR')])

F = 'einsatzgebiete.html'; URL = BASE + F
TITLE = 'Einsatzgebiete: Berlin, Brandenburg & NRW | Masar'
DESC = 'Masar Werbeagentur: Studio in Berlin-Wedding, Einsatz in Berlin, Brandenburg und NRW (Montageteam, keine Filiale). Welche Leistung wo – mit allen Stadtseiten.'
FAQ = [
 ('Wo sitzt Masar Werbeagentur?', 'Unser Studio mit Werkstatt ist in der Bristolstraße 19E, 13349 Berlin-Wedding. Das ist unser einziger Standort. Besuche nach Terminvereinbarung, Montag bis Samstag 08:00–20:00 Uhr.'),
 ('Haben Sie eine Niederlassung in NRW?', 'Nein. In Nordrhein-Westfalen arbeitet ein eigenes Montageteam für uns, das Aufmaß, Montage und Beschriftung vor Ort übernimmt. Anfragen aus NRW laufen über dieselbe Nummer, dieselbe E-Mail und denselben Anfrage-Assistenten.'),
 ('Welche Leistungen gibt es nur in Berlin?', 'Messebau und Expressdruck (Druck und Folie am selben Tag) bieten wir nur in Berlin an. Foto- und Videoaufnahmen machen wir in Berlin, nicht in NRW.'),
 ('Kostet die Anfahrt nach Brandenburg extra?', 'Die Anfahrt ist im Festpreis enthalten und dort einzeln ausgewiesen. Sie wissen vorher genau, was Sie zahlen. Für reine Druck- und Designaufträge fällt keine Anfahrt an.'),
 ('Gelten in NRW andere Preise?', 'Ja. In NRW arbeitet ein eigenes Montageteam vor Ort, deshalb liegen die Startpreise dort leicht über Berlin – zum Beispiel Firmenschild ab 179 € statt ab 149 € netto, LED-Leuchtbuchstaben ab 229 € statt ab 199 € pro Buchstabe.'),
 ('Wie schnell bekomme ich ein Angebot?', 'In der Regel innerhalb von 24 Stunden. Ein Foto vom Ort und Ihr Logo reichen für ein erstes Angebot; den verbindlichen Festpreis nennen wir nach Fotos oder Aufmaß.'),
 ('In welchen Sprachen beraten Sie?', 'Auf Deutsch, Englisch, Arabisch und Türkisch.'),
]
ROWS = [
 ('Schilder & Leuchtreklame', '✓', '✓', '✓ (Montageteam)'),
 ('Schaufenster & Fensterfolien', '✓', '✓', '✓ (Montageteam)'),
 ('Fahrzeug- & LKW-Beschriftung', '✓', '✓', '✓ (Montageteam)'),
 ('PVC-Banner & Druck', '✓', '✓ (Lieferung/Montage)', '✓ (Lieferung/Montage)'),
 ('Expressdruck am selben Tag', '✓', '–', '–'),
 ('Messebau', '✓ (Berliner Messen)', '–', '–'),
 ('Foto & Video', '✓', 'auf Anfrage', '–'),
 ('Grafikdesign, Webdesign, Social Media, KI', '✓', '✓ (online)', '✓ (online)'),
]
PRICES = [('Firmenschild (Alu-Dibond)', 'ab 149 €', 'ab 179 €'), ('LED-Leuchtbuchstaben', 'ab 199 € / Buchstabe', 'ab 229 € / Buchstabe'),
          ('Schaufensterbeschriftung', 'ab 149 €', 'ab 179 €'), ('Sichtschutzfolie', 'ab 190 €', 'ab 229 €'),
          ('Fahrzeug-Teilbeschriftung', 'ab 290 €', 'ab 340 €'), ('PVC-Banner', 'ab 19 € / m²', 'ab 22 € / m²')]

def build():
    js = lambda o: '<script type="application/ld+json">\n' + json.dumps(o, ensure_ascii=False, indent=2) + '\n</script>\n'
    page = {"@context": "https://schema.org", "@type": "WebPage", "@id": URL + "#webpage", "url": URL, "name": TITLE, "description": DESC,
            "about": {"@id": BASE + "#identity"}, "inLanguage": "de"}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
          {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE}, {"@type": "ListItem", "position": 2, "name": "Einsatzgebiete", "item": URL}]}
    fq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
          {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    t, d = esc(TITLE), esc(DESC)
    meta = f'''<title>{t}</title>
<meta name="description" content="{d}">
<meta name="robots" content="index, follow">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{URL}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://masar-werbeagentur.de/logo.png">
<meta property="og:locale" content="de_DE">
<meta property="og:site_name" content="Masar Werbeagentur Berlin">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="https://masar-werbeagentur.de/logo.png">
<link rel="canonical" href="{URL}">
<link rel="alternate" hreflang="de" href="{URL}">
<link rel="alternate" hreflang="x-default" href="{URL}">
'''
    css = '''<style>
.eg-fact{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:1rem}
.eg-fact div{background:#fff;border:1px solid var(--border);border-radius:var(--r);padding:1.1rem 1.2rem}
.eg-fact b{display:block;color:var(--navy);font-size:15px;margin-bottom:.25rem}.eg-fact span{color:var(--muted);font-size:15px;line-height:1.55}
.eg-city{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:.7rem}
.eg-city a{display:block;background:#fff;border:1px solid var(--border);border-radius:10px;padding:.8rem 1rem;text-decoration:none;color:var(--navy);font-weight:700}
.eg-city a small{display:block;font-weight:400;color:var(--muted);font-size:13px;margin-top:.15rem}
.eg-city a:hover{border-color:var(--teal)}
</style>'''
    def tbl(cols, rows, cap):
        th = ''.join(f'<th scope="col">{c}</th>' for c in cols)
        tr = ''.join('<tr>' + ''.join(f'<td data-label="{cols[i]}">{v}</td>' for i, v in enumerate(r)) + '</tr>' for r in rows)
        return f'<div class="price-scroll"><table class="price-table rt"><caption class="sr-only" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);">{cap}</caption><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
    bb = ''.join(f'<a href="/werbeagentur-{c["slug"]}.html">{c["name"]}<small>{c["kreis"]}{"" if c["km"] in (0, None) else " · ca. " + str(c["km"]) + " km"}</small></a>' for c in CITIES)
    nrw_c = [('werbeagentur-koeln', 'Köln'), ('werbeagentur-duesseldorf', 'Düsseldorf'), ('werbeagentur-dortmund', 'Dortmund'), ('werbeagentur-essen', 'Essen'),
             ('werbeagentur-bochum', 'Bochum'), ('werbeagentur-herne', 'Herne'), ('werbeagentur-muelheim', 'Mülheim an der Ruhr'), ('werbeagentur-bottrop', 'Bottrop')]
    nn = ''.join(f'<a href="/{u}.html">{n}<small>Montageteam NRW</small></a>' for u, n in nrw_c)
    w = wa('Hallo, ich habe eine Anfrage: ')
    body = f'''<section class="hero" id="main-content" role="main" tabindex="-1" style="min-height:auto;padding-bottom:3rem">
  <div class="hero-lines"></div>
  <div class="container"><div style="max-width:820px">
    <div class="hero-badge">{I['star']}Standort &amp; Einsatzgebiete</div>
    <h1>Wo wir <em>für Sie arbeiten</em></h1>
    <p class="hero-sub">Masar Werbeagentur hat einen Standort: unser Studio mit Werkstatt in Berlin-Wedding. Von hier aus arbeiten wir in Berlin und Brandenburg; für Werbetechnik, Druck und Design in Nordrhein-Westfalen gibt es ein eigenes Montageteam – ohne Niederlassung.</p>
    <div class="hero-btns"><a href="#anfrage" class="btn btn-teal">Anfrage starten</a><a href="{w}" target="_blank" rel="noopener noreferrer" class="btn btn-outline">{I['wa']}WhatsApp</a></div>
  </div></div>
</section>
<nav aria-label="Breadcrumb" class="bc-bar"><div class="container"><ol class="bc-list"><li><a href="/">Home</a></li><li class="bc-sep">/</li><li><span class="bc-cur">Einsatzgebiete</span></li></ol></div></nav>
'''
    body += sec('Auf einen Blick', 'Masar Werbeagentur <em>– das Unternehmen</em>', None, f'''    <div class="eg-fact">
      <div><b>Standort</b><span>Bristolstraße 19E, 13349 Berlin-Wedding – Studio und Werkstatt, unser einziger Standort.</span></div>
      <div><b>Inhaber</b><span>Amjad Alblili, Mediengestalter</span></div>
      <div><b>Kontakt</b><span>Telefon / WhatsApp 0178 514 3918<br>info@masar-werbeagentur.de</span></div>
      <div><b>Erreichbar</b><span>Montag bis Samstag, 08:00–20:00 Uhr; Besuche vor Ort nach Vereinbarung</span></div>
      <div><b>Sprachen</b><span>Deutsch, Englisch, Arabisch, Türkisch</span></div>
      <div><b>Arbeitsweise</b><span>Gestaltung, Produktion und Montage aus einer Hand; Angebot in der Regel innerhalb von 24 Stunden; Preise netto zzgl. 19&nbsp;% MwSt.</span></div>
    </div>
    <div class="blog-prose" style="max-width:820px;margin:1.6rem auto 0">
      <p>Wir machen Werbetechnik und Design für Unternehmen: <a href="/schilder-berlin.html">Schilder</a>, <a href="/leuchtreklame-berlin.html">Leuchtreklame</a>, <a href="/fahrzeugbeschriftung-berlin.html">Fahrzeug-</a> und <a href="/lkw-beschriftung-berlin.html">LKW-Beschriftung</a>, <a href="/schaufensterbeschriftung-berlin.html">Schaufensterbeschriftung</a>, <a href="/fensterfolie-berlin.html">Fensterfolien</a> (Sonnenschutz, Sichtschutz, Sicherheit), <a href="/pvc-banner-berlin.html">PVC-Banner</a>, <a href="/print.html">Druck</a>, <a href="/grafikdesign-berlin.html">Grafikdesign</a>, <a href="/webdesign-berlin.html">Webdesign</a>, <a href="/digital.html">Social Media</a>, <a href="/messebau-berlin.html">Messebau</a>, <a href="/digital-signage-berlin.html">Digital Signage</a> und <a href="/ki-loesungen/">KI-Lösungen</a>. Eigene Arbeiten zeigen wir unter <a href="/referenzen.html">Referenzen</a>.</p>
    </div>''', icon='check')
    body += sec('Leistungen je Region', 'Was wir <em>wo anbieten</em>', 'Nicht jede Leistung gibt es überall – hier steht, was gilt.', tbl(['Leistung', 'Berlin', 'Brandenburg', 'NRW'], ROWS, 'Leistungen je Region') + '<p class="price-note">Montageteam NRW: Aufmaß, Montage und Beschriftung vor Ort – unser Firmensitz bleibt Berlin.</p>', alt=True, icon='tag')
    body += sec('Preise', 'Berlin &amp; Brandenburg <em>oder NRW</em>', 'Startpreise netto zzgl. 19 % MwSt.; Festpreis nach Fotos oder Aufmaß.', tbl(['Leistung', 'Berlin & Brandenburg', 'NRW'], PRICES, 'Startpreise je Region') + '<p class="price-note">Bei Montage außerhalb Berlins ist die Anfahrt im Festpreis enthalten und einzeln ausgewiesen.</p>', icon='tag')
    body += sec('Berlin', 'Berlin <em>– alle Bezirke</em>', 'Von unserem Studio im Wedding sind wir in der ganzen Stadt unterwegs.', '''    <div class="blog-prose" style="max-width:820px;margin:0 auto"><p>Mitte, Friedrichshain-Kreuzberg, Pankow, Charlottenburg-Wilmersdorf, Spandau, Steglitz-Zehlendorf, Tempelhof-Schöneberg, Neukölln, Treptow-Köpenick, Marzahn-Hellersdorf, Lichtenberg und Reinickendorf. Mehr zu unserem Standort: <a href="/werbetechnik-berlin-wedding.html">Werbetechnik Berlin-Wedding</a>.</p></div>''', alt=True, icon='check')
    body += sec('Brandenburg', 'Brandenburg <em>&amp; Berliner Umland</em>', 'Betreut aus Berlin – Montage vor Ort.', f'    <div class="eg-city"><a href="/werbetechnik-potsdam.html">Potsdam<small>Landeshauptstadt</small></a><a href="/werbetechnik-brandenburg.html">Brandenburg – Übersicht<small>alle Regionen</small></a>{bb}</div>', icon='check')
    body += sec('Nordrhein-Westfalen', 'NRW <em>– mit eigenem Montageteam</em>', 'Keine Niederlassung, aber ein Team vor Ort. Messebau, Expressdruck und Foto/Video bieten wir in NRW nicht an.', f'    <div class="eg-city"><a href="/werbeagentur-nrw.html">Werbeagentur NRW<small>Übersicht</small></a>{nn}</div>', alt=True, icon='check')
    fqh = ''.join(f'\n      <div class="faq-item"><button class="faq-q">{q}</button><div class="faq-a"><p>{a}</p></div></div>' for q, a in FAQ)
    body += sec('Häufige Fragen', 'Standort &amp; Einsatz – <em>Fragen &amp; Antworten</em>', None, f'    <div class="faq-wrap">{fqh}\n    </div>', icon='faq')
    body += f'''<section class="section bg-alt" id="anfrage"><div class="container">
  <div class="sec-head center reveal"><span class="eyebrow">{I['mail']}Anfrage</span><h2 class="sec-title">Ihr Projekt – <em>in wenigen Klicks</em></h2></div>
  <div data-assistent></div>
  <noscript><p style="text-align:center">Schreiben Sie uns an <a href="mailto:info@masar-werbeagentur.de">info@masar-werbeagentur.de</a> oder per <a href="{w}">WhatsApp</a>.</p></noscript>
</div></section>
{'' if 'assistent.js' in FOOT else '<script src="/assistent.js?v=6" defer></script>'}
'''
    out = HEAD_A + meta + js(page) + js(bc) + js(fq) + HEAD_B
    out = out.replace('</head>', css + '\n</head>', 1) + body + '\n' + FOOT
    import re as _re
    out = _re.sub(r'<div class="scta-txt">.*?</div>', f'<div class="scta-txt">{I["star"]}<span>Masar Werbeagentur</span> – Berlin, Brandenburg &amp; NRW</div>', out, count=1, flags=_re.S)
    open(ROOT + F, 'w', encoding='utf-8').write(out)
    return F, len(out), len(TITLE), len(DESC)

if __name__ == '__main__':
    print(build())
