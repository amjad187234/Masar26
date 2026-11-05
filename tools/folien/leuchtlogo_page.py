"""Leuchtlogo-Seite mit Konfigurator (leuchtlogo-berlin.html) – Generator auf Basis von gen_folien.build_f.
Werkzeug: /leuchtlogo.js (Vorschau im Browser; Logo und Wandfoto werden nicht hochgeladen), Stil aus konfigurator_page.py (kf-*).
Keine Preise für Leuchtkästen (nicht freigegeben) – Festpreis-Angebot. Echte Projektfotos aus /referenzen/ (Freigabe Inhaber 05.11.2026).
Aufruf: python3 tools/folien/leuchtlogo_page.py
"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'gen_folien.py'), encoding='utf-8').read()
exec(src[:src.index("\nif __name__")])
k = open(os.path.join(HERE, 'konfigurator_page.py'), encoding='utf-8').read()
exec(k[k.index('def knoepfe'):k.index('FONTBTN')])          # knoepfe, swatches, Farben
KCSS = k[k.index("CSS = '<style id=\"konfig-css\">'"):k.index("P = dict(")]
exec(KCSS.replace("CSS = '<style id=\"konfig-css\">' + FF + '''", "CSS = '<style id=\"konfig-css\">' + '''", 1))

ICO_KREIS = '<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="5.5" stroke-dasharray="2 2"/></svg>'
ICO_ECK = '<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true" focusable="false"><rect x="3.5" y="5.5" width="17" height="13" rx="1.5"/><rect x="6.5" y="8.5" width="11" height="7" rx="1" stroke-dasharray="2 2"/></svg>'
RAHMEN = [('#15181c', 'Schwarz'), ('#f2f2f0', 'Weiß'), ('#a7adb3', 'Silber')]
FRONT = [('#ffffff', 'Weiß'), ('#111418', 'Schwarz'), ('#132e50', 'Navy'), ('#c8102e', 'Rot')]

def sw(farben, pressed, label, auto=False):
    out = '<button type="button" class="kf-sw kf-sw-auto" data-c="auto" aria-pressed="true" title="Wie Logo-Hintergrund" aria-label="Wie Logo-Hintergrund">Auto</button>' if auto else ''
    out += ''.join(f'<button type="button" class="kf-sw" data-c="{c}" aria-pressed="{"true" if c == pressed and not auto else "false"}" style="--c:{c}" aria-label="{n}" title="{n}"></button>' for c, n in farben)
    if auto: out += f'<label class="kf-sw kf-sw-pick" title="Eigene Farbe"><span class="sr">{label}: eigene Farbe</span><input type="color" value="#ffffff"></label>'
    return out

WERKZEUG = f'''    <div class="kf" id="leuchtlogo">
      <div class="kf-view">
        <div class="kf-stage"><canvas id="ll-canvas" tabindex="0" role="img" aria-label="Vorschau des Leuchtlogos an der Wand. Mit Maus, Finger oder Pfeiltasten verschieben."></canvas></div>
        <div class="kf-bar">
          <div class="kf-seg" id="ll-ansicht" role="group" aria-label="Ansicht">{knoepfe([('tag', 'Tag', ''), ('nacht', 'Nacht', ''), ('vergleich', 'Vergleich', '')], 'vergleich')}</div>
          <button type="button" id="ll-masse" aria-pressed="true">Maße</button>
          <label class="kf-upl"><input type="file" id="ll-foto" accept="image/*"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true" focusable="false"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3Z"/><circle cx="12" cy="13" r="3"/></svg> Eigene Wand</label>
        </div>
        <p class="kf-tip" id="ll-splittip">Teiler ziehen: links Tag, rechts Nacht · Schild ziehen zum Verschieben · Ihre Bilder bleiben auf Ihrem Gerät</p>
        <div class="kf-row" id="ll-fotowrap" hidden>
          <div class="kf-f"><label for="ll-fw">Breite der Wand im Foto (m)</label><input id="ll-fw" type="number" min="0.5" max="40" step="0.1" value="4" inputmode="decimal"></div>
          <button type="button" class="kf-link" id="ll-demo">Zur Beispiel-Wand</button>
        </div>
      </div>

      <div class="kf-ctrl">
        <fieldset class="kf-step"><legend><span>1</span>Ihr Logo</legend>
          <label class="ll-drop"><input type="file" id="ll-logo" accept="image/png,image/jpeg,image/webp,image/svg+xml"><strong>Logo hochladen</strong><span>PNG, JPG, WebP oder SVG</span></label>
          <p class="kf-small">Aktuell: <span id="ll-logoname">Masar-Logo (Beispiel)</span></p>
          <label class="ll-check"><input type="checkbox" id="ll-weiss" checked> Weißen Hintergrund des Logos entfernen</label>
          <div class="kf-f kf-range"><label for="ll-zoom">Logo-Größe auf der Front: <output id="ll-zoom-out" for="ll-zoom">78 %</output></label><input id="ll-zoom" type="range" min="40" max="100" value="78"></div>
        </fieldset>
        <fieldset class="kf-step"><legend><span>2</span>Form &amp; Größe</legend>
          <div class="kf-typ ll-typ2" id="ll-form"><button type="button" data-v="rund" aria-pressed="true">{ICO_KREIS}<span>Rund</span></button><button type="button" data-v="eckig" aria-pressed="false">{ICO_ECK}<span>Eckig</span></button></div>
          <div class="kf-row" id="ll-rund"><div class="kf-f"><label for="ll-d">Durchmesser (cm)</label><input id="ll-d" type="number" min="20" max="250" value="60" inputmode="numeric"></div></div>
          <div class="kf-row" id="ll-eckig" hidden>
            <div class="kf-f"><label for="ll-w">Breite (cm)</label><input id="ll-w" type="number" min="20" max="400" value="80" inputmode="numeric"></div>
            <div class="kf-f"><label for="ll-h">Höhe (cm)</label><input id="ll-h" type="number" min="20" max="250" value="50" inputmode="numeric"></div></div>
          <p class="kf-lab" id="ll-art-l">Montage</p>
          <div class="kf-seg kf-seg3" id="ll-art" role="group" aria-labelledby="ll-art-l">{knoepfe([('wand', '<strong>An der Wand</strong><small>einseitig leuchtend</small>', ''), ('ausleger', '<strong>Ausleger</strong><small>doppelseitig, steht ab</small>', '')], 'wand')}</div>
        </fieldset>
        <fieldset class="kf-step"><legend><span>3</span>Farben &amp; Licht</legend>
          <p class="kf-lab" id="ll-rahmen-l">Rahmen</p><div class="kf-sws" id="ll-rahmen" role="group" aria-labelledby="ll-rahmen-l">{''.join(f'<button type="button" class="kf-sw" data-c="{c}" aria-pressed="{"true" if i == 0 else "false"}" style="--c:{c}" aria-label="{n}" title="{n}"></button>' for i, (c, n) in enumerate(RAHMEN))}</div>
          <p class="kf-lab" id="ll-face-l">Hintergrund der Front</p><div class="kf-sws" id="ll-face" role="group" aria-labelledby="ll-face-l">{sw(FRONT, '#ffffff', 'Front', auto=True)}</div>
          <p class="kf-lab" id="ll-licht-l">Lichtfarbe</p><div class="kf-seg" id="ll-licht" role="group" aria-labelledby="ll-licht-l">{knoepfe([('kalt', 'Kaltweiß', ''), ('warm', 'Warmweiß', '')], 'kalt')}</div>
          <div id="ll-wandwrap"><p class="kf-lab" id="ll-wand-l">Wand (Beispiel)</p><div class="kf-seg" id="ll-wand" role="group" aria-labelledby="ll-wand-l">{knoepfe([('putz', 'Putz hell', ''), ('beton', 'Beton', ''), ('ziegel', 'Ziegel', ''), ('dunkel', 'Dunkel', '')], 'putz')}</div></div>
          <div class="kf-f"><label for="ll-region">Standort</label><select id="ll-region"><option value="berlin">Berlin</option><option value="nrw">NRW</option><option value="hamburg">Hamburg</option><option value="andere">Anderer Ort</option></select></div>
        </fieldset>
      </div>

      <div class="kf-res">
        <table class="kf-tab"><caption>Ihr Leuchtlogo</caption><tbody id="ll-tab"></tbody></table>
        <div>
          <p class="kf-gen" id="ll-gen" style="margin-top:0"></p>
        </div>
        <div class="kf-act">
          <button type="button" class="btn btn-teal" id="ll-anfrage">Festpreis-Angebot anfordern</button>
          <button type="button" class="btn kf-btn2" id="ll-wa">Per WhatsApp senden</button>
          <button type="button" class="kf-again" id="ll-png">Vorschau speichern (Tag + Nacht)</button>
        </div>
        <p class="kf-small">Die Vorschau ist eine Näherung. Vor der Fertigung bekommen Sie einen Entwurf zur Freigabe – Ihr Logo bereiten wir dafür druckfertig auf.</p>
      </div>
    </div>'''

LCSS = CSS.replace('<style id="konfig-css">', '<style id="konfig-css">.kf-sw-auto{background:#fff;font:700 11px Barlow,sans-serif;color:var(--navy)}'
    '.ll-typ2{grid-template-columns:repeat(2,minmax(0,1fr))!important}'
    '.ll-drop{position:relative;display:flex;flex-direction:column;align-items:center;gap:.2rem;border:2px dashed var(--teal);border-radius:12px;background:var(--off);padding:1rem;cursor:pointer;text-align:center}'
    '.ll-drop input{position:absolute;inset:0;opacity:0;cursor:pointer;width:100%}.ll-drop:focus-within{outline:3px solid var(--navy);outline-offset:2px}'
    '.ll-drop strong{color:var(--navy)}.ll-drop span{font-size:13.5px;color:var(--muted)}'
    '.ll-check{display:flex;gap:.5rem;align-items:center;font-size:14.5px;margin-top:.6rem;min-height:44px}.ll-check input{width:20px;height:20px;accent-color:#177567}'
    '#ll-ansicht button{flex:0 1 auto}', 1)

GAL = [('/referenzen/leuchtlogo-rund-bside-01-720.webp', 540, 720, 'Runder, beleuchteter Ausleger mit dem Logo „The B-Side Events – Berlin Wedding“ im Dunkeln', 'The B-Side Events, Berlin-Wedding: runder Leuchtausleger beim Lichttest', False),
       ('/referenzen/leuchtlogo-rund-burgereat-01-720.webp', 540, 720, 'Runder Leuchtkasten mit Fotodruck und Schriftzug „Burger Eat“, eingeschaltet', 'Burger Eat: runder Leuchtkasten mit Fotodruck', False),
       ('/referenzen/leuchtlogo-rund-bside-burgereat-01-720.webp', 540, 720, 'Zwei runde Leuchtausleger mit schwarzem Wandhalter, an eine Wand gelehnt', 'Zwei doppelseitige Ausleger mit Wandhalter, fertig zur Montage', False),
       ('/referenzen/leuchtreklame-berlin-06.webp', 1079, 1080, 'Runder Ausleger eines Barbershops wird über dem Eingang montiert', 'Barbershop: runder Ausleger über dem Eingang, während der Montage', False)]

P = dict(file='leuchtlogo-berlin.html', crumb='Leuchtlogo', img='leuchtlogo',
 parent=('Leuchtreklame', 'leuchtreklame-berlin.html'), finder_strip=False, tab_ey='Ausführungen', hero_mobile=True,
 img_alt='Runder Leuchtausleger mit dem Logo „The B-Side Events – Berlin Wedding“, im Dunkeln leuchtend',
 title='Leuchtlogo Berlin: runder Leuchtkasten mit Vorschau | Masar',
 desc='Ihr Logo als Leuchtkasten – rund oder eckig, an der Wand oder als Ausleger. Logo hochladen, Größe in cm wählen und bei Tag und Nacht ansehen. Festpreis.',
 service_type='Leuchtreklame', schema_name='Leuchtlogo und runder Leuchtkasten',
 badge='Leuchtlogo · Leuchtkasten rund &amp; eckig', h1='Leuchtlogo <em>Berlin</em>',
 sub='Ihr Logo als Leuchtkasten – rund oder eckig, flach an der Wand oder als doppelseitiger Ausleger über dem Eingang. Laden Sie Ihr Logo hoch, wählen Sie die Größe in Zentimetern und sehen Sie sofort, wie es bei Tag und bei Nacht an Ihrer Wand wirkt.',
 trust='Rund oder eckig · Wand oder Ausleger · Vorschau Tag & Nacht · Berlin, NRW & Hamburg',
 usp=['Vorschau mit Ihrem Logo', 'Rund oder eckig', 'Wand oder Ausleger', 'Festpreis nach Entwurf'],
 wa='Hallo, ich hätte gern ein Leuchtlogo (Leuchtkasten) mit unserem Logo. Ich schicke Ihnen das Logo und ein Foto der Wand.',
 top=('Jetzt ausprobieren', 'Ihr Logo <em>zum Leuchten bringen</em>',
      'Logo hochladen, Form und Größe wählen – mit „Vergleich“ sehen Sie Tag und Nacht nebeneinander. Mit „Eigene Wand“ setzen Sie das Leuchtlogo auf ein Foto Ihres Geschäfts.',
      WERKZEUG),
 angles_ey='Warum ein Leuchtlogo', angles_h2='Ihr Logo, <em>Tag und Nacht sichtbar</em>',
 angles_sub='Ein Leuchtkasten mit Logo ist das Erkennungszeichen über dem Eingang – auch dann, wenn es draußen dunkel ist.',
 angles=[
  ('Auffallen im Vorbeigehen', 'Ein Ausleger steht quer zur Straße und ist von beiden Seiten zu sehen – Passanten erkennen Ihr Geschäft schon von weitem.'),
  ('Abends sichtbar', 'Gerade in der dunklen Jahreszeit fällt ein beleuchtetes Logo auf, wenn andere Schilder im Dunkeln verschwinden.'),
  ('Ihr Logo in Farbe', 'Die Front wird mit Ihrem Logo bedruckt – auch Fotos, Verläufe und viele Farben, wie bei Burger Eat.'),
  ('Vorher sehen', 'Mit der Vorschau entscheiden Sie Form, Größe und Farben, bevor etwas gebaut wird.'),
 ],
 gallery=dict(h2='Leuchtlogos <em>aus unserer Arbeit</em>', sub='Runde Leuchtkästen und Ausleger, die wir geplant und mit unseren Partnerbetrieben umgesetzt haben.', items=GAL,
              note='<a href="/referenzen.html">Alle Referenzen ansehen →</a>'),
 tab_h2='Rund, eckig <em>oder Ausleger?</em>', tab_sub='Welche Form passt, hängt von Logo, Fassade und Standort ab – wir beraten Sie gern per Foto.',
 tab_cols=['Ausführung', 'Ideal für', 'Gut zu wissen'],
 tab_rows=[
  ['Rund', 'runde oder kompakte Logos, Signets, Embleme', 'wirkt wie ein Siegel; klassisch für Barbershop, Café und Gastronomie'],
  ['Eckig', 'breite Logos und Schriftzüge', 'nutzt die Fläche besser aus, wenn das Logo eher breit als hoch ist'],
  ['Ausleger (doppelseitig)', 'Ladenlokale an Straßen mit viel Fußverkehr', 'quer zur Fassade montiert, von beiden Seiten lesbar; über dem Gehweg oft erlaubnispflichtig'],
 ],
 tab_note='Bau und Montage beleuchteter Anlagen übernehmen in die Handwerksrolle eingetragene Partnerbetriebe, den elektrischen Anschluss ein Elektrofachbetrieb. Für Schriftzüge aus Einzelbuchstaben nutzen Sie den <a href="/leuchtbuchstaben-konfigurator.html">Leuchtbuchstaben-Konfigurator</a>.',
 svc_h2='Passend <em>zu Ihrem Leuchtlogo</em>', svc_sub='Alles aus einer Hand – vom Logo bis zur Fassade.',
 services=[
  ('neon', 'Leuchtbuchstaben', 'Einzelbuchstaben front- oder rückleuchtend für die Fassade.', '/leuchtbuchstaben-konfigurator.html'),
  ('stern', 'Leuchtreklame', 'Fassadenwerbung, Leuchtkästen und Lichtwerbung in Berlin.', '/leuchtreklame-berlin.html'),
  ('web', 'Logo-Design', 'Noch kein Logo oder nur als Pixelbild? Wir gestalten und vektorisieren es.', '/grafikdesign-berlin.html'),
  ('karte', 'Schaufensterbeschriftung', 'Öffnungszeiten, Logo und Leistungen auf dem Glas.', '/schaufensterbeschriftung-berlin.html'),
 ],
 preis_h2='Was kostet <em>ein Leuchtlogo?</em>',
 preis_html='''<p>Der Preis hängt von Größe, Form, ein- oder doppelseitiger Ausführung, Halterung, Montage und Genehmigung ab. Deshalb nennen wir Ihnen einen <strong>Festpreis nach Ihrem Entwurf</strong> – schicken Sie uns einfach die Vorschau aus dem Konfigurator, ein Foto der Wand und die gewünschte Größe. Sie bekommen das Angebot in der Regel innerhalb von 24 Stunden.</p>
<p>Ein Logo nur als Pixelbild? Kein Problem: Wir bereiten es für den Druck auf. Für Schriftzüge aus Einzelbuchstaben finden Sie Startpreise auf der Seite <a href="/leuchtreklame-berlin.html">Leuchtreklame Berlin</a>.</p>''',
 recht_ey='Gut zu wissen', recht_h2='Genehmigung, Strom <em>und Montage</em>', recht_sub=None,
 recht_html='''<p><strong>Genehmigung:</strong> In Berlin sind Werbeanlagen bis 1&nbsp;m² Ansichtsfläche verfahrensfrei, am eigenen Geschäft bis 2,5&nbsp;m²; in NRW und Hamburg gilt 1&nbsp;m². Ein Ausleger ragt über den Gehweg in den öffentlichen Raum – dafür ist oft zusätzlich eine Erlaubnis der Stadt bzw. des Bezirksamts nötig. Wir prüfen das für Ihren Standort. Mehr im <a href="/blog/aussenwerbung-berlin-ratgeber.html">Ratgeber Außenwerbung Berlin</a>.</p>
<p><strong>Strom:</strong> Ein Leuchtlogo braucht einen Stromanschluss in der Nähe. Den Anschluss übernimmt ein eingetragener Elektrofachbetrieb aus unserem Partnernetz. Zu Betriebszeiten und Verbrauch: <a href="/blog/leuchtreklame-strom-betriebszeiten.html">Leuchtreklame – Strom und Betriebszeiten</a>.</p>
<p><strong>Ihre Daten:</strong> Logo und Wandfoto werden in der Vorschau nur in Ihrem Browser verarbeitet und nicht hochgeladen. Erst wenn Sie uns die Vorschau schicken, erhalten wir sie.</p>''',
 ablauf=[
  ('Vorschau', 'Logo hochladen, Form, Größe und Farben wählen – auf der Beispiel-Wand oder Ihrem eigenen Foto.'),
  ('Senden', 'Mit einem Klick geht Ihr Entwurf samt Vorschau an uns – per Formular oder WhatsApp.'),
  ('Festpreis & Entwurf', 'Sie bekommen ein Festpreis-Angebot und einen Entwurf, die Genehmigung prüfen wir mit.'),
  ('Fertigung & Montage', 'Nach Freigabe und Anzahlung wird gefertigt; Bau, Montage und Anschluss übernehmen eingetragene Partnerbetriebe.'),
 ],
 faq_h2='Leuchtlogo – <em>Fragen &amp; Antworten</em>',
 faq=[
  ('Welche Größe sollte ein runder Leuchtkasten haben?', 'Das hängt von Fassade und Leseabstand ab. Probieren Sie verschiedene Durchmesser in der Vorschau aus – die Person mit 1,75 m zeigt den Maßstab. Wir beraten Sie gern anhand eines Fotos.'),
  ('Kann mein Logo auch ein Foto oder viele Farben enthalten?', 'Ja. Die Front wird bedruckt, auch Fotos und Verläufe sind möglich – zum Beispiel wie beim runden Leuchtkasten von Burger Eat.'),
  ('Was ist ein Ausleger?', 'Ein Ausleger ist ein Schild, das quer zur Fassade montiert wird und von beiden Seiten leuchtet. So sehen Passanten Ihr Logo aus beiden Gehrichtungen.'),
  ('Brauche ich eine Genehmigung?', 'Oft ja – abhängig von Größe, Standort und davon, ob der Ausleger über den Gehweg ragt. Wir prüfen die Regeln für Ihren Standort.'),
  ('Wird mein Logo hochgeladen?', 'Nein. Logo und Wandfoto werden nur in Ihrem Browser angezeigt. Wir sehen sie erst, wenn Sie uns die Vorschau selbst schicken.'),
  ('Was kostet ein Leuchtlogo?', 'Sie bekommen einen Festpreis nach Ihrem Entwurf, in der Regel innerhalb von 24 Stunden. Der Preis hängt von Größe, Ausführung, Montage und Genehmigung ab.'),
 ],
 links=[('/leuchtbuchstaben-konfigurator.html', 'Leuchtbuchstaben-Konfigurator'), ('/leuchtreklame-berlin.html', 'Leuchtreklame Berlin'), ('/referenzen.html', 'Referenzen'),
        ('/grafikdesign-berlin.html', 'Logo-Design'), ('/blog/aussenwerbung-berlin-ratgeber.html', 'Ratgeber Genehmigung')],
 form_opts=['Leuchtlogo rund', 'Leuchtlogo eckig', 'Ausleger (doppelseitig)', 'Noch offen – bitte beraten'],
 form_labels=('Welche Ausführung?', 'Größe, Ort &amp; Wunsch', 'Vorschau, Logo oder Wandfoto', 'Mit „Festpreis-Angebot anfordern“ in der Vorschau wird das Bild hier automatisch angehängt. Ihr Logo können Sie zusätzlich mitschicken.'),
 form_sub='Ihr Entwurf aus der Vorschau wird automatisch eingetragen. Ergänzen Sie Ihre Kontaktdaten – Sie bekommen ein Festpreis-Angebot, in der Regel innerhalb von 24 Stunden.',
 subject='Anfrage Leuchtlogo (Website)', msg_ph='z. B. runder Ausleger Ø 60 cm über dem Eingang, Berlin-Wedding, Strom vorhanden',
 sticky=('Leuchtlogo', 'Logo hochladen, Tag & Nacht ansehen'))

APP = {"@context": "https://schema.org", "@type": "WebApplication", "name": "Leuchtlogo-Vorschau",
       "url": "https://masar-werbeagentur.de/leuchtlogo-berlin.html", "applicationCategory": "DesignApplication",
       "operatingSystem": "Web-Browser", "inLanguage": "de", "isAccessibleForFree": True,
       "description": "Eigenes Logo hochladen und als runden oder eckigen Leuchtkasten bei Tag und Nacht an der Wand ansehen.",
       "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}, "provider": {"@id": "https://masar-werbeagentur.de/#identity"}}

if __name__ == '__main__':
    f, n = build_f(P)
    path = ROOT + f
    s = open(path, encoding='utf-8').read()
    s = s.replace('<section class="section" id="preise">', '<section class="section" id="vorschau">', 1)
    s = s.replace('<a href="#kontakt" class="btn btn-teal">Angebot anfordern</a>', '<a href="#vorschau" class="btn btn-teal">Mein Logo ansehen</a>', 1)
    s = s.replace('Kostenloses Angebot <em>anfordern</em>', 'Festpreis-Angebot <em>für Ihr Leuchtlogo</em>', 1)
    s = s.replace('</head>', LCSS + '\n<script type="application/ld+json">\n' + json.dumps(APP, ensure_ascii=False, indent=2) + '\n</script>\n</head>', 1)
    s = s.replace('</body>', '<script src="/leuchtlogo.js?v=3" defer></script>\n</body>', 1)
    open(path, 'w', encoding='utf-8').write(s)
    print(f, len(s))
