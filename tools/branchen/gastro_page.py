"""Branchenseite „Werbung für Gastronomie & Imbiss in Berlin“ → werbung-gastronomie-berlin.html.

Vom Inhaber am 07.11.2026 freigegeben. Aufbau wie die übrigen Branchenseiten (werbung-<branche>-berlin.html):
Kopf, Navigation, untere Leiste und Fußzeile kommen aus werbung-fahrschule-berlin.html, die Bausteine
(Icons, sec(), wa()) aus gen_branchen.py. Das Datenmodul der älteren Branchenseiten (branchen/pages.py) ist nicht
wiederhergestellt – deshalb ein eigener Generator.

Regeln (CLAUDE.md): nur Preise aus der Preistabelle (netto, „ab“; brutto setzt tools/seo/brutto.py),
nur echte Projektfotos, die referenzen.html öffentlich zeigt (Kunden nur so benannt wie dort),
keine eigene Werkstatt (Partnerwerkstatt; beleuchtete Anlagen bauen eingetragene Partnerbetriebe), keine Garantien.
Recht mit Quellen: § 13 PAngV (Preisverzeichnis Gaststätten), § 61 Abs. 1 BauO Bln (verfahrensfreie Werbeanlagen),
§ 11 BerlStrG (Kundenstopper = Sondernutzung, siehe blog/kundenstopper-erlaubnis.html).

Aufruf: python3 tools/branchen/gastro_page.py   (danach wie immer die Nachbearbeitung über build_all.py)
"""
import os, re, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, 'gen_branchen.py'), encoding='utf-8').read()
exec(_src[:_src.index('\nimport pages')])          # ROOT, BASE, I, SVC, svg, esc, wa, sec
sys.path.insert(0, os.path.join(HERE, '..', 'seo'))
sys.path.insert(0, os.path.join(HERE, '..'))
import brutto                                       # noqa: E402  (Bruttopreise wie in der Nachbearbeitung)
import add_assistent                                # noqa: E402  (Anfrage-Assistent wie auf den Leistungsseiten)

FILE = 'werbung-gastronomie-berlin.html'
URL = BASE + FILE
VORLAGE = 'werbung-fahrschule-berlin.html'

TITLE = 'Werbung für Gastronomie &amp; Imbiss in Berlin | Masar'
DESC = ('Leuchtreklame, Menütafeln, Schaufenster, Imbisswagen-Folierung und Preisaushang '
        'für Restaurants und Imbisse in Berlin – Leuchtbuchstaben ab 149 € netto.')
THEMA = 'Werbung für Gastronomie'
WA_TEXT = 'Hallo, ich habe eine Anfrage für Werbung für unser Restaurant / unseren Imbiss in Berlin.'

# Echte Projektfotos – Dateien und Bildunterschriften wie auf referenzen.html
HERO = ('leuchtlogo-rund-burgereat-01', 1200, 1600,
        'Runder Leuchtkasten mit Burger, Pommes und Getränk und dem Schriftzug „Burger Eat“, hell leuchtend',
        'Burger Eat: runder Leuchtkasten mit Fotodruck, eingeschaltet')
FOTOS = [
    ('menuetafel-imbiss-montiert-01', 720, 540,
     'Breite schwarze Menütafel mit Döner, Pasta, Pizza und Burger über der Theke eines Imbisses',
     'BISSWERK: Menütafel über der Theke, fertig montiert'),
    ('imbisswagen-menuetafeln-01', 720, 540,
     'Gelber Imbisswagen mit großer schwarzer Menütafel, zwei Aufstellern und bedruckten Blenden',
     'Grill Chicken: große Menütafel, Aufsteller und Blenden für den Imbisswagen'),
    ('leuchtlogo-rund-bside-burgereat-01', 540, 720,
     'Zwei runde Leuchtausleger „The B-Side Events“ und „Burger Eat“ mit schwarzem Wandhalter und Kabel, an eine Wand gelehnt',
     'Zwei doppelseitige Ausleger mit Wandhalter, fertig zur Montage'),
    ('werkstatt-folie-aufziehen-menuetafel-01', 540, 720,
     'Bedruckte Menütafel mit Seifenwasser, eine Hand rakelt die Folie glatt',
     'Nassverklebung: Folie wird blasenfrei auf die Tafel gerakelt'),
]

