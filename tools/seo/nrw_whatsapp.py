"""WhatsApp auf allen Seiten auf die Firmennummer 0178 514 3918 setzen (Inhaber, 23.11.2026: „setz meine Nummer“).
Vom 28.10. bis 23.11.2026 führten die NRW-Seiten (data-region="nrw") zur Nummer des NRW-Teams (0178 2410682); der Inhaber sah diese
Anfragen dadurch nicht. Das Skript entfernt die NRW-Nummer überall, wo Generatoren oder alte Fassungen sie noch einsetzen. Idempotent.
Aufruf: python3 tools/seo/nrw_whatsapp.py
"""
import os, glob

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
ERSETZEN = [('wa.me/491782410682', 'wa.me/491785143918'), ('0178 2410682', '0178 514 3918'),
            ('Am einfachsten per WhatsApp an unser NRW-Team (', 'Am einfachsten per WhatsApp (')]


def main():
    n = 0
    for p in glob.glob(os.path.join(ROOT, '*.html')) + glob.glob(os.path.join(ROOT, 'blog', '*.html')):
        s = open(p, encoding='utf-8').read(); o = s
        if '2410682' not in s: continue
        for a, b in ERSETZEN: s = s.replace(a, b)
        if s != o: open(p, 'w', encoding='utf-8').write(s); n += 1
    print(n, 'Seiten auf die Firmennummer (WhatsApp) umgestellt')


if __name__ == '__main__':
    main()
