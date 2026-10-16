/*
 * Masar – Kostenlose Beratung buchen
 * Ablauf: Art → Sprache → Tag & Uhrzeit → Kontakt → Bestätigung
 * Server: /termin.php (freie Zeiten, Buchung). Container: <div data-termin></div>
 */
(function () {
  'use strict';
  var root = document.querySelector('[data-termin]');
  if (!root || root.getAttribute('data-tm-ready')) return;
  root.setAttribute('data-tm-ready', '1');

  var ARTEN = [
    ['telefon', 'Telefon', 'Wir rufen Sie an', 'M6.5 3.5 9 8l-2 2a13 13 0 0 0 7 7l2-2 4.5 2.5-1.4 3.1a2 2 0 0 1-2.2 1.1C10.1 20.4 3.6 13.9 2.3 6.1A2 2 0 0 1 3.4 3.9Z'],
    ['video', 'WhatsApp-Video', 'Sie zeigen uns Fassade, Fenster oder Entwurf', 'M3 7h12v10H3zM15 10l6-3v10l-6-3'],
    ['vorort', 'Vor Ort (Berlin)', 'Wir kommen zu Ihnen, sehen uns alles an und messen', 'M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11Z']
  ];
  var SPRACHEN = [['de', 'Deutsch'], ['en', 'English'], ['ar', 'العربية'], ['tr', 'Türkçe']];
  var THEMEN = ['Leuchtreklame', 'Schilder', 'Schaufenster & Fensterfolie', 'Fahrzeugbeschriftung', 'Banner & Druck', 'Logo & Webdesign', 'Social Media', 'Sonstiges'];
  var TAGE = ['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa'];
  var MON = ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'];
  var STEPS = ['Art', 'Sprache', 'Termin', 'Kontakt'];

  var css = ''
    + '.tm{max-width:860px;margin:0 auto;background:#fff;border:1px solid var(--border,#e0eaea);border-radius:16px;padding:1.6rem;box-shadow:0 10px 30px rgba(19,46,80,.07);text-align:left;scroll-margin-top:96px}'
    + '.tm-top{display:flex;align-items:center;gap:1rem;margin-bottom:1.1rem;flex-wrap:wrap}'
    + '.tm-bar{flex:1;min-width:140px;height:6px;border-radius:3px;background:#e0eaea;overflow:hidden}.tm-bar i{display:block;height:100%;background:var(--teal,#58d0bd);transition:width .3s}'
    + '.tm-step{font:700 13px Barlow,sans-serif;letter-spacing:1.2px;text-transform:uppercase;color:var(--teal-ink,#177567)}'
    + '.tm-q{font:900 clamp(1.4rem,3vw,1.9rem)/1.1 "Barlow Condensed",sans-serif;text-transform:uppercase;color:var(--navy,#132e50);margin:0 0 1.1rem;outline:none}'
    + '.tm-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:.7rem}'
    + '.tm-opt{display:flex;align-items:center;gap:.8rem;width:100%;text-align:left;background:#f4f7f7;border:2px solid transparent;border-radius:12px;padding:1rem;font:600 16px/1.3 Barlow,sans-serif;color:var(--navy,#132e50);cursor:pointer;transition:border-color .15s,background .15s;min-height:56px}'
    + '.tm-opt small{display:block;font-weight:400;font-size:13.5px;color:var(--muted,#5a7070);margin-top:2px}'
    + '.tm-opt:hover,.tm-opt[aria-pressed="true"]{border-color:var(--teal,#58d0bd);background:#e8f8f5}'
    + '.tm-opt svg{width:24px;height:24px;flex-shrink:0;fill:none;stroke:var(--teal-ink,#177567);stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}'
    + '.tm-days{display:flex;gap:.5rem;overflow-x:auto;padding:2px 2px 10px;scroll-snap-type:x proximity}'
    + '.tm-day{flex:0 0 74px;scroll-snap-align:start;background:#f4f7f7;border:2px solid transparent;border-radius:12px;padding:.6rem .3rem;text-align:center;cursor:pointer;font:600 14px/1.25 Barlow,sans-serif;color:var(--navy,#132e50)}'
    + '.tm-day b{display:block;font:900 22px/1.1 "Barlow Condensed",sans-serif}.tm-day small{display:block;font-size:12px;color:var(--muted,#5a7070)}'
    + '.tm-day:hover,.tm-day[aria-pressed="true"]{border-color:var(--teal,#58d0bd);background:#e8f8f5}'
    + '.tm-day[disabled]{opacity:.35;cursor:not-allowed;background:#f4f7f7;border-color:transparent}'
    + '.tm-times{display:grid;grid-template-columns:repeat(auto-fill,minmax(86px,1fr));gap:.5rem;margin-top:.6rem}'
    + '.tm-time{background:#fff;border:2px solid var(--border,#e0eaea);border-radius:10px;padding:.65rem 0;font:700 15px Barlow,sans-serif;color:var(--navy,#132e50);cursor:pointer}'
    + '.tm-time:hover,.tm-time[aria-pressed="true"]{border-color:var(--teal,#58d0bd);background:#e8f8f5}'
    + '.tm-sub{display:block;font:700 14px Barlow,sans-serif;color:var(--navy,#132e50);margin:1.1rem 0 .45rem}.tm-sub small{font-weight:400;color:var(--muted,#5a7070)}'
    + '.tm-in{width:100%;font:16px Barlow,sans-serif;border:1px solid var(--border,#e0eaea);border-radius:8px;padding:12px 14px;background:#fff;color:#132e50}'
    + '.tm-in:focus{outline:2px solid var(--teal,#58d0bd);outline-offset:1px}textarea.tm-in{min-height:84px;resize:vertical}'
    + '.tm-two{display:grid;grid-template-columns:1fr 1fr;gap:0 1rem}'
    + '.tm-chk{display:flex;gap:.55rem;align-items:flex-start;font-size:14px;line-height:1.45;color:var(--muted,#5a7070);margin-top:1rem}.tm-chk input{margin-top:3px;width:18px;height:18px}'
    + '.tm-err{color:#b3261e;font-size:14px;margin:.6rem 0 0;min-height:1em}'
    + '.tm-sum{background:#e8f8f5;border:1px solid var(--teal,#58d0bd);border-radius:10px;padding:.8rem 1rem;font-size:15px;color:var(--navy,#132e50);margin-bottom:1rem}'
    + '.tm-nav{display:flex;justify-content:space-between;align-items:center;gap:.8rem;margin-top:1.4rem;flex-wrap:wrap}'
    + '.tm-back{background:none;border:0;color:var(--muted,#5a7070);font:600 14px Barlow,sans-serif;cursor:pointer;padding:.6rem 0;text-decoration:underline}'
    + '.tm-go{background:var(--navy,#132e50);color:#fff;border:0;border-radius:8px;padding:13px 22px;font:700 15px Barlow,sans-serif;cursor:pointer}.tm-go[disabled]{opacity:.4;cursor:not-allowed}'
    + '.tm-ok{border-radius:12px;background:linear-gradient(135deg,#132e50,#0e2340);color:#fff;padding:1.5rem}'
    + '.tm-ok h4{font:900 1.7rem/1.05 "Barlow Condensed",sans-serif;text-transform:uppercase;margin:.2rem 0 .6rem;color:#fff}'
    + '.tm-ok p{color:rgba(255,255,255,.85);line-height:1.6;margin:0 0 .7rem;font-size:15px}'
    + '.tm-ok .tm-big{font:700 19px Barlow,sans-serif;color:#58d0bd}'
    + '.tm-btns{display:flex;gap:.6rem;flex-wrap:wrap;margin-top:.8rem}'
    + '.tm-btn{display:inline-flex;align-items:center;justify-content:center;border:0;border-radius:8px;padding:12px 18px;font:700 15px Barlow,sans-serif;text-decoration:none;cursor:pointer;background:#fff;color:#132e50}.tm-btn.tm-wa{background:#25d366;color:#08331a}'
    + '.tm-load{color:var(--muted,#5a7070);font-size:14px;margin:.6rem 0}'
    + '@media(max-width:620px){.tm{padding:1.1rem}.tm-two{grid-template-columns:1fr}.tm-nav .tm-go{margin-right:64px}}';
  css += '.tm-ok{animation:masarIn .45s ease both}@keyframes masarIn{from{opacity:0;transform:translateY(10px) scale(.98)}to{opacity:1;transform:none}}@media(prefers-reduced-motion:reduce){.tm-ok{animation:none}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function txt(tag, cls, t) { var e = el(tag, cls); e.textContent = t; return e; }
  function ico(d) { return '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="' + d + '"/></svg>'; }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function datum(tag) { var p = tag.split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function tagText(tag) { var d = datum(tag); return TAGE[d.getDay()] + ', ' + pad(d.getDate()) + '.' + pad(d.getMonth() + 1) + '.' + d.getFullYear(); }
  function artName(k) { for (var i = 0; i < ARTEN.length; i++) if (ARTEN[i][0] === k) return ARTEN[i][1]; return k; }
  function sprName(k) { for (var i = 0; i < SPRACHEN.length; i++) if (SPRACHEN[i][0] === k) return SPRACHEN[i][1]; return k; }

  var t0 = Date.now();
  var s = { art: null, sprache: null, tag: null, zeit: null, name: '', tel: '', mail: '', firma: '', adresse: '', ort: '', thema: '', info: '' };
  // Kunde auf diesem Gerät merken (nur mit Häkchen; localStorage)
  var KUNDE = 'masar-kunde';
  function kLesen() { try { return JSON.parse(localStorage.getItem(KUNDE) || 'null'); } catch (e) { return null; } }
  function kSchreiben(k) { try { localStorage.setItem(KUNDE, JSON.stringify(k)); } catch (e) {} }
  var kunde = kLesen();
  if (kunde) { s.name = kunde.name || ''; s.tel = kunde.tel || ''; s.mail = kunde.mail || ''; s.firma = kunde.firma || ''; s.ort = kunde.ort || ''; }
  s.merken = !!kunde;
  // Thema aus dem Link der Leistungsseite (?thema=LKW-Beschriftung Berlin); „Werbeagentur Bernau“ → Ort
  try {
    var q = (new URLSearchParams(location.search).get('thema') || '').slice(0, 80).trim();
    var wa = /^Werbeagentur (.+)$/.exec(q);
    if (wa) s.ort = wa[1]; else if (q) s.thema = q;
    // Von NRW-Seiten: Beratung nur per Telefon/Video (Vor-Ort-Termine gibt es nur in Berlin)
    if (new URLSearchParams(location.search).get('region') === 'nrw') {
      ARTEN = ARTEN.filter(function (a) { return a[0] !== 'vorort'; });
      var st = /(Köln|Düsseldorf|Dortmund|Essen|Bochum|Herne|Mülheim an der Ruhr|Bottrop)$/.exec(q);
      if (st && !s.ort) s.ort = st[1];
      s.nrw = true;
    }
  } catch (e) {}
  var step = 0, tageCache = {};
  var box = el('div', 'tm'); root.innerHTML = ''; root.appendChild(box);

  function opt(cls, html, on, fn) {
    var b = el('button', cls, html); b.type = 'button'; b.setAttribute('aria-pressed', on ? 'true' : 'false');
    b.addEventListener('click', fn); return b;
  }

  function render() {
    box.innerHTML = '';
    var top = el('div', 'tm-top');
    top.appendChild(txt('span', 'tm-step', 'Schritt ' + (step + 1) + ' von ' + STEPS.length + ' · ' + STEPS[step]));
    var bar = el('div', 'tm-bar', '<i style="width:' + ((step + 1) / STEPS.length * 100) + '%"></i>'); top.appendChild(bar);
    box.appendChild(top);
    [stepArt, stepSprache, stepTermin, stepKontakt][step]();
  }

  function frage(t) { var h = txt('h3', 'tm-q', t); h.tabIndex = -1; box.appendChild(h); return h; }
  function nav(weiter, ok) {
    var n = el('div', 'tm-nav');
    if (step > 0) { var b = txt('button', 'tm-back', '← Zurück'); b.type = 'button'; b.addEventListener('click', function () { step--; render(); }); n.appendChild(b); } else n.appendChild(el('span'));
    if (weiter) { var g = txt('button', 'tm-go', weiter); g.type = 'button'; g.disabled = !ok; g.addEventListener('click', function () { step++; render(); box.querySelector('.tm-q').focus(); }); n.appendChild(g); }
    box.appendChild(n);
  }

  function stepArt() {
    if (kunde && kunde.name) box.appendChild(el('div', 'tm-sum', '👋 Willkommen zurück, <b>' + kunde.name.split(' ')[0].replace(/[<>&"]/g, '') + '</b>! Ihre Kontaktdaten sind schon eingetragen.'));
    if (s.thema) box.appendChild(el('div', 'tm-sum', 'Thema: <b>' + s.thema.replace(/[<>&"]/g, '') + '</b>'));
    frage('Wie möchten Sie beraten werden?');
    var g = el('div', 'tm-grid');
    ARTEN.forEach(function (a) {
      g.appendChild(opt('tm-opt', ico(a[3]) + '<span>' + a[1] + '<small>' + a[2] + '</small></span>', s.art === a[0], function () {
        if (s.art !== a[0]) { s.tag = null; s.zeit = null; }
        s.art = a[0]; step++; render(); box.querySelector('.tm-q').focus();
      }));
    });
    box.appendChild(g);
    box.appendChild(el('p', 'tm-load', s.nrw ? 'Kostenlos und unverbindlich · 30 Minuten · für NRW per Telefon oder WhatsApp-Video – Aufmaß und Montage macht unser Team vor Ort'
                                            : 'Kostenlos und unverbindlich · 30 Minuten (vor Ort 60) · Vor-Ort-Termine nur in Berlin'));
  }

  function stepSprache() {
    frage('In welcher Sprache?');
    var g = el('div', 'tm-grid');
    SPRACHEN.forEach(function (l) {
      g.appendChild(opt('tm-opt', '<span' + (l[0] === 'ar' ? ' dir="rtl" lang="ar"' : ' lang="' + l[0] + '"') + '>' + l[1] + '</span>', s.sprache === l[0], function () {
        s.sprache = l[0]; step++; render(); box.querySelector('.tm-q').focus();
      }));
    });
    box.appendChild(g);
    nav(null);
  }

  function stepTermin() {
    frage('Wann passt es Ihnen?');
    box.appendChild(el('span', 'tm-sub', 'Tag <small>(' + artName(s.art) + ', ' + (s.art === 'vorort' ? '60' : '30') + ' Min.)</small>'));
    var days = el('div', 'tm-days'); box.appendChild(days);
    var zeitWrap = el('div'); box.appendChild(zeitWrap);
    var err = el('p', 'tm-err'); box.appendChild(err);
    nav('Weiter zu Ihren Daten', !!(s.tag && s.zeit));
    var go = box.querySelector('.tm-go');

    function zeiten() {
      zeitWrap.innerHTML = '';
      if (!s.tag) return;
      zeitWrap.appendChild(el('span', 'tm-sub', 'Uhrzeit <small>am ' + tagText(s.tag) + '</small>'));
      var lade = txt('p', 'tm-load', 'Freie Zeiten werden geladen …'); zeitWrap.appendChild(lade);
      fetch('/termin.php?tag=' + s.tag + '&art=' + s.art, { cache: 'no-store' }).then(function (r) { return r.json(); }).then(function (j) {
        lade.remove();
        var z = (j && j.zeiten) || [];
        if (!z.length) { zeitWrap.appendChild(txt('p', 'tm-load', 'An diesem Tag ist leider nichts mehr frei.')); return; }
        var g = el('div', 'tm-times');
        z.forEach(function (u) {
          g.appendChild(opt('tm-time', u, s.zeit === u, function () {
            s.zeit = u; Array.prototype.forEach.call(g.children, function (c) { c.setAttribute('aria-pressed', c.textContent === u ? 'true' : 'false'); }); go.disabled = false;
          }));
        });
        zeitWrap.appendChild(g);
      }).catch(function () { lade.textContent = 'Die Zeiten konnten nicht geladen werden. Bitte später erneut versuchen oder anrufen: 0178 514 3918.'; });
    }

    function tage(liste) {
      days.innerHTML = '';
      liste.forEach(function (t) {
        var d = datum(t.tag);
        var b = opt('tm-day', TAGE[d.getDay()] + '<b>' + d.getDate() + '</b><small>' + MON[d.getMonth()] + '</small>', s.tag === t.tag, function () {
          s.tag = t.tag; s.zeit = null; go.disabled = true;
          Array.prototype.forEach.call(days.children, function (c) { c.setAttribute('aria-pressed', c === b ? 'true' : 'false'); });
          zeiten();
        });
        b.setAttribute('aria-label', tagText(t.tag) + (t.frei ? ', ' + t.frei + ' Zeiten frei' : ', ausgebucht oder geschlossen'));
        if (!t.frei) b.disabled = true;
        days.appendChild(b);
      });
      if (s.tag) zeiten();
    }

    if (tageCache[s.art]) tage(tageCache[s.art]);
    else {
      days.appendChild(txt('p', 'tm-load', 'Kalender wird geladen …'));
      fetch('/termin.php?tage=1&art=' + s.art, { cache: 'no-store' }).then(function (r) { return r.json(); }).then(function (j) {
        tageCache[s.art] = (j && j.tage) || []; tage(tageCache[s.art]);
      }).catch(function () { days.innerHTML = ''; err.textContent = 'Der Kalender konnte nicht geladen werden. Bitte rufen Sie uns an: 0178 514 3918.'; });
    }
  }

  function feld(label, key, typ, ph, pflicht) {
    var w = el('label'); w.style.display = 'block';
    w.appendChild(el('span', 'tm-sub', label + (pflicht ? '' : ' <small>(optional)</small>')));
    var i = el(typ === 'area' ? 'textarea' : 'input', 'tm-in');
    if (typ !== 'area') i.type = typ;
    if (typ === 'tel') i.autocomplete = 'tel'; if (typ === 'email') i.autocomplete = 'email'; if (key === 'name') i.autocomplete = 'name';
    i.placeholder = ph || ''; i.value = s[key] || '';
    i.addEventListener('input', function () { s[key] = i.value; });
    w.appendChild(i); return w;
  }

  function stepKontakt() {
    frage('Ihre Kontaktdaten');
    box.appendChild(el('div', 'tm-sum', '<b>' + tagText(s.tag) + ', ' + s.zeit + ' Uhr</b> · ' + artName(s.art) + ' · ' + sprName(s.sprache)));
    var two = el('div', 'tm-two');
    two.appendChild(feld('Name', 'name', 'text', 'Vor- und Nachname', true));
    two.appendChild(feld('Telefon / WhatsApp', 'tel', 'tel', 'z. B. 0176 …', true));
    two.appendChild(feld('E-Mail', 'mail', 'email', 'für die Terminbestätigung', false));
    two.appendChild(feld('Firma', 'firma', 'text', '', false));
    box.appendChild(two);
    if (s.art === 'vorort') box.appendChild(feld('Adresse in Berlin', 'adresse', 'text', 'Straße, Hausnummer, PLZ', true));
    else box.appendChild(feld('Ihr Ort', 'ort', 'text', 'z. B. Köln oder 13349', false));
    var tw = el('label'); tw.style.display = 'block'; tw.appendChild(el('span', 'tm-sub', 'Worum geht es? <small>(optional)</small>'));
    var sel = el('select', 'tm-in'); sel.appendChild(txt('option', '', '– bitte wählen –')); sel.firstChild.value = '';
    (s.thema && THEMEN.indexOf(s.thema) < 0 ? [s.thema].concat(THEMEN) : THEMEN).forEach(function (t) { var o = txt('option', '', t); o.value = t; if (s.thema === t) o.selected = true; sel.appendChild(o); });
    sel.addEventListener('change', function () { s.thema = sel.value; }); tw.appendChild(sel); box.appendChild(tw);
    box.appendChild(feld('Nachricht', 'info', 'area', 'z. B. Maße, Wunschtermin für die Umsetzung, Fragen …', false));
    var hp = el('input'); hp.type = 'text'; hp.name = 'website'; hp.tabIndex = -1; hp.autocomplete = 'off'; hp.style.cssText = 'position:absolute;left:-9999px;width:1px;height:1px'; hp.setAttribute('aria-hidden', 'true'); box.appendChild(hp);
    var mk = el('label', 'tm-chk', '<input type="checkbox"' + (s.merken ? ' checked' : '') + '> <span>Meine Kontaktdaten <b>auf diesem Gerät</b> merken – für die nächste Buchung und den <a href="/status.html" target="_blank" rel="noopener">Anfrage-Status</a>. Jederzeit löschbar.</span>');
    mk.querySelector('input').addEventListener('change', function (e) { s.merken = e.target.checked; });
    box.appendChild(mk);
    var ck = el('label', 'tm-chk', '<input type="checkbox"> <span>Ich bin einverstanden, dass meine Angaben zur Terminvereinbarung gespeichert und verarbeitet werden (<a href="/datenschutz.html" target="_blank" rel="noopener">Datenschutzerklärung</a>).</span>');
    box.appendChild(ck);
    var err = el('p', 'tm-err'); err.setAttribute('role', 'alert'); box.appendChild(err);
    var n = el('div', 'tm-nav');
    var b = txt('button', 'tm-back', '← Zurück'); b.type = 'button'; b.addEventListener('click', function () { step--; render(); }); n.appendChild(b);
    var go = txt('button', 'tm-go', 'Termin verbindlich buchen'); go.type = 'button'; n.appendChild(go);
    box.appendChild(n);

    go.addEventListener('click', function () {
      err.textContent = '';
      if (s.name.trim().length < 2) { err.textContent = 'Bitte Ihren Namen angeben.'; return; }
      if (s.tel.replace(/\D/g, '').length < 6) { err.textContent = 'Bitte eine Telefonnummer angeben.'; return; }
      if (s.mail.trim() && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s.mail.trim())) { err.textContent = 'Bitte eine gültige E-Mail-Adresse angeben.'; return; }
      if (s.art === 'vorort' && !/\b1[0-4]\d{3}\b/.test(s.adresse)) { err.textContent = 'Bitte Straße und Berliner Postleitzahl angeben.'; return; }
      if (!ck.querySelector('input').checked) { err.textContent = 'Bitte der Datenschutzerklärung zustimmen.'; return; }
      go.disabled = true; go.textContent = 'Wird gebucht …';
      fetch('/termin.php', { method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'same-origin', body: JSON.stringify({
        _t: Date.now() - t0, _honey: hp.value, art: s.art, sprache: s.sprache, tag: s.tag, zeit: s.zeit,
        name: s.name.trim(), telefon: s.tel.trim(), email: s.mail.trim(), firma: s.firma.trim(), adresse: s.adresse.trim(), ort: s.ort.trim(), thema: s.thema, nachricht: s.info.trim(), consent: true
      }) }).then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); }).then(function (x) {
        if (x.ok && x.j.nr) { fertig(x.j); return; }
        go.disabled = false; go.textContent = 'Termin verbindlich buchen';
        err.textContent = (x.j && x.j.fehler) || 'Das hat leider nicht geklappt. Bitte rufen Sie uns an: 0178 514 3918.';
        if (x.j && x.j.vergeben) { delete tageCache[s.art]; s.zeit = null; setTimeout(function () { step = 2; render(); }, 1800); }
      }).catch(function () { go.disabled = false; go.textContent = 'Termin verbindlich buchen'; err.textContent = 'Keine Verbindung. Bitte später erneut versuchen oder anrufen: 0178 514 3918.'; });
    });
  }

  function ics(j) {
    var a = new Date(j.start), e = new Date(a.getTime() + j.dauer * 60000);
    function f(d) { return d.getUTCFullYear() + pad(d.getUTCMonth() + 1) + pad(d.getUTCDate()) + 'T' + pad(d.getUTCHours()) + pad(d.getUTCMinutes()) + '00Z'; }
    var t = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Masar Werbeagentur//Termin//DE', 'BEGIN:VEVENT', 'UID:' + j.nr + '@masar-werbeagentur.de', 'DTSTAMP:' + f(new Date()),
      'DTSTART:' + f(a), 'DTEND:' + f(e), 'SUMMARY:Kostenlose Beratung – Masar Werbeagentur (' + artName(s.art) + ')',
      'DESCRIPTION:Terminnummer ' + j.nr + '. Verschieben oder absagen: WhatsApp 0178 514 3918', s.art === 'vorort' ? 'LOCATION:' + s.adresse.replace(/[,;]/g, '\\$&') : 'LOCATION:Telefon / WhatsApp',
      'END:VEVENT', 'END:VCALENDAR'].join('\r\n');
    return URL.createObjectURL(new Blob([t], { type: 'text/calendar' }));
  }

  function fertig(j) {
    try {
      if (s.merken) {
        var k = kLesen() || {}; k.name = s.name.trim(); k.tel = s.tel.trim(); k.mail = s.mail.trim(); k.firma = s.firma.trim(); if (s.ort) k.ort = s.ort.trim();
        k.anfragen = [{ nr: j.nr, leistung: 'Beratung' + (s.thema ? ': ' + s.thema : '') + ' · ' + j.termin, datum: new Date().toLocaleDateString('de-DE') }].concat((k.anfragen || []).filter(function (a) { return a.nr !== j.nr; })).slice(0, 10);
        kSchreiben(k);
      } else if (kunde) localStorage.removeItem(KUNDE);
    } catch (e) {}
    box.innerHTML = '';
    var ok = el('div', 'tm-ok');
    ok.appendChild(txt('h4', '', 'Termin gebucht – danke!'));
    ok.appendChild(txt('p', 'tm-big', j.termin));
    ok.appendChild(txt('p', '', artName(s.art) + ' · ' + sprName(s.sprache) + ' · Terminnummer ' + j.nr));
    ok.appendChild(txt('p', '', s.art === 'vorort' ? 'Wir kommen zu Ihnen: ' + s.adresse + '.' : 'Wir melden uns zum Termin unter ' + s.tel + '.'
      + (s.mail ? ' Eine Bestätigung ist per E-Mail unterwegs.' : '')));
    var btns = el('div', 'tm-btns');
    var cal = txt('a', 'tm-btn', 'In Kalender eintragen'); cal.href = ics(j); cal.download = 'Termin-Masar-' + j.nr + '.ics'; btns.appendChild(cal);
    var stl = txt('a', 'tm-btn', 'Status ansehen'); stl.href = '/status.html?nr=' + encodeURIComponent(j.nr); btns.appendChild(stl);
    var wa = txt('a', 'tm-btn tm-wa', 'Verschieben per WhatsApp'); wa.href = 'https://wa.me/491785143918?text=' + encodeURIComponent('Hallo, ich möchte meinen Beratungstermin ' + j.nr + ' (' + j.termin + ') verschieben.');
    wa.target = '_blank'; wa.rel = 'noopener noreferrer'; btns.appendChild(wa);
    ok.appendChild(btns);
    box.appendChild(ok);
    box.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  render();
})();
