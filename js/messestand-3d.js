/* Interaktiver 3D-Messestand für /messebau-berlin.html
   – wird nur auf Desktop mit WebGL geladen (siehe Seite)
   – Maus bewegt die Kamera, fünf Standfarben zum Ausprobieren
   – bei "prefers-reduced-motion" bleibt die Ansicht ruhig */
import * as THREE from './three.module.min.js';

const NAVY = '#132e50';
const INK = '#0f2440';

/* ── Farbhilfen ─────────────────────────────────────── */
const rgb = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
const mix = (a, b, t) => {
  const A = rgb(a), B = rgb(b);
  return `rgb(${A.map((v, i) => Math.round(v + (B[i] - v) * t)).join(',')})`;
};

/* ── Grafik-Bausteine für die Standgrafik ───────────── */
function logo(ctx, cx, cy, s, C) {
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

function text(ctx, str, x, y, px, color, { weight = 900, family = '"Barlow Condensed"', align = 'center', spacing = 0 } = {}) {
  ctx.font = `${weight} ${px}px ${family}, "Arial Narrow", sans-serif`;
  ctx.fillStyle = color;
  ctx.textAlign = align;
  ctx.textBaseline = 'middle';
  if ('letterSpacing' in ctx) ctx.letterSpacing = spacing + 'px';
  ctx.fillText(str, x, y);
  if ('letterSpacing' in ctx) ctx.letterSpacing = '0px';
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
    logo(ctx, w / 2, h * 0.2, h * 0.18, C);
    text(ctx, 'IHR LOGO', w / 2, h * 0.39, h * 0.11, NAVY);
    text(ctx, 'IHRE MARKE. ÜBERALL SICHTBAR.', w / 2, h * 0.49, h * 0.042, mix(NAVY, '#ffffff', 0.15), { weight: 500, family: '"Barlow"', spacing: h * 0.012 });
  },
  counter(ctx, w, h, C) {
    paper(ctx, w, h);
    shards(ctx, w * 0.22, h * 0.05, w * 0.2, h * 0.95, C);
    shards(ctx, w * 0.58, h * 0.05, w * 0.2, h * 0.95, C, true);
    ctx.fillStyle = mix(C, NAVY, 0.7);
    ctx.fillRect(0, h * 0.94, w, h * 0.06);
    logo(ctx, w / 2, h * 0.36, h * 0.24, C);
    text(ctx, 'IHR LOGO', w / 2, h * 0.68, h * 0.15, NAVY);
  },
  rollupA(ctx, w, h, C) {
    paper(ctx, w, h);
    logo(ctx, w / 2, h * 0.1, w * 0.2, C);
    text(ctx, 'IHR LOGO', w / 2, h * 0.19, w * 0.12, NAVY);
    ['STARKE', 'MARKEN.', 'STARKE', 'AUFTRITTE.'].forEach((t, i) =>
      text(ctx, t, w * 0.14, h * (0.3 + i * 0.055), w * 0.1, NAVY, { align: 'left' }));
    shards(ctx, 0, h * 0.56, w, h * 0.44, C);
  },
  rollupB(ctx, w, h, C) {
    paper(ctx, w, h);
    logo(ctx, w / 2, h * 0.1, w * 0.2, C);
    text(ctx, 'IHR LOGO', w / 2, h * 0.19, w * 0.12, NAVY);
    ['LÖSUNGEN', 'FÜR STARKE', 'MARKEN.'].forEach((t, i) =>
      text(ctx, t, w / 2, h * (0.31 + i * 0.055), w * 0.1, NAVY));
    shards(ctx, 0, h * 0.54, w, h * 0.46, C, true);
  },
  flag(ctx, w, h, C) {
    paper(ctx, w, h);
    logo(ctx, w * 0.5, h * 0.2, w * 0.2, C);
    text(ctx, 'IHR LOGO', w * 0.5, h * 0.28, w * 0.13, NAVY);
    ['IDEEN', 'SICHTBAR', 'MACHEN'].forEach((t, i) =>
      text(ctx, t, w * 0.2, h * (0.38 + i * 0.045), w * 0.12, NAVY, { align: 'left' }));
    shards(ctx, 0, h * 0.58, w, h * 0.42, C, true);
  },
};

