"""Vorschaubilder (1200×630) für Social Media / WhatsApp und passende Meta-Tags.

Neue Seite:
  python3 tools/og/og_cards.py add <seite.html> <bild.webp|grafik.html|-> "<Kategorie>" "<Überschrift>" "<Unterzeile>"
  → erzeugt og/<seite>.jpg (Playwright/Chromium) und setzt og:image, og:image:alt und twitter:image.
Nur Meta-Tags neu setzen (Bild existiert schon):
  python3 tools/og/og_cards.py meta <seite.html> "<Überschrift>"
Neu erzeugte Seiten (Generatoren in tools/folien) haben zuerst logo.png als og:image –
danach für jede betroffene Seite „meta“ (oder „add“ bei neuen Seiten) ausführen.
Einträge werden in tools/og/cards.json gesammelt.
"""
import json, os, re, sys, html, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(HERE, '..', '..'))).rstrip('/') + '/'
BASE = 'https://masar-werbeagentur.de'
REG = os.path.join(HERE, 'cards.json')

TPL = '''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:B;font-weight:400;src:url(file://{ROOT}fonts/barlow-regular.woff2)}
@font-face{font-family:B;font-weight:600;src:url(file://{ROOT}fonts/barlow-semibold.woff2)}
@font-face{font-family:BC;font-weight:900;src:url(file://{ROOT}fonts/barlow-condensed-black.woff2)}
@font-face{font-family:Barlow;font-weight:400;src:url(file://{ROOT}fonts/barlow-regular.woff2)}
@font-face{font-family:Barlow;font-weight:600 800;src:url(file://{ROOT}fonts/barlow-semibold.woff2)}
@font-face{font-family:"Barlow Condensed";font-weight:900;src:url(file://{ROOT}fonts/barlow-condensed-black.woff2)}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1200px;height:630px;overflow:hidden;background:#132e50;font-family:B,sans-serif;color:#fff;position:relative}
.bg{position:absolute;inset:0;background:radial-gradient(ellipse 70% 90% at 0% 100%,rgba(88,208,189,.22),transparent 60%),linear-gradient(160deg,#16365e,#0e2340)}
.l{position:absolute;left:64px;top:56px;bottom:56px;width:{LW}px;display:flex;flex-direction:column}
.logo{display:flex;align-items:center;gap:16px}.logo img{height:64px;background:#fff;border-radius:14px;padding:6px 10px}
.logo span{font:600 18px B;letter-spacing:5px;color:rgba(255,255,255,.85)}
.ey{margin-top:auto;font:600 20px B;letter-spacing:4px;text-transform:uppercase;color:#58d0bd}
h1{font:900 {HS}px/.95 BC,sans-serif;text-transform:uppercase;margin-top:14px}
.sub{font:400 27px/1.3 B;color:rgba(255,255,255,.88);margin-top:18px}
.url{margin-top:auto;font:600 20px B;color:rgba(255,255,255,.7);display:flex;align-items:center;gap:12px}
.url i{display:inline-block;width:28px;height:4px;background:#58d0bd;border-radius:2px}
.r{position:absolute;right:0;top:0;width:504px;height:630px;overflow:hidden}
.r img{width:100%;height:100%;object-fit:cover}
.r:before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,#132e50 0,rgba(19,46,80,0) 60px);z-index:1}
.r.v{display:flex;align-items:center;justify-content:center;padding:0 34px 0 0}.r.v:before{display:none}.r.v .tv{width:440px}
</style></head><body><div class="bg"></div>
{RIGHT}
<div class="l"><div class="logo"><img src="file://{ROOT}logo.webp"><span>MASAR WERBEAGENTUR</span></div>
<div class="ey">{EY}</div><h1>{H}</h1><div class="sub">{SUB}</div>
<div class="url"><i></i>masar-werbeagentur.de</div></div></body></html>'''


def og_name(f):
    return 'og/' + f.replace('/index.html', '').replace('.html', '').replace('/', '-') + '.jpg'


def render(f, img, ey, h, sub):
    if img and img.endswith('.html'):   # gestaltete Grafik statt Foto (z. B. tools/og/visuals/termin.html)
        right = '<div class="r v">' + open(os.path.join(HERE, '..', '..', img) if not os.path.isabs(img) else img, encoding='utf-8').read() + '</div>'
    else:
        right = f'<div class="r"><img src="file://{ROOT}{img}"></div>' if img else ''
    lw = 600 if img else 1070
    hs = 78 if len(h) <= 22 else (66 if len(h) <= 30 else 56)
    if not img:
        hs = 96
    page = (TPL.replace('{ROOT}', ROOT).replace('{LW}', str(lw)).replace('{HS}', str(hs)).replace('{RIGHT}', right)
            .replace('{EY}', html.escape(ey)).replace('{H}', html.escape(h)).replace('{SUB}', html.escape(sub)))
    jobs = os.path.join(HERE, 'jobs.json')
    json.dump([{'out': ROOT + og_name(f), 'html': page}], open(jobs, 'w', encoding='utf-8'))
    try:
        subprocess.run(['node', os.path.join(HERE, 'render.mjs'), jobs], check=True)
    finally:
        os.remove(jobs)


def meta(f, h):
    p = ROOT + f
    s = open(p, encoding='utf-8').read()
    url = BASE + '/' + og_name(f)
    alt = html.escape(h + ' – Masar Werbeagentur')
    block = (f'<meta property="og:image" content="{url}">\n<meta property="og:image:width" content="1200">\n'
             f'<meta property="og:image:height" content="630">\n<meta property="og:image:type" content="image/jpeg">\n'
             f'<meta property="og:image:alt" content="{alt}">\n')
    s = re.sub(r'<meta property="og:image[^>]*>\n?', '', s)
    if '<meta property="og:locale"' in s:
        s = s.replace('<meta property="og:locale"', block + '<meta property="og:locale"', 1)
    else:
        s = s.replace('</head>', block + '</head>', 1)
    s = re.sub(r'<meta name="twitter:image" content="[^"]*">', f'<meta name="twitter:image" content="{url}">', s)
    open(p, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) == 6 and a[0] == 'add':
        f, img, ey, h, sub = a[1], (None if a[2] == '-' else a[2]), a[3], a[4], a[5]
        render(f, img, ey, h, sub)
        meta(f, h)
        reg = json.load(open(REG, encoding='utf-8')) if os.path.exists(REG) else {}
        reg[f] = [img, ey, h, sub]
        json.dump(reg, open(REG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('ok', og_name(f))
    elif len(a) == 3 and a[0] == 'meta':
        meta(a[1], a[2])
        print('ok')
    else:
        print(__doc__)
