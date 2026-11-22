#!/usr/bin/env python3
"""Erzeugt schaufensterfolie-store-eroeffnung.html (Schaufensterfolie vor der Store-Eröffnung, „Opening Soon“)
aus der Vorlage schaufenster-weihnachten-black-friday.html. Zielgruppe: Retail-Marken, Filialisten, Visual Merchandising,
Ladenbau – mit englischem Abschnitt für internationale Marken. Keine Kundennamen, keine erfundenen Zahlen.
Aufruf: python3 tools/folien/store_eroeffnung_page.py"""
import html, json, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
VORLAGE = os.path.join(ROOT, 'schaufenster-weihnachten-black-friday.html')
ZIEL = 'schaufensterfolie-store-eroeffnung.html'
URL = 'https://masar-werbeagentur.de/' + ZIEL
TITEL = 'Schaufensterfolie zur Store-Eröffnung – Opening Soon'
DESC = ('Schaufenster vor der Eröffnung vollflächig bekleben: farbige oder blickdichte Folie, Logo und „Opening Soon“. '
        'Montage und Entfernung in Berlin, Hamburg und NRW.')
WA = ('https://wa.me/491785143918?text=Hallo%2C%20wir%20er%C3%B6ffnen%20einen%20Store%20und%20m%C3%B6chten%20die%20Schaufenster'
      '%20vorher%20bekleben%20lassen.%20Ich%20schicke%20Ihnen%20Ma%C3%9Fe%20und%20Fotos.')

IC = {
 'flaeche': '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/>',
 'auge': '<path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/><path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/><path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/><path d="m2 2 20 20"/>',
 'schrift': '<path d="M4 7V4h16v3"/><path d="M9 20h6"/><path d="M12 4v16"/>',
 'wechsel': '<path d="m16 3 4 4-4 4"/><path d="M20 7H4"/><path d="m8 21-4-4 4-4"/><path d="M4 17h16"/>',
 'muster': '<circle cx="13.5" cy="6.5" r=".5" fill="currentColor"/><circle cx="17.5" cy="10.5" r=".5" fill="currentColor"/><circle cx="8.5" cy="7.5" r=".5" fill="currentColor"/><circle cx="6.5" cy="12.5" r=".5" fill="currentColor"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/>',
 'chat': '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
}

KARTEN = [
 ('flaeche', 'Farbige Folie, vollflächig',
  'Transparente Farbfolie in Ihrem Markenton auf allen Scheiben: Von außen wirkt die Front wie eine farbige Fläche, innen bleibt es hell. Geklebt wird von innen, geschützt vor Wetter und Passanten.',
  'Farbton nach Muster'),
 ('auge', 'Blickdicht während des Umbaus',
  'Wenn niemand die Baustelle sehen soll, decken wir die Scheiben mit blickdichter, bedruckter oder einfarbiger Folie ab. Der Laden wirbt schon, während drinnen noch gebaut wird.',
  'Aktionsfolie ab 190 € netto (Berlin)'),
 ('schrift', 'Logo &amp; „Opening Soon“',
  'Logo, Schriftzug und Webadresse schneiden wir als Folienplott aus Ihren Vektordaten und setzen sie von außen auf die Scheibe – maßgenau nach Ihrem Layout, auf einer Linie über mehrere Fenster und die Tür.',
  'Beschriftung ab 149 € netto (Berlin)'),
 ('wechsel', 'Entfernen in Etappen',
  'Zur Eröffnung nehmen wir den Schriftzug ab, die Farbfläche bleibt auf Wunsch noch einige Wochen. Beide Termine planen wir von Anfang an mit ein, damit am Eröffnungstag nichts offen ist.',
  'Termine im Angebot'),
 ('muster', 'Muster &amp; Mockup vorab',
  'Bevor wir produzieren, sehen Sie den Farbton als Muster auf Glas – bei Tag und mit Licht von innen – und ein maßstäbliches Mockup mit allen Maßen und Höhen zur Freigabe.',
  'Freigabe vor der Produktion'),
 ('chat', 'Ein Ansprechpartner',
  'Abstimmung mit Visual Merchandising, Store-Team und Zentrale – auf Deutsch, Englisch, Arabisch oder Türkisch. Rechnung mit Ihrer Bestell- oder Projektnummer.',
  'Preise netto zzgl. 19 % MwSt.'),
]

