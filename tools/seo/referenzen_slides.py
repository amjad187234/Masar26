"""Referenzen-Seite: je Leistung eine eigene Bilderstrecke (Slideshow) statt Filter-Raster.
Klick auf ein Bild öffnet die vorhandene Lightbox (blättert nur innerhalb der Kategorie).
Bilder liegen in /referenzen/ (groß: name.webp, Vorschau: name-720.webp falls vorhanden).
Nur echte Projektfotos; Kundennamen nur mit Erlaubnis. Idempotent (Marker).
Aufruf: python3 tools/seo/referenzen_slides.py
"""
import os, re, html
from PIL import Image

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
SEITE = os.path.join(ROOT, 'referenzen.html')
A, Z = '<!-- slides:start -->', '<!-- slides:ende -->'

# (Datei ohne .webp, Bildunterschrift, Alt-Text)
KATEGORIEN = [
    ('leuchtreklame', 'Leuchtreklame', 'Leuchtkästen, Leuchtbuchstaben und Ausleger – produziert und montiert.', [
        ('leuchtkasten-schaufenster-fahrschule-01', 'Fahrschule JAD: Leuchtkasten über dem Schaufenster, direkt nach der Montage', 'Blauer Leuchtkasten „Fahrschule JAD“ über einem bedruckten Schaufenster, davor eine Leiter'),
        ('leuchtreklame-berlin-08', 'Barbershop: Fassadenanlage am Eröffnungstag', 'Fassadenbeschriftung eines Barbershops in Berlin am Eröffnungstag'),
        ('leuchtreklame-berlin-06', 'Ausleger über dem Eingang, während der Montage', 'Runder Ausleger eines Barbershops wird über dem Eingang montiert'),
        ('leuchtreklame-berlin-05', 'Hinterleuchtetes Logo im Innenraum', 'Hinterleuchtetes Logoschild eines Barbershops an einer Innenwand in Berlin'),
        ('leuchtreklame-berlin-09', 'Fassadenschrift über einem Ladengeschäft', 'Goldfarbene Fassadenbeschriftung eines Juweliers in Berlin'),
        ('leuchtreklame-berlin-04', 'Zweisprachige Anlage, deutsch und arabisch', 'Zweisprachige Leuchtwerbung für einen Eventsaal, deutsch und arabisch'),
        ('leuchtreklame-berlin-01', 'Leuchtlogo und Thekenfront in einem Food-Court', 'Leuchtendes Logo und beleuchtete Thekenfront eines Dessert-Ladens in Berlin'),
        ('leuchtreklame-berlin-03', 'Leuchtlogo über der Theke, daneben die Menü-Bildschirme', 'Rundes Leuchtlogo über einer Café-Theke neben zwei Menü-Bildschirmen'),
    ]),
    ('schaufenster', 'Schaufenster & Folien', 'Beschriftung, Druckfolie und Milchglas – von innen oder außen verklebt.', [
        ('schaufensterbeschriftung-showroom-berlin-01', 'LAUFEN Berlin Gallery: weiße Schrift und Logo auf beiden Schaufenstern und der Tür, von innen montiert', 'Showroom-Front in Berlin mit weißer Folienschrift „BERLIN GALLERY“ und LAUFEN-Logo auf zwei großen Schaufenstern und der Eingangstür'),
        ('schaufensterbeschriftung-showroom-berlin-02', 'LAUFEN Berlin Gallery: Folienschrift nach Brand Guide, exakt ausgerichtet', 'Nahaufnahme eines Schaufensters mit weißer Folienschrift „BERLIN GALLERY“ und LAUFEN-Logo, dahinter Showroom mit Leuchten'),
        ('praxis-schaufenster-berlin-02', 'LIVE Physio, Berlin: Eröffnungsbeklebung, Logo-Blenden und Milchglas', 'Fertig beklebte Schaufensterfront einer neuen Physiotherapiepraxis in Berlin mit bedruckten Folien, Logo-Blenden und Milchglas'),
        ('praxis-schaufenster-berlin-01', 'LIVE Physio, Berlin: unser Team bei der Montage', 'Schaufenster einer Physiotherapiepraxis mit bedruckter Folie; zwei Monteure kleben weitere Folie'),
        ('schaufensterfolie-fahrschule-01', 'Fahrschule JAD: bedruckte Schaufensterfolie mit freiem Sichtfenster in der Mitte', 'Bedruckte Schaufensterfolie einer Fahrschule in Blau und Grün mit Leistungen, Website und freiem Sichtfenster'),
        ('fensterbeschriftung-praxis-gold-01', 'Praxis: Schriftzug und Logo in Gold auf dem Oberlicht der Eingangstür', 'Goldene Folienschrift „Physiotherapie“ mit Logo auf dem gewölbten Oberlicht einer Eingangstür'),
        ('schaufensterbeschriftung-pflegedienst-berlin-01', 'Galileo Pflege GmbH, Berlin: Logo und Firmenname am Fenster, Öffnungszeiten an der Tür', 'Weiße Fensterbeschriftung eines ambulanten Pflegedienstes in Berlin mit Logo, Firmenname und Öffnungszeiten an der Tür'),
        ('schaufensterbeschriftung-berlin-01', 'Kioskfront, vollflächig bedruckt', 'Vollflächig bedruckte Front eines Imbiss-Kiosks in Berlin'),
    ]),
    ('fahrzeuge', 'Fahrzeuge', 'Teilbeschriftung bis Vollfolierung – vom Transporter bis zum Imbisswagen.', [
        ('fahrzeugbeschriftung-berlin-04', 'Transporter eines Bauunternehmens, fertig beschriftet', 'Komplett beschrifteter Transporter eines Bauunternehmens in Berlin'),
        ('fahrzeugbeschriftung-berlin-03', 'Seitenbeschriftung mit Leistungsübersicht', 'Fertige Fahrzeugbeschriftung mit Logo, Leistungsliste und Kontaktdaten auf einem Transporter'),
        ('fahrzeugbeschriftung-berlin-01', 'Folie wird auf die Schiebetür aufgezogen', 'Beschriftungsfolie wird auf die Schiebetür eines Transporters aufgezogen'),
        ('fahrzeugbeschriftung-berlin-02', 'Applikationsfolie wird abgezogen', 'Applikationsfolie wird von der frisch verklebten Fahrzeugbeschriftung abgezogen'),
        ('fahrzeugfolierung-berlin-01', 'Vollfolierung eines Imbisswagens', 'Vollflächig folierter Imbisswagen für italienisches Streetfood'),
        ('fahrzeugfolierung-berlin-02', 'Menütafel direkt auf die Klappe foliert', 'Auf den Imbisswagen folierte Speisekarte mit Preisen'),
        ('fahrzeugfolierung-berlin-03', 'Logo und Illustration auf der Rückseite', 'Folierte Rückwand eines Imbisswagens mit Logo und Illustration'),
    ]),
    ('druck', 'Druck & Gastro-Werbung', 'Menütafeln, Kundenstopper, Blenden und Plakate – gedruckt in unserer Werkstatt.', [
        ('menuetafel-imbiss-montiert-01', 'BISSWERK: Menütafel über der Theke, fertig montiert', 'Breite schwarze Menütafel mit Döner, Pasta, Pizza und Burger über der Theke eines Imbisses'),
        ('imbisswagen-menuetafeln-01', 'Grill Chicken: große Menütafel, Aufsteller und Blenden für den Imbisswagen', 'Gelber Imbisswagen mit großer schwarzer Menütafel, zwei Aufstellern und bedruckten Blenden'),
        ('grossformatdruck-werkstatt-01', 'Grill Chicken: Blende für den Imbisswagen im Großformatdruck', 'Großformatdrucker druckt eine Blende mit Logo „Grill Chicken“ und „Kalte Getränke“'),
    ]),
    ('werkstatt', 'Aus der Werkstatt', 'So entstehen die Arbeiten – bevor sie an die Fassade kommen.', [
        ('leuchtkasten-rund-werkstatt-01', 'Feel Good Food by Omar: runder Leuchtkasten beim Testlauf', 'Runder schwarzer Leuchtkasten mit weiß leuchtendem Logo „Feel Good Food by Omar“ in der Werkstatt'),
        ('werkstatt-kaschieren-menuetafel-01', 'BISSWERK-Menütafel: Druckfolie wird mit Heißluft und Rakel aufgezogen', 'Zwei Hände ziehen bedruckte Folie mit Heißluftföhn und Rakel auf eine schwarze Menütafel'),
        ('werkstatt-folie-aufziehen-menuetafel-01', 'Nassverklebung: Folie wird blasenfrei auf die Tafel gerakelt', 'Bedruckte Menütafel mit Seifenwasser, eine Hand rakelt die Folie glatt'),
        ('leuchtreklame-berlin-07', 'Leuchtbuchstaben, fertig verdrahtet', 'Blau leuchtende Profilbuchstaben für einen Barbershop, aufgebaut in der Werkstatt'),
        ('leuchtreklame-berlin-02', 'Leuchtkasten mit ausgefrästen Buchstaben, vor der Montage', 'Leuchtkasten für einen Friseursalon mit hinterleuchteten Buchstaben in der Werkstatt'),
        ('neon-berlin-01', 'LED-Neonbuchstaben in der Fertigung', 'Rote LED-Neonbuchstaben auf der Werkbank, noch nicht verkabelt'),
        ('werkstatt-farbfaecher-01', 'Farbton wählen wir gemeinsam am Folien-Farbfächer aus', 'Aufgefächerter Farbfächer für Klebefolien in der Hand, viele Farbtöne von Grün bis Gelb'),
    ]),
    ('displays', 'Digital Signage', 'Menü-Bildschirme mit Inhalten von uns.', [
        ('digital-signage-berlin-01', 'Menü-Bildschirme über der Theke, Inhalte von uns gestaltet', 'Fünf digitale Menütafeln über der Theke eines Dessert-Ladens in Berlin'),
        ('digital-signage-berlin-02', 'Produktvideo auf dem Thekenbildschirm', 'Digitaler Bildschirm mit Produktvideo über einer Café-Theke'),
    ]),
    ('design', 'Grafikdesign', 'Speisekarten, Logos und Druckdaten.', [
        ('speisekarte-design-berlin-01', 'Speisekarte, Titelseite', 'Gestaltete Titelseite einer Speisekarte mit Logo, Öffnungszeiten und QR-Code'),
        ('speisekarte-design-berlin-02', 'Speisekarte, Innenseite', 'Innenseite einer gestalteten Speisekarte mit Gerichten und Preisen'),
        ('speisekarte-design-berlin-03', 'Speisekarte, Hauptgerichte', 'Seite einer Speisekarte mit Tellergerichten und Produktfotos'),
        ('speisekarte-design-berlin-04', 'Speisekarte, Beilagen und Allergenkennzeichnung', 'Seite einer Speisekarte mit Salaten, Beilagen und Allergenkennzeichnung'),
    ]),
]

