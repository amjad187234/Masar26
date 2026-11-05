"""Schilder- & Leuchtbuchstaben-Konfigurator (leuchtbuchstaben-konfigurator.html) – Generator auf Basis von gen_folien.build_f.
Werkzeug: /konfigurator.js (Vorschau im Browser, eigenes Fassadenfoto wird nicht hochgeladen). Schriften selbst gehostet in /fonts/konfig/ (OFL).
Lesbarkeit nach USSC (Legibility Index 30 ft/in; ×0,83 / ×0,67). Keine Preisberechnung (Inhaber, 24.10.2026) – nur die freigegebenen „ab“-Preise im Text.
Aufruf: python3 tools/folien/konfigurator_page.py
"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'gen_folien.py'), encoding='utf-8').read()
exec(src[:src.index("\nif __name__")])

def knoepfe(items, pressed):
    return ''.join(f'<button type="button" data-v="{v}" aria-pressed="{"true" if v == pressed else "false"}"{extra}>{t}</button>' for v, t, extra in items)

def swatches(farben, pressed, label):
    return (''.join(f'<button type="button" class="kf-sw" data-c="{c}" aria-pressed="{"true" if c == pressed else "false"}" style="--c:{c}" aria-label="{n}" title="{n}"></button>' for c, n in farben)
            + f'<label class="kf-sw kf-sw-pick" title="Eigene Farbe"><span class="sr">{label}: eigene Farbe</span><input type="color" value="{pressed}"></label>')

FRONT = [('#ffffff', 'Weiß'), ('#111418', 'Schwarz'), ('#132e50', 'Navy'), ('#c8102e', 'Rot'), ('#f2c200', 'Gelb'), ('#58d0bd', 'Türkis'), ('#2e7d32', 'Grün'), ('#b0b7bd', 'Silber')]
SEITE = [('#1d2226', 'Schwarz'), ('#ffffff', 'Weiß'), ('#9aa3aa', 'Silber'), ('#132e50', 'Navy')]
UNTERGRUND = [('#132e50', 'Navy'), ('#111418', 'Schwarz'), ('#ffffff', 'Weiß'), ('#c8102e', 'Rot'), ('#58d0bd', 'Türkis'), ('#9aa3aa', 'Silber')]
SCHRIFTEN = [('montserrat', 'Montserrat'), ('barlow', 'Barlow Condensed'), ('poppins', 'Poppins'), ('oswald', 'Oswald'),
             ('bebas', 'Bebas Neue'), ('playfair', 'Playfair Display'), ('dancing', 'Dancing Script')]
TYP_ICON = {
 'buchstaben': '<path d="M4 20 9 4h2l5 16"/><path d="M6.2 13h7.6"/><path d="M17 8h3v12"/>',
 'leuchtkasten': '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M7 10h10M7 14h6"/><path d="M12 2v2M4.5 3.5l1.4 1.4M19.5 3.5l-1.4 1.4"/>',
 'schild': '<rect x="3" y="6" width="18" height="12" rx="1"/><circle cx="6" cy="9" r=".6"/><circle cx="18" cy="9" r=".6"/><circle cx="6" cy="15" r=".6"/><circle cx="18" cy="15" r=".6"/>',
 'ausleger': '<path d="M3 3v18"/><path d="M3 7h6"/><rect x="9" y="5" width="11" height="11" rx="5.5"/>',
 'fenster': '<rect x="3" y="3" width="18" height="18" rx="1"/><path d="M7 9h10M7 13h7"/><path d="M3 17h18"/>',
}
TYPEN = [('buchstaben', 'Buchstaben'), ('leuchtkasten', 'Leuchtkasten'), ('schild', 'Firmenschild'), ('ausleger', 'Ausleger'), ('fenster', 'Schaufenster')]
ICO = lambda d: f'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{d}</svg>'

FONTBTN = ''.join('<button type="button" data-v="%s" aria-pressed="%s" style="font-family:K-%s"><span class="kf-fs">Abc</span><small>%s</small></button>' % (v, 'true' if v == 'montserrat' else 'false', v, n) for v, n in SCHRIFTEN)
WERKZEUG = f'''    <div class="kf" id="konfig">
      <div class="kf-view">
        <div class="kf-stage"><canvas id="kf-canvas" tabindex="0" role="img" aria-label="Vorschau des Schilds an der Fassade. Mit Maus, Finger oder Pfeiltasten verschieben."></canvas></div>
        <div class="kf-bar">
          <button type="button" id="kf-nacht" aria-pressed="false"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true" focusable="false"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/></svg> Nacht</button>
          <button type="button" id="kf-masse" aria-pressed="true">Maße</button>
          <label class="kf-upl"><input type="file" id="kf-foto" accept="image/*"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true" focusable="false"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3Z"/><circle cx="12" cy="13" r="3"/></svg> Eigene Fassade</label>
        </div>
        <p class="kf-tip">Schild ziehen zum Verschieben · Ihr Foto bleibt auf Ihrem Gerät</p>
        <div class="kf-row" id="kf-fotowrap" hidden>
          <div class="kf-f"><label for="kf-fw">Breite der Fassade im Foto (m)</label><input id="kf-fw" type="number" min="1" max="60" step="0.1" value="8" inputmode="decimal"></div>
          <button type="button" class="kf-link" id="kf-demo">Zur Beispiel-Fassade</button>
        </div>
        <p class="kf-warn" id="kf-warn" role="status" hidden></p>
      </div>

      <div class="kf-ctrl">
        <fieldset class="kf-step"><legend><span>1</span>Schildart</legend>
          <div class="kf-typ" id="kf-typ">{''.join(f'<button type="button" data-v="{v}" aria-pressed="{"true" if v == "buchstaben" else "false"}">{ICO(TYP_ICON[v])}<span>{t}</span></button>' for v, t in TYPEN)}</div>
          <div id="kf-optwrap"><p class="kf-lab" id="kf-opt-l">Ausführung der Buchstaben</p>
            <div class="kf-seg kf-seg3" id="kf-opt" role="group" aria-labelledby="kf-opt-l">{knoepfe([('front', '<strong>Frontleuchtend</strong><small>Front leuchtet</small>', ''), ('halo', '<strong>Rückleuchtend</strong><small>Lichtkranz an der Wand</small>', ''), ('unbel', '<strong>Unbeleuchtet</strong><small>3D, ohne Licht</small>', '')], 'front')}</div>
          </div>
        </fieldset>
        <fieldset class="kf-step"><legend><span>2</span>Text &amp; Schrift</legend>
          <div class="kf-f"><label for="kf-text">Firmenname</label><input id="kf-text" type="text" maxlength="40" value="Ihr Name" autocomplete="organization"></div>
          <div class="kf-f"><label for="kf-text2">Zweite Zeile <span class="kf-opt-t">(optional, z. B. „Friseur“)</span></label><input id="kf-text2" type="text" maxlength="50"></div>
          <p class="kf-lab" id="kf-font-l">Schrift</p>
          <div class="kf-font" id="kf-font" role="group" aria-labelledby="kf-font-l">{FONTBTN}</div>
        </fieldset>
        <fieldset class="kf-step"><legend><span>3</span>Farben &amp; Licht</legend>
          <p class="kf-lab" id="kf-face-l">Schriftfarbe</p><div class="kf-sws" id="kf-face" role="group" aria-labelledby="kf-face-l">{swatches(FRONT, '#ffffff', 'Schriftfarbe')}</div>
          <div id="kf-sidewrap"><p class="kf-lab" id="kf-side-l">Seiten (Zarge)</p><div class="kf-sws" id="kf-side" role="group" aria-labelledby="kf-side-l">{swatches(SEITE, '#1d2226', 'Seitenfarbe')}</div></div>
          <div id="kf-bgwrap" hidden><p class="kf-lab" id="kf-bg-l">Untergrund</p><div class="kf-sws" id="kf-bg" role="group" aria-labelledby="kf-bg-l">{swatches(UNTERGRUND, '#132e50', 'Untergrund')}</div></div>
          <div id="kf-lichtwrap"><p class="kf-lab" id="kf-licht-l">Lichtfarbe</p><div class="kf-seg" id="kf-licht" role="group" aria-labelledby="kf-licht-l">{knoepfe([('kalt', 'Kaltweiß', ''), ('warm', 'Warmweiß', ''), ('farbe', 'Wie Schrift', '')], 'kalt')}</div></div>
          <div id="kf-wandwrap"><p class="kf-lab" id="kf-wand-l">Fassade (Beispiel)</p><div class="kf-seg" id="kf-wand" role="group" aria-labelledby="kf-wand-l">{knoepfe([('hell', 'Hell', ''), ('grau', 'Grau', ''), ('anthrazit', 'Anthrazit', ''), ('ziegel', 'Ziegel', '')], 'hell')}</div></div>
        </fieldset>
        <fieldset class="kf-step"><legend><span>4</span>Größe</legend>
          <div class="kf-seg" id="kf-modus" role="group" aria-label="Größe bestimmen">{knoepfe([('platz', 'Nach Platz', ''), ('abstand', 'Nach Leseabstand', ''), ('eigen', 'Eigene Höhe', '')], 'platz')}</div>
          <div class="kf-m" data-m="platz"><div class="kf-row">
            <div class="kf-f"><label for="kf-pw">Verfügbare Breite (cm)</label><input id="kf-pw" type="number" min="10" max="3000" value="400" inputmode="numeric"></div>
            <div class="kf-f"><label for="kf-ph">Verfügbare Höhe (cm)</label><input id="kf-ph" type="number" min="5" max="1000" value="80" inputmode="numeric"></div></div>
            <p class="kf-small">Wir setzen die Buchstaben so groß, wie es auf die Fläche passt.</p></div>
          <div class="kf-m" data-m="abstand" hidden>
            <p class="kf-small">Drei Größen nach der Lesbarkeits-Methode der USSC – je unruhiger die Umgebung, desto größer:</p>
            <div class="kf-opt3">{''.join(f'<button type="button" aria-pressed="{"true" if i == 1 else "false"}"><strong>{t}</strong><span class="kf-o-h">–</span><small class="kf-o-m"></small><em>{d}</em></button>' for i, (t, d) in enumerate([('Lesbar', 'ruhige Umgebung'), ('Empfohlen', 'normale Straße'), ('Auffällig', 'viel Betrieb, viel Werbung')]))}</div>
          </div>
          <div class="kf-m" data-m="eigen" hidden><div class="kf-f"><label for="kf-he">Höhe der Großbuchstaben (cm)</label><input id="kf-he" type="number" min="2" max="500" value="40" inputmode="numeric"></div></div>
          <div class="kf-f kf-range"><label for="kf-dist">Leseabstand: <output id="kf-dist-out" for="kf-dist">25 m</output></label><input id="kf-dist" type="range" min="3" max="150" value="25"></div>
          <div class="kf-f"><label for="kf-region">Standort</label><select id="kf-region"><option value="berlin">Berlin</option><option value="nrw">NRW</option><option value="hamburg">Hamburg</option><option value="andere">Anderer Ort</option></select></div>
        </fieldset>
      </div>

      <div class="kf-res">
        <div class="kf-mini"><canvas id="kf-mini" aria-hidden="true"></canvas><p id="kf-mini-cap" class="kf-small" aria-live="polite"></p></div>
        <table class="kf-tab"><caption>Ihr Entwurf</caption><tbody id="kf-tab"></tbody></table>
        <p class="kf-gen" id="kf-gen"></p>
        <div class="kf-act">
          <button type="button" class="btn btn-teal" id="kf-anfrage">Festpreis-Angebot anfordern</button>
          <button type="button" class="btn kf-btn2" id="kf-wa">Per WhatsApp senden</button>
          <button type="button" class="kf-again" id="kf-png">Vorschau speichern (PNG)</button>
        </div>
        <p class="kf-small">Die Vorschau ist eine Näherung. Vor der Fertigung bekommen Sie einen maßstabsgerechten Entwurf zur Freigabe.</p>
      </div>
    </div>'''

FF = ''.join(f"@font-face{{font-family:'K-{k}';src:url(/fonts/{p}) format('woff2');font-weight:{w};font-display:swap}}" for k, p, w in [
    ('montserrat', 'konfig/montserrat-800.woff2', 800), ('barlow', 'barlow-condensed-black.woff2', 900), ('poppins', 'konfig/poppins-600.woff2', 600),
    ('oswald', 'konfig/oswald-600.woff2', 600), ('bebas', 'konfig/bebas-neue-400.woff2', 400), ('playfair', 'konfig/playfair-700.woff2', 700),
    ('dancing', 'konfig/dancing-script-700.woff2', 700)])

CSS = '<style id="konfig-css">' + FF + '''
.kf{display:grid;grid-template-columns:minmax(0,1fr);gap:1.2rem;max-width:1180px;margin:0 auto}
.kf-view{position:sticky;top:calc(var(--nav-h,70px) + 6px);z-index:5;background:var(--off);border:1px solid var(--border);border-radius:16px;padding:.7rem;box-shadow:0 10px 30px rgba(19,46,80,.08)}
.kf-stage{display:flex;justify-content:center}
.kf-stage canvas{display:block;max-width:100%;border-radius:10px;touch-action:none;background:#dfe5e8}
.kf-stage canvas:focus-visible{outline:3px solid var(--navy);outline-offset:3px}
.kf-stage canvas.drag{cursor:grabbing!important}
.kf-bar{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:.6rem}
.kf-bar button,.kf-upl{display:inline-flex;align-items:center;gap:.4rem;font:inherit;font-weight:700;font-size:14px;padding:.55rem .9rem;min-height:44px;border-radius:10px;border:1px solid #b9c7c7;background:#fff;color:var(--navy);cursor:pointer;position:relative}
.kf-bar button[aria-pressed=true]{background:var(--navy);color:#fff;border-color:var(--navy)}
.kf-upl input{position:absolute;inset:0;opacity:0;cursor:pointer;width:100%}
.kf-upl:focus-within{outline:3px solid var(--navy);outline-offset:2px}
.kf-tip{font-size:12.5px;color:var(--muted);margin:.4rem 0 0}
.kf-warn{margin:.5rem 0 0;font-size:14px;color:#8a5100;background:#fff6e5;border:1px solid #f0cf8f;border-radius:8px;padding:.5rem .7rem}
.kf-ctrl{display:grid;gap:1rem}
.kf-step{border:1px solid var(--border);border-radius:14px;padding:1rem 1rem 1.1rem;background:#fff;min-width:0}
.kf-step legend{font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:1.25rem;text-transform:uppercase;color:var(--navy);padding:0 .4rem;display:flex;align-items:center;gap:.5rem}
.kf-step legend span{display:inline-flex;width:28px;height:28px;border-radius:50%;background:var(--teal);color:var(--navy);align-items:center;justify-content:center;font-size:1rem}
.kf-lab{font-weight:700;color:var(--navy);font-size:15px;margin:.9rem 0 .45rem}
.kf [hidden]{display:none!important}
.kf-typ{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.45rem}
.kf-typ button{display:flex;flex-direction:column;align-items:center;gap:.3rem;font:inherit;font-size:13px;font-weight:700;padding:.6rem .2rem;min-height:72px;border-radius:12px;border:1.5px solid var(--border);background:#fff;color:var(--navy);cursor:pointer}
.kf-typ button span{overflow-wrap:anywhere;text-align:center;line-height:1.2}
.kf button[aria-pressed=true]{border-color:var(--teal-ink);background:#e6f7f4;box-shadow:inset 0 0 0 1px var(--teal-ink)}
.kf-bar button[aria-pressed=true]{background:var(--navy);box-shadow:none}
.kf-seg{display:flex;flex-wrap:wrap;gap:.45rem}
.kf-seg button{flex:1 1 auto;font:inherit;font-size:14px;font-weight:700;padding:.55rem .7rem;min-height:44px;border-radius:10px;border:1.5px solid var(--border);background:#fff;color:var(--navy);cursor:pointer}
.kf-seg3 button{display:flex;flex-direction:column;align-items:flex-start;text-align:left;flex:1 1 140px}
.kf-seg3 small{font-weight:400;color:var(--muted);font-size:12.5px}
.kf-font{display:grid;grid-template-columns:repeat(auto-fill,minmax(96px,1fr));gap:.45rem}
.kf-font button{display:flex;flex-direction:column;align-items:center;gap:.1rem;padding:.5rem .3rem;min-height:64px;border-radius:10px;border:1.5px solid var(--border);background:#fff;color:var(--navy);cursor:pointer}
.kf-fs{font-size:1.5rem;line-height:1.1}
.kf-font small{font-family:Barlow,sans-serif;font-size:12px;color:var(--muted);text-align:center}
.kf-sws{display:flex;flex-wrap:wrap;gap:.45rem}
.kf-sw{width:44px;height:44px;border-radius:50%;border:2px solid #fff;box-shadow:0 0 0 1.5px #b9c7c7;background:var(--c);cursor:pointer;position:relative;padding:0}
.kf .kf-sw[aria-pressed=true]{box-shadow:0 0 0 3px var(--teal-ink);background:var(--c)}
.kf-sw-pick{background:conic-gradient(#e53935,#fdd835,#43a047,#1e88e5,#8e24aa,#e53935);display:inline-block}
.kf-sw-pick input{position:absolute;inset:0;opacity:0;cursor:pointer;width:100%;height:100%}
.kf-sw-pick:focus-within{outline:3px solid var(--navy);outline-offset:2px}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.kf-row{display:flex;flex-wrap:wrap;gap:.8rem;align-items:flex-end}
.kf-f{display:flex;flex-direction:column;gap:.3rem;flex:1 1 150px;min-width:0;margin-top:.7rem}
.kf-f label{font-weight:700;color:var(--navy);font-size:14.5px}
.kf-opt-t{font-weight:400;color:var(--muted)}
.kf-f input[type=text],.kf-f input[type=number],.kf-f select{font:inherit;font-size:16px;padding:.65rem .8rem;border:1px solid #b9c7c7;border-radius:10px;background:#fff;color:var(--text);min-height:46px;width:100%}
.kf-range input{width:100%;accent-color:#177567;min-height:32px}
.kf-small{font-size:13.5px;color:var(--muted);margin:.5rem 0 0}
.kf-link{font:inherit;font-weight:700;color:var(--teal-ink);background:none;border:0;text-decoration:underline;cursor:pointer;min-height:44px}
.kf-opt3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.45rem;margin-top:.6rem}
.kf-opt3 button{display:flex;flex-direction:column;align-items:flex-start;gap:.1rem;text-align:left;font:inherit;padding:.6rem .7rem;border-radius:12px;border:1.5px solid var(--border);background:#fff;color:var(--navy);cursor:pointer;min-width:0}
.kf-o-h{font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:1.5rem;line-height:1.1}
.kf-opt3 small{font-size:12.5px;color:var(--text)}.kf-opt3 em{font-style:normal;font-size:12px;color:var(--muted)}
.kf-res{background:#fff;border:1px solid var(--border);border-radius:16px;padding:1rem;min-width:0}
.kf-mini canvas{display:block;width:100%;border-radius:10px;background:#cfd9df}
.kf-tab{width:100%;border-collapse:collapse;margin-top:1rem;font-size:15px}
.kf-tab caption{text-align:left;font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:1.2rem;text-transform:uppercase;color:var(--navy);margin-bottom:.3rem}
.kf-tab th{text-align:left;font-weight:600;color:var(--muted);padding:.45rem .5rem .45rem 0;border-top:1px solid var(--border);width:42%;vertical-align:top}
.kf-tab td{padding:.45rem 0;border-top:1px solid var(--border);color:var(--navy);font-weight:700;overflow-wrap:anywhere}
.kf-gen{font-size:14px;background:var(--off);border-left:4px solid var(--teal);border-radius:8px;padding:.7rem .9rem;margin:1rem 0 0}
.kf-gen a{color:var(--teal-ink);font-weight:700}
.kf-act{display:flex;flex-wrap:wrap;gap:.6rem;margin-top:1rem}
.kf-act .btn{flex:1 1 220px;justify-content:center;text-align:center;cursor:pointer;border:0;font:inherit;font-weight:700}
.kf-btn2{background:var(--navy);color:#fff}
.kf-again{flex:1 1 180px;font:inherit;font-weight:700;padding:.8rem 1rem;border-radius:10px;border:2px solid var(--border);background:#fff;color:var(--navy);cursor:pointer;min-height:48px}
@media(min-width:1000px){.kf{grid-template-columns:400px minmax(0,1fr);grid-template-areas:"ctrl view" "ctrl res";align-items:start}
 .kf-ctrl{grid-area:ctrl}.kf-view{grid-area:view}.kf-res{grid-area:res}.kf-res{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:0 1.2rem}
 .kf-res .kf-tab{margin-top:0}.kf-gen,.kf-act,.kf-res>.kf-small{grid-column:1/-1}}
@media(max-width:600px){.kf-view{padding:.45rem;top:calc(var(--nav-h,70px) + 2px)}.kf-tip{display:none}.kf-step{padding:.8rem}.kf-opt3{grid-template-columns:1fr}.kf-opt3 button{flex-direction:row;flex-wrap:wrap;align-items:baseline;gap:.2rem .6rem}}
</style>'''

P = dict(file='leuchtbuchstaben-konfigurator.html', crumb='Konfigurator', img='konfigurator',
 parent=('Leuchtreklame', 'leuchtreklame-berlin.html'), finder_strip=False, tab_ey='Ausführungen', hero_mobile=True,
 img_alt='Vorschau aus dem Konfigurator: rückleuchtende Buchstaben bei Nacht an einer Fassade mit Maßangaben',
 title='Leuchtbuchstaben-Konfigurator mit Vorschau | Masar',
 desc='Schild und Leuchtbuchstaben online planen: Schrift, Farben, Größe und Lesbarkeit – mit Vorschau auf Ihrem Fassadenfoto bei Tag und Nacht. Kostenlos.',
 service_type='Leuchtreklame', schema_name='Leuchtbuchstaben- und Schilder-Konfigurator',
 area=[{"@type": "City", "name": "Berlin"}, {"@type": "State", "name": "Nordrhein-Westfalen"}, {"@type": "City", "name": "Hamburg"}],
 badge='Kostenloses Werkzeug · Schilder &amp; Leuchtreklame', h1='Leuchtbuchstaben- <em>Konfigurator</em>',
 sub='Planen Sie Ihr Schild selbst: fünf Schildarten, drei Ausführungen für Buchstaben, sieben Schriften und Ihre Farben. Die Vorschau zeigt Ihr Schild an der Fassade – auf Wunsch auf Ihrem eigenen Foto, bei Tag und bei Nacht, mit Maßen und Lesbarkeit.',
 trust='Kostenlos · ohne Anmeldung · Vorschau Tag & Nacht · Ihr Foto bleibt auf Ihrem Gerät',
 usp=['5 Schildarten', '3 Ausführungen für Buchstaben', 'Vorschau auf Ihrer Fassade', 'Maße &amp; Lesbarkeit'],
 wa='Hallo, ich plane ein Schild bzw. Leuchtbuchstaben und hätte gern ein Angebot. Ich schicke Ihnen ein Foto der Fassade.',
 top=('Jetzt planen', 'Ihr Schild <em>in drei Minuten</em>',
      'Text eingeben, Schildart und Ausführung wählen, Größe festlegen – die Vorschau ändert sich sofort. Mit „Eigene Fassade“ setzen Sie das Schild auf ein Foto Ihres Geschäfts.',
      WERKZEUG),
 angles_ey='Warum vorher planen', angles_h2='Sicher entscheiden, <em>bevor gebaut wird</em>',
 angles_sub='Ein Schild hängt viele Jahre. Die Vorschau hilft, Größe, Schrift und Wirkung vorher zu sehen.',
 angles=[
  ('Die richtige Größe', 'Zu klein wird übersehen, zu groß wirkt erdrückend. Die Maße und die Ansicht aus der Entfernung zeigen, was zu Ihrer Fassade passt.'),
  ('Tag und Nacht', 'Leuchtbuchstaben wirken abends ganz anders. Schalten Sie um und sehen Sie Front- und Rückleuchten im Vergleich.'),
  ('Lesbar aus der Entfernung', 'Der Konfigurator rechnet nach einer anerkannten Methode, ab wie vielen Metern Ihr Schriftzug lesbar ist.'),
  ('Genehmigung im Blick', 'Die Ansichtsfläche wird mitgerechnet – mit einem Hinweis, ab wann meist eine Genehmigung nötig ist.'),
 ],
 tab_h2='Drei Ausführungen <em>für Buchstaben</em>', tab_sub='Welche passt, hängt von Fassade, Schrift und gewünschter Wirkung ab – wir beraten Sie vor Ort oder per Foto.',
 tab_cols=['Ausführung', 'Wirkung', 'Gut zu wissen'],
 tab_rows=[
  ['Frontleuchtend', 'Die Front der Buchstaben leuchtet, gut lesbar auch nachts', 'Front meist aus Acrylglas, Seiten blickdicht; klassisch für Läden und Gastronomie'],
  ['Rückleuchtend (Halo)', 'Licht strahlt nach hinten auf die Wand – ein edler Lichtkranz', 'Buchstaben stehen mit Abstand zur Wand; wirkt besonders auf glatten, hellen Fassaden'],
  ['Unbeleuchtet (3D)', 'Plastische Buchstaben, tagsüber hochwertig', 'aus Acryl, Aluminium oder Edelstahl; nachts bei Bedarf mit Strahlern beleuchtet'],
 ],
 tab_note='Bau und Montage beleuchteter Anlagen übernehmen in die Handwerksrolle eingetragene Partnerbetriebe, den elektrischen Anschluss ein Elektrofachbetrieb. Mehr zu Leuchtreklame auf <a href="/leuchtreklame-berlin.html">Leuchtreklame Berlin</a>.',
 svc_h2='Schildarten <em>im Überblick</em>', svc_sub='Alle fünf Arten können Sie im Konfigurator ausprobieren.',
 services=[
  ('neon', 'Leuchtbuchstaben', 'Front- oder rückleuchtend – die stärkste Wirkung bei Nacht.', '/leuchtreklame-berlin.html'),
  ('stern', 'Einzelbuchstaben', 'Unbeleuchtete 3D-Buchstaben aus Acryl, Alu oder Edelstahl.', '/schilder-berlin.html'),
  ('karte', 'Leuchtkasten', 'Beleuchtete Fläche mit Logo und Schrift – auch als Ausleger.', '/leuchtreklame-berlin.html'),
  ('schutz', 'Firmenschild', 'Alu-Dibond-Schild für Fassade, Eingang und Hof.', '/schilder-berlin.html'),
  ('druck', 'Praxis- und Kanzleischild', 'Acrylglas oder Alu für Praxis, Kanzlei und Büro.', '/praxisbeschilderung-berlin.html'),
  ('web', 'Schaufensterbeschriftung', 'Schriftzug, Öffnungszeiten und Logo auf dem Glas.', '/schaufensterbeschriftung-berlin.html'),
 ],
 preis_h2='Was kostet <em>mein Schild?</em>',
 preis_html=table('Startpreise Schilder', ['Leistung', 'Berlin', 'NRW'], [
     ['Leuchtbuchstaben (je Buchstabe)', 'ab 199&nbsp;€', 'ab 229&nbsp;€'], ['Einzelbuchstaben', 'ab 119&nbsp;€', 'ab 139&nbsp;€'],
     ['Firmenschild', 'ab 149&nbsp;€', 'ab 179&nbsp;€'], ['Schaufensterbeschriftung', 'ab 149&nbsp;€', 'ab 179&nbsp;€']]) + '''
<p style="margin-top:1.2rem">Alle Preise netto zzgl. 19&nbsp;% MwSt., Startpreise für einfache Ausführungen. Den genauen Preis bestimmen Größe, Material, Licht, Montage und Genehmigung. Schicken Sie uns Ihren Entwurf aus dem Konfigurator – Sie bekommen ein <strong>Festpreis-Angebot</strong>, in der Regel innerhalb von 24 Stunden.</p>''',
 recht_ey='So rechnen wir', recht_h2='Lesbarkeit und <em>Genehmigung</em>', recht_sub=None,
 recht_html='''<p><strong>Lesbarkeit:</strong> Der Konfigurator nutzt den Legibility Index der US-amerikanischen Sign-Branche (USSC): Bei guten Bedingungen ist ein Großbuchstabe von 1 Zoll Höhe etwa 30 Fuß weit lesbar – rund 2,8 cm Buchstabenhöhe je 10 m Abstand. Für unruhige Umgebungen empfiehlt die USSC einen Abschlag (Faktor 0,83 bei mittlerer, 0,67 bei hoher visueller Komplexität). Daraus entstehen die drei Größen „Lesbar“, „Empfohlen“ und „Auffällig“. Das sind Mindestwerte für die Lesbarkeit; damit ein Schild auffällt, wird es oft größer geplant.</p>
<p><strong>Ansicht aus der Entfernung:</strong> Das kleine Bild zeigt Ihr Schild ungefähr so groß, wie es auf einem Handyfoto aus dem gewählten Abstand erscheint. Eine Näherung, die beim Vergleichen hilft.</p>
<p><strong>Genehmigung:</strong> In Berlin sind Werbeanlagen bis 1&nbsp;m² Ansichtsfläche verfahrensfrei, am eigenen Geschäft bis 2,5&nbsp;m²; in NRW und Hamburg gilt 1&nbsp;m². Denkmalschutz oder örtliche Satzungen können zusätzlich gelten. Wir prüfen das für Ihren Standort – Details im <a href="/blog/aussenwerbung-berlin-ratgeber.html">Ratgeber Außenwerbung Berlin</a>.</p>
<p><strong>Ihr Foto:</strong> Das Fassadenfoto wird nur in Ihrem Browser verarbeitet und nicht hochgeladen. Erst wenn Sie die Vorschau selbst an uns senden, erhalten wir sie.</p>
<p class="price-note">Quellen: <a href="https://usscfoundation.org/wp-content/uploads/2018/03/USSC-Guideline-Standards-for-On-Premise-Signs-2018.pdf" rel="noopener" target="_blank">USSC Guideline Standards for On-Premise Signs (2018)</a> · <a href="https://www.fhwa.dot.gov/publications/research/safety/15027/004.cfm" rel="noopener" target="_blank">FHWA: Legibility of Signs</a></p>''',
 ablauf=[
  ('Planen', 'Text, Schildart, Schrift, Farben und Größe wählen – auf der Beispiel-Fassade oder Ihrem eigenen Foto.'),
  ('Senden', 'Mit einem Klick geht Ihr Entwurf samt Vorschau an uns – per Formular oder WhatsApp.'),
  ('Festpreis & Entwurf', 'Sie bekommen ein Angebot und einen maßstabsgerechten Entwurf, die Genehmigung prüfen wir mit.'),
  ('Fertigung & Montage', 'Nach Freigabe und Anzahlung wird gefertigt und montiert – beleuchtete Anlagen von eingetragenen Partnerbetrieben.'),
 ],
 faq_h2='Konfigurator – <em>Fragen &amp; Antworten</em>',
 faq=[
  ('Wird mein Fassadenfoto hochgeladen?', 'Nein. Das Foto wird nur in Ihrem Browser angezeigt. Wir sehen es erst, wenn Sie uns die Vorschau selbst schicken.'),
  ('Wie groß sollten Leuchtbuchstaben sein?', 'Das hängt vom Leseabstand und vom Platz an der Fassade ab. Als Anhalt: Bei guten Bedingungen reichen rund 2,8 cm Buchstabenhöhe je 10 m Abstand, in belebten Straßen deutlich mehr. Der Konfigurator zeigt drei Größen und wie sie an Ihrer Fassade wirken.'),
  ('Was ist der Unterschied zwischen front- und rückleuchtend?', 'Bei frontleuchtenden Buchstaben leuchtet die Vorderseite, die Schrift ist nachts klar lesbar. Rückleuchtende Buchstaben (Halo) strahlen nach hinten auf die Wand und erzeugen einen Lichtkranz – edel, aber etwas weniger kontrastreich.'),
  ('Brauche ich eine Genehmigung?', 'Oft ja, wenn die Ansichtsfläche über 1 m² liegt (in Berlin am eigenen Geschäft über 2,5 m²). Der Konfigurator zeigt die Fläche; wir prüfen die Regeln an Ihrem Standort.'),
  ('Sind die Preise im Konfigurator enthalten?', 'Nein. Sie bekommen nach Ihrem Entwurf ein Festpreis-Angebot – in der Regel innerhalb von 24 Stunden. Startpreise stehen weiter oben auf dieser Seite.'),
  ('Kann ich mein Logo einsetzen?', 'Im Konfigurator planen Sie den Schriftzug. Ihr Logo bauen wir im Entwurf ein – schicken Sie es einfach mit der Anfrage.'),
 ],
 links=[('/leuchtlogo-berlin.html', 'Leuchtlogo rund &amp; eckig'), ('/leuchtreklame-berlin.html', 'Leuchtreklame Berlin'), ('/schilder-berlin.html', 'Schilder Berlin'), ('/blog/aussenwerbung-berlin-ratgeber.html', 'Ratgeber Genehmigung'),
        ('/blog/leuchtreklame-strom-betriebszeiten.html', 'Leuchtreklame: Strom &amp; Betriebszeiten'), ('/druckdaten-check.html', 'Druckdaten-Check')],
 form_opts=['Leuchtbuchstaben', 'Einzelbuchstaben (unbeleuchtet)', 'Leuchtkasten', 'Firmenschild', 'Ausleger / Nasenschild', 'Schaufensterbeschriftung'],
 form_labels=('Welche Schildart?', 'Ihr Entwurf &amp; Wunsch', 'Vorschau oder Fassadenfoto', 'Mit „Festpreis-Angebot anfordern“ im Konfigurator wird die Vorschau hier automatisch angehängt.'),
 form_sub='Ihr Entwurf aus dem Konfigurator wird automatisch eingetragen. Ergänzen Sie Ihre Kontaktdaten – Sie bekommen ein Festpreis-Angebot, in der Regel innerhalb von 24 Stunden.',
 subject='Anfrage Konfigurator Schild (Website)', msg_ph='z. B. Leuchtbuchstaben über dem Eingang, Fassade ca. 8 m breit, Montage in Berlin-Neukölln',
 sticky=('Schild-Konfigurator', 'Planen, Vorschau sehen, Festpreis anfragen'))

APP = {"@context": "https://schema.org", "@type": "WebApplication", "name": "Leuchtbuchstaben- und Schilder-Konfigurator",
       "url": "https://masar-werbeagentur.de/leuchtbuchstaben-konfigurator.html", "applicationCategory": "DesignApplication",
       "operatingSystem": "Web-Browser", "inLanguage": "de", "isAccessibleForFree": True,
       "description": P['desc'], "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
       "provider": {"@id": "https://masar-werbeagentur.de/#identity"}}

if __name__ == '__main__':
    f, n = build_f(P)
    path = ROOT + f
    s = open(path, encoding='utf-8').read()
    s = s.replace('<section class="section" id="preise">', '<section class="section" id="planen">', 1)
    s = s.replace('<a href="#kontakt" class="btn btn-teal">Angebot anfordern</a>', '<a href="#planen" class="btn btn-teal">Jetzt Schild planen</a>', 1)
    s = s.replace('Kostenloses Angebot <em>anfordern</em>', 'Festpreis-Angebot <em>für Ihren Entwurf</em>', 1)
    s = s.replace('</head>', CSS + '\n<script type="application/ld+json">\n' + json.dumps(APP, ensure_ascii=False, indent=2) + '\n</script>\n</head>', 1)
    s = s.replace('</body>', '<script src="/konfigurator.js?v=1" defer></script>\n</body>', 1)
    open(path, 'w', encoding='utf-8').write(s)
    print(f, len(s))