SCHRITTE = [
 ('Maße &amp; Fotos', 'Sie schicken die Maße jeder Scheibe, Fotos von innen und außen und Ihr Layout. Fehlen Maße, nehmen wir sie vor Ort auf.'),
 ('Muster &amp; Mockup', 'Sie erhalten Angebot, Farbmuster und ein maßstäbliches Mockup. Erst nach Ihrer Freigabe bestellen wir das Material.'),
 ('Montage', 'Unser Team reinigt die Klebeflächen, klebt die Fläche von innen und setzt Logo und Schrift von außen – in Berlin, Hamburg oder NRW.'),
 ('Eröffnung', 'Am vereinbarten Tag nehmen wir den Schriftzug ab, später die Fläche. Das Glas ist danach wieder frei.'),
]

BRAUCHEN = [
 ('Scheibenmaße', 'Breite × Höhe', 'Jede Scheibe einzeln, auch Oberlichter, Tür und schmale Seitenscheiben. Eine Skizze oder der Ladenbauplan genügt.'),
 ('Fotos', 'innen und außen', 'Von der ganzen Front und von Details: Rahmen, Griffe, vorhandene Beschriftung, Aufkleber.'),
 ('Logo &amp; Layout', 'Vektordatei', 'Logo und Schrift als AI, EPS, SVG oder Vektor-PDF. Aus Bilddateien können wir nachzeichnen, das Original ist aber genauer.'),
 ('Farbton', 'nach Farbkarte', 'Ihr Markenton als Referenz – wir schlagen die nächstliegenden Folienfarben vor und zeigen sie auf Glas.'),
 ('Termine', 'drei Daten', 'Montagetag, Eröffnungstag und der Tag, an dem die Fläche wieder ab soll.'),
 ('Zugang', 'vor Ort', 'Wer öffnet, ab wann darf gearbeitet werden, gibt es Vorgaben des Centers oder Vermieters, liegt eine alte Beschriftung auf dem Glas?'),
]

FAQ = [
 ('Was kostet eine Schaufensterfolie zur Eröffnung?',
  'Das hängt von der Glasfläche, der Folie und der Zahl der Termine ab – Montage, Abnahme des Schriftzugs und Entfernen der Fläche. Als Orientierung: Aktionsfolie beginnt in Berlin bei 190 € netto, Schaufensterbeschriftung bei 149 € netto; in NRW und Hamburg bei 229 € und 179 € netto. Für eine ganze Front erhalten Sie nach Maßen und Fotos ein festes Angebot.'),
 ('Wie früh sollten wir anfragen?',
  'So früh wie möglich. Farbmuster, Mockup und Freigabe brauchen einige Tage, und farbige Transparentfolie in der passenden Breite ist nicht immer ab Lager lieferbar – die Beschaffung kann mehrere Werktage bis rund zwei Wochen dauern. Den Montagetermin bestätigen wir, sobald das Material sicher ist.'),
 ('Bleibt es im Laden hell?',
  'Mit transparenter Farbfolie ja: Sie färbt das Licht, lässt es aber durch. Bei Tageslicht sieht man von außen kaum hinein, abends leuchtet die Front in Ihrer Farbe, wenn innen Licht brennt. Blickdichte Folie nimmt dagegen Licht weg – welche Variante passt, zeigen wir mit einem Muster auf Glas.'),
 ('Sieht man bei großen Scheiben Stöße?',
  'Farbige Folie kommt auf Rollen mit begrenzter Breite. Breite Scheiben kleben wir deshalb in Bahnen mit feinen, geraden Stößen, die wir symmetrisch setzen. Aus der Nähe sind sie zu erkennen, aus dem üblichen Abstand von der Straße kaum. Im Mockup zeichnen wir die Stöße vorher ein.'),
 ('Lässt sich die Folie wieder entfernen?',
  'Ja. Für befristete Einsätze verwenden wir Folien, die sich in der Regel ohne Kleberreste vom Glas lösen. Das Entfernen übernehmen wir und planen es gleich mit ein. Schäden, die schon im Glas sind – etwa alte Kratzer – halten wir vor der Montage mit Fotos fest.'),
 ('Können Sie die alte Beschriftung des Vormieters entfernen?',
  'Ja, das berechnen wir nach Aufwand. Folienschrift ist schnell ab; aufgeklebte Platten oder alte Klebebänder brauchen spezielle Reiniger und mehr Zeit. Ein Foto vorab hilft uns, das richtig einzuschätzen.'),
 ('Montieren Sie auch in mehreren Städten?',
  'Ja. In Berlin sitzen wir selbst, in Hamburg und in NRW arbeiten eigene Teams vor Ort. Ein Layout, ein Angebot, ein Ansprechpartner – die Montage planen wir je Standort.'),
]