CSS = '''<style id="slides-css">
.sl-cat{margin:0 0 2.8rem}
.sl-head{display:flex;align-items:flex-end;justify-content:space-between;gap:1rem;margin:0 0 .9rem}
.sl-head h3{font:900 clamp(1.4rem,3vw,1.9rem)/1.05 "Barlow Condensed",sans-serif;text-transform:uppercase;color:var(--navy);margin:0}
.sl-head p{margin:.25rem 0 0;color:var(--muted);font-size:14.5px}
.sl-head small{color:var(--teal-ink);font-weight:700;letter-spacing:.6px}
.sl-nav{display:flex;gap:.5rem;flex:0 0 auto}
.sl-nav button{width:44px;height:44px;border-radius:50%;border:1px solid var(--border);background:#fff;color:var(--navy);font-size:22px;line-height:1;cursor:pointer;transition:.2s}
.sl-nav button:hover{border-color:var(--teal);color:var(--teal-ink)}
.sl-track{display:flex;gap:1rem;overflow-x:auto;scroll-snap-type:x mandatory;scroll-behavior:smooth;padding:4px 2px 10px;scrollbar-width:none;-webkit-overflow-scrolling:touch}
.sl-track::-webkit-scrollbar{display:none}
.sl-track .gal-item{flex:0 0 calc((100% - 2rem)/3);scroll-snap-align:start}
.sl-track .gal-item:hover{transform:none}
.sl-track .gal-item img{aspect-ratio:4/3;object-fit:cover;height:auto}
.sl-cap{display:block;padding:.65rem .85rem;font-size:13.5px;line-height:1.45;color:var(--muted);text-align:left;background:#fff}
.sl-dots{display:flex;gap:6px;justify-content:center;margin-top:.4rem}
.sl-dots button{width:8px;height:8px;border-radius:4px;border:0;background:var(--border);padding:0;cursor:pointer;transition:width .25s,background .25s}
.sl-dots button[aria-current="true"]{width:22px;background:var(--teal)}
@media(max-width:900px){.sl-track .gal-item{flex-basis:calc((100% - 1rem)/2)}}
@media(max-width:600px){.sl-track .gal-item{flex-basis:84%}.sl-nav{display:none}}
@media(prefers-reduced-motion:reduce){.sl-track{scroll-behavior:auto}}
</style>'''

