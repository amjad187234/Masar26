/* 3D-Messestand-Planer für /messebau-berlin.html
   – vier Standtypen (Reihe, Ecke, Kopf, Insel), Standfarbe, eigenes Logo & Firmenname
   – Maus bewegt die Kamera (Desktop), seitlich wischen dreht den Stand (Touch)
   – "Entwurf speichern" lädt ein Bild herunter, "Diesen Stand anfragen" füllt das Formular
   – das Logo wird nur im Browser verarbeitet und erst mit der Anfrage (als Entwurfsbild) gesendet
   – Ausstattung zu- und abschaltbar (LED-Stele, Lichttraverse, Sitzecke, Pflanzen, Beachflag, Roll-ups), Maße, Ansichten
   – Desktop: Nachbearbeitung mit Leuchten (Bloom) und Kantenglättung (SMAA),
     die sich bei schwacher Grafik selbst abschaltet
   – Standgröße 4–10 × 3–5 m, Möbel per Maus/Finger verschieben und drehen, Besucher-Blick,
     Entwurf als Link teilen, 360°-Video, Stückliste in der Anfrage
   – bei "prefers-reduced-motion" bleibt die Ansicht ruhig */
import * as THREE from './three.module.min.js';
import { RoomEnvironment } from './RoomEnvironment.js';

const NAVY = '#132e50';
const INK = '#0f2440';
const TYPES = {
  reihe: { name: 'Reihenstand', open: 'eine Seite offen', yaw: 0.02, pitch: 0.13, range: 0.32 },
  eck: { name: 'Eckstand', open: 'zwei Seiten offen', yaw: 0.34, pitch: 0.12, range: 0.4 },
  kopf: { name: 'Kopfstand', open: 'drei Seiten offen', yaw: 0.22, pitch: 0.11, range: 0.5 },
  insel: { name: 'Inselstand', open: 'vier Seiten offen', yaw: 0.3, pitch: 0.17, range: 0.6 },
};

/* ── Farbhilfen ─────────────────────────────────────── */
const rgb = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
const mix = (a, b, t) => {
  const A = rgb(a), B = rgb(b);
  return `rgb(${A.map((v, i) => Math.round(v + (B[i] - v) * t)).join(',')})`;
};

/* ── Zustand ────────────────────────────────────────── */
const state = { type: 'kopf', color: '#58d0bd', colorName: 'Türkis', logo: null, name: '' };

/* ── Grafik-Bausteine ───────────────────────────────── */
function diamond(ctx, cx, cy, s, C) {
  ctx.save();
  ctx.translate(cx, cy);
  ctx.rotate(Math.PI / 4);
  ctx.fillStyle = C;
  ctx.fillRect(-s / 2, -s / 2, s, s);
  ctx.fillStyle = mix(C, INK, 0.72);
  ctx.fillRect(-s / 2 + s * 0.2, -s / 2 + s * 0.2, s * 0.62, s * 0.62);
  ctx.fillStyle = mix(C, '#ffffff', 0.35);
  ctx.fillRect(-s / 2 + s * 0.2, -s / 2 + s * 0.2, s * 0.3, s * 0.3);
  ctx.restore();
}

function font(px, weight = 900, family = '"Barlow Condensed"') {
  return `${weight} ${px}px ${family}, "Arial Narrow", sans-serif`;
}

function text(ctx, str, x, y, px, color, { weight = 900, family = '"Barlow Condensed"', align = 'center', spacing = 0, maxW = 0 } = {}) {
  ctx.font = font(px, weight, family);
  if ('letterSpacing' in ctx) ctx.letterSpacing = spacing + 'px';
  if (maxW) {
    const w = ctx.measureText(str).width;
    if (w > maxW) { px *= maxW / w; ctx.font = font(px, weight, family); }
  }
  ctx.fillStyle = color;
  ctx.textAlign = align;
  ctx.textBaseline = 'middle';
  ctx.fillText(str, x, y);
  if ('letterSpacing' in ctx) ctx.letterSpacing = '0px';
}

/* Marke in einem Rechteck: eigenes Logo, sonst Platzhalter-Raute; darunter Name bzw. "IHR LOGO" */
function brand(ctx, x, y, w, h, C) {
  const label = state.name ? state.name.toUpperCase() : 'IHR LOGO';
  const img = state.logo;
  if (img) {
    const boxH = state.name ? h * 0.66 : h;
    const k = Math.min((w * 0.92) / img.width, (boxH * 0.92) / img.height);
    const dw = img.width * k, dh = img.height * k;
    ctx.drawImage(img, x + (w - dw) / 2, y + (boxH - dh) / 2, dw, dh);
    if (state.name) text(ctx, label, x + w / 2, y + h * 0.84, h * 0.2, NAVY, { maxW: w });
    return;
  }
  const s = Math.min(w * 0.5, h * 0.44);
  diamond(ctx, x + w / 2, y + h * 0.3, s, C);
  text(ctx, label, x + w / 2, y + h * 0.8, h * 0.26, NAVY, { maxW: w });
}

/* Diagonale Flächen wie in der Standgrafik */
function shards(ctx, x, y, w, h, C, flip = false) {
  ctx.save();
  if (flip) { ctx.translate(x + w, y); ctx.scale(-1, 1); ctx.translate(-x, -y); }
  const poly = (pts, fill) => {
    ctx.beginPath();
    pts.forEach(([px, py], i) => (i ? ctx.lineTo : ctx.moveTo).call(ctx, x + px * w, y + py * h));
    ctx.closePath();
    ctx.fillStyle = fill;
    ctx.fill();
  };
  poly([[0, 0.28], [0.62, 1], [0, 1]], mix(C, NAVY, 0.78));
  poly([[0, 0.55], [0.4, 1], [0, 1]], mix(C, NAVY, 0.45));
  poly([[0.18, 1], [0.92, 0.22], [1, 0.3], [1, 1]], mix(C, '#ffffff', 0.18));
  poly([[0.5, 1], [1, 0.52], [1, 1]], mix(C, NAVY, 0.6));
  poly([[0.72, 1], [1, 0.76], [1, 1]], C);
  ctx.restore();
}

function paper(ctx, w, h) {
  const g = ctx.createLinearGradient(0, 0, 0, h);
  g.addColorStop(0, '#ffffff');
  g.addColorStop(1, '#eef2f5');
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, w, h);
}

const PAINT = {
  wall(ctx, w, h, C) {
    paper(ctx, w, h);
    shards(ctx, 0, h * 0.18, w * 0.3, h * 0.82, C);
    shards(ctx, w * 0.7, 0, w * 0.3, h, C, true);
    ctx.fillStyle = mix(C, NAVY, 0.55);
    ctx.fillRect(0, 0, w, h * 0.018);
    brand(ctx, w * 0.32, h * 0.08, w * 0.36, h * 0.36, C);
    text(ctx, 'IHRE MARKE. ÜBERALL SICHTBAR.', w / 2, h * 0.5, h * 0.042, mix(NAVY, '#ffffff', 0.15), { weight: 500, family: '"Barlow"', spacing: h * 0.012 });
  },
  side(ctx, w, h, C) {
    paper(ctx, w, h);
    shards(ctx, 0, h * 0.45, w, h * 0.55, C, true);
    ctx.fillStyle = mix(C, NAVY, 0.55);
    ctx.fillRect(0, 0, w, h * 0.018);
    brand(ctx, w * 0.3, h * 0.1, w * 0.4, h * 0.26, C);
  },
  counter(ctx, w, h, C) {
    paper(ctx, w, h);
    shards(ctx, w * 0.22, h * 0.05, w * 0.2, h * 0.95, C);
    shards(ctx, w * 0.58, h * 0.05, w * 0.2, h * 0.95, C, true);
    ctx.fillStyle = mix(C, NAVY, 0.7);
    ctx.fillRect(0, h * 0.94, w, h * 0.06);
    brand(ctx, w * 0.42, h * 0.1, w * 0.16, h * 0.72, C);
  },
  rollupA(ctx, w, h, C) {
    paper(ctx, w, h);
    brand(ctx, w * 0.12, h * 0.035, w * 0.76, h * 0.17, C);
    ['STARKE', 'MARKEN.', 'STARKE', 'AUFTRITTE.'].forEach((t, i) =>
      text(ctx, t, w * 0.14, h * (0.3 + i * 0.055), w * 0.1, NAVY, { align: 'left' }));
    shards(ctx, 0, h * 0.56, w, h * 0.44, C);
  },
  rollupB(ctx, w, h, C) {
    paper(ctx, w, h);
    brand(ctx, w * 0.12, h * 0.035, w * 0.76, h * 0.17, C);
    ['LÖSUNGEN', 'FÜR STARKE', 'MARKEN.'].forEach((t, i) =>
      text(ctx, t, w / 2, h * (0.31 + i * 0.055), w * 0.1, NAVY));
    shards(ctx, 0, h * 0.54, w, h * 0.46, C, true);
  },
  flag(ctx, w, h, C) {
    paper(ctx, w, h);
    brand(ctx, w * 0.2, h * 0.13, w * 0.6, h * 0.17, C);
    ['IDEEN', 'SICHTBAR', 'MACHEN'].forEach((t, i) =>
      text(ctx, t, w * 0.2, h * (0.38 + i * 0.045), w * 0.12, NAVY, { align: 'left' }));
    shards(ctx, 0, h * 0.58, w, h * 0.42, C, true);
  },
  ring(ctx, w, h, C) {
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = C;
    ctx.fillRect(0, 0, w, h * 0.12);
    ctx.fillRect(0, h * 0.88, w, h * 0.12);
    for (let i = 0; i < 4; i++) brand(ctx, w * (i / 4) + w * 0.06, h * 0.16, w * 0.13, h * 0.68, C);
  },
};