/* ── Szene ──────────────────────────────────────────── */
export async function init(hero) {
  const stage = hero.querySelector('.mb-stage');
  const canvas = stage.querySelector('canvas');
  const ui = hero.querySelector('.mb-ui');
  const swatches = [...hero.querySelectorAll('.mb-sw button')];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  try {
    await Promise.race([
      Promise.all([document.fonts.load('900 64px "Barlow Condensed"'), document.fonts.load('500 32px "Barlow"')]),
      new Promise(r => setTimeout(r, 2500)),
    ]);
  } catch (e) { /* Schrift-Fallback reicht */ }

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  const aniso = renderer.capabilities.getMaxAnisotropy();

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(30, 1, 0.1, 100);

  /* Standgrafik als Canvas-Texturen */
  const tex = {};
  const makeTex = (key, w, h) => {
    const c = document.createElement('canvas');
    c.width = w; c.height = h;
    const t = new THREE.CanvasTexture(c);
    t.colorSpace = THREE.SRGBColorSpace;
    t.anisotropy = aniso;
    tex[key] = { c, t, ctx: c.getContext('2d') };
    return t;
  };
  makeTex('wall', 2048, 1112);
  makeTex('counter', 2048, 480);
  makeTex('rollupA', 512, 1206);
  makeTex('rollupB', 512, 1206);
  makeTex('flag', 512, 1664);

  const mat = (o) => new THREE.MeshStandardMaterial(o);
  const white = mat({ color: 0xf4f6f8, roughness: 0.35 });
  const dark = mat({ color: 0x1b2433, roughness: 0.55, metalness: 0.2 });
  const metal = mat({ color: 0xc9ced6, roughness: 0.28, metalness: 0.75 });
  const wood = mat({ color: 0xb98a5a, roughness: 0.6 });
  const accentDark = mat({ color: 0x1b2a3d, roughness: 0.5 });

  const shadowed = (m, cast = true, receive = true) => { m.castShadow = cast; m.receiveShadow = receive; return m; };
  const booth = new THREE.Group();
  scene.add(booth);
  const FLOOR = 0.12;

  /* Podest mit Lichtkante */
  const carpet = mat({ color: 0x4b515b, roughness: 1 });
  booth.add(shadowed(new THREE.Mesh(new THREE.BoxGeometry(6.6, FLOOR, 4.4), [metal, metal, carpet, dark, metal, metal]), false, true))
    .children.at(-1).position.set(0, FLOOR / 2, 0);
  const led = new THREE.MeshBasicMaterial({ color: 0xfff1d0 });
  [[6.62, 0.028, 0.028, 0, FLOOR - 0.02, 2.2], [0.028, 0.028, 4.42, -3.3, FLOOR - 0.02, 0], [0.028, 0.028, 4.42, 3.3, FLOOR - 0.02, 0]]
    .forEach(([w, h, d, x, y, z]) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), led); m.position.set(x, y, z); booth.add(m); });

  /* Lichtschein auf dem Boden */
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

  /* Gebogene Rückwand (Pop-up-Wand) */
  const WW = 4.8, WH = 2.55, SAG = 0.55, WZ = -1.6;
  const wg = new THREE.PlaneGeometry(WW, WH, 60, 1);
  const wp = wg.attributes.position;
  for (let i = 0; i < wp.count; i++) { const x = wp.getX(i); wp.setZ(i, SAG * (x / (WW / 2)) ** 2); }
  wg.computeVertexNormals();
  const wall = new THREE.Group();
  wall.position.set(0, FLOOR + WH / 2, WZ);
  wall.add(shadowed(new THREE.Mesh(wg, mat({ map: tex.wall.t, roughness: 0.55 })), true, true));
  wall.add(new THREE.Mesh(wg, mat({ color: 0x222c3a, roughness: 0.7, side: THREE.BackSide })));
  const slope = Math.atan(2 * SAG / (WW / 2));
  [-1, 1].forEach(sd => {
    const cap = shadowed(new THREE.Mesh(new THREE.BoxGeometry(0.09, WH + 0.02, 0.34), accentDark));
    cap.position.set(sd * (WW / 2 + 0.03), 0, SAG - 0.1);
    cap.rotation.y = -sd * slope;
    wall.add(cap);
  });
  booth.add(wall);

  /* Strahler auf der Wand */
  scene.add(new THREE.HemisphereLight(0xdff6ff, 0x1a2536, 1.1));
  const key = new THREE.DirectionalLight(0xffffff, 2.4);
  key.position.set(4, 8, 7); key.castShadow = true;
  Object.assign(key.shadow.camera, { left: -5, right: 5, top: 5, bottom: -5, near: 1, far: 25 });
  key.shadow.mapSize.set(2048, 2048); key.shadow.bias = -0.0004; key.shadow.normalBias = 0.02;
  scene.add(key);
  const fill = new THREE.DirectionalLight(0xbfe9ff, 0.8);
  fill.position.set(-6, 4, 3);
  scene.add(fill);
  const lensMat = new THREE.MeshBasicMaterial({ color: 0xfff6e0 });
  [-1.5, 0, 1.5].forEach(x => {
    const zTop = WZ + SAG * (x / (WW / 2)) ** 2;
    const y = FLOOR + WH;
    const arm = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.03, 0.38), dark);
    arm.position.set(x, y + 0.05, zTop + 0.17); booth.add(arm);
    const head = new THREE.Group();
    head.position.set(x, y + 0.06, zTop + 0.38);
    head.rotation.x = 2.3;
    const body = new THREE.Mesh(new THREE.CylinderGeometry(0.055, 0.08, 0.17, 20), dark);
    const lens = new THREE.Mesh(new THREE.CircleGeometry(0.07, 20), lensMat);
    lens.position.y = -0.086; lens.rotation.x = Math.PI / 2;
    head.add(body, lens); booth.add(head);
    const sp = new THREE.SpotLight(0xfff1dc, 22, 0, 0.6, 0.65, 2);
    sp.position.set(x, y + 0.02, zTop + 0.4);
    sp.target.position.set(x, FLOOR + 1.35, zTop);
    booth.add(sp, sp.target);
  });

  /* Theke */
  const counter = new THREE.Group();
  counter.position.set(0.25, FLOOR, 0.45);
  const sx = 1.35, sz = 0.72;
  const cBody = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.62, 0.62, 0.98, 72, 1, true, Math.PI, Math.PI * 2), mat({ map: tex.counter.t, roughness: 0.45 })));
  cBody.scale.set(sx, 1, sz); cBody.position.y = 0.53;
  const cTop = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.67, 0.67, 0.05, 72), mat({ color: 0x20252d, roughness: 0.3, metalness: 0.3 })));
  cTop.scale.set(sx, 1, sz); cTop.position.y = 1.045;
  const cBase = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.6, 0.6, 0.05, 72), dark));
  cBase.scale.set(sx, 1, sz); cBase.position.y = 0.025;
  counter.add(cBody, cTop, cBase);
  const stack = shadowed(new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.035, 0.2), white));
  stack.position.set(-0.05, 1.088, 0.05); stack.rotation.y = 0.2;
  counter.add(stack);
  const holder = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.26, 0.07), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.05, transparent: true, opacity: 0.28 }));
  holder.position.set(0.48, 1.2, 0.02); holder.rotation.set(-0.12, -0.3, 0);
  const flyer = new THREE.Mesh(new THREE.PlaneGeometry(0.17, 0.24), mat({ map: tex.rollupA.t, roughness: 0.5 }));
  flyer.position.set(0.48, 1.2, 0.03); flyer.rotation.set(-0.12, -0.3, 0);
  counter.add(holder, flyer);
  booth.add(counter);

  /* Roll-ups */
  function rollup(t, x, z, ry) {
    const g = new THREE.Group();
    g.position.set(x, FLOOR, z); g.rotation.y = ry;
    const W = 0.85, H = 2.0;
    const ban = shadowed(new THREE.Mesh(new THREE.PlaneGeometry(W, H), mat({ map: t, roughness: 0.5 })));
    ban.position.y = 0.13 + H / 2;
    const back = new THREE.Mesh(new THREE.PlaneGeometry(W, H), mat({ color: 0xd9dde2, roughness: 0.8, side: THREE.BackSide }));
    back.position.copy(ban.position);
    const cas = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, W + 0.06, 24), metal));
    cas.rotation.z = Math.PI / 2; cas.position.set(0, 0.075, 0.01);
    const bar = new THREE.Mesh(new THREE.CylinderGeometry(0.013, 0.013, W + 0.02, 12), metal);
    bar.rotation.z = Math.PI / 2; bar.position.set(0, 0.13 + H, 0.005);
    const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.009, 0.009, H, 8), metal);
    pole.position.set(0, 0.13 + H / 2, -0.03);
    [-1, 1].forEach(s => { const f = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.02, 0.3), metal); f.position.set(s * (W / 2 - 0.05), 0.01, 0); g.add(f); });
    g.add(ban, back, cas, bar, pole);
    booth.add(g);
  }
  rollup(tex.rollupA.t, -2.78, 0.35, 0.32);
  rollup(tex.rollupB.t, 2.9, -0.45, -0.45);

  /* Beachflag (Feder-Form, weht leicht) */
  const flag = new THREE.Group();
  flag.position.set(2.5, FLOOR, 1.45); flag.rotation.y = 0.2;
  const SU = 14, SV = 44;
  const fg = new THREE.PlaneGeometry(1, 1, SU, SV);
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
  const sail = shadowed(new THREE.Mesh(fg, mat({ map: tex.flag.t, roughness: 0.6, side: THREE.DoubleSide })));
  const polePts = [new THREE.Vector3(0, 0.02, 0), new THREE.Vector3(0, 1.8, 0), new THREE.Vector3(0, 3.05, 0)];
  for (let k = 1; k <= 6; k++) { const u = k / 6; polePts.push(new THREE.Vector3(u * wid(1), yTop(u), 0)); }
  const fpole = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(polePts), 64, 0.014, 8), dark);
  fpole.castShadow = true;
  const fbase = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.26, 0.05, 32), dark));
  fbase.position.y = 0.025;
  flag.add(sail, fpole, fbase);
  booth.add(flag);

  /* Tisch und Stühle */
  const table = new THREE.Group();
  table.position.set(1.45, FLOOR, -0.55);
  const tt = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.38, 0.03, 40), white)); tt.position.y = 0.74;
  const ts = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.72, 12), metal)); ts.position.y = 0.37;
  const tb = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.25, 0.025, 32), metal)); tb.position.y = 0.012;
  table.add(tt, ts, tb);
  booth.add(table);
  function chair(x, z, ry) {
    const g = new THREE.Group(); g.position.set(x, FLOOR, z); g.rotation.y = ry;
    const seat = shadowed(new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.05, 0.42), white)); seat.position.y = 0.46;
    const back = shadowed(new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.36, 0.04), white)); back.position.set(0, 0.68, -0.2); back.rotation.x = -0.12;
    g.add(seat, back);
    [[-1, -1], [1, -1], [-1, 1], [1, 1]].forEach(([a, b]) => {
      const l = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.012, 0.47, 8), wood));
      l.position.set(a * 0.16, 0.225, b * 0.16); l.rotation.set(b * 0.08, 0, -a * 0.08); g.add(l);
    });
    booth.add(g);
  }
  chair(1.0, -0.35, 1.2);
  chair(1.9, -0.3, -1.25);

  /* Pflanzen */
  const leafGeo = new THREE.SphereGeometry(1, 12, 8);
  const greens = [0x2f7d3b, 0x3d9447, 0x28692f, 0x4aa653];
  function plant(x, y, z, s) {
    const g = new THREE.Group(); g.position.set(x, y, z); g.scale.setScalar(s);
    const pot = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.15, 0.5, 32), mat({ color: 0xf5f5f2, roughness: 0.25 }))); pot.position.y = 0.25;
    const soil = new THREE.Mesh(new THREE.CircleGeometry(0.19, 24), mat({ color: 0x3a2a1e, roughness: 1 })); soil.rotation.x = -Math.PI / 2; soil.position.y = 0.49;
    g.add(pot, soil);
    const n = 20;
    for (let i = 0; i < n; i++) {
      const a = (i / n) * Math.PI * 2 + (i % 3) * 0.4, tilt = 0.25 + ((i * 7) % 10) / 14, len = 0.3 + ((i * 5) % 7) / 28;
      const leaf = shadowed(new THREE.Mesh(leafGeo, mat({ color: greens[i % 4], roughness: 0.6 })), true, false);
      leaf.scale.set(0.075, len, 0.012);
      const piv = new THREE.Group(); piv.position.y = 0.5; piv.rotation.set(0, a, 0);
      const inner = new THREE.Group(); inner.rotation.x = tilt;
      leaf.position.y = len; inner.add(leaf); piv.add(inner); g.add(piv);
    }
    booth.add(g);
  }
  plant(-1.95, FLOOR, -0.85, 1.25);
  plant(-0.45, FLOOR + 1.07, 0.45, 0.42);

  /* ── Farbe ─────────────────────────────────────── */
  function paint(C) {
    for (const k in tex) {
      const { c, ctx, t } = tex[k];
      PAINT[k](ctx, c.width, c.height, C);
      t.needsUpdate = true;
    }
    accentDark.color.set(mix(C, NAVY, 0.8));
    hero.style.setProperty('--mb-accent', C);
  }
  let current = (swatches.find(b => b.getAttribute('aria-pressed') === 'true') || swatches[0]);
  paint(current ? current.dataset.c : '#58d0bd');
  swatches.forEach(b => b.addEventListener('click', () => {
    swatches.forEach(o => o.setAttribute('aria-pressed', String(o === b)));
    paint(b.dataset.c);
    kick();
  }));

  /* ── Kamera & Maus ─────────────────────────────── */
  const T = new THREE.Vector3(0, 1.2, 0);
  const BASE_YAW = 0.22, BASE_PITCH = 0.11;
  let yaw = BASE_YAW, pitch = BASE_PITCH, tYaw = yaw, tPitch = pitch, dist = 14, lastMove = -1e9;
  if (!reduced) {
    hero.addEventListener('pointermove', e => {
      if (e.pointerType === 'touch') return;
      const r = hero.getBoundingClientRect();
      const nx = (e.clientX - r.left) / r.width * 2 - 1;
      const ny = (e.clientY - r.top) / r.height * 2 - 1;
      tYaw = BASE_YAW + nx * 0.5;
      tPitch = BASE_PITCH - ny * 0.07;
      lastMove = performance.now();
      kick();
    }, { passive: true });
    hero.addEventListener('pointerleave', () => { lastMove = performance.now() - 1500; });
  }

  function resize() {
    const w = stage.clientWidth, h = stage.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    const vt = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));
    const frac = w > 1100 ? 0.45 : 0.5;
    dist = Math.max(3.5 / (vt * camera.aspect * frac), 1.75 / (vt * 0.74), 9);
    camera.setViewOffset(w, h, -w * (w > 1100 ? 0.22 : 0.23), -h * 0.03, w, h);
    camera.updateProjectionMatrix();
    kick();
  }
  new ResizeObserver(resize).observe(stage);

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
      tYaw = BASE_YAW + Math.sin(t * 0.22) * 0.28;
      tPitch = BASE_PITCH + Math.sin(t * 0.17) * 0.03;
    }
    const k = 1 - Math.exp(-dt * 3.2);
    yaw += (tYaw - yaw) * k; pitch += (tPitch - pitch) * k;
    camera.position.set(T.x + dist * Math.sin(yaw) * Math.cos(pitch), T.y + dist * Math.sin(pitch), T.z + dist * Math.cos(yaw) * Math.cos(pitch));
    camera.lookAt(T);

    if (!reduced) {
      for (let i = 0; i < fp.count; i++) {
        const x = base[i * 3], y = base[i * 3 + 1];
        const u = x / 0.74;
        fp.setZ(i, Math.sin(t * 2.1 + y * 2.2 + u * 2.5) * 0.045 * u);
      }
      fp.needsUpdate = true;
      fg.computeVertexNormals();
    }

    renderer.render(scene, camera);
    if (first) { first = false; hero.classList.add('mb-3d'); if (ui) ui.hidden = false; }
    const moving = !reduced || Math.abs(tYaw - yaw) > 1e-3 || Math.abs(tPitch - pitch) > 1e-3;
    if (moving && visible && !document.hidden) requestAnimationFrame(frame);
    else running = false;
  }
  resize();
  kick();
}
