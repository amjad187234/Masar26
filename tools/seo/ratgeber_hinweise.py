"""Kurze Ratgeber-Hinweise (Marktrecherche 11/2026) auf passenden Leistungsseiten – vor dem Kontaktbereich.
Je Seite ein Kasten mit 1–3 Links. Marker ratgeber-hinweis, Block wird an Ort und Stelle erneuert. Idempotent.
Aufruf: python3 tools/seo/ratgeber_hinweise.py
"""
import os, re
ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))).rstrip('/')
A, Z = '<!-- ratgeber-hinweis -->', '<!-- /ratgeber-hinweis -->'
R = {
    'eroeffnung': ('/blog/ladeneroeffnung-werbung-checkliste.html', 'Ladeneröffnung: Werbe-Checkliste mit Fristen'),
    'miete': ('/blog/werbeschild-mietobjekt-vermieter.html', 'Werbeschild am gemieteten Laden'),
    'kosten': ('/blog/leuchtreklame-kosten-berlin.html', 'Was kostet Leuchtreklame? Preise & 7 Prüfpunkte'),
    'stopper': ('/blog/kundenstopper-erlaubnis.html', 'Kundenstopper: Erlaubnis in Berlin, Hamburg, NRW'),
    'fehler': ('/blog/werbung-teure-fehler.html', 'Teure Fehler in der Werbung'),
    'check': ('/genehmigungs-check.html', 'Kostenloser Genehmigungs-Check'),
    'leasing': ('/blog/leasingrueckgabe-fahrzeugbeschriftung-entfernen.html', 'Leasingrückgabe: Beschriftung richtig entfernen'),
    'google': ('/blog/google-unternehmensprofil-abzocke.html', 'Google-Profil: Abzocke-Anrufe erkennen'),
    'saison': ('/schaufenster-weihnachten-black-friday.html', 'Schaufenster für Black Friday & Weihnachten'),
    'schilder': ('/schilder-berlin.html', 'Schilder Berlin'),
    'schaufenster': ('/schaufensterbeschriftung-berlin.html', 'Schaufensterbeschriftung Berlin'),
    'praxis': ('/praxisbeschilderung-berlin.html', 'Praxisschilder'),
    'kanzlei': ('/kanzleischild-berlin.html', 'Kanzleischild'),
    'praxisregeln': ('/blog/praxisschild-regeln-kosten.html', 'Praxisschild: Regeln & Kosten'),
    'sichtschutz': ('/sichtschutzfolie-berlin.html', 'Sichtschutzfolie'),
    'ki_praxis': ('/ki-fuer-arztpraxen-berlin.html', 'KI für Arztpraxen'),
    'aussen_rat': ('/blog/aussenwerbung-berlin-ratgeber.html', 'Ratgeber Außenwerbung Berlin'),
    'glastuer': ('/blog/glastueren-kennzeichnen.html', 'Glastüren richtig kennzeichnen'),
    'fz_tipps': ('/blog/fahrzeugbeschriftung-tipps.html', 'Tipps zur Fahrzeugbeschriftung'),
    'fz_pflege': ('/blog/fahrzeugbeschriftung-pflegedienst.html', 'Fahrzeugbeschriftung für Pflegedienste'),
    'fotowand': ('/blog/fotowand-firmenfeier.html', 'Fotowand für die Firmenfeier'),
    'express': ('/express-druck-berlin.html', 'Express-Druck Berlin'),
    'banner': ('/pvc-banner-berlin.html', 'PVC-Banner Berlin'),
    'sf_tipps': ('/blog/schaufensterbeschriftung-tipps.html', 'Tipps zur Schaufensterbeschriftung'),
    'leucht': ('/leuchtreklame-berlin.html', 'Leuchtreklame Berlin'),
    'grafik': ('/grafikdesign-berlin.html', 'Grafikdesign Berlin'),
}
SEITEN = {
    'fahrzeugbeschriftung-berlin.html': ['leasing', 'fz_tipps', 'fz_pflege'],
    'fahrzeugbeschriftung-nrw.html': ['leasing'],
    'lkw-beschriftung-berlin.html': ['leasing'],
    'werbung-handwerker-berlin.html': ['leasing'],
    'werbeagentur-nrw.html': ['check'],
    'pvc-banner-berlin.html': ['check', 'saison', 'fotowand', 'express'],
    'schilder-berlin.html': ['check', 'eroeffnung', 'miete', 'stopper', 'praxis', 'kanzlei', 'praxisregeln'],
    'schaufensterbeschriftung-berlin.html': ['check', 'eroeffnung', 'stopper', 'sf_tipps'],
    'leuchtreklame-berlin.html': ['check', 'kosten', 'miete', 'schilder', 'aussen_rat'],
    'leuchtreklame-nrw.html': ['check', 'kosten', 'miete'],
    'aussenwerbung-berlin.html': ['check', 'miete', 'stopper', 'kosten'],
    'print.html': ['stopper', 'fehler', 'banner'],
    'grafikdesign-berlin.html': ['fehler'],
    'webdesign-berlin.html': ['google', 'fehler'],
    'digital.html': ['google', 'fehler'],
    'werbeagentur-hamburg.html': ['check', 'stopper', 'saison'],
    'werbetechnik.html': ['schilder', 'schaufenster', 'check'],
    'praxisbeschilderung-berlin.html': ['sichtschutz', 'kanzlei', 'ki_praxis'],
    'kanzleischild-berlin.html': ['praxis'],
    'sichtschutzfolie-berlin.html': ['glastuer'],
    'foliendruck-berlin.html': ['saison'],
    'schaufensterbeschriftung-nrw.html': ['saison'],
    'blog/glastueren-kennzeichnen.html': ['sichtschutz'],
    'blog/schaufensterbeschriftung-tipps.html': ['saison'],
    'blog/ladeneroeffnung-werbung-checkliste.html': ['saison', 'leucht', 'banner', 'check', 'grafik'],
    'blog/leuchtreklame-kosten-berlin.html': ['check', 'schilder'],
}


