"""Werbeagentur-Städteseiten im Berliner Umland (kompakt: Leistungs-Kacheln → Anfrage mit vorausgefülltem Betreff)."""
import os, re, json
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, '..', 'branchen', 'gen_branchen.py'), encoding='utf-8').read()
exec(src[:src.index('\nimport pages')])  # HEAD_A, HEAD_B, FOOT, I, SVC, esc, wa, sec, ROOT, BASE

CITIES = [
 dict(slug='brandenburg-havel', name='Brandenburg an der Havel', short='Brandenburg/Havel', kreis='kreisfreie Stadt im Westen Brandenburgs', km=70),
 dict(slug='frankfurt-oder', name='Frankfurt (Oder)', short='Frankfurt (Oder)', kreis='kreisfreie Stadt an der polnischen Grenze', km=90),
 dict(slug='bernau', name='Bernau bei Berlin', short='Bernau', kreis='Landkreis Barnim', km=25),
 dict(slug='koenigs-wusterhausen', name='Königs Wusterhausen', short='Königs Wusterhausen', kreis='Landkreis Dahme-Spreewald', km=30),
 dict(slug='eberswalde', name='Eberswalde', short='Eberswalde', kreis='Kreisstadt des Landkreises Barnim', km=50),
 dict(slug='falkensee', name='Falkensee', short='Falkensee', kreis='Landkreis Havelland', km=20),
 dict(slug='teltow-kleinmachnow', name='Teltow & Kleinmachnow', short='Teltow & Kleinmachnow', kreis='Landkreis Potsdam-Mittelmark', km=0),
 dict(slug='fuerstenwalde', name='Fürstenwalde', short='Fürstenwalde', kreis='Landkreis Oder-Spree', km=60),
 dict(slug='hennigsdorf', name='Hennigsdorf', short='Hennigsdorf', kreis='Landkreis Oberhavel', km=0),
 dict(slug='neuruppin', name='Neuruppin', short='Neuruppin', kreis='Kreisstadt des Landkreises Ostprignitz-Ruppin', km=75),
 dict(slug='rathenow', name='Rathenow', short='Rathenow', kreis='Kreisstadt des Landkreises Havelland', km=80),
 dict(slug='zossen', name='Zossen', short='Zossen', kreis='Landkreis Teltow-Fläming', km=40),
 dict(slug='luckenwalde', name='Luckenwalde', short='Luckenwalde', kreis='Kreisstadt des Landkreises Teltow-Fläming', km=55),
 dict(slug='jueterbog', name='Jüterbog', short='Jüterbog', kreis='Landkreis Teltow-Fläming', km=70),
 dict(slug='beelitz', name='Beelitz', short='Beelitz', kreis='Landkreis Potsdam-Mittelmark', km=45),
]