JS = '''<script id="slides-js">
document.addEventListener('DOMContentLoaded', function(){
  var ruhig = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.sl-cat').forEach(function(cat){
    var tr = cat.querySelector('.sl-track'), items = tr.children, dots = cat.querySelector('.sl-dots');
    function breite(){ return items[0] ? items[0].getBoundingClientRect().width + 16 : tr.clientWidth; }
    function pos(){ return Math.round(tr.scrollLeft / breite()); }
    function geh(i){ var max = tr.scrollWidth - tr.clientWidth; var x = i * breite(); if (x > max + 4) x = 0; if (x < 0) x = max; tr.scrollTo({left: x, behavior: ruhig ? 'auto' : 'smooth'}); }
    cat.querySelector('.sl-prev').addEventListener('click', function(){ geh(pos() - 1); });
    cat.querySelector('.sl-next').addEventListener('click', function(){ geh(pos() + 1); });
    Array.prototype.forEach.call(items, function(it, i){ var b = document.createElement('button'); b.type = 'button'; b.setAttribute('aria-label', 'Bild ' + (i + 1)); b.addEventListener('click', function(){ geh(i); }); dots.appendChild(b); });
    function markieren(){ var p = Math.min(pos(), items.length - 1); if (tr.scrollLeft + tr.clientWidth >= tr.scrollWidth - 4) p = items.length - 1; dots.querySelectorAll('button').forEach(function(b, i){ b.setAttribute('aria-current', String(i === p)); }); }
    tr.addEventListener('scroll', function(){ window.requestAnimationFrame(markieren); }, {passive: true}); markieren();
    if (ruhig || items.length < 2) return;
    var halt = false, sicht = false;
    ['mouseenter', 'focusin', 'touchstart'].forEach(function(e){ cat.addEventListener(e, function(){ halt = true; }, {passive: true}); });
    ['mouseleave', 'focusout'].forEach(function(e){ cat.addEventListener(e, function(){ halt = false; }); });
    if ('IntersectionObserver' in window) new IntersectionObserver(function(es){ sicht = es[0].isIntersecting; }, {threshold: .4}).observe(tr);
    setInterval(function(){ var v = tr.querySelector('video'); if (sicht && !halt && !document.hidden && !(v && !v.paused) && !document.getElementById('lb').classList.contains('open')) geh(pos() + 1); }, 4500);
  });
});
</script>'''