/* ── Ausstattung & Ansichten ────────────────────────── */
const EXTRAS = {
  screen: 'LED-Stele',
  truss: 'Lichttraverse',
  seating: 'Sitzecke',
  plants: 'Pflanzen',
  flag: 'Beachflag',
  rollups: 'Roll-ups',
};
Object.assign(state, {
  extras: { screen: true, truss: false, seating: true, plants: true, flag: true, rollups: true },
  dims: false,
  view: 'standard',
  w: 6, d: 4,          /* Standgröße in m */
  pos: {},             /* verschobene Elemente: key → {x, z, r} */
  arrange: false,      /* Möbel-verschieben-Modus */
});
const WIDTHS = [4, 6, 8, 10], DEPTHS = [3, 4, 5];

/* Inhalt der LED-Stele: drei Folien im Wechsel */
function paintScreen(ctx, w, h, t, C) {
  const slide = Math.floor(t / 3.2) % 3, local = (t % 3.2) / 3.2;
  const g = ctx.createLinearGradient(0, 0, w, h);
  g.addColorStop(0, mix(C, NAVY, 0.82)); g.addColorStop(1, mix(C, NAVY, 0.45));
  ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
  ctx.save();
  ctx.globalAlpha = 0.18;
  for (let i = 0; i < 6; i++) {
    ctx.fillStyle = C;
    const y = ((i * 0.22 + t * 0.05) % 1.3 - 0.15) * h;
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y - w * 0.6); ctx.lineTo(w, y - w * 0.6 + h * 0.04); ctx.lineTo(0, y + h * 0.04); ctx.fill();
  }
  ctx.restore();
  const fade = Math.min(1, local * 6, (1 - local) * 6);
  ctx.globalAlpha = fade;
  const W = '#ffffff';
  if (slide === 0) {
    ctx.save(); ctx.fillStyle = 'rgba(255,255,255,.96)';
    ctx.fillRect(w * 0.1, h * 0.26, w * 0.8, h * 0.3); ctx.restore();
    brand(ctx, w * 0.14, h * 0.28, w * 0.72, h * 0.26, C);
    text(ctx, 'WILLKOMMEN', w / 2, h * 0.68, w * 0.14, W);
  } else if (slide === 1) {
    text(ctx, 'IHRE', w / 2, h * 0.36, w * 0.2, W);
    text(ctx, 'BOTSCHAFT', w / 2, h * 0.47, w * 0.2, C, { maxW: w * 0.86 });
    text(ctx, 'IN BEWEGUNG.', w / 2, h * 0.58, w * 0.13, W, { maxW: w * 0.86 });
  } else {
    text(ctx, 'JETZT', w / 2, h * 0.4, w * 0.16, W);
    text(ctx, 'BERATEN', w / 2, h * 0.5, w * 0.16, W);
    text(ctx, 'LASSEN', w / 2, h * 0.6, w * 0.16, C);
  }
  ctx.globalAlpha = 1;
  ctx.fillStyle = 'rgba(255,255,255,.18)'; ctx.fillRect(w * 0.1, h * 0.9, w * 0.8, h * 0.008);
  ctx.fillStyle = C; ctx.fillRect(w * 0.1, h * 0.9, w * 0.8 * local, h * 0.008);
}

function labelSprite(str) {
  const c = document.createElement('canvas'); c.width = 256; c.height = 96;
  const x = c.getContext('2d');
  x.fillStyle = 'rgba(88,208,189,.95)';
  x.beginPath(); x.roundRect ? x.roundRect(8, 14, 240, 68, 18) : x.rect(8, 14, 240, 68); x.fill();
  x.strokeStyle = 'rgba(255,255,255,.9)'; x.lineWidth = 3; x.stroke();
  text(x, str, 128, 49, 50, '#0f2440', { weight: 800 });
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, depthTest: false, transparent: true, toneMapped: false }));
  sp.scale.set(0.95, 0.36, 1); sp.renderOrder = 10;
  return sp;
}