NRW_CITIES = [
 dict(slug='herne', name='Herne', short='Herne', kreis='kreisfreie Stadt im Ruhrgebiet', km=None, nrw=True),
 dict(slug='muelheim', name='Mülheim an der Ruhr', short='Mülheim an der Ruhr', kreis='kreisfreie Stadt im Ruhrgebiet', km=None, nrw=True),
 dict(slug='bottrop', name='Bottrop', short='Bottrop', kreis='kreisfreie Stadt im Ruhrgebiet', km=None, nrw=True),
]
NRW_NEAR = [('/werbeagentur-nrw.html', 'NRW'), ('/werbeagentur-essen.html', 'Essen'), ('/werbeagentur-bochum.html', 'Bochum'), ('/werbeagentur-dortmund.html', 'Dortmund'), ('/werbeagentur-duesseldorf.html', 'Düsseldorf'), ('/werbeagentur-koeln.html', 'Köln')]
SERV_NRW = [
 ('Schilder', 'Firmen-, Praxis- und Türschilder aus Alu, Acryl und Edelstahl', 'ab 59 €', 'schilder', '/schilder-nrw.html'),
 ('Leuchtreklame', 'Leuchtbuchstaben, Leuchtkästen und LED-Neon', 'ab 229 € / Buchstabe', 'leuchtreklamen', '/leuchtreklame-nrw.html'),
 ('Schaufenster', 'Beschriftung, Milchglas und Druckfolie', 'ab 179 €', 'schaufenster', '/schaufensterbeschriftung-nrw.html'),
 ('Fahrzeugbeschriftung', 'Auto, Transporter und Flotte', 'ab 340 €', 'fahrzeug', '/fahrzeugbeschriftung-nrw.html'),
 ('Fensterfolie', 'Sichtschutz, Sonnenschutz, Sicherheit', 'Sichtschutz ab 229 €', 'fensterfolie', '/fensterfolie-nrw.html'),
 ('PVC-Banner', 'Wetterfest, mit oder ohne Ösen', 'ab 22 € / m²', 'pvc-banner', '/pvc-banner-nrw.html'),
 ('Logo & Grafikdesign', 'Logo, Visitenkarten, Corporate Design', 'Logo ab 490 €', 'grafikdesign', '/grafikdesign-berlin.html'),
 ('Flyer & Druck', 'Flyer, Plakate, Visitenkarten, Aufkleber', 'Festpreis', 'druck', '/print.html'),
 ('Webdesign', 'Website, Landingpage, Relaunch', 'Festpreis', 'webdesign', '/webdesign-nrw.html'),
 ('Social Media', 'Instagram, Facebook, TikTok – Betreuung', 'ab 490 € / Monat', 'social-media', '/digital.html'),
]

# Leistungen: (Titel, Kurztext, Preis, Bild, Detailseite)
SERV = [
 ('Schilder', 'Firmen-, Praxis- und Türschilder aus Alu, Acryl und Edelstahl', 'ab 45 €', 'schilder', '/schilder-berlin.html'),
 ('Leuchtreklame', 'Leuchtbuchstaben, Leuchtkästen und LED-Neon', 'ab 199 € / Buchstabe', 'leuchtreklamen', '/leuchtreklame-berlin.html'),
 ('Schaufenster', 'Beschriftung, Milchglas und Druckfolie', 'ab 149 €', 'schaufenster', '/schaufensterbeschriftung-berlin.html'),
 ('Fahrzeugbeschriftung', 'Auto, Transporter und Flotte', 'ab 290 €', 'fahrzeug', '/fahrzeugbeschriftung-berlin.html'),
 ('Fensterfolie', 'Sichtschutz, Sonnenschutz, Sicherheit', 'Sichtschutz ab 190 €', 'fensterfolie', '/fensterfolie-berlin.html'),
 ('PVC-Banner', 'Wetterfest, mit oder ohne Ösen', 'ab 19 € / m²', 'pvc-banner', '/pvc-banner-berlin.html'),
 ('Logo & Grafikdesign', 'Logo, Visitenkarten, Corporate Design', 'Logo ab 490 €', 'grafikdesign', '/grafikdesign-berlin.html'),
 ('Flyer & Druck', 'Flyer, Plakate, Visitenkarten, Aufkleber', 'Festpreis', 'druck', '/print.html'),
 ('Webdesign', 'Website, Landingpage, Relaunch', 'Festpreis', 'webdesign', '/webdesign-berlin.html'),
 ('Social Media', 'Instagram, Facebook, TikTok – Betreuung', 'ab 490 € / Monat', 'social-media', '/digital.html'),
]
IMGQ = {'fensterfolie': '?v=2'}
ASMAP = {'Schilder': 'schild:0', 'Leuchtreklame': 'schild:1', 'Schaufenster': 'schaufenster:0', 'Fahrzeugbeschriftung': 'fahrzeug',
         'Fensterfolie': 'fensterfolie', 'PVC-Banner': 'druck:1', 'Logo & Grafikdesign': 'design:0', 'Flyer & Druck': 'druck:0',
         'Webdesign': 'web:0', 'Social Media': 'web:3'}

