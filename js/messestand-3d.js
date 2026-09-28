/* 3D-Messestand-Planer für /messebau-berlin.html
   – vier Standtypen (Reihe, Ecke, Kopf, Insel), Standfarbe, eigenes Logo & Firmenname
   – Maus bewegt die Kamera (Desktop), seitlich wischen dreht den Stand (Touch)
   – "Entwurf speichern" lädt ein Bild herunter, "Diesen Stand anfragen" füllt das Formular
   – das Logo wird nur im Browser verarbeitet und erst mit der Anfrage (als Entwurfsbild) gesendet
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
      Promise.all([document.fonts.load('900 64px "Barlow Condensed"'), document.fonts.load('500 32px "Barlow"')]),
      new Promise(r => setTimeout(r, 2500)),
    ]);
  } catch (e) { /* Schrift-Fallback reicht */ }

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
  const PR = Math.min(window.devicePixelRatio || 1, small.matches ? 1.5 : 1.75);
  renderer.setPixelRatio(PR);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.0;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  const aniso = renderer.capabilities.getMaxAnisotropy();

  const scene = new THREE.Scene();
  /* Studio-Umgebung für realistische Reflexionen auf Metall, Theke und Folien */
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environmentIntensity = 0.55;
  pmrem.dispose();
  const camera = new THREE.PerspectiveCamera(30, 1, 0.1, 100);

  /* Standgrafik als Canvas-Texturen */
  const tex = {};
  const makeTex = (key, w, h, wrap = false) => {
    const c = document.createElement('canvas');
    c.width = w; c.height = h;
    const t = new THREE.CanvasTexture(c);
    t.colorSpace = THREE.SRGBColorSpace;
    t.anisotropy = aniso;
    if (wrap) t.wrapS = THREE.RepeatWrapping;
    tex[key] = { c, t, ctx: c.getContext('2d') };
    return t;
  };
  makeTex('wall', 2048, 1112);
  makeTex('side', 1312, 1112);
  makeTex('counter', 2048, 480);
  makeTex('rollupA', 512, 1206);
  makeTex('rollupB', 512, 1206);
  makeTex('flag', 512, 1664);
  makeTex('ring', 2048, 256, true);

  const mat = (o) => new THREE.MeshStandardMaterial(o);
  const white = mat({ color: 0xf4f6f8, roughness: 0.3 });
  const dark = mat({ color: 0x1b2433, roughness: 0.5, metalness: 0.3 });
  const metal = mat({ color: 0xd4d8de, roughness: 0.22, metalness: 0.9 });
  const wood = mat({ color: 0xb98a5a, roughness: 0.6 });
  const accentDark = mat({ color: 0x1b2a3d, roughness: 0.45 });
  const print = (t, extra = {}) => mat({ map: t, roughness: 0.5, ...extra });

  const shadowed = (m, cast = true, receive = true) => { m.castShadow = cast; m.receiveShadow = receive; return m; };
  const booth = new THREE.Group();
  scene.add(booth);
  const FLOOR = 0.12;
  const add = (parent, m, x = 0, y = 0, z = 0) => { m.position.set(x, y, z); parent.add(m); return m; };

  /* Podest mit Lichtkante */
  const carpet = mat({ color: 0x4b515b, roughness: 1 });
  add(booth, shadowed(new THREE.Mesh(new THREE.BoxGeometry(6.6, FLOOR, 4.4), [metal, metal, carpet, dark, metal, metal]), false, true), 0, FLOOR / 2, 0);
  const led = new THREE.MeshBasicMaterial({ color: 0xfff1d0 });
  [[6.62, 0.028, 0.028, 0, FLOOR - 0.02, 2.2], [0.028, 0.028, 4.42, -3.3, FLOOR - 0.02, 0], [0.028, 0.028, 4.42, 3.3, FLOOR - 0.02, 0]]
    .forEach(([w, h, d, x, y, z]) => add(booth, new THREE.Mesh(new THREE.BoxGeometry(w, h, d), led), x, y, z));

  /* Lichtschein auf dem Boden + Schatten */
  const gc = document.createElement('canvas'); gc.width = gc.height = 256;
  const gx = gc.getContext('2d');
  const rg = gx.createRadialGradient(128, 128, 20, 128, 128, 128);
  rg.addColorStop(0, 'rgba(255,240,210,.55)'); rg.addColorStop(1, 'rgba(255,240,210,0)');
  gx.fillStyle = rg; gx.fillRect(0, 0, 256, 256);
  const glow = new THREE.Mesh(new THREE.PlaneGeometry(10, 7.5), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(gc), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, opacity: 0.55 }));
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
  const WW = 4.8, WH = 2.55, SAG = 0.55, WZ = -1.6;
  const backRig = new THREE.Group();
  booth.add(backRig);
  const wg = new THREE.PlaneGeometry(WW, WH, 60, 1);
  const wp = wg.attributes.position;
  for (let i = 0; i < wp.count; i++) { const x = wp.getX(i); wp.setZ(i, SAG * (x / (WW / 2)) ** 2); }
  wg.computeVertexNormals();
  const wall = new THREE.Group();
  wall.position.set(0, FLOOR + WH / 2, WZ);
  wall.add(shadowed(new THREE.Mesh(wg, print(tex.wall.t, { roughness: 0.55 }))));
  wall.add(new THREE.Mesh(wg, mat({ color: 0x222c3a, roughness: 0.7, side: THREE.BackSide })));
  const slope = Math.atan(2 * SAG / (WW / 2));
  [-1, 1].forEach(sd => {
    const cap = add(wall, shadowed(new THREE.Mesh(new THREE.BoxGeometry(0.09, WH + 0.02, 0.34), accentDark)), sd * (WW / 2 + 0.03), 0, SAG - 0.1);
    cap.rotation.y = -sd * slope;
  });
  backRig.add(wall);
  const lensMat = new THREE.MeshBasicMaterial({ color: 0xfff6e0 });
  [-1.5, 0, 1.5].forEach(x => {
    const zTop = WZ + SAG * (x / (WW / 2)) ** 2;
    const y = FLOOR + WH;
    add(backRig, new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.03, 0.38), dark), x, y + 0.05, zTop + 0.17);
    const head = add(backRig, new THREE.Group(), x, y + 0.06, zTop + 0.38);
    head.rotation.x = 2.3;
    head.add(new THREE.Mesh(new THREE.CylinderGeometry(0.055, 0.08, 0.17, 20), dark));
    const lens = add(head, new THREE.Mesh(new THREE.CircleGeometry(0.07, 20), lensMat), 0, -0.086, 0);
    lens.rotation.x = Math.PI / 2;
    const sp = new THREE.SpotLight(0xfff1dc, 22, 0, 0.6, 0.65, 2);
    sp.position.set(x, y + 0.02, zTop + 0.4);
    sp.target.position.set(x, FLOOR + 1.35, zTop);
    backRig.add(sp, sp.target);
  });

  /* Seitenwände (Reihen- und Eckstand) */
  const SD = 3.0;
  function sideWall(sd) {
    const g = new THREE.Group();
    g.position.set(sd * 3.2, FLOOR + WH / 2, -0.6);
    g.rotation.y = -sd * Math.PI / 2;
    const pg = new THREE.PlaneGeometry(SD, WH);
    const face = shadowed(new THREE.Mesh(pg, print(tex.side.t, { roughness: 0.55 })));
    g.add(face);
    g.add(new THREE.Mesh(pg, mat({ color: 0x222c3a, roughness: 0.7, side: THREE.BackSide })));
    add(g, shadowed(new THREE.Mesh(new THREE.BoxGeometry(SD + 0.04, 0.05, 0.08), accentDark)), 0, WH / 2 + 0.02, 0);
    add(g, shadowed(new THREE.Mesh(new THREE.BoxGeometry(0.08, WH + 0.04, 0.1), accentDark)), sd * (SD / 2), 0, 0);
    booth.add(g);
    return g;
  }
  const leftWall = sideWall(-1);
  const rightWall = sideWall(1);

  /* Hängebanner (Inselstand) */
  const ringRig = new THREE.Group();
  ringRig.position.set(0.1, FLOOR + 3.55, 0.1);
  const rg2 = new THREE.CylinderGeometry(1.35, 1.35, 0.72, 96, 1, true);
  tex.ring.t.repeat.x = 1;
  ringRig.add(shadowed(new THREE.Mesh(rg2, print(tex.ring.t, { roughness: 0.55 })), true, false));
  ringRig.add(new THREE.Mesh(rg2, mat({ color: 0xe8ecf0, roughness: 0.8, side: THREE.BackSide })));
  [0, 1, 2, 3].forEach(i => {
    const a = i * Math.PI / 2 + Math.PI / 4;
    add(ringRig, new THREE.Mesh(new THREE.CylinderGeometry(0.004, 0.004, 3, 4), metal), Math.cos(a) * 1.3, 1.85, Math.sin(a) * 1.3);
  });
  booth.add(ringRig);

  /* Theke */
  const counter = add(booth, new THREE.Group(), 0.25, FLOOR, 0.45);
  const sx = 1.35, sz = 0.72;
  const cBody = add(counter, shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.62, 0.62, 0.98, 72, 1, true, Math.PI, Math.PI * 2), print(tex.counter.t, { roughness: 0.4 }))), 0, 0.53, 0);
  cBody.scale.set(sx, 1, sz);
  const cTop = add(counter, shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.67, 0.67, 0.05, 72), mat({ color: 0x20252d, roughness: 0.18, metalness: 0.4 }))), 0, 1.045, 0);
  cTop.scale.set(sx, 1, sz);
  const cBase = add(counter, shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.6, 0.6, 0.05, 72), dark)), 0, 0.025, 0);
  cBase.scale.set(sx, 1, sz);
  add(counter, shadowed(new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.035, 0.2), white)), -0.05, 1.088, 0.05).rotation.y = 0.2;
  const holder = add(counter, new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.26, 0.07), new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: 0.04, transparent: true, opacity: 0.3 })), 0.48, 1.2, 0.02);
  holder.rotation.set(-0.12, -0.3, 0);
  const flyer = add(counter, new THREE.Mesh(new THREE.PlaneGeometry(0.17, 0.24), print(tex.rollupA.t)), 0.48, 1.2, 0.03);
  flyer.rotation.set(-0.12, -0.3, 0);

  /* Roll-ups */
  function rollup(t, x, z, ry) {
    const g = add(booth, new THREE.Group(), x, FLOOR, z);
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
  rollup(tex.rollupA.t, -2.78, 0.35, 0.32);
  rollup(tex.rollupB.t, 2.9, -0.45, -0.45);

  /* Beachflag (Feder-Form, weht leicht) */
  const flag = add(booth, new THREE.Group(), 2.5, FLOOR, 1.45);
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

  /* Tisch und Stühle */
  const table = add(booth, new THREE.Group(), 1.45, FLOOR, -0.55);
  add(table, shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.38, 0.03, 40), white)), 0, 0.74, 0);
  add(table, shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.72, 12), metal)), 0, 0.37, 0);
  add(table, shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.25, 0.025, 32), metal)), 0, 0.012, 0);
  function chair(x, z, ry) {
    const g = add(booth, new THREE.Group(), x, FLOOR, z); g.rotation.y = ry;
    add(g, shadowed(new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.05, 0.42), white)), 0, 0.46, 0);
    add(g, shadowed(new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.36, 0.04), white)), 0, 0.68, -0.2).rotation.x = -0.12;
    [[-1, -1], [1, -1], [-1, 1], [1, 1]].forEach(([a, b]) => {
      const l = add(g, shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.012, 0.47, 8), wood)), a * 0.16, 0.225, b * 0.16);
      l.rotation.set(b * 0.08, 0, -a * 0.08);
    });
  }
  chair(1.0, -0.35, 1.2);
  chair(1.9, -0.3, -1.25);

  /* Pflanzen */
  const leafGeo = new THREE.SphereGeometry(1, 12, 8);
  const greens = [0x2f7d3b, 0x3d9447, 0x28692f, 0x4aa653].map(c => mat({ color: c, roughness: 0.55 }));
  const potMat = mat({ color: 0xf5f5f2, roughness: 0.2 });
  function plant(x, y, z, s) {
    const g = add(booth, new THREE.Group(), x, y, z); g.scale.setScalar(s);
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
  }
  plant(-1.95, FLOOR, -0.85, 1.25);
  plant(-0.45, FLOOR + 1.07, 0.45, 0.42);

  /* ── Grafik neu zeichnen ───────────────────────── */
  function repaint() {
    const C = state.color;
    for (const k in tex) {
      const { c, ctx, t } = tex[k];
      ctx.clearRect(0, 0, c.width, c.height);
      PAINT[k](ctx, c.width, c.height, C);
      t.needsUpdate = true;
    }
    accentDark.color.set(mix(C, NAVY, 0.8));
    hero.style.setProperty('--mb-accent', C);
    kick();
  }

  /* ── Standtyp ──────────────────────────────────── */
  function setType(t) {
    if (!TYPES[t]) return;
    state.type = t;
    backRig.visible = t !== 'insel';
    leftWall.visible = t === 'reihe' || t === 'eck';
    rightWall.visible = t === 'reihe';
    ringRig.visible = t === 'insel';
    $$('.mb-seg button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.type === t)));
    const lbl = $('.mb-type-lbl');
    if (lbl) lbl.textContent = `${TYPES[t].name} · ${TYPES[t].open}`;
    tYaw = TYPES[t].yaw; tPitch = TYPES[t].pitch;
    lastMove = performance.now();
    resize();
  }

  /* ── Kamera & Eingabe ──────────────────────────── */
  const T = new THREE.Vector3(0, 1.2, 0);
  let yaw = TYPES.kopf.yaw, pitch = TYPES.kopf.pitch, tYaw = yaw, tPitch = pitch, dist = 14, lastMove = -1e9;
  const cfg = () => TYPES[state.type];

  let drag = null;
  canvas.addEventListener('pointerdown', e => {
    if (e.pointerType === 'mouse') return;
    drag = { x: e.clientX, yaw: tYaw };
  }, { passive: true });
  canvas.addEventListener('pointermove', e => {
    if (!drag) return;
    const dx = (e.clientX - drag.x) / Math.max(stage.clientWidth, 1);
    tYaw = THREE.MathUtils.clamp(drag.yaw + dx * 2.6, cfg().yaw - 0.9, cfg().yaw + 0.9);
    lastMove = performance.now() + 2000;
    kick();
  }, { passive: true });
  const endDrag = () => { drag = null; };
  canvas.addEventListener('pointerup', endDrag);
  canvas.addEventListener('pointercancel', endDrag);
  if (!reduced) {
    hero.addEventListener('pointermove', e => {
      if (e.pointerType !== 'mouse' || small.matches) return;
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
    const halfH = state.type === 'insel' ? 2.25 : 1.75;
    T.y = state.type === 'insel' ? 1.75 : 1.2;
    return Math.max(3.55 / (vt * (w / h) * fracW), halfH / (vt * fracH), 8);
  }
  function resize() {
    const w = stage.clientWidth, h = stage.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
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

  /* ── Render-Schleife (nur wenn sichtbar) ───────── */
  let visible = true, running = false, first = true;
  new IntersectionObserver(([en]) => { visible = en.isIntersecting; kick(); }).observe(hero);
  document.addEventListener('visibilitychange', kick);
  const clock = new THREE.Clock();
  function kick() { if (!running && visible && !document.hidden) { running = true; clock.getDelta(); requestAnimationFrame(frame); } }

  function frame() {
    const dt = Math.min(clock.getDelta(), 0.05);
    const t = clock.elapsedTime;
    if (!reduced && performance.now() - lastMove > 2500) {
      tYaw = cfg().yaw + Math.sin(t * 0.22) * cfg().range * 0.55;
      tPitch = cfg().pitch + Math.sin(t * 0.17) * 0.03;
    }
    const k = 1 - Math.exp(-dt * 3.2);
    yaw += (tYaw - yaw) * k; pitch += (tPitch - pitch) * k;
    place();

    if (!reduced) {
      for (let i = 0; i < fp.count; i++) {
        const x = base[i * 3], y = base[i * 3 + 1];
        const u = x / 0.74;
        fp.setZ(i, Math.sin(t * 2.1 + y * 2.2 + u * 2.5) * 0.045 * u);
      }
      fp.needsUpdate = true;
      fg.computeVertexNormals();
      if (ringRig.visible) ringRig.rotation.y = t * 0.12;
    }

    renderer.render(scene, camera);
    if (first) { first = false; hero.classList.add('mb-3d'); document.documentElement.classList.add('mb-ready'); if (ui) ui.hidden = false; }
    const moving = !reduced || Math.abs(tYaw - yaw) > 1e-3 || Math.abs(tPitch - pitch) > 1e-3;
    if (moving && visible && !document.hidden) requestAnimationFrame(frame);
    else running = false;
  }

  /* ── Entwurf als Bild ──────────────────────────── */
  function snapshot(W = 1600, H = 1000) {
    const out = document.createElement('canvas');
    out.width = W; out.height = H;
    const o = out.getContext('2d');
    const bg = o.createLinearGradient(0, 0, W, H);
    bg.addColorStop(0, '#0b1f38'); bg.addColorStop(0.6, NAVY); bg.addColorStop(1, '#0d4a4a');
    o.fillStyle = bg; o.fillRect(0, 0, W, H);
    const SH = H - Math.round(H * 0.11);
    renderer.setPixelRatio(1);
    renderer.setSize(W, SH, false);
    camera.clearViewOffset();
    camera.aspect = W / SH;
    const d0 = dist;
    dist = fit(W, SH, 0.7, 0.78);
    place();
    camera.updateProjectionMatrix();
    renderer.render(scene, camera);
    o.drawImage(renderer.domElement, 0, 0, W, SH);
    dist = d0;
    renderer.setPixelRatio(PR);
    resize();
    place();
    renderer.render(scene, camera);
    const FH = H - SH, Y1 = SH + FH * 0.38, Y2 = SH + FH * 0.74, P1 = Math.round(FH * 0.3), P2 = Math.round(FH * 0.2), M = Math.round(W * 0.03);
    o.fillStyle = 'rgba(0,0,0,.35)'; o.fillRect(0, SH, W, H - SH);
    o.fillStyle = state.color; o.fillRect(0, SH, W, 4);
    text(o, `3D-ENTWURF · ${TYPES[state.type].name.toUpperCase()} · ${TYPES[state.type].open.toUpperCase()}`, M, Y1, P1, '#ffffff', { align: 'left' });
    text(o, `Standfarbe: ${state.colorName} (${state.color})${state.name ? ' · ' + state.name : ''}`, M, Y2, P2, 'rgba(255,255,255,.75)', { weight: 500, family: '"Barlow"', align: 'left', maxW: W * 0.55 });
    text(o, 'MASAR WERBEAGENTUR · MESSEBAU BERLIN', W - M, Y1, Math.round(P1 * 0.88), state.color, { align: 'right' });
    text(o, 'masar-werbeagentur.de · Unverbindliche Visualisierung', W - M, Y2, Math.round(P2 * 0.92), 'rgba(255,255,255,.7)', { weight: 500, family: '"Barlow"', align: 'right' });
    return new Promise(res => { try { out.toBlob(b => res(b), 'image/jpeg', 0.9); } catch (e) { res(null); } });
  }

  const safeSnap = () => Promise.race([
    Promise.resolve().then(snapshot).catch(() => null),
    new Promise(r => setTimeout(() => r(null), 5000)),
  ]);

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
      `• Standfarbe: ${state.colorName} (${state.color})`,
    ];
    if (state.name) lines.push(`• Firmenname auf dem Stand: ${state.name}`);
    lines.push(state.logo ? '• Eigenes Logo im Entwurf verwendet' : '• Logo: folgt');
    if (attached) lines.push('• Entwurfsbild ist angehängt');
    lines.push('', 'Messe / Termin / Standgröße (m²): ');
    if (ta) {
      const rest = ta.value.replace(/^Meine Auswahl im 3D-Planer:[\s\S]*?Messe \/ Termin \/ Standgröße \(m²\): ?/, '');
      ta.value = lines.join('\n') + rest;
    }
    let hid = form.querySelector('input[name="art"]');
    if (!hid) { hid = document.createElement('input'); hid.type = 'hidden'; hid.name = 'art'; form.appendChild(hid); }
    hid.value = `3D-Planer: ${TYPES[state.type].name}, ${state.colorName} ${state.color}`;
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
  repaint();
  setType('kopf');
  kick();
}