VA, VZ = '<!-- videos:start -->', '<!-- videos:ende -->'
FILM = ('digital-signage-donuts-film', 'Werbevideo für CRAVÉZ Berlin', 'Von uns gedreht und geschnitten: Cookies, Eis und Saucen direkt am Tresen – Marketingvideo für die Bildschirme im Laden und für Social Media, 26 Sekunden.')
# Menütafeln mit hellem Hintergrund (rote Imbiss-Tafeln bewusst nicht auf der Referenzseite)
TAFELN = [
    ('digital-signage-donuts-01', 'Handmade Donuts', 'Sortiment und Boxpreise im Wechsel mit Produktaufnahmen.'),
    ('digital-signage-bubble-tea-01', 'Signature Bubble Tea', 'Acht Sorten mit Preisen für zwei Größen.'),
    ('digital-signage-bubble-tea-02', 'Bubble Tea Milky Classics', 'Vier Klassiker, ruhig animiert.'),
    ('digital-signage-restaurant-01', 'Manakisch & Teigtaschen', 'Tagesangebot mit Preisen.'),
    ('digital-signage-restaurant-02', 'Burger', 'Vier Burger mit Preisschildern.'),
    ('digital-signage-restaurant-03', 'Eiergerichte & Salate', 'Frühstück und Salate auf einer Tafel.'),
]