WARUM = [
    ('Abends gesehen werden', 'Wer im Vorbeigehen nicht auffällt, wird nicht betreten. Ein Leuchtlogo oder Leuchtbuchstaben über dem Eingang machen Ihren Laden auch zwischen hellen Nachbarn sichtbar – von weitem und nach Sonnenuntergang.'),
    ('Die Karte auf einen Blick', 'Über der Theke entscheidet sich, was bestellt wird. Eine Menütafel mit Fotos, klaren Gruppen und lesbaren Preisen hilft Gästen, die zum ersten Mal da sind – und macht die Schlange kürzer.'),
    ('Preise richtig zeigen', 'Gaststätten müssen ein Preisverzeichnis neben dem Eingang aushängen. Wir gestalten den Aushang passend zu Ihrer Menütafel, damit innen und außen dieselben Preise stehen.'),
    ('Gefunden werden', 'Wer „Imbiss in der Nähe“ sucht, sieht zuerst die Karte bei Google. Aktuelle Öffnungszeiten, Fotos vom Essen und die Speisekarte im Google-Profil bringen Gäste, bevor sie überhaupt vor der Tür stehen.'),
]

LEISTUNGEN = [
    ('licht', 'Leuchtreklame &amp; Leuchtlogo', 'Leuchtbuchstaben ab 149 € je Buchstabe netto, runde Leuchtausleger und Leuchtkästen mit Ihrem Logo, LED-Neon für den Gastraum ab 249 € netto. Gebaut und montiert von eingetragenen Partnerbetrieben.', '/leuchtreklame-berlin.html'),
    ('druck', 'Menütafeln über der Theke', 'Gedruckte Speisekarten-Tafeln mit Fotos und Preisen – auf Platte aufgezogen, für Laden oder Imbisswagen. Angebot nach Größe.', '/foliendruck-berlin.html'),
    ('web', 'Digitale Menütafeln', 'Bildschirme über der Theke: Preis ändern, Datei tauschen – statt neu zu drucken.', '/digital-signage-berlin.html'),
    ('glas', 'Schaufenster &amp; Öffnungszeiten', 'Name, Logo und Öffnungszeiten auf Glas ab 149 € netto, Aktionsfolie für Mittagstisch oder Eröffnung ab 190 € netto.', '/schaufensterbeschriftung-berlin.html'),
    ('schild', 'Imbisswagen &amp; Foodtruck', 'Teilbeschriftung mit Logo, Name und Kontakt ab 290 € netto, Vollfolierung nach Angebot – dazu Blenden, Menütafel und Aufsteller.', '/fahrzeugbeschriftung-berlin.html'),
    ('karte', 'Flyer &amp; Speisekarten', 'Speisekarten, Lieferflyer, Tischaufsteller und Aufkleber – gestaltet und gedruckt. Preis nach Auflage.', '/print.html'),
    ('weg', 'Kundenstopper', 'Aufsteller mit wechselbarem Plakat für das Tagesangebot. Auf dem Gehweg braucht er meist eine Erlaubnis vom Bezirksamt.', '/blog/kundenstopper-erlaubnis.html'),
    ('doc_svc', 'Preisaushang', 'Preisverzeichnis für den Eingang nach § 13 Preisangabenverordnung – passend zur Menütafel gestaltet und gedruckt.', '#gut-zu-wissen'),
    ('phone', 'Google-Profil &amp; Social Media', 'Öffnungszeiten, Fotos und Speisekarte im Google-Profil aktuell halten; Social Media mit Fotos und Reels ab 490 € pro Monat netto.', '/digital.html'),
]
SVC['doc_svc'] = ('<rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>'
                  '<path d="M12 11h4"/><path d="M12 16h4"/><path d="M8 11h.01"/><path d="M8 16h.01"/>')

