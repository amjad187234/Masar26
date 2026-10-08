/*
 * Anfrage-Assistent: in drei Klicks zur passenden Leistung und zur fertigen Anfrage.
 * Einbau: <div data-assistent></div>  (optional data-start="fensterfolie" überspringt Schritt 1)
 * Preise: nur „ab“-Preise, die so auch auf den jeweiligen Leistungsseiten stehen (netto).
 * Es werden keine Daten gespeichert oder verschickt – der Besucher sendet selbst per WhatsApp oder E-Mail.
 */
(function () {
  var roots = document.querySelectorAll('[data-assistent]');
  if (!roots.length) return;

  var WA = '491785143918';
  var MAIL = 'info@masar-werbeagentur.de';

  // Thema → Frage → Antworten [Text, Ziel-Seite, ab-Preis netto oder null, Hinweis]
  var T = {
    fensterfolie: { name: 'Fensterfolie', icon: 'M3 3h18v18H3zM3 12h18M12 3v18', q: 'Was stört Sie am Fenster?', a: [
      ['Hitze und Sonne', '/sonnenschutzfolie-berlin.html', null, 'Sonnenschutzfolie – wir prüfen vorher Ihr Glas und nennen nach Fotos einen Festpreis.', 'Sonnenschutzfolie'],
      ['Einblicke von außen', '/sichtschutzfolie-berlin.html', 190, 'Sichtschutz- oder Milchglasfolie – blickdicht, aber hell.', 'Sichtschutzfolie'],
      ['Glasbruch / Sicherheit', '/sicherheitsfolie-berlin.html', null, 'Splitterschutz- oder durchwurfhemmende Folie – Preis nach Prüfklasse und Fläche.', 'Sicherheitsfolie'],
      ['Glastür markieren', '/blog/glastueren-kennzeichnen.html', null, 'Markierung in zwei Höhen – als Streifen oder mit Ihrem Logo.', 'Glasmarkierung'],
      ['Werbung aufs Glas', '/schaufensterbeschriftung-berlin.html', 149, 'Schaufensterbeschriftung mit Logo, Leistungen und Öffnungszeiten.', 'Schaufensterbeschriftung']
    ]},
    schaufenster: { name: 'Schaufenster', icon: 'M3 4h18v12H3zM8 20h8M12 16v4', q: 'Was soll aufs Schaufenster?', a: [
      ['Logo & Öffnungszeiten', '/schaufensterbeschriftung-berlin.html', 149, 'Klassische Beschriftung aus Folie – sauber, langlebig, wieder entfernbar.', 'Schaufensterbeschriftung'],
      ['Vollflächiger Druck', '/schaufensterbeschriftung-berlin.html', null, 'Bedruckte Folie oder Lochfolie – Preis nach Fläche.', 'Bedruckte Schaufensterfolie'],
      ['Sichtschutz mit Logo', '/sichtschutzfolie-berlin.html', 190, 'Milchglas mit ausgespartem Logo oder Muster.', 'Milchglas mit Logo'],
      ['Aktion / Saison-Deko', '/schaufensterbeschriftung-berlin.html', 190, 'Temporäre Beklebung für Eröffnung, Sale oder Feiertage.', 'Saisonale Deko-Folie']
    ]},
    fahrzeug: { name: 'Fahrzeug', icon: 'M2.5 16V6.5h11V16M13.5 9.5h3.8l3.2 3.2V16h-7', q: 'Was für ein Fahrzeug?', a: [
      ['PKW', '/fahrzeugbeschriftung-berlin.html', 290, 'Beschriftung mit Logo, Leistungen und Kontakt.', 'Fahrzeugbeschriftung PKW'],
      ['Transporter', '/fahrzeugbeschriftung-berlin.html', 290, 'Mehr Fläche, mehr Wirkung – Preis nach Umfang.', 'Transporter-Beschriftung'],
      ['LKW / Sattelzug', '/lkw-beschriftung-berlin.html', null, 'Fahrerhaus, Kofferaufbau oder Plane – Montage bei Ihnen vor Ort, Festpreis nach Fotos.', 'LKW-Beschriftung'],
      ['Mehrere Fahrzeuge', '/fahrzeugbeschriftung-berlin.html', 290, 'Einheitliches Design für die ganze Flotte.', 'Flottenbeschriftung'],
      ['Vollfolierung', '/fahrzeugbeschriftung-berlin.html', null, 'Komplette Folierung – Preis nach Fahrzeug und Folie.', 'Fahrzeug-Vollfolierung']
    ]},
    schild: { name: 'Schild & Leuchtreklame', icon: 'M9 18h6M10 21h4M12 3a6 6 0 0 0-3.6 10.8c.5.4.8 1 .9 1.6l.1.6h5.2l.1-.6c.1-.6.4-1.2.9-1.6A6 6 0 0 0 12 3Z', q: 'Was brauchen Sie?', a: [
      ['Firmen- oder Türschild', '/schilder-berlin.html', 45, 'Alu-Dibond, Acryl oder Edelstahl – passend zum Eingang.', 'Firmen- & Türschilder'],
      ['Leuchtreklame außen', '/leuchtreklame-berlin.html', null, 'Leuchtbuchstaben oder Leuchtkasten – Preis nach Größe und Montage.', 'Leuchtreklame'],
      ['LED-Neon innen', '/leuchtreklame-berlin.html', 249, 'Schriftzug oder Logo für Wand oder Schaufenster, inkl. Entwurf.', 'LED-Neon-Schriftzug'],
      ['Praxis- oder Kanzleischild', '/praxisbeschilderung-berlin.html', null, 'Schild, Türschild und Sichtschutz – auch als Paket.', 'Praxis- & Kanzleischild']
    ]},
    druck: { name: 'Druck & Aufkleber', icon: 'M6 3h12v6H6zM6 14H4a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2h-2M6 14h12v7H6z', q: 'Was soll gedruckt werden?', a: [
      ['Flyer & Visitenkarten', '/print.html', null, 'Druck mit Gestaltung – Preis nach Auflage und Papier.', 'Flyer & Visitenkarten'],
      ['Aufkleber & Folien', '/foliendruck-berlin.html', 45, 'Klebefolie, Aufkleber und Bodenkleber.', 'Foliendruck & Aufkleber'],
      ['Banner & Roll-ups', '/messebeschriftung-berlin.html', null, 'Für Messe, Event und Ladenlokal.', 'Banner & Roll-ups'],
      ['Express – heute noch', '/express-druck-berlin.html', null, 'Druck und Folie am selben Tag in Berlin.', 'Expressdruck']
    ]},
    design: { name: 'Logo & Design', icon: 'M16.5 3.5a2.1 2.1 0 0 1 3 3L8 18l-4 1 1-4ZM14.5 5.5l3 3', q: 'Was soll gestaltet werden?', a: [
      ['Logo', '/grafikdesign-berlin.html', 490, 'Logo-Design mit druckfertigen Dateien.', 'Logo-Design'],
      ['Corporate Design', '/grafikdesign-berlin.html', null, 'Logo, Farben, Schriften und Vorlagen aus einem Guss.', 'Corporate Design'],
      ['Speisekarte / Menütafel', '/digital-signage-berlin.html', null, 'Gedruckt oder digital auf Bildschirmen.', 'Speisekarte & Menütafel'],
      ['Social-Media-Design', '/digital.html', null, 'Posts, Reels und Vorlagen im eigenen Look.', 'Social-Media-Design']
    ]},
    web: { name: 'Website & Social Media', icon: 'M3 12h18M12 3a14 14 0 0 1 0 18 14 14 0 0 1 0-18Z', q: 'Was planen Sie?', a: [
      ['Neue Website', '/webdesign-berlin.html', null, 'Programmiert oder mit WordPress – Preis nach Umfang.', 'Website'],
      ['Online-Shop', '/webdesign-berlin.html', null, 'Shop mit Zahlung und Versand.', 'Online-Shop'],
      ['Social Media betreuen', '/digital.html', null, 'Posts und Reels für Instagram und TikTok.', 'Social-Media-Betreuung'],
      ['Website überarbeiten', '/webdesign-berlin.html', null, 'Schneller, barrierearm, besser bei Google.', 'Website-Relaunch']
    ]},
    messe: { name: 'Messe', icon: 'M3 21h18M5 21V8l7-4 7 4v13M9 21v-6h6v6', berlin: true, q: 'Was brauchen Sie für die Messe?', a: [
      ['Kompletter Messestand', '/messebau-berlin.html', null, 'Konzept, 3D-Entwurf, Bau sowie Auf- und Abbau.', 'Messebau'],
      ['Messewand & Roll-ups', '/messebeschriftung-berlin.html', null, 'Mobile Displays für Messe und Event.', 'Messewand & Roll-ups'],
      ['Messegrafik', '/messebeschriftung-berlin.html', null, 'Grafik für einen bestehenden Stand.', 'Messegrafik']
    ]}
  };
  var WER = ['Firma', 'Privat'];
  var WANN = ['So schnell wie möglich', 'In den nächsten Wochen', 'Erst mal Preis-Info'];

  var css = ''
    + '.as{max-width:860px;margin:0 auto;background:#fff;border:1px solid var(--border,#e0eaea);border-radius:16px;padding:1.6rem;box-shadow:0 10px 30px rgba(19,46,80,.07);text-align:left}'
    + '.as-top{display:flex;align-items:center;justify-content:space-between;gap:1rem;margin-bottom:1.1rem;flex-wrap:wrap}'
    + '.as-steps{display:flex;gap:.4rem}.as-dot{width:34px;height:6px;border-radius:3px;background:#e0eaea}.as-dot.on{background:var(--teal,#58d0bd)}'
    + '.as-step{font:700 13px Barlow,sans-serif;letter-spacing:1.2px;text-transform:uppercase;color:var(--teal-ink,#177567)}'
    + '.as-q{font:900 clamp(1.4rem,3vw,1.9rem)/1.1 "Barlow Condensed",sans-serif;text-transform:uppercase;color:var(--navy,#132e50);margin:0 0 1.1rem;outline:none}'
    + '.as-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:.7rem}'
    + '.as-opt{display:flex;align-items:center;gap:.7rem;width:100%;text-align:left;background:#f4f7f7;border:2px solid transparent;border-radius:12px;padding:.95rem 1rem;font:600 15.5px/1.3 Barlow,sans-serif;color:var(--navy,#132e50);cursor:pointer;transition:border-color .15s,background .15s,transform .15s;min-height:56px}'
    + '.as-opt:hover{border-color:var(--teal,#58d0bd);background:#e8f8f5;transform:translateY(-1px)}'
    + '.as-opt[aria-pressed="true"]{border-color:var(--teal,#58d0bd);background:#e8f8f5}'
    + '.as-opt svg{width:22px;height:22px;flex-shrink:0;fill:none;stroke:var(--teal-ink,#177567);stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}'
    + '.as-sub{font:700 14px Barlow,sans-serif;color:var(--navy,#132e50);margin:1.2rem 0 .55rem}'
    + '.as-row{display:flex;flex-wrap:wrap;gap:.5rem}.as-row .as-opt{width:auto;min-height:44px;padding:.6rem 1rem}'
    + '.as-in{width:100%;font:16px Barlow,sans-serif;border:1px solid var(--border,#e0eaea);border-radius:8px;padding:12px 14px;margin-top:.2rem}'
    + '.as-nav{display:flex;justify-content:space-between;gap:.8rem;margin-top:1.4rem;flex-wrap:wrap}'
    + '.as-back{background:none;border:0;color:var(--muted,#5a7070);font:600 14px Barlow,sans-serif;cursor:pointer;padding:.6rem 0;text-decoration:underline}'
    + '.as-go{background:var(--navy,#132e50);color:#fff;border:0;border-radius:8px;padding:13px 22px;font:700 15px Barlow,sans-serif;cursor:pointer}.as-go[disabled]{opacity:.4;cursor:not-allowed}'
    + '.as-res{border-radius:12px;background:linear-gradient(135deg,#132e50,#0e2340);color:#fff;padding:1.4rem}'
    + '.as-res h4{font:900 1.6rem/1.05 "Barlow Condensed",sans-serif;text-transform:uppercase;margin:.2rem 0 .5rem;color:#fff}'
    + '.as-res p{color:rgba(255,255,255,.82);line-height:1.6;margin:0 0 .6rem;font-size:15px}'
    + '.as-price{display:inline-block;background:rgba(88,208,189,.16);border:1px solid rgba(88,208,189,.45);color:#58d0bd;font:700 14px Barlow,sans-serif;padding:5px 12px;border-radius:6px;margin:.2rem 0 .7rem}'
    + '.as-sum{background:rgba(255,255,255,.07);border-radius:8px;padding:.8rem 1rem;font-size:14px;line-height:1.6;color:rgba(255,255,255,.85);margin:.6rem 0 1rem}'
    + '.as-btns{display:flex;flex-wrap:wrap;gap:.6rem}'
    + '.as-btn{display:inline-flex;align-items:center;gap:.5rem;border-radius:8px;padding:13px 20px;font:700 15px Barlow,sans-serif;text-decoration:none;cursor:pointer}'
    + '.as-wa{background:#25d366;color:#08331a}.as-mail{background:#fff;color:#132e50}.as-page{border:1.5px solid rgba(255,255,255,.35);color:#fff}'
    + '.as-btn:hover{filter:brightness(1.05);transform:translateY(-1px)}'
    + '.as-hint{font-size:13px;color:rgba(255,255,255,.6);margin-top:.9rem}'
    + '@media(max-width:520px){.as{padding:1.1rem}.as-grid{grid-template-columns:1fr 1fr}.as-opt{font-size:14.5px;padding:.8rem .75rem}.as-btn{width:100%;justify-content:center}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  function ico(d) { return '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="' + d + '"/></svg>'; }
  function eur(n) { return n.toLocaleString('de-DE', { minimumFractionDigits: 0, maximumFractionDigits: 2 }) + ' €'; }
  function brutto(n) { return (Math.round(n * 119) / 100).toLocaleString('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' €'; }
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }

  Array.prototype.forEach.call(roots, function (root, idx) {
    var nrw = root.getAttribute('data-region') === 'nrw';
    var start = root.getAttribute('data-start');
    var s = { thema: T[start] ? start : null, wahl: null, wer: null, wann: null, ort: '' };
    var step = s.thema ? 2 : 1;
    var minStep = step;
    var box = el('div', 'as'); root.appendChild(box);
    var live = el('p', 'hp'); live.setAttribute('aria-live', 'polite'); live.style.cssText = 'position:absolute;left:-9999px'; root.appendChild(live);

    function render(focus) {
      var total = 4 - minStep, n = step - minStep + 1;
      box.innerHTML = '';
      var top = el('div', 'as-top');
      var dots = el('div', 'as-steps');
      for (var i = 1; i <= total; i++) dots.appendChild(el('span', 'as-dot' + (i <= n ? ' on' : '')));
      top.appendChild(el('span', 'as-step', n <= total ? 'Schritt ' + n + ' von ' + total : 'Ihre Empfehlung'));
      top.appendChild(dots);
      box.appendChild(top);

      if (step === 1) {
        box.appendChild(head('Worum geht es?'));
        var g = el('div', 'as-grid');
        Object.keys(T).forEach(function (k) {
          if (nrw && T[k].berlin) return;
          g.appendChild(opt(ico(T[k].icon) + '<span>' + T[k].name + '</span>', s.thema === k, function () { s.thema = k; s.wahl = null; step = 2; render(true); }));
        });
        box.appendChild(g);
      } else if (step === 2) {
        var t = T[s.thema];
        box.appendChild(head(t.q));
        var g2 = el('div', 'as-grid');
        t.a.forEach(function (a, i) {
          g2.appendChild(opt('<span>' + a[0] + '</span>', s.wahl === i, function () { s.wahl = i; step = 3; render(true); }));
        });
        box.appendChild(g2);
        nav(step > minStep, null);
      } else if (step === 3) {
        box.appendChild(head('Fast fertig'));
        box.appendChild(el('p', 'as-sub', 'Für wen?'));
        box.appendChild(row(WER, 'wer'));
        box.appendChild(el('p', 'as-sub', 'Wann?'));
        box.appendChild(row(WANN, 'wann'));
        var lab = el('label', 'as-sub', 'Ort oder Bezirk <span style="font-weight:400;color:var(--muted,#5a7070)">(optional)</span>');
        var id = 'as-ort-' + idx; lab.setAttribute('for', id); lab.style.display = 'block';
        var inp = el('input', 'as-in'); inp.id = id; inp.type = 'text'; inp.autocomplete = 'address-level2'; inp.placeholder = 'z. B. Berlin-Wedding'; inp.value = s.ort;
        inp.addEventListener('input', function () { s.ort = inp.value.slice(0, 60); });
        box.appendChild(lab); box.appendChild(inp);
        nav(true, s.wer && s.wann ? function () { step = 4; render(true); } : null, true);
      } else {
        result();
        nav(true, null);
      }
      if (focus) { var h = box.querySelector('.as-q, .as-res h4'); if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); live.textContent = h.textContent; } }
      if (focus) { var navH = (document.querySelector('nav') || {}).offsetHeight || 0; var top = root.getBoundingClientRect().top; if (top < navH + 8) window.scrollBy({ top: top - navH - 16, behavior: 'smooth' }); }
    }
    function head(t) { var h = el('h3', 'as-q'); h.textContent = t; return h; }
    function opt(html, on, fn) { var b = el('button', 'as-opt', html); b.type = 'button'; b.setAttribute('aria-pressed', on ? 'true' : 'false'); b.addEventListener('click', fn); return b; }
    function row(list, key) {
      var r = el('div', 'as-row'); r.setAttribute('role', 'group');
      list.forEach(function (v) { r.appendChild(opt(v, s[key] === v, function () { s[key] = v; render(false); var b = box.querySelectorAll('.as-row')[key === 'wer' ? 0 : 1].querySelectorAll('.as-opt')[list.indexOf(v)]; if (b) b.focus(); })); });
      return r;
    }
    function nav(back, next, showNext) {
      var n = el('div', 'as-nav');
      if (back) { var b = el('button', 'as-back', '← Zurück'); b.type = 'button'; b.addEventListener('click', function () { step = Math.max(minStep, step - 1); render(true); }); n.appendChild(b); } else n.appendChild(el('span'));
      if (showNext) { var g = el('button', 'as-go', 'Empfehlung anzeigen →'); g.type = 'button'; if (!next) g.disabled = true; else g.addEventListener('click', next); n.appendChild(g); }
      box.appendChild(n);
    }
    function result() {
      var t = T[s.thema], a = t.a[s.wahl];
      var res = el('div', 'as-res');
      var h = el('h4'); h.textContent = a[4]; res.appendChild(h);
      var p = el('p'); p.textContent = a[3]; res.appendChild(p);
      if (a[2]) res.appendChild(el('span', 'as-price', 'ab ' + eur(a[2]) + ' netto' + (s.wer === 'Privat' ? ' · ' + brutto(a[2]) + ' inkl. MwSt.' : '')));
      else res.appendChild(el('span', 'as-price', 'Festpreis nach Fotos oder Aufmaß'));
      var lines = ['Thema: ' + t.name + ' – ' + a[0], 'Für: ' + s.wer, 'Zeitrahmen: ' + s.wann];
      if (s.ort.trim()) lines.push('Ort: ' + s.ort.trim());
      var sum = el('div', 'as-sum'); sum.innerHTML = '<strong style="color:#fff">Ihre Anfrage:</strong><br>'; lines.forEach(function (l, i) { sum.appendChild(document.createTextNode(l)); if (i < lines.length - 1) sum.appendChild(document.createElement('br')); });
      res.appendChild(sum);
      var msg = 'Hallo Masar Werbeagentur,\n\nich interessiere mich für: ' + t.name + ' – ' + a[0] + '\nFür: ' + s.wer + '\nZeitrahmen: ' + s.wann + (s.ort.trim() ? '\nOrt: ' + s.ort.trim() : '') + '\n\nIch schicke Ihnen gleich Fotos bzw. Unterlagen.\n\nViele Grüße';
      var btns = el('div', 'as-btns');
      var w = el('a', 'as-btn as-wa', '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8 8 0 0 1-11.6 7.1L4 20.5l1.9-5.1A8 8 0 1 1 21 11.5Z"/></svg>Per WhatsApp senden');
      w.href = 'https://wa.me/' + WA + '?text=' + encodeURIComponent(msg); w.target = '_blank'; w.rel = 'noopener noreferrer';
      var m = el('a', 'as-btn as-mail', 'Per E-Mail senden');
      m.href = 'mailto:' + MAIL + '?subject=' + encodeURIComponent('Anfrage: ' + t.name + ' – ' + a[0]) + '&body=' + encodeURIComponent(msg);
      btns.appendChild(w); btns.appendChild(m);
      if (location.pathname !== a[1]) { var pg = el('a', 'as-btn as-page', 'Mehr dazu →'); pg.href = a[1]; btns.appendChild(pg); }
      res.appendChild(btns);
      res.appendChild(el('p', 'as-hint', 'Tipp: Hängen Sie in WhatsApp direkt Fotos von Fenster, Fassade oder Fahrzeug an – dann bekommen Sie Ihr Angebot schneller. Antwort in der Regel innerhalb von 24 Stunden.'));
      box.appendChild(res);
    }
    render(false);
  });
})();