EN_TEXT = [
 'Opening a store in Germany? We cover your shop windows before the opening: full-surface coloured or opaque film on the inside, your logo and “Opening Soon” lettering on the outside.',
 'You send us the pane sizes, photos and your artwork. We send film samples on glass, a to-scale mockup with all dimensions for approval, install on site and remove the film again after the opening – in one step or in stages.',
 'Our teams install in Berlin, Hamburg and North Rhine-Westphalia. Communication, quotation and invoice in English, with your PO or project reference.',
]


def e(t):
    return html.escape(t, quote=True)


def svg(name):
    return f'<svg class="i-svg" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{IC[name]}</svg>'


def main():
    s = open(VORLAGE, encoding='utf-8').read()
    alt_url = 'https://masar-werbeagentur.de/schaufenster-weihnachten-black-friday.html'
    alt_titel = 'Schaufenster Black Friday &amp; Weihnachten – Aktionsfolie'
    alt_desc = re.search(r'<meta name="description" content="([^"]*)"', s).group(1)
    s = s.replace(alt_url, URL).replace(alt_titel, e(TITEL)).replace(alt_desc, e(DESC))

    # JSON-LD neu
    bl = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://masar-werbeagentur.de/"},
        {"@type": "ListItem", "position": 2, "name": "Schaufensterbeschriftung", "item": "https://masar-werbeagentur.de/schaufensterbeschriftung-berlin.html"},
        {"@type": "ListItem", "position": 3, "name": "Schaufensterfolie zur Store-Eröffnung", "item": URL}]}
    svc = {"@context": "https://schema.org", "@type": "Service",
           "name": "Schaufensterfolie zur Store-Eröffnung (Opening Soon)",
           "description": "Befristete Schaufensterfolierung vor der Eröffnung eines Ladens: vollflächige farbige oder blickdichte Folie innen, Logo und Schriftzug außen, Muster und Mockup vorab, Montage und Entfernung durch Teams in Berlin, Hamburg und NRW.",
           "serviceType": "Befristete Schaufensterfolierung zur Neueröffnung",
           "audience": {"@type": "BusinessAudience", "audienceType": "Einzelhandel, Filialisten, Marken, Visual Merchandising, Ladenbau"},
           "provider": {"@type": ["LocalBusiness", "ProfessionalService"], "@id": "https://masar-werbeagentur.de/#identity",
                        "name": "Masar Werbeagentur", "url": "https://masar-werbeagentur.de", "telephone": "+49 178 5143918",
                        "email": "info@masar-werbeagentur.de",
                        "address": {"@type": "PostalAddress", "streetAddress": "Bristolstraße 19E", "addressLocality": "Berlin",
                                    "addressRegion": "Berlin", "postalCode": "13349", "addressCountry": "DE"}},
           "areaServed": [{"@type": "City", "name": "Berlin"}, {"@type": "State", "name": "Brandenburg"},
                          {"@type": "State", "name": "Nordrhein-Westfalen"}, {"@type": "City", "name": "Hamburg"}],
           "availableLanguage": ["de", "en", "ar", "tr"]}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": f, "acceptedAnswer": {"@type": "Answer", "text": a}} for f, a in FAQ]}
    bloecke = list(re.finditer(r'<script type="application/ld\+json">.*?</script>', s, re.S))
    assert len(bloecke) >= 3
    neu = '\n'.join('<script type="application/ld+json">\n' + json.dumps(x, ensure_ascii=False, indent=2) + '\n</script>' for x in (bl, svc, faq))
    s = s[:bloecke[0].start()] + neu + s[bloecke[2].end():]

    # Hauptinhalt zwischen HERO und KONTAKT ersetzen
    a = s.index('<!-- HERO -->'); b = s.index('<!-- KONTAKT -->')
    regionen = re.search(r'<section class="section" aria-labelledby="regionen-heading">.*?</section>', s, re.S).group(0)
    regionen = regionen.replace('class="section"', 'class="section bg-alt"', 1)
    karten = ''.join(
        f'''
      <div class="svc-card" role="listitem">
        <div class="svc-icon" aria-hidden="true">{svg(i)}</div>
        <h3>{t}</h3>
        <p>{p}</p>
        <span class="price-tag">{tag}</span>
      </div>''' for i, t, p, tag in KARTEN)
    schritte = ''.join(
        f'''
      <div>
        <div class="step-num" aria-hidden="true">{n}</div>
        <div class="step-title">{t}</div>
        <p class="step-desc">{p}</p>
      </div>''' for n, (t, p) in enumerate(SCHRITTE, 1))
    brauchen = ''.join(
        f'''
      <div class="zeit-card">
        <h3>{t}</h3>
        <div class="zeit-datum">{d}</div>
        <p>{p}</p>
      </div>''' for t, d, p in BRAUCHEN)
    faq_html = ''.join(
        f'''
      <div class="faq-item">
        <button class="faq-q" aria-expanded="false">{e(f)}</button>
        <div class="faq-a"><p>{e(x)}</p></div>
      </div>''' for f, x in FAQ)
    en = ''.join(f'<p style="margin:0 0 .9rem">{e(t)}</p>' for t in EN_TEXT)
    haupt = f'''<!-- HERO -->
<section class="hero" aria-labelledby="hero-heading">
  <div class="hero-lines" aria-hidden="true"></div>
  <div class="container">
    <div class="hero-inner hero-split">
      <div>
        <div class="hero-badge" aria-hidden="true"><svg class="i-inline" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{IC['flaeche']}</svg>Neueröffnung · Umbau · Pop-up</div>
        <h1 id="hero-heading">Schaufensterfolie zur Store-Eröffnung<span style="position:absolute;left:-9999px"> – </span><em>Opening Soon, bis Sie öffnen.</em></h1>
        <p class="hero-sub">Für Marken, Filialisten, Visual Merchandising und Ladenbau: Wir bekleben Ihre Schaufenster vor der Eröffnung vollflächig, setzen Logo und Schriftzug darauf und nehmen alles wieder ab, wenn der Laden öffnet – in Berlin, Hamburg und NRW.</p>
        <div class="kopf-preis"><b>Festes Angebot nach Maßen und Fotos</b><span>Muster auf Glas und maßstäbliches Mockup vor der Produktion</span></div>
        <ul class="kopf-checks">
          <li>Farbige oder blickdichte Folie auf der ganzen Front</li>
          <li>Logo und „Opening Soon“ nach Ihrem Layout</li>
          <li>Montage und Entfernung – auch in Etappen</li>
          <li>Beratung auf Deutsch, Englisch, Arabisch &amp; Türkisch</li>
        </ul>
        <div class="hero-btns">
          <a href="#kontakt" class="btn btn-teal" data-as-open="schaufenster:3">Projekt anfragen</a>
          <a href="{WA}" target="_blank" rel="noopener noreferrer" class="btn btn-outline"><svg class="i-inline" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{IC['chat']}</svg> Maße &amp; Fotos per WhatsApp</a>
        </div>
        <div class="hero-trust">
          <a class="hero-trust-txt" href="#english" style="background:rgba(88,208,189,.12);border:1px solid rgba(88,208,189,.3);color:var(--teal);padding:4px 10px;border-radius:4px;font-size:11px;letter-spacing:1px;text-decoration:none">International brands: information in English ↓</a>
        </div>
      </div>
      <div class="hero-visual">
        <img class="hero-shot" src="/opening-soon-front.webp" srcset="/opening-soon-front-360.webp 360w, /opening-soon-front-540.webp 540w, /opening-soon-front-720.webp 720w, /opening-soon-front.webp 1080w" sizes="(max-width:900px) 340px, 360px" width="1080" height="1350" alt="Illustration: Ladenfront vor der Eröffnung – farbige Folie auf allen Scheiben, darauf Markenname, „Opening Soon“ und Webadresse" fetchpriority="high">
      </div>
    </div>
  </div>
</section>

<!-- LEISTUNG -->
<section class="section" aria-labelledby="vorteile-heading">
  <div class="container">
    <div class="sec-head">
      <span class="eyebrow">Für Marken, Filialen &amp; Ladenbau</span>
      <h2 class="sec-title" id="vorteile-heading">Die Front wirbt, <em>bevor der Laden öffnet</em></h2>
      <p class="sec-sub">Zwischen Schlüsselübergabe und Eröffnung liegen oft Wochen. In dieser Zeit ist das Schaufenster Ihre größte Werbefläche – und der Sichtschutz für den Umbau.</p>
    </div>
    <div class="svc-grid" role="list">{karten}
    </div>
    <figure class="ideen-foto ideen-foto--breit">
      <img src="/opening-soon-phasen-720.webp" srcset="/opening-soon-phasen-720.webp 720w, /opening-soon-phasen.webp 1600w" sizes="(max-width:700px) 100vw, 500px" width="720" height="432" alt="Illustration in drei Schritten: vor der Eröffnung Farbfläche mit Logo und Schriftzug, zur Eröffnung nur noch die Farbfläche, danach freies Glas" loading="lazy">
      <figcaption>
        <span class="eyebrow" style="margin-bottom:.6rem">So läuft es</span>
        <strong>Eine Front, drei Phasen</strong>
        Vor der Eröffnung trägt die Front Ihre Farbe, Ihr Logo und den Schriftzug. Am Eröffnungstag nehmen wir die Schrift ab, die Farbfläche kann bleiben. Später entfernen wir auch sie – das Glas ist wieder frei. Die Abbildung ist eine Illustration mit Beispielmarke.
      </figcaption>
    </figure>
  </div>
</section>

<!-- ABLAUF -->
<section class="section bg-alt" aria-labelledby="ablauf-heading">
  <div class="container">
    <div class="sec-head">
      <span class="eyebrow">So läuft es ab</span>
      <h2 class="sec-title" id="ablauf-heading">In vier Schritten bis zur <em>Eröffnung</em></h2>
    </div>
    <div class="steps-grid">{schritte}
    </div>
  </div>
</section>

<!-- VORAB -->
<section class="section" aria-labelledby="termine-heading">
  <div class="container">
    <div class="sec-head">
      <span class="eyebrow">Checkliste</span>
      <h2 class="sec-title" id="termine-heading">Was wir <em>vorab brauchen</em></h2>
      <p class="sec-sub">Je vollständiger die Angaben, desto schneller steht das Angebot – und desto sicherer der Montagetermin.</p>
    </div>
    <div class="zeit-grid">{brauchen}
    </div>
    <div class="zeit-hinweis">
      <strong>Gut zu wissen:</strong> Von innen kleben wir das ganze Jahr. Für Logo und Schrift <strong>von außen</strong> muss die Scheibe trocken sein und die Temperatur zur Folie passen – im Winter legen wir den Außentermin deshalb auf einen geeigneten Tag. Eine Lieferzeit nennen wir <strong>verbindlich mit dem Angebot</strong>.
    </div>
  </div>
</section>

<!-- ENGLISH -->
<section class="section bg-alt" id="english" aria-labelledby="english-heading" lang="en">
  <div class="container">
    <div class="sec-head">
      <span class="eyebrow">For international brands</span>
      <h2 class="sec-title" id="english-heading">Window film for your <em>store opening in Germany</em></h2>
    </div>
    <div style="max-width:760px;margin:0 auto;background:#fff;border:1px solid var(--border);border-radius:14px;padding:1.6rem 1.8rem;font-size:16px;line-height:1.7;color:var(--text)">
      {en}
      <p style="margin:0"><a href="mailto:info@masar-werbeagentur.de?subject=Window%20film%20for%20store%20opening" style="color:var(--teal-ink);font-weight:700">info@masar-werbeagentur.de</a> · <a href="{WA}" target="_blank" rel="noopener noreferrer" style="color:var(--teal-ink);font-weight:700">WhatsApp +49 178 514 3918</a></p>
    </div>
  </div>
</section>

<!-- REGIONEN -->
{regionen.replace('class="section bg-alt"', 'class="section"', 1)}

<!-- FAQ -->
<section class="section bg-alt" aria-labelledby="faq-heading">
  <div class="container">
    <div class="sec-head">
      <span class="eyebrow">Häufige Fragen</span>
      <h2 class="sec-title" id="faq-heading">Fragen zur <em>Eröffnungsfolie</em></h2>
    </div>
    <div class="faq-wrap">{faq_html}
    </div>
  </div>
</section>

<!-- CTA -->
<div class="cta-band">
  <div class="container">
    <h2>Eröffnung geplant? <em style="color:var(--teal-ink);font-style:normal;">Jetzt Folie anfragen</em></h2>
    <p>Maße und Fotos schicken, Muster und Mockup erhalten, Montagetermin sichern – für einen Store oder mehrere.</p>
    <div class="btns">
      <a href="#kontakt" class="btn btn-teal" data-as-open="schaufenster:3">Anfrage-Assistent starten →</a>
      <a href="{WA}" target="_blank" rel="noopener noreferrer" class="btn btn-outline">WhatsApp schreiben</a>
    </div>
  </div>
</div>

'''
    s = s[:a] + haupt + s[b:]
    # Hinweis-Kasten der Vorlage entfernen (setzt ratgeber_hinweise.py neu)
    s = re.sub(r'<!-- ratgeber-hinweis -->.*?<!-- /ratgeber-hinweis -->\n?', '', s, flags=re.S)
    # Kontaktbereich und Reste der Vorlage
    for alt, neu2 in [
        ('Saison-<em>Angebot</em> anfordern', 'Projekt <em>anfragen</em>'),
        ('Wählen Sie „Aktion / Eröffnung“ und nennen Sie Ort, Termin und Anzahl der Filialen. Fotos der Scheiben helfen uns beim Angebot.',
         'Wählen Sie „Aktion / Eröffnung“ und nennen Sie Ort, Eröffnungstermin und Anzahl der Scheiben. Maße und Fotos helfen uns beim Angebot.'),
        ('Neue Anfrage – Schaufenster Black Friday / Weihnachten', 'Neue Anfrage – Schaufensterfolie zur Store-Eröffnung'),
        ('thema=Schaufenster%20Black%20Friday%20%26%20Weihnachten', 'thema=Schaufensterfolie%20zur%20Store-Er%C3%B6ffnung'),
    ]:
        assert alt in s, alt
        s = s.replace(alt, neu2)
    s = re.sub(r'(<textarea id="beschreibung" name="beschreibung" placeholder=")[^"]*(")',
               r'\1z. B. neuer Store in Hamburg, Eröffnung am …, 2 Schaufenster je 250 × 300 cm und Tür, farbige Folie innen, Logo und „Opening Soon“ außen, Entfernung nach der Eröffnung\2', s)
    s = re.sub(r'https://wa\.me/491785143918\?text=Hallo%2C%20wir%20m%C3%B6chten%20unser%20Schaufenster[^"]*', WA, s)
    reste = [w for w in ('Black Friday', 'Weihnacht', 'Saison-', 'Januar-Sale', 'Black Week') if w in s]
    assert not reste, reste
    open(os.path.join(ROOT, ZIEL), 'w', encoding='utf-8').write(s)
    print(ZIEL, len(s), 'Zeichen,', len(FAQ), 'FAQ')


if __name__ == '__main__':
    main()
