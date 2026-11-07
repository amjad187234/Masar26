"""Bewertungskarte 85 × 55 mm (Vorder- + Rückseite) mit QR-Code zu /bewerten.html – zum Beilegen bei jeder Lieferung/Montage.
Vorderseite: Bitte um Bewertung + QR. Rückseite: Kontakt + Claim. Keine Anreize für Bewertungen (Google-Richtlinie, UWG).
Aufruf: python3 tools/brand/bewertungskarte.py → tools/brand/Masar_Bewertungskarte.pdf (2 Seiten, 3 mm Beschnitt)
"""
import os, subprocess
HIER = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HIER, '..', '..'))
F = 'file://' + ROOT + '/fonts/'
qr = open(os.path.join(HIER, 'qr-bewerten.svg'), encoding='utf-8').read()
qr = qr[qr.index('<svg'):]
html = f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><style>
@font-face{{font-family:BC;src:url({F}barlow-condensed-black.woff2)}}
@font-face{{font-family:B;src:url({F}barlow-regular.woff2)}}
@font-face{{font-family:BS;src:url({F}barlow-semibold.woff2)}}
@page{{size:91mm 61mm;margin:0}}
*{{margin:0;padding:0;box-sizing:border-box}}
.s{{width:91mm;height:61mm;padding:3mm;page-break-after:always;overflow:hidden}}
.i{{width:85mm;height:55mm;padding:5mm 5.5mm;position:relative}}
.v{{background:#132e50;color:#fff}}
.v .i{{display:grid;grid-template-columns:1fr 25mm;gap:4mm;align-items:center}}
h1{{font-family:BC;font-size:17pt;line-height:.95;text-transform:uppercase;letter-spacing:.2px}}
h1 em{{color:#58d0bd;font-style:normal}}
.v p{{font-family:B;font-size:7.4pt;line-height:1.4;margin-top:2.2mm;color:rgba(255,255,255,.85)}}
.stars{{color:#58d0bd;font-size:10pt;letter-spacing:1px;margin-top:2mm}}
.qr{{background:#fff;padding:2mm;border-radius:1.5mm}}.qr svg{{width:100%;height:auto;display:block}}
.qr small{{display:block;text-align:center;font-family:BS;font-size:5.4pt;color:#132e50;margin-top:1mm}}
.r{{background:#f4f7f7;color:#1a2a2a}}
.r .brand{{font-family:BC;font-size:20pt;color:#132e50;letter-spacing:1px}}.r .sub{{font-family:BS;font-size:6pt;letter-spacing:1.6px;color:#177567}}
.r .k{{font-family:B;font-size:7.6pt;line-height:1.55;margin-top:3mm}}
.r .claim{{position:absolute;left:5.5mm;bottom:5mm;font-family:BC;font-size:10pt;text-transform:uppercase;color:#177567}}
.r .bar{{position:absolute;left:-3mm;right:-3mm;bottom:-3mm;height:5mm;background:#58d0bd}}
</style></head><body>
<div class="s v"><div class="i"><div>
<h1>Zufrieden mit<br>unserer <em>Arbeit?</em></h1>
<div class="stars">★★★★★</div>
<p>Eine kurze Google-Bewertung hilft uns sehr – und anderen bei der Entscheidung. Dauert eine Minute.</p>
</div><div class="qr">{qr}<small>Code scannen</small></div></div></div>
<div class="s r"><div class="i">
<div class="brand">MASAR</div><div class="sub">WERBEAGENTUR BERLIN</div>
<div class="k">Bristolstraße 19E · 13349 Berlin<br>Tel./WhatsApp 0178 514 3918<br>info@masar-werbeagentur.de · masar-werbeagentur.de</div>
<div class="claim">Werbung, die man sieht.</div><div class="bar"></div>
</div></div>
</body></html>'''
f = os.path.join(HIER, 'bewertungskarte.html')
open(f, 'w', encoding='utf-8').write(html)
subprocess.run(['node', os.path.join(ROOT, 'tools', 'angebot', 'pdf.mjs'), f, os.path.join(HIER, 'Masar_Bewertungskarte.pdf')], check=True)
os.remove(f)
print('tools/brand/Masar_Bewertungskarte.pdf')
