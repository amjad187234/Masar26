/* Masar Schilder- & Leuchtbuchstaben-Konfigurator – Vorschau auf Demo-Fassade oder eigenem Fassadenfoto.
   Alles im Browser (Foto wird nicht hochgeladen). Lesbarkeit nach USSC-Methode (Legibility Index 30 ft/in,
   Faktor 0,83 bzw. 0,67 bei mittlerer bzw. hoher visueller Komplexität). Keine Preise (Inhaber, 24.10.2026). */
(function () {
  'use strict';
  var root = document.getElementById('konfig');
  if (!root) return;
  var $ = function (s) { return root.querySelector(s); };
  var $$ = function (s) { return Array.prototype.slice.call(root.querySelectorAll(s)); };
  var WA = '491785143918';

  var FONTS = {
    montserrat: ['Montserrat', '/fonts/konfig/montserrat-800.woff2', 800],
    barlow: ['Barlow Condensed', '/fonts/barlow-condensed-black.woff2', 900],
    poppins: ['Poppins', '/fonts/konfig/poppins-600.woff2', 600],
    oswald: ['Oswald', '/fonts/konfig/oswald-600.woff2', 600],
    bebas: ['Bebas Neue', '/fonts/konfig/bebas-neue-400.woff2', 400],
    playfair: ['Playfair Display', '/fonts/konfig/playfair-700.woff2', 700],
    dancing: ['Dancing Script', '/fonts/konfig/dancing-script-700.woff2', 700]
  };
  var TYPEN = {
    buchstaben: 'Einzelbuchstaben / Leuchtbuchstaben',
    leuchtkasten: 'Leuchtkasten',
    schild: 'Firmenschild (Alu-Dibond)',
    ausleger: 'Ausleger / Nasenschild',
    fenster: 'Schaufensterbeschriftung'
  };
  var OPT = { front: 'Frontleuchtend', halo: 'Rückleuchtend (Halo)', unbel: 'Unbeleuchtet (3D)' };
  var LICHT = { kalt: '#f3f8ff', warm: '#ffe2b0', farbe: null };
  var WAND = { hell: ['#e9e4dc', '#d8d1c6'], grau: ['#9aa1a6', '#868d93'], anthrazit: ['#3b4045', '#33373b'], ziegel: ['#9c5a43', '#8a4c38'] };
  var REGION = {
    berlin: 'Berlin: Nach der Berliner Bauordnung sind Werbeanlagen bis 1 m² Ansichtsfläche verfahrensfrei, am eigenen Geschäft bis 2,5 m². Größere Anlagen brauchen meist eine Genehmigung; Denkmalschutz kann zusätzlich gelten.',
    nrw: 'NRW: Verfahrensfrei bis 1 m² (§ 62 Abs. 1 Nr. 12 BauO NRW); Flächen nebeneinander werden zusammengerechnet. Darüber ist meist eine Genehmigung nötig.',
    hamburg: 'Hamburg: Bis 1 m² genehmigungsfrei (Anlage 2 HBauO), sonst meist Baugenehmigung; zuständig ist das Bezirksamt.',
    andere: 'Die Regeln unterscheiden sich je Bundesland und Gemeinde. Wir prüfen für Ihren Standort, ob eine Genehmigung nötig ist.'
  };

  var S = {
    text: 'Ihr Name', text2: '', typ: 'buchstaben', opt: 'front', font: 'montserrat',
    face: '#ffffff', side: '#1d2226', bg: '#132e50', licht: 'kalt', wand: 'hell',
    modus: 'platz', platzW: 4, platzH: 0.8, dist: 25, wahl: 1, hEigen: 40, region: 'berlin',
    nacht: false, masse: true, foto: null, fassW: 8, pos: null
  };

  /* ---------- Schriften laden ---------- */
  var geladen = {};
  function ladeFont(k) { // Schriften sind per @font-face (K-…) eingebunden; hier nur sicher laden
    if (!geladen[k]) geladen[k] = document.fonts && document.fonts.load ? document.fonts.load(fontStr(k, 40)).catch(function () {}) : Promise.resolve();
    return geladen[k];
  }
  function fontStr(k, px) { return FONTS[k][2] + ' ' + px + 'px "K-' + k + '", sans-serif'; }

  /* ---------- Maße ---------- */
  var mc = document.createElement('canvas').getContext('2d');
  function metr(txt, k) { // Werte relativ zur Versalhöhe 1
    mc.font = fontStr(k, 200);
    var h = mc.measureText('H'), cap = (h.actualBoundingBoxAscent || 140) / 200;
    var m = mc.measureText(txt || ' ');
    return { cap: cap, w: m.width / 200 / cap, asc: (m.actualBoundingBoxAscent || cap * 200) / 200 / cap, desc: (m.actualBoundingBoxDescent || 0) / 200 / cap, l: (m.actualBoundingBoxLeft || 0) / 200 / cap };
  }
  function padFuer(t) { return t === 'buchstaben' || t === 'fenster' ? 0 : t === 'schild' ? 0.45 : 0.5; }
  function block(Hm) { // Abmessungen des Schilds in m bei Versalhöhe Hm
    var a = metr(S.text, S.font), H2 = S.text2 ? Hm * 0.42 : 0, b = S.text2 ? metr(S.text2, S.font) : null;
    var w = Math.max(a.w * Hm, b ? b.w * H2 : 0), gap = S.text2 ? Hm * 0.38 : 0;
    var top = Math.max(1, a.asc) * Hm, h = top + a.desc * Hm + (b ? gap + Math.max(1, b.asc) * H2 + b.desc * H2 : 0);
    var p = padFuer(S.typ) * Hm, W = w + 2 * p, HH = h + 2 * p;
    if (S.typ === 'ausleger') { var q = Math.max(W, HH); W = HH = q; }
    return { W: W, H: HH, tw: w, th: h, pad: p, H1: Hm, H2: H2, gap: gap, a: a, b: b, top: top };
  }
  var LI = [30, 30 * 0.83, 30 * 0.67]; // ft pro inch → H(m) = d(m) / (12 · LI)
  function hAusAbstand(d, i) { return d / (12 * LI[i]); }
  function lesbarBis(H) { return [H * 12 * LI[2], H * 12 * LI[0]]; }
  function hoehe() {
    if (S.modus === 'eigen') return Math.max(0.02, S.hEigen / 100);
    if (S.modus === 'abstand') return hAusAbstand(S.dist, S.wahl);
    // nach Platz: größte Versalhöhe, die in Breite × Höhe passt
    var b = block(1), k = Math.min(S.platzW / b.W, S.platzH / b.H);
    return Math.max(0.02, k);
  }
  function cm(m) { return m >= 1 ? (Math.round(m * 100) / 100).toString().replace('.', ',') + ' m' : Math.round(m * 100) + ' cm'; }
  function zahl(x, n) { return x.toFixed(n || 0).replace('.', ','); }

  /* ---------- Szene ---------- */
  var cv = $('#kf-canvas'), ctx = cv.getContext('2d'), mini = $('#kf-mini'), mctx = mini.getContext('2d');
  var scene = document.createElement('canvas'), sctx = scene.getContext('2d');
  var foto = null, W_m = 8, H_m = 4.5, ppm = 100, signBox = null;

  function demoFassade(c, w, h) {
    var wd = WAND[S.wand], P = ppm;
    var g = c.createLinearGradient(0, 0, 0, h); g.addColorStop(0, wd[0]); g.addColorStop(1, wd[1]);
    c.fillStyle = g; c.fillRect(0, 0, w, h);
    if (S.wand === 'ziegel') { // Fugen
      c.strokeStyle = 'rgba(255,255,255,.12)'; c.lineWidth = 1;
      for (var y = 0; y < h; y += 0.075 * P) { c.beginPath(); c.moveTo(0, y); c.lineTo(w, y); c.stroke(); }
    }
    var gy = h - 0.35 * P; // Gehweg
    c.fillStyle = '#8f9396'; c.fillRect(0, gy, w, h - gy);
    c.fillStyle = 'rgba(0,0,0,.18)'; c.fillRect(0, gy, w, 3);
    // Schaufenster + Tür
    var fx = 0.6 * P, fw = W_m * 0.55 * P, fy = gy - 2.4 * P, fh = 2.25 * P;
    var dx = fx + fw + 0.45 * P, dw = 1.05 * P, dy = gy - 2.25 * P;
    [[fx, fy, fw, fh], [dx, dy, dw, 2.25 * P]].forEach(function (r) {
      c.fillStyle = '#2b3138'; c.fillRect(r[0] - 6, r[1] - 6, r[2] + 12, r[3] + 6);
      var gl = c.createLinearGradient(r[0], r[1], r[0] + r[2], r[1] + r[3]);
      gl.addColorStop(0, S.nacht ? '#ffe9b8' : '#8fb2c6'); gl.addColorStop(1, S.nacht ? '#d9a75a' : '#5f8296');
      c.fillStyle = gl; c.fillRect(r[0], r[1], r[2], r[3]);
      c.fillStyle = 'rgba(255,255,255,.14)';
      c.beginPath(); c.moveTo(r[0], r[1]); c.lineTo(r[0] + r[2] * 0.35, r[1]); c.lineTo(r[0], r[1] + r[3] * 0.6); c.fill();
    });
    c.fillStyle = '#c9ced2'; c.fillRect(dx + dw - 0.14 * P, dy + 1.05 * P, 0.06 * P, 0.25 * P);
    // Person 1,75 m als Maßstab
    var px = Math.min(w - 0.5 * P, dx + dw + 0.7 * P), ph = 1.75 * P;
    c.fillStyle = 'rgba(19,46,80,.75)';
    c.beginPath(); c.arc(px, gy - ph + 0.12 * P, 0.11 * P, 0, 7); c.fill();
    c.beginPath(); c.moveTo(px - 0.2 * P, gy - ph + 0.27 * P); c.lineTo(px + 0.2 * P, gy - ph + 0.27 * P); c.lineTo(px + 0.16 * P, gy - 0.85 * P);
    c.lineTo(px + 0.12 * P, gy); c.lineTo(px + 0.02 * P, gy); c.lineTo(px, gy - 0.8 * P); c.lineTo(px - 0.02 * P, gy); c.lineTo(px - 0.12 * P, gy);
    c.lineTo(px - 0.16 * P, gy - 0.85 * P); c.closePath(); c.fill();
    c.fillStyle = S.wand === 'anthrazit' || S.wand === 'ziegel' ? 'rgba(255,255,255,.85)' : 'rgba(19,46,80,.8)'; c.font = '600 ' + Math.max(10, 0.13 * P) + 'px Barlow, sans-serif';
    c.fillText('1,75 m', px + 0.22 * P, gy - ph + 0.2 * P);
    return { fx: fx, fy: fy, fw: fw, fh: fh, gy: gy };
  }

  function lichtFarbe() { return S.licht === 'farbe' ? S.face : LICHT[S.licht]; }

  function textZeilen(c, B, x0, y0, s, fill, mode) {
    // zeichnet die Zeilen; mode: 'face' | 'extr' | 'glow'
    var f1 = B.H1 * s / B.a.cap, xm = x0 + B.W * s / 2;
    c.textAlign = 'center'; c.textBaseline = 'alphabetic';
    var by = y0 + (B.pad + B.top) * s;
    if (S.typ === 'ausleger') by = y0 + (B.H - B.th) / 2 * s + B.top * s;
    var gl = mode === 'glow'; if (gl) { c.strokeStyle = fill; c.lineJoin = 'round'; c.lineWidth = Math.max(2, B.H1 * s * 0.12); }
    c.font = fontStr(S.font, f1); c.fillStyle = fill; c.fillText(S.text, xm, by); if (gl) c.strokeText(S.text, xm, by);
    if (S.text2) {
      var f2 = B.H2 * s / B.b.cap, by2 = by + B.a.desc * B.H1 * s + B.gap * s + Math.max(1, B.b.asc) * B.H2 * s;
      c.font = fontStr(S.font, f2); c.fillText(S.text2, xm, by2); if (gl) c.strokeText(S.text2, xm, by2);
    }
  }

  function zeichneSchild(c, B, x, y, s) {
    var night = S.nacht, L = lichtFarbe();
    c.save();
    if (S.typ === 'buchstaben') {
      var d = Math.max(2, 0.07 * s); // Zargentiefe (Darstellung)
      if (!night) { c.shadowColor = 'rgba(0,0,0,.35)'; c.shadowBlur = 0.05 * s; c.shadowOffsetX = 0.05 * s; c.shadowOffsetY = 0.06 * s; }
      if (night && S.opt !== 'unbel') { // Lichtschein auf der Wand
        var cxw = x + B.W * s / 2, cyw = y + B.H * s / 2, rw = Math.max(B.W, B.H) * s * 0.75;
        var rg = c.createRadialGradient(cxw, cyw, 0, cxw, cyw, rw); rg.addColorStop(0, rgba(L, S.opt === 'halo' ? 0.34 : 0.16)); rg.addColorStop(1, rgba(L, 0));
        c.save(); c.translate(cxw, cyw); c.scale(1, Math.min(1, (B.H * 2.2) / B.W)); c.translate(-cxw, -cyw); c.fillStyle = rg; c.fillRect(cxw - rw, cyw - rw, rw * 2, rw * 2); c.restore();
      }
      if (night && S.opt === 'halo') { // Lichtkranz hinter den Buchstaben
        c.save(); c.globalCompositeOperation = 'lighter';
        [0.06, 0.16, 0.34, 0.7].forEach(function (k, j) { c.shadowColor = L; c.shadowBlur = Math.max(4, k * B.H1 * s); c.globalAlpha = [0.95, 0.85, 0.7, 0.55][j]; textZeilen(c, B, x, y, s, L, 'glow'); });
        c.restore();
      }
      for (var i = Math.round(d); i >= 1; i--) textZeilen(c, B, x + i * 0.55, y + i * 0.75, s, night && S.opt === 'front' ? shade(S.side, -0.2) : shade(S.side, -0.25 * i / d), 'extr');
      c.shadowColor = 'transparent';
      if (night && S.opt === 'front') { c.shadowColor = L; c.shadowBlur = Math.max(8, 0.18 * B.H1 * s); textZeilen(c, B, x, y, s, mix(S.face, L, 0.35), 'face'); c.shadowBlur = Math.max(4, 0.06 * B.H1 * s); textZeilen(c, B, x, y, s, mix(S.face, '#ffffff', 0.25), 'face'); }
      else if (night && S.opt === 'halo') textZeilen(c, B, x, y, s, mix(shade(S.side, -0.1), S.face, 0.12), 'face');
      else if (night) textZeilen(c, B, x, y, s, shade(S.face, -0.6), 'face');
      else textZeilen(c, B, x, y, s, S.face, 'face');
    } else if (S.typ === 'fenster') {
      textZeilen(c, B, x, y, s, night ? mix(S.face, '#000', 0.15) : S.face, 'face');
    } else {
      var w = B.W * s, h = B.H * s, r = S.typ === 'schild' ? Math.min(6, 0.02 * s) : Math.min(10, 0.04 * s);
      if (S.typ === 'ausleger') { // Halter zur Wand
        c.fillStyle = '#2b3036'; c.fillRect(x - 0.18 * s, y + h * 0.2, 0.18 * s, Math.max(3, 0.04 * s)); c.fillRect(x - 0.2 * s, y + h * 0.12, Math.max(3, 0.03 * s), h * 0.2);
      }
      if (S.typ !== 'schild') { // Kastentiefe
        c.fillStyle = shade(S.bg, -0.45); rr(c, x + 0.05 * s, y + 0.07 * s, w, h, r); c.fill();
      }
      if (night && S.typ !== 'schild') { c.shadowColor = mix(S.bg, L, 0.6); c.shadowBlur = Math.max(14, 0.25 * s); }
      else if (!night) { c.shadowColor = 'rgba(0,0,0,.3)'; c.shadowBlur = 0.06 * s; c.shadowOffsetY = 0.04 * s; }
      c.fillStyle = night ? (S.typ === 'schild' ? shade(S.bg, -0.6) : mix(S.bg, L, 0.25)) : S.bg;
      rr(c, x, y, w, h, r); c.fill();
      c.shadowColor = 'transparent';
      if (S.typ === 'schild') { // Abstandhalter
        c.fillStyle = night ? '#555' : '#c7cdd2'; var o = Math.max(3, 0.04 * s);
        [[o * 1.6, o * 1.6], [w - o * 1.6, o * 1.6], [o * 1.6, h - o * 1.6], [w - o * 1.6, h - o * 1.6]].forEach(function (p) { c.beginPath(); c.arc(x + p[0], y + p[1], o * 0.55, 0, 7); c.fill(); });
      }
      if (night && S.typ !== 'schild') { c.shadowColor = L; c.shadowBlur = Math.max(5, 0.05 * B.H1 * s); }
      textZeilen(c, B, x, y, s, night && S.typ === 'schild' ? shade(S.face, -0.6) : S.face, 'face');
    }
    c.restore();
  }
  function rr(c, x, y, w, h, r) { c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); }
  function rgba(h, a) { var x = hex(h); return 'rgba(' + x.join(',') + ',' + a + ')'; }
  function hex(h) { h = h.replace('#', ''); if (h.length === 3) h = h.replace(/./g, '$&$&'); var n = parseInt(h, 16); return [n >> 16 & 255, n >> 8 & 255, n & 255]; }
  function rgb(a) { return 'rgb(' + a.map(function (v) { return Math.max(0, Math.min(255, Math.round(v))); }).join(',') + ')'; }
  function shade(h, f) { var a = hex(h); return rgb(a.map(function (v) { return f < 0 ? v * (1 + f) : v + (255 - v) * f; })); }
  function mix(a, b, t) { var x = hex(a), y = hex(b.indexOf('rgb') === 0 ? '#ffffff' : b); return rgb(x.map(function (v, i) { return v + (y[i] - v) * t; })); }

  function masslinien(c, B, x, y, s) {
    var w = B.W * s, h = B.H * s;
    c.save(); c.strokeStyle = '#58d0bd'; c.fillStyle = '#0e2340'; c.lineWidth = 1.5;
    c.font = '700 ' + Math.max(11, Math.min(15, 0.12 * ppm)) + 'px Barlow, sans-serif'; c.textAlign = 'center';
    var yy = y - Math.max(12, 0.12 * s);
    line(c, x, yy, x + w, yy); tick(c, x, yy, 'v'); tick(c, x + w, yy, 'v');
    lab(c, cm(B.W), x + w / 2, yy - 5);
    var xx = x + w + Math.max(12, 0.12 * s);
    line(c, xx, y, xx, y + h); tick(c, xx, y, 'h'); tick(c, xx, y + h, 'h');
    c.save(); c.translate(xx + 5, y + h / 2); c.rotate(-Math.PI / 2); lab(c, cm(B.H), 0, 10); c.restore();
    c.restore();
  }
  function line(c, a, b, d, e) { c.beginPath(); c.moveTo(a, b); c.lineTo(d, e); c.stroke(); }
  function tick(c, x, y, o) { if (o === 'v') line(c, x, y - 5, x, y + 5); else line(c, x - 5, y, x + 5, y); }
  function lab(c, t, x, y) { var w = c.measureText(t).width + 10; c.save(); c.fillStyle = 'rgba(255,255,255,.92)'; c.fillRect(x - w / 2, y - 14, w, 18); c.restore(); c.fillText(t, x, y); }

  var raf = 0;
  function render() { cancelAnimationFrame(raf); raf = requestAnimationFrame(draw); }
  function draw() {
    var wrap = $('.kf-stage'), cw = wrap.clientWidth, dpr = Math.min(window.devicePixelRatio || 1, 2);
    W_m = foto ? S.fassW : 8;
    var ar = foto ? foto.height / foto.width : 0.56;
    var ch = Math.min(cw * ar, window.innerHeight * (window.innerWidth < 1000 ? 0.34 : 0.58));
    if (ch < cw * ar) cw = ch / ar;
    H_m = W_m * ar; ppm = cw / W_m;
    cv.width = Math.round(cw * dpr); cv.height = Math.round(ch * dpr); cv.style.width = cw + 'px'; cv.style.height = ch + 'px';
    scene.width = cv.width; scene.height = cv.height;
    var c = sctx; c.setTransform(dpr, 0, 0, dpr, 0, 0);
    var dem = null;
    if (foto) {
      c.drawImage(foto, 0, 0, cw, ch);
      if (S.nacht) { c.fillStyle = 'rgba(8,14,30,.72)'; c.fillRect(0, 0, cw, ch); }
    } else {
      dem = demoFassade(c, cw, ch);
      if (S.nacht) { c.fillStyle = 'rgba(8,14,30,.66)'; c.fillRect(0, 0, cw, ch); c.globalCompositeOperation = 'lighter'; c.fillStyle = 'rgba(255,200,120,.18)'; c.fillRect(dem.fx, dem.fy, dem.fw, dem.fh); c.globalCompositeOperation = 'source-over'; }
    }
    var Hm = hoehe(), B = block(Hm), s = ppm;
    if (!S.pos) S.pos = S.typ === 'fenster' ? { x: 0.33, y: 0.62 } : { x: 0.42, y: 0.18 };
    var x = S.pos.x * cw - B.W * s / 2, y = S.pos.y * ch - B.H * s / 2;
    if (S.typ === 'fenster' && dem && !S._fensterPos) { x = dem.fx + (dem.fw - B.W * s) / 2; y = dem.fy + dem.fh * 0.12; }
    signBox = { x: x, y: y, w: B.W * s, h: B.H * s };
    zeichneSchild(c, B, x, y, s);
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(scene, 0, 0);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    if (S.masse) masslinien(ctx, B, x, y, s);
    zuGross(B);
    zeichneMini(B, x, y, s, cw, ch, dpr);
    ergebnis(Hm, B);
  }
  function zuGross(B) {
    var w = $('#kf-warn'), t = '';
    if (B.W > W_m * 0.98) t = 'Das Schild ist breiter als die Fassade in der Vorschau. Kürzeren Text wählen oder kleinere Buchstaben.';
    else if (S.modus === 'abstand' && B.H1 < 0.08 && S.typ === 'buchstaben' && S.opt !== 'unbel') t = 'Sehr kleine Leuchtbuchstaben sind technisch begrenzt – wir beraten Sie zur Mindestgröße.';
    w.textContent = t; w.hidden = !t;
  }

  function zeichneMini(B, x, y, s, cw, ch, dpr) {
    var mw = mini.clientWidth || 260, mh = Math.round(mw * 0.62);
    mini.width = Math.round(mw * dpr); mini.height = Math.round(mh * dpr); mini.style.height = mh + 'px';
    var c = mctx; c.setTransform(1, 0, 0, 1, 0, 0);
    c.fillStyle = S.nacht ? '#0b1322' : '#cfd9df'; c.fillRect(0, 0, mini.width, mini.height);
    var Wv = 2 * S.dist * Math.tan(32 * Math.PI / 180); // Blickfeld ≈ 64° (wie Handy-Hauptkamera, quer)
    var cx = (x + B.W * s / 2) * dpr, cy = (y + B.H * s / 2) * dpr, sw = Wv * ppm * dpr, sh = sw * mh / mw;
    var sx = cx - sw / 2, sy = cy - sh / 2, k = mini.width / sw;
    // Quelle auf die Szene beschneiden und Ziel passend versetzen
    var x0 = Math.max(0, sx), y0 = Math.max(0, sy), x1 = Math.min(scene.width, sx + sw), y1 = Math.min(scene.height, sy + sh);
    if (x1 > x0 && y1 > y0) c.drawImage(scene, x0, y0, x1 - x0, y1 - y0, (x0 - sx) * k, (y0 - sy) * k, (x1 - x0) * k, (y1 - y0) * k);
    var req = hAusAbstand(S.dist, 0), ok = B.H1 >= req ? (B.H1 >= hAusAbstand(S.dist, 2) ? 'gut' : 'knapp') : 'nein';
    var L = { gut: ['Gut lesbar', '#177567'], knapp: ['Lesbar bei guter Sicht', '#9a5b00'], nein: ['Zu klein für diesen Abstand', '#b3261e'] }[ok];
    $('#kf-mini-cap').innerHTML = 'So wirkt es aus <strong>' + S.dist + ' m</strong> (Blickfeld wie ein Handyfoto) · <span style="color:' + L[1] + ';font-weight:700">' + L[0] + '</span>';
  }

  /* ---------- Ergebnis ---------- */
  var last = null;
  function ergebnis(Hm, B) {
    var n = (S.text + S.text2).replace(/\s/g, '').length, fl = B.W * B.H;
    var lb = lesbarBis(Hm);
    var rows = [['Schildart', TYPEN[S.typ] + (S.typ === 'buchstaben' ? ' · ' + OPT[S.opt] : '')],
      ['Text', esc(S.text) + (S.text2 ? ' / ' + esc(S.text2) : '')], ['Schrift', FONTS[S.font][0]],
      ['Versalhöhe', cm(Hm) + (S.text2 ? ' (Zeile 2: ' + cm(B.H2) + ')' : '')], ['Gesamtmaß', cm(B.W) + ' × ' + cm(B.H)],
      ['Ansichtsfläche', zahl(fl, 2) + ' m²']];
    if (S.typ === 'buchstaben' || S.typ === 'fenster') rows.push([S.typ === 'fenster' ? 'Zeichen' : 'Buchstaben', String(n)]);
    rows.push(['Lesbar bis ca.', r10(lb[0]) + '–' + r10(lb[1]) + ' m']);
    $('#kf-tab').innerHTML = rows.map(function (r) { return '<tr><th scope="row">' + r[0] + '</th><td>' + r[1] + '</td></tr>'; }).join('');
    var g = fl <= 1 ? 'Mit ' + zahl(fl, 2) + ' m² liegt die Fläche bei 1 m² oder darunter. ' : 'Mit ' + zahl(fl, 2) + ' m² liegt die Fläche über 1 m². ';
    $('#kf-gen').innerHTML = '<strong>Genehmigung:</strong> ' + g + REGION[S.region] + ' <a href="/blog/aussenwerbung-berlin-ratgeber.html">Mehr im Ratgeber</a>';
    // drei Größen nach Abstand
    $$('.kf-opt3 button').forEach(function (b, i) {
      var h = hAusAbstand(S.dist, i), bb = block(h);
      b.querySelector('.kf-o-h').textContent = cm(h);
      b.querySelector('.kf-o-m').textContent = cm(bb.W) + ' × ' + cm(bb.H);
      b.setAttribute('aria-pressed', String(S.wahl === i));
    });
    last = { Hm: Hm, B: B, n: n, fl: fl, lb: lb };
  }
  function r10(x) { return x < 20 ? Math.round(x) : Math.round(x / 5) * 5; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function zusammenfassung() {
    var B = last.B;
    return ['Schildart: ' + TYPEN[S.typ] + (S.typ === 'buchstaben' ? ' – ' + OPT[S.opt] : ''),
      'Text: ' + S.text + (S.text2 ? ' / ' + S.text2 : ''), 'Schrift: ' + FONTS[S.font][0],
      'Farben: Front ' + S.face + (S.typ === 'buchstaben' ? ', Seite ' + S.side : ', Untergrund ' + S.bg) + (S.typ !== 'schild' && S.opt !== 'unbel' ? ', Licht ' + { kalt: 'kaltweiß', warm: 'warmweiß', farbe: 'farbig' }[S.licht] : ''),
      'Versalhöhe: ' + cm(last.Hm) + ' · Gesamtmaß ' + cm(B.W) + ' × ' + cm(B.H) + ' · ' + zahl(last.fl, 2) + ' m²',
      'Ort: ' + { berlin: 'Berlin', nrw: 'NRW', hamburg: 'Hamburg', andere: 'anderer Ort' }[S.region]].join('\n');
  }
  function bildBlob(cb) {
    var out = document.createElement('canvas'), pad = 0, info = 64 * (window.devicePixelRatio > 1 ? 2 : 1);
    out.width = cv.width; out.height = cv.height + info;
    var c = out.getContext('2d'); c.drawImage(cv, 0, 0);
    c.fillStyle = '#132e50'; c.fillRect(0, cv.height, out.width, info);
    c.fillStyle = '#58d0bd'; c.font = '700 ' + info * 0.32 + 'px Barlow, sans-serif'; c.textBaseline = 'middle';
    c.fillText('Masar Werbeagentur · Entwurfsvorschau', info * 0.3, cv.height + info * 0.33);
    c.fillStyle = '#fff'; c.font = '500 ' + info * 0.26 + 'px Barlow, sans-serif';
    c.fillText(TYPEN[S.typ] + ' · ' + cm(last.B.W) + ' × ' + cm(last.B.H) + ' · Versalhöhe ' + cm(last.Hm) + ' · ' + (S.nacht ? 'Nacht' : 'Tag'), info * 0.3, cv.height + info * 0.72);
    void pad; out.toBlob(cb, 'image/png');
  }

  /* ---------- Bedienung ---------- */
  function set(k, v) { S[k] = v; if (k === 'font') ladeFont(v).then(render); render(); }
  $('#kf-text').addEventListener('input', function (e) { set('text', e.target.value.slice(0, 40) || ' '); });
  $('#kf-text2').addEventListener('input', function (e) { set('text2', e.target.value.slice(0, 50)); });
  function gruppe(sel, key, after) {
    $$(sel + ' [data-v]').forEach(function (b) {
      b.addEventListener('click', function () {
        $$(sel + ' [data-v]').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
        b.setAttribute('aria-pressed', 'true'); S[key] = b.getAttribute('data-v'); if (after) after(S[key]);
        if (key === 'font') ladeFont(S.font).then(render); render();
      });
    });
  }
  gruppe('#kf-typ', 'typ', function (v) {
    $('#kf-optwrap').hidden = v !== 'buchstaben';
    $('#kf-bgwrap').hidden = v === 'buchstaben' || v === 'fenster';
    $('#kf-sidewrap').hidden = v !== 'buchstaben';
    $('#kf-lichtwrap').hidden = v === 'schild' || v === 'fenster';
    S._fensterPos = false; S.pos = null;
    if (v === 'schild' || v === 'leuchtkasten' || v === 'ausleger') { if (S.face === '#ffffff' && S.bg === '#ffffff') S.bg = '#132e50'; }
    var D = { buchstaben: [400, 80], leuchtkasten: [350, 80], schild: [250, 60], ausleger: [70, 70], fenster: [200, 40] }[v]; // Startfläche je Schildart
    S.platzW = D[0] / 100; S.platzH = D[1] / 100; $('#kf-pw').value = D[0]; $('#kf-ph').value = D[1];
  });
  gruppe('#kf-opt', 'opt', function () { $('#kf-lichtwrap').hidden = S.opt === 'unbel'; });
  gruppe('#kf-font', 'font');
  gruppe('#kf-licht', 'licht');
  gruppe('#kf-wand', 'wand');
  gruppe('#kf-modus', 'modus', function (v) { $$('.kf-m').forEach(function (d) { d.hidden = d.getAttribute('data-m') !== v; }); });
  function farben(sel, key) {
    $$(sel + ' [data-c]').forEach(function (b) { b.addEventListener('click', function () { $$(sel + ' [data-c]').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); }); b.setAttribute('aria-pressed', 'true'); set(key, b.getAttribute('data-c')); }); });
    var inp = root.querySelector(sel + ' input[type=color]');
    if (inp) inp.addEventListener('input', function () { $$(sel + ' [data-c]').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); }); set(key, inp.value); });
  }
  farben('#kf-face', 'face'); farben('#kf-side', 'side'); farben('#kf-bg', 'bg');
  function num(id, key, f) { $(id).addEventListener('input', function (e) { var v = parseFloat(String(e.target.value).replace(',', '.')); if (v > 0) set(key, f ? f(v) : v); }); }
  num('#kf-pw', 'platzW', function (v) { return v / 100; }); num('#kf-ph', 'platzH', function (v) { return v / 100; });
  num('#kf-he', 'hEigen'); num('#kf-fw', 'fassW');
  var dist = $('#kf-dist'), distOut = $('#kf-dist-out');
  dist.addEventListener('input', function () { distOut.textContent = dist.value + ' m'; set('dist', +dist.value); });
  $$('.kf-opt3 button').forEach(function (b, i) { b.addEventListener('click', function () { set('wahl', i); }); });
  $('#kf-region').addEventListener('change', function (e) { set('region', e.target.value); });
  $('#kf-nacht').addEventListener('click', function (e) { var b = e.currentTarget; S.nacht = !S.nacht; b.setAttribute('aria-pressed', String(S.nacht)); b.lastChild.textContent = S.nacht ? ' Tag' : ' Nacht'; render(); });
  $('#kf-masse').addEventListener('click', function (e) { var b = e.currentTarget; S.masse = !S.masse; b.setAttribute('aria-pressed', String(S.masse)); render(); });

  // Eigenes Foto (als data:-URL – die CSP erlaubt keine blob:-Bilder)
  function dataUrl(f, cb) { var r = new FileReader(); r.onload = function () { cb(r.result); }; r.onerror = function () { cb(null); }; r.readAsDataURL(f); }
  $('#kf-foto').addEventListener('change', function (e) {
    var f = e.target.files[0]; if (!f) return;
    var img = new Image(); img.onload = function () {
      var max = 2400, k = Math.min(1, max / Math.max(img.width, img.height)), c = document.createElement('canvas');
      c.width = Math.round(img.width * k); c.height = Math.round(img.height * k); c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
      foto = c; S.pos = { x: 0.5, y: 0.3 }; $('#kf-fotowrap').hidden = false; $('#kf-wandwrap').hidden = true; render();
    };
    dataUrl(f, function (u) { if (u) img.src = u; });
  });
  $('#kf-demo').addEventListener('click', function () { foto = null; S.pos = null; $('#kf-fotowrap').hidden = true; $('#kf-wandwrap').hidden = false; $('#kf-foto').value = ''; render(); });

  // Verschieben (Maus, Finger, Tastatur)
  var drag = null;
  cv.addEventListener('pointerdown', function (e) {
    var r = cv.getBoundingClientRect(), x = e.clientX - r.left, y = e.clientY - r.top;
    if (!signBox || x < signBox.x - 10 || x > signBox.x + signBox.w + 10 || y < signBox.y - 10 || y > signBox.y + signBox.h + 10) return;
    drag = { dx: x - (signBox.x + signBox.w / 2), dy: y - (signBox.y + signBox.h / 2), r: r }; cv.setPointerCapture(e.pointerId); cv.classList.add('drag'); e.preventDefault();
  });
  cv.addEventListener('pointermove', function (e) {
    var r = cv.getBoundingClientRect(), x = e.clientX - r.left, y = e.clientY - r.top;
    if (!drag) { cv.style.cursor = signBox && x >= signBox.x && x <= signBox.x + signBox.w && y >= signBox.y && y <= signBox.y + signBox.h ? 'grab' : ''; return; }
    S.pos = { x: Math.max(0, Math.min(1, (x - drag.dx) / r.width)), y: Math.max(0, Math.min(1, (y - drag.dy) / r.height)) }; S._fensterPos = true; render();
  });
  function stop() { drag = null; cv.classList.remove('drag'); }
  cv.addEventListener('pointerup', stop); cv.addEventListener('pointercancel', stop);
  cv.addEventListener('keydown', function (e) {
    var k = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, -1], ArrowDown: [0, 1] }[e.key]; if (!k || !S.pos) return;
    e.preventDefault(); var st = e.shiftKey ? 0.05 : 0.01; S.pos = { x: Math.max(0, Math.min(1, S.pos.x + k[0] * st)), y: Math.max(0, Math.min(1, S.pos.y + k[1] * st)) }; S._fensterPos = true; render();
  });

  // Ergebnis-Aktionen
  $('#kf-png').addEventListener('click', function () {
    bildBlob(function (b) { var a = document.createElement('a'); a.href = URL.createObjectURL(b); a.download = 'masar-schild-vorschau.png'; document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500); });
  });
  $('#kf-wa').addEventListener('click', function () {
    var t = 'Hallo, ich habe im Konfigurator auf Ihrer Website ein Schild geplant:\n' + zusammenfassung() + '\nBitte um ein Festpreis-Angebot. Die Vorschau schicke ich als Bild.';
    window.open('https://wa.me/' + WA + '?text=' + encodeURIComponent(t), '_blank', 'noopener');
  });
  $('#kf-anfrage').addEventListener('click', function () {
    var ta = document.getElementById('fo-nachricht'), fi = document.getElementById('fo-datei'), sel = document.getElementById('fo-folie');
    if (ta) ta.value = 'Mein Entwurf aus dem Konfigurator:\n' + zusammenfassung() + '\n\n' + (ta.value || '');
    if (sel) { for (var i = 0; i < sel.options.length; i++) if (sel.options[i].text.indexOf(S.typ === 'buchstaben' ? (S.opt === 'unbel' ? 'Einzelbuchstaben' : 'Leuchtbuchstaben') : TYPEN[S.typ].split(' ')[0]) === 0) { sel.selectedIndex = i; break; } }
    bildBlob(function (b) {
      try { if (fi && window.DataTransfer) { var dt = new DataTransfer(); dt.items.add(new File([b], 'schild-vorschau.png', { type: 'image/png' })); fi.files = dt.files; } } catch (e) {}
      var k = document.getElementById('kontakt'); if (k) k.scrollIntoView({ behavior: 'smooth' });
      setTimeout(function () { var n = document.getElementById('fo-name'); if (n) n.focus({ preventScroll: true }); }, 600);
    });
  });

  window.addEventListener('resize', render);
  Promise.all([ladeFont(S.font), document.fonts ? document.fonts.ready : 0]).then(render);
  render();
})();