def dauer(name):
    import subprocess
    try:
        return round(float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0',
                                           os.path.join(ROOT, 'videos', name + '.mp4')], capture_output=True, text=True).stdout))
    except Exception:
        return 0


def videokarte(name, titel, text, eager=False):
    w, h = Image.open(os.path.join(ROOT, 'videos', name + '.webp')).size
    return (f'<figure class="vid-card"><a class="vid-play" href="/videos/{name}.mp4" data-video data-w="1280" data-h="720" aria-label="Video abspielen: {html.escape(titel, quote=True)}">'
            f'<img src="/videos/{name}.webp" alt="{html.escape(titel, quote=True)} – Standbild aus dem Video" loading="{"eager" if eager else "lazy"}" width="{w}" height="{h}">'
            f'<span class="vid-icon" aria-hidden="true"></span></a><figcaption><strong>{html.escape(titel)}</strong>{html.escape(text)}</figcaption></figure>\n')


def videoblock():
    karten = ''.join(videokarte(n, t, x + (f' {dauer(n)} Sekunden.' if not x.endswith('Sekunden.') else '')) for n, t, x in TAFELN)
    return (f'{VA}\n<style>.vid-film{{max-width:860px;margin:0 auto 2rem}}.sl-track .vid-card{{flex:0 0 calc((100% - 2rem)/3);scroll-snap-align:start;margin:0}}'
            f'@media(max-width:900px){{.sl-track .vid-card{{flex-basis:calc((100% - 1rem)/2)}}}}@media(max-width:600px){{.sl-track .vid-card{{flex-basis:84%}}}}</style>\n'
            f'<div class="vid-film">{videokarte(*FILM, eager=True)}</div>\n'
            f'<div class="sl-cat" id="ref-menuetafeln"><div class="sl-head"><div><small>{len(TAFELN)} Videos</small><h3>Menütafeln</h3><p>Antippen startet das Video.</p></div>'
            f'<div class="sl-nav"><button class="sl-prev" type="button" aria-label="Menütafeln: vorheriges Video">‹</button><button class="sl-next" type="button" aria-label="Menütafeln: nächstes Video">›</button></div></div>\n'
            f'<div class="sl-track" role="region" aria-label="Bilderstrecke Menütafeln" tabindex="0">\n{karten}</div><div class="sl-dots"></div></div>\n{VZ}\n')



def bild(name):
    gross = f'/referenzen/{name}.webp'
    klein = f'/referenzen/{name}-720.webp' if os.path.exists(os.path.join(ROOT, 'referenzen', name + '-720.webp')) else gross
    w, h = Image.open(os.path.join(ROOT, klein.lstrip('/'))).size
    return gross, klein, w, h


