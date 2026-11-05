"""Kostenloser Druckdaten-Check (druckdaten-check.html) – Generator auf Basis von gen_folien.build_f.
Werkzeug: /druckcheck.js (Prüfung im Browser, pdf.js selbst gehostet unter /js/pdfjs/). Keine Übertragung der Datei.
Richtwerte (ppi, Beschnitt, Sicherheitsabstand) stehen in druckcheck.js (TYP) und in der Tabelle unten – beide gleich halten.
Aufruf: python3 tools/folien/druckcheck_page.py
"""
import os, re, json
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'gen_folien.py'), encoding='utf-8').read()
exec(src[:src.index("\nif __name__")])

WERKZEUG = '''    <div class="dc" id="druckcheck">
      <div class="dc-form">
        <div class="dc-row">
          <div class="dc-f">
            <label for="dc-prod">1. Was soll gedruckt werden?</label>
            <select id="dc-prod">
              <option value="vk">Visitenkarte 85 × 55 mm</option>
              <option value="a6">Flyer / Postkarte DIN A6</option>
              <option value="dl">Flyer DIN lang</option>
              <option value="a5" selected>Flyer DIN A5</option>
              <option value="a4">Flyer / Briefpapier DIN A4</option>
              <option value="a3">Plakat DIN A3</option>
              <option value="a2">Plakat DIN A2</option>
              <option value="a1">Plakat DIN A1</option>
              <option value="a0">Plakat DIN A0</option>
              <option value="rollup">Roll-up 85 × 200 cm</option>
              <option value="eigen">Eigene Größe (Banner, Folie, Schild …)</option>
            </select>
          </div>
          <div class="dc-f dc-f-s">
            <label for="dc-bleed">Beschnitt je Seite (mm)</label>
            <input id="dc-bleed" type="number" min="0" max="100" step="0.5" value="3" inputmode="decimal">
          </div>
        </div>
        <div class="dc-row" id="dc-custom" hidden>
          <div class="dc-f dc-f-s"><label for="dc-w">Breite (cm)</label><input id="dc-w" type="number" min="1" step="0.1" value="300" inputmode="decimal"></div>
          <div class="dc-f dc-f-s"><label for="dc-h">Höhe (cm)</label><input id="dc-h" type="number" min="1" step="0.1" value="100" inputmode="decimal"></div>
          <div class="dc-f">
            <label for="dc-typ">Art</label>
            <select id="dc-typ">
              <option value="banner">Banner &amp; Großformat</option>
              <option value="plakat">Plakat &amp; Roll-up</option>
              <option value="folie">Folie, Schaufenster &amp; Fahrzeug</option>
              <option value="papier">Papier (Flyer, Karten)</option>
            </select>
          </div>
        </div>
        <p class="dc-hint" id="dc-hint"></p>
        <label class="dc-drop" for="dc-file">
          <input id="dc-file" type="file" accept=".pdf,application/pdf,image/jpeg,image/png,image/webp">
          <span class="dc-drop-ic" aria-hidden="true"><svg viewBox="0 0 24 24" width="34" height="34" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8Z"/><path d="M14 3v5h5"/><path d="M12 18v-6"/><path d="m9 14.5 3-3 3 3"/></svg></span>
          <strong>2. Datei hier ablegen oder auswählen</strong>
          <span>PDF, JPG oder PNG · bis 200 MB</span>
        </label>
        <p class="dc-priv"><svg class="i-inline" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>Ihre Datei bleibt auf Ihrem Gerät: Die Prüfung läuft komplett in Ihrem Browser, nichts wird hochgeladen oder gespeichert.</p>
        <noscript><p class="dc-priv">Für den Check wird JavaScript benötigt. Schicken Sie uns die Datei alternativ über das Formular unten – wir prüfen sie kostenlos.</p></noscript>
      </div>
      <div id="dc-out" aria-live="polite"></div>
    </div>
    <div class="dc-calc" id="dc-rechner">
      <h3>Pixel-Rechner: Wie groß kann ich mein Bild drucken?</h3>
      <div class="dc-calc-grid">
        <fieldset>
          <legend>Pixel → Druckgröße</legend>
          <div class="dc-row"><div class="dc-f dc-f-s"><label for="rc-pw">Breite (px)</label><input id="rc-pw" type="number" min="1" value="3000" inputmode="numeric"></div>
          <div class="dc-f dc-f-s"><label for="rc-ph">Höhe (px)</label><input id="rc-ph" type="number" min="1" value="2000" inputmode="numeric"></div>
          <div class="dc-f dc-f-s"><label for="rc-dpi">Auflösung (ppi)</label><input id="rc-dpi" type="number" min="1" value="300" inputmode="numeric"></div></div>
          <output id="rc-out1" for="rc-pw rc-ph rc-dpi">–</output>
        </fieldset>
        <fieldset>
          <legend>Druckgröße → benötigte Pixel</legend>
          <div class="dc-row"><div class="dc-f dc-f-s"><label for="rc-cw">Breite (cm)</label><input id="rc-cw" type="number" min="0.1" step="0.1" value="21" inputmode="decimal"></div>
          <div class="dc-f dc-f-s"><label for="rc-ch">Höhe (cm)</label><input id="rc-ch" type="number" min="0.1" step="0.1" value="29.7" inputmode="decimal"></div>
          <div class="dc-f dc-f-s"><label for="rc-dpi2">Auflösung (ppi)</label><input id="rc-dpi2" type="number" min="1" value="300" inputmode="numeric"></div></div>
          <output id="rc-out2" for="rc-cw rc-ch rc-dpi2">–</output>
        </fieldset>
      </div>
    </div>'''