CSS = '''<style>
.ua-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:1rem}
.ua-card{display:flex;flex-direction:column;background:#fff;border:1px solid var(--border);border-radius:var(--r);overflow:hidden;text-decoration:none;color:inherit;transition:transform .15s,box-shadow .15s;cursor:pointer;text-align:left;font:inherit;padding:0}
.ua-card:hover,.ua-card:focus-visible{transform:translateY(-3px);box-shadow:0 10px 26px rgba(19,46,80,.12)}
.ua-card img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block;background:var(--off)}
.ua-card .b{padding:.85rem 1rem 1rem;display:flex;flex-direction:column;gap:.3rem;flex:1}
.ua-card h3{font-size:1.15rem;margin:0;color:var(--navy);hyphens:auto;overflow-wrap:anywhere}
.ua-card p{font-size:14px;line-height:1.45;color:var(--muted);margin:0}
.ua-card .pr{font-weight:700;color:var(--teal-ink);font-size:14.5px;margin-top:auto;padding-top:.35rem}
.ua-card .go{display:inline-flex;align-items:center;justify-content:center;margin-top:.55rem;background:var(--teal);color:var(--navy);font-weight:700;font-size:14px;border-radius:8px;padding:.55rem .8rem}
.ua-more{display:block;text-align:center;font-size:13px;padding:.55rem;border-top:1px solid var(--border);color:var(--teal-ink);text-decoration:none}
.ua-pick{background:var(--tealbg,#e8f8f5);border:1px solid var(--teal);border-radius:10px;padding:.7rem 1rem;margin-bottom:1rem;font-size:15px;color:var(--navy);display:none}
.ua-pick.on{display:block}
.ua-steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1rem;counter-reset:s}
.ua-steps div{background:#fff;border:1px solid var(--border);border-radius:var(--r);padding:1.1rem 1.2rem}
.ua-steps div:before{counter-increment:s;content:counter(s);display:inline-flex;width:32px;height:32px;border-radius:50%;background:var(--teal);color:var(--navy);font-weight:800;align-items:center;justify-content:center;margin-bottom:.5rem}
@media(max-width:600px){.ua-grid{grid-template-columns:1fr 1fr;gap:.6rem}.ua-card .b{padding:.6rem .65rem .7rem}.ua-card p{display:none}.ua-card h3{font-size:1rem}.ua-card .pr{font-size:13px}.ua-card .go{font-size:13px;padding:.45rem .5rem}.ua-more{font-size:12px;padding:.45rem}}
.ua-steps h4{margin:0 0 .3rem;color:var(--navy)}.ua-steps p{margin:0;color:var(--muted);font-size:15px;line-height:1.55}
</style>'''

def card(c, t, d, pr, img, more):
    bet = f'{t} in {c["short"]}'
    q = IMGQ.get(img, '')
    return f'''
      <div style="display:flex;flex-direction:column;background:#fff;border:1px solid var(--border);border-radius:var(--r);overflow:hidden">
        <a href="#kontakt" class="ua-card" data-betreff="{esc(bet)}" data-as-open="{ASMAP.get(t, "")}" style="border:0;border-radius:0" aria-label="{esc(t)} anfragen">
          <img src="/{img}-360.webp{q}" width="360" height="450" alt="{esc(t)} – Masar Werbeagentur" loading="lazy" decoding="async">
          <div class="b"><h3>{t.replace("Fahrzeugbeschriftung","Fahrzeug&shy;beschriftung")}</h3><p>{d}</p><span class="pr">{pr} netto</span><span class="go">Angebot anfragen →</span></div>
        </a>
        <a class="ua-more" href="{more}" aria-label="Mehr zu {esc(t)}">Mehr erfahren →</a>
      </div>'''

