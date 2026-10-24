"""Lokale Inhalte für die NRW-Städte-Leistungsseiten (gegen fast identische Seiten / Doorway-Risiko).

Fügt vor dem Kontaktbereich einen Abschnitt „<Leistung> in <Stadt>: was vor Ort gilt“ ein – mit den belegten
lokalen Regeln aus tools/blog/stadt_ratgeber.py (Satzungen, Zuständigkeit) und den Stadtteilen.
Idempotent über Marker-Kommentare; nach dem Neu-Erzeugen der Seiten erneut ausführen:
    python3 tools/seo/stadt_lokal.py
"""
import os, re, importlib.util

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
spec = importlib.util.spec_from_file_location('sr', os.path.join(ROOT, 'tools', 'blog', 'stadt_ratgeber.py'))
SR = importlib.util.module_from_spec(spec); spec.loader.exec_module(SR)
STADT = {c['slug']: c for c in SR.STAEDTE}

TEILE = {
    'koeln': ('Innenstadt, Altstadt, Ehrenfeld und Nippes', 'Leverkusen und Bergisch Gladbach'),
    'duesseldorf': ('Stadtmitte, Altstadt, Pempelfort und Bilk', 'Neuss und Ratingen'),
    'dortmund': ('Innenstadt, Hörde, Aplerbeck und Brackel', 'Bochum und Unna'),
    'essen': ('Stadtkern, Rüttenscheid, Holsterhausen und Frohnhausen', 'Mülheim an der Ruhr und Gelsenkirchen'),
    'bochum': ('Innenstadt, Ehrenfeld, Weitmar und Linden', 'Herne und Witten'),
}
LEISTUNG = {
    'schilder': ('Schilder', 'Firmen- und Praxisschilder'),
    'leuchtreklame': ('Leuchtreklame', 'Leuchtbuchstaben und Leuchtkästen'),
    'schaufensterbeschriftung': ('Schaufensterbeschriftung', 'Werbung am Schaufenster'),
    'werbeagentur': ('Werbeanlagen', 'Schilder, Leuchtreklame und Beschriftung'),
    'fensterfolie': ('Fensterfolie', 'Sonnen-, Sicht- und Splitterschutz'),
}
A, Z = '<!-- lokal:start -->', '<!-- lokal:ende -->'


def abschnitt(svc, slug):
    c = STADT[slug]; s = c['stadt']; titel, art = LEISTUNG[svc]; teile, umland = TEILE[slug]
    absaetze = ''.join(f'<p style="margin-top:.8rem">{p}</p>' for p in c['lokal'][:2])
    if svc == 'fensterfolie':
        inhalt = (f'<p>Unser Team in NRW montiert Fensterfolien in ganz {s} – zum Beispiel in {teile} – und im Umland wie {umland}. '
                  'Vor der Montage prüfen wir das Glas (Art, Größe, Sonneneinstrahlung), denn nicht jede Folie passt zu jeder Scheibe.</p>'
                  f'<p style="margin-top:.8rem">Gut zu wissen: Soll die Folie zusätzlich Ihr Logo oder Werbung zeigen, kann sie als Werbeanlage gelten. '
                  f'Was dafür in {s} vor Ort gilt, steht in unserem Ratgeber.</p>')
    else:
        tipps = ''.join(f'<li style="margin-bottom:.4rem">{t}</li>' for t in c['tipps'])
        faq = ''.join(f'<p style="margin-top:.8rem"><strong style="color:var(--navy,#132e50)">{q}</strong><br>{a}</p>' for q, a in c['faq'])
        inhalt = (f'<p>{c["kurz"]}</p>{absaetze}'
                  f'<h3 style="margin-top:1.4rem;color:var(--navy,#132e50);font-size:1.15rem">Unsere Tipps für {s}</h3><ul style="margin:.6rem 0 0 1.2rem">{tipps}</ul>'
                  f'<h3 style="margin-top:1.4rem;color:var(--navy,#132e50);font-size:1.15rem">Häufige Fragen aus {s}</h3>{faq}')
    return (f'{A}\n<section class="section" id="vor-ort" style="padding:3rem 0;background:var(--off,#f4f7f7)">\n  <div class="container">\n'
            f'    <div class="sec-head reveal" style="margin-bottom:1.2rem;"><span class="eyebrow">Vor Ort in {s}</span>'
            f'<h2 class="sec-title" style="font-size:clamp(1.5rem,3vw,2.2rem);">{titel} in {s}: <em>was vor Ort gilt</em></h2></div>\n'
            f'    <div class="reveal" style="max-width:820px;margin:0 auto;font-size:16px;line-height:1.8;color:var(--muted,#5a7070)">{inhalt}'
            f'<p style="margin-top:1rem"><strong style="color:var(--navy,#132e50)">Einsatzgebiet:</strong> {teile} sowie {umland}. '
            f'<a href="/blog/werbeanlage-{slug}.html" style="color:var(--teal-ink,#177567);font-weight:700">Ratgeber: Werbeanlage in {s} →</a></p></div>\n'
            f'  </div>\n</section>\n{Z}\n')


def main():
    n = 0
    for svc in LEISTUNG:
        for slug in TEILE:
            f = os.path.join(ROOT, f'{svc}-{slug}.html')
            if not os.path.exists(f): continue
            s = open(f, encoding='utf-8').read()
            s = re.sub(re.escape(A) + r'.*?' + re.escape(Z) + r'\n?', '', s, flags=re.S)
            for anker in ['<!-- CONTACT -->', '<section class="section" id="kontakt">', '<div class="cta-strip" id="kontakt">']:
                if anker in s:
                    i = s.index(anker); s = s[:i] + abschnitt(svc, slug) + s[i:]; break
            else:
                print('kein Anker:', f); continue
            open(f, 'w', encoding='utf-8').write(s); n += 1
    print(n, 'Seiten mit lokalem Abschnitt')


if __name__ == '__main__':
    main()