/* ── Szene ──────────────────────────────────────────── */
export async function init(hero) {
  const stage = hero.querySelector('.mb-stage');
  const canvas = stage.querySelector('canvas');
  const ui = hero.querySelector('.mb-ui');
  const $ = s => hero.querySelector(s);
  const $$ = s => [...hero.querySelectorAll(s)];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const small = matchMedia('(max-width: 900px)');

  try {
    await Promise.race([
      Promise.all([document.fonts.load('900 64px "Barlow Condensed"'), document.fonts.load('500 32px "Barlow"'), document.fonts.load('800 32px "Barlow Condensed"')]),
      new Promise(r => setTimeout(r, 2500)),
    ]);
  } catch (e) { /* Schrift-Fallback reicht */ }

  /* Nachbearbeitung nur auf Desktop laden */
  let POST = null;
  if (!small.matches) { try { POST = await import('./mb-post.js'); } catch (e) { POST = null; } }

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: !POST, alpha: true, powerPreference: 'high-performance' });
  const PR = Math.min(window.devicePixelRatio || 1, small.matches ? 1.75 : 2);
  renderer.setPixelRatio(PR);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.0;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  const aniso = renderer.capabilities.getMaxAnisotropy();
  const MAXT = renderer.capabilities.maxTextureSize || 4096;
  /* Grafik-Auflösung: Desktop schärfer, Smartphone Standard (Speicher) */
  const Q = !small.matches && MAXT >= 4096 ? 1.6 : 1;

  const scene = new THREE.Scene();
  /* Studio-Umgebung für realistische Reflexionen auf Metall, Theke und Folien */
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environmentIntensity = 0.55;
  pmrem.dispose();
  const camera = new THREE.PerspectiveCamera(30, 1, 0.1, 100);

  /* Hintergrund passend zum Seitenkopf (die Nachbearbeitung braucht ein deckendes Bild) */
  const bgC = document.createElement('canvas'); bgC.width = 64; bgC.height = 256;
  const bgX = bgC.getContext('2d');
  const bgG = bgX.createLinearGradient(0, 0, 0, 256);
  bgG.addColorStop(0, '#11294a'); bgG.addColorStop(0.55, '#132e50'); bgG.addColorStop(1, '#0f3f45');
  bgX.fillStyle = bgG; bgX.fillRect(0, 0, 64, 256);
  const bgTex = new THREE.CanvasTexture(bgC); bgTex.colorSpace = THREE.SRGBColorSpace;

  /* Standgrafik als Canvas-Texturen */
  const tex = {};
  const makeTex = (key, w, h, wrap = false, q = Q) => {
    const c = document.createElement('canvas');
    c.width = Math.round(w * q); c.height = Math.round(h * q);
    const t = new THREE.CanvasTexture(c);
    t.colorSpace = THREE.SRGBColorSpace;
    t.anisotropy = aniso;
    if (wrap) t.wrapS = THREE.RepeatWrapping;
    tex[key] = { c, t, ctx: c.getContext('2d'), mats: [], w, h, wrap };
    return t;
  };
  /* Textur mit neuer Breite neu anlegen (Grafik bleibt unverzerrt) */
  const retex = (key, w) => {
    const o = tex[key];
    const W = Math.min(Math.round(w * Q), MAXT);
    if (o.c.width === W) return;
    const c = document.createElement('canvas'); c.width = W; c.height = o.c.height;
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = aniso;
    o.mats.forEach(m => { m.map = t; m.needsUpdate = true; });
    o.t.dispose();
    Object.assign(o, { c, t, ctx: c.getContext('2d') });
  };

  makeTex('wall', 2048, 1112);
  makeTex('side', 1312, 1112);
  makeTex('counter', 2048, 560);
  makeTex('rollupA', 768, 1809);
  makeTex('rollupB', 768, 1809);
  makeTex('flag', 768, 2496);
  makeTex('ring', 2048, 256, true);
  const scr = { c: document.createElement('canvas') };
  scr.c.width = 432; scr.c.height = 768;
  scr.ctx = scr.c.getContext('2d');
  scr.t = new THREE.CanvasTexture(scr.c); scr.t.colorSpace = THREE.SRGBColorSpace; scr.t.anisotropy = aniso;

  const mat = (o) => new THREE.MeshStandardMaterial(o);
  const white = mat({ color: 0xf4f6f8, roughness: 0.3 });
  const dark = mat({ color: 0x1b2433, roughness: 0.5, metalness: 0.3 });
  const metal = mat({ color: 0xd4d8de, roughness: 0.22, metalness: 0.9 });
  const alu = mat({ color: 0xc8cdd4, roughness: 0.32, metalness: 0.85 });
  const wood = mat({ color: 0xb98a5a, roughness: 0.6 });
  const accentDark = mat({ color: 0x1b2a3d, roughness: 0.45 });
  const print = (t, extra = {}) => mat({ map: t, roughness: 0.5, ...extra });
  const printK = (key, extra) => { const m = print(tex[key].t, extra); tex[key].mats.push(m); return m; };

  const shadowed = (m, cast = true, receive = true) => { m.castShadow = cast; m.receiveShadow = receive; return m; };
  const booth = new THREE.Group();
  scene.add(booth);
  const FLOOR = 0.12;
  let PW = state.w, PD = state.d;
  const add = (parent, m, x = 0, y = 0, z = 0) => { m.position.set(x, y, z); parent.add(m); return m; };
  const group = (parent = booth) => add(parent, new THREE.Group());

  /* Teppich mit feiner Struktur (prozedurale Bump-Map) */
  const nC = document.createElement('canvas'); nC.width = nC.height = 256;
  const nX = nC.getContext('2d'); const nD = nX.createImageData(256, 256);
  for (let i = 0; i < nD.data.length; i += 4) { const v = 110 + Math.random() * 90; nD.data[i] = nD.data[i + 1] = nD.data[i + 2] = v; nD.data[i + 3] = 255; }
  nX.putImageData(nD, 0, 0);
  const nT = new THREE.CanvasTexture(nC); nT.wrapS = nT.wrapT = THREE.RepeatWrapping; nT.repeat.set(10, 7);
  const carpet = mat({ color: 0x4b515b, roughness: 1, bumpMap: nT, bumpScale: 0.6 });

  /* Podest mit Lichtkante */
  const podium = group();
  add(podium, shadowed(new THREE.Mesh(new THREE.BoxGeometry(6, FLOOR, 4), [metal, metal, carpet, dark, metal, metal]), false, true), 0, FLOOR / 2, 0);
  const led = new THREE.MeshBasicMaterial({ color: 0xfff1d0, toneMapped: false });
  [[6.02, 0.028, 0.028, 0, FLOOR - 0.02, 2], [0.028, 0.028, 4.02, -3, FLOOR - 0.02, 0], [0.028, 0.028, 4.02, 3, FLOOR - 0.02, 0]]
    .forEach(([w, h, d, x, y, z]) => add(podium, new THREE.Mesh(new THREE.BoxGeometry(w, h, d), led), x, y, z));

  /* Lichtschein auf dem Boden + Schatten */
  const gc = document.createElement('canvas'); gc.width = gc.height = 256;
  const gx = gc.getContext('2d');
  const rg = gx.createRadialGradient(128, 128, 20, 128, 128, 128);
  rg.addColorStop(0, 'rgba(255,240,210,.55)'); rg.addColorStop(1, 'rgba(255,240,210,0)');
  gx.fillStyle = rg; gx.fillRect(0, 0, 256, 256);
  const glow = new THREE.Mesh(new THREE.PlaneGeometry(9.5, 7), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(gc), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, opacity: 0.55 }));
  glow.rotation.x = -Math.PI / 2; glow.position.y = 0.002;
  scene.add(glow);
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(40, 40), new THREE.ShadowMaterial({ opacity: 0.35 }));
  ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true;
  scene.add(ground);

  /* Licht */
  scene.add(new THREE.HemisphereLight(0xdff6ff, 0x1a2536, 0.6));
  const key = new THREE.DirectionalLight(0xffffff, 2.1);
  key.position.set(4, 8, 7); key.castShadow = true;
  Object.assign(key.shadow.camera, { left: -5, right: 5, top: 5, bottom: -5, near: 1, far: 25 });
  key.shadow.mapSize.setScalar(small.matches ? 1024 : 2048); key.shadow.bias = -0.0004; key.shadow.normalBias = 0.02;
  scene.add(key);
  const fill = new THREE.DirectionalLight(0xbfe9ff, 0.6);
  fill.position.set(-6, 4, 3);
  scene.add(fill);

  /* Gebogene Rückwand (Pop-up-Wand) mit Strahlern */
  const WW = 4.8, WH = 2.55, SAG = 0.55, WZ = -1.45;
  const backRig = group();
  const wg = new THREE.PlaneGeometry(WW, WH, 60, 1);
  const wp = wg.attributes.position;
  for (let i = 0; i < wp.count; i++) { const x = wp.getX(i); wp.setZ(i, SAG * (x / (WW / 2)) ** 2); }
  wg.computeVertexNormals();
  const wall = add(backRig, new THREE.Group(), 0, FLOOR + WH / 2, WZ);
  wall.add(shadowed(new THREE.Mesh(wg, printK('wall', { roughness: 0.55 }))));
  wall.add(new THREE.Mesh(wg, mat({ color: 0x222c3a, roughness: 0.7, side: THREE.BackSide })));
  const slope = Math.atan(2 * SAG / (WW / 2));
  [-1, 1].forEach(sd => {
    const cap = add(wall, shadowed(new THREE.Mesh(new THREE.BoxGeometry(0.09, WH + 0.02, 0.34), accentDark)), sd * (WW / 2 + 0.03), 0, SAG - 0.1);
    cap.rotation.y = -sd * slope;
  });
  const lensMat = new THREE.MeshBasicMaterial({ color: 0xfff6e0, toneMapped: false });
  const wallSpots = [-1.5, 0, 1.5].map(x => {
    const zTop = WZ + SAG * (x / (WW / 2)) ** 2;
    const y = FLOOR + WH;
    const sg = add(backRig, new THREE.Group(), x, 0, 0);
    add(sg, new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.03, 0.38), dark), 0, y + 0.05, zTop + 0.17);
    const head = add(sg, new THREE.Group(), 0, y + 0.06, zTop + 0.38);
    head.rotation.x = 2.3;
    head.add(new THREE.Mesh(new THREE.CylinderGeometry(0.055, 0.08, 0.17, 20), dark));
    add(head, new THREE.Mesh(new THREE.CircleGeometry(0.07, 20), lensMat), 0, -0.086, 0).rotation.x = Math.PI / 2;
    const sp = new THREE.SpotLight(0xfff1dc, 22, 0, 0.6, 0.65, 2);
    sp.position.set(0, y + 0.02, zTop + 0.4);
    sp.target.position.set(0, FLOOR + 1.35, zTop);
    sg.add(sp, sp.target);
    return { sg, x };
  });

  /* Seitenwände (Reihen- und Eckstand) */
  const SD = 2.7, SX = PW / 2 - 0.08, SZ = -0.62;
  function sideWall(sd) {
    const g = add(booth, new THREE.Group(), sd * SX, FLOOR + WH / 2, SZ);
    g.rotation.y = -sd * Math.PI / 2;
    const pg = new THREE.PlaneGeometry(SD, WH);
    g.add(shadowed(new THREE.Mesh(pg, printK('side', { roughness: 0.55 }))));
    g.add(new THREE.Mesh(pg, mat({ color: 0x222c3a, roughness: 0.7, side: THREE.BackSide })));
    add(g, shadowed(new THREE.Mesh(new THREE.BoxGeometry(SD + 0.04, 0.05, 0.08), accentDark)), 0, WH / 2 + 0.02, 0);
    add(g, shadowed(new THREE.Mesh(new THREE.BoxGeometry(0.08, WH + 0.04, 0.1), accentDark)), sd * (SD / 2), 0, 0);
    return g;
  }
  const leftWall = sideWall(-1);
  const rightWall = sideWall(1);

  /* Hängebanner (Inselstand) */
  const ringRig = add(booth, new THREE.Group(), 0.1, FLOOR + 3.55, 0.1);
  const rg2 = new THREE.CylinderGeometry(1.35, 1.35, 0.72, 96, 1, true);
  ringRig.add(shadowed(new THREE.Mesh(rg2, print(tex.ring.t, { roughness: 0.55 })), true, false));
  ringRig.add(new THREE.Mesh(rg2, mat({ color: 0xe8ecf0, roughness: 0.8, side: THREE.BackSide })));
  [0, 1, 2, 3].forEach(i => {
    const a = i * Math.PI / 2 + Math.PI / 4;
    add(ringRig, new THREE.Mesh(new THREE.CylinderGeometry(0.004, 0.004, 3, 4), metal), Math.cos(a) * 1.3, 1.85, Math.sin(a) * 1.3);
  });

  /* Theke (Klarlack-Platte) */
  const counter = add(booth, new THREE.Group(), 0.25, FLOOR, 0.45);
  const sx = 1.35, sz = 0.72;
  add(counter, shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.62, 0.62, 0.98, 72, 1, true, Math.PI, Math.PI * 2), print(tex.counter.t, { roughness: 0.4 }))), 0, 0.53, 0).scale.set(sx, 1, sz);
  add(counter, shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.67, 0.67, 0.05, 72), new THREE.MeshPhysicalMaterial({ color: 0x1c2129, roughness: 0.25, metalness: 0.2, clearcoat: 1, clearcoatRoughness: 0.06 }))), 0, 1.045, 0).scale.set(sx, 1, sz);
  add(counter, shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.6, 0.6, 0.05, 72), dark)), 0, 0.025, 0).scale.set(sx, 1, sz);
  add(counter, shadowed(new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.035, 0.2), white)), -0.05, 1.088, 0.05).rotation.y = 0.2;
  const holder = add(counter, new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.26, 0.07), new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: 0.04, transparent: true, opacity: 0.3 })), 0.48, 1.2, 0.02);
  holder.rotation.set(-0.12, -0.3, 0);
  const flyer = add(counter, new THREE.Mesh(new THREE.PlaneGeometry(0.17, 0.24), print(tex.rollupA.t)), 0.48, 1.2, 0.03);
  flyer.rotation.set(-0.12, -0.3, 0);

  /* Roll-ups */
  const rollups = group();
  function rollup(t, x, z, ry) {
    const g = add(rollups, new THREE.Group(), x, FLOOR, z);
    g.rotation.y = ry;
    const W = 0.85, H = 2.0;
    add(g, shadowed(new THREE.Mesh(new THREE.PlaneGeometry(W, H), print(t))), 0, 0.13 + H / 2, 0);
    add(g, new THREE.Mesh(new THREE.PlaneGeometry(W, H), mat({ color: 0xd9dde2, roughness: 0.8, side: THREE.BackSide })), 0, 0.13 + H / 2, 0);
    add(g, shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, W + 0.06, 24), metal)), 0, 0.075, 0.01).rotation.z = Math.PI / 2;
    add(g, new THREE.Mesh(new THREE.CylinderGeometry(0.013, 0.013, W + 0.02, 12), metal), 0, 0.13 + H, 0.005).rotation.z = Math.PI / 2;
    add(g, new THREE.Mesh(new THREE.CylinderGeometry(0.009, 0.009, H, 8), metal), 0, 0.13 + H / 2, -0.03);
    [-1, 1].forEach(s => add(g, new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.02, 0.3), metal), s * (W / 2 - 0.05), 0.01, 0));
    return g;
  }
  const rollA = rollup(tex.rollupA.t, -2.45, 0.3, 0.32);
  const rollB = rollup(tex.rollupB.t, 2.5, -0.55, -0.45);

  /* Beachflag (Feder-Form, weht leicht) */
  const flag = add(booth, new THREE.Group(), 2.2, FLOOR, 1.3);
  flag.rotation.y = 0.2;
  const fg = new THREE.PlaneGeometry(1, 1, 14, 44);
  const fp = fg.attributes.position, fuv = fg.attributes.uv;
  const yTop = u => 3.05 - 0.3 * u * u, yBot = 0.62;
  const wid = v => 0.44 + 0.3 * Math.pow(v, 1.4);
  const base = new Float32Array(fp.count * 3);
  for (let i = 0; i < fp.count; i++) {
    const u = fuv.getX(i), v = fuv.getY(i);
    const x = u * wid(v), y = yBot + (yTop(u) - yBot) * v;
    fp.setXYZ(i, x, y, 0); base.set([x, y, 0], i * 3);
  }
  fg.computeVertexNormals();
  flag.add(shadowed(new THREE.Mesh(fg, print(tex.flag.t, { roughness: 0.6, side: THREE.DoubleSide }))));
  const polePts = [new THREE.Vector3(0, 0.02, 0), new THREE.Vector3(0, 1.8, 0), new THREE.Vector3(0, 3.05, 0)];
  for (let k = 1; k <= 6; k++) { const u = k / 6; polePts.push(new THREE.Vector3(u * wid(1), yTop(u), 0)); }
  const fpole = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(polePts), 64, 0.014, 8), dark);
  fpole.castShadow = true;
  flag.add(fpole);
  add(flag, shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.26, 0.05, 32), dark)), 0, 0.025, 0);

  /* Sitzecke */
  const seating = group();
  const table = add(seating, new THREE.Group(), 1.4, FLOOR, -0.55);
  add(table, shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.38, 0.03, 40), white)), 0, 0.74, 0);
  add(table, shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.72, 12), metal)), 0, 0.37, 0);
  add(table, shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.25, 0.025, 32), metal)), 0, 0.012, 0);
  function chair(x, z, ry) {
    const g = add(seating, new THREE.Group(), x, FLOOR, z); g.rotation.y = ry;
    add(g, shadowed(new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.05, 0.42), white)), 0, 0.46, 0);
    add(g, shadowed(new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.36, 0.04), white)), 0, 0.68, -0.2).rotation.x = -0.12;
    [[-1, -1], [1, -1], [-1, 1], [1, 1]].forEach(([a, b]) => {
      const l = add(g, shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.012, 0.47, 8), wood)), a * 0.16, 0.225, b * 0.16);
      l.rotation.set(b * 0.08, 0, -a * 0.08);
    });
  }
  chair(0.95, -0.35, 1.2);
  chair(1.85, -0.3, -1.25);
  /* Sitzecke als Einheit um ihren Mittelpunkt verschiebbar */
  seating.children.forEach(c => { c.position.x -= 1.4; c.position.z += 0.5; });
  seating.position.set(1.4, 0, -0.5);

  /* Pflanzen */
  const plants = group();
  const leafGeo = new THREE.SphereGeometry(1, 12, 8);
  const greens = [0x2f7d3b, 0x3d9447, 0x28692f, 0x4aa653].map(c => mat({ color: c, roughness: 0.55 }));
  const potMat = mat({ color: 0xf5f5f2, roughness: 0.2 });
  function plant(x, y, z, s) {
    const g = add(plants, new THREE.Group(), x, y, z); g.scale.setScalar(s);
    add(g, shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.15, 0.5, 32), potMat)), 0, 0.25, 0);
    add(g, new THREE.Mesh(new THREE.CircleGeometry(0.19, 24), mat({ color: 0x3a2a1e, roughness: 1 })), 0, 0.49, 0).rotation.x = -Math.PI / 2;
    const n = 20;
    for (let i = 0; i < n; i++) {
      const a = (i / n) * Math.PI * 2 + (i % 3) * 0.4, tilt = 0.25 + ((i * 7) % 10) / 14, len = 0.3 + ((i * 5) % 7) / 28;
      const leaf = shadowed(new THREE.Mesh(leafGeo, greens[i % 4]), true, false);
      leaf.scale.set(0.075, len, 0.012);
      const piv = add(g, new THREE.Group(), 0, 0.5, 0); piv.rotation.y = a;
      const inner = add(piv, new THREE.Group()); inner.rotation.x = tilt;
      add(inner, leaf, 0, len, 0);
    }
    return g;
  }
  const plantBig = plant(-1.9, FLOOR, -0.8, 1.25);
  const plantSmall = plant(-0.45, FLOOR + 1.07, 0.45, 0.42);
  counter.attach(plantSmall);   /* steht auf der Theke und wandert mit */

  /* LED-Stele mit bewegtem Inhalt */
  const screen = add(booth, new THREE.Group(), -1.3, FLOOR, 1.2);
  screen.rotation.y = 0.28;
  const SW_ = 0.62, SH_ = 1.1;
  add(screen, shadowed(new THREE.Mesh(new THREE.BoxGeometry(SW_ + 0.08, SH_ + 0.08, 0.07), dark)), 0, 0.72 + SH_ / 2, 0);
  add(screen, new THREE.Mesh(new THREE.PlaneGeometry(SW_, SH_), new THREE.MeshBasicMaterial({ map: scr.t, toneMapped: false })), 0, 0.72 + SH_ / 2, 0.037);
  add(screen, shadowed(new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.72, 0.1), dark)), 0, 0.36, -0.02);
  add(screen, shadowed(new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.03, 0.4), dark)), 0, 0.015, -0.02);

  /* Lichttraverse (4-Punkt-Truss) mit Scheinwerfern */
  const truss = group();
  truss.position.y = FLOOR + 3.25;
  let TX = 2.6, TZ = 1.7;
  const TR = 0.14;
  const chordGeo = new THREE.CylinderGeometry(0.018, 0.018, 1, 8);
  const braceGeo = new THREE.CylinderGeometry(0.007, 0.007, 1, 6);
  function bar(p, q, geo, parent) {
    const d = new THREE.Vector3().subVectors(q, p), m = new THREE.Mesh(geo, alu);
    m.position.copy(p).addScaledVector(d, 0.5); m.scale.y = d.length();
    m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize());
    parent.add(m); return m;
  }
  function beam(a, b) {
    const dir = new THREE.Vector3().subVectors(b, a), len = dir.length(); dir.normalize();
    const side = new THREE.Vector3(-dir.z, 0, dir.x).multiplyScalar(TR / 2), up = new THREE.Vector3(0, TR, 0);
    const corners = [side.clone(), side.clone().negate(), side.clone().add(up), side.clone().negate().add(up)];
    corners.forEach(c => bar(a.clone().add(c), b.clone().add(c), chordGeo, truss));
    const n = Math.max(2, Math.round(len / 0.28));
    for (let i = 0; i < n; i++) {
      const p = a.clone().addScaledVector(dir, (i / n) * len), q = a.clone().addScaledVector(dir, ((i + 1) / n) * len);
      bar(p.clone().add(corners[i % 2 ? 0 : 2]), q.clone().add(corners[i % 2 ? 2 : 0]), braceGeo, truss);
      bar(p.clone().add(corners[i % 2 ? 1 : 3]), q.clone().add(corners[i % 2 ? 3 : 1]), braceGeo, truss);
    }
  }
  function buildTruss() {
    truss.children.slice().forEach(c => { truss.remove(c); });
    TX = Math.max(1.4, PW / 2 - 0.4); TZ = Math.max(1, PD / 2 - 0.3);
    const tc = [new THREE.Vector3(-TX, 0, -TZ), new THREE.Vector3(TX, 0, -TZ), new THREE.Vector3(TX, 0, TZ), new THREE.Vector3(-TX, 0, TZ)];
    for (let i = 0; i < 4; i++) beam(tc[i], tc[(i + 1) % 4]);
    tc.forEach(c => add(truss, new THREE.Mesh(new THREE.BoxGeometry(TR + 0.06, TR + 0.06, TR + 0.06), alu), c.x, TR / 2, c.z));
    tc.forEach(c => add(truss, new THREE.Mesh(new THREE.CylinderGeometry(0.004, 0.004, 2.6, 4), metal), c.x, 1.4, c.z));
    [[-TX / 2, TZ], [TX / 2, TZ], [-TX / 2, -TZ], [TX / 2, -TZ]].forEach(([x, z]) => {
      const head = add(truss, new THREE.Group(), x, -0.12, z);
      head.lookAt(new THREE.Vector3(x * 0.4, -3, z * 0.2).add(truss.position));
      head.add(new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.1, 0.22, 16), dark).rotateX(Math.PI / 2));
      add(head, new THREE.Mesh(new THREE.CircleGeometry(0.085, 16), lensMat), 0, 0, 0.112);
      const sp = new THREE.SpotLight(0xfff4e2, 16, 0, 0.5, 0.7, 2);
      sp.position.set(x, -0.15, z);
      sp.target.position.set(x * 0.4, -3.1, z * 0.2);
      truss.add(sp, sp.target);
    });
  }
  buildTruss();

  /* Maße */
  const dims = group();
  const dimMat = new THREE.LineBasicMaterial({ color: 0x58d0bd, depthTest: false, transparent: true });
  function dimLine(a, b, label, off) {
    const pts = [a, b];
    const tick = off.clone().setLength(0.12);
    [a, b].forEach(p => pts.push(p.clone().sub(tick), p.clone().add(tick)));
    const g = new THREE.BufferGeometry().setFromPoints([pts[0], pts[1], pts[2], pts[3], pts[4], pts[5]]);
    const l = new THREE.LineSegments(g, dimMat); l.renderOrder = 9; dims.add(l);
    const sp = labelSprite(label); sp.position.copy(a).add(b).multiplyScalar(0.5).add(off.clone().setLength(0.34)); dims.add(sp);
  }
  const mfmt = v => String(Math.round(v * 10) / 10).replace('.', ',') + ' m';
  function buildDims() {
    dims.children.slice().forEach(c => { dims.remove(c); if (c.geometry) c.geometry.dispose(); if (c.material && c.material.map) { c.material.map.dispose(); c.material.dispose(); } });
    dimLine(new THREE.Vector3(-PW / 2, FLOOR + 0.01, PD / 2 + 0.35), new THREE.Vector3(PW / 2, FLOOR + 0.01, PD / 2 + 0.35), mfmt(PW), new THREE.Vector3(0, 0, 1));
    dimLine(new THREE.Vector3(PW / 2 + 0.35, FLOOR + 0.01, -PD / 2), new THREE.Vector3(PW / 2 + 0.35, FLOOR + 0.01, PD / 2), mfmt(PD), new THREE.Vector3(1, 0, 0));
    const ws = wall.scale.x, wz = backRig.position.z + WZ + SAG;
    dimLine(new THREE.Vector3(-WW * ws / 2 - 0.35, FLOOR, wz), new THREE.Vector3(-WW * ws / 2 - 0.35, FLOOR + WH, wz), '2,5 m', new THREE.Vector3(-1, 0, 0));
  }

  /* ── Verschiebbare Elemente ────────────────────── */
  /* Standardpositionen gelten für 6 × 4 m und werden mit der Standgröße mitskaliert */
  const MOV = {
    counter: { obj: counter, name: 'Theke', r: 0.85 },
    screen: { obj: screen, name: 'LED-Stele', r: 0.45, extra: 'screen' },
    flag: { obj: flag, name: 'Beachflag', r: 0.5, extra: 'flag' },
    rollA: { obj: rollA, name: 'Roll-up links', r: 0.55, extra: 'rollups' },
    rollB: { obj: rollB, name: 'Roll-up rechts', r: 0.55, extra: 'rollups' },
    seating: { obj: seating, name: 'Sitzecke', r: 0.9, extra: 'seating' },
    plant: { obj: plantBig, name: 'Pflanze', r: 0.35, extra: 'plants' },
  };
  for (const k in MOV) { const o = MOV[k].obj; MOV[k].def = { x: o.position.x, z: o.position.z, r: o.rotation.y }; }
  const clampPos = (k, x, z) => {
    const m = MOV[k].r * 0.6;
    return [THREE.MathUtils.clamp(x, -PW / 2 + m, PW / 2 - m), THREE.MathUtils.clamp(z, -PD / 2 + m * 0.6, PD / 2 - m * 0.5)];
  };
  function placeMovables() {
    const sx = PW / 6, sz = PD / 4;
    for (const k in MOV) {
      const { obj, def } = MOV[k], p = state.pos[k];
      const [x, z] = clampPos(k, p ? p.x : def.x * sx, p ? p.z : def.z * sz);
      obj.position.x = x; obj.position.z = z;
      obj.rotation.y = p && p.r != null ? p.r : def.r;
    }
  }

  /* ── Standgröße anwenden ───────────────────────── */
  function layout() {
    PW = state.w; PD = state.d;
    podium.scale.set(PW / 6, 1, PD / 4);
    glow.scale.set(PW / 6 * 1.05, PD / 4 * 1.05, 1);
    nT.repeat.set(10 * PW / 6, 7 * PD / 4);
    /* Rückwand: breiter Stand → breitere Wand, Grafik wird neu im passenden Format gezeichnet */
    const ws = THREE.MathUtils.clamp((PW - 1.2) / WW, 0.6, 1.8);
    wall.scale.x = ws;
    wallSpots.forEach(o => { o.sg.position.x = o.x * ws; });
    retex('wall', 2048 * ws);
    backRig.position.z = (-PD / 2 + 0.55) - WZ;
    /* Seitenwände über die Standtiefe */
    const sd = Math.max(1.6, PD - 1.3), ss = sd / SD;
    [[leftWall, -1], [rightWall, 1]].forEach(([g, d]) => { g.position.set(d * (PW / 2 - 0.08), FLOOR + WH / 2, -PD / 2 + 0.03 + sd / 2); g.scale.x = ss; });
    retex('side', 1312 * ss);
    buildTruss();
    buildDims();
    placeMovables();
    Object.assign(key.shadow.camera, { left: -(PW / 2 + 2), right: PW / 2 + 2, top: PD / 2 + 3, bottom: -(PD / 2 + 3) });
    key.shadow.camera.updateProjectionMatrix();
    $$('.mb-dim[data-k="w"] button').forEach(b => b.setAttribute('aria-pressed', String(+b.dataset.v === PW)));
    $$('.mb-dim[data-k="d"] button').forEach(b => b.setAttribute('aria-pressed', String(+b.dataset.v === PD)));
    const sl = $('.mb-size-lbl'); if (sl) sl.textContent = `${PW} × ${PD} m · ${PW * PD} m²`;
  }

  /* ── Grafik neu zeichnen ───────────────────────── */
  function repaint() {
    const C = state.color;
    for (const k in tex) {
      const { c, ctx, t } = tex[k];
      ctx.clearRect(0, 0, c.width, c.height);
      PAINT[k](ctx, c.width, c.height, C);
      t.needsUpdate = true;
    }
    paintScreen(scr.ctx, scr.c.width, scr.c.height, clock ? clock.elapsedTime : 0, C);
    scr.t.needsUpdate = true;
    accentDark.color.set(mix(C, NAVY, 0.8));
    hero.style.setProperty('--mb-accent', C);
    kick();
  }

  /* ── Sichtbarkeit von Standtyp und Ausstattung ─── */
  const EXTRA_OBJ = { screen, truss, seating, plants, flag, rollups };
  function applyVisibility() {
    const t = state.type;
    backRig.visible = t !== 'insel';
    leftWall.visible = t === 'reihe' || t === 'eck';
    rightWall.visible = t === 'reihe';
    ringRig.visible = t === 'insel' && !state.extras.truss;
    for (const k in EXTRA_OBJ) EXTRA_OBJ[k].visible = !!state.extras[k];
    plantSmall.visible = !!state.extras.plants;
    if (typeof sel !== 'undefined' && sel && !shown(sel)) select(null);
    if (typeof updateParts === 'function') updateParts();
    dims.visible = state.dims;
    $$('.mb-chip[data-extra]').forEach(b => b.setAttribute('aria-pressed', String(!!state.extras[b.dataset.extra])));
    $$('.mb-chip[data-dims]').forEach(b => b.setAttribute('aria-pressed', String(state.dims)));
    kick();
  }
  function setType(t) {
    if (!TYPES[t]) return;
    state.type = t;
    applyVisibility();
    $$('.mb-seg button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.type === t)));
    const lbl = $('.mb-type-lbl');
    if (lbl) lbl.textContent = `${TYPES[t].name} · ${TYPES[t].open}`;
    if (state.view === 'standard') { tYaw = TYPES[t].yaw; tPitch = TYPES[t].pitch; }
    lastMove = performance.now();
    resize();
  }
  function setView(v) {
    state.view = v;
    $$('.mb-view button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.view === v)));
    if (v === 'top') { tYaw = 0.0001; tPitch = 1.02; }
    else if (v === 'standard') { tYaw = cfg().yaw; tPitch = cfg().pitch; }
    else if (v === 'besucher') { tYaw = 0.12; tPitch = 0.02; }
    else { tPitch = 0.16; }
    lastMove = performance.now();
    resize();
  }

  /* ── Kamera & Eingabe ──────────────────────────── */
  const T = new THREE.Vector3(0, 1.2, 0);
  let yaw = TYPES.kopf.yaw, pitch = TYPES.kopf.pitch, tYaw = yaw, tPitch = pitch, dist = 14, lastMove = -1e9;
  const cfg = () => TYPES[state.type];

  let drag = null;
  canvas.addEventListener('pointerdown', e => {
    if (state.arrange) return;
    if (e.pointerType === 'mouse') return;
    drag = { x: e.clientX, yaw: tYaw };
  }, { passive: true });
  canvas.addEventListener('pointermove', e => {
    if (!drag) return;
    if (state.view === 'tour') setView('standard');
    const dx = (e.clientX - drag.x) / Math.max(stage.clientWidth, 1);
    tYaw = THREE.MathUtils.clamp(drag.yaw + dx * 2.6, cfg().yaw - 1.2, cfg().yaw + 1.2);
    lastMove = performance.now() + 2000;
    kick();
  }, { passive: true });
  const endDrag = () => { drag = null; };
  canvas.addEventListener('pointerup', endDrag);
  canvas.addEventListener('pointercancel', endDrag);
  if (!reduced) {
    hero.addEventListener('pointermove', e => {
      if (e.pointerType !== 'mouse' || small.matches || state.view !== 'standard' || state.arrange) return;
      if (ui && ui.contains(e.target)) return;
      const r = hero.getBoundingClientRect();
      const nx = (e.clientX - r.left) / r.width * 2 - 1;
      const ny = (e.clientY - r.top) / r.height * 2 - 1;
      tYaw = cfg().yaw + nx * cfg().range;
      tPitch = cfg().pitch - ny * 0.07;
      lastMove = performance.now();
      kick();
    }, { passive: true });
    hero.addEventListener('pointerleave', () => { lastMove = performance.now() - 1500; });
  }

  function fit(w, h, fracW, fracH) {
    const vt = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));
    const tall = state.type === 'insel' || state.extras.truss;
    const halfH = state.view === 'top' ? 2.3 : (tall ? 2.25 : 1.75);
    T.y = state.view === 'top' ? 0.6 : (tall ? 1.75 : 1.2);
    if (state.view === 'besucher') { T.y = 1.6; return Math.max(PD / 2 + 3.2, (PW / 2 + 0.6) / (vt * (w / h) * fracW)); }
    const halfW = PW / 2 + (state.dims ? 0.7 : 0.35) + Math.max(0, PD - 4) * 0.25;
    return Math.max(halfW / (vt * (w / h) * fracW), halfH / (vt * fracH), 8);
  }

  /* ── Nachbearbeitung (Desktop) ─────────────────── */
  let composer = null, gtao = null, bloom = null, smaa = null;
  const postPR = () => Math.min(window.devicePixelRatio || 1, 1.5);
  if (POST) {
    try {
      scene.background = bgTex;
      composer = new POST.EffectComposer(renderer);
      composer.setPixelRatio(postPR());
      composer.addPass(new POST.RenderPass(scene, camera));
      /* Umgebungsverdeckung (GTAO) bewusst nicht: sie erzeugte hinter verschiebbaren Möbeln
         einen dunklen Kasten im Bild. Weiche Schatten der Schlüssellicht-Quelle übernehmen das. */
      bloom = new POST.UnrealBloomPass(new THREE.Vector2(800, 600), 0.5, 0.35, 5.5);
      composer.addPass(bloom);
      smaa = new POST.SMAAPass(800, 600);
      composer.addPass(smaa);
      composer.addPass(new POST.OutputPass());
      /* Lichtquellen heller als Weiß, damit nur sie leuchten */
      led.color.multiplyScalar(9); lensMat.color.multiplyScalar(12);
      renderer.setPixelRatio(postPR());
    } catch (e) { composer = null; scene.background = null; }
  }
  const draw = () => { if (composer) composer.render(); else renderer.render(scene, camera); };
  const sizeAll = (w, h) => {
    renderer.setSize(w, h, false);
    if (composer) composer.setSize(w, h);
  };

  function resize() {
    const w = stage.clientWidth, h = stage.clientHeight;
    if (!w || !h) return;
    sizeAll(w, h);
    camera.aspect = w / h;
    camera.fov = state.view === 'besucher' ? 50 : 30;
    if (small.matches) {
      dist = fit(w, h, 0.8, 0.8);
      camera.clearViewOffset();
    } else {
      dist = fit(w, h, w > 1100 ? 0.44 : 0.48, 0.66);
      camera.setViewOffset(w, h, -w * (w > 1100 ? 0.22 : 0.23), h * 0.07, w, h);
    }
    camera.updateProjectionMatrix();
    kick();
  }
  new ResizeObserver(resize).observe(stage);

  function place() {
    camera.position.set(T.x + dist * Math.sin(yaw) * Math.cos(pitch), T.y + dist * Math.sin(pitch), T.z + dist * Math.cos(yaw) * Math.cos(pitch));
    camera.lookAt(T);
  }

  /* ── Render-Schleife (nur wenn sichtbar), mit automatischer Qualitätsanpassung ── */
  let visible = true, running = false, first = true;
  new IntersectionObserver(([en]) => { visible = en.isIntersecting; kick(); }).observe(hero);
  document.addEventListener('visibilitychange', kick);
  const clock = new THREE.Clock();
  function kick() { if (!running && visible && !document.hidden) { running = true; clock.getDelta(); requestAnimationFrame(frame); } }
  let perfN = -40, perfSum = 0, perfLevel = 0, lastScreen = -1;
  function adapt(dt) {
    if (!composer || perfLevel >= 2) return;
    perfN++; if (perfN <= 0) return; perfSum += dt;
    if (perfN < 50) return;
    const avg = perfSum / perfN; perfN = 0; perfSum = 0;
    if (avg > 0.034) {
      perfLevel++;
      if (perfLevel === 1 && gtao) { gtao.enabled = false; }
      if (perfLevel === 2) { composer = null; scene.background = null; renderer.setPixelRatio(Math.min(PR, 1.5)); resize(); }
    }
  }

  let recording = null;
  function frame() {
    const dt = Math.min(clock.getDelta(), 0.05);
    const t = clock.elapsedTime;
    if (recording) {
      const pr = Math.min(1, (performance.now() - recording.t0) / recording.dur);
      tYaw = yaw = recording.yaw0 + pr * Math.PI * 2; tPitch = pitch = 0.17;
      if (pr >= 1 && !recording.stopped) { recording.stopped = true; recording.done(); }
    } else if (state.view === 'tour' && !reduced) {
      tYaw += dt * 0.32; tPitch = 0.16;
    } else if (state.view === 'standard' && !reduced && !state.arrange && performance.now() - lastMove > 2500) {
      tYaw = cfg().yaw + Math.sin(t * 0.22) * cfg().range * 0.55;
      tPitch = cfg().pitch + Math.sin(t * 0.17) * 0.03;
    }
    const k = 1 - Math.exp(-dt * 3.2);
    yaw += (tYaw - yaw) * k; pitch += (tPitch - pitch) * k;
    place();

    if (!reduced) {
      if (flag.visible) {
        for (let i = 0; i < fp.count; i++) {
          const x = base[i * 3], y = base[i * 3 + 1];
          const u = x / 0.74;
          fp.setZ(i, Math.sin(t * 2.1 + y * 2.2 + u * 2.5) * 0.045 * u);
        }
        fp.needsUpdate = true;
        fg.computeVertexNormals();
      }
      if (ringRig.visible) ringRig.rotation.y = t * 0.12;
      if (screen.visible && t - lastScreen > 1 / 24) {
        lastScreen = t;
        paintScreen(scr.ctx, scr.c.width, scr.c.height, t, state.color);
        scr.t.needsUpdate = true;
      }
    }

    draw();
    adapt(dt);
    if (first) { first = false; hero.classList.add('mb-3d'); document.documentElement.classList.add('mb-ready'); if (ui) ui.hidden = false; }
    const moving = !reduced || !!recording || Math.abs(tYaw - yaw) > 1e-3 || Math.abs(tPitch - pitch) > 1e-3;
    if (moving && visible && !document.hidden) requestAnimationFrame(frame);
    else running = false;
  }

  /* ── Entwurf als Bild ──────────────────────────── */
  const extrasText = () => Object.keys(EXTRAS).filter(k => state.extras[k]).map(k => EXTRAS[k]).join(', ') || 'keine';
  function snapshot(W = small.matches ? 1800 : 2400, H = small.matches ? 1125 : 1500) {
    const out = document.createElement('canvas');
    out.width = W; out.height = H;
    const o = out.getContext('2d');
    const bg = o.createLinearGradient(0, 0, W, H);
    bg.addColorStop(0, '#0b1f38'); bg.addColorStop(0.6, NAVY); bg.addColorStop(1, '#0d4a4a');
    o.fillStyle = bg; o.fillRect(0, 0, W, H);
    const SH = H - Math.round(H * 0.11);
    const SS = Math.max(1, Math.min(small.matches ? 1.25 : (composer ? 1.25 : 1.6), (MAXT * 0.9) / W));
    renderer.setPixelRatio(SS);
    if (composer) composer.setPixelRatio(SS);
    sizeAll(W, SH);
    camera.clearViewOffset();
    camera.aspect = W / SH;
    const d0 = dist;
    dist = fit(W, SH, 0.7, 0.78);
    place();
    camera.updateProjectionMatrix();
    draw();
    o.imageSmoothingEnabled = true; o.imageSmoothingQuality = 'high';
    o.drawImage(renderer.domElement, 0, 0, W, SH);
    dist = d0;
    renderer.setPixelRatio(composer ? postPR() : (perfLevel >= 2 ? Math.min(PR, 1.5) : PR));
    if (composer) composer.setPixelRatio(postPR());
    resize();
    place();
    draw();
    const FH = H - SH, Y1 = SH + FH * 0.38, Y2 = SH + FH * 0.74, P1 = Math.round(FH * 0.3), P2 = Math.round(FH * 0.2), M = Math.round(W * 0.03);
    o.fillStyle = 'rgba(0,0,0,.35)'; o.fillRect(0, SH, W, H - SH);
    o.fillStyle = state.color; o.fillRect(0, SH, W, 4);
    text(o, `3D-ENTWURF · ${TYPES[state.type].name.toUpperCase()} · ${PW} × ${PD} M · ${TYPES[state.type].open.toUpperCase()}`, M, Y1, P1, '#ffffff', { align: 'left', maxW: W * 0.55 });
    text(o, `Standfarbe: ${state.colorName} (${state.color})${state.name ? ' · ' + state.name : ''} · Ausstattung: ${extrasText()}`, M, Y2, P2, 'rgba(255,255,255,.75)', { weight: 500, family: '"Barlow"', align: 'left', maxW: W * 0.6 });
    text(o, 'MASAR WERBEAGENTUR · MESSEBAU BERLIN', W - M, Y1, Math.round(P1 * 0.88), state.color, { align: 'right', maxW: W * 0.38 });
    text(o, 'masar-werbeagentur.de · Unverbindliche Visualisierung', W - M, Y2, Math.round(P2 * 0.92), 'rgba(255,255,255,.7)', { weight: 500, family: '"Barlow"', align: 'right', maxW: W * 0.36 });
    return new Promise(res => { try { out.toBlob(b => res(b), 'image/jpeg', 0.93); } catch (e) { res(null); } });
  }

  const safeSnap = () => Promise.race([
    Promise.resolve().then(snapshot).catch(() => null),
    new Promise(r => setTimeout(() => r(null), 20000)),
  ]);

  /* ── Möbel verschieben (Maus & Touch) ──────────── */
  const ray = new THREE.Raycaster(), ndc = new THREE.Vector2(), hitP = new THREE.Vector3();
  const floorPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), -FLOOR);
  const selRing = new THREE.Mesh(new THREE.RingGeometry(0.9, 1, 56), new THREE.MeshBasicMaterial({ color: 0x58d0bd, transparent: true, opacity: 0.95, depthTest: false, toneMapped: false }));
  selRing.rotation.x = -Math.PI / 2; selRing.renderOrder = 8; selRing.visible = false; booth.add(selRing);
  let sel = null, mdrag = null;
  const movKeyOf = o => { while (o) { for (const k in MOV) if (MOV[k].obj === o) return k; o = o.parent; } return null; };
  const shown = k => !MOV[k].extra || !!state.extras[MOV[k].extra];
  function aim(e) {
    const r = canvas.getBoundingClientRect();
    ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    ray.setFromCamera(ndc, camera);
  }
  function pick(e) {
    aim(e);
    const objs = Object.keys(MOV).filter(shown).map(k => MOV[k].obj);
    const hit = ray.intersectObjects(objs, true)[0];
    return hit ? movKeyOf(hit.object) : null;
  }
  function ringTo() { if (sel) { const o = MOV[sel].obj; selRing.position.set(o.position.x, FLOOR + 0.012, o.position.z); } }
  function select(k) {
    sel = k && shown(k) ? k : null;
    selRing.visible = !!sel;
    if (sel) { selRing.scale.setScalar(MOV[sel].r); ringTo(); }
    const lbl = $('.mb-sel-lbl'); if (lbl) lbl.textContent = sel ? `Ausgewählt: ${MOV[sel].name}` : 'Element antippen und ziehen';
    $$('.mb-rot').forEach(b => { b.disabled = !sel; });
    kick();
  }
  const store = k => { const o = MOV[k].obj; state.pos[k] = { x: +o.position.x.toFixed(2), z: +o.position.z.toFixed(2), r: +o.rotation.y.toFixed(3) }; };
  const isUi = t => (ui && ui.contains(t)) || (t.closest && t.closest('a,button,input,label,select,textarea'));
  hero.addEventListener('pointerdown', e => {
    if (!state.arrange || isUi(e.target)) return;
    const k = pick(e);
    select(k);
    if (!k) return;
    e.preventDefault();
    const o = MOV[k].obj;
    if (ray.ray.intersectPlane(floorPlane, hitP)) mdrag = { k, dx: o.position.x - hitP.x, dz: o.position.z - hitP.z, id: e.pointerId };
    try { hero.setPointerCapture(e.pointerId); } catch (er) { /* egal */ }
  });
  hero.addEventListener('pointermove', e => {
    if (!state.arrange) return;
    if (!mdrag) { if (e.pointerType === 'mouse' && !isUi(e.target)) canvas.style.cursor = pick(e) ? 'grab' : 'default'; return; }
    aim(e);
    if (!ray.ray.intersectPlane(floorPlane, hitP)) return;
    const [x, z] = clampPos(mdrag.k, hitP.x + mdrag.dx, hitP.z + mdrag.dz);
    const o = MOV[mdrag.k].obj; o.position.x = x; o.position.z = z;
    canvas.style.cursor = 'grabbing';
    store(mdrag.k); ringTo(); kick();
  });
  const endM = e => { if (mdrag) { mdrag = null; canvas.style.cursor = 'grab'; updateParts(); try { hero.releasePointerCapture(e.pointerId); } catch (er) { /* egal */ } } };
  hero.addEventListener('pointerup', endM);
  hero.addEventListener('pointercancel', endM);
  function rotateSel(step = Math.PI / 4) {
    if (!sel) return;
    MOV[sel].obj.rotation.y += step; store(sel); kick();
  }
  function setArrange(on) {
    state.arrange = on;
    hero.classList.toggle('mb-arranging', on);
    $$('.mb-chip[data-arrange]').forEach(b => b.setAttribute('aria-pressed', String(on)));
    $$('.mb-arr-tools').forEach(t => { t.hidden = !on; });
    canvas.style.touchAction = on ? 'none' : '';
    if (on) { setView('standard'); tPitch = Math.max(cfg().pitch, 0.42); lastMove = performance.now() + 1e9; }
    else { select(null); canvas.style.cursor = ''; tPitch = cfg().pitch; lastMove = performance.now(); }
    resize();
  }
  hero.addEventListener('keydown', e => {
    if (!state.arrange || !sel) return;
    if (e.key === 'r' || e.key === 'R') rotateSel();
    if (e.key === 'Escape') select(null);
  });

  /* ── Stückliste ────────────────────────────────── */
  const dm = v => String(Math.round(v * 10) / 10).replace('.', ',');
  function parts() {
    const t = state.type, L = [`Standfläche ${PW} × ${PD} m (${PW * PD} m²), ${TYPES[t].name} – ${TYPES[t].open}`];
    if (t !== 'insel') L.push(`Rückwand (Pop-up, gebogen), ca. ${dm(WW * wall.scale.x)} × 2,5 m, bedruckt`);
    const sides = t === 'reihe' ? 2 : t === 'eck' ? 1 : 0;
    if (sides) L.push(`${sides === 2 ? '2 Seitenwände' : '1 Seitenwand'}, je ca. ${dm(SD * leftWall.scale.x)} × 2,5 m, bedruckt`);
    if (t === 'insel' && !state.extras.truss) L.push('Hängebanner rund, Ø ca. 2,7 m');
    L.push('Theke rund mit Druck und Ablage');
    if (state.extras.screen) L.push('LED-Stele (Bildschirm im Hochformat)');
    if (state.extras.truss) L.push(`Lichttraverse ca. ${dm(TX * 2)} × ${dm(TZ * 2)} m mit 4 Strahlern`);
    if (state.extras.seating) L.push('Sitzecke: 1 Tisch, 2 Stühle');
    if (state.extras.rollups) L.push('2 Roll-ups, 85 × 200 cm');
    if (state.extras.flag) L.push('Beachflag, ca. 3 m');
    if (state.extras.plants) L.push('2 Pflanzen');
    if (Object.keys(state.pos).length) L.push('Möbel individuell angeordnet');
    return L;
  }
  function updateParts() {
    const ul = $('.mb-parts ul'); if (!ul) return;
    ul.textContent = '';
    parts().forEach(x => { const li = document.createElement('li'); li.textContent = x; ul.appendChild(li); });
  }

  /* ── Entwurf als Link (ohne Logo – das bleibt im Browser) ── */
  const XK = Object.keys(EXTRAS);
  function encodeState() {
    const q = new URLSearchParams({ t: state.type, c: state.color.slice(1), w: PW, d: PD, e: XK.map(k => state.extras[k] ? 1 : 0).join('') });
    if (state.name) q.set('n', state.name);
    const ps = Object.entries(state.pos).map(([k, v]) => `${k}:${v.x}:${v.z}:${v.r}`).join(';');
    if (ps) q.set('p', ps);
    return '#stand=' + encodeURIComponent(q.toString());
  }
  function decodeState() {
    const h = location.hash;
    if (!h.startsWith('#stand=')) return false;
    let q; try { q = new URLSearchParams(decodeURIComponent(h.slice(7))); } catch (e) { return false; }
    if (TYPES[q.get('t')]) state.type = q.get('t');
    const c = q.get('c'); if (/^[0-9a-f]{6}$/i.test(c || '')) { state.color = '#' + c.toLowerCase(); state.colorName = 'Eigene Farbe'; }
    if (WIDTHS.includes(+q.get('w'))) state.w = +q.get('w');
    if (DEPTHS.includes(+q.get('d'))) state.d = +q.get('d');
    const e = q.get('e'); if (/^[01]+$/.test(e || '')) XK.forEach((k, i) => { state.extras[k] = e[i] === '1'; });
    if (q.get('n')) state.name = q.get('n').slice(0, 28);
    (q.get('p') || '').split(';').forEach(x => {
      const [k, a, b, r] = x.split(':');
      if (MOV[k] && [a, b, r].every(v => isFinite(+v))) state.pos[k] = { x: +a, z: +b, r: +r };
    });
    return true;
  }
  const linkUrl = () => location.origin + location.pathname + encodeState();
  async function share() {
    const url = linkUrl();
    try { history.replaceState(null, '', encodeState()); } catch (e) { /* egal */ }
    if (navigator.share && small.matches) {
      try { await navigator.share({ title: 'Mein Messestand-Entwurf', text: 'Mein 3D-Entwurf für den Messestand', url }); return; } catch (e) { if (e && e.name === 'AbortError') return; }
    }
    try { await navigator.clipboard.writeText(url); say('✓ Link kopiert – damit öffnet sich genau dieser Entwurf (ohne Logo).'); }
    catch (e) { say('Link: ' + url); }
    setTimeout(() => say(''), 6000);
  }

  /* ── 360°-Video ────────────────────────────────── */
  async function recordVideo(btn) {
    if (recording) return;
    if (!canvas.captureStream || typeof MediaRecorder === 'undefined') { say('Ihr Browser kann leider kein Video aufnehmen – bitte „Entwurf speichern“ nutzen.'); return; }
    const mime = ['video/mp4;codecs=avc1', 'video/mp4', 'video/webm;codecs=vp9', 'video/webm;codecs=vp8', 'video/webm'].find(t => MediaRecorder.isTypeSupported(t)) || '';
    let rec;
    try { rec = new MediaRecorder(canvas.captureStream(30), mime ? { mimeType: mime, videoBitsPerSecond: 8000000 } : undefined); }
    catch (e) { say('Die Aufnahme konnte nicht gestartet werden.'); return; }
    const chunks = [];
    rec.ondataavailable = ev => { if (ev.data && ev.data.size) chunks.push(ev.data); };
    const label = btn ? btn.textContent : '';
    if (btn) { btn.disabled = true; btn.textContent = 'Aufnahme läuft …'; }
    /* Stand mittig ins Bild, wie beim Entwurfsbild */
    camera.clearViewOffset();
    const w = stage.clientWidth, h = stage.clientHeight;
    dist = fit(w, h, 0.72, 0.8); camera.updateProjectionMatrix();
    const stopped = new Promise(res => { rec.onstop = res; });
    await new Promise(res => { recording = { t0: performance.now(), yaw0: yaw, dur: 8000, done: res }; rec.start(250); kick(); });
    rec.stop(); await stopped;
    recording = null; tYaw = yaw = cfg().yaw; tPitch = cfg().pitch;
    if (btn) { btn.disabled = false; btn.textContent = label; }
    resize();
    const type = (mime || 'video/webm').split(';')[0];
    const blob = new Blob(chunks, { type });
    if (!blob.size) { say('Die Aufnahme ist leer – bitte noch einmal versuchen.'); return; }
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `messestand-360-${state.type}.${type.includes('mp4') ? 'mp4' : 'webm'}`;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 8000);
    say('✓ Video gespeichert.'); setTimeout(() => say(''), 4000);
  }

  /* ── Bedienelemente ────────────────────────────── */
  const swatches = $$('.mb-sw button');
  const picker = $('.mb-pick input');
  function setColor(hex, name) {
    state.color = hex; state.colorName = name;
    swatches.forEach(o => o.setAttribute('aria-pressed', String(o.dataset.c === hex)));
    if (picker && picker.value !== hex) picker.value = hex;
    repaint();
  }
  swatches.forEach(b => b.addEventListener('click', () => setColor(b.dataset.c, b.title)));
  if (picker) picker.addEventListener('input', () => setColor(picker.value.toLowerCase(), 'Eigene Farbe'));

  $$('.mb-seg button').forEach(b => b.addEventListener('click', () => setType(b.dataset.type)));
  $$('.mb-chip[data-arrange]').forEach(b => b.addEventListener('click', () => setArrange(!state.arrange)));
  $$('.mb-share').forEach(b => b.addEventListener('click', share));
  $$('.mb-video').forEach(b => b.addEventListener('click', () => recordVideo(b)));
  $$('.mb-rot').forEach(b => b.addEventListener('click', () => rotateSel()));
  $$('.mb-reset').forEach(b => b.addEventListener('click', () => { state.pos = {}; placeMovables(); select(null); updateParts(); kick(); }));
  $$('.mb-dim button').forEach(b => b.addEventListener('click', () => {
    state[b.parentNode.dataset.k] = +b.dataset.v;
    layout(); repaint(); resize(); updateParts();
    if (PW * PD <= 16) { say('Tipp: Auf kleinen Ständen wirkt weniger Ausstattung großzügiger – unter „Ausstattung“ Elemente abwählen oder verschieben.'); setTimeout(() => say(''), 7000); }
  }));
  $$('.mb-view button').forEach(b => b.addEventListener('click', () => setView(b.dataset.view)));
  $$('.mb-chip[data-extra]').forEach(b => b.addEventListener('click', () => {
    const k = b.dataset.extra; state.extras[k] = !state.extras[k];
    applyVisibility(); resize();
  }));
  $$('.mb-chip[data-dims]').forEach(b => b.addEventListener('click', () => { state.dims = !state.dims; applyVisibility(); resize(); }));
  /* Reiter im Planer */
  const tabs = $$('.mb-tabs button');
  tabs.forEach(b => b.addEventListener('click', () => {
    tabs.forEach(o => { const on = o === b; o.setAttribute('aria-selected', String(on)); o.tabIndex = on ? 0 : -1; });
    $$('.mb-pane').forEach(p => { p.hidden = p.id !== b.getAttribute('aria-controls'); });
  }));
  tabs.forEach((b, i) => b.addEventListener('keydown', e => {
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
    const n = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length];
    n.click(); n.focus();
  }));
  document.querySelectorAll('[data-mb-type]').forEach(b => b.addEventListener('click', e => {
    e.preventDefault();
    setType(b.dataset.mbType);
    hero.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth' });
  }));

  const nameIn = $('.mb-name');
  if (nameIn) nameIn.addEventListener('input', () => { state.name = nameIn.value.trim().slice(0, 28); repaint(); });

  const fileIn = $('.mb-file input');
  const clearBtn = $('.mb-x');
  const msg = $('.mb-msg');
  const say = t => { if (msg) { msg.textContent = t; msg.hidden = !t; } };
  if (fileIn) fileIn.addEventListener('change', () => {
    const f = fileIn.files && fileIn.files[0];
    if (!f) return;
    const isImg = /^image\//.test(f.type) || /\.(png|jpe?g|webp|svg|gif|heic|heif)$/i.test(f.name || '');
    if (!isImg || f.size > 8 * 1024 * 1024) {
      say('Bitte ein Logo als PNG, JPG, WebP oder SVG (max. 8 MB) wählen.');
      return;
    }
    const rd = new FileReader();
    rd.onload = () => {
      const img = new Image();
      img.onload = () => {
        if (!img.width || !img.height) { img.width = 600; img.height = 300; }
        state.logo = img;
        if (clearBtn) clearBtn.hidden = false;
        say('✓ Logo ist jetzt auf dem Stand.');
        setTimeout(() => say(''), 3500);
        repaint();
      };
      img.onerror = () => say('Dieses Dateiformat kann Ihr Browser nicht anzeigen. Bitte das Logo als PNG oder JPG wählen.');
      img.src = rd.result;
    };
    rd.readAsDataURL(f);
  });
  if (clearBtn) clearBtn.addEventListener('click', () => {
    state.logo = null; clearBtn.hidden = true;
    if (fileIn) fileIn.value = '';
    repaint();
  });

  const saveBtn = $('.mb-save');
  if (saveBtn) saveBtn.addEventListener('click', async () => {
    const blob = await safeSnap();
    if (!blob) { say('Das Bild konnte nicht erstellt werden.'); return; }
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `messestand-entwurf-${state.type}.jpg`;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 4000);
  });

  const goBtn = $('.mb-go');
  if (goBtn) goBtn.addEventListener('click', async () => {
    const box = document.getElementById('kontakt');
    const form = document.querySelector('#kontakt form');
    if (box) box.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth' });
    if (!form) return;
    const ta = form.querySelector('#cf-nachricht');
    let attached = false;
    try {
      const sel = form.querySelector('#cf-produkt');
      if (sel && !sel.value) {
        const opt = [...sel.options].find(o => /komplett/i.test(o.textContent));
        if (opt) sel.value = opt.value || opt.textContent;
      }
      const fi = form.querySelector('input[type="file"][name="attachment"]');
      const blob = await safeSnap();
      if (fi && blob && typeof DataTransfer !== 'undefined') {
        try {
          const dt = new DataTransfer();
          dt.items.add(new File([blob], `messestand-entwurf-${state.type}.jpg`, { type: 'image/jpeg' }));
          fi.files = dt.files;
          attached = fi.files.length === 1;
        } catch (e) { attached = false; }
      }
    } catch (e) { /* Formular trotzdem ausfüllen */ }
    const lines = [
      'Meine Auswahl im 3D-Planer:',
      `• Standtyp: ${TYPES[state.type].name} (${TYPES[state.type].open})`,
      `• Standgröße: ${PW} × ${PD} m (${PW * PD} m²)`,
      `• Standfarbe: ${state.colorName} (${state.color})`,
      `• Ausstattung: ${extrasText()}`,
      ...parts().slice(1).map(x => `   – ${x}`),
    ];
    if (state.name) lines.push(`• Firmenname auf dem Stand: ${state.name}`);
    lines.push(state.logo ? '• Eigenes Logo im Entwurf verwendet' : '• Logo: folgt');
    if (attached) lines.push('• Entwurfsbild ist angehängt');
    lines.push(`• Link zum Entwurf: ${linkUrl()}`);
    lines.push('', 'Messe / Termin: ');
    if (ta) {
      const rest = ta.value.replace(/^Meine Auswahl im 3D-Planer:[\s\S]*?Messe \/ Termin(?: \/ Standgröße \(m²\))?: ?/, '');
      ta.value = lines.join('\n') + rest;
    }
    let hid = form.querySelector('input[name="art"]');
    if (!hid) { hid = document.createElement('input'); hid.type = 'hidden'; hid.name = 'art'; form.appendChild(hid); }
    hid.value = `3D-Planer: ${TYPES[state.type].name} ${PW}×${PD} m, ${state.colorName} ${state.color}`;
    let note = document.querySelector('.mb-sent');
    if (!note) {
      note = document.createElement('div');
      note.className = 'mb-sent';
      note.setAttribute('role', 'status');
      form.parentNode.insertBefore(note, form);
    }
    note.textContent = attached
      ? '✓ Ihr 3D-Entwurf ist übernommen und als Bild angehängt. Ergänzen Sie nur noch Ihre Kontaktdaten sowie Messe, Termin und Standgröße.'
      : '✓ Ihre Auswahl aus dem 3D-Planer steht in der Nachricht. Ergänzen Sie nur noch Ihre Kontaktdaten sowie Messe, Termin und Standgröße.';
    setTimeout(() => { if (ta) { ta.focus({ preventScroll: true }); ta.setSelectionRange(ta.value.length, ta.value.length); } }, reduced ? 0 : 700);
  });

  hero.mbSnapshot = snapshot;
  hero.mbScreenOf = k => { const v = new THREE.Vector3(); MOV[k].obj.getWorldPosition(v); v.y += 0.6; v.project(camera); const r = canvas.getBoundingClientRect(); return [r.left + (v.x + 1) / 2 * r.width, r.top + (1 - v.y) / 2 * r.height]; };
  hero.mbState = () => ({ type: state.type, w: PW, d: PD, pos: state.pos, sel, arrange: state.arrange, view: state.view, link: encodeState(), parts: parts() });
  hero.mbDebug = () => ({ post: !!composer, gtao: !!(gtao && gtao.enabled && composer), perfLevel });
  const fromLink = decodeState();
  if (fromLink) {
    if (nameIn) nameIn.value = state.name;
    if (picker) picker.value = state.color;
    swatches.forEach(o => o.setAttribute('aria-pressed', String(o.dataset.c === state.color)));
  }
  layout();
  repaint();
  setType(state.type);
  applyVisibility();
  updateParts();
  kick();
}
