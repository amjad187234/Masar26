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
    'google': ('/blog/google-unternehmensprofil-abzocke.html', 'Google-Profil: Abzocke-Anrufe erkennen'),
}
SEITEN = {
    'schilder-berlin.html': ['eroeffnung', 'miete', 'stopper'],
    'schaufensterbeschriftung-berlin.html': ['eroeffnung', 'stopper'],
    'leuchtreklame-berlin.html': ['kosten', 'miete'],
    'leuchtreklame-nrw.html': ['kosten', 'miete'],
    'aussenwerbung-berlin.html': ['miete', 'stopper', 'kosten'],
    'print.html': ['stopper', 'fehler'],
    'grafikdesign-berlin.html': ['fehler'],
    'webdesign-berlin.html': ['google', 'fehler'],
    'digital.html': ['google', 'fehler'],
    'werbeagentur-hamburg.html': ['stopper'],
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
            m = re.search(r'<(section|div)[^>]*id="kontakt"', s)
            if not m: print('kein Ziel:', f); continue
            s = s[:m.start()] + b + s[m.start():]
        if s != alt: open(p, 'w', encoding='utf-8').write(s); n += 1
    print(n, 'Seiten mit Ratgeber-Hinweis')


if __name__ == '__main__':
    main()