CSS = '''<style id="druckcheck-css">
.dc{display:grid;grid-template-columns:minmax(0,1fr);gap:1.5rem;max-width:920px;margin:0 auto}
.dc-form{background:#fff;border:1px solid var(--border);border-radius:16px;padding:1.5rem;box-shadow:0 10px 30px rgba(19,46,80,.06)}
.dc-row{display:flex;flex-wrap:wrap;gap:1rem;margin-bottom:1rem}
.dc-row[hidden]{display:none}
.dc-f{flex:1 1 260px;display:flex;flex-direction:column;gap:.35rem;min-width:0}
.dc-f-s{flex:1 1 130px}
.dc-f label,.dc-calc legend{font-weight:700;color:var(--navy);font-size:15px}
.dc-f select,.dc-f input{font:inherit;font-size:16px;padding:.7rem .8rem;border:1px solid #b9c7c7;border-radius:10px;background:#fff;color:var(--text);width:100%;min-height:48px}
.dc-hint{font-size:14px;color:var(--muted);margin:-.3rem 0 1rem}
.dc-drop{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.35rem;text-align:center;border:2px dashed var(--teal);border-radius:14px;background:var(--off);padding:2rem 1rem;cursor:pointer;transition:background .15s,border-color .15s}
.dc-drop:hover,.dc-drop.on{background:#e6f7f4;border-color:var(--teal-ink)}
.dc-drop input{position:absolute;inset:0;opacity:0;cursor:pointer;width:100%;height:100%}
.dc-drop:focus-within{outline:3px solid var(--navy);outline-offset:3px}
.dc-drop strong{font-size:1.15rem;color:var(--navy)}
.dc-drop span{font-size:14px;color:var(--muted)}
.dc-drop-ic{color:var(--teal-ink)}
.dc-priv{font-size:14px;color:var(--muted);margin-top:.9rem;display:flex;gap:.5rem;align-items:flex-start}
.dc-priv svg{flex:none;margin-top:.15rem;stroke:var(--teal-ink)}
.dc-busy{display:flex;align-items:center;gap:.8rem;padding:1.2rem;font-weight:700;color:var(--navy)}
.dc-busy-b{flex:1;min-width:0;display:flex;flex-direction:column;gap:.5rem}
.dc-prog{width:100%;max-width:420px;height:10px;accent-color:#177567}
.dc-spin{width:26px;height:26px;border-radius:50%;border:3px solid var(--border);border-top-color:var(--teal-ink);animation:dcs 0.8s linear infinite}
@keyframes dcs{to{transform:rotate(360deg)}}
@media (prefers-reduced-motion:reduce){.dc-spin{animation:none}}
.dc-verdict{display:flex;gap:1rem;align-items:flex-start;border-radius:14px;padding:1.2rem 1.3rem;margin-bottom:1rem;border:1px solid}
.dc-verdict strong{display:block;font-size:1.3rem;color:var(--navy);font-family:'Barlow Condensed',sans-serif;text-transform:uppercase;letter-spacing:.3px}
.dc-verdict p{margin:.2rem 0 .3rem}
.dc-count{display:flex;flex-wrap:wrap;gap:.4rem;margin:.1rem 0 .5rem}
.dc-c{font-size:13px;font-weight:700;padding:.1rem .6rem;border-radius:20px;background:#fff;border:1px solid var(--border)}
.dc-c.dc-ok{color:#177567}.dc-c.dc-warn{color:#8a5100}.dc-c.dc-bad{color:#b3261e}
.dc-verdict small{color:var(--muted);font-size:13px;overflow-wrap:anywhere}
.dc-verdict:focus{outline:3px solid var(--navy);outline-offset:3px}
.dc-ic{flex:none;width:34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;color:#fff;font-size:17px}
.dc-ok .dc-ic{background:#177567}.dc-warn .dc-ic{background:#9a5b00}.dc-bad .dc-ic{background:#b3261e}.dc-info .dc-ic{background:#132e50}
.dc-verdict.dc-ok{background:#e9f7f4;border-color:#9ed9cd}.dc-verdict.dc-warn{background:#fff6e5;border-color:#f0cf8f}.dc-verdict.dc-bad{background:#fdeceb;border-color:#f0b4ae}
.dc-list{list-style:none;margin:0;padding:0;display:grid;gap:.6rem}
.dc-list li{display:flex;gap:.9rem;align-items:flex-start;background:#fff;border:1px solid var(--border);border-radius:12px;padding:.9rem 1rem}
.dc-list .dc-ic{width:28px;height:28px;font-size:14px}
.dc-list strong{color:var(--navy);display:flex;flex-wrap:wrap;gap:.5rem;align-items:center}
.dc-list p{margin:.2rem 0 0;font-size:15px;color:var(--text);overflow-wrap:anywhere}
.dc-tag{font-size:12px;font-weight:700;padding:.1rem .5rem;border-radius:20px;background:var(--off);color:var(--muted);text-transform:uppercase;letter-spacing:.4px}
.dc-ok .dc-tag{color:#177567}.dc-warn .dc-tag{color:#8a5100}.dc-bad .dc-tag{color:#b3261e}
.dc-h3{margin:1.6rem 0 .4rem;color:var(--navy)}
.dc-legend{font-size:13.5px;color:var(--muted);display:flex;flex-wrap:wrap;gap:.3rem .9rem;align-items:center;margin-bottom:.8rem}
.dc-li{display:inline-flex;align-items:center;gap:.4rem;white-space:nowrap}
.dc-legend i{display:inline-block;width:22px;height:0;border-top:3px dashed}
.dc-legend .dc-l1{border-color:#d63b3b}.dc-legend .dc-l2{border-color:#177567}.dc-legend .dc-l3{border:0;height:12px;background:rgba(19,46,80,.28)}
.dc-legend .dc-m{width:16px;height:12px;border:2px solid}
.dc-legend .dc-m-edge{border-color:#d63b3b;background:rgba(214,59,59,.18)}.dc-legend .dc-m-hair{border-color:#c25e00;background:rgba(194,94,0,.16)}
.dc-legend .dc-m-small{border-color:#132e50;background:rgba(19,46,80,.14)}.dc-legend .dc-m-img{border:3px dashed #b3261e}
.dc-thumbs{display:flex;flex-wrap:wrap;gap:1rem}
.dc-thumb{margin:0;max-width:100%;padding:0;border:0;background:none;font:inherit;text-align:left;cursor:zoom-in;border-radius:8px}
.dc-thumb canvas{display:block;max-width:100%;height:auto;border:1px solid var(--border);border-radius:6px;box-shadow:0 8px 24px rgba(19,46,80,.12);background:#fff;transition:box-shadow .15s}
.dc-thumb:hover canvas{box-shadow:0 10px 30px rgba(19,46,80,.28)}
.dc-thumb:focus-visible{outline:3px solid var(--navy);outline-offset:4px}
.dc-cap{display:block;font-size:13px;color:var(--muted);margin-top:.4rem}
.dc-imgs{margin-top:1rem;background:#fff;border:1px solid var(--border);border-radius:12px;padding:0 1rem .4rem}
.dc-imgs summary{cursor:pointer;font-weight:700;color:var(--navy);padding:.8rem 0;min-height:44px}
.dc-imgs summary:focus-visible{outline:3px solid var(--navy);outline-offset:2px}
.dc-tw{overflow-x:auto;max-width:100%}
.dc-tw:focus-visible{outline:3px solid var(--navy);outline-offset:2px}
.dc-tab{width:100%;border-collapse:collapse;font-size:14px}
.dc-tab th,.dc-tab td{padding:.45rem .6rem;border-bottom:1px solid var(--border);text-align:left;white-space:nowrap}
.dc-tab th{color:var(--navy);background:var(--off)}
.dc-st{font-weight:700}.dc-st.dc-ok{color:#177567}.dc-st.dc-warn{color:#8a5100}.dc-st.dc-bad{color:#b3261e}
.dc-actions{display:flex;flex-wrap:wrap;gap:.7rem;margin-top:1.4rem}
.dc-actions .btn{flex:1 1 240px;justify-content:center;text-align:center}
.dc-btn2{background:var(--navy);color:#fff;border:2px solid var(--navy)}
.dc-print,.dc-again{flex:1 1 180px;font:inherit;font-weight:700;padding:.85rem 1rem;border-radius:10px;border:2px solid var(--border);background:#fff;color:var(--navy);cursor:pointer;min-height:48px}
.dc-small{font-size:13.5px;color:var(--muted);margin-top:.8rem}
.dc-calc{max-width:920px;margin:2rem auto 0;background:var(--off);border:1px solid var(--border);border-radius:16px;padding:1.5rem}
.dc-calc h3{color:var(--navy);margin:0 0 1rem}
.dc-calc-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1rem}
.dc-calc fieldset{border:1px solid var(--border);border-radius:12px;padding:1rem;background:#fff;min-width:0}
.dc-calc legend{padding:0 .4rem}
.dc-calc .dc-row{margin-bottom:.6rem;gap:.6rem}
.dc-calc .dc-f-s{flex:1 1 90px}
.dc-calc output{display:block;font-weight:800;color:var(--teal-ink);font-size:1.1rem}
@media(max-width:600px){.dc-form,.dc-calc{padding:1rem}.dc-drop{padding:1.5rem .8rem}}
html.dc-lb-open{overflow:hidden}
.dc-lb{width:100vw;height:100vh;height:100dvh;max-width:none;max-height:none;margin:0;padding:0;border:0;background:#0e2340;color:#fff;flex-direction:column}
.dc-lb[open]{display:flex}
.dc-lb::backdrop{background:rgba(14,35,64,.85)}
.dc-lb-bar{display:flex;flex-wrap:wrap;align-items:center;gap:.5rem;padding:.6rem .8rem;background:#132e50}
.dc-lb .dc-lb-t{flex:1 1 220px;margin:0;font:700 16px/1.3 Barlow,sans-serif;color:#fff;text-transform:none;letter-spacing:0;min-width:0}
.dc-lb-grp{display:flex;align-items:center;gap:.3rem}
.dc-lb-grp[hidden]{display:none}
.dc-lb button{font:inherit;font-weight:700;font-size:18px;min-width:44px;min-height:44px;padding:0 .6rem;border-radius:10px;border:1px solid rgba(255,255,255,.4);background:rgba(255,255,255,.08);color:#fff;cursor:pointer}
.dc-lb button:hover{background:rgba(255,255,255,.18)}
.dc-lb button:disabled{opacity:.45;cursor:default}
.dc-lb .dc-lb-fit{font-size:14px}
.dc-lb button:focus-visible,.dc-lb input:focus-visible,.dc-lb-view:focus-visible{outline:3px solid #58d0bd;outline-offset:2px}
.dc-lb-z{min-width:4.3em;text-align:center;font-size:14px;font-variant-numeric:tabular-nums}
.dc-lb-opts{display:flex;flex-wrap:wrap;gap:.2rem 1.2rem;padding:.3rem .9rem;font-size:14px}
.dc-lb-opts label{display:flex;align-items:center;gap:.45rem;min-height:40px;cursor:pointer}
.dc-lb-opts input{width:20px;height:20px;accent-color:#58d0bd;margin:0}
.dc-lb-view{flex:1;min-height:0;overflow:auto;display:flex;padding:12px;touch-action:none;cursor:grab;background:#2a3f5a}
.dc-lb-view.drag{cursor:grabbing}
.dc-lb-stage{margin:auto;position:relative;flex:none;background:#fff;box-shadow:0 10px 40px rgba(0,0,0,.45)}
.dc-lb-stage canvas{position:absolute;top:0;left:0;display:block}
.dc-lb-help{margin:0;padding:.45rem .9rem;font-size:13px;color:#d1d3d4}
@media(max-width:600px){.dc-lb-help{display:none}.dc-lb .dc-lb-t{flex-basis:100%;font-size:15px}.dc-lb-bar{gap:.4rem;padding:.5rem}}
#dc-report{display:none}
@media print{
html.dc-printing body>*:not(#dc-report){display:none!important}
html.dc-printing body{background:#fff!important;margin:0!important;padding:0!important}
html.dc-printing #dc-report{display:block;color:#1a2a2a;font:10.5pt/1.45 Barlow,Arial,sans-serif}
#dc-report *{-webkit-print-color-adjust:exact;print-color-adjust:exact}
@page{size:A4;margin:14mm}
.dcr-head{display:flex;align-items:center;gap:10px;border-bottom:3px solid #58d0bd;padding-bottom:8px;margin-bottom:12px}
.dcr-head img{width:14mm;height:14mm;object-fit:contain}
.dcr-head strong{display:block;font:900 17pt/1 'Barlow Condensed',sans-serif;text-transform:uppercase;color:#132e50}
.dcr-head span{font-size:9pt;font-weight:700;color:#177567}
.dcr-head p{margin:0 0 0 auto;text-align:right;font-size:9pt;color:#132e50}
.dcr-h1{font:900 21pt/1.1 'Barlow Condensed',sans-serif;text-transform:uppercase;color:#132e50;margin:0 0 8px}
.dcr-h2{font:900 15pt/1.1 'Barlow Condensed',sans-serif;text-transform:uppercase;color:#132e50;margin:8mm 0 3mm;break-after:avoid}
.dcr-meta{border-collapse:collapse;margin:0 0 10px}
.dcr-meta th{text-align:left;padding:2px 16px 2px 0;color:#132e50;vertical-align:top}
.dcr-meta td{padding:2px 0}
#dc-report .dc-verdict,#dc-report .dc-list li,#dc-report tr{break-inside:avoid}
#dc-report .dc-verdict{padding:10px 12px}
#dc-report .dc-list{gap:4px}
#dc-report .dc-list li{padding:6px 10px}
#dc-report .dc-list p{font-size:10pt}
#dc-report .dc-imgs summary{list-style:none;padding:6px 0}
#dc-report .dc-imgs summary::-webkit-details-marker{display:none}
#dc-report .dc-tw{overflow:visible}
.dcr-shots{display:flex;flex-wrap:wrap;gap:6mm}
.dcr-shots figure{margin:0;break-inside:avoid}
.dcr-shots img{display:block;max-width:82mm;max-height:105mm;border:1px solid #d1d3d4}
.dcr-shots figcaption{font-size:9pt;color:#555;margin-top:2px}
.dcr-foot{margin-top:8mm;padding-top:4px;border-top:1px solid #d1d3d4;font-size:8.5pt;color:#555}
}
</style>'''

