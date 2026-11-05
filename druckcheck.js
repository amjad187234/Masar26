/* Masar Druckdaten-Check – prüft PDF/JPG/PNG direkt im Browser (keine Übertragung an einen Server).
   PDF-Analyse mit pdf.js (selbst gehostet unter /js/pdfjs/, Apache-2.0, siehe /lizenzen/).
   Prüft: Format + Beschnitt, effektive Bildauflösung, eingebettete Schriften, Farbraum, Sonderfarben,
   Texte zu nah am Rand. Ergebnis als Ampel + Vorschau mit Schnitt- und Sicherheitslinie. */
(function () {
  'use strict';
  var root = document.getElementById('druckcheck');
  if (!root) return;
  var $ = function (s) { return root.querySelector(s); };
  var WA = '491785143918';
  var MAX_MB = 200, MAX_PAGES = 30, THUMBS = 6;

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
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function fmtMM(w, h) { return w >= 1000 || h >= 1000 ? r1(w / 10) + ' × ' + r1(h / 10) + ' cm' : r0(w) + ' × ' + r0(h) + ' mm'; }
  function mul(m, n) { // m × n (PDF-Matrizen)
    return [m[0] * n[0] + m[1] * n[2], m[0] * n[1] + m[1] * n[3], m[2] * n[0] + m[3] * n[2], m[2] * n[1] + m[3] * n[3],
      m[4] * n[0] + m[5] * n[2] + n[4], m[4] * n[1] + m[5] * n[3] + n[5]];
  }

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

  // Seite (mm) gegen Ziel prüfen → Status, Text, Maßstab k (Endformat = Datei × k), Schnittrand in Datei-mm
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
          best = { s: 'info', t: 'Datei ist im Maßstab 1:' + r1(k) + ' angelegt (Endformat ' + fmtMM(W, H) + (c[2] ? ' mit Beschnitt' : '') + '). Das ist bei Großformaten üblich – die Auflösung wird auf das Endformat umgerechnet.', k: k, inset: c[2] / k };
      });
    });
    if (best) return best;
    return { s: 'bad', t: 'Format passt nicht: Datei ' + fmtMM(w, h) + ', erwartet ' + fmtMM(z.W + 2 * z.b, z.H + 2 * z.b) + (z.b ? ' (Endformat ' + fmtMM(z.W, z.H) + ' + Beschnitt)' : '') + '. Bitte Format prüfen oder oben das richtige Produkt wählen.', k: w ? (z.W / w) : 1, inset: 0, mismatch: true };
  }

  function ppiStatus(ppi, z) { return ppi >= z.rec * 0.95 ? 'ok' : ppi >= z.min ? 'warn' : 'bad'; }

  /* ---------- Rohdaten-Scan (Farbräume, Sonderfarben, PDF/X) ---------- */
  function inflate(bytes) {
    if (typeof DecompressionStream === 'undefined') return Promise.resolve('');
    try {
      var ds = new DecompressionStream('deflate');
      var w = ds.writable.getWriter(); w.write(bytes).catch(function () {}); w.close().catch(function () {});
      return new Response(ds.readable).arrayBuffer().then(function (ab) { return latin(new Uint8Array(ab)); }, function () { return ''; });
    } catch (e) { return Promise.resolve(''); }
  }
  function latin(u8) {
    var s = '', CH = 0x8000;
    for (var i = 0; i < u8.length; i += CH) s += String.fromCharCode.apply(null, u8.subarray(i, i + CH));
    return s;
  }
  function rawScan(u8) {
    var raw = latin(u8.length > 120e6 ? u8.subarray(0, 120e6) : u8);
    var res = { cmykImg: 0, rgbImg: 0, grayImg: 0, cmykOps: 0, rgbOps: 0, spots: {}, pdfx: /GTS_PDFX|pdfxid:GTS_PDFXVersion|<pdfxid:/i.test(raw), outputIntent: /\/OutputIntents/.test(raw), transp: /\/SMask\s*\/|\/CA\s+0?\.\d|\/ca\s+0?\.\d/.test(raw) };
    var objs = {}, jobs = [], budget = 60e6;
    var re = /(\d+)\s+0\s+obj\b/g, m;
    while ((m = re.exec(raw))) {
      var start = m.index + m[0].length;
      var sIdx = raw.indexOf('stream', start), eIdx = raw.indexOf('endobj', start);
      if (eIdx < 0) break;
      var isStream = sIdx > -1 && sIdx < eIdx;
      var dict = raw.slice(start, isStream ? sIdx : Math.min(eIdx, start + 4000));
      objs[m[1]] = dict.slice(0, 1500);
      if (isStream) {
        var ds = sIdx + 6; if (raw[ds] === '\r') ds++; if (raw[ds] === '\n') ds++;
        var es = raw.indexOf('endstream', ds); if (es < 0 || es > eIdx) es = eIdx;
        if (/\/Subtype\s*\/Image/.test(dict)) { jobs.push({ img: dict }); }
        else if (/\/FlateDecode/.test(dict) && !/\/Length[123]\b|\/FontFile|\/Type1C|\/CIDFontType0C|\/OpenType|\/XRef|\/Alternate|\/N\s+[134]\b/.test(dict) && es - ds < 25e6 && budget > 0) {
          budget -= es - ds; jobs.push({ z: u8.subarray(ds, es) });
        }
        re.lastIndex = es;
      } else re.lastIndex = eIdx;
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
    var texts = [raw.length > 30e6 ? '' : raw];
    return jobs.reduce(function (p, j) {
      return p.then(function () {
        if (j.img) {
          if (/\/ImageMask\s+true/.test(j.img)) return;
          var c = /\/ColorSpace\s*(\/\w+|\[[^\]]*\]|\d+\s+0\s+R)/.exec(j.img), cs = c ? csOf(c[1], 0) : '';
          if (cs === 'cmyk') res.cmykImg++; else if (cs === 'rgb') res.rgbImg++; else if (cs === 'gray') res.grayImg++;
          return;
        }
        return inflate(j.z).then(function (t) { if (t) texts.push(t); });
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
      return res;
    });
  }

  /* ---------- PDF ---------- */
  function checkPdf(file, buf, z) {
    var u8 = new Uint8Array(buf), out = { checks: [], pages: [] };
    return loadPdfjs().then(function (lib) {
      return lib.getDocument({ data: u8.slice(0), isEvalSupported: false, disableFontFace: false, useSystemFonts: false, verbosity: 0 }).promise;
    }).then(function (doc) {
      out.doc = doc; out.n = doc.numPages;
      var fonts = {}, n = Math.min(doc.numPages, MAX_PAGES), chain = Promise.resolve();
      for (var i = 1; i <= n; i++) (function (i) {
        chain = chain.then(function () { return doc.getPage(i); }).then(function (page) {
          var vp = page.getViewport({ scale: 1 });
          var w = vp.width * MM, h = vp.height * MM;
          var pg = { i: i, page: page, w: w, h: h, fc: formatCheck(w, h, z), imgs: [], edge: [] };
          out.pages.push(pg);
          return page.getOperatorList().then(function (ol) {
            var O = pdfjs.OPS, ctm = [1, 0, 0, 1, 0, 0], st = [], cur = null;
            for (var j = 0; j < ol.fnArray.length; j++) {
              var fn = ol.fnArray[j], a = ol.argsArray[j];
              if (fn === O.save) st.push(ctm);
              else if (fn === O.restore) ctm = st.pop() || ctm;
              else if (fn === O.transform) ctm = mul(a, ctm);
              else if (fn === O.paintFormXObjectBegin) { st.push(ctm); if (a && a[0]) ctm = mul(a[0], ctm); }
              else if (fn === O.paintFormXObjectEnd) ctm = st.pop() || ctm;
              else if (fn === O.paintImageXObject || fn === O.paintInlineImageXObject) {
                var pw = fn === O.paintImageXObject ? a[1] : a[0] && a[0].width, ph = fn === O.paintImageXObject ? a[2] : a[0] && a[0].height;
                var sw = Math.hypot(ctm[0], ctm[1]) * MM, sh = Math.hypot(ctm[2], ctm[3]) * MM;
                if (pw && ph && sw > 3 && sh > 3) {
                  var ppi = Math.min(pw / (sw / 25.4), ph / (sh / 25.4)) / pg.fc.k;
                  pg.imgs.push({ pw: pw, ph: ph, sw: sw * pg.fc.k, sh: sh * pg.fc.k, ppi: ppi });
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
            // Texte zu nah am Rand (in mm, Ursprung unten links)
            var v = page.view, ins = pg.fc.mismatch ? 0 : pg.fc.inset, safe = z.safe / pg.fc.k;
            tc.items.forEach(function (it) {
              if (!it.str || !it.str.trim()) return;
              var x = (it.transform[4] - v[0]) * MM, y = (it.transform[5] - v[1]) * MM;
              var tw = it.width * MM, th = (it.height || Math.hypot(it.transform[2], it.transform[3])) * MM;
              if (Math.abs(it.transform[1]) > Math.abs(it.transform[0])) { var t = tw; tw = th; th = t; x -= tw; }
              var lo = ins + safe, hiX = w - ins - safe, hiY = h - ins - safe;
              if (x < lo || y < lo || x + tw > hiX || y + th > hiY) {
                if (x + tw < 0 || y + th < 0 || x > w || y > h) return;
                pg.edge.push({ x: x, y: y, w: tw, h: th, s: it.str.trim().slice(0, 40) });
              }
            });
          });
        });
      })(i);
      return chain.then(function () { out.fonts = fonts; return rawScan(u8); });
    }).then(function (scan) {
      out.scan = scan; return out;
    });
  }

  function pdfChecks(o, z) {
    var c = [], P = o.pages;
    // Format
    var bad = P.filter(function (p) { return p.fc.s === 'bad'; }), warn = P.filter(function (p) { return p.fc.s === 'warn'; });
    var first = P[0].fc;
    var sizes = {}; P.forEach(function (p) { sizes[fmtMM(p.w, p.h)] = 1; });
    if (bad.length) c.push(['bad', 'Format & Beschnitt', (P.length > 1 ? 'Seite ' + bad.map(function (p) { return p.i; }).join(', ') + ': ' : '') + bad[0].fc.t]);
    else if (warn.length) c.push(['warn', 'Format & Beschnitt', warn[0].fc.t]);
    else c.push([first.s, 'Format & Beschnitt', first.t]);
    if (Object.keys(sizes).length > 1) c.push(['warn', 'Seitengrößen', 'Die Seiten haben unterschiedliche Größen: ' + Object.keys(sizes).join(' · ') + '.']);
    // Seitenzahl
    c.push(['info', 'Seiten', o.n + (o.n === 1 ? ' Seite' : ' Seiten') + (o.n > MAX_PAGES ? ' – geprüft wurden die ersten ' + MAX_PAGES + '.' : '.') + (o.n === 2 ? ' Bei Flyern und Karten: Seite 1 = Vorderseite, Seite 2 = Rückseite.' : '')]);
    // Bilder
    var imgs = []; P.forEach(function (p) { p.imgs.forEach(function (im) { im.p = p.i; imgs.push(im); }); });
    if (!imgs.length) c.push(['ok', 'Bildauflösung', 'Keine Pixelbilder gefunden – nur Vektoren und Text. Das druckt immer scharf.']);
    else {
      imgs.sort(function (a, b) { return a.ppi - b.ppi; });
      var w0 = imgs[0], s = ppiStatus(w0.ppi, z), nLow = imgs.filter(function (i) { return i.ppi < z.min; }).length;
      var t = imgs.length + (imgs.length === 1 ? ' Bild' : ' Bilder') + ' gefunden. Niedrigste Auflösung: ' + r0(w0.ppi) + ' ppi (Seite ' + w0.p + ', ' + w0.pw + ' × ' + w0.ph + ' Pixel auf ' + fmtMM(w0.sw, w0.sh) + '). Richtwert für dieses Produkt: ' + z.rec + ' ppi, mindestens ' + z.min + ' ppi.';
      if (s === 'bad') t += ' ' + nLow + (nLow === 1 ? ' Bild wirkt' : ' Bilder wirken') + ' im Druck wahrscheinlich unscharf oder pixelig – besser ein größeres Original verwenden.';
      else if (s === 'warn') t += ' Das geht, wirkt aus der Nähe aber etwas weicher.';
      c.push([s, 'Bildauflösung', t]);
    }
    // Schriften
    var fn = Object.keys(o.fonts), miss = fn.filter(function (f) { return o.fonts[f].missing; });
    if (miss.length) c.push(['bad', 'Schriften', 'Nicht eingebettet: ' + miss.slice(0, 6).map(esc).join(', ') + (miss.length > 6 ? ' …' : '') + '. Ohne eingebettete Schrift kann der Text beim Drucken anders aussehen. Lösung: beim PDF-Export „Schriften einbetten“ wählen oder Text in Pfade umwandeln.']);
    else if (fn.length) c.push(['ok', 'Schriften', fn.length === 1 ? 'Die Schrift ist eingebettet.' : 'Alle ' + fn.length + ' Schriften sind eingebettet.']);
    else c.push(['ok', 'Schriften', 'Keine Schriften im PDF – Texte sind in Pfade umgewandelt oder es gibt keinen Text.']);
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
    else if (edge) c.push(['warn', 'Sicherheitsabstand', edge + ' Textstelle' + (edge > 1 ? 'n liegen' : ' liegt') + ' näher als ' + z.safe + ' mm am Schnitt (Seite ' + ep.join(', ') + ', in der Vorschau rot markiert), z. B. „' + esc(P.filter(function (p) { return p.edge.length; })[0].edge[0].s) + '“. Beim Schneiden kann es knapp werden – Text weiter nach innen setzen.']);
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

  /* ---------- Ausgabe ---------- */
  var ICON = { ok: '✓', warn: '!', bad: '✕', info: 'i' };
  var LABEL = { ok: 'In Ordnung', warn: 'Hinweis', bad: 'Bitte prüfen', info: 'Info' };
  function renderChecks(name, info, checks) {
    var n = { ok: 0, warn: 0, bad: 0 };
    checks.forEach(function (c) { if (n[c[0]] !== undefined) n[c[0]]++; });
    var verdict = n.bad ? ['bad', 'Bitte vor dem Druck prüfen', n.bad + (n.bad === 1 ? ' Punkt sollte' : ' Punkte sollten') + ' korrigiert werden. Wir helfen gern dabei.']
      : n.warn ? ['warn', 'Druckbar – mit Hinweisen', 'Die Datei lässt sich drucken. Lesen Sie die Hinweise, damit das Ergebnis so wird, wie Sie es erwarten.']
        : ['ok', 'Sieht druckfertig aus', 'Wir haben keine Probleme gefunden.'];
    var h = '<div class="dc-verdict dc-' + verdict[0] + '"><span class="dc-ic" aria-hidden="true">' + ICON[verdict[0]] + '</span><div><strong>' + verdict[1] + '</strong><p>' + verdict[2] + '</p><small>' + esc(name) + ' · ' + info + '</small></div></div>';
    h += '<ul class="dc-list">' + checks.map(function (c) {
      return '<li class="dc-' + c[0] + '"><span class="dc-ic" aria-hidden="true">' + ICON[c[0]] + '</span><div><strong>' + c[1] + ' <span class="dc-tag">' + LABEL[c[0]] + '</span></strong><p>' + c[2] + '</p></div></li>';
    }).join('') + '</ul>';
    return { html: h, verdict: verdict };
  }

  function overlay(ctx, cw, ch, wmm, hmm, inset, safe, edges) {
    var sx = cw / wmm, sy = ch / hmm;
    ctx.save(); ctx.lineWidth = 2; ctx.setLineDash([8, 5]);
    if (inset > 0) { // Beschnittbereich abdunkeln
      ctx.fillStyle = 'rgba(19,46,80,.28)';
      ctx.fillRect(0, 0, cw, inset * sy); ctx.fillRect(0, ch - inset * sy, cw, inset * sy);
      ctx.fillRect(0, inset * sy, inset * sx, ch - 2 * inset * sy); ctx.fillRect(cw - inset * sx, inset * sy, inset * sx, ch - 2 * inset * sy);
      ctx.strokeStyle = '#d63b3b'; ctx.strokeRect(inset * sx, inset * sy, cw - 2 * inset * sx, ch - 2 * inset * sy);
    }
    var s2 = inset + safe;
    if (s2 * 2 < Math.min(wmm, hmm)) { ctx.strokeStyle = '#177567'; ctx.strokeRect(s2 * sx, s2 * sy, cw - 2 * s2 * sx, ch - 2 * s2 * sy); }
    ctx.setLineDash([]);
    (edges || []).forEach(function (e) {
      ctx.strokeStyle = '#d63b3b'; ctx.fillStyle = 'rgba(214,59,59,.18)';
      var x = e.x * sx, y = ch - (e.y + e.h) * sy;
      ctx.fillRect(x - 2, y - 2, e.w * sx + 4, e.h * sy + 4); ctx.strokeRect(x - 2, y - 2, e.w * sx + 4, e.h * sy + 4);
    });
    ctx.restore();
  }
  function canvasFor(wmm, hmm) {
    var maxW = Math.min(root.clientWidth - 32, 420), maxH = 420, sc = Math.min(maxW / wmm, maxH / hmm);
    var cw = Math.max(60, Math.round(wmm * sc)), ch = Math.max(60, Math.round(hmm * sc)), dpr = Math.min(window.devicePixelRatio || 1, 2);
    var cv = document.createElement('canvas'); cv.width = cw * dpr; cv.height = ch * dpr; cv.style.width = cw + 'px'; cv.style.height = ch + 'px';
    return { cv: cv, cw: cw * dpr, ch: ch * dpr, dpr: dpr };
  }
  var LEGEND = '<p class="dc-legend"><span class="dc-l1"></span>Schnittkante <span class="dc-l2"></span>Sicherheitsabstand <span class="dc-l3"></span>Beschnitt (wird abgeschnitten)</p>';

  function renderPdfPreviews(o, z, box) {
    var P = o.pages.slice(0, THUMBS), chain = Promise.resolve();
    box.innerHTML = '<h3 class="dc-h3">Vorschau</h3>' + LEGEND + '<div class="dc-thumbs"></div>' + (o.n > THUMBS ? '<p class="dc-small">Vorschau der ersten ' + THUMBS + ' Seiten.</p>' : '');
    var wrap = box.querySelector('.dc-thumbs');
    P.forEach(function (p) {
      chain = chain.then(function () {
        var c = canvasFor(p.w, p.h), vp1 = p.page.getViewport({ scale: 1 });
        var vp = p.page.getViewport({ scale: c.cw / vp1.width });
        var fig = document.createElement('figure'); fig.className = 'dc-thumb'; fig.appendChild(c.cv);
        var cap = document.createElement('figcaption'); cap.textContent = 'Seite ' + p.i + ' · ' + fmtMM(p.w * p.fc.k, p.h * p.fc.k); fig.appendChild(cap);
        wrap.appendChild(fig);
        var ctx = c.cv.getContext('2d'); ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, c.cw, c.ch);
        return p.page.render({ canvasContext: ctx, viewport: vp }).promise.then(function () {
          if (!p.fc.mismatch) overlay(ctx, c.cw, c.ch, p.w, p.h, p.fc.inset, z.safe / p.fc.k, p.edge);
        }, function () {});
      });
    });
    return chain;
  }
  function renderImgPreview(r, box) {
    var c = canvasFor(r.FW, r.FH), ctx = c.cv.getContext('2d');
    ctx.fillStyle = '#eef2f2'; ctx.fillRect(0, 0, c.cw, c.ch);
    var s = Math.max(c.cw / r.w, c.ch / r.h), dw = r.w * s, dh = r.h * s; // füllend (wie beim Druck randlos)
    ctx.drawImage(r.img, (c.cw - dw) / 2, (c.ch - dh) / 2, dw, dh);
    overlay(ctx, c.cw, c.ch, r.FW, r.FH, r.z.b, r.z.safe, []);
    box.innerHTML = '<h3 class="dc-h3">Vorschau im Format</h3>' + LEGEND + '<div class="dc-thumbs"></div>';
    var fig = document.createElement('figure'); fig.className = 'dc-thumb'; fig.appendChild(c.cv);
    var cap = document.createElement('figcaption'); cap.textContent = fmtMM(r.FW, r.FH) + ' (randlos gefüllt)'; fig.appendChild(cap);
    box.querySelector('.dc-thumbs').appendChild(fig);
  }

  function actions(name, z, checks, verdict) {
    var lines = checks.filter(function (c) { return c[0] !== 'info'; }).map(function (c) { return '- ' + c[1] + ': ' + LABEL[c[0]]; });
    var txt = 'Hallo, ich habe meine Druckdatei mit dem Druckdaten-Check auf Ihrer Website geprüft.\nDatei: ' + name + '\nProdukt: ' + z.name + '\nErgebnis: ' + verdict[1] + '\n' + lines.join('\n') + '\nIch schicke Ihnen die Datei gleich. Können Sie das drucken?';
    return '<div class="dc-actions"><a class="btn btn-teal" href="https://wa.me/' + WA + '?text=' + encodeURIComponent(txt) + '" target="_blank" rel="noopener noreferrer">Ergebnis per WhatsApp senden</a>' +
      '<a class="btn dc-btn2" href="#kontakt">Datei von uns prüfen lassen – kostenlos</a>' +
      '<button type="button" class="dc-again">Andere Datei prüfen</button></div>' +
      '<p class="dc-small">Die automatische Prüfung ersetzt keinen Blick vom Profi. Schicken Sie uns die Datei – wir sehen sie vor dem Druck kostenlos durch.</p>';
  }

  /* ---------- Ablauf ---------- */
  var out = $('#dc-out'), busy = false, lastFile = null;
  function status(msg) { out.innerHTML = '<div class="dc-busy" role="status"><span class="dc-spin" aria-hidden="true"></span>' + msg + '</div>'; }
  function fail(msg) { out.innerHTML = '<div class="dc-verdict dc-bad"><span class="dc-ic" aria-hidden="true">✕</span><div><strong>Prüfung nicht möglich</strong><p>' + msg + '</p></div></div>'; }

  function run(file) {
    if (busy || !file) return;
    lastFile = file;
    var z = ziel();
    if (!z) { fail('Bitte Breite und Höhe in Zentimetern eingeben.'); return; }
    if (file.size > MAX_MB * 1048576) { fail('Die Datei ist größer als ' + MAX_MB + ' MB. Schicken Sie sie uns bitte per WeTransfer oder E-Mail – wir prüfen sie kostenlos.'); return; }
    var isPdf = /pdf/i.test(file.type) || /\.pdf$/i.test(file.name), isImg = /^image\/(jpeg|png|webp)$/.test(file.type) || /\.(jpe?g|png|webp)$/i.test(file.name);
    if (!isPdf && !isImg) { fail('Bitte eine PDF-, JPG- oder PNG-Datei wählen. Für AI-, EPS-, PSD- oder TIFF-Dateien schicken Sie uns die Datei einfach – wir prüfen sie kostenlos.'); return; }
    busy = true; status('Datei wird geprüft …');
    var t0 = Date.now();
    file.arrayBuffer().then(function (buf) {
      if (isPdf) return checkPdf(file, buf, z).then(function (o) {
        var checks = pdfChecks(o, z), r = renderChecks(file.name, o.n + (o.n === 1 ? ' Seite' : ' Seiten') + ' · ' + z.name, checks);
        out.innerHTML = r.html + '<div class="dc-prev"></div>' + actions(file.name, z, checks, r.verdict);
        return renderPdfPreviews(o, z, out.querySelector('.dc-prev'));
      });
      return checkImage(file, buf, z).then(function (res) {
        var r = renderChecks(file.name, res.w + ' × ' + res.h + ' px · ' + z.name, res.checks);
        out.innerHTML = r.html + '<div class="dc-prev"></div>' + actions(file.name, z, res.checks, r.verdict);
        renderImgPreview(res, out.querySelector('.dc-prev'));
      });
    }).then(function () {
      out.querySelector('.dc-verdict').setAttribute('tabindex', '-1');
      try { out.querySelector('.dc-verdict').focus({ preventScroll: true }); } catch (e) {}
      out.scrollIntoView({ behavior: 'smooth', block: 'start' });
      try { if (window.plausible) window.plausible('Druckcheck'); } catch (e) {}
    }).catch(function (e) {
      try { console.warn('Druckcheck:', e); } catch (x) {}
      var m = String(e && (e.name || e.message) || '');
      fail(/Password/i.test(m) ? 'Die PDF ist mit einem Passwort geschützt. Bitte ohne Passwort speichern und erneut prüfen.'
        : 'Die Datei konnte nicht gelesen werden – vielleicht ist sie beschädigt oder in einem Sonderformat. Schicken Sie sie uns, wir schauen sie uns kostenlos an.');
    }).then(function () { busy = false; void t0; });
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
    if (e.target.closest('.dc-again')) { fileIn.value = ''; lastFile = null; out.innerHTML = ''; drop.scrollIntoView({ behavior: 'smooth', block: 'center' }); fileIn.click(); }
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
