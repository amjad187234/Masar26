/*
 * Preisrechner – sofortige „ab“-Preise aus der offiziellen Preisliste (netto, zzgl. 19 % MwSt.).
 * Einbau:  <div data-preisrechner data-produkt="banner|leuchtbuchstaben|lochfolie" data-region="nrw|hamburg"></div>
 * Ohne data-region gelten die Preise für Berlin & Brandenburg. Nur Startpreise – Festpreis nach Fotos oder Aufmaß.
 */
(function () {
  'use strict';
  var roots = document.querySelectorAll('[data-preisrechner]');
  if (!roots.length) return;
  var WA = '491785143918';
  // Preisliste (CLAUDE.md): [Berlin, NRW/Hamburg]
  var P = {
    pvc: [19, 22], mesh: [22, 25], blockout: [29, 33], bannerMin: [39, 49],
    buchstabe: [199, 229], loch: [45, 55]
  };
  var css = '.pr{background:#fff;border:1px solid #e0eaea;border-radius:14px;padding:20px;box-shadow:0 6px 24px rgba(19,46,80,.07);max-width:640px;margin:0 auto;font-family:Barlow,system-ui,sans-serif;color:#1a2a2a}'
    + '.pr h3{font-family:"Barlow Condensed",sans-serif;font-weight:800;font-size:1.5rem;text-transform:uppercase;color:#132e50;margin:0 0 4px}'
    + '.pr .pr-s{font-size:14px;color:#5a7070;margin:0 0 14px}'
    + '.pr-tabs{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px}'
    + '.pr-tabs button{border:1.5px solid #e0eaea;background:#fff;border-radius:999px;padding:8px 14px;font:600 14px Barlow,sans-serif;color:#132e50;cursor:pointer}'
    + '.pr-tabs button[aria-pressed=true]{background:#58d0bd;border-color:#58d0bd}'
    + '.pr-g{display:grid;grid-template-columns:1fr 1fr;gap:10px}'
    + '.pr label{display:block;font-size:13px;font-weight:600;color:#5a7070;margin-bottom:4px}'
    + '.pr input,.pr select{width:100%;border:1px solid #e0eaea;border-radius:8px;padding:11px 12px;font:16px Barlow,sans-serif;background:#fff;color:#1a2a2a}'
    + '.pr input:focus,.pr select:focus{outline:none;border-color:#58d0bd;box-shadow:0 0 0 3px rgba(88,208,189,.2)}'
    + '.pr-out{margin-top:16px;background:linear-gradient(135deg,#132e50,#0d4a4a);color:#fff;border-radius:12px;padding:16px 18px;display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:6px}'
    + '.pr-out b{font:800 2rem "Barlow Condensed",sans-serif;color:#58d0bd}.pr-out span{font-size:13px;color:rgba(255,255,255,.75)}'
    + '.pr-n{font-size:12.5px;color:#5a7070;margin:10px 0 0;line-height:1.6}'
    + '.pr-b{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}'
    + '.pr-b a,.pr-b button{flex:1 1 200px;text-align:center;border:0;border-radius:10px;padding:13px 14px;font:700 15px Barlow,sans-serif;cursor:pointer;text-decoration:none}'
    + '.pr-b .p1{background:#58d0bd;color:#132e50}.pr-b .p2{background:#25d366;color:#fff}'
    + '@media(max-width:520px){.pr-g{grid-template-columns:1fr}.pr{padding:16px}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  function eur(v) { return v.toLocaleString('de-DE', { minimumFractionDigits: 0, maximumFractionDigits: 0 }) + ' €'; }
  function el(t, c, h) { var e = document.createElement(t); if (c) e.className = c; if (h != null) e.innerHTML = h; return e; }

  roots.forEach(function (root) {
    var reg = root.getAttribute('data-region'); var r = (reg === 'nrw' || reg === 'hamburg') ? 1 : 0;
    var gebiet = reg === 'hamburg' ? 'Hamburg' : reg === 'nrw' ? 'NRW' : 'Berlin & Brandenburg';
    var produkt = root.getAttribute('data-produkt') || 'banner';
    var box = el('div', 'pr'); root.innerHTML = ''; root.appendChild(box);
    box.appendChild(el('h3', '', 'Preisrechner'));
    box.appendChild(el('p', 'pr-s', 'Sofort einen Startpreis sehen – Preise für ' + gebiet + ', netto zzgl. 19 % MwSt.'));
    var tabs = el('div', 'pr-tabs'); box.appendChild(tabs);
    var form = el('div'); box.appendChild(form);
    var out = el('div', 'pr-out'); box.appendChild(out);
    var note = el('p', 'pr-n'); box.appendChild(note);
    var btns = el('div', 'pr-b'); box.appendChild(btns);
    var DEF = {
      banner: ['Banner', function () {
        return '<div class="pr-g"><div><label>Breite (cm)</label><input type="number" inputmode="numeric" min="10" max="5000" value="300" data-k="b"></div>'
          + '<div><label>Höhe (cm)</label><input type="number" inputmode="numeric" min="10" max="2000" value="100" data-k="h"></div></div>'
          + '<div style="margin-top:10px"><label>Material</label><select data-k="m"><option value="pvc">PVC-Banner (wetterfest)</option><option value="mesh">Mesh-Banner (Gerüst, Bauzaun)</option><option value="blockout">Blockout-Banner (beidseitig, blickdicht)</option></select></div>'
          + '<div style="margin-top:10px"><label>Anzahl</label><input type="number" inputmode="numeric" min="1" max="500" value="1" data-k="n"></div>';
      }, function (v) {
        var b = Math.max(10, +v.b || 0), h = Math.max(10, +v.h || 0), n = Math.max(1, Math.round(+v.n || 1));
        var m2 = b * h / 10000, satz = P[v.m || 'pvc'][r];
        var stueck = Math.max(m2 * satz, P.bannerMin[r]);
        return { preis: stueck * n, text: n + ' × ' + b + ' × ' + h + ' cm (' + m2.toLocaleString('de-DE', { maximumFractionDigits: 2 }) + ' m²), ' + { pvc: 'PVC', mesh: 'Mesh', blockout: 'Blockout' }[v.m || 'pvc'] + '-Banner',
          info: satz + ' €/m², Mindestpreis ' + P.bannerMin[r] + ' € je Banner. Ösen, Hohlsaum und Montage nennen wir im Festpreis.', as: ['druck', 1] };
      }],
      leuchtbuchstaben: ['Leuchtbuchstaben', function () {
        return '<div><label>Ihr Schriftzug (oder Anzahl Buchstaben)</label><input type="text" maxlength="60" value="CAFÉ LUNA" data-k="t"></div>';
      }, function (v) {
        var t = (v.t || '').trim(), n = /^\d+$/.test(t) ? +t : t.replace(/[^\p{L}\p{N}&]/gu, '').length;
        n = Math.max(1, Math.min(n, 60));
        return { preis: n * P.buchstabe[r], text: n + ' LED-Leuchtbuchstaben' + (/^\d+$/.test(t) ? '' : ' („' + t.slice(0, 40) + '“)'),
          info: 'ab ' + P.buchstabe[r] + ' € je Buchstabe. Größe, Montage, Elektrik und ggf. Genehmigung nennen wir im Festpreis.', as: ['schild', 1] };
      }],
      lochfolie: ['Lochfolie / bedrucktes Fenster', function () {
        return '<div class="pr-g"><div><label>Breite (cm)</label><input type="number" inputmode="numeric" min="10" max="2000" value="200" data-k="b"></div>'
          + '<div><label>Höhe (cm)</label><input type="number" inputmode="numeric" min="10" max="1000" value="150" data-k="h"></div></div>'
          + '<div style="margin-top:10px"><label>Anzahl Fenster</label><input type="number" inputmode="numeric" min="1" max="50" value="1" data-k="n"></div>';
      }, function (v) {
        var b = Math.max(10, +v.b || 0), h = Math.max(10, +v.h || 0), n = Math.max(1, Math.round(+v.n || 1)), m2 = b * h / 10000;
        return { preis: m2 * n * P.loch[r], text: n + ' × ' + b + ' × ' + h + ' cm Lochfolie (' + (m2 * n).toLocaleString('de-DE', { maximumFractionDigits: 2 }) + ' m²)',
          info: 'ab ' + P.loch[r] + ' €/m². Gestaltung und Montage nennen wir im Festpreis.', as: ['schaufenster', 1] };
      }]
    };
    var cur = DEF[produkt] ? produkt : 'banner', res = null;
    Object.keys(DEF).forEach(function (k) {
      var b = el('button', '', DEF[k][0]); b.type = 'button'; b.setAttribute('aria-pressed', k === cur);
      b.addEventListener('click', function () { cur = k; tabs.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b); }); draw(); });
      tabs.appendChild(b);
    });
    function vals() { var v = {}; form.querySelectorAll('[data-k]').forEach(function (i) { v[i.getAttribute('data-k')] = i.value; }); return v; }
    function calc() {
      res = DEF[cur][2](vals());
      out.innerHTML = '<span>Startpreis für ' + res.text + '</span><b>ab ' + eur(res.preis) + ' netto</b><span>≈ ' + eur(res.preis * 1.19) + ' brutto</span>';
      note.textContent = res.info + ' Unverbindliche Schätzung – Ihr Festpreis kommt nach Fotos oder Aufmaß, in der Regel innerhalb von 24 Stunden.';
      var wa = 'Hallo, ich möchte ein Angebot (' + gebiet + '): ' + res.text + '. Preisrechner: ab ' + eur(res.preis) + ' netto.';
      btns.innerHTML = '';
      var a1 = el('a', 'p1', 'Festpreis anfragen →'); a1.href = '#kontakt';
      a1.addEventListener('click', function (e) { if (window.MasarAssistent && document.querySelector('[data-assistent]')) { e.preventDefault(); window.MasarAssistent.open(res.as[0], res.as[1]); var t = document.querySelector('[data-assistent]'); if (t) t.scrollIntoView({ behavior: 'smooth', block: 'start' }); } });
      var a2 = el('a', 'p2', 'Per WhatsApp senden'); a2.href = 'https://wa.me/' + WA + '?text=' + encodeURIComponent(wa); a2.target = '_blank'; a2.rel = 'noopener';
      btns.appendChild(a1); btns.appendChild(a2);
    }
    function draw() { form.innerHTML = DEF[cur][1](); form.querySelectorAll('input,select').forEach(function (i) { i.addEventListener('input', calc); }); calc(); }
    draw();
  });
})();