def block():
    teile = []
    for i, (key, titel, text, bilder) in enumerate(KATEGORIEN):
        karten = ''
        for j, (name, cap, alt) in enumerate(bilder):
            gross, klein, w, h = bild(name)
            lade = 'eager' if i == 0 and j < 3 else 'lazy'
            karten += (f'<button class="gal-item" type="button" data-cat="{key}" data-src="{gross}" data-cap="{html.escape(cap, quote=True)}">'
                       f'<img src="{klein}" alt="{html.escape(alt, quote=True)}" loading="{lade}" width="{w}" height="{h}">'
                       f'<span class="sl-cap">{html.escape(cap)}</span></button>\n')
        teile.append(f'''<div class="sl-cat reveal" id="ref-{key}">
  <div class="sl-head"><div><small>{len(bilder)} Bilder</small><h3>{titel}</h3><p>{text}</p></div>
  <div class="sl-nav"><button class="sl-prev" type="button" aria-label="{titel}: vorheriges Bild">‹</button><button class="sl-next" type="button" aria-label="{titel}: nächstes Bild">›</button></div></div>
  <div class="sl-track" role="region" aria-label="Bilderstrecke {titel}" tabindex="0">
{karten}  </div>
  <div class="sl-dots"></div>
</div>''')
    nav = ''.join(f'<a class="filter-btn" href="#ref-{k}">{t}<span class="filter-count">{len(b)}</span></a>' for k, t, _, b in KATEGORIEN)
    return (f'{A}\n{CSS}\n<div class="filters" role="navigation" aria-label="Zu einer Leistung springen">{nav}</div>\n'
            + '\n'.join(teile) + f'\n{JS}\n{Z}\n')


def main():
    s = open(SEITE, encoding='utf-8').read()
    if A in s:
        s = re.sub(re.escape(A) + r'.*?' + re.escape(Z) + r'\n?', block(), s, flags=re.S)
    else:   # erstes Mal: Filter + Raster ersetzen
        m = re.search(r'    <div class="filters" role="group".*?<p class="gal-empty" id="galEmpty" hidden>.*?</p>\n', s, flags=re.S)
        if not m: raise SystemExit('Galerie nicht gefunden')
        s = s[:m.start()] + block() + s[m.end():]
        s = s.replace('<p class="sec-sub">Filtern Sie nach dem, was Sie selbst vorhaben. Ein Klick auf ein Bild zeigt es in groß.</p>',
                      '<p class="sec-sub">Jede Leistung hat ihre eigene Bilderstrecke – wischen oder mit den Pfeilen blättern. Ein Klick zeigt das Bild in groß.</p>')
        # Lightbox blättert nur innerhalb der Kategorie des geöffneten Bildes
        s = s.replace("function visible(){ return items.filter(function(it){ return !it.hidden; }); }",
                      "function visible(){ var c = opener ? opener.dataset.cat : null; return items.filter(function(it){ return !it.hidden && (!c || it.dataset.cat === c); }); }")
    if VA in s:
        s = re.sub(re.escape(VA) + r'.*?' + re.escape(VZ) + r'\n?', videoblock(), s, flags=re.S)
    else:
        m = re.search(r'    <div class="vid-grid">.*?\n    </div>\n', s, flags=re.S)
        if m: s = s[:m.start()] + videoblock() + s[m.end():]
    s = s.replace('<p class="sec-sub">Eine Menütafel steht selten still. Zwei Beispiele – alle acht Tafeln aus drei Betrieben liegen auf der Seite zu dieser Leistung.</p>',
                  '<p class="sec-sub">Eine Menütafel steht selten still. Oben ein Werbevideo, das wir vor Ort gedreht haben, darunter Menütafeln aus unserem Studio.</p>')
    open(SEITE, 'w', encoding='utf-8').write(s)
    print(sum(len(k[3]) for k in KATEGORIEN), 'Bilder in', len(KATEGORIEN), 'Bilderstrecken')


if __name__ == '__main__':
    main()