RICHTWERTE = [
    ['Visitenkarten, Flyer, Briefpapier, Plakat bis A3', '300 ppi (mind. 200)', '3 mm', '3 mm'],
    ['Plakate ab A2, Roll-ups', '150 ppi (mind. 100)', '3 mm', '10 mm'],
    ['Banner, Bauzaun, Großformat', '100 ppi (mind. 60)', 'nach Absprache (Saum, Ösen)', '30 mm'],
    ['Folien, Schaufenster, Fahrzeug', '150 ppi (mind. 100)', '3 mm', '10 mm'],
]

P = dict(file='druckdaten-check.html', crumb='Druckdaten-Check', img='druckdaten-check',
 parent=('Druckerei', 'print.html'), finder_strip=False, tab_ey='Richtwerte', hero_mobile=True,
 img_alt='Illustration: Flyer mit Schnittkante und Sicherheitsabstand, daneben ein Prüfergebnis mit Format, Auflösung, Schriften, Farben und Randabstand',
 title='Druckdaten-Check kostenlos: PDF online prüfen | Masar',
 desc='Druckdaten kostenlos online prüfen: Auflösung (ppi), Beschnitt, Format, Schriften und Farben Ihrer PDF oder Ihres Bildes – sofort im Browser, ohne Upload.',
 service_type='Druckdatenprüfung', schema_name='Kostenloser Druckdaten-Check',
 area=[{"@type": "Country", "name": "Deutschland"}],
 badge='Kostenloses Werkzeug · Druckdaten', h1='Druckdaten-Check <em>kostenlos</em>',
 sub='Prüfen Sie Ihre PDF oder Ihr Bild, bevor Sie es drucken lassen: Auflösung, Beschnitt, Format, Schriften und Farben – in Sekunden und direkt in Ihrem Browser. Ihre Datei wird dabei nicht hochgeladen.',
 trust='Kostenlos · ohne Anmeldung · PDF, JPG, PNG · für jede Druckerei',
 usp=['Kostenlos &amp; ohne Anmeldung', 'Datei bleibt auf Ihrem Gerät', 'PDF, JPG und PNG', 'Ergebnis in Sekunden'],
 wa='Hallo, ich möchte eine Druckdatei prüfen lassen. Ich schicke Ihnen die Datei.',
 top=('Jetzt prüfen', 'Datei wählen – <em>Ergebnis in Sekunden</em>',
      'Wählen Sie, was gedruckt werden soll, und legen Sie Ihre Datei ab. Der Check zeigt, was passt und was Sie vor dem Druck ändern sollten.',
      WERKZEUG),
 angles_ey='Warum prüfen', angles_h2='Die vier häufigsten <em>Druckfehler</em>',
 angles_sub='Fast alle Probleme beim Drucken entstehen in der Datei – und lassen sich vorher leicht erkennen.',
 angles=[
  ('Unscharfe Bilder', 'Ein Foto, das am Bildschirm gut aussieht, kann im Druck pixelig werden. Entscheidend ist, wie viele Pixel auf jeden Zentimeter kommen.'),
  ('Weiße Blitzer am Rand', 'Fehlt der Beschnitt, bleibt beim Schneiden oft ein dünner weißer Streifen stehen – besonders bei farbigen Hintergründen.'),
  ('Abgeschnittene Texte', 'Text, der zu nah an der Kante steht, kann beim Schneiden angeschnitten werden. Ein paar Millimeter Abstand reichen.'),
  ('Andere Farben und Schriften', 'Bildschirmfarben (RGB) wirken im Druck oft etwas matter, nicht eingebettete Schriften werden ersetzt.'),
 ],
 tab_h2='Wie viel Auflösung <em>braucht mein Druck?</em>', tab_sub='Mit diesen Richtwerten arbeitet der Check. Je weiter man vom Druck entfernt steht, desto weniger Pixel braucht das Motiv.',
 tab_cols=['Produkt', 'Auflösung am Endformat', 'Beschnitt je Seite', 'Sicherheitsabstand'],
 tab_rows=RICHTWERTE,
 tab_note='ppi = Pixel pro Zoll (2,54 cm), oft auch dpi genannt. Vektorgrafiken (Logos und Texte als PDF, SVG, AI oder EPS) sind immer scharf – egal wie groß. Mehr dazu im Ratgeber <a href="/blog/logo-dateien-werbetechnik.html">Logo-Dateien für Werbetechnik</a>.',
 svc_h2='Datei geprüft? <em>Wir drucken sie.</em>', svc_sub='Von der Visitenkarte bis zum Banner – gedruckt und auf Wunsch montiert.',
 services=[
  ('druck', 'Flyer, Karten &amp; Plakate', 'Visitenkarten, Flyer, Plakate und Roll-ups für Ihr Geschäft.', '/print.html'),
  ('stern', 'PVC-Banner', 'Banner für Fassade, Bauzaun und Events – mit Saum und Ösen.', '/pvc-banner-berlin.html'),
  ('karte', 'Folien &amp; Aufkleber', 'Bedruckte Folien, Sticker und Schriftzüge für Fenster und Wände.', '/foliendruck-berlin.html'),
  ('schutz', 'Fahrzeugbeschriftung', 'Logo und Kontaktdaten auf Auto, Transporter und LKW.', '/fahrzeugbeschriftung-berlin.html'),
  ('neon', 'Textildruck', 'T-Shirts, Hoodies und Taschen mit Ihrem Logo – ab 5 Stück.', '/textildruck-berlin.html'),
  ('web', 'Gestaltung', 'Keine fertige Datei? Wir gestalten Ihr Motiv druckfertig.', '/grafikdesign-berlin.html'),
 ],
 preis_h2='Was kostet <em>der Check?</em>',
 preis_html='''<p><strong>Nichts.</strong> Der Druckdaten-Check ist kostenlos, ohne Anmeldung und so oft Sie möchten nutzbar – auch wenn Sie woanders drucken lassen.</p>
<p>Sie möchten auf Nummer sicher gehen? Schicken Sie uns Ihre Datei per WhatsApp oder über das Formular unten. Wir sehen sie uns <strong>kostenlos</strong> an und sagen Ihnen, ob sie druckfertig ist. Muss etwas geändert werden, erfahren Sie vorher, was zu tun ist – und ob dafür Kosten entstehen.</p>''',
 recht_ey='Anleitung', recht_h2='So exportieren Sie <em>eine druckfertige PDF</em>', recht_sub=None,
 recht_html='''<p><strong>Canva:</strong> Unter „Datei“ den Anschnitt einblenden und Hintergründe bis über den Rand ziehen. Beim Herunterladen „PDF (Druck)“ wählen und „Schnittmarken und Anschnitt“ aktivieren.</p>
<p><strong>Adobe InDesign oder Illustrator:</strong> Dokument im Endformat mit 3&nbsp;mm Anschnitt anlegen. Exportieren als „PDF/X-4“ und unter „Marken und Anschnitt“ die Anschnitteinstellungen des Dokuments übernehmen.</p>
<p><strong>Affinity Publisher oder Designer:</strong> Beim Export die Voreinstellung „PDF/X-4“ wählen und „Anschnitt einschließen“ aktivieren.</p>
<p><strong>Word oder PowerPoint:</strong> Diese Programme kennen keinen Beschnitt. Lassen Sie am Rand einen weißen Streifen oder legen Sie die Seite je Seite 3&nbsp;mm größer an. Beim Speichern als PDF die Option „ISO 19005-1-kompatibel (PDF/A)“ wählen – dann sind die Schriften eingebettet.</p>
<p><strong>Fotos vom Handy:</strong> Immer das Original schicken, nicht ein Bild aus WhatsApp oder Social Media – dort werden Fotos stark verkleinert.</p>''',
 ablauf=[
  ('Produkt wählen', 'Wählen Sie Format oder Größe – zum Beispiel Flyer A5, Roll-up oder Banner nach Maß.'),
  ('Datei ablegen', 'Ziehen Sie Ihre PDF, JPG oder PNG in das Feld. Die Prüfung läuft auf Ihrem Gerät.'),
  ('Ergebnis lesen', 'Grün passt, Orange ist ein Hinweis, Rot sollten Sie ändern. Ein Klick auf die Vorschau öffnet die Seite groß – mit Zoom, Schnittkante und markierten Problemstellen.'),
  ('Drucken lassen', 'Schicken Sie uns die Datei mit dem Ergebnis per WhatsApp oder Formular – Sie bekommen ein Angebot. Den Prüfbericht können Sie drucken oder als PDF speichern.'),
 ],
 faq_h2='Druckdaten-Check – <em>Fragen &amp; Antworten</em>',
 faq=[
  ('Wird meine Datei hochgeladen?', 'Nein. Die Prüfung läuft vollständig in Ihrem Browser. Die Datei verlässt Ihr Gerät nicht und wird von uns weder gespeichert noch gesehen – erst wenn Sie sie uns selbst schicken.'),
  ('Was prüft der Check genau?', 'Format und Beschnitt (bei PDFs auch über die hinterlegte TrimBox, den Rahmen des Endformats), die Auflösung jedes Bildes im Endformat, eingebettete Schriften, Farbraum (RGB, CMYK, PDF/X) und Sonderfarben, den Abstand von Texten zur Schnittkante, Haarlinien unter 0,25 pt und Schrift unter 6 pt im Endformat. Alle Bilder sehen Sie in einer Liste, jede Seite in einer großen Ansicht mit Zoom.'),
  ('Was bedeutet dpi bzw. ppi?', 'Die Zahl gibt an, wie viele Pixel auf einen Zoll (2,54 cm) kommen. Für Flyer und Visitenkarten sind 300 ppi am Endformat üblich, für Plakate ab A2 und Roll-ups reichen meist 150 ppi, für große Banner etwa 100 ppi.'),
  ('Was ist Beschnitt?', 'Eine Zugabe rund um das Endformat, meist 3 mm je Seite. Farben und Bilder, die bis zum Rand gehen, laufen in diese Zugabe hinein. Sie wird beim Schneiden entfernt – so entstehen keine weißen Ränder.'),
  ('Muss meine Datei in CMYK sein?', 'Nicht unbedingt. Gedruckt wird in CMYK; RGB-Dateien rechnen wir um. Sehr leuchtende Farben wie Neongrün oder kräftiges Blau können dabei etwas matter werden. Wer die Farben selbst steuern will, exportiert als PDF/X-4 in CMYK.'),
  ('Welche Dateien kann ich prüfen?', 'PDF, JPG, PNG und WebP bis 200 MB. Bei PDF-Dateien werden die ersten 30 Seiten geprüft. AI-, EPS-, PSD- oder TIFF-Dateien können Sie uns direkt schicken – wir prüfen sie kostenlos.'),
  ('Ersetzt der Check eine Prüfung durch die Druckerei?', 'Er findet die häufigsten Fehler automatisch, kann aber nicht alles beurteilen – etwa Farbauftrag, Überdrucken, Rechtschreibung, Farbwirkung oder ob das Layout gefällt. Für einen zweiten Blick schicken Sie uns die Datei.'),
 ],
 links=[('/print.html', 'Druckerei Berlin'), ('/blog/logo-dateien-werbetechnik.html', 'Logo-Dateien'), ('/pvc-banner-berlin.html', 'PVC-Banner'),
        ('/foliendruck-berlin.html', 'Foliendruck &amp; Sticker'), ('/grafikdesign-berlin.html', 'Grafikdesign')],
 form_opts=['Flyer / Visitenkarten', 'Plakat / Roll-up', 'Banner', 'Folie / Aufkleber', 'Textildruck', 'Etwas anderes'],
 form_labels=('Was soll gedruckt werden?', 'Format, Stückzahl &amp; Wunsch', 'Ihre Druckdatei (optional)', 'PDF, JPG oder PNG. Wir sehen die Datei kostenlos durch und melden uns.'),
 form_sub='Schicken Sie uns Ihre Datei – wir prüfen sie kostenlos und sagen Ihnen, ob sie druckfertig ist. Auf Wunsch bekommen Sie gleich ein Angebot.',
 subject='Druckdaten-Check (Website)', msg_ph='z. B. 500 Flyer A5, beidseitig, bitte Datei prüfen',
 sticky=('Druckdaten-Check', 'Kostenlos prüfen – Ihre Datei bleibt bei Ihnen'))