PREISE = [  # nur Werte aus der Preistabelle in CLAUDE.md (Berlin, netto, „ab“)
    ('Leuchtbuchstaben', 'beleuchtet, je Buchstabe', 'ab 149 € je Buchstabe netto'),
    ('LED-Neon (innen)', 'Schriftzug oder Logo für den Gastraum', 'ab 249 € netto'),
    ('Firmenschild', 'Schild für Fassade oder Eingang', 'ab 149 € netto'),
    ('Schaufensterbeschriftung', 'Name, Logo, Öffnungszeiten', 'ab 149 € netto'),
    ('Aktionsfolie', 'Mittagstisch, Eröffnung, Saison', 'ab 190 € netto'),
    ('Fahrzeug-Teilbeschriftung', 'Imbisswagen, Foodtruck, Lieferfahrzeug', 'ab 290 € netto'),
    ('PVC-Banner', 'z. B. zur Eröffnung, je m²', 'ab 29 € / m² netto'),
    ('Logo-Design', 'für Schild, Karte und Social Media', 'ab 490 € netto'),
    ('Social-Media-Betreuung', 'Fotos, Posts und Reels', 'ab 490 € pro Monat netto'),
    ('Menütafeln, Leuchtkästen, Speisekarten, Flyer, Vollfolierung', 'nach Größe bzw. Auflage', 'individuelles Angebot'),
]

RECHT = [
    ('Preisverzeichnis am Eingang', 'Gaststätten müssen ein Preisverzeichnis neben dem Eingang aushängen (§ 13 Preisangabenverordnung) – die Menütafel oder die Bildschirme über der Theke reichen dafür nicht. Preise für Privatkunden gelten immer inklusive Mehrwertsteuer. Wir gestalten den Aushang passend zu Ihren Menütafeln.'),
    ('Leuchtreklame und Schilder', 'In Berlin sind Werbeanlagen bis 1 m² Ansichtsfläche verfahrensfrei, am eigenen Geschäft bis 2,5 m² (§ 61 Abs. 1 BauO Bln). Größere Anlagen, Ausleger über dem Gehweg und Anlagen im Denkmalbereich brauchen eine Genehmigung beim Bezirksamt. Den Antrag bereiten wir mit Ihnen vor – einen ersten Überblick gibt der <a href="/genehmigungs-check.html">Genehmigungs-Check</a>.'),
    ('Kundenstopper auf dem Gehweg', 'Der Gehweg gehört der Stadt. Ein Aufsteller dort ist in Berlin eine Sondernutzung (§ 11 Berliner Straßengesetz) und braucht meist eine Erlaubnis vom Bezirksamt, in dem Ihr Laden liegt. Alles dazu im Ratgeber <a href="/blog/kundenstopper-erlaubnis.html">Kundenstopper: Was ist erlaubt?</a>'),
    ('Imbisswagen und Leasing', 'Für Miet- und Leasingfahrzeuge verwenden wir rückstandsfrei entfernbare Folien und stimmen das Material auf die Rückgabebedingungen ab.'),
]
QUELLEN = ('Kein Rechtsrat, Stand November 2026. Grundlagen: '
           '<a href="https://www.gesetze-im-internet.de/pangv_2022/__13.html" target="_blank" rel="noopener noreferrer">§ 13 PAngV</a>, '
           '<a href="https://gesetze.co/BE/BauO_Bln/61" target="_blank" rel="noopener noreferrer">§ 61 BauO Bln</a>, '
           '<a href="https://service.berlin.de/dienstleistung/350896/" target="_blank" rel="noopener noreferrer">service.berlin.de – Genehmigung Werbeanlage</a>.')

