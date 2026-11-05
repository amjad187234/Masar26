/* Masar Leuchtlogo-Konfigurator: Logo als runder oder eckiger Leuchtkasten, an der Wand oder als Ausleger.
   Vorschau im Browser (Logo und Wandfoto werden nicht hochgeladen): Tag, Nacht und Vergleich mit Schieberegler.
   Keine Preise (Inhaber, 24.10.2026). */
(function () {
  'use strict';
  var root = document.getElementById('leuchtlogo');
  if (!root) return;
  var $ = function (s) { return root.querySelector(s); };
  var $$ = function (s) { return Array.prototype.slice.call(root.querySelectorAll(s)); };
  var WA = '491785143918';
  var REGION = {
    berlin: 'Berlin: Werbeanlagen bis 1 m² Ansichtsfläche sind verfahrensfrei, am eigenen Geschäft bis 2,5 m². Ausleger ragen in den öffentlichen Raum – dafür ist oft eine Sondernutzungserlaubnis des Bezirksamts nötig.',
    nrw: 'NRW: verfahrensfrei bis 1 m² (§ 62 Abs. 1 Nr. 12 BauO NRW); Ausleger über dem Gehweg brauchen meist zusätzlich eine Erlaubnis der Stadt.',
    hamburg: 'Hamburg: bis 1 m² genehmigungsfrei (Anlage 2 HBauO), sonst meist Baugenehmigung; zuständig ist das Bezirksamt.',
    andere: 'Die Regeln unterscheiden sich je Bundesland und Gemeinde. Wir prüfen für Ihren Standort, ob eine Genehmigung nötig ist.'
  };
  var S = { form: 'rund', d: 60, w: 80, h: 50, art: 'wand', rahmen: '#15181c', face: 'auto', zoom: 78, ansicht: 'vergleich', split: 0.5, region: 'berlin', masse: true, wand: 'putz', fassW: 4, pos: null, licht: 'kalt' };
  var RAHMEN = { '#15181c': 'Schwarz', '#f2f2f0': 'Weiß', '#a7adb3': 'Silber' };

  /* ---------- Logo laden & aufbereiten ---------- */
  var logo = null, logoName = 'Masar-Logo (Beispiel)', faceAuto = '#ffffff';
  function trim(img, weiss) {
    var c = document.createElement('canvas'), w = img.naturalWidth || img.width, h = img.naturalHeight || img.height;
    var k = Math.min(1, 1600 / Math.max(w, h)); c.width = Math.max(1, Math.round(w * k)); c.height = Math.max(1, Math.round(h * k));
    var x = c.getContext('2d'); x.drawImage(img, 0, 0, c.width, c.height);
    var d = x.getImageData(0, 0, c.width, c.height), p = d.data, W = c.width, H = c.height;
    // Hintergrundfarbe aus den Ecken
    var ec = [[0, 0], [W - 1, 0], [0, H - 1], [W - 1, H - 1]].map(function (q) { var i = (q[1] * W + q[0]) * 4; return [p[i], p[i + 1], p[i + 2], p[i + 3]]; });
    var transp = ec.every(function (e) { return e[3] < 20; });
    var bg = ec[0];
    if (!transp && weiss) { // einfarbigen Hintergrund (z. B. Weiß beim JPG) entfernen
      for (var i = 0; i < p.length; i += 4) {
        var dd = Math.abs(p[i] - bg[0]) + Math.abs(p[i + 1] - bg[1]) + Math.abs(p[i + 2] - bg[2]);
        if (dd < 36) p[i + 3] = 0; else if (dd < 70) p[i + 3] = Math.min(p[i + 3], (dd - 36) * 7.5);
      }
      x.putImageData(d, 0, 0); transp = true;
    }
    if (!transp) faceAuto = 'rgb(' + bg[0] + ',' + bg[1] + ',' + bg[2] + ')'; else faceAuto = '#ffffff';
    // Rand beschneiden (Zeilen/Spalten mit sehr wenigen Pixeln zählen nicht – robust gegen Rauschen)
    var cols = new Uint32Array(W), rows = new Uint32Array(H), tot = 0;
    for (var yy = 0; yy < H; yy++) for (var xx = 0; xx < W; xx++) {
      var j = (yy * W + xx) * 4, on = transp ? p[j + 3] > 24 : (Math.abs(p[j] - bg[0]) + Math.abs(p[j + 1] - bg[1]) + Math.abs(p[j + 2] - bg[2]) > 40);
      if (on) { cols[xx]++; rows[yy]++; tot++; }
    }
    var mc = Math.max(1, H * 0.004), mr = Math.max(1, W * 0.004), x0 = 0, x1 = W - 1, y0 = 0, y1 = H - 1;
    while (x0 < W && cols[x0] < mc) x0++; while (x1 > x0 && cols[x1] < mc) x1--;
    while (y0 < H && rows[y0] < mr) y0++; while (y1 > y0 && rows[y1] < mr) y1--;
    if (!tot || x0 >= x1 || y0 >= y1) x1 = -1;
    if (x1 < 0) return c;
    var o = document.createElement('canvas'); o.width = x1 - x0 + 2; o.height = y1 - y0 + 2;
    o.getContext('2d').drawImage(c, x0, y0, o.width, o.height, 0, 0, o.width, o.height);
    return o;
  }
  var rohLogo = null;
  function ladeLogo(src, name) {
    var im = new Image();
    im.onload = function () { rohLogo = im; logo = trim(im, $('#ll-weiss').checked); logoName = name; $('#ll-logoname').textContent = name; render(); };
    im.onerror = function () { $('#ll-logoname').textContent = 'Datei konnte nicht gelesen werden – bitte PNG, JPG oder SVG wählen.'; };
    im.src = src;
  }

  /* ---------- Wand ---------- */
  var foto = null;
  function demoWand(c, w, h, ppm) {
    var farben = { putz: ['#e6e1d8', '#d6cfc3'], beton: ['#a9abab', '#929595'], ziegel: ['#9a5a44', '#874c39'], dunkel: ['#3a3f45', '#30343a'] }[S.wand];
    var g = c.createLinearGradient(0, 0, 0, h); g.addColorStop(0, farben[0]); g.addColorStop(1, farben[1]); c.fillStyle = g; c.fillRect(0, 0, w, h);
    // Struktur
    var rnd = 7; function r() { rnd = (rnd * 16807) % 2147483647; return rnd / 2147483647; }
    if (S.wand === 'ziegel') {
      c.strokeStyle = 'rgba(235,225,215,.35)'; c.lineWidth = Math.max(1, 0.012 * ppm);
      var bh = 0.075 * ppm, bw = 0.25 * ppm;
      for (var y = 0, row = 0; y < h; y += bh, row++) {
        c.beginPath(); c.moveTo(0, y); c.lineTo(w, y); c.stroke();
        for (var x = (row % 2) * bw / 2; x < w; x += bw) { c.beginPath(); c.moveTo(x, y); c.lineTo(x, y + bh); c.stroke(); }
      }
      for (var k = 0; k < 900; k++) { c.fillStyle = 'rgba(0,0,0,' + (r() * 0.06) + ')'; c.fillRect(r() * w, r() * h, bw * 0.8, bh * 0.8); }
    } else {
      for (var n = 0; n < 2600; n++) { c.fillStyle = (r() > 0.5 ? 'rgba(255,255,255,' : 'rgba(0,0,0,') + (r() * 0.05) + ')'; var s = r() * 3 + 1; c.fillRect(r() * w, r() * h, s, s); }
      if (S.wand === 'beton') { c.strokeStyle = 'rgba(0,0,0,.08)'; c.lineWidth = 1; for (var yy = 0.6 * ppm; yy < h; yy += 0.6 * ppm) { c.beginPath(); c.moveTo(0, yy); c.lineTo(w, yy); c.stroke(); } }
    }
    // Lichtverlauf (Tageslicht von oben)
    var lg = c.createLinearGradient(0, 0, w, h); lg.addColorStop(0, 'rgba(255,255,255,.10)'); lg.addColorStop(1, 'rgba(0,0,0,.10)'); c.fillStyle = lg; c.fillRect(0, 0, w, h);
    // Person 1,75 m als Maßstab
    var gy = h - 0.08 * ppm, px = w - 0.95 * ppm, ph = 1.75 * ppm;
    if (px > 0.3 * ppm && h > ph * 1.02) {
      c.fillStyle = 'rgba(19,46,80,.55)';
      c.beginPath(); c.arc(px, gy - ph + 0.12 * ppm, 0.11 * ppm, 0, 7); c.fill();
      c.beginPath(); c.moveTo(px - 0.2 * ppm, gy - ph + 0.27 * ppm); c.lineTo(px + 0.2 * ppm, gy - ph + 0.27 * ppm); c.lineTo(px + 0.16 * ppm, gy - 0.85 * ppm); c.lineTo(px + 0.12 * ppm, gy); c.lineTo(px + 0.02 * ppm, gy); c.lineTo(px, gy - 0.8 * ppm); c.lineTo(px - 0.02 * ppm, gy); c.lineTo(px - 0.12 * ppm, gy); c.lineTo(px - 0.16 * ppm, gy - 0.85 * ppm); c.closePath(); c.fill();
      c.font = '600 ' + Math.max(11, 0.12 * ppm) + 'px Barlow, sans-serif'; c.fillStyle = S.wand === 'dunkel' || S.wand === 'ziegel' ? 'rgba(255,255,255,.8)' : 'rgba(19,46,80,.75)'; c.fillText('1,75 m', px + 0.22 * ppm, gy - ph + 0.2 * ppm);
    }
  }

  /* ---------- Leuchtkasten zeichnen ---------- */
  function lichtFarbe() { return S.licht === 'warm' ? [255, 228, 186] : [244, 249, 255]; }
  function pfad(c, x, y, w, h) {
    c.beginPath();
    if (S.form === 'rund') c.ellipse(x + w / 2, y + h / 2, w / 2, h / 2, 0, 0, Math.PI * 2);
    else { var r = Math.min(w, h) * 0.06; c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); }
  }
  function faceFarbe() { return S.face === 'auto' ? faceAuto : S.face; }
  function kasten(c, x, y, w, h, nacht) {
    var rim = Math.max(3, Math.min(w, h) * 0.045), L = lichtFarbe(), Ls = 'rgb(' + L.join(',') + ')';
    c.save();
    // Ausleger-Halter
    if (S.art === 'ausleger') {
      var arm = Math.max(10, h * 0.28), pl = Math.max(6, h * 0.05);
      c.fillStyle = nacht ? '#0c0e11' : '#1d2126';
      c.fillRect(x + w / 2 - pl * 2.2, y - arm - pl, pl * 4.4, pl); // Wandplatte oben (Decke/Wand)
      c.fillRect(x + w / 2 - pl * 0.7, y - arm, pl * 1.4, arm + rim);
    }
    // Schatten / Lichtschein auf der Wand
    if (!nacht) { c.save(); c.shadowColor = 'rgba(0,0,0,.38)'; c.shadowBlur = Math.max(8, w * 0.06); c.shadowOffsetX = w * 0.025; c.shadowOffsetY = h * 0.035; pfad(c, x, y, w, h); c.fillStyle = S.rahmen; c.fill(); c.restore(); }
    else {
      var cx = x + w / 2, cy = y + h / 2, R = Math.max(w, h) * 1.15;
      var g = c.createRadialGradient(cx, cy, Math.min(w, h) * 0.35, cx, cy, R);
      g.addColorStop(0, 'rgba(' + L.join(',') + ',.38)'); g.addColorStop(0.45, 'rgba(' + L.join(',') + ',.12)'); g.addColorStop(1, 'rgba(' + L.join(',') + ',0)');
      c.fillStyle = g; c.fillRect(cx - R, cy - R, R * 2, R * 2);
    }
    // Rahmen (Zarge) mit Rundung
    pfad(c, x, y, w, h);
    var rg = c.createLinearGradient(x, y, x + w, y + h);
    rg.addColorStop(0, mix(S.rahmen, '#ffffff', nacht ? 0.08 : 0.28)); rg.addColorStop(0.5, S.rahmen); rg.addColorStop(1, mix(S.rahmen, '#000000', 0.35));
    c.fillStyle = rg; c.fill();
    // Front
    var fx = x + rim, fy = y + rim, fw = w - 2 * rim, fh = h - 2 * rim;
    c.save(); pfad(c, fx, fy, fw, fh); c.clip();
    c.fillStyle = faceFarbe(); c.fillRect(fx, fy, fw, fh);
    if (logo) {
      var z = S.zoom / 100, k = Math.min(fw * z / logo.width, fh * z / logo.height);
      if (S.form === 'rund') k *= 0.9;
      var lw = logo.width * k, lh = logo.height * k;
      c.drawImage(logo, fx + (fw - lw) / 2, fy + (fh - lh) / 2, lw, lh);
    }
    if (nacht) { // durchleuchtete Front: hell in der Mitte, Farben strahlen
      c.globalCompositeOperation = 'screen';
      var fg = c.createRadialGradient(fx + fw / 2, fy + fh / 2, 0, fx + fw / 2, fy + fh / 2, Math.max(fw, fh) * 0.62);
      fg.addColorStop(0, 'rgba(' + L.join(',') + ',.30)'); fg.addColorStop(1, 'rgba(' + L.join(',') + ',.08)');
      c.fillStyle = fg; c.fillRect(fx, fy, fw, fh);
      c.globalCompositeOperation = 'source-over';
    } else { // Acrylglanz
      var gl = c.createLinearGradient(fx, fy, fx + fw * 0.7, fy + fh * 0.7);
      gl.addColorStop(0, 'rgba(255,255,255,.28)'); gl.addColorStop(0.42, 'rgba(255,255,255,.05)'); gl.addColorStop(0.43, 'rgba(255,255,255,0)');
      c.fillStyle = gl; c.fillRect(fx, fy, fw, fh);
    }
    c.restore();
    // Leuchtring innen (wie bei LED-Kästen mit Lichtkante)
    c.save(); pfad(c, fx, fy, fw, fh); c.lineWidth = Math.max(1.5, rim * (nacht ? 0.5 : 0.25));
    if (nacht) { c.shadowColor = Ls; c.shadowBlur = Math.max(6, rim * 2.2); c.strokeStyle = Ls; }
    else c.strokeStyle = 'rgba(255,255,255,.55)';
    c.stroke(); c.restore();
    if (nacht) { c.save(); c.globalCompositeOperation = 'lighter'; c.shadowColor = Ls; c.shadowBlur = Math.max(10, w * 0.08); pfad(c, x, y, w, h); c.strokeStyle = 'rgba(' + L.join(',') + ',.25)'; c.lineWidth = 2; c.stroke(); c.restore(); }
    c.restore();
  }
  function mix(a, b, t) { var x = hex(a), y = hex(b); return 'rgb(' + x.map(function (v, i) { return Math.round(v + (y[i] - v) * t); }).join(',') + ')'; }
  function hex(h) { if (h.indexOf('rgb') === 0) return h.match(/\d+/g).slice(0, 3).map(Number); h = h.replace('#', ''); var n = parseInt(h, 16); return [n >> 16 & 255, n >> 8 & 255, n & 255]; }

  /* ---------- Szene ---------- */
  var cv = $('#ll-canvas'), ctx = cv.getContext('2d'), tag = document.createElement('canvas'), nacht = document.createElement('canvas'), box = null;
  function massM() { return S.form === 'rund' ? [S.d / 100, S.d / 100] : [S.w / 100, S.h / 100]; }
  function szene(c, cw, ch, dpr, ppm, istNacht) {
    c.setTransform(dpr, 0, 0, dpr, 0, 0);
    if (foto) c.drawImage(foto, 0, 0, cw, ch); else demoWand(c, cw, ch, ppm);
    if (istNacht) { c.fillStyle = 'rgba(6,10,22,.74)'; c.fillRect(0, 0, cw, ch); }
    var m = massM(), w = m[0] * ppm, h = m[1] * ppm;
    if (!S.pos) S.pos = { x: 0.5, y: 0.38 };
    var x = S.pos.x * cw - w / 2, y = S.pos.y * ch - h / 2;
    box = { x: x, y: y, w: w, h: h };
    kasten(c, x, y, w, h, istNacht);
  }
  var raf = 0;
  function render() { cancelAnimationFrame(raf); raf = requestAnimationFrame(draw); }
  function draw() {
    var wrap = $('.kf-stage'), cw = wrap.clientWidth, dpr = Math.min(window.devicePixelRatio || 1, 2);
    var Wm = foto ? S.fassW : 5, ar = foto ? foto.height / foto.width : 0.62;
    var ch = Math.min(cw * ar, window.innerHeight * (window.innerWidth < 1000 ? 0.36 : 0.6));
    if (ch < cw * ar) cw = ch / ar;
    var ppm = cw / Wm;
    [cv, tag, nacht].forEach(function (k) { k.width = Math.round(cw * dpr); k.height = Math.round(ch * dpr); });
    cv.style.width = cw + 'px'; cv.style.height = ch + 'px';
    szene(tag.getContext('2d'), cw, ch, dpr, ppm, false);
    szene(nacht.getContext('2d'), cw, ch, dpr, ppm, true);
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    if (S.ansicht === 'tag') ctx.drawImage(tag, 0, 0);
    else if (S.ansicht === 'nacht') ctx.drawImage(nacht, 0, 0);
    else {
      var sx = Math.round(cv.width * S.split);
      ctx.drawImage(tag, 0, 0); ctx.drawImage(nacht, sx, 0, cv.width - sx, cv.height, sx, 0, cv.width - sx, cv.height);
      ctx.fillStyle = '#fff'; ctx.fillRect(sx - dpr, 0, 2 * dpr, cv.height);
      ctx.beginPath(); ctx.arc(sx, cv.height / 2, 16 * dpr, 0, 7); ctx.fill();
      ctx.fillStyle = '#132e50'; ctx.font = 700 + ' ' + 13 * dpr + 'px Barlow, sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('‹ ›', sx, cv.height / 2 + dpr);
      ctx.textAlign = 'left'; ctx.fillStyle = 'rgba(255,255,255,.9)'; ctx.font = '700 ' + 12 * dpr + 'px Barlow, sans-serif';
      lab(ctx, 'TAG', 10 * dpr, 12 * dpr, dpr); lab(ctx, 'NACHT', cv.width - 62 * dpr, 12 * dpr, dpr);
    }
    if (S.masse) masse(ctx, dpr);
    ergebnis();
  }
  function lab(c, t, x, y, dpr) { var w = c.measureText(t).width + 14 * dpr; c.fillStyle = 'rgba(19,46,80,.82)'; c.fillRect(x, y, w, 22 * dpr); c.fillStyle = '#fff'; c.textBaseline = 'middle'; c.fillText(t, x + 7 * dpr, y + 11 * dpr); }
  function masse(c, dpr) {
    var b = box, m = massM(); c.save(); c.setTransform(dpr, 0, 0, dpr, 0, 0); c.strokeStyle = '#58d0bd'; c.lineWidth = 1.5; c.fillStyle = '#0e2340';
    c.font = '700 13px Barlow, sans-serif'; c.textAlign = 'center'; c.textBaseline = 'alphabetic';
    var yy = b.y + b.h + 16; ln(c, b.x, yy, b.x + b.w, yy); ln(c, b.x, yy - 5, b.x, yy + 5); ln(c, b.x + b.w, yy - 5, b.x + b.w, yy + 5);
    pill(c, (S.form === 'rund' ? 'Ø ' : '') + cm(m[0]), b.x + b.w / 2, yy + 17);
    if (S.form !== 'rund') { var xx = b.x + b.w + 16; ln(c, xx, b.y, xx, b.y + b.h); ln(c, xx - 5, b.y, xx + 5, b.y); ln(c, xx - 5, b.y + b.h, xx + 5, b.y + b.h); c.save(); c.translate(xx + 14, b.y + b.h / 2); c.rotate(-Math.PI / 2); pill(c, cm(m[1]), 0, 5); c.restore(); }
    c.restore();
  }
  function ln(c, a, b, d, e) { c.beginPath(); c.moveTo(a, b); c.lineTo(d, e); c.stroke(); }
  function pill(c, t, x, y) { var w = c.measureText(t).width + 12; c.save(); c.fillStyle = 'rgba(255,255,255,.94)'; c.fillRect(x - w / 2, y - 14, w, 19); c.restore(); c.fillText(t, x, y); }
  function cm(m) { return Math.round(m * 100) + ' cm'; }
  function zahl(x) { return x.toFixed(2).replace('.', ','); }

  var last = null;
  function ergebnis() {
    var m = massM(), fl = S.form === 'rund' ? Math.PI * m[0] * m[0] / 4 : m[0] * m[1];
    var rows = [['Form', S.form === 'rund' ? 'Rund' : 'Eckig'], ['Größe', S.form === 'rund' ? 'Ø ' + cm(m[0]) : cm(m[0]) + ' × ' + cm(m[1])],
      ['Montage', S.art === 'ausleger' ? 'Ausleger, doppelseitig' : 'An der Wand, einseitig'], ['Rahmen', RAHMEN[S.rahmen] || S.rahmen],
      ['Lichtfarbe', S.licht === 'warm' ? 'Warmweiß' : 'Kaltweiß'], ['Ansichtsfläche', zahl(fl) + ' m²' + (S.art === 'ausleger' ? ' je Seite' : '')], ['Logo', esc(logoName)]];
    $('#ll-tab').innerHTML = rows.map(function (r) { return '<tr><th scope="row">' + r[0] + '</th><td>' + r[1] + '</td></tr>'; }).join('');
    $('#ll-gen').innerHTML = '<strong>Genehmigung:</strong> ' + REGION[S.region] + ' <a href="/blog/aussenwerbung-berlin-ratgeber.html">Mehr im Ratgeber</a>';
    last = { m: m, fl: fl };
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function text() {
    var m = last.m;
    return ['Leuchtlogo: ' + (S.form === 'rund' ? 'rund, Ø ' + cm(m[0]) : 'eckig, ' + cm(m[0]) + ' × ' + cm(m[1])),
      'Montage: ' + (S.art === 'ausleger' ? 'Ausleger, doppelseitig' : 'an der Wand, einseitig'), 'Rahmen: ' + (RAHMEN[S.rahmen] || S.rahmen) + ' · Licht: ' + (S.licht === 'warm' ? 'warmweiß' : 'kaltweiß'),
      'Ort: ' + { berlin: 'Berlin', nrw: 'NRW', hamburg: 'Hamburg', andere: 'anderer Ort' }[S.region]].join('\n');
  }
  function bild(cb) {
    var dpr = cv.width / parseFloat(cv.style.width), info = Math.round(60 * dpr), o = document.createElement('canvas');
    o.width = cv.width * 2; o.height = cv.height + info; var c = o.getContext('2d');
    c.drawImage(tag, 0, 0); c.drawImage(nacht, cv.width, 0);
    c.fillStyle = '#132e50'; c.fillRect(0, cv.height, o.width, info);
    c.fillStyle = '#58d0bd'; c.font = '700 ' + info * 0.34 + 'px Barlow, sans-serif'; c.textBaseline = 'middle';
    c.fillText('Masar Werbeagentur · Leuchtlogo-Vorschau', info * 0.35, cv.height + info * 0.34);
    c.fillStyle = '#fff'; c.font = '500 ' + info * 0.27 + 'px Barlow, sans-serif';
    c.fillText(text().split('\n').slice(0, 2).join(' · ') + ' · links Tag, rechts Nacht', info * 0.35, cv.height + info * 0.72);
    o.toBlob(cb, 'image/png');
  }

  /* ---------- Bedienung ---------- */
  function gruppe(sel, key, after) {
    $$(sel + ' [data-v]').forEach(function (b) {
      b.addEventListener('click', function () {
        $$(sel + ' [data-v]').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); }); b.setAttribute('aria-pressed', 'true');
        S[key] = b.getAttribute('data-v'); if (after) after(S[key]); render();
      });
    });
  }
  gruppe('#ll-form', 'form', function (v) { $('#ll-rund').hidden = v !== 'rund'; $('#ll-eckig').hidden = v === 'rund'; });
  gruppe('#ll-art', 'art');
  gruppe('#ll-licht', 'licht');
  gruppe('#ll-wand', 'wand');
  gruppe('#ll-ansicht', 'ansicht', function (v) { $('#ll-splittip').hidden = v !== 'vergleich'; });
  $$('#ll-rahmen [data-c]').forEach(function (b) { b.addEventListener('click', function () { $$('#ll-rahmen [data-c]').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); }); b.setAttribute('aria-pressed', 'true'); S.rahmen = b.getAttribute('data-c'); render(); }); });
  $$('#ll-face [data-c]').forEach(function (b) { b.addEventListener('click', function () { $$('#ll-face [data-c]').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); }); b.setAttribute('aria-pressed', 'true'); S.face = b.getAttribute('data-c'); render(); }); });
  var fpick = root.querySelector('#ll-face input[type=color]'); if (fpick) fpick.addEventListener('input', function () { $$('#ll-face [data-c]').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); }); S.face = fpick.value; render(); });
  function num(id, key) { $(id).addEventListener('input', function (e) { var v = parseFloat(String(e.target.value).replace(',', '.')); if (v > 0) { S[key] = Math.min(400, v); render(); } }); }
  num('#ll-d', 'd'); num('#ll-w', 'w'); num('#ll-h', 'h'); num('#ll-fw', 'fassW');
  var zoom = $('#ll-zoom'); zoom.addEventListener('input', function () { S.zoom = +zoom.value; $('#ll-zoom-out').textContent = zoom.value + ' %'; render(); });
  $('#ll-region').addEventListener('change', function (e) { S.region = e.target.value; render(); });
  $('#ll-masse').addEventListener('click', function (e) { S.masse = !S.masse; e.currentTarget.setAttribute('aria-pressed', String(S.masse)); render(); });
  $('#ll-logo').addEventListener('change', function (e) {
    var f = e.target.files[0]; if (!f) return;
    var url = URL.createObjectURL(f); ladeLogo(url, f.name);
  });
  $('#ll-weiss').addEventListener('change', function () { if (rohLogo) { logo = trim(rohLogo, $('#ll-weiss').checked); render(); } });
  $('#ll-foto').addEventListener('change', function (e) {
    var f = e.target.files[0]; if (!f) return; var im = new Image();
    im.onload = function () { var k = Math.min(1, 2400 / Math.max(im.width, im.height)), c = document.createElement('canvas'); c.width = Math.round(im.width * k); c.height = Math.round(im.height * k); c.getContext('2d').drawImage(im, 0, 0, c.width, c.height); foto = c; S.pos = { x: 0.5, y: 0.4 }; $('#ll-fotowrap').hidden = false; $('#ll-wandwrap').hidden = true; render(); };
    im.src = URL.createObjectURL(f);
  });
  $('#ll-demo').addEventListener('click', function () { foto = null; S.pos = null; $('#ll-fotowrap').hidden = true; $('#ll-wandwrap').hidden = false; $('#ll-foto').value = ''; render(); });

  // Ziehen: Schild verschieben, im Vergleich den Teiler
  var drag = null;
  function pt(e) { var r = cv.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top, r: r }; }
  function aufSchild(p) { return box && p.x >= box.x - 8 && p.x <= box.x + box.w + 8 && p.y >= box.y - 8 && p.y <= box.y + box.h + 8; }
  cv.addEventListener('pointerdown', function (e) {
    var p = pt(e);
    if (S.ansicht === 'vergleich' && Math.abs(p.x - S.split * p.r.width) < 26) drag = { t: 'split' };
    else if (aufSchild(p)) drag = { t: 'box', dx: p.x - (box.x + box.w / 2), dy: p.y - (box.y + box.h / 2) };
    else if (S.ansicht === 'vergleich') { drag = { t: 'split' }; S.split = Math.max(0.02, Math.min(0.98, p.x / p.r.width)); render(); }
    if (drag) { cv.setPointerCapture(e.pointerId); e.preventDefault(); }
  });
  cv.addEventListener('pointermove', function (e) {
    var p = pt(e);
    if (!drag) { cv.style.cursor = S.ansicht === 'vergleich' && Math.abs(p.x - S.split * p.r.width) < 26 ? 'ew-resize' : aufSchild(p) ? 'grab' : ''; return; }
    if (drag.t === 'split') S.split = Math.max(0.02, Math.min(0.98, p.x / p.r.width));
    else S.pos = { x: Math.max(0, Math.min(1, (p.x - drag.dx) / p.r.width)), y: Math.max(0, Math.min(1, (p.y - drag.dy) / p.r.height)) };
    render();
  });
  ['pointerup', 'pointercancel'].forEach(function (ev) { cv.addEventListener(ev, function () { drag = null; }); });
  cv.addEventListener('keydown', function (e) {
    var k = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, -1], ArrowDown: [0, 1] }[e.key]; if (!k) return; e.preventDefault();
    if (S.ansicht === 'vergleich' && !e.shiftKey && k[1] === 0) S.split = Math.max(0.02, Math.min(0.98, S.split + k[0] * 0.04));
    else { S.pos = S.pos || { x: 0.5, y: 0.4 }; S.pos = { x: Math.max(0, Math.min(1, S.pos.x + k[0] * 0.02)), y: Math.max(0, Math.min(1, S.pos.y + k[1] * 0.02)) }; }
    render();
  });

  $('#ll-png').addEventListener('click', function () { bild(function (b) { var a = document.createElement('a'); a.href = URL.createObjectURL(b); a.download = 'masar-leuchtlogo-vorschau.png'; document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500); }); });
  $('#ll-wa').addEventListener('click', function () { window.open('https://wa.me/' + WA + '?text=' + encodeURIComponent('Hallo, ich habe auf Ihrer Website ein Leuchtlogo geplant:\n' + text() + '\nBitte um ein Festpreis-Angebot. Logo und Vorschau schicke ich als Bild.'), '_blank', 'noopener'); });
  $('#ll-anfrage').addEventListener('click', function () {
    var ta = document.getElementById('fo-nachricht'), fi = document.getElementById('fo-datei');
    if (ta) ta.value = 'Mein Leuchtlogo aus der Vorschau:\n' + text() + '\n\n' + (ta.value || '');
    bild(function (b) {
      try { if (fi && window.DataTransfer) { var dt = new DataTransfer(); dt.items.add(new File([b], 'leuchtlogo-vorschau.png', { type: 'image/png' })); fi.files = dt.files; } } catch (e) {}
      var k = document.getElementById('kontakt'); if (k) k.scrollIntoView({ behavior: 'smooth' });
      setTimeout(function () { var n = document.getElementById('fo-name'); if (n) n.focus({ preventScroll: true }); }, 600);
    });
  });
  window.addEventListener('resize', render);
  ladeLogo('/logo.png', 'Masar-Logo (Beispiel)');
  render();
})();