APP = {"@context": "https://schema.org", "@type": "WebApplication", "name": "Druckdaten-Check",
       "url": "https://masar-werbeagentur.de/druckdaten-check.html", "applicationCategory": "UtilitiesApplication",
       "operatingSystem": "Web-Browser", "inLanguage": "de", "isAccessibleForFree": True,
       "description": P['desc'],
       "featureList": ["Format und Beschnitt (auch TrimBox)", "Bildauflösung je Bild", "Eingebettete Schriften", "Farbraum und Sonderfarben",
                       "Sicherheitsabstand zur Schnittkante", "Haarlinien und kleine Schrift", "Vorschau mit Zoom", "Prüfbericht zum Drucken"],
       "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
       "provider": {"@id": "https://masar-werbeagentur.de/#identity"}}

if __name__ == '__main__':
    f, n = build_f(P)
    path = ROOT + f
    s = open(path, encoding='utf-8').read()
    s = s.replace('<section class="section" id="preise">', '<section class="section" id="check">', 1)
    s = s.replace('<a href="#kontakt" class="btn btn-teal">Angebot anfordern</a>', '<a href="#check" class="btn btn-teal">Datei jetzt prüfen</a>', 1)
    s = s.replace('Foto per WhatsApp schicken</a>', 'Datei per WhatsApp schicken</a>', 1)
    s = s.replace('Kostenloses Angebot <em>anfordern</em>', 'Datei <em>von uns prüfen lassen</em>', 1)
    s = s.replace('✓ Anfrage senden – kostenlos &amp; unverbindlich', '✓ Datei senden – kostenlos prüfen lassen', 1)
    s = s.replace('</head>', CSS + '\n<script type="application/ld+json">\n' + json.dumps(APP, ensure_ascii=False, indent=2) + '\n</script>\n</head>', 1)
    s = s.replace('</body>', '<script src="/druckcheck.js?v=3" defer></script>\n</body>', 1)
    open(path, 'w', encoding='utf-8').write(s)
    print(f, len(s))