ABLAUF = [
    ('Fotos &amp; Wunsch schicken', 'Ein Foto von Fassade, Theke oder Imbisswagen, Ihr Logo und Ihre Karte – per WhatsApp, E-Mail oder Formular. Antwort innerhalb von 24 Stunden.'),
    ('Entwurf am Foto', 'Wir zeigen Ihnen Leuchtlogo, Menütafel oder Folierung vorab auf dem Foto Ihres Ladens – mit Maßen und Festpreis-Angebot.'),
    ('Fertigung', 'Druck, Folie und Tafeln entstehen in unserer Partnerwerkstatt, beleuchtete Anlagen bauen eingetragene Partnerbetriebe. Wenn nötig, kümmern wir uns um die Genehmigung.'),
    ('Montage passend zum Betrieb', 'Wir stimmen den Termin mit Ihnen ab, damit Küche und Verkauf möglichst weiterlaufen – zum Beispiel vor der Öffnung.'),
]

FAQ = [
    ('Was kostet Leuchtreklame für ein Restaurant oder einen Imbiss?',
     'Leuchtbuchstaben beginnen ab 149 € je Buchstabe netto, LED-Neon für innen ab 249 € netto. Runde Leuchtausleger und Leuchtkästen mit Logo rechnen wir nach Größe – Sie bekommen nach Fotos und Maßen ein Festpreis-Angebot.'),
    ('Brauche ich für mein Leuchtschild eine Genehmigung?',
     'Das hängt von der Größe ab: Bis 1 m² Ansichtsfläche, am eigenen Geschäft bis 2,5 m², sind Werbeanlagen in Berlin verfahrensfrei (§ 61 Abs. 1 BauO Bln). Größere Anlagen, Ausleger über dem Gehweg und Anlagen im Denkmalbereich brauchen eine Genehmigung beim Bezirksamt. Den Antrag bereiten wir mit Ihnen vor.'),
    ('Müssen wir unsere Preise am Eingang aushängen?',
     'Ja. Gaststätten müssen ein Preisverzeichnis neben dem Eingang aushängen (§ 13 Preisangabenverordnung) – die Menütafel über der Theke reicht dafür nicht. Preise für Privatkunden gelten immer inklusive Mehrwertsteuer. Wir gestalten den Aushang passend zu Ihrer Menütafel.'),
    ('Darf ich einen Kundenstopper vor die Tür stellen?',
     'Auf Ihrem eigenen Grundstück meist ja. Auf dem Gehweg ist ein Aufsteller in Berlin eine Sondernutzung (§ 11 Berliner Straßengesetz) und braucht in der Regel eine Erlaubnis vom Bezirksamt. Details stehen in unserem Ratgeber zum Kundenstopper.'),
    ('Können Sie unseren Imbisswagen oder Foodtruck gestalten?',
     'Ja. Eine Teilbeschriftung mit Logo, Name und Kontakt beginnt ab 290 € netto, eine Vollfolierung rechnen wir nach Fahrzeug. Dazu gestalten und drucken wir Menütafel, Blenden und Aufsteller – so wie für den Imbisswagen von Grill Chicken.'),
    ('Kümmern Sie sich auch um das Google-Profil?',
     'Ja. Wir bringen Öffnungszeiten, Fotos und Speisekarte in Ihrem Google-Unternehmensprofil auf den aktuellen Stand oder richten es mit Ihnen ein. Das Profil selbst kostet bei Google nichts – Vorsicht bei Anrufen, die dafür Geld verlangen.'),
    ('In welchen Sprachen beraten Sie?',
     'Auf Deutsch, Englisch, Arabisch und Türkisch – persönlich in Berlin, am Telefon oder per WhatsApp.'),
]

LINKS = [
    ('/blog/kundenstopper-erlaubnis.html', 'Ratgeber: Kundenstopper – was ist erlaubt?'),
    ('/blog/digitale-menuetafel-gestalten.html', 'Ratgeber: Digitale Menütafel gestalten'),
    ('/blog/leuchtreklame-kosten-berlin.html', 'Ratgeber: Was kostet Leuchtreklame?'),
    ('/blog/google-unternehmensprofil-abzocke.html', 'Ratgeber: Google-Profil – Abzocke erkennen'),
    ('/leuchtreklame-berlin.html', 'Leuchtreklame Berlin'),
    ('/digital-signage-berlin.html', 'Digitale Menütafeln'),
    ('/referenzen.html', 'Referenzen'),
    ('/angebote/', 'Alle Branchen-Angebote'),
]