def box(keys):
    links = ' · '.join(f'<a href="{R[k][0]}" style="color:#177567;font-weight:700">{R[k][1]}</a>' for k in keys)
    return (f'{A}\n<div class="ratgeber-hinweis" style="max-width:1100px;margin:2rem auto;padding:0 16px;box-sizing:border-box">'
            f'<p style="margin:0;background:#fff;border:1px solid #e0eaea;border-radius:10px;padding:.9rem 1.2rem;font-size:15px;line-height:1.7;color:#1a2a2a">'
            f'<strong>Gut zu wissen:</strong> {links}</p></div>\n{Z}\n')


def main():
    n = 0
    for f, keys in SEITEN.items():
        p = os.path.join(ROOT, f)
        if not os.path.exists(p): continue
        s = open(p, encoding='utf-8').read(); alt = s; b = box(keys)
        s, k = re.subn(re.escape(A) + r'.*?' + re.escape(Z) + r'\n', lambda m: b, s, count=1, flags=re.S)
        if not k:
            m = re.search(r'<(section|div)[^>]*id="kontakt"', s) or re.search(r'<div class="sources">', s)
            if m: i = m.start()
            else:  # Ratgeber ohne Quellen: vor dem Block „Weitere Artikel“
                w = s.find('Weitere Artikel')
                i = max(s.rfind('<div', 0, w), s.rfind('<section', 0, w)) if w > 0 else -1
                if i < 0: print('kein Ziel:', f); continue
                i = s.rfind('\n', 0, i) + 1
            s = s[:i] + b + s[i:]
        if s != alt: open(p, 'w', encoding='utf-8').write(s); n += 1
    print(n, 'Seiten mit Ratgeber-Hinweis')


if __name__ == '__main__':
    main()
