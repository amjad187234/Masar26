"""Werkstatt-Aussagen an die tatsächliche Arbeitsweise anpassen (Inhaber, 05.11.2026):
Masar hat ein Studio in Berlin-Wedding; gefertigt (Druck, Plott, Schilder, Folien) wird in einer Partnerwerkstatt,
beleuchtete Anlagen baut und montiert ein eingetragener Partnerbetrieb (siehe partner_hinweis.py).
Keine „eigene Werkstatt“, kein „Druck im eigenen Haus“, keine „eigenen Maschinen“ behaupten.
Wirkt auf Seiten UND Generatoren (damit Neu-Erzeugen nichts zurückholt). Idempotent.
Aufruf: python3 tools/seo/partnerwerkstatt.py [--dry]
"""
import os, re, sys
ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))).rstrip('/')
OHNE = ('.git', '.claude', 'node_modules', '__pycache__', os.path.join('tools', 'angebot', 'privat'), os.path.join('tools', 'brand'))
ENDUNG = ('.html', '.js', '.txt', '.py', '.json', '.php', '.md')
SELBST = os.path.abspath(__file__)

# (alt, neu) – Reihenfolge wichtig: spezielle Sätze vor allgemeinen Mustern
R = [
    ('Wir gestalten, drucken auf eigenen Großformat-Druckern, schneiden am Plotter und montieren vor Ort.',
     'Wir gestalten, unsere Partnerwerkstatt in Berlin druckt und fertigt, und wir montieren vor Ort.'),
    ('Wir gestalten, lassen in unserer Partnerwerkstatt in Berlin drucken und fertigen und montieren vor Ort.',
     'Wir gestalten, unsere Partnerwerkstatt in Berlin druckt und fertigt, und wir montieren vor Ort.'),
    ('Werkstatt und Druck im Haus', 'Studio und Partnerwerkstatt'),
    ('Eigenes Studio mit angeschlossener Werkstatt – hier wird gestaltet, gedruckt und aufgebaut.',
     'Im eigenen Studio wird gestaltet, gefertigt wird in unserer Partnerwerkstatt in Berlin.'),
    ('Zum Studio gehört eine eigene Werkstatt: Wir gestalten, drucken auf unseren eigenen Großformat-Druckern, schneiden am Plotter, fertigen Schilder und Folienarbeiten und montieren vor Ort.',
     'Wir gestalten im eigenen Studio, lassen Druck, Plott, Schilder und Folienarbeiten in unserer Partnerwerkstatt fertigen und montieren vor Ort.'),
    ('Entwurf, Druckdaten, Großformatdruck, Folienschnitt, Schilder und Montage laufen bei uns im Haus in Berlin-Wedding.',
     'Entwurf, Druckdaten und Montage machen wir selbst, Großformatdruck, Folienschnitt und Schilder fertigt unsere Partnerwerkstatt in Berlin.'),
    ('<h3>Werkstatt und Partnerbetrieb</h3><p>Schilder, Zuschnitte und Folienarbeiten entstehen in unserer eigenen Werkstatt.',
     '<h3>Partnerwerkstatt und Fachbetrieb</h3><p>Schilder, Zuschnitte und Folienarbeiten entstehen in unserer Partnerwerkstatt.'),
    ('Großformat läuft auf unseren eigenen Maschinen.', 'Großformat drucken wir mit unserer Partnerwerkstatt in Berlin.'),
    ('Erst den Druck. Dann den Plotter. Dann die Werkstatt, in der Buchstaben entstehen.', 'Erst den Druck. Dann den Plotter. Dann, wie Buchstaben entstehen.'),
    ('Was hier steht, können wir belegen – notfalls in der Werkstatt.', 'Was hier steht, können wir belegen.'),
    ('<h3>Druck im Haus</h3><p>Hochauflösender Großformatdruck auf eigenen Maschinen. Farbkontrolle passiert bei uns, nicht per E-Mail mit einem Zulieferer.</p>',
     '<h3>Druck in der Partnerwerkstatt</h3><p>Hochauflösender Großformatdruck in unserer Partnerwerkstatt in Berlin. Die Farben stimmen wir vor dem Druck mit Ihnen ab.</p>'),
    ('noch am selben Tag – auf eigenen Maschinen in Berlin-Wedding.', 'noch am selben Tag – mit unserer Partnerwerkstatt in Berlin.'),
    ('7 Tipps aus der Berliner Werkstatt', '7 Tipps aus der Praxis'),
    ('Eigene Werkstatt · Druck und Plott im Haus', 'Fertigung in der Partnerwerkstatt'),
    ('Eigene Werkstatt &amp; Druck im Haus', 'Studio &amp; Partnerwerkstatt in Berlin'),
    ('Eigene Werkstatt im Wedding', 'Studio im Wedding'),
    ('Eigene Werkstatt in Berlin-Wedding', 'Studio in Berlin-Wedding'),
    ('Eigene Werkstatt<', 'Partnerwerkstatt in Berlin<'),
    ('Druck und Plott im eigenen Haus', 'Druck und Plott in Berlin'),
    ('Druck und Plott im Haus', 'Druck und Plott in Berlin'),
    ('Messegrafik aus eigener Produktion', 'Messegrafik aus Berliner Produktion'),
    ('gestaltet und gedruckt im eigenen Haus', 'gestaltet von uns, gedruckt in Berlin'),
    ('Banner aus unserer Werkstatt', 'Banner aus Berlin'),
    ('Echte Projekte aus unserer Werkstatt', 'Echte Projekte aus unserer Arbeit'),
    ('Montage in unserer Werkstatt im Wedding', 'Montage in unserer Partnerwerkstatt in Berlin'),
    ('Unsere Werkstatt sitzt in Berlin-Wedding.', 'Unser Studio sitzt in Berlin-Wedding.'),
    ('Werkstatt in Berlin-Wedding – Aufmaß und Montage', 'Studio in Berlin-Wedding – Aufmaß und Montage'),
    ('✦ Werkstatt in Berlin-Wedding', '✦ Studio in Berlin-Wedding'),
    ('Montage aus einer Hand, Werkstatt in Berlin.', 'Montage aus einer Hand, Studio in Berlin.'),
    ('– Studio und Werkstatt, unser einziger Standort.', '– unser Studio und einziger Standort.'),
    ('aus unserer Werkstatt in Berlin-Wedding', 'aus Berlin'),
    ('aus unserer Werkstatt in Berlin', 'aus unseren Projekten in Berlin'),
    ('Live aus unserer Werkstatt', 'Live aus unserer Partnerwerkstatt'),
    ('aus unserer Werkstatt', 'aus unseren Projekten'),
    ('in unserer Werkstatt', 'in unserer Partnerwerkstatt'),
]
RX = [
    (r'([Ss]tudio) mit (?:eigener |angeschlossener )?Werkstatt', r'\1'),
    (r'([Ss]tudio) (&amp;|&|und) Werkstatt', r'\1'),
    (r'(Studio)(?: und|) Werkstatt im Wedding', r'\1 im Wedding'),
    (r'Produktion in Berlin-Wedding', 'Produktion in Berlin'),
]


def dateien():
    for d, ds, fs in os.walk(ROOT):
        rel = os.path.relpath(d, ROOT)
        if any(rel == o or rel.startswith(o + os.sep) for o in OHNE):
            ds[:] = []; continue
        for f in fs:
            if f.endswith(ENDUNG):
                p = os.path.join(d, f)
                if os.path.abspath(p) != SELBST: yield p


def main():
    dry = '--dry' in sys.argv; n = 0
    for p in dateien():
        try: s = open(p, encoding='utf-8').read()
        except UnicodeDecodeError: continue
        alt = s
        for a, b in R: s = s.replace(a, b)
        for a, b in RX: s = re.sub(a, b, s)
        if s != alt:
            n += 1; print(os.path.relpath(p, ROOT))
            if not dry: open(p, 'w', encoding='utf-8').write(s)
    print(n, 'Dateien angepasst' + (' (Probelauf)' if dry else ''))


if __name__ == '__main__':
    main()