FORM_OPTS = ['Leuchtreklame / Leuchtlogo', 'LED-Neon', 'Menütafel (gedruckt)', 'Digitale Menütafel', 'Schaufenster / Öffnungszeiten',
             'Imbisswagen / Foodtruck', 'Flyer / Speisekarten', 'Kundenstopper', 'Preisaushang', 'Google-Profil / Social Media',
             'Noch nicht entschieden']


def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + '\n</script>\n'


def kopf(t):
    """Kopf der Vorlage: alles vor <title> und alles nach dem letzten JSON-LD-Block bleibt, dazwischen neu."""
    a = t[:t.index('<title>')]
    h = t.index('</head>')
    ende = t.index('</script>\n', t.rindex('application/ld+json', 0, h)) + len('</script>\n')
    b = t[ende:h]
    og = 'og/' + FILE.replace('.html', '.jpg')
    og_url = BASE + og if os.path.exists(ROOT + og) else BASE + 'logo.png'
    meta = f'''<title>{TITLE}</title>
<meta name="description" content="{esc(DESC)}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="robots" content="index, follow">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{esc(DESC)}">
<meta property="og:url" content="{URL}">
<meta property="og:type" content="website">
<meta property="og:image" content="{og_url}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:alt" content="Werbung für Gastronomie &amp; Imbiss – Masar Werbeagentur">
<meta property="og:locale" content="de_DE">
<meta property="og:site_name" content="Masar Werbeagentur Berlin">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="{esc(DESC)}">
<meta name="twitter:image" content="{og_url}">
<link rel="canonical" href="{URL}">
<link rel="alternate" hreflang="de" href="{URL}">
<link rel="alternate" hreflang="x-default" href="{URL}">
'''
    angebote = [('Leuchtbuchstaben (je Buchstabe)', 149), ('Schaufensterbeschriftung', 149), ('LED-Neon innen', 249),
                ('Fahrzeug-Teilbeschriftung Imbisswagen', 290)]
    service = {
        '@context': 'https://schema.org', '@type': 'Service',
        'serviceType': 'Werbung, Leuchtreklame und Menütafeln für Gastronomie',
        'name': 'Werbung für Gastronomie & Imbiss in Berlin', 'description': DESC, 'url': URL,
        'areaServed': [{'@type': 'City', 'name': 'Berlin'}],
        'provider': {'@type': 'LocalBusiness', '@id': BASE + '#identity', 'name': 'Masar Werbeagentur',
                     'telephone': '+49 178 5143918',
                     'address': {'@type': 'PostalAddress', 'streetAddress': 'Bristolstraße 19E', 'postalCode': '13349',
                                 'addressLocality': 'Berlin', 'addressCountry': 'DE'}},
        'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Werbung für Gastronomie Berlin – Einzelpreise',
                            'itemListElement': [{'@type': 'Offer', 'name': n, 'priceCurrency': 'EUR',
                                                 'priceSpecification': {'@type': 'PriceSpecification', 'minPrice': p,
                                                                        'priceCurrency': 'EUR', 'valueAddedTaxIncluded': False}}
                                                for n, p in angebote]}}
    crumbs = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': BASE},
        {'@type': 'ListItem', 'position': 2, 'name': 'Branchen-Angebote', 'item': BASE + 'angebote/'},
        {'@type': 'ListItem', 'position': 3, 'name': 'Gastronomie & Imbiss', 'item': URL}]}
    faq = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}
    return a + meta + ld(service) + ld(crumbs) + ld(faq) + b + '</head>'


def bild(name, w, h, alt, cap):
    return (f'<figure style="margin:0;background:#fff;border:1px solid var(--border,#e0eaea);border-radius:12px;overflow:hidden">'
            f'<a href="/referenzen.html" style="display:block"><img src="/referenzen/{name}-720.webp" width="{w}" height="{h}" alt="{esc(alt)}" loading="lazy" '
            f'style="width:100%;aspect-ratio:1/1;object-fit:cover;display:block"></a>'
            f'<figcaption style="padding:.7rem .9rem;font-size:14px;color:var(--muted,#5a7070);line-height:1.5">{esc(cap)}</figcaption></figure>')


