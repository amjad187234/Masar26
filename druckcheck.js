/* Masar Druckdaten-Check – prüft PDF/JPG/PNG direkt im Browser (keine Übertragung an einen Server).
   PDF-Analyse mit pdf.js (selbst gehostet unter /js/pdfjs/, Apache-2.0, siehe /lizenzen/).
   Prüft: Format + Beschnitt (auch über TrimBox/BleedBox der PDF), effektive Bildauflösung je Bild, eingebettete Schriften,
   Farbraum, Sonderfarben, Texte zu nah am Rand, Haarlinien (< 0,25 pt) und sehr kleine Schrift (< 6 pt) im Endformat.
   Ergebnis als Ampel, Bildliste, Vorschau mit Linien, große Ansicht mit Zoom und druckbarer Prüfbericht. */
(function () {
  'use strict';
  var root = document.getElementById('druckcheck');
  if (!root) return;
  var $ = function (s) { return root.querySelector(s); };
  var WA = '491785143918';
  var MAX_MB = 200, MAX_PAGES = 30, THUMBS = 6, MAX_MARKS = 200;
  var HAIR = 0.25, SMALL = 6; // pt im Endformat

  // Produkt: Endformat (mm), empfohlene / minimale Auflösung (ppi am Endformat), Beschnitt (mm), Sicherheitsabstand (mm)
  var TYP = {
    papier: { rec: 300, min: 200, bleed: 3, safe: 3, name: 'Papier (Flyer, Karten, Briefpapier)' },
    plakat: { rec: 150, min: 100, bleed: 3, safe: 10, name: 'Plakat & Roll-up' },
    banner: { rec: 100, min: 60, bleed: 0, safe: 30, name: 'Banner & Großformat' },
    folie: { rec: 150, min: 100, bleed: 3, safe: 10, name: 'Folie, Schaufenster & Fahrzeug' }
  };
  var PROD = {
    vk: ['Visitenkarte 85 × 55 mm', 85, 55, 'papier'],
    a6: ['Flyer / Postkarte DIN A6 (105 × 148 mm)', 105, 148, 'papier'],
    dl: ['Flyer DIN lang (99 × 210 mm)', 99, 210, 'papier'],
    a5: ['Flyer DIN A5 (148 × 210 mm)', 148, 210, 'papier'],
    a4: ['Flyer / Briefpapier DIN A4 (210 × 297 mm)', 210, 297, 'papier'],
    a3: ['Plakat DIN A3 (297 × 420 mm)', 297, 420, 'papier'],
    a2: ['Plakat DIN A2 (420 × 594 mm)', 420, 594, 'plakat'],
    a1: ['Plakat DIN A1 (594 × 841 mm)', 594, 841, 'plakat'],
    a0: ['Plakat DIN A0 (841 × 1189 mm)', 841, 1189, 'plakat'],
    rollup: ['Roll-up 85 × 200 cm', 850, 2000, 'plakat']
  };

  var pdfjs = null;
  function loadPdfjs() {
    if (pdfjs) return Promise.resolve(pdfjs);
    return import('/js/pdfjs/pdf.min.js').then(function (m) {
      m.GlobalWorkerOptions.workerSrc = '/js/pdfjs/pdf.worker.min.js';
      pdfjs = m; return m;
    });
  }

  /* ---------- Hilfen ---------- */
  var MM = 25.4 / 72; // mm pro Punkt
  function r0(x) { return Math.round(x); }
  function r1(x) { return (Math.round(x * 10) / 10).toString().replace('.', ','); }
  function r2(x) { return (Math.round(x * 100) / 100).toString().replace('.', ','); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function fmtMM(w, h) { return w >= 1000 || h >= 1000 ? r1(w / 10) + ' × ' + r1(h / 10) + ' cm' : r0(w) + ' × ' + r0(h) + ' mm'; }
  function plural(n, a, b) { return n + ' ' + (n === 1 ? a : b); }
  function mul(m, n) { // m × n (PDF-Matrizen)
    return [m[0] * n[0] + m[1] * n[2], m[0] * n[1] + m[1] * n[3], m[2] * n[0] + m[3] * n[2], m[2] * n[1] + m[3] * n[3],
      m[4] * n[0] + m[5] * n[2] + n[4], m[4] * n[1] + m[5] * n[3] + n[5]];
  }
  function tRect(m, r) { // achsenparalleles Rechteck nach Transformation
    var xs = [], ys = [];
    [[r[0], r[1]], [r[2], r[1]], [r[0], r[3]], [r[2], r[3]]].forEach(function (p) {
      xs.push(m[0] * p[0] + m[2] * p[1] + m[4]); ys.push(m[1] * p[0] + m[3] * p[1] + m[5]);
    });
    return [Math.min.apply(null, xs), Math.min.apply(null, ys), Math.max.apply(null, xs), Math.max.apply(null, ys)];
  }
  function norm(r) { return [Math.min(r[0], r[2]), Math.min(r[1], r[3]), Math.max(r[0], r[2]), Math.max(r[1], r[3])]; }
  function hits(a, b) { return a[0] <= b[2] && a[2] >= b[0] && a[1] <= b[3] && a[3] >= b[1]; }
  function inside(a, b) { return a[0] >= b[0] && a[1] >= b[1] && a[2] <= b[2] && a[3] <= b[3]; }
  function inter(a, b) { var r = [Math.max(a[0], b[0]), Math.max(a[1], b[1]), Math.min(a[2], b[2]), Math.min(a[3], b[3])]; return r[2] > r[0] && r[3] > r[1] ? r : null; }
  function same(a, b, t) { return Math.abs(a[0] - b[0]) <= t && Math.abs(a[1] - b[1]) <= t && Math.abs(a[2] - b[2]) <= t && Math.abs(a[3] - b[3]) <= t; }
  function shrink(r, d) { var s = [r[0] + d, r[1] + d, r[2] - d, r[3] - d]; return s[2] > s[0] && s[3] > s[1] ? s : null; }
  function tick() { return new Promise(function (res) { setTimeout(res, 0); }); }

  function ziel() {
    var k = $('#dc-prod').value, t, W, H, name;
    if (k === 'eigen') {
      t = TYP[$('#dc-typ').value] || TYP.papier;
      W = parseFloat(String($('#dc-w').value).replace(',', '.')) * 10;
      H = parseFloat(String($('#dc-h').value).replace(',', '.')) * 10;
      if (!(W > 0 && H > 0)) return null;
      name = 'Eigene Größe ' + fmtMM(W, H);
    } else {
      var p = PROD[k]; t = TYP[p[3]]; W = p[1]; H = p[2]; name = p[0];
    }
    var b = parseFloat(String($('#dc-bleed').value).replace(',', '.'));
    if (!(b >= 0)) b = t.bleed;
    return { W: W, H: H, b: b, rec: t.rec, min: t.min, safe: t.safe, name: name };
  }

  // Seite (mm) gegen Ziel prüfen (ohne TrimBox) → Status, Text, Maßstab k (Endformat = Datei × k), Schnittrand in Datei-mm
  function formatCheck(w, h, z) {
    var tol = 1.2, best = null;
    [[z.W, z.H], [z.H, z.W]].forEach(function (o) {
      var W = o[0], H = o[1];
      if (best) return;
      if (Math.abs(w - (W + 2 * z.b)) <= tol && Math.abs(h - (H + 2 * z.b)) <= tol && z.b > 0)
        best = { s: 'ok', t: 'Endformat ' + fmtMM(W, H) + ' plus ' + r1(z.b) + ' mm Beschnitt je Seite – passt.', k: 1, inset: z.b };
      else if (Math.abs(w - W) <= tol && Math.abs(h - H) <= tol)
        best = z.b > 0
          ? { s: 'warn', t: 'Datei hat genau das Endformat, aber keinen Beschnitt. Reichen Farben oder Bilder bis zum Rand, brauchen sie ' + r1(z.b) + ' mm Zugabe je Seite – sonst können weiße Blitzer entstehen.', k: 1, inset: 0 }
          : { s: 'ok', t: 'Endformat ' + fmtMM(W, H) + ' – passt.', k: 1, inset: 0 };
    });
    if (best) return best;
    // Maßstab (z. B. 1:10 bei Bannern)
    [[z.W, z.H], [z.H, z.W]].forEach(function (o) {
      if (best) return;
      var W = o[0], H = o[1];
      [[W + 2 * z.b, H + 2 * z.b, z.b], [W, H, 0]].forEach(function (c) {
        if (best) return;
        var k = c[0] / w;
        if (k > 1.02 && Math.abs(c[1] / h - k) / k < 0.01)
          best = { s: scaleS(k), t: 'Datei ist im Maßstab 1:' + r1(k) + ' angelegt (Endformat ' + fmtMM(W, H) + (c[2] ? ' mit Beschnitt' : '') + '). ' + scaleT(k), k: k, inset: c[2] / k };
      });
    });
    if (best) return best;
    return { s: 'bad', t: 'Format passt nicht: Datei ' + fmtMM(w, h) + ', erwartet ' + fmtMM(z.W + 2 * z.b, z.H + 2 * z.b) + (z.b ? ' (Endformat ' + fmtMM(z.W, z.H) + ' + Beschnitt)' : '') + '. Bitte Format prüfen oder oben das richtige Produkt wählen.', k: w ? Math.max(z.W, z.H) / Math.max(w, h) : 1, inset: 0, mismatch: true };
  }

  // Verkleinert angelegt: ab 1:2 bei Großformaten üblich, darunter eher falsches Produkt oder falsche Größe
  function scaleS(k) { return k >= 1.9 ? 'info' : 'warn'; }
  function scaleT(k) {
    return k >= 1.9 ? 'Das ist bei Großformaten üblich – Auflösung, Linien und Schriftgrößen werden auf das Endformat umgerechnet.'
      : 'Die Datei wird beim Drucken vergrößert – bitte prüfen, ob das richtige Produkt gewählt ist. Auflösung, Linien und Schriftgrößen sind auf das Endformat umgerechnet.';
  }
  // Seite mit TrimBox: tw × th = Endformat laut PDF (mm), bl = Beschnitt je Seite (Datei-mm)
  function formatTrim(tw, th, bl, z) {
    var tol = 1.2, k = 0, W = 0, H = 0, pre = 'TrimBox erkannt (in der PDF hinterlegtes Endformat): ';
    [[z.W, z.H], [z.H, z.W]].forEach(function (o) { if (!k && Math.abs(tw - o[0]) <= tol && Math.abs(th - o[1]) <= tol) { k = 1; W = o[0]; H = o[1]; } });
    if (!k) [[z.W, z.H], [z.H, z.W]].forEach(function (o) { var kk = o[0] / tw; if (!k && kk > 1.02 && Math.abs(o[1] / th - kk) / kk < 0.01) { k = kk; W = o[0]; H = o[1]; } });
    if (!k) return { s: 'bad', t: pre + fmtMM(tw, th) + '. Erwartet wird ' + fmtMM(z.W, z.H) + '. Bitte Format prüfen oder oben das richtige Produkt wählen.', k: Math.max(z.W, z.H) / Math.max(tw, th), mismatch: true, box: true };
    var blF = bl * k, sc = k > 1.02 ? ' im Maßstab 1:' + r1(k) : '', e = 'Endformat ' + fmtMM(W, H) + sc;
    var okS = k > 1.02 ? scaleS(k) : 'ok', okT = k > 1.02 ? ' ' + scaleT(k) : '';
    var fit = k > 1.02 ? '.' : ' – passt.';
    if (z.b <= 0) return { s: okS, t: pre + e + fit + okT, k: k, box: true };
    if (blF >= z.b - 0.3) return { s: okS, t: pre + e + ' plus ' + r1(blF) + ' mm Beschnitt je Seite' + fit + okT, k: k, box: true };
    if (blF < 0.3) return { s: 'warn', t: pre + e + ' passt, aber es gibt keinen Beschnitt. Reichen Farben oder Bilder bis zum Rand, brauchen sie ' + r1(z.b) + ' mm Zugabe je Seite.', k: k, box: true };
    return { s: 'warn', t: pre + e + ' passt, der Beschnitt ist aber nur ' + r1(blF) + ' mm je Seite (empfohlen: ' + r1(z.b) + ' mm). Beim Schneiden können weiße Blitzer entstehen.', k: k, box: true };
  }

  function ppiStatus(ppi, z) { return ppi >= z.rec * 0.95 ? 'ok' : ppi >= z.min ? 'warn' : 'bad'; }

  /* ---------- Rohdaten-Scan (Seitenrahmen, Farbräume, Sonderfarben, PDF/X) ---------- */
  function inflate(bytes) {
    if (typeof DecompressionStream === 'undefined') return Promise.resolve('');
    try {
      var ds = new DecompressionStream('deflate');
      var w = ds.writable.getWriter(); w.write(bytes).catch(function () {}); w.close().catch(function () {});
      return new Response(ds.readable).arrayBuffer().then(function (ab) { return latin(new Uint8Array(ab)); }, function () { return ''; });
    } catch (e) { return Promise.resolve(''); }
  }
  function ascii85(u8) { // ASCII85-Kodierung (z. B. „/ASCII85Decode /FlateDecode“) → Bytes
    var outb = [], g = [], i, c;
    for (i = 0; i < u8.length; i++) {
      c = u8[i];
      if (c === 126) break; // ~> Ende
      if (c === 122 && !g.length) { outb.push(0, 0, 0, 0); continue; } // z = vier Nullbytes
      if (c < 33 || c > 117) continue;
      g.push(c - 33);
      if (g.length === 5) {
        var v = (((g[0] * 85 + g[1]) * 85 + g[2]) * 85 + g[3]) * 85 + g[4];
        outb.push((v >>> 24) & 255, (v >>> 16) & 255, (v >>> 8) & 255, v & 255); g = [];
      }
    }
    if (g.length > 1) {
      var n = g.length; while (g.length < 5) g.push(84);
      var w = (((g[0] * 85 + g[1]) * 85 + g[2]) * 85 + g[3]) * 85 + g[4];
      [(w >>> 24) & 255, (w >>> 16) & 255, (w >>> 8) & 255, w & 255].slice(0, n - 1).forEach(function (b) { outb.push(b); });
    }
    return new Uint8Array(outb);
  }
  function latin(u8) {
    var s = '', CH = 0x8000;
    for (var i = 0; i < u8.length; i += CH) s += String.fromCharCode.apply(null, u8.subarray(i, i + CH));
    return s;
  }
  var RE_PAGE = /\/Type\s*\/Page(?![A-Za-z])/;
  function rawScan(u8, prog) {
    var raw = latin(u8.length > 120e6 ? u8.subarray(0, 120e6) : u8);
    var res = { cmykImg: 0, rgbImg: 0, grayImg: 0, cmykOps: 0, rgbOps: 0, spots: {}, boxes: {}, common: null, pdfx: /GTS_PDFX|pdfxid:GTS_PDFXVersion|<pdfxid:/i.test(raw), outputIntent: /\/OutputIntents/.test(raw), transp: /\/SMask\s*\/|\/CA\s+0?\.\d|\/ca\s+0?\.\d/.test(raw) };
    var objs = {}, pageDicts = {}, jobs = [], budget = 60e6;
    var re = /(\d+)\s+0\s+obj\b/g, m;
    while ((m = re.exec(raw))) {
      var start = m.index + m[0].length;
      var sIdx = raw.indexOf('stream', start), eIdx = raw.indexOf('endobj', start);
      if (eIdx < 0) break;
      var isStream = sIdx > -1 && sIdx < eIdx;
      var dict = raw.slice(start, isStream ? sIdx : Math.min(eIdx, start + 4000));
      objs[m[1]] = dict.slice(0, 1500);
      if (!isStream && RE_PAGE.test(dict)) pageDicts[m[1]] = dict;
      if (isStream) {
        var ds = sIdx + 6; if (raw[ds] === '\r') ds++; if (raw[ds] === '\n') ds++;
        var es = raw.indexOf('endstream', ds); if (es < 0 || es > eIdx) es = eIdx;
        // Ende der Daten: /Length (direkt) oder Zeilenende vor „endstream“ abziehen – sonst lehnt DecompressionStream die Daten ab
        var ln = /\/Length\s+(\d+)(?!\s+\d+\s+R)/.exec(dict);
        if (ln && ds + (+ln[1]) <= es) es = ds + (+ln[1]);
        else while (es > ds && /[\r\n ]/.test(raw[es - 1])) es--;
        var a85 = /\/ASCII85Decode|\/A85\b/.test(dict);
        if (/\/Subtype\s*\/Image/.test(dict)) { jobs.push({ img: dict }); }
        else if (/\/Type\s*\/ObjStm/.test(dict) && es - ds < 25e6) {
          var first = /\/First\s+(\d+)/.exec(dict);
          if (first && !/\/Filter/.test(dict)) jobs.push({ os: raw.slice(ds, es), first: +first[1] });
          else if (first && /\/FlateDecode/.test(dict) && !/\/DecodeParms/.test(dict) && budget > 0) { budget -= es - ds; jobs.push({ osz: u8.subarray(ds, es), first: +first[1], a85: a85 }); }
        }
        else if (/\/FlateDecode/.test(dict) && !/\/Length[123]\b|\/FontFile|\/Type1C|\/CIDFontType0C|\/OpenType|\/XRef|\/Alternate|\/N\s+[134]\b/.test(dict) && es - ds < 25e6 && budget > 0) {
          budget -= es - ds; jobs.push({ z: u8.subarray(ds, es), a85: a85 });
        }
        re.lastIndex = es;
      } else re.lastIndex = eIdx;
    }
    function objStm(t, first) { // komprimierte Objekte (PDF 1.5+): Kopf „Nr Offset …“, ab /First die Objekte
      var hd = t.slice(0, first).trim().split(/\s+/), list = [];
      for (var i = 0; i + 1 < hd.length; i += 2) list.push([hd[i], first + (+hd[i + 1])]);
      list.forEach(function (o, i) {
        var txt = t.slice(o[1], i + 1 < list.length ? list[i + 1][1] : t.length);
        objs[o[0]] = txt.slice(0, 1500);
        if (RE_PAGE.test(txt)) pageDicts[o[0]] = txt.slice(0, 4000);
      });
    }
    function csOf(txt, depth) {
      if (!txt || depth > 3) return '';
      if (/DeviceCMYK|\/CalCMYK/.test(txt)) return 'cmyk';
      if (/DeviceRGB|\/CalRGB|\/Lab\b/.test(txt)) return 'rgb';
      if (/DeviceGray|\/CalGray/.test(txt)) return 'gray';
      var ic = /\/ICCBased\s+(\d+)\s+0\s+R/.exec(txt);
      if (ic) { var n = /\/N\s+(\d)/.exec(objs[ic[1]] || ''); return n ? (n[1] === '4' ? 'cmyk' : n[1] === '3' ? 'rgb' : 'gray') : ''; }
      var ref = /^\s*(\d+)\s+0\s+R/.exec(txt);
      if (ref) return csOf(objs[ref[1]], depth + 1);
      return '';
    }
    function box(txt, key) {
      var mm = new RegExp('/' + key + '\\s*(\\[[^\\]]*\\]|(\\d+)\\s+\\d+\\s+R)').exec(txt);
      if (!mm) return null;
      var a = mm[2] ? (/\[[^\]]*\]/.exec(objs[mm[2]] || '') || [''])[0] : mm[1];
      var n = (a.match(/-?\d*\.?\d+/g) || []).map(Number);
      return n.length === 4 && n.every(isFinite) ? norm(n) : null;
    }
    var texts = [raw.length > 30e6 ? '' : raw], done = 0;
    return jobs.reduce(function (p, j) {
      return p.then(function () {
        if (++done % 40 === 0) { prog(done / jobs.length, 'Farben und Seitenrahmen werden gelesen …'); return tick().then(step); }
        return step();
        function step() {
          if (j.img) {
            if (/\/ImageMask\s+true/.test(j.img)) return;
            var c = /\/ColorSpace\s*(\/\w+|\[[^\]]*\]|\d+\s+0\s+R)/.exec(j.img), cs = c ? csOf(c[1], 0) : '';
            if (cs === 'cmyk') res.cmykImg++; else if (cs === 'rgb') res.rgbImg++; else if (cs === 'gray') res.grayImg++;
            return;
          }
          if (j.os) { objStm(j.os, j.first); texts.push(j.os); return; }
          var zb = j.osz || j.z;
          return inflate(j.a85 ? ascii85(zb) : zb).then(function (t) { if (!t) return; if (j.osz) objStm(t, j.first); texts.push(t); });
        }
      });
    }, Promise.resolve()).then(function () {
      texts.forEach(function (t) {
        var a = t.match(/(?:^|[\s\]])(?:-?\d*\.?\d+\s+){4}[kK](?=\s)/g); if (a) res.cmykOps += a.length;
        var b = t.match(/(?:^|[\s\]])(?:-?\d*\.?\d+\s+){3}(?:rg|RG)(?=\s)/g); if (b) res.rgbOps += b.length;
        var sp = /\/Separation\s*\/([^\s\/\[\]<>()]+)/g, q;
        while ((q = sp.exec(t))) { var nm = q[1].replace(/#([0-9a-f]{2})/gi, function (_, h) { return String.fromCharCode(parseInt(h, 16)); }); if (!/^(All|None)$/.test(nm)) res.spots[nm] = 1; }
        if (!res.pdfx && /GTS_PDFX/.test(t)) res.pdfx = true;
        if (!res.transp && /\/SMask\s*\/|\/ca\s+0?\.\d/.test(t)) res.transp = true;
      });
      // Seitenrahmen je Seitenobjekt (Zuordnung später über die Objektnummer der Seite)
      var keys = Object.keys(pageDicts), sig = {};
      keys.forEach(function (n) {
        var d = pageDicts[n], b = { trim: box(d, 'TrimBox'), bleed: box(d, 'BleedBox'), art: box(d, 'ArtBox') };
        res.boxes[n] = b; sig[JSON.stringify(b)] = b;
      });
      var s = Object.keys(sig);
      if (s.length === 1 && sig[s[0]].trim) res.common = sig[s[0]];
      return res;
    });
  }

  /* ---------- PDF ---------- */
  function pathBox(a, O) { // Begrenzung eines Pfads aus constructPath-Argumenten (lokale Koordinaten)
    var ops = a[0], ar = a[1], i = 0, x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    function pt(x, y) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
    for (var j = 0; j < ops.length; j++) {
      var o = ops[j];
      if (o === O.moveTo || o === O.lineTo) { pt(ar[i], ar[i + 1]); i += 2; }
      else if (o === O.curveTo) { pt(ar[i], ar[i + 1]); pt(ar[i + 2], ar[i + 3]); pt(ar[i + 4], ar[i + 5]); i += 6; }
      else if (o === O.curveTo2 || o === O.curveTo3) { pt(ar[i], ar[i + 1]); pt(ar[i + 2], ar[i + 3]); i += 4; }
      else if (o === O.rectangle) { pt(ar[i], ar[i + 1]); pt(ar[i] + ar[i + 2], ar[i + 1] + ar[i + 3]); i += 4; }
    }
    return x1 >= x0 ? [x0, y0, x1, y1] : null;
  }

  function analyzePage(page, z, scan, fonts) {
    var vp1 = page.getViewport({ scale: 1 }), view = page.view.slice();
    var w = vp1.width * MM, h = vp1.height * MM;
    var pg = { i: page.pageNumber, page: page, vp1: vp1, w: w, h: h, imgs: [], edge: [], hair: [], small: [], nHair: 0, minLw: Infinity, nSmall: 0, minPt: Infinity, trim: null, safe: null };
    var bx = (page.ref && scan.boxes[page.ref.num]) || scan.common, trim = null;
    if (bx && bx.trim) { var t = inter(bx.trim, view); if (t && !same(t, view, 0.5)) trim = t; }
    if (trim) {
      var tr = norm(vp1.convertToViewportRectangle(trim)), lim = (bx.bleed && inter(bx.bleed, view)) || view;
      var bl = Math.max(0, Math.min(trim[0] - lim[0], trim[1] - lim[1], lim[2] - trim[2], lim[3] - trim[3])) * MM;
      pg.fc = formatTrim((tr[2] - tr[0]) * MM, (tr[3] - tr[1]) * MM, bl, z);
      pg.trim = trim;
    } else {
      pg.fc = formatCheck(w, h, z);
      if (!pg.fc.mismatch) pg.trim = shrink(view, pg.fc.inset / MM) || view;
    }
    var k = pg.fc.k;
    if (pg.trim) pg.safe = shrink(pg.trim, z.safe / k / MM);
    return page.getOperatorList().then(function (ol) {
      var O = pdfjs.OPS, ctm = [1, 0, 0, 1, 0, 0], lw = 1, st = [], cur = null, path = null, annot = 0;
      for (var j = 0; j < ol.fnArray.length; j++) {
        var fn = ol.fnArray[j], a = ol.argsArray[j];
        if (annot) { if (fn === O.endAnnotation) annot--; else if (fn === O.beginAnnotation) annot++; continue; }
        if (fn === O.beginAnnotation) { annot = 1; continue; }
        if (fn === O.save) st.push([ctm, lw]);
        else if (fn === O.restore) { var sv = st.pop(); if (sv) { ctm = sv[0]; lw = sv[1]; } }
        else if (fn === O.transform) ctm = mul(a, ctm);
        else if (fn === O.paintFormXObjectBegin) { st.push([ctm, lw]); if (a && a[0]) ctm = mul(a[0], ctm); }
        else if (fn === O.paintFormXObjectEnd) { var sf = st.pop(); if (sf) { ctm = sf[0]; lw = sf[1]; } }
        else if (fn === O.setLineWidth) lw = a[0];
        else if (fn === O.setGState && a && a[0]) a[0].forEach(function (kv) { if (kv[0] === 'LW') lw = kv[1]; });
        else if (fn === O.constructPath) path = pathBox(a, O);
        else if (fn === O.stroke || fn === O.closeStroke || fn === O.fillStroke || fn === O.eoFillStroke || fn === O.closeFillStroke || fn === O.closeEOFillStroke) {
          if (path) {
            var eff = lw * Math.sqrt(Math.abs(ctm[0] * ctm[3] - ctm[1] * ctm[2])) * k; // Linienstärke in pt am Endformat
            if (eff < HAIR) {
              var bb = tRect(ctm, path);
              if (!pg.trim || hits(bb, pg.trim)) { // Schnittmarken und Infos außerhalb des Endformats zählen nicht
                pg.nHair++; if (eff < pg.minLw) pg.minLw = eff;
                if (pg.hair.length < MAX_MARKS) pg.hair.push(bb);
              }
            }
          }
          path = null;
        }
        else if (fn === O.paintImageXObject || fn === O.paintInlineImageXObject) {
          var pw = fn === O.paintImageXObject ? a[1] : a[0] && a[0].width, ph = fn === O.paintImageXObject ? a[2] : a[0] && a[0].height;
          var sw = Math.hypot(ctm[0], ctm[1]) * MM, sh = Math.hypot(ctm[2], ctm[3]) * MM;
          if (pw && ph && sw > 3 && sh > 3) {
            var ppi = Math.min(pw / (sw / 25.4), ph / (sh / 25.4)) / k;
            pg.imgs.push({ pw: pw, ph: ph, sw: sw * k, sh: sh * k, ppi: ppi, r: tRect(ctm, [0, 0, 1, 1]) });
          }
        } else if (fn === O.setFont && a) cur = a[0];
        else if (cur && (fn === O.showText || fn === O.showSpacedText || fn === O.nextLineShowText || fn === O.nextLineSetSpacingShowText) && page.commonObjs.has(cur)) {
          var f = page.commonObjs.get(cur);
          if (f && !f.isType3Font) {
            var nm = String(f.name || cur).replace(/^[A-Z]{6}\+/, '');
            if (!fonts[nm]) fonts[nm] = { missing: false };
            if (f.missingFile) fonts[nm].missing = true;
          }
        }
      }
      return page.getTextContent();
    }).then(function (tc) {
      tc.items.forEach(function (it) {
        if (!it.str || !it.str.trim()) return;
        var m = it.transform, s = Math.hypot(m[2], m[3]) || it.height || 0, n = Math.hypot(m[0], m[1]) || 1;
        var ux = m[0] / n, uy = m[1] / n, vn = Math.hypot(m[2], m[3]) || 1, vx = m[2] / vn, vy = m[3] / vn, x = m[4], y = m[5], wd = it.width || 0;
        var xs = [x, x + ux * wd, x + vx * s, x + ux * wd + vx * s], ys = [y, y + uy * wd, y + vy * s, y + uy * wd + vy * s];
        var r = [Math.min.apply(null, xs), Math.min.apply(null, ys), Math.max.apply(null, xs), Math.max.apply(null, ys)];
        if (pg.trim && !hits(r, pg.trim)) return; // Text komplett außerhalb des Endformats (z. B. Infozeile im Beschnitt)
        var txt = it.str.trim().slice(0, 40);
        if (!pg.fc.mismatch && pg.safe && !inside(r, pg.safe)) pg.edge.push({ r: r, s: txt });
        var pt = s * k;
        if (pt > 0 && pt < SMALL - 0.05) {
          pg.nSmall++; if (pt < pg.minPt) { pg.minPt = pt; pg.minTxt = txt; }
          if (pg.small.length < MAX_MARKS) pg.small.push(r);
        }
      });
      return pg;
    });
  }

  function checkPdf(file, buf, z, prog) {
    var u8 = new Uint8Array(buf), out = { pages: [] }, fonts = {};
    prog(0, 'Farben und Seitenrahmen werden gelesen …');
    return rawScan(u8, function (f, t) { prog(f * 0.15, t); }).then(function (scan) {
      out.scan = scan;
      return loadPdfjs();
    }).then(function (lib) {
      return lib.getDocument({ data: u8.slice(0), isEvalSupported: false, disableFontFace: false, useSystemFonts: false, verbosity: 0 }).promise;
    }).then(function (doc) {
      out.doc = doc; out.n = doc.numPages;
      return doc.getMetadata().catch(function () { return null; });
    }).then(function (meta) {
      out.info = (meta && meta.info) || {};
      var n = Math.min(out.n, MAX_PAGES), chain = Promise.resolve();
      for (var i = 1; i <= n; i++) (function (i) {
        chain = chain.then(function () {
          prog(0.15 + 0.85 * (i - 1) / n, n > 1 ? 'Seite ' + i + ' von ' + n + ' wird geprüft …' : 'Seite wird geprüft …');
          return tick();
        }).then(function () { return out.doc.getPage(i); })
          .then(function (page) { return analyzePage(page, z, out.scan, fonts); })
          .then(function (pg) { out.pages.push(pg); });
      })(i);
      return chain.then(function () { out.fonts = fonts; prog(1, 'Ergebnis wird erstellt …'); return out; });
    });
  }

  function pageList(arr) { return arr.length > 8 ? arr.slice(0, 8).join(', ') + ' …' : arr.join(', '); }

  function pdfChecks(o, z) {
    var c = [], P = o.pages;
    // Format
    var bad = P.filter(function (p) { return p.fc.s === 'bad'; }), warn = P.filter(function (p) { return p.fc.s === 'warn'; });
    var first = P[0].fc;
    var sizes = {}; P.forEach(function (p) { sizes[fmtMM(Math.max(p.w, p.h), Math.min(p.w, p.h))] = 1; }); // Hoch- und Querformat zählen gleich
    if (bad.length) c.push(['bad', 'Format & Beschnitt', (P.length > 1 ? 'Seite ' + pageList(bad.map(function (p) { return p.i; })) + ': ' : '') + bad[0].fc.t]);
    else if (warn.length) c.push(['warn', 'Format & Beschnitt', (P.length > 1 ? 'Seite ' + pageList(warn.map(function (p) { return p.i; })) + ': ' : '') + warn[0].fc.t]);
    else c.push([first.s, 'Format & Beschnitt', first.t]);
    if (Object.keys(sizes).length > 1) c.push(['warn', 'Seitengrößen', 'Die Seiten haben unterschiedliche Größen: ' + Object.keys(sizes).slice(0, 6).join(' · ') + '.']);
    // Seitenzahl + Datei
    var inf = o.info || {}, prod = String(inf.Creator || inf.Producer || '').trim().slice(0, 60);
    if (/^(anonymous|unknown|unspecified|none)$/i.test(prod)) prod = '';
    c.push(['info', 'Seiten & Datei', o.n + (o.n === 1 ? ' Seite' : ' Seiten') + (o.n > MAX_PAGES ? ' – geprüft wurden die ersten ' + MAX_PAGES : '') +
      (inf.PDFFormatVersion ? ' · PDF ' + esc(inf.PDFFormatVersion) : '') + (prod ? ' · erstellt mit ' + esc(prod) : '') + '.' +
      (o.n === 2 ? ' Bei Flyern und Karten: Seite 1 = Vorderseite, Seite 2 = Rückseite.' : '')]);
    // Bilder
    var imgs = []; P.forEach(function (p) { p.imgs.forEach(function (im) { im.p = p.i; im.s = ppiStatus(im.ppi, z); imgs.push(im); }); });
    o.imgs = imgs.sort(function (a, b) { return a.ppi - b.ppi; });
    if (!imgs.length) c.push(['ok', 'Bildauflösung', 'Keine Pixelbilder gefunden – nur Vektoren und Text. Das druckt immer scharf.']);
    else {
      var w0 = imgs[0], s = w0.s, nLow = imgs.filter(function (i) { return i.ppi < z.min; }).length;
      var t = plural(imgs.length, 'Bild', 'Bilder') + ' gefunden. Niedrigste Auflösung: ' + r0(w0.ppi) + ' ppi (Seite ' + w0.p + ', ' + w0.pw + ' × ' + w0.ph + ' Pixel auf ' + fmtMM(w0.sw, w0.sh) + '). Richtwert für dieses Produkt: ' + z.rec + ' ppi, mindestens ' + z.min + ' ppi.';
      if (s === 'bad') t += ' ' + nLow + (nLow === 1 ? ' Bild wirkt' : ' Bilder wirken') + ' im Druck wahrscheinlich unscharf oder pixelig (in der Vorschau markiert) – besser ein größeres Original verwenden.';
      else if (s === 'warn') t += ' Das geht, wirkt aus der Nähe aber etwas weicher.';
      c.push([s, 'Bildauflösung', t]);
    }
    // Schriften
    var fn = Object.keys(o.fonts), miss = fn.filter(function (f) { return o.fonts[f].missing; });
    if (miss.length) c.push(['bad', 'Schriften', 'Nicht eingebettet: ' + miss.slice(0, 6).map(esc).join(', ') + (miss.length > 6 ? ' …' : '') + '. Ohne eingebettete Schrift kann der Text beim Drucken anders aussehen. Lösung: beim PDF-Export „Schriften einbetten“ wählen oder Text in Pfade umwandeln.']);
    else if (fn.length) c.push(['ok', 'Schriften', fn.length === 1 ? 'Die Schrift ist eingebettet.' : 'Alle ' + fn.length + ' Schriften sind eingebettet.']);
    else c.push(['ok', 'Schriften', 'Keine Schriften im PDF – Texte sind in Pfade umgewandelt oder es gibt keinen Text.']);
    // Schriftgröße
    var nS = 0, sp = [], minPt = Infinity, minTxt = '';
    P.forEach(function (p) { if (p.nSmall) { nS += p.nSmall; sp.push(p.i); if (p.minPt < minPt) { minPt = p.minPt; minTxt = p.minTxt; } } });
    if (nS) c.push(['warn', 'Schriftgröße', plural(nS, 'Textstelle ist', 'Textstellen sind') + ' im Endformat kleiner als ' + SMALL + ' pt (kleinste: ' + r1(minPt) + ' pt, Seite ' + pageList(sp) + ', in der Vorschau blau markiert), z. B. „' + esc(minTxt) + '“. So kleine Schrift ist schwer lesbar und kann im Druck zulaufen.']);
    else if (fn.length) c.push(['ok', 'Schriftgröße', 'Alle Texte sind im Endformat mindestens ' + SMALL + ' pt groß.']);
    // Linien
    var nH = 0, hp = [], minLw = Infinity;
    P.forEach(function (p) { if (p.nHair) { nH += p.nHair; hp.push(p.i); minLw = Math.min(minLw, p.minLw); } });
    if (nH) c.push(['warn', 'Haarlinien', plural(nH, 'Linie ist', 'Linien sind') + ' im Endformat dünner als ' + r2(HAIR) + ' pt (≈ 0,09 mm; dünnste: ' + (minLw < 0.005 ? 'Linienstärke 0' : r2(minLw) + ' pt') + ', Seite ' + pageList(hp) + ', in der Vorschau orange markiert). So feine Linien können im Druck brechen oder verschwinden – besser mindestens ' + r2(HAIR) + ' pt verwenden.']);
    else c.push(['ok', 'Haarlinien', 'Keine Linien dünner als ' + r2(HAIR) + ' pt im Endformat gefunden.']);
    // Farben
    var sc = o.scan, rgb = sc.rgbImg + sc.rgbOps, cmyk = sc.cmykImg + sc.cmykOps;
    if (sc.pdfx) c.push(['ok', 'Farben', 'PDF/X-Datei erkannt – das ist ein Druckstandard mit festgelegtem Farbprofil.' + (rgb ? ' Enthält auch RGB-Elemente, die über das Profil umgerechnet werden.' : '')]);
    else if (rgb && !cmyk) c.push(['warn', 'Farben', 'Die Datei ist in RGB (Bildschirmfarben). Gedruckt wird in CMYK – wir rechnen die Farben um. Sehr leuchtende Töne wie Neongrün, Orange oder kräftiges Blau können dabei etwas matter werden.']);
    else if (rgb && cmyk) c.push(['warn', 'Farben', 'Gemischte Farben: CMYK und RGB (' + (sc.rgbImg ? sc.rgbImg + ' RGB-Bild' + (sc.rgbImg > 1 ? 'er' : '') : 'RGB-Flächen') + '). Die RGB-Teile werden für den Druck umgerechnet und können leicht abweichen.']);
    else if (cmyk) c.push(['ok', 'Farben', 'Farben sind in CMYK angelegt – passend für den Druck.']);
    else c.push(['info', 'Farben', 'Farbraum nicht eindeutig erkennbar (nur Graustufen oder komprimierte Struktur). Wir prüfen das bei Ihrer Bestellung.']);
    var spots = Object.keys(sc.spots);
    if (spots.length) {
      var cut = spots.filter(function (s) { return /cut|kontur|contour|schnitt|stanz|plot/i.test(s); });
      c.push(['info', 'Sonderfarben', 'Gefunden: ' + spots.slice(0, 8).map(esc).join(', ') + '.' + (cut.length ? ' „' + esc(cut[0]) + '“ sieht nach einer Schneidekontur aus – gut für Aufkleber und Folien.' : ' Sonderfarben (z. B. Pantone, HKS) werden im Digitaldruck in CMYK nachgebildet – sagen Sie uns, wenn ein Farbton exakt stimmen muss.')]);
    }
    // Rand
    var edge = 0, ep = []; P.forEach(function (p) { if (p.edge.length) { edge += p.edge.length; ep.push(p.i); } });
    if (P.some(function (p) { return p.fc.mismatch; })) { /* ohne passendes Format keine Randprüfung */ }
    else if (edge) c.push(['warn', 'Sicherheitsabstand', plural(edge, 'Textstelle liegt', 'Textstellen liegen') + ' näher als ' + z.safe + ' mm am Schnitt (Seite ' + pageList(ep) + ', in der Vorschau rot markiert), z. B. „' + esc(P.filter(function (p) { return p.edge.length; })[0].edge[0].s) + '“. Beim Schneiden kann es knapp werden – Text weiter nach innen setzen.']);
    else c.push(['ok', 'Sicherheitsabstand', 'Alle Texte halten mindestens ' + z.safe + ' mm Abstand zum Schnitt.']);
    if (sc.transp) c.push(['info', 'Transparenzen', 'Die Datei enthält Transparenzen (z. B. Schatten oder halbtransparente Flächen). Meist kein Problem – bei Fehldarstellungen hilft der Export als PDF/X-4.']);
    return c;
  }

  /* ---------- Pixelbild ---------- */
  function jpegInfo(u8) {
    if (u8[0] !== 0xFF || u8[1] !== 0xD8) return null;
    var i = 2, info = {};
    while (i < u8.length - 9) {
      if (u8[i] !== 0xFF) { i++; continue; }
      var mk = u8[i + 1], len = (u8[i + 2] << 8) | u8[i + 3];
      if (mk >= 0xC0 && mk <= 0xCF && mk !== 0xC4 && mk !== 0xC8 && mk !== 0xCC) {
        info.h = (u8[i + 5] << 8) | u8[i + 6]; info.w = (u8[i + 7] << 8) | u8[i + 8]; info.comp = u8[i + 9]; return info;
      }
      i += 2 + len;
    }
    return info;
  }
  function checkImage(file, buf, z) {
    var u8 = new Uint8Array(buf);
    return new Promise(function (res, rej) {
      var url = URL.createObjectURL(file), im = new Image();
      im.onload = function () { res({ img: im, url: url }); };
      im.onerror = function () { rej(new Error('bild')); };
      im.src = url;
    }).then(function (r) {
      var w = r.img.naturalWidth, h = r.img.naturalHeight, c = [];
      var land = w >= h, W = land === (z.W >= z.H) ? z.W : z.H, H = W === z.W ? z.H : z.W;
      var FW = W + 2 * z.b, FH = H + 2 * z.b;
      var ppi = Math.min(w / (FW / 25.4), h / (FH / 25.4)), s = ppiStatus(ppi, z);
      var t = w + ' × ' + h + ' Pixel auf ' + fmtMM(FW, FH) + ' (Endformat' + (z.b ? ' + Beschnitt' : '') + ') = ' + r0(ppi) + ' ppi. Richtwert: ' + z.rec + ' ppi, mindestens ' + z.min + ' ppi.';
      if (s === 'bad') t += ' Das Bild wirkt in dieser Größe wahrscheinlich unscharf oder pixelig.';
      else if (s === 'warn') t += ' Das geht, wirkt aus der Nähe aber etwas weicher.';
      c.push([s, 'Auflösung', t]);
      var maxW = w / z.rec * 25.4, maxH = h / z.rec * 25.4;
      c.push(['info', 'Maximale Druckgröße', 'Bei ' + z.rec + ' ppi reicht dieses Bild für bis zu ' + fmtMM(maxW, maxH) + '.']);
      var ar = (w / h) / (FW / FH);
      if (Math.abs(ar - 1) > 0.02) c.push(['warn', 'Seitenverhältnis', 'Das Bild hat ein anderes Seitenverhältnis als das Format (' + fmtMM(FW, FH) + '). Es wird beschnitten oder es bleiben Ränder – in der Vorschau sehen Sie, was wegfällt.']);
      else c.push(['ok', 'Seitenverhältnis', 'Passt zum Format.']);
      var j = jpegInfo(u8);
      if (j && j.comp === 4) c.push(['ok', 'Farben', 'JPG in CMYK – passend für den Druck.']);
      else c.push(['warn', 'Farben', (j ? 'JPG' : file.type === 'image/png' ? 'PNG' : 'Bild') + ' in RGB (Bildschirmfarben). Wir rechnen es für den Druck in CMYK um; sehr leuchtende Töne können etwas matter werden.']);
      if (file.type === 'image/png' || file.type === 'image/webp') c.push(['info', 'Text & Logos', 'Pixelbilder werden beim Vergrößern unscharf. Für Logos und Text ist ein PDF oder SVG (Vektor) besser.']);
      return { checks: c, img: r.img, url: r.url, w: w, h: h, FW: FW, FH: FH, z: z };
    });
  }

  /* ---------- Vorschau-Quellen (gemeinsam für Miniaturen und große Ansicht) ----------
     geo: Seite in eigenen Einheiten (PDF: pt bei Maßstab 1, oben links; Bild: mm) mit Schnitt, Sicherheitslinie, Markierungen */
  function pdfSource(o, z) {
    return {
      n: o.pages.length,
      label: function (i) { var p = o.pages[i]; return 'Seite ' + p.i + ' · ' + fmtMM(p.w * p.fc.k, p.h * p.fc.k); },
      geo: function (i) {
        var p = o.pages[i], vp = p.vp1;
        if (!p.geo) {
          var vr = function (r) { return norm(vp.convertToViewportRectangle(r)); }, marks = [];
          p.edge.forEach(function (e) { marks.push({ k: 'edge', r: vr(e.r) }); });
          p.hair.forEach(function (r) { marks.push({ k: 'hair', r: vr(r) }); });
          p.small.forEach(function (r) { marks.push({ k: 'small', r: vr(r) }); });
          p.imgs.forEach(function (im) { if (ppiStatus(im.ppi, z) === 'bad') marks.push({ k: 'img', r: vr(im.r) }); });
          p.geo = { W: vp.width, H: vp.height, trim: p.trim && vr(p.trim), safe: p.safe && vr(p.safe), marks: marks };
        }
        return p.geo;
      },
      render: function (i, ctx, px) {
        var p = o.pages[i], vp = p.page.getViewport({ scale: px / p.vp1.width });
        var task = p.page.render({ canvasContext: ctx, viewport: vp });
        return { promise: task.promise, cancel: function () { try { task.cancel(); } catch (e) {} } };
      }
    };
  }
  function imgSource(r) {
    var b = r.z.b, g = { W: r.FW, H: r.FH, trim: b > 0 ? [b, b, r.FW - b, r.FH - b] : null, marks: [] };
    g.safe = shrink([b, b, r.FW - b, r.FH - b], r.z.safe);
    return {
      n: 1,
      label: function () { return fmtMM(r.FW, r.FH) + ' (randlos gefüllt)'; },
      geo: function () { return g; },
      render: function (i, ctx, px) {
        var cw = ctx.canvas.width, ch = ctx.canvas.height;
        ctx.fillStyle = '#eef2f2'; ctx.fillRect(0, 0, cw, ch);
        var s = Math.max(cw / r.w, ch / r.h), dw = r.w * s, dh = r.h * s; // füllend (wie beim Druck randlos)
        ctx.imageSmoothingQuality = 'high';
        ctx.drawImage(r.img, (cw - dw) / 2, (ch - dh) / 2, dw, dh);
        return { promise: Promise.resolve(), cancel: function () {} };
      }
    };
  }

  var MARK = { edge: ['#d63b3b', 'rgba(214,59,59,.18)'], hair: ['#c25e00', 'rgba(194,94,0,.16)'], small: ['#132e50', 'rgba(19,46,80,.14)'], img: ['#b3261e', 'rgba(179,38,30,.10)'] };
  // Linien und Markierungen zeichnen: s = Pixel je geo-Einheit, d = Pixel je CSS-Pixel
  function overlay(ctx, s, g, show, d) {
    var cw = g.W * s, ch = g.H * s;
    ctx.save();
    if (show.trim && g.trim) {
      var t = g.trim.map(function (v) { return v * s; });
      ctx.fillStyle = 'rgba(19,46,80,.28)';
      ctx.fillRect(0, 0, cw, t[1]); ctx.fillRect(0, t[3], cw, ch - t[3]);
      ctx.fillRect(0, t[1], t[0], t[3] - t[1]); ctx.fillRect(t[2], t[1], cw - t[2], t[3] - t[1]);
      ctx.lineWidth = 2 * d; ctx.setLineDash([8 * d, 5 * d]); ctx.strokeStyle = '#d63b3b';
      ctx.strokeRect(t[0], t[1], t[2] - t[0], t[3] - t[1]);
    }
    if (show.safe && g.safe) {
      ctx.lineWidth = 2 * d; ctx.setLineDash([8 * d, 5 * d]); ctx.strokeStyle = '#177567';
      ctx.strokeRect(g.safe[0] * s, g.safe[1] * s, (g.safe[2] - g.safe[0]) * s, (g.safe[3] - g.safe[1]) * s);
    }
    if (show.marks) {
      g.marks.forEach(function (m) {
        var c = MARK[m.k], p = 3 * d;
        ctx.setLineDash(m.k === 'img' ? [4 * d, 3 * d] : []);
        ctx.lineWidth = (m.k === 'img' ? 3 : 1.5) * d; ctx.strokeStyle = c[0]; ctx.fillStyle = c[1];
        var x = m.r[0] * s - p, y = m.r[1] * s - p, w = (m.r[2] - m.r[0]) * s + 2 * p, h = (m.r[3] - m.r[1]) * s + 2 * p;
        ctx.fillRect(x, y, w, h); ctx.strokeRect(x, y, w, h);
      });
    }
    ctx.restore();
  }
  function legend(kinds) {
    var it = function (c, t) { return '<span class="dc-li"><i class="' + c + '" aria-hidden="true"></i>' + t + '</span>'; };
    return '<p class="dc-legend">' + it('dc-l1', 'Schnittkante') + it('dc-l2', 'Sicherheitsabstand') + it('dc-l3', 'Beschnitt (wird abgeschnitten)') +
      (kinds.edge ? it('dc-m dc-m-edge', 'Text am Rand') : '') + (kinds.hair ? it('dc-m dc-m-hair', 'Haarlinie') : '') +
      (kinds.small ? it('dc-m dc-m-small', 'Kleine Schrift') : '') + (kinds.img ? it('dc-m dc-m-img', 'Bild unscharf') : '') + '</p>';
  }
  function thumbSize(W, H) {
    var maxW = Math.min(root.clientWidth - 32, 420), maxH = 420, sc = Math.min(maxW / W, maxH / H);
    return [Math.max(60, Math.round(W * sc)), Math.max(60, Math.round(H * sc))];
  }
  function renderPreviews(src, box, extra) {
    var n = Math.min(src.n, THUMBS), kinds = {}, chain = Promise.resolve();
    for (var i = 0; i < n; i++) src.geo(i).marks.forEach(function (m) { kinds[m.k] = 1; });
    box.innerHTML = '<h3 class="dc-h3">Vorschau</h3>' + legend(kinds) + '<div class="dc-thumbs"></div>' +
      '<p class="dc-small">' + (src.n > 1 ? 'Seite antippen für die große Ansicht mit Zoom und allen ' + src.n + ' Seiten.' : 'Vorschau antippen für die große Ansicht mit Zoom.') + (extra || '') + '</p>';
    var wrap = box.querySelector('.dc-thumbs'), dpr = Math.min(window.devicePixelRatio || 1, 2);
    for (var j = 0; j < n; j++) (function (i) {
      var g = src.geo(i), sz = thumbSize(g.W, g.H);
      var btn = document.createElement('button'); btn.type = 'button'; btn.className = 'dc-thumb'; btn.setAttribute('data-i', i);
      btn.setAttribute('aria-label', src.label(i) + ' – groß anzeigen');
      var cv = document.createElement('canvas'); cv.width = sz[0] * dpr; cv.height = sz[1] * dpr; cv.style.width = sz[0] + 'px'; cv.style.height = sz[1] + 'px';
      var cap = document.createElement('span'); cap.className = 'dc-cap'; cap.textContent = src.label(i);
      btn.appendChild(cv); btn.appendChild(cap); wrap.appendChild(btn);
      chain = chain.then(function () {
        var ctx = cv.getContext('2d'); ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, cv.width, cv.height);
        return src.render(i, ctx, cv.width).promise.then(function () {
          overlay(ctx, cv.width / g.W, g, { trim: 1, safe: 1, marks: 1 }, dpr);
        }, function () {});
      });
    })(j);
    return chain;
  }

  /* ---------- Große Ansicht (Lightbox) ---------- */
  var LB = null;
  function lightbox() {
    if (LB) return LB;
    var dlg = document.createElement('dialog');
    dlg.className = 'dc-lb'; dlg.setAttribute('aria-labelledby', 'dc-lb-t');
    dlg.innerHTML = '<div class="dc-lb-bar"><h2 class="dc-lb-t" id="dc-lb-t">Vorschau</h2>' +
      '<div class="dc-lb-grp dc-lb-nav"><button type="button" data-a="prev" aria-label="Vorherige Seite">‹</button><button type="button" data-a="next" aria-label="Nächste Seite">›</button></div>' +
      '<div class="dc-lb-grp"><button type="button" data-a="out" aria-label="Verkleinern">−</button><output class="dc-lb-z" aria-live="polite">100 %</output><button type="button" data-a="in" aria-label="Vergrößern">+</button><button type="button" data-a="fit" class="dc-lb-fit">Einpassen</button></div>' +
      '<button type="button" data-a="close" class="dc-lb-x" aria-label="Große Ansicht schließen">✕</button></div>' +
      '<div class="dc-lb-opts" role="group" aria-label="Linien anzeigen"><label><input type="checkbox" data-o="trim" checked> Schnittkante</label><label><input type="checkbox" data-o="safe" checked> Sicherheitsabstand</label><label><input type="checkbox" data-o="marks" checked> Markierte Probleme</label></div>' +
      '<div class="dc-lb-view" role="region" tabindex="0" aria-label="Seitenansicht. Verschieben mit Pfeiltasten oder Ziehen, Zoom mit Plus und Minus."><div class="dc-lb-stage"><canvas class="dc-lb-c" role="img"></canvas><canvas class="dc-lb-o" aria-hidden="true"></canvas></div></div>' +
      '<p class="dc-lb-help">Ziehen zum Verschieben · Strg + Mausrad oder zwei Finger zum Zoomen · Esc schließt</p>';
    document.body.appendChild(dlg);
    var q = function (s) { return dlg.querySelector(s); };
    var view = q('.dc-lb-view'), stage = q('.dc-lb-stage'), cv = q('.dc-lb-c'), ov = q('.dc-lb-o'), zOut = q('.dc-lb-z');
    var st = { src: null, i: 0, zoom: 1, show: { trim: true, safe: true, marks: true }, task: null, timer: 0, opener: null, css: [0, 0] };

    function fit() { var g = st.src.geo(st.i); return Math.min((view.clientWidth - 24) / g.W, (view.clientHeight - 24) / g.H); }
    function layout() { // CSS-Größe sofort setzen (Bild wird kurz gestreckt), scharf neu zeichnen nach kurzer Pause
      var g = st.src.geo(st.i), s = fit() * st.zoom, w = Math.max(40, Math.round(g.W * s)), h = Math.max(40, Math.round(g.H * s));
      st.css = [w, h];
      [stage, cv, ov].forEach(function (el) { el.style.width = w + 'px'; el.style.height = h + 'px'; });
      zOut.textContent = Math.round(st.zoom * 100) + ' %';
      clearTimeout(st.timer); st.timer = setTimeout(draw, 140);
    }
    function draw() {
      var g = st.src.geo(st.i), dpr = Math.min(window.devicePixelRatio || 1, 2), w = st.css[0] * dpr, h = st.css[1] * dpr;
      var lim = Math.min(1, 8192 / Math.max(w, h), Math.sqrt(16e6 / (w * h))); // Speichergrenze der Browser
      w = Math.max(1, Math.round(w * lim)); h = Math.max(1, Math.round(h * lim));
      if (st.task) st.task.cancel();
      var tmp = document.createElement('canvas'); tmp.width = w; tmp.height = h;
      var ctx = tmp.getContext('2d'); ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, w, h);
      var task = st.task = st.src.render(st.i, ctx, w), idx = st.i;
      task.promise.then(function () {
        if (st.task !== task || idx !== st.i) return;
        cv.width = w; cv.height = h; cv.getContext('2d').drawImage(tmp, 0, 0);
        ov.width = w; ov.height = h; drawOv();
      }, function () {});
    }
    function drawOv() {
      var g = st.src.geo(st.i), ctx = ov.getContext('2d');
      ctx.clearRect(0, 0, ov.width, ov.height);
      overlay(ctx, ov.width / g.W, g, st.show, ov.width / st.css[0]);
    }
    function zoomTo(nz, cx, cy) {
      nz = Math.max(0.5, Math.min(12, nz));
      if (cx === undefined) { cx = view.clientWidth / 2; cy = view.clientHeight / 2; }
      var ow = st.css[0], oh = st.css[1], sr = stage.getBoundingClientRect(), vr = view.getBoundingClientRect();
      var fx = (vr.left + cx - sr.left) / ow, fy = (vr.top + cy - sr.top) / oh;
      st.zoom = nz; layout();
      var nr = stage.getBoundingClientRect();
      view.scrollLeft += (nr.left + fx * st.css[0]) - (vr.left + cx);
      view.scrollTop += (nr.top + fy * st.css[1]) - (vr.top + cy);
    }
    function show(i) {
      st.i = Math.max(0, Math.min(st.src.n - 1, i)); st.zoom = 1;
      q('.dc-lb-t').textContent = st.src.label(st.i) + (st.src.n > 1 ? ' (' + (st.i + 1) + ' von ' + st.src.n + ')' : '');
      cv.setAttribute('aria-label', 'Vorschau ' + st.src.label(st.i));
      q('.dc-lb-nav').hidden = st.src.n < 2;
      q('[data-a="prev"]').disabled = st.i === 0; q('[data-a="next"]').disabled = st.i >= st.src.n - 1;
      cv.width = ov.width = 1; cv.height = ov.height = 1;
      layout(); view.scrollTop = 0; view.scrollLeft = 0;
    }
    dlg.addEventListener('click', function (e) {
      var b = e.target.closest('[data-a]');
      if (!b) return;
      var a = b.getAttribute('data-a');
      if (a === 'close') dlg.close();
      else if (a === 'prev') show(st.i - 1);
      else if (a === 'next') show(st.i + 1);
      else if (a === 'in') zoomTo(st.zoom * 1.4);
      else if (a === 'out') zoomTo(st.zoom / 1.4);
      else if (a === 'fit') { st.zoom = 1; layout(); }
    });
    dlg.addEventListener('change', function (e) { var o = e.target.getAttribute('data-o'); if (o) { st.show[o] = e.target.checked; drawOv(); } });
    dlg.addEventListener('keydown', function (e) {
      if (e.key === 'Tab') { // Fokus im Dialog halten
        var f = [].filter.call(dlg.querySelectorAll('button,input,[tabindex="0"]'), function (el) { return !el.disabled && el.offsetParent !== null; });
        if (!f.length) return;
        var a = f[0], z = f[f.length - 1];
        if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); }
        else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); }
        return;
      }
      if (e.target.tagName === 'INPUT') return;
      if (e.key === '+' || e.key === '=') { e.preventDefault(); zoomTo(st.zoom * 1.4); }
      else if (e.key === '-') { e.preventDefault(); zoomTo(st.zoom / 1.4); }
      else if (e.key === '0') { e.preventDefault(); st.zoom = 1; layout(); }
      else if (e.key === 'PageDown') { e.preventDefault(); show(st.i + 1); }
      else if (e.key === 'PageUp') { e.preventDefault(); show(st.i - 1); }
    });
    dlg.addEventListener('close', function () {
      if (st.task) st.task.cancel(); clearTimeout(st.timer);
      document.documentElement.classList.remove('dc-lb-open');
      if (st.opener && document.contains(st.opener)) try { st.opener.focus(); } catch (e) {}
    });
    // Zoom per Strg + Mausrad / Trackpad-Geste
    view.addEventListener('wheel', function (e) {
      if (!e.ctrlKey) return;
      e.preventDefault();
      var vr = view.getBoundingClientRect();
      zoomTo(st.zoom * Math.exp(-e.deltaY * 0.01), e.clientX - vr.left, e.clientY - vr.top);
    }, { passive: false });
    // Verschieben (Maus, Stift, ein Finger) und Zwei-Finger-Zoom
    var pts = {}, pinch = null;
    view.addEventListener('pointerdown', function (e) {
      pts[e.pointerId] = { x: e.clientX, y: e.clientY };
      try { view.setPointerCapture(e.pointerId); } catch (x) {}
      var ids = Object.keys(pts);
      if (ids.length === 2) {
        var a = pts[ids[0]], b = pts[ids[1]], vr = view.getBoundingClientRect();
        pinch = { d: Math.hypot(a.x - b.x, a.y - b.y) || 1, z: st.zoom, cx: (a.x + b.x) / 2 - vr.left, cy: (a.y + b.y) / 2 - vr.top };
      }
      view.classList.add('drag');
    });
    view.addEventListener('pointermove', function (e) {
      var p = pts[e.pointerId]; if (!p) return;
      var ids = Object.keys(pts);
      if (pinch && ids.length === 2) {
        p.x = e.clientX; p.y = e.clientY;
        var a = pts[ids[0]], b = pts[ids[1]];
        zoomTo(pinch.z * Math.hypot(a.x - b.x, a.y - b.y) / pinch.d, pinch.cx, pinch.cy);
        return;
      }
      view.scrollLeft -= e.clientX - p.x; view.scrollTop -= e.clientY - p.y;
      p.x = e.clientX; p.y = e.clientY;
    });
    function up(e) { delete pts[e.pointerId]; if (Object.keys(pts).length < 2) pinch = null; if (!Object.keys(pts).length) view.classList.remove('drag'); }
    view.addEventListener('pointerup', up); view.addEventListener('pointercancel', up);
    window.addEventListener('resize', function () { if (dlg.open) layout(); });

    LB = {
      open: function (src, i, opener) {
        st.src = src; st.opener = opener || null;
        document.documentElement.classList.add('dc-lb-open');
        if (typeof dlg.showModal === 'function') dlg.showModal(); else dlg.setAttribute('open', '');
        show(i || 0);
        try { q('.dc-lb-x').focus(); } catch (e) {}
      },
      close: function () { if (dlg.open) dlg.close(); }
    };
    return LB;
  }

  /* ---------- Ausgabe ---------- */
  var ICON = { ok: '✓', warn: '!', bad: '✕', info: 'i' };
  var LABEL = { ok: 'In Ordnung', warn: 'Hinweis', bad: 'Bitte prüfen', info: 'Info' };
  function renderChecks(name, info, checks) {
    var n = { ok: 0, warn: 0, bad: 0 };
    checks.forEach(function (c) { if (n[c[0]] !== undefined) n[c[0]]++; });
    var verdict = n.bad ? ['bad', 'Bitte vor dem Druck prüfen', n.bad + (n.bad === 1 ? ' Punkt sollte' : ' Punkte sollten') + ' korrigiert werden. Wir helfen gern dabei.']
      : n.warn ? ['warn', 'Druckbar – mit Hinweisen', 'Die Datei lässt sich drucken. Lesen Sie die Hinweise, damit das Ergebnis so wird, wie Sie es erwarten.']
        : ['ok', 'Sieht druckfertig aus', 'Wir haben keine Probleme gefunden.'];
    var cnt = '<p class="dc-count"><span class="dc-c dc-ok">' + n.ok + ' in Ordnung</span><span class="dc-c dc-warn">' + plural(n.warn, 'Hinweis', 'Hinweise') + '</span><span class="dc-c dc-bad">' + n.bad + ' bitte prüfen</span></p>';
    var h = '<div class="dc-verdict dc-' + verdict[0] + '"><span class="dc-ic" aria-hidden="true">' + ICON[verdict[0]] + '</span><div><strong>' + verdict[1] + '</strong><p>' + verdict[2] + '</p>' + cnt + '<small>' + esc(name) + ' · ' + info + '</small></div></div>';
    h += '<ul class="dc-list">' + checks.map(function (c) {
      return '<li class="dc-' + c[0] + '"><span class="dc-ic" aria-hidden="true">' + ICON[c[0]] + '</span><div><strong>' + c[1] + ' <span class="dc-tag">' + LABEL[c[0]] + '</span></strong><p>' + c[2] + '</p></div></li>';
    }).join('') + '</ul>';
    return { html: h, verdict: verdict };
  }

  function imgTable(imgs, open) {
    if (!imgs || !imgs.length) return '';
    var rows = imgs.slice(0, 100).map(function (im) {
      return '<tr><td>' + im.p + '</td><td>' + im.pw + ' × ' + im.ph + '</td><td>' + fmtMM(im.sw, im.sh) + '</td><td>' + r0(im.ppi) + ' ppi</td><td><span class="dc-st dc-' + im.s + '">' + LABEL[im.s] + '</span></td></tr>';
    }).join('');
    return '<details class="dc-imgs"' + (open ? ' open' : '') + '><summary>Alle Bilder im Detail (' + imgs.length + ')</summary>' +
      '<div class="dc-tw" role="region" aria-label="Bildliste" tabindex="0"><table class="dc-tab"><thead><tr><th scope="col">Seite</th><th scope="col">Pixel</th><th scope="col">Größe im Druck</th><th scope="col">Auflösung</th><th scope="col">Status</th></tr></thead><tbody>' + rows + '</tbody></table></div>' +
      (imgs.length > 100 ? '<p class="dc-small">Die 100 Bilder mit der niedrigsten Auflösung.</p>' : '') + '<p class="dc-small">Sortiert nach Auflösung, schwächstes Bild zuerst. Auflösung = Pixel pro Zoll im Endformat.</p></details>';
  }

  function actions(name, z, checks, verdict) {
    var lines = checks.filter(function (c) { return c[0] !== 'info'; }).map(function (c) { return '- ' + c[1] + ': ' + LABEL[c[0]]; });
    var txt = 'Hallo, ich habe meine Druckdatei mit dem Druckdaten-Check auf Ihrer Website geprüft.\nDatei: ' + name + '\nProdukt: ' + z.name + '\nErgebnis: ' + verdict[1] + '\n' + lines.join('\n') + '\nIch schicke Ihnen die Datei gleich. Können Sie das drucken?';
    return '<div class="dc-actions"><a class="btn btn-teal" href="https://wa.me/' + WA + '?text=' + encodeURIComponent(txt) + '" target="_blank" rel="noopener noreferrer">Ergebnis per WhatsApp senden</a>' +
      '<a class="btn dc-btn2" href="#kontakt">Datei von uns prüfen lassen – kostenlos</a>' +
      '<button type="button" class="dc-print">Prüfbericht drucken / als PDF speichern</button>' +
      '<button type="button" class="dc-again">Andere Datei prüfen</button></div>' +
      '<p class="dc-small">Die automatische Prüfung ersetzt keinen Blick vom Profi. Schicken Sie uns die Datei – wir sehen sie vor dem Druck kostenlos durch.</p>';
  }

  /* ---------- Prüfbericht (Druckansicht) ---------- */
  function printReport() {
    if (!last) return;
    var rep = document.getElementById('dc-report');
    if (!rep) { rep = document.createElement('div'); rep.id = 'dc-report'; document.body.appendChild(rep); }
    var d = new Date(), when = d.toLocaleDateString('de-DE', { day: '2-digit', month: '2-digit', year: 'numeric' }) + ', ' + d.toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' }) + ' Uhr';
    var shots = [].slice.call(out.querySelectorAll('.dc-thumb canvas'), 0, 4).map(function (c, i) {
      var cap = out.querySelectorAll('.dc-thumb .dc-cap')[i];
      try { return '<figure><img src="' + c.toDataURL('image/jpeg', 0.88) + '" alt="Vorschau ' + esc(cap ? cap.textContent : '') + '"><figcaption>' + esc(cap ? cap.textContent : '') + '</figcaption></figure>'; } catch (e) { return ''; }
    }).join('');
    var lg = out.querySelector('.dc-legend');
    rep.innerHTML = '<div class="dcr-head"><img src="/logo.webp" alt="Masar Werbeagentur" width="56" height="56"><div><strong>Masar Werbeagentur</strong><span>Werbung, die man sieht.</span></div><p>Druckdaten-Check<br>Prüfbericht</p></div>' +
      '<h1 class="dcr-h1">Prüfbericht Druckdaten</h1>' +
      '<table class="dcr-meta"><tbody><tr><th scope="row">Datei</th><td>' + esc(last.name) + '</td></tr><tr><th scope="row">Produkt</th><td>' + esc(last.z.name) + (last.z.b ? ', Beschnitt ' + r1(last.z.b) + ' mm' : '') + '</td></tr><tr><th scope="row">Geprüft am</th><td>' + when + '</td></tr><tr><th scope="row">Ergebnis</th><td><strong>' + last.verdict[1] + '</strong></td></tr></tbody></table>' +
      last.html + imgTable(last.imgs, true) +
      (shots ? '<h2 class="dcr-h2">Vorschau</h2>' + (lg ? lg.outerHTML : '') + '<div class="dcr-shots">' + shots + '</div>' : '') +
      '<p class="dcr-foot">Automatische Prüfung im Browser auf masar-werbeagentur.de/druckdaten-check.html – die Datei wurde dabei nicht hochgeladen. Der Bericht ersetzt keine Prüfung durch die Druckerei.<br>Masar Werbeagentur · Bristolstraße 19E, 13349 Berlin · 0178 514 3918 · info@masar-werbeagentur.de</p>';
    var html = document.documentElement;
    html.classList.add('dc-printing');
    var done = function () { html.classList.remove('dc-printing'); window.removeEventListener('afterprint', done); };
    window.addEventListener('afterprint', done);
    var img = rep.querySelector('.dcr-head img'), go = function () { window.print(); }; // Klasse bleibt bis „afterprint“ (wirkt nur im Druck)
    if (img.complete) go(); else { img.onload = img.onerror = go; setTimeout(function () { if (!img.complete) go(); }, 1200); }
  }

  /* ---------- Ablauf ---------- */
  var out = $('#dc-out'), busy = false, pending = null, lastFile = null, last = null, lastDoc = null, src = null;
  var lastUpd = 0;
  function status(msg, f) {
    var now = Date.now(), el = out.querySelector('.dc-busy');
    if (el && f !== undefined && f < 1 && now - lastUpd < 120) return;
    lastUpd = now;
    if (!el) {
      out.innerHTML = '<div class="dc-busy" role="status"><span class="dc-spin" aria-hidden="true"></span><div class="dc-busy-b"><span class="dc-busy-t"></span><progress class="dc-prog" max="100" value="0" aria-label="Fortschritt der Prüfung"></progress></div></div>';
      el = out.querySelector('.dc-busy');
    }
    el.querySelector('.dc-busy-t').textContent = msg;
    var p = el.querySelector('progress');
    if (f === undefined) p.removeAttribute('value'); else p.value = Math.round(f * 100);
  }
  function fail(msg) { out.innerHTML = '<div class="dc-verdict dc-bad"><span class="dc-ic" aria-hidden="true">✕</span><div><strong>Prüfung nicht möglich</strong><p>' + msg + '</p></div></div>'; }

  function run(file) {
    if (!file) return;
    if (busy) { pending = file; return; } // neue Datei oder neues Produkt während der Prüfung: danach prüfen
    lastFile = file; last = null; src = null;
    if (LB) LB.close();
    if (lastDoc) { try { lastDoc.destroy(); } catch (e) {} lastDoc = null; }
    var z = ziel();
    if (!z) { fail('Bitte Breite und Höhe in Zentimetern eingeben.'); return; }
    if (file.size > MAX_MB * 1048576) { fail('Die Datei ist größer als ' + MAX_MB + ' MB. Schicken Sie sie uns bitte per WeTransfer oder E-Mail – wir prüfen sie kostenlos.'); return; }
    var isPdf = /pdf/i.test(file.type) || /\.pdf$/i.test(file.name), isImg = /^image\/(jpeg|png|webp)$/.test(file.type) || /\.(jpe?g|png|webp)$/i.test(file.name);
    if (!isPdf && !isImg) { fail('Bitte eine PDF-, JPG- oder PNG-Datei wählen. Für AI-, EPS-, PSD- oder TIFF-Dateien schicken Sie uns die Datei einfach – wir prüfen sie kostenlos.'); return; }
    busy = true; out.innerHTML = ''; status('Datei wird geladen …');
    file.arrayBuffer().then(function (buf) {
      if (isPdf) return checkPdf(file, buf, z, function (f, t) { status(t, f); }).then(function (o) {
        lastDoc = o.doc;
        var checks = pdfChecks(o, z), r = renderChecks(file.name, o.n + (o.n === 1 ? ' Seite' : ' Seiten') + ' · ' + z.name, checks);
        last = { name: file.name, z: z, verdict: r.verdict, html: r.html, imgs: o.imgs };
        out.innerHTML = r.html + imgTable(o.imgs) + '<div class="dc-prev"></div>' + actions(file.name, z, checks, r.verdict);
        src = pdfSource(o, z);
        finish();
        return renderPreviews(src, out.querySelector('.dc-prev'), o.n > MAX_PAGES ? ' Geprüft und angezeigt werden die ersten ' + MAX_PAGES + ' Seiten.' : '');
      });
      return checkImage(file, buf, z).then(function (res) {
        var r = renderChecks(file.name, res.w + ' × ' + res.h + ' px · ' + z.name, res.checks);
        last = { name: file.name, z: z, verdict: r.verdict, html: r.html, imgs: null };
        out.innerHTML = r.html + '<div class="dc-prev"></div>' + actions(file.name, z, res.checks, r.verdict);
        src = imgSource(res);
        finish();
        return renderPreviews(src, out.querySelector('.dc-prev'));
      });
    }).catch(function (e) {
      try { console.warn('Druckcheck:', e); } catch (x) {}
      var m = String(e && (e.name || e.message) || '');
      fail(/Password/i.test(m) ? 'Die PDF ist mit einem Passwort geschützt. Bitte ohne Passwort speichern und erneut prüfen.'
        : 'Die Datei konnte nicht gelesen werden – vielleicht ist sie beschädigt oder in einem Sonderformat. Schicken Sie sie uns, wir schauen sie uns kostenlos an.');
    }).then(function () {
      busy = false;
      if (pending) { var p = pending; pending = null; run(p); }
    });
  }
  function finish() {
    var v = out.querySelector('.dc-verdict');
    v.setAttribute('tabindex', '-1');
    try { v.focus({ preventScroll: true }); } catch (e) {}
    out.scrollIntoView({ behavior: 'smooth', block: 'start' });
    try { if (window.plausible) window.plausible('Druckcheck'); } catch (e) {}
  }

  // Bedienung
  var fileIn = $('#dc-file'), drop = $('.dc-drop');
  fileIn.addEventListener('change', function () { if (fileIn.files[0]) run(fileIn.files[0]); });
  ['dragenter', 'dragover'].forEach(function (ev) { drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.add('on'); }); });
  ['dragleave', 'drop'].forEach(function (ev) { drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.remove('on'); }); });
  drop.addEventListener('drop', function (e) { var f = e.dataTransfer && e.dataTransfer.files[0]; if (f) run(f); });
  function syncProd() {
    var k = $('#dc-prod').value, eigen = k === 'eigen';
    $('#dc-custom').hidden = !eigen;
    var t = eigen ? TYP[$('#dc-typ').value] : TYP[PROD[k][3]];
    $('#dc-bleed').value = String(t.bleed);
    $('#dc-hint').textContent = 'Richtwert ' + t.rec + ' ppi (mindestens ' + t.min + ') · Sicherheitsabstand ' + t.safe + ' mm';
  }
  $('#dc-prod').addEventListener('change', function () { syncProd(); if (lastFile) run(lastFile); });
  $('#dc-typ').addEventListener('change', function () { syncProd(); if (lastFile) run(lastFile); });
  ['#dc-bleed', '#dc-w', '#dc-h'].forEach(function (s) { $(s).addEventListener('change', function () { if (lastFile) run(lastFile); }); });
  out.addEventListener('click', function (e) {
    if (e.target.closest('.dc-again')) { fileIn.value = ''; lastFile = null; out.innerHTML = ''; drop.scrollIntoView({ behavior: 'smooth', block: 'center' }); fileIn.click(); return; }
    if (e.target.closest('.dc-print')) { printReport(); return; }
    var t = e.target.closest('.dc-thumb');
    if (t && src) lightbox().open(src, +t.getAttribute('data-i'), t);
  });
  syncProd();

  /* ---------- Pixel-Rechner ---------- */
  var calc = document.getElementById('dc-rechner');
  if (calc) {
    var q = function (s) { return calc.querySelector(s); };
    var num = function (s) { return parseFloat(String(q(s).value).replace(',', '.')); };
    var upd = function () {
      var pw = num('#rc-pw'), ph = num('#rc-ph'), d = num('#rc-dpi'), o1 = q('#rc-out1');
      o1.textContent = pw > 0 && ph > 0 && d > 0 ? 'Druckgröße: ' + r1(pw / d * 2.54) + ' × ' + r1(ph / d * 2.54) + ' cm' : '–';
      var cw = num('#rc-cw'), ch = num('#rc-ch'), d2 = num('#rc-dpi2'), o2 = q('#rc-out2');
      o2.textContent = cw > 0 && ch > 0 && d2 > 0 ? 'Benötigt: ' + r0(cw / 2.54 * d2).toLocaleString('de-DE') + ' × ' + r0(ch / 2.54 * d2).toLocaleString('de-DE') + ' Pixel' : '–';
    };
    calc.addEventListener('input', upd); upd();
  }
})();