def head(c, url, title, desc, faq):
    svc = {"@context": "https://schema.org", "@type": "Service", "serviceType": "Werbeagentur", "name": f"Werbeagentur {c['name']}",
           "description": desc, "url": url, "areaServed": [{"@type": "City", "name": c['name']}],
           "provider": {"@type": "LocalBusiness", "@id": BASE + "#identity", "name": "Masar Werbeagentur", "telephone": "+49 178 5143918",
                        "address": {"@type": "PostalAddress", "streetAddress": "Bristolstraße 19E", "postalCode": "13349", "addressLocality": "Berlin", "addressCountry": "DE"}}}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
          {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
          ({"@type": "ListItem", "position": 2, "name": "Werbeagentur NRW", "item": BASE + "werbeagentur-nrw.html"} if c.get('nrw') else {"@type": "ListItem", "position": 2, "name": "Brandenburg & Umland", "item": BASE + "werbetechnik-brandenburg.html"}),
          {"@type": "ListItem", "position": 3, "name": f"Werbeagentur {c['name']}", "item": url}]}
    fq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
          {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    js = lambda o: '<script type="application/ld+json">\n' + json.dumps(o, ensure_ascii=False, indent=2) + '\n</script>\n'
    t, d = esc(title), esc(desc)
    meta = f'''<title>{t}</title>
<meta name="description" content="{d}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="robots" content="index, follow">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://masar-werbeagentur.de/logo.png">
<meta property="og:locale" content="de_DE">
<meta property="og:site_name" content="Masar Werbeagentur Berlin">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="https://masar-werbeagentur.de/logo.png">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="de" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
'''
    return HEAD_A + meta + js(svc) + js(bc) + js(fq) + HEAD_B

def build(c):
    n, s = c['name'], c['short']
    NRW = c.get('nrw')
    f = f'werbeagentur-{c["slug"]}.html'; url = BASE + f
    nah = 'im Einsatzgebiet unseres Teams in NRW' if NRW else ('direkt an der Berliner Stadtgrenze' if c['km'] == 0 else f'rund {c["km"]} km von unserem Studio in Berlin-Wedding')
    title = f'Werbeagentur {s}: Schilder, Werbetechnik & Design | Masar'
    if len(title) > 60: title = f'Werbeagentur {s}: Werbetechnik & Design | Masar'
    if len(title) > 60: title = f'Werbeagentur {s} – Schilder & Design | Masar'
    if len(title) > 60: title = f'Werbeagentur {s} | Masar'
    desc = f'Werbeagentur für {s}: Schilder ab {"59" if NRW else "45"} €, Leuchtreklame, Schaufenster, Fahrzeugbeschriftung, Banner, Logo und Website – Montage vor Ort, Angebot in 24 h.'
    if len(desc) > 158: desc = f'Werbeagentur für {s}: Schilder, Leuchtreklame, Schaufenster, Fahrzeuge, Banner, Logo und Website – Montage vor Ort, Angebot in 24 h.'
    faq = [
     (f'Kommen Sie für die Montage nach {n}?', (f'Ja. Unser Team in NRW kommt zu Ihnen nach {n}, misst auf und montiert Schilder, Leuchtreklame, Folien und Banner vor Ort. Unser Firmensitz ist in Berlin.' if c.get('nrw') else f'Ja. {n} liegt {nah}. Wir messen vor Ort auf und montieren Schilder, Leuchtreklame, Folien und Banner bei Ihnen.')),
     ('Was kostet die Anfahrt?', 'Die Anfahrt ist im Festpreis enthalten und dort einzeln ausgewiesen – Sie wissen vorher genau, was Sie zahlen. Für reine Druck- und Designaufträge fällt keine Anfahrt an.'),
     ('Wie schnell bekomme ich ein Angebot?', 'In der Regel innerhalb von 24 Stunden. Ein Foto vom Ort und Ihr Logo reichen für ein erstes Angebot.'),
     ('Brauche ich eine Genehmigung für mein Schild?', 'Das hängt von Größe, Lage und Gemeinde ab. Wir prüfen vor dem Auftrag, was an Ihrer Fassade erlaubt ist, und sagen Ihnen, ob ein Antrag nötig ist.'),
    ]
    w = wa(f'Hallo, ich habe eine Anfrage für {s}: ')
    cards = ''.join(card(c, *x) for x in (SERV_NRW if NRW else SERV))
    body = f'''<section class="hero" id="main-content" role="main" tabindex="-1">
  <div class="hero-lines"></div>
  <div class="container">
    <div class="hero-inner">
      <div>
        <div class="hero-badge">{I['star']}Werbeagentur · {esc(s)}</div>
        <h1>Werbeagentur <em>{esc(s)}</em></h1>
        <p class="hero-sub">Schilder, Leuchtreklame, Schaufenster, Fahrzeuge, Banner, Logo und Website – alles aus einer Hand für Unternehmen in {esc(n)} ({c['kreis']}). Wählen Sie unten Ihre Leistung, wir melden uns innerhalb von 24 Stunden.</p>
        <div class="hero-btns">
          <a href="#leistungen" class="btn btn-teal">Leistung wählen ↓</a>
          <a href="{w}" target="_blank" rel="noopener noreferrer" class="btn btn-outline">{I['wa']}WhatsApp schreiben</a>
        </div>
        <div class="hero-trust"><span class="hero-trust-txt">{'Team vor Ort in NRW' if NRW else (nah.capitalize() if c['km'] == 0 else 'Studio in Berlin-Wedding · ' + str(c['km']) + ' km entfernt')} · Montage vor Ort · Angebot in 24 h</span></div>
      </div>
      <div class="hero-visual">
        <img class="hero-shot" src="/aussenwerbung-720.webp" srcset="/aussenwerbung-360.webp 360w, /aussenwerbung-540.webp 540w, /aussenwerbung-720.webp 720w, /aussenwerbung.webp 1080w" sizes="360px" width="1080" height="1350" alt="Außenwerbung, Schilder und Leuchtreklame von Masar Werbeagentur" loading="eager" fetchpriority="high">
      </div>
    </div>
  </div>
</section>

<nav aria-label="Breadcrumb" class="bc-bar">
  <div class="container">
    <ol class="bc-list">
      <li><a href="/">Home</a></li>
      <li class="bc-sep">/</li>
      <li><a href="{'/werbeagentur-nrw.html' if NRW else '/werbetechnik-brandenburg.html'}">{'Werbeagentur NRW' if NRW else 'Brandenburg &amp; Umland'}</a></li>
      <li class="bc-sep">/</li>
      <li><span class="bc-cur">Werbeagentur {esc(s)}</span></li>
    </ol>
  </div>
</nav>

<div style="background:var(--teal);padding:.9rem 0;">
  <div class="container">
    <div class="usp-row">{''.join(f'<span>{I["check"]}{u}</span>' for u in ['Alles aus einer Hand', 'Montage vor Ort', 'Festpreis vorab', 'Angebot in 24 h'])}</div>
  </div>
</div>

<section class="section" id="leistungen">
  <div class="container">
    <div class="sec-head center reveal">
      <span class="eyebrow">{I['star']}Was brauchen Sie?</span>
      <h2 class="sec-title">Leistung wählen – <em>Angebot erhalten</em></h2>
      <p class="sec-sub">Tippen Sie auf eine Leistung – der Anfrage-Assistent führt Sie in wenigen Klicks zum Angebot.</p>
    </div>
    <div class="ua-grid">{cards}
    </div>
    <p class="price-note" style="text-align:center;margin-top:1.2rem">Alle Preise netto zzgl. 19&nbsp;% MwSt. Bei Montage in {esc(n)} ist die Anfahrt im Festpreis enthalten und einzeln ausgewiesen.</p>
  </div>
</section>

<section class="section bg-alt">
  <div class="container">
    <div class="sec-head center reveal">
      <span class="eyebrow">{I['check']}So einfach geht's</span>
      <h2 class="sec-title">In drei Schritten <em>zu Ihrer Werbung</em></h2>
    </div>
    <div class="ua-steps">
      <div><h4>Anfragen</h4><p>Leistung wählen, kurz beschreiben, Foto oder Logo mitschicken – per Formular oder WhatsApp.</p></div>
      <div><h4>Festpreis</h4><p>Innerhalb von 24 Stunden bekommen Sie ein klares Angebot mit Entwurf, ohne Überraschungen.</p></div>
      <div><h4>Umsetzung</h4><p>Wir produzieren und montieren bei Ihnen in {esc(n)} – oder liefern Druck und Design direkt zu Ihnen.</p></div>
    </div>
    <p style="text-align:center;margin-top:1.4rem;font-size:15px;color:var(--muted)">Eigene Arbeiten ansehen: <a href="/referenzen.html" style="color:var(--teal-ink);font-weight:700">Referenzen →</a></p>
  </div>
</section>
'''
    fqh = ''.join(f'\n      <div class="faq-item"><button class="faq-q">{q}</button><div class="faq-a"><p>{a}</p></div></div>' for q, a in faq)
    body += sec('Häufige Fragen', f'Werbeagentur {esc(s)} – <em>Fragen &amp; Antworten</em>', None, f'    <div class="faq-wrap">{fqh}\n    </div>', icon='faq')
    pool = NRW_CITIES if NRW else CITIES
    others = ''.join(f'\n      <a href="/werbeagentur-{o["slug"]}.html" class="chip">{o["short"]}</a>' for o in pool if o is not c)
    if NRW: others = ''.join(f'\n      <a href="{u}" class="chip">{t}</a>' for u, t in NRW_NEAR) + others
    body += f'''<section class="section bg-alt" style="padding:2.2rem 0;">
  <div class="container">
    <div class="sec-head reveal" style="margin-bottom:1.2rem;"><span class="eyebrow">{I['link']}Auch in Ihrer Nähe</span></div>
    <div class="chip-row">
      {'' if NRW else '<a href="/" class="chip">Berlin</a>'}
      {'' if NRW else '<a href="/werbetechnik-potsdam.html" class="chip">Potsdam</a>'}{others}
    </div>
  </div>
</section>
<section class="section" id="kontakt">
  <div class="container">
    <div class="sec-head reveal">
      <span class="eyebrow">{I['mail']}Anfrage</span>
      <h2 class="sec-title">Kostenloses Angebot <em>anfordern</em></h2>
      <p class="sec-sub">In fünf kurzen Schritten zur fertigen Anfrage – am Ende senden Sie sie per WhatsApp oder E-Mail.</p>
    </div>
    <div data-assistent data-ort="{esc(n)}"{' data-region="nrw"' if NRW else ''}></div>
    <noscript><div class="form-wrap">
      <form action="/kontakt.php" method="POST" enctype="multipart/form-data">
        <input type="hidden" name="_subject" value="Anfrage Werbeagentur {esc(s)} (Website)">
        <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
        <div class="form-grid">
          <div class="fg"><label for="fo-name">Name *</label><input type="text" id="fo-name" name="name" autocomplete="name" placeholder="Vor- und Nachname" required></div>
          <div class="fg"><label for="fo-telefon">Telefon / WhatsApp</label><input type="tel" id="fo-telefon" name="telefon" autocomplete="tel" placeholder="+49 ..."></div>
        </div>
        <div class="form-grid">
          <div class="fg"><label for="fo-email">E-Mail *</label><input type="email" id="fo-email" name="email" autocomplete="email" placeholder="info@beispiel.de" required></div>
          <div class="fg"><label for="betreffInput">Leistung *</label><input type="text" id="betreffInput" name="betreff" placeholder="z. B. Schild und Schaufenster in {esc(s)}" required></div>
        </div>
        <div class="fg"><label for="fo-nachricht">Ihre Nachricht</label><textarea id="fo-nachricht" name="nachricht" placeholder="Was soll es werden, ungefähre Größe, Wunschtermin – ein paar Stichworte reichen."></textarea></div>
        <div class="fg"><label for="fo-datei">Foto oder Logo (optional)</label><input type="file" id="fo-datei" name="attachment" accept="image/*,.pdf,.svg,.ai,.eps" style="background:#fff;border:1px dashed var(--border);border-radius:8px;padding:11px 14px;color:var(--muted);font-family:'Barlow',sans-serif;font-size:14px;width:100%;cursor:pointer;"></div>
        <div class="consent-row">
          <input type="checkbox" id="fo-consent" name="consent" required>
          <label for="fo-consent">Ich habe die <a href="/datenschutz.html">Datenschutzerklärung</a> zur Kenntnis genommen und stimme der Verarbeitung meiner Daten zu (Art.&nbsp;6 Abs.&nbsp;1 lit.&nbsp;b DSGVO). *</label>
        </div>
        <button type="submit" class="submit-btn">✓ Anfrage senden – kostenlos &amp; unverbindlich</button>
        <p style="text-align:center;font-size:12px;color:var(--muted);margin-top:.6rem;">Oder direkt per <a href="{w}" target="_blank" rel="noopener noreferrer">WhatsApp</a> · Antwort innerhalb von 24 Stunden.</p>
      </form>
    </div></noscript>
  </div>
</section>
{'' if 'assistent.js' in FOOT else '<script src="/assistent.js?v=5" defer></script>'}
<script>
document.querySelectorAll('[data-betreff]').forEach(function(a){{a.addEventListener('click',function(){{var i=document.getElementById('betreffInput');var b=a.getAttribute('data-betreff');if(i){{i.value=b;}}var p=document.getElementById('uaPick');if(p){{p.textContent='Ausgewählt: '+b+' – ergänzen Sie einfach ein paar Stichworte.';p.className='ua-pick on';}}setTimeout(function(){{var n=document.getElementById('fo-name');if(n){{n.focus({{preventScroll:true}});}}}},450);}});}});
</script>
'''
    out = head(c, url, title, desc, faq).replace('</head>', CSS + '\n</head>', 1) + body + '\n' + FOOT
    if NRW: out = out.replace('"name": "Brandenburg & Umland", "item": "' + BASE + 'werbetechnik-brandenburg.html"', '"name": "Werbeagentur NRW", "item": "' + BASE + 'werbeagentur-nrw.html"')
    out = re.sub(r'<div class="scta-txt">.*?</div>', f'<div class="scta-txt">{I["star"]}<span>Werbeagentur {esc(s)}</span> – Angebot in 24 h</div>', out, count=1, flags=re.S)
    if NRW:
        waN = wa(f'Hallo, ich habe eine Anfrage für {s}: ')
        out = re.sub(r'<a href="tel:01785143918" class="nav-phone".*?</a>', lambda m: f'<a href="{waN}" target="_blank" rel="noopener noreferrer" class="nav-phone" aria-label="Per WhatsApp schreiben">WhatsApp</a>', out, count=1, flags=re.S)
        out = re.sub(r'<a href="tel:01785143918" class="mob-call-btn">.*?</a>', '<a href="#kontakt" class="mob-call-btn">E-Mail</a>', out, count=1, flags=re.S)
        out = re.sub(r'<a href="tel:01785143918" class="scta-btn primary">.*?</a>', lambda m: f'<a href="{waN}" target="_blank" rel="noopener noreferrer" class="scta-btn primary">{I["wa"]}WhatsApp</a>', out, count=1, flags=re.S)
    open(ROOT + f, 'w', encoding='utf-8').write(out)
    return f, len(out), len(title), len(desc)

if __name__ == '__main__':
    for c in CITIES + NRW_CITIES:
        print(build(c))
