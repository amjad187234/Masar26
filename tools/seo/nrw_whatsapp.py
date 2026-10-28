"""WhatsApp-Links auf NRW-Seiten (data-region="nrw") auf die Nummer des NRW-Teams umstellen.
Telefon/Impressum/JSON-LD bleiben bei der Firmennummer (Standort Berlin). Idempotent.
Aufruf: python3 tools/seo/nrw_whatsapp.py  (nach dem Neu-Erzeugen von NRW-Seiten ausführen)
"""
import os, glob

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
FIRMA, NRW = 'wa.me/491785143918', 'wa.me/491782410682'


def main():
    n = 0
    for p in glob.glob(os.path.join(ROOT, '*.html')):
        s = open(p, encoding='utf-8').read()
        if 'data-region="nrw"' not in s or FIRMA not in s: continue
        open(p, 'w', encoding='utf-8').write(s.replace(FIRMA, NRW)); n += 1
    print(n, 'NRW-Seiten auf WhatsApp NRW-Team umgestellt')


if __name__ == '__main__':
    main()