def why(items):
    return '    <div class="why-grid">\n' + ''.join(
        f'      <div class="why-item">\n        <div class="why-num">{i}</div>\n        <div><h3>{h}</h3><p>{p}</p></div>\n      </div>\n'
        for i, (h, p) in enumerate(items, 1)) + '    </div>'


def inhalt():
    n, w, h, alt, cap = HERO
    hero = f'''<section class="hero">
  <div class="hero-lines"></div>
  <div class="container">
    <div class="hero-inner">
      <div>
        <div class="hero-badge">{I["star"]}Für Restaurants, Imbisse &amp; Foodtrucks</div>
        <h1>Ihr Restaurant.<em>Von weitem gesehen.</em>An der Theke verstanden.</h1>
        <p class="hero-sub">Gäste entscheiden in Sekunden, ob sie reinkommen. Leuchtlogo, Schaufenster, Menütafel und Preisaushang müssen deshalb von der Straße aus funktionieren. Wir gestalten, lassen fertigen und montieren – Leuchtbuchstaben ab 149 € je Buchstabe netto, Schaufensterbeschriftung ab 149 € netto.</p>
        <div class="hero-btns">
          <a href="#preise" class="btn btn-teal">Preise ansehen</a>
          <a href="{wa(WA_TEXT)}" target="_blank" rel="noopener noreferrer" class="btn btn-outline">{I["wa"]}WhatsApp schreiben</a>
        </div>
        <div class="hero-trust">
          <span class="hero-trust-txt">Restaurant · Imbiss · Café · Bäckerei · Foodtruck</span>
        </div>
      </div>
      <div class="hero-visual">
        <img class="hero-shot" src="/referenzen/{n}-720.webp" srcset="/referenzen/{n}-480.webp 360w, /referenzen/{n}-720.webp 540w, /referenzen/{n}.webp 1200w" sizes="360px" width="{w}" height="{h}" alt="{esc(alt)}" loading="eager" fetchpriority="high" style="aspect-ratio:3/4">
        <p style="font-size:13px;color:rgba(255,255,255,.78);margin:.7rem auto 0;max-width:340px;line-height:1.5">{esc(cap)}</p>
      </div>
    </div>
  </div>
</section>

'''
    usp = ''.join(f'<span>{I["check"]}{u}</span>' for u in
                  ['Echte Projekte für Imbisse', 'Preisaushang nach § 13 PAngV', 'Genehmigung beim Bezirksamt', 'Angebot in 24 h'])
    usp = f'''<div style="background:var(--teal);padding:.9rem 0;">
  <div class="container">
    <div class="usp-row">{usp}</div>
  </div>
</div>
'''
    karten = '    <div class="svc-grid">\n' + ''.join(
        f'''      <a href="{href}" class="svc-card" style="text-decoration:none;color:inherit;display:block;">
        <div class="svc-icon">{svg(ic)}</div>
        <h3>{t}</h3>
        <p>{p}</p>
      </a>
''' for ic, t, p, href in LEISTUNGEN) + '    </div>'
    galerie = ('    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1rem;max-width:1100px;margin:0 auto">'
               + ''.join(bild(*f) for f in FOTOS) + '</div>\n'
               '    <p style="text-align:center;margin-top:1.2rem"><a href="/referenzen.html" style="color:var(--teal-ink,#177567);font-weight:700">Alle Referenzen ansehen →</a></p>')
    zeilen = ''.join(f'''          <tr>
            <td data-label="Leistung">{a}</td>
            <td data-label="Umfang">{b}</td>
            <td class="pcell" data-label="Preis">{c}</td>
          </tr>
''' for a, b, c in PREISE)
    preise = f'''    <div class="price-scroll">
      <table class="price-table rt">
        <caption class="sr-only" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);">Einzelpreise Gastronomie</caption>
        <thead><tr><th scope="col">Leistung</th><th scope="col">Umfang</th><th scope="col">Preis</th></tr></thead>
        <tbody>
{zeilen}        </tbody>
      </table>
    </div>
    <p class="price-note">Alle Preise netto zzgl. 19 % Umsatzsteuer, Berlin. Der Endpreis hängt von Größe, Material und Montage ab – Sie bekommen nach Fotos und Maßen ein Festpreis-Angebot, in der Regel innerhalb von 24 Stunden.</p>'''
    recht = ('    <div class="blog-prose" style="max-width:820px;margin:0 auto;">\n'
             + ''.join(f'      <p><strong>{h}:</strong> {p}</p>\n' for h, p in RECHT)
             + f'      <p style="font-size:13px;">{QUELLEN}</p>\n    </div>')
    faq = ('    <div class="faq-wrap">\n' + ''.join(
        f'      <div class="faq-item"><button class="faq-q">{esc(q)}</button><div class="faq-a"><p>{esc(a)}</p></div></div>\n'
        for q, a in FAQ) + '    </div>')
    chips = '    <div class="chip-row">\n' + ''.join(f'      <a href="{u}" class="chip">{t}</a>\n' for u, t in LINKS) + '    </div>'
    links = f'''<section class="section" style="padding:2.5rem 0;">
  <div class="container">
    <div class="sec-head reveal" style="margin-bottom:1.5rem;">
      <span class="eyebrow">{I["link"]}Passend dazu</span>
      <h2 class="sec-title" style="font-size:clamp(1.5rem,3vw,2.2rem);">Ratgeber &amp; <em>Leistungen</em></h2>
    </div>
{chips}
  </div>
</section>
'''
    opts = ''.join(f'            <option>{o}</option>\n' for o in FORM_OPTS)
    kontakt = f'''<section class="section" id="kontakt">
  <div class="container">
    <div class="sec-head reveal">
      <span class="eyebrow">{I["mail"]}Anfrage</span>
      <h2 class="sec-title">Kostenloses Angebot <em>anfordern</em></h2>
      <p class="sec-sub">Nennen Sie uns kurz Ihren Betrieb und Ihr Vorhaben – am besten mit einem Foto von Fassade, Theke oder Imbisswagen. Wir melden uns innerhalb von 24 Stunden mit einem Angebot.</p>
    </div>
    <div class="form-wrap">
      <form action="/kontakt.php" method="POST" enctype="multipart/form-data">
        <input type="hidden" name="_subject" value="Werbung Gastronomie Berlin – Anfrage">
        <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
        <div class="form-grid">
          <div class="fg"><label for="br-firma">Restaurant / Imbiss *</label><input type="text" id="br-firma" name="firma" autocomplete="organization" placeholder="Name Ihres Betriebs" required></div>
          <div class="fg"><label for="br-name">Ansprechpartner *</label><input type="text" id="br-name" name="name" autocomplete="name" placeholder="Vor- und Nachname" required></div>
        </div>
        <div class="form-grid">
          <div class="fg"><label for="br-email">E-Mail *</label><input type="email" id="br-email" name="email" autocomplete="email" placeholder="info@beispiel.de" required></div>
          <div class="fg"><label for="br-telefon">Telefon / WhatsApp</label><input type="tel" id="br-telefon" name="telefon" autocomplete="tel" placeholder="+49 ..."></div>
        </div>
        <div class="fg">
          <label for="br-thema">Worum geht es?</label>
          <select id="br-thema" name="thema">
            <option value="">Bitte wählen...</option>
{opts}          </select>
        </div>
        <div class="fg"><label for="br-nachricht">Ihr Anliegen</label><textarea id="br-nachricht" name="nachricht" placeholder="Zum Beispiel: Leuchtlogo über dem Eingang, neue Menütafel über der Theke mit 20 Gerichten, Öffnungszeiten auf die Tür."></textarea></div>
        <div class="fg"><label for="br-datei">Datei anhängen (optional)</label><input type="file" id="br-datei" name="attachment" accept="image/*,.pdf,.svg,.ai,.eps,.zip" style="background:#fff;border:1px dashed var(--border);border-radius:8px;padding:11px 14px;color:var(--muted);font-family:'Barlow','Barlow Fallback',sans-serif;font-size:14px;width:100%;cursor:pointer;"><p style="font-size:12.5px;color:var(--muted);line-height:1.6;margin-top:.45rem;">Optional. Ein Foto von Fassade, Theke oder Imbisswagen, Ihr Logo und Ihre aktuelle Karte helfen uns beim Angebot.</p></div>
        <div class="consent-row">
          <input type="checkbox" id="br-consent" name="consent" required>
          <label for="br-consent">Ich habe die <a href="/datenschutz.html">Datenschutzerklärung</a> zur Kenntnis genommen und stimme der Verarbeitung meiner Daten zu (Art.&nbsp;6 Abs.&nbsp;1 lit.&nbsp;b DSGVO). *</label>
        </div>
        <button type="submit" class="submit-btn">✓ Anfrage senden – kostenlos &amp; unverbindlich</button>
        <p style="text-align:center;font-size:12px;color:var(--muted);margin-top:.6rem;">Kein Spam. Ihre Daten werden vertraulich behandelt. Antwort innerhalb von 24 Stunden.</p>
      </form>
    </div>
  </div>
</section>
'''
    return (hero + usp
            + sec('Was Gastronomie braucht', 'Gäste entscheiden <em>auf den letzten zehn Metern</em>',
                  'Ob jemand reinkommt, hängt an dem, was er von der Straße und an der Theke sieht.', why(WARUM))
            + sec('Leistungen', 'Alles für Ihr <em>Restaurant oder Ihren Imbiss</em>',
                  'Einzeln oder zusammen – alles in Ihrem Design, aus einer Hand.', karten, alt=True)
            + sec('Aus unserer Arbeit', 'Menütafeln und Leuchtlogos <em>aus unseren Projekten</em>',
                  'Echte Aufträge aus unseren Referenzen – Druck und Aufziehen der Tafeln in unserer Partnerwerkstatt.', galerie, sid='projekte')
            + sec('Preise', 'Was kostet <em>Werbung für Gastronomie?</em>',
                  'Einzelpreise aus unserer Preisliste – Pakete stellen wir Ihnen nach Ihrem Vorhaben zusammen.', preise, alt=True, sid='preise', icon='tag')
            + sec('Gut zu wissen', 'Was für Gastronomie <em>gilt</em>',
                  'Kein Rechtsrat – aber die Punkte, die wir mit Restaurants und Imbissen vorab klären.', recht, sid='gut-zu-wissen', icon='doc')
            + sec('Ablauf', 'So läuft es <em>ab</em>', None, why(ABLAUF), alt=True)
            + sec('Häufige Fragen', 'Gastronomie – <em>Fragen &amp; Antworten</em>', None, faq, icon='faq')
            + links + kontakt)


def main():
    t = open(ROOT + VORLAGE, encoding='utf-8').read()
    m_a = t.index('<main id="main-content" tabindex="-1">\n') + len('<main id="main-content" tabindex="-1">\n')
    m_b = t.index('</main>')
    body = t[t.index('</head>') + len('</head>'):m_a]
    body = re.sub(r'(data-termin-link data-btn href="/termin\.html\?thema=)[^"]*"',
                  lambda m: m.group(1) + urllib.parse.quote(THEMA) + '"', body, count=1)
    body = re.sub(r'(<div class="scta-btns">\s*<a href=")https://wa\.me/[^"]*"', lambda m: m.group(1) + wa(WA_TEXT) + '"', body, count=1)
    assert 'Fahrschul' not in body, 'Vorlage enthält noch Fahrschul-Text außerhalb von <main>'
    s = kopf(t) + body + inhalt() + '\n' + t[m_b:]
    s = brutto.bearbeiten(s)
    open(ROOT + FILE, 'w', encoding='utf-8').write(s)
    print(FILE, 'geschrieben;', 'Assistent:', add_assistent.inject(FILE, '', 0, ''))


if __name__ == '__main__':
    main()
