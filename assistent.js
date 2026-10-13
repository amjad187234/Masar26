/*
 * Anfrage-Assistent (Version 2): in wenigen Klicks zur fertigen Anfrage.
 * Ablauf: Leistung → Auswahl → Details → Zeitrahmen & Ort → Kontakt → Zusammenfassung → Senden.
 * Senden: per WhatsApp (vorausgefüllte Nachricht) oder per E-Mail (Formular an /kontakt.php, optional mit Foto).
 *
 * Einbau:  <div data-assistent></div>
 *   data-start="fensterfolie"     startet mit einer Leistung (Schritt 1 entfällt)
 *   data-start="schild:1"         startet mit Leistung und Auswahl (Schritt 1 und 2 entfallen)
 *   data-region="nrw"             NRW-Preise und NRW-Seiten, ohne Berlin-only-Leistungen
 *   data-ort="Bernau"             Ort vorbelegen
 * Von außen öffnen: <a href="#..." data-as-open="schild:0">  oder  window.MasarAssistent.open('schild', 0)
 * Preise: nur „ab“-Preise, die so auch auf den Leistungsseiten stehen (netto).
 * Zwischenstand bleibt nur in dieser Browser-Sitzung (sessionStorage), es wird nichts ohne Klick verschickt.
 */
(function () {
  var roots = document.querySelectorAll('[data-assistent]');
  if (!roots.length) return;

  var WA = '491785143918';

  // a: [Auswahl, Seite Berlin, ab-Preis Berlin, Hinweis, Titel, ab-Preis NRW, Einheit, Seite NRW]
  var T = {
    schild: { name: 'Schild & Leuchtreklame', icon: 'M9 18h6M10 21h4M12 3a6 6 0 0 0-3.6 10.8c.5.4.8 1 .9 1.6l.1.6h5.2l.1-.6c.1-.6.4-1.2.9-1.6A6 6 0 0 0 12 3Z', q: 'Was brauchen Sie?', a: [
      ['Firmen- oder Türschild', '/schilder-berlin.html', 45, 'Alu-Dibond, Acryl oder Edelstahl – passend zum Eingang.', 'Firmen- & Türschilder', 59, '', '/schilder-nrw.html'],
      ['Leuchtreklame außen', '/leuchtreklame-berlin.html', 199, 'Leuchtbuchstaben oder Leuchtkasten – Preis nach Größe und Montage.', 'Leuchtreklame', 229, ' / Buchstabe', '/leuchtreklame-nrw.html'],
      ['LED-Neon innen', '/leuchtreklame-berlin.html', 249, 'Schriftzug oder Logo für Wand oder Schaufenster, inkl. Entwurf.', 'LED-Neon-Schriftzug', null, '', '/leuchtreklame-nrw.html'],
      ['Praxis- oder Kanzleischild', '/praxisbeschilderung-berlin.html', null, 'Schild, Türschild und Sichtschutz – auch als Paket.', 'Praxis- & Kanzleischild', null, '', '/schilder-nrw.html']
    ], d: ['Wo soll es hin?', ['Innen', 'Außen an der Fassade', 'Noch unklar']] },
    schaufenster: { name: 'Schaufenster', icon: 'M3 4h18v12H3zM8 20h8M12 16v4', q: 'Was soll aufs Schaufenster?', a: [
      ['Logo & Öffnungszeiten', '/schaufensterbeschriftung-berlin.html', 149, 'Klassische Beschriftung aus Folie – sauber, langlebig, wieder entfernbar.', 'Schaufensterbeschriftung', 179, '', '/schaufensterbeschriftung-nrw.html'],
      ['Vollflächiger Druck', '/schaufensterbeschriftung-berlin.html', null, 'Bedruckte Folie oder Lochfolie – Preis nach Fläche.', 'Bedruckte Schaufensterfolie', null, '', '/schaufensterbeschriftung-nrw.html'],
      ['Sichtschutz mit Logo', '/sichtschutzfolie-berlin.html', 190, 'Milchglas mit ausgespartem Logo oder Muster.', 'Milchglas mit Logo', 229, '', '/fensterfolie-nrw.html'],
      ['Aktion / Eröffnung', '/schaufensterbeschriftung-berlin.html', 190, 'Temporäre Beklebung für Eröffnung, Sale oder Feiertage.', 'Aktions- & Eröffnungsfolie', 229, '', '/schaufensterbeschriftung-nrw.html']
    ], d: ['Wie groß ist die Fläche?', ['1 Scheibe', '2–3 Scheiben', 'Ganze Ladenfront']] },
    fahrzeug: { name: 'Fahrzeug', icon: 'M2.5 16V6.5h11V16M13.5 9.5h3.8l3.2 3.2V16h-7', q: 'Was für ein Fahrzeug?', a: [
      ['PKW', '/fahrzeugbeschriftung-berlin.html', 290, 'Beschriftung mit Logo, Leistungen und Kontakt.', 'Fahrzeugbeschriftung PKW', 340, '', '/fahrzeugbeschriftung-nrw.html'],
      ['Transporter', '/fahrzeugbeschriftung-berlin.html', 290, 'Mehr Fläche, mehr Wirkung – Preis nach Umfang.', 'Transporter-Beschriftung', 340, '', '/fahrzeugbeschriftung-nrw.html'],
      ['LKW / Sattelzug', '/lkw-beschriftung-berlin.html', null, 'Fahrerhaus, Kofferaufbau oder Plane – Montage bei Ihnen, Festpreis nach Fotos.', 'LKW-Beschriftung', null, '', '/lkw-beschriftung-nrw.html'],
      ['Vollfolierung', '/fahrzeugbeschriftung-berlin.html', null, 'Komplette Folierung – Preis nach Fahrzeug und Folie.', 'Fahrzeug-Vollfolierung', null, '', '/fahrzeugbeschriftung-nrw.html']
    ], d: ['Wie viele Fahrzeuge?', ['1', '2–5', '6 oder mehr']] },
    fensterfolie: { name: 'Fensterfolie', icon: 'M3 3h18v18H3zM3 12h18M12 3v18', q: 'Was stört Sie am Fenster?', a: [
      ['Hitze und Sonne', '/sonnenschutzfolie-berlin.html', null, 'Sonnenschutzfolie – wir prüfen vorher Ihr Glas und nennen nach Fotos einen Festpreis.', 'Sonnenschutzfolie', null, '', '/fensterfolie-nrw.html'],
      ['Einblicke von außen', '/sichtschutzfolie-berlin.html', 190, 'Sichtschutz- oder Milchglasfolie – blickdicht, aber hell.', 'Sichtschutzfolie', 229, '', '/fensterfolie-nrw.html'],
      ['Glasbruch / Sicherheit', '/sicherheitsfolie-berlin.html', null, 'Splitterschutz- oder durchwurfhemmende Folie – Preis nach Prüfklasse und Fläche.', 'Sicherheitsfolie', null, '', '/fensterfolie-nrw.html'],
      ['Glastür markieren', '/blog/glastueren-kennzeichnen.html', null, 'Markierung in zwei Höhen – als Streifen oder mit Ihrem Logo.', 'Glasmarkierung', null, '', '/blog/glastueren-kennzeichnen.html'],
      ['Werbung aufs Glas', '/schaufensterbeschriftung-berlin.html', 149, 'Schaufensterbeschriftung mit Logo, Leistungen und Öffnungszeiten.', 'Schaufensterbeschriftung', 179, '', '/schaufensterbeschriftung-nrw.html']
    ], d: ['Wie viele Fenster?', ['1', '2–4', '5–10', 'Mehr als 10']] },
    druck: { name: 'Druck & Banner', icon: 'M6 3h12v6H6zM6 14H4a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2h-2M6 14h12v7H6z', q: 'Was soll gedruckt werden?', a: [
      ['Flyer & Visitenkarten', '/print.html', null, 'Druck mit Gestaltung – Preis nach Auflage und Papier.', 'Flyer & Visitenkarten', null, '', '/print.html'],
      ['PVC-Banner', '/pvc-banner-berlin.html', 19, 'Wetterfest, mit oder ohne Ösen, Mesh für Gerüst und Bauzaun.', 'PVC-Banner', 22, ' / m²', '/pvc-banner-nrw.html'],
      ['Aufkleber & Folien', '/foliendruck-berlin.html', 45, 'Klebefolie, Aufkleber und Bodenkleber.', 'Foliendruck & Aufkleber', null, '', '/foliendruck-berlin.html'],
      ['Roll-ups & Messewände', '/messebeschriftung-berlin.html', null, 'Für Messe, Event und Ladenlokal.', 'Roll-ups & Displays', null, '', '/messebeschriftung-berlin.html'],
      ['Express – heute noch', '/express-druck-berlin.html', null, 'Druck und Folie am selben Tag in Berlin.', 'Expressdruck', null, '', null]
    ], d: ['Welche Menge?', ['Einzelstück', 'bis 250 Stück', '250–1.000 Stück', 'mehr als 1.000']] },
    design: { name: 'Logo & Design', icon: 'M16.5 3.5a2.1 2.1 0 0 1 3 3L8 18l-4 1 1-4ZM14.5 5.5l3 3', q: 'Was soll gestaltet werden?', a: [
      ['Logo', '/grafikdesign-berlin.html', 490, 'Logo-Design mit druckfertigen Dateien.', 'Logo-Design', 490, '', '/grafikdesign-berlin.html'],
      ['Corporate Design', '/grafikdesign-berlin.html', 790, 'Logo, Farben, Schriften und Vorlagen aus einem Guss.', 'Corporate Design', 790, '', '/grafikdesign-berlin.html'],
      ['Speisekarte / Menütafel', '/digital-signage-berlin.html', null, 'Gedruckt oder digital auf Bildschirmen.', 'Speisekarte & Menütafel', null, '', '/digital-signage-berlin.html'],
      ['Social-Media-Design', '/digital.html', null, 'Posts, Reels und Vorlagen im eigenen Look.', 'Social-Media-Design', null, '', '/digital.html']
    ], d: ['Was gibt es schon?', ['Noch nichts', 'Ein altes Logo', 'Fertiges Logo']] },
    web: { name: 'Website & Social Media', icon: 'M3 12h18M12 3a14 14 0 0 1 0 18 14 14 0 0 1 0-18Z', q: 'Was planen Sie?', a: [
      ['Neue Website', '/webdesign-berlin.html', null, 'Schnell, mobil und gut bei Google – Festpreis nach Umfang.', 'Website', null, '', '/webdesign-nrw.html'],
      ['Website überarbeiten', '/webdesign-berlin.html', null, 'Schneller, barrierearm, besser bei Google.', 'Website-Relaunch', null, '', '/webdesign-nrw.html'],
      ['Online-Shop', '/webdesign-berlin.html', null, 'Shop mit Zahlung und Versand.', 'Online-Shop', null, '', '/webdesign-nrw.html'],
      ['Social Media betreuen', '/digital.html', 490, 'Posts und Reels für Instagram, Facebook und TikTok.', 'Social-Media-Betreuung', 490, ' / Monat', '/digital.html']
    ], d: ['Was gibt es schon?', ['Noch keine Website', 'Eine alte Website', 'Nur Social Media']] },
    messe: { name: 'Messe', icon: 'M3 21h18M5 21V8l7-4 7 4v13M9 21v-6h6v6', berlin: true, q: 'Was brauchen Sie für die Messe?', a: [
      ['Kompletter Messestand', '/messebau-berlin.html', null, 'Konzept, 3D-Entwurf, Bau sowie Auf- und Abbau.', 'Messebau', null, '', null],
      ['Messewand & Roll-ups', '/messebeschriftung-berlin.html', null, 'Mobile Displays für Messe und Event.', 'Messewand & Roll-ups', null, '', null],
      ['Messegrafik', '/messebeschriftung-berlin.html', null, 'Grafik für einen bestehenden Stand.', 'Messegrafik', null, '', null]
    ], d: ['Wie groß ist der Stand?', ['bis 12 m²', '12–30 m²', 'über 30 m²', 'Noch unklar']] }
  };
  var LOGO = ['Ja, Logo/Daten vorhanden', 'Nein, bitte mitgestalten'];
  var WER = ['Firma', 'Privat'];
  var WANN = ['So schnell wie möglich', 'In den nächsten Wochen', 'Erst mal Preis-Info'];
  var STEPS = ['Leistung', 'Auswahl', 'Details', 'Zeit & Ort', 'Kontakt', 'Prüfen'];

  var css = ''
    + '.as{max-width:860px;margin:0 auto;background:#fff;border:1px solid var(--border,#e0eaea);border-radius:16px;padding:1.6rem;box-shadow:0 10px 30px rgba(19,46,80,.07);text-align:left;scroll-margin-top:96px}'
    + '.as-top{display:flex;align-items:center;justify-content:space-between;gap:1rem;margin-bottom:1.1rem;flex-wrap:wrap}'
    + '.as-bar{flex:1;min-width:140px;height:6px;border-radius:3px;background:#e0eaea;overflow:hidden}.as-bar i{display:block;height:100%;background:var(--teal,#58d0bd);transition:width .3s}'
    + '.as-step{font:700 13px Barlow,sans-serif;letter-spacing:1.2px;text-transform:uppercase;color:var(--teal-ink,#177567)}'
    + '.as-chip{display:inline-flex;align-items:center;gap:.4rem;background:#e8f8f5;border:1px solid var(--teal,#58d0bd);color:var(--navy,#132e50);border-radius:999px;padding:.3rem .8rem;font:600 13.5px Barlow,sans-serif;margin:0 0 .9rem}'
    + '.as-q{font:900 clamp(1.4rem,3vw,1.9rem)/1.1 "Barlow Condensed",sans-serif;text-transform:uppercase;color:var(--navy,#132e50);margin:0 0 1.1rem;outline:none}'
    + '.as-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:.7rem}'
    + '.as-opt{display:flex;align-items:center;gap:.7rem;width:100%;text-align:left;background:#f4f7f7;border:2px solid transparent;border-radius:12px;padding:.95rem 1rem;font:600 15.5px/1.3 Barlow,sans-serif;color:var(--navy,#132e50);cursor:pointer;transition:border-color .15s,background .15s,transform .15s;min-height:56px}'
    + '.as-opt:hover{border-color:var(--teal,#58d0bd);background:#e8f8f5;transform:translateY(-1px)}'
    + '.as-opt[aria-pressed="true"]{border-color:var(--teal,#58d0bd);background:#e8f8f5}'
    + '.as-opt[aria-pressed="true"]:after{content:"✓";margin-left:auto;color:var(--teal-ink,#177567);font-weight:800}'
    + '.as-opt svg{width:22px;height:22px;flex-shrink:0;fill:none;stroke:var(--teal-ink,#177567);stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}'
    + '.as-sub{display:block;font:700 14px Barlow,sans-serif;color:var(--navy,#132e50);margin:1.2rem 0 .55rem}'
    + '.as-sub small{font-weight:400;color:var(--muted,#5a7070)}'
    + '.as-row{display:flex;flex-wrap:wrap;gap:.5rem}.as-row .as-opt{width:auto;min-height:44px;padding:.6rem 1rem}'
    + '.as-in{width:100%;font:16px Barlow,sans-serif;border:1px solid var(--border,#e0eaea);border-radius:8px;padding:12px 14px;margin-top:.2rem;background:#fff;color:#132e50}'
    + '.as-in:focus{outline:2px solid var(--teal,#58d0bd);outline-offset:1px}'
    + 'textarea.as-in{min-height:90px;resize:vertical}'
    + '.as-two{display:grid;grid-template-columns:1fr 1fr;gap:0 1rem}'
    + '.as-err{color:#b3261e;font-size:13.5px;margin:.4rem 0 0;min-height:1em}'
    + '.as-nav{display:flex;justify-content:space-between;align-items:center;gap:.8rem;margin-top:1.4rem;flex-wrap:wrap}'
    + '.as-back{background:none;border:0;color:var(--muted,#5a7070);font:600 14px Barlow,sans-serif;cursor:pointer;padding:.6rem 0;text-decoration:underline}'
    + '.as-go{background:var(--navy,#132e50);color:#fff;border:0;border-radius:8px;padding:13px 22px;font:700 15px Barlow,sans-serif;cursor:pointer}.as-go[disabled]{opacity:.4;cursor:not-allowed}'
    + '.as-skip{background:none;border:0;color:var(--teal-ink,#177567);font:600 14px Barlow,sans-serif;cursor:pointer;padding:.6rem 0}'
    + '.as-res{border-radius:12px;background:linear-gradient(135deg,#132e50,#0e2340);color:#fff;padding:1.4rem}'
    + '.as-res h4{font:900 1.6rem/1.05 "Barlow Condensed",sans-serif;text-transform:uppercase;margin:.2rem 0 .5rem;color:#fff}'
    + '.as-res p{color:rgba(255,255,255,.82);line-height:1.6;margin:0 0 .6rem;font-size:15px}'
    + '.as-price{display:inline-block;background:rgba(88,208,189,.16);border:1px solid rgba(88,208,189,.45);color:#58d0bd;font:700 14px Barlow,sans-serif;padding:5px 12px;border-radius:6px;margin:.2rem 0 .8rem}'
    + '.as-list{list-style:none;margin:.2rem 0 1rem;padding:0;border-top:1px solid rgba(255,255,255,.12)}'
    + '.as-list li{display:flex;gap:.8rem;align-items:baseline;padding:.55rem 0;border-bottom:1px solid rgba(255,255,255,.12);font-size:14.5px}'
    + '.as-list b{flex:0 0 108px;color:rgba(255,255,255,.6);font-weight:600}.as-list span{flex:1;color:#fff}'
    + '.as-edit{background:none;border:0;color:#58d0bd;font:600 13px Barlow,sans-serif;cursor:pointer;text-decoration:underline;padding:0}'
    + '.as-send{display:grid;grid-template-columns:1fr 1fr;gap:.8rem;margin-top:.4rem}'
    + '.as-card{background:rgba(255,255,255,.07);border-radius:10px;padding:1rem;display:flex;flex-direction:column;gap:.6rem}'
    + '.as-card h5{margin:0;font:700 15px Barlow,sans-serif;color:#fff}.as-card p{margin:0;font-size:13.5px;color:rgba(255,255,255,.7);line-height:1.5}'
    + '.as-btn{display:inline-flex;align-items:center;justify-content:center;gap:.5rem;border:0;border-radius:8px;padding:13px 18px;font:700 15px Barlow,sans-serif;text-decoration:none;cursor:pointer;width:100%;margin-top:auto}'
    + '.as-wa{background:#25d366;color:#08331a}.as-mail{background:#fff;color:#132e50}.as-mail[disabled]{opacity:.5;cursor:not-allowed}'
    + '.as-btn:hover{filter:brightness(1.05)}'
    + '.as-card label{font-size:13px;color:rgba(255,255,255,.8);display:flex;gap:.5rem;align-items:flex-start;line-height:1.45}.as-card label a{color:#58d0bd}'
    + '.as-card input[type=file]{font-size:13px;color:rgba(255,255,255,.8);width:100%}'
    + '.as-hint{font-size:13px;color:rgba(255,255,255,.6);margin:.9rem 0 0}.as-more{color:#58d0bd;font-weight:600}'
    + '@media(max-width:620px){.as{padding:1.1rem}.as-grid{grid-template-columns:1fr 1fr}.as-opt{font-size:14.5px;padding:.8rem .75rem}.as-two,.as-send{grid-template-columns:1fr}.as-list b{flex-basis:88px}.as-nav .as-go{margin-right:64px}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  function ico(d) { return '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="' + d + '"/></svg>'; }
  function eur(n) { return n.toLocaleString('de-DE', { maximumFractionDigits: 2 }) + ' €'; }
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function txt(tag, cls, t) { var e = el(tag, cls); e.textContent = t; return e; }
  function store(k, v) { try { if (v === undefined) return JSON.parse(sessionStorage.getItem(k) || 'null'); sessionStorage.setItem(k, JSON.stringify(v)); } catch (e) { return null; } }

  var api = [];
  window.MasarAssistent = { open: function (thema, wahl) { if (api[0]) api[0](thema, wahl); } };
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('[data-as-open]'); if (!a || !api[0]) return;
    e.preventDefault(); var v = a.getAttribute('data-as-open').split(':'); api[0](v[0], v[1] != null ? +v[1] : null);
  });

  Array.prototype.forEach.call(roots, function (root, idx) {
    var nrw = root.getAttribute('data-region') === 'nrw';
    var sv = (root.getAttribute('data-start') || '').split(':');
    var key = 'masar-as-' + location.pathname + '-' + idx;
    var t0 = String(Date.now());
    var s = store(key) || { thema: null, wahl: null, detail: null, logo: null, info: '', wer: null, wann: null, ort: root.getAttribute('data-ort') || '', name: '', tel: '', mail: '', firma: '' };
    if (T[sv[0]]) { s.thema = sv[0]; if (sv[1] != null && T[sv[0]].a[+sv[1]]) s.wahl = +sv[1]; }
    var minStep = T[sv[0]] ? (sv[1] != null ? 3 : 2) : 1;
    var step = minStep;
    if (s.thema && s.wahl != null && store(key)) step = Math.max(minStep, 3);
    var box = el('div', 'as'); root.appendChild(box);
    var live = el('p'); live.setAttribute('aria-live', 'polite'); live.style.cssText = 'position:absolute;left:-9999px'; root.appendChild(live);

    function A() { return s.thema != null && s.wahl != null ? T[s.thema].a[s.wahl] : null; }
    function price(a) { var p = nrw ? a[5] : a[2]; return p ? 'ab ' + eur(p) + (a[6] || '') + ' netto' : 'Festpreis nach Fotos oder Aufmaß'; }
    function page(a) { return nrw ? a[7] : a[1]; }
    function save() { store(key, s); }

    function render(focus) {
      save();
      box.innerHTML = '';
      var total = 6 - minStep + 1, n = step - minStep + 1;
      var top = el('div', 'as-top');
      top.appendChild(txt('span', 'as-step', step < 6 ? 'Schritt ' + n + ' von ' + (total - 1) + ' · ' + STEPS[step - 1] : 'Zusammenfassung'));
      var bar = el('div', 'as-bar', '<i style="width:' + Math.round(n / total * 100) + '%"></i>'); top.appendChild(bar);
      box.appendChild(top);
      if (step > 2 && A()) box.appendChild(txt('div', 'as-chip', T[s.thema].name + ' · ' + A()[0]));

      if (step === 1) {
        box.appendChild(head('Worum geht es?'));
        var g = el('div', 'as-grid');
        Object.keys(T).forEach(function (k) {
          if (nrw && T[k].berlin) return;
          g.appendChild(opt(ico(T[k].icon) + '<span>' + T[k].name + '</span>', s.thema === k, function () { if (s.thema !== k) { s.wahl = null; s.detail = null; } s.thema = k; go(2); }));
        });
        box.appendChild(g);
        nav(false);
      } else if (step === 2) {
        var t = T[s.thema];
        box.appendChild(head(t.q));
        var g2 = el('div', 'as-grid');
        t.a.forEach(function (a, i) {
          if (nrw && !a[7]) return;
          g2.appendChild(opt('<span>' + a[0] + '</span>', s.wahl === i, function () { s.wahl = i; go(3); }));
        });
        box.appendChild(g2);
        nav(step > minStep);
      } else if (step === 3) {
        var tt = T[s.thema];
        box.appendChild(head('Ein paar Details'));
        box.appendChild(txt('span', 'as-sub', tt.d[0]));
        box.appendChild(row(tt.d[1], 'detail'));
        if (s.thema !== 'design' && s.thema !== 'web') { box.appendChild(txt('span', 'as-sub', 'Gibt es schon ein Logo bzw. Druckdaten?')); box.appendChild(row(LOGO, 'logo')); }
        field('Kurz beschreiben', 'optional', 'info', 'textarea', 'z. B. Maße, Text, Farben, Wunsch – Stichworte reichen.', 500);
        nav(true, function () { return !!s.detail; }, 'Weiter →', 'Bitte eine Antwort zu „' + tt.d[0] + '“ wählen.');
      } else if (step === 4) {
        box.appendChild(head('Wann und wo?'));
        box.appendChild(txt('span', 'as-sub', 'Für wen?')); box.appendChild(row(WER, 'wer'));
        box.appendChild(txt('span', 'as-sub', 'Wann?')); box.appendChild(row(WANN, 'wann'));
        field('Ort oder Bezirk', 'optional', 'ort', 'input', nrw ? 'z. B. Essen-Rüttenscheid' : 'z. B. Berlin-Wedding', 60, 'address-level2');
        nav(true, function () { return s.wer && s.wann; }, 'Weiter →', 'Bitte „Für wen?“ und „Wann?“ wählen.');
      } else if (step === 5) {
        box.appendChild(head('Wie erreichen wir Sie?'));
        var two = el('div', 'as-two'); box.appendChild(two);
        field('Name', 'Pflicht', 'name', 'input', 'Vor- und Nachname', 80, 'name', two);
        field('Firma', 'optional', 'firma', 'input', 'falls gewerblich', 80, 'organization', two);
        field('Telefon / WhatsApp', 'optional', 'tel', 'input', '+49 …', 40, 'tel', two, 'tel');
        field('E-Mail', 'für Antwort per E-Mail', 'mail', 'input', 'info@beispiel.de', 100, 'email', two, 'email');
        nav(true, function () { return s.name.trim().length > 1; }, 'Zur Zusammenfassung →', 'Bitte Ihren Namen eintragen.');
      } else {
        result();
      }
      if (focus) { var h = box.querySelector('.as-q, .as-res h4'); if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); live.textContent = h.textContent; } box.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
    }
    function go(n) { step = n; render(true); }
    function head(t) { var h = el('h3', 'as-q'); h.textContent = t; return h; }
    function opt(html, on, fn) { var b = el('button', 'as-opt', html); b.type = 'button'; b.setAttribute('aria-pressed', on ? 'true' : 'false'); b.addEventListener('click', fn); return b; }
    function row(list, k) {
      var r = el('div', 'as-row'); r.setAttribute('role', 'group');
      list.forEach(function (v) {
        r.appendChild(opt(v, s[k] === v, function () { s[k] = v; save(); Array.prototype.forEach.call(r.children, function (b) { b.setAttribute('aria-pressed', b.textContent === v ? 'true' : 'false'); }); var e = box.querySelector('.as-err'); if (e) e.textContent = ''; }));
      });
      return r;
    }
    function field(label, hint, k, tag, ph, max, ac, parent, type) {
      var wrap = el('div'); var id = 'as-' + k + '-' + idx;
      var lab = el('label', 'as-sub', label + ' <small>(' + hint + ')</small>'); lab.setAttribute('for', id);
      var inp = el(tag, 'as-in'); inp.id = id; if (tag === 'input') inp.type = type || 'text'; inp.placeholder = ph; inp.maxLength = max; inp.value = s[k] || ''; if (ac) inp.autocomplete = ac;
      inp.addEventListener('input', function () { s[k] = inp.value.slice(0, max); save(); });
      wrap.appendChild(lab); wrap.appendChild(inp); (parent || box).appendChild(wrap);
    }
    function nav(back, ok, label, msg) {
      var err = el('p', 'as-err'); err.setAttribute('role', 'alert');
      var n = el('div', 'as-nav');
      if (back) { var b = el('button', 'as-back', '← Zurück'); b.type = 'button'; b.addEventListener('click', function () { go(Math.max(minStep, step - 1)); }); n.appendChild(b); } else n.appendChild(el('span'));
      if (ok) { var g = el('button', 'as-go', label); g.type = 'button'; g.addEventListener('click', function () { if (ok()) go(step + 1); else err.textContent = msg; }); n.appendChild(g); }
      box.appendChild(err); box.appendChild(n);
    }
    function lines() {
      var a = A(), L = [['Leistung', T[s.thema].name + ' – ' + a[0], 2]];
      L.push([T[s.thema].d[0].replace('?', ''), s.detail, 3]);
      if (s.logo) L.push(['Logo/Daten', s.logo, 3]);
      if (s.info.trim()) L.push(['Beschreibung', s.info.trim(), 3]);
      L.push(['Für', s.wer, 4], ['Zeitrahmen', s.wann, 4]);
      if (s.ort.trim()) L.push(['Ort', s.ort.trim(), 4]);
      L.push(['Name', s.name.trim() + (s.firma.trim() ? ' (' + s.firma.trim() + ')' : ''), 5]);
      if (s.tel.trim()) L.push(['Telefon', s.tel.trim(), 5]);
      if (s.mail.trim()) L.push(['E-Mail', s.mail.trim(), 5]);
      return L;
    }
    function result() {
      var a = A(), L = lines();
      var res = el('div', 'as-res');
      var h = el('h4'); h.textContent = 'Ihre Anfrage: ' + a[4]; res.appendChild(h);
      res.appendChild(txt('p', '', a[3]));
      res.appendChild(txt('span', 'as-price', price(a)));
      var ul = el('ul', 'as-list');
      L.forEach(function (l) {
        var li = el('li'); li.appendChild(txt('b', '', l[0])); li.appendChild(txt('span', '', l[1]));
        if (l[2] >= minStep) { var e = el('button', 'as-edit', 'ändern'); e.type = 'button'; e.addEventListener('click', function () { go(l[2]); }); li.appendChild(e); }
        ul.appendChild(li);
      });
      res.appendChild(ul);

      var msg = 'Hallo Masar Werbeagentur,\n\nhier meine Anfrage:\n' + L.map(function (l) { return '• ' + l[0] + ': ' + l[1]; }).join('\n') + '\n\nViele Grüße\n' + s.name.trim();
      var send = el('div', 'as-send');
      // WhatsApp
      var c1 = el('div', 'as-card');
      c1.appendChild(txt('h5', '', 'Per WhatsApp – am schnellsten'));
      c1.appendChild(txt('p', '', 'Die Nachricht ist fertig vorbereitet. Fotos können Sie in WhatsApp direkt anhängen.'));
      var w = el('a', 'as-btn as-wa', '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8 8 0 0 1-11.6 7.1L4 20.5l1.9-5.1A8 8 0 1 1 21 11.5Z"/></svg>WhatsApp öffnen');
      w.href = 'https://wa.me/' + WA + '?text=' + encodeURIComponent(msg); w.target = '_blank'; w.rel = 'noopener noreferrer';
      w.addEventListener('click', function () { try { sessionStorage.removeItem(key); } catch (e) {} });
      c1.appendChild(w); send.appendChild(c1);
      // E-Mail (Formular an kontakt.php)
      var c2 = el('form', 'as-card'); c2.action = '/kontakt.php'; c2.method = 'POST'; c2.enctype = 'multipart/form-data';
      c2.appendChild(txt('h5', '', 'Per E-Mail – mit Foto'));
      var hid = { _subject: 'Anfrage: ' + a[4] + (s.ort.trim() ? ' – ' + s.ort.trim() : '') + ' (Assistent)', _honey: '', _t: t0, name: s.name.trim(), email: s.mail.trim(), telefon: s.tel.trim(), firma: s.firma.trim(), ort: s.ort.trim(), thema: T[s.thema].name, produkt: a[0], beschreibung: s.detail ? T[s.thema].d[0] + ' ' + s.detail : '', design: s.logo || '', wann: s.wann || '', art: s.wer || '', nachricht: s.info.trim() };
      Object.keys(hid).forEach(function (k) { var i = el('input'); i.type = 'hidden'; i.name = k; i.value = hid[k]; if (k === '_honey') { i.type = 'text'; i.style.display = 'none'; i.tabIndex = -1; i.autocomplete = 'off'; } c2.appendChild(i); });
      var fl = el('label', '', 'Foto oder Logo (optional, max. 10 MB)'); var fi = el('input'); fi.type = 'file'; fi.name = 'attachment'; fi.accept = 'image/*,.pdf,.svg,.ai,.eps'; fl.style.flexDirection = 'column'; fl.appendChild(fi); c2.appendChild(fl);
      var cl = el('label'); var cb = el('input'); cb.type = 'checkbox'; cb.name = 'consent';
      cl.appendChild(cb); cl.appendChild(el('span', '', 'Ich stimme der Verarbeitung meiner Daten zur Bearbeitung der Anfrage zu (<a href="/datenschutz.html" target="_blank" rel="noopener">Datenschutz</a>).'));
      c2.appendChild(cl);
      var mb = el('button', 'as-btn as-mail', 'Anfrage per E-Mail senden'); mb.type = 'submit'; c2.appendChild(mb);
      var me = el('p', 'as-err'); me.style.color = '#ffb4ab'; me.setAttribute('role', 'alert'); c2.appendChild(me);
      c2.addEventListener('submit', function (ev) {
        var ok = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(s.mail.trim());
        if (!ok) { ev.preventDefault(); me.innerHTML = 'Für den Versand per E-Mail brauchen wir Ihre E-Mail-Adresse – <button type="button" class="as-edit">jetzt eintragen</button>.'; me.querySelector('button').addEventListener('click', function () { go(5); }); return; }
        if (!cb.checked) { ev.preventDefault(); me.textContent = 'Bitte der Datenverarbeitung zustimmen.'; return; }
        try { sessionStorage.removeItem(key); } catch (e) {}
      });
      send.appendChild(c2);
      res.appendChild(send);
      var pg = page(a);
      var hint = el('p', 'as-hint', 'Antwort in der Regel innerhalb von 24 Stunden.' + (pg && pg !== location.pathname ? ' <a class="as-more" href="' + pg + '">Mehr zu ' + a[4] + ' →</a>' : ''));
      res.appendChild(hint);
      box.appendChild(res);
      var n = el('div', 'as-nav'); var b = el('button', 'as-back', '← Zurück'); b.type = 'button'; b.addEventListener('click', function () { go(5); }); n.appendChild(b);
      var r = el('button', 'as-skip', 'Neue Anfrage starten'); r.type = 'button'; r.addEventListener('click', function () { try { sessionStorage.removeItem(key); } catch (e) {} s = { thema: T[sv[0]] ? sv[0] : null, wahl: null, detail: null, logo: null, info: '', wer: null, wann: null, ort: root.getAttribute('data-ort') || '', name: s.name, tel: s.tel, mail: s.mail, firma: s.firma }; minStep = T[sv[0]] ? 2 : 1; go(minStep); });
      n.appendChild(r); box.appendChild(n);
    }
    api.push(function (thema, wahl) {
      if (!T[thema]) return;
      if (s.thema !== thema || s.wahl !== wahl) { s.detail = null; s.logo = null; }
      s.thema = thema; s.wahl = (wahl != null && T[thema].a[wahl]) ? wahl : null;
      minStep = 1; step = s.wahl != null ? 3 : 2; render(true);
    });
    render(false);
  });
})();
