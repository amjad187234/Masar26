// Werbevideos für die Website (16:9, 1280×720, 30 fps, ohne Ton) aus echten Referenzfotos.
// Aufbau: Intro → 4 Projekt-Szenen (Foto mit langsamem Zoom, Bildunterschrift, Nutzen-Satz) → Abschlusskarte.
// Bild für Bild mit Chromium gerendert (Web-Animations angehalten und gesetzt), dann ffmpeg → MP4 (H.264) + WebM (VP9) + Poster.
// Aufruf: node tools/video/werbevideos.mjs [name]   (Playwright-Pfad ggf. über PW=… setzen)
// Keine Preise im Video (Preisangaben bleiben auf den Seiten, brutto/netto).
import { createRequire } from 'module';
import fs from 'fs'; import path from 'path'; import { execFileSync } from 'child_process';
const PW = process.env.PW || '/opt/node-tools/node_modules/playwright/index.mjs';
const { chromium } = await import(PW);
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..');
const OUT = path.join(ROOT, 'videos');
const TMP = process.env.TMPDIR_VIDEO || path.join(ROOT, '..', 'video-frames');
const FPS = 30, INTRO = 1.3, SZENE = 2.7, OUTRO = 3.0;

const VIDEOS = [
  { name: 'werbung-leuchtreklame-berlin', eyebrow: 'Leuchtreklame · Berlin', titel: 'Leuchtreklame,<br><em>die man sieht.</em>', sub: 'Entwurf · Genehmigung · Montage',
    szenen: [
      ['leuchtreklame-berlin-08', 'Fassadenanlage am Eröffnungstag', 'Sichtbar – bei Tag und Nacht.'],
      ['leuchtlogo-rund-bside-montiert-01', 'The B-Side Events: runder Leuchtausleger', 'Ihr Logo als Leuchtkasten.'],
      ['leuchtreklame-berlin-07', 'Leuchtbuchstaben, fertig verdrahtet', 'Gebaut von eingetragenen Partnerbetrieben.'],
      ['leuchtreklame-berlin-04', 'Zweisprachige Leuchtwerbung für einen Eventsaal', 'Die Genehmigung prüfen wir mit.']],
    cta: 'Festpreis-Angebot nach Fotos' },
  { name: 'werbung-schaufenster-berlin', eyebrow: 'Schaufenster · Folien', titel: 'Schaufenster,<br><em>die verkaufen.</em>', sub: 'Beschriftung · Milchglas · Aktionsfolie',
    szenen: [
      ['praxis-schaufenster-berlin-02', 'Praxis: Eröffnungsbeklebung und Milchglas', 'Sichtschutz, der gut aussieht.'],
      ['schaufensterfolie-fahrschule-01', 'Fahrschule JAD: bedruckte Schaufensterfolie', 'Ihr Angebot – rund um die Uhr im Fenster.'],
      ['fensterbeschriftung-praxis-gold-01', 'Schriftzug in Gold auf dem Oberlicht', 'Edel bis ins Detail.'],
      ['schaufensterbeschriftung-pflegedienst-berlin-01', 'Pflegedienst: Logo und Öffnungszeiten', 'Öffnungszeiten immer im Blick.']],
    cta: 'Festpreis-Angebot nach Fotos' },
  { name: 'werbung-fahrzeugbeschriftung-berlin', eyebrow: 'Fahrzeugbeschriftung · Berlin', titel: 'Werbung,<br><em>die mitfährt.</em>', sub: 'Teilbeschriftung bis Vollfolierung',
    szenen: [
      ['fahrzeugbeschriftung-berlin-04', 'Transporter, fertig beschriftet', 'Ihr Fahrzeug wirbt bei jeder Fahrt.'],
      ['fahrzeugbeschriftung-berlin-01', 'Folie wird auf die Schiebetür aufgezogen', 'Sauber und blasenfrei verklebt.'],
      ['fahrzeugfolierung-berlin-01', 'Vollfolierung eines Imbisswagens', 'Vom Logo bis zur Vollfolierung.'],
      ['fahrzeugbeschriftung-berlin-03', 'Leistungen und Kontakt auf einen Blick', 'Entwurf inklusive.']],
    cta: 'Festpreis-Angebot nach Fotos' },
];

function html(v) {
  const u = p => 'file://' + path.join(ROOT, p);
  const T = INTRO + v.szenen.length * SZENE + OUTRO;
  const sz = v.szenen.map(([img, cap, satz], i) => {
    const t0 = INTRO + i * SZENE;
    return `<div class="sc" style="--t0:${t0}s"><div class="ph"><img src="${u('referenzen/' + img + '.webp')}"></div><div class="cap">${cap}</div></div>
      <div class="satz" style="--t0:${t0}s">${satz}</div>`;
  }).join('');
  const bars = v.szenen.map((_, i) => `<i style="--t0:${INTRO + i * SZENE}s"></i>`).join('');
  return `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:BC;src:url(${u('fonts/barlow-condensed-black.woff2')})}
@font-face{font-family:B;src:url(${u('fonts/barlow-regular.woff2')})}
@font-face{font-family:BS;src:url(${u('fonts/barlow-semibold.woff2')})}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1280px;height:720px;overflow:hidden;background:#132e50;font-family:B,sans-serif;color:#fff;position:relative}
.lines{position:absolute;inset:0;background:repeating-linear-gradient(115deg,rgba(88,208,189,.06) 0 2px,transparent 2px 46px)}
.left{position:absolute;left:64px;top:0;width:470px;height:720px;display:flex;flex-direction:column;justify-content:center}
.eb{font-family:BS;font-size:17px;letter-spacing:3px;text-transform:uppercase;color:#58d0bd;opacity:0;animation:fadeup .6s ease-out .2s forwards}
h1{font-family:BC;font-size:78px;line-height:.95;text-transform:uppercase;margin:.25em 0 .3em;opacity:0;animation:fadeup .7s ease-out .4s forwards}
h1 em{font-style:normal;color:#58d0bd}
.sub{font-family:BS;font-size:22px;color:#d1d3d4;opacity:0;animation:fadeup .6s ease-out .7s forwards}
.satz{position:absolute;left:64px;top:560px;width:480px;font-family:BS;font-size:27px;line-height:1.25;opacity:0;animation:satz ${SZENE}s ease-in-out var(--t0) both}
.right{position:absolute;right:0;top:0;width:720px;height:720px}
.sc{position:absolute;inset:0;opacity:0;animation:sc ${SZENE + .5}s ease-in-out var(--t0) both}
.ph{position:absolute;inset:0;overflow:hidden;clip-path:polygon(12% 0,100% 0,100% 100%,0 100%)}
.ph img{width:100%;height:100%;object-fit:cover;animation:kb ${SZENE + .6}s linear var(--t0) both}
.cap{position:absolute;right:28px;bottom:28px;max-width:520px;background:rgba(14,35,64,.88);border-left:4px solid #58d0bd;padding:10px 16px;font-family:BS;font-size:18px;border-radius:6px}
.bars{position:absolute;left:64px;top:640px;display:flex;gap:8px}
.bars i{display:block;width:46px;height:4px;border-radius:2px;background:rgba(255,255,255,.18);position:relative;overflow:hidden}
.bars i::after{content:"";position:absolute;inset:0;background:#58d0bd;transform-origin:left;transform:scaleX(0);animation:bar ${SZENE}s linear var(--t0) forwards}
.out{position:absolute;inset:0;background:#132e50;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;opacity:0;animation:fadein .6s ease-out ${T - OUTRO}s forwards}
.out img{width:140px;height:140px;object-fit:contain;background:#fff;border-radius:22px;padding:10px;margin-bottom:22px}
.out .c{font-family:BC;font-size:64px;text-transform:uppercase}.out .c em{font-style:normal;color:#58d0bd}
.out .k{font-family:BS;font-size:26px;margin-top:14px;color:#d1d3d4}
.out .btn{margin-top:26px;background:#58d0bd;color:#132e50;font-family:BS;font-size:26px;padding:14px 30px;border-radius:12px}
@keyframes fadeup{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:none}}
@keyframes fadein{from{opacity:0}to{opacity:1}}
@keyframes sc{0%{opacity:0}12%{opacity:1}88%{opacity:1}100%{opacity:0}}
@keyframes satz{0%{opacity:0;transform:translateY(16px)}14%{opacity:1;transform:none}86%{opacity:1}100%{opacity:0}}
@keyframes kb{from{transform:scale(1.02)}to{transform:scale(1.12)}}
@keyframes bar{to{transform:scaleX(1)}}
</style></head><body><div class="lines"></div>
<div class="right">${sz.replace(/<div class="satz"[\s\S]*?<\/div>/g, '')}</div>
<div class="left"><div class="eb">${v.eyebrow}</div><h1>${v.titel}</h1><div class="sub">${v.sub}</div></div>
${v.szenen.map(([, , satz], i) => `<div class="satz" style="--t0:${INTRO + i * SZENE}s">${satz}</div>`).join('')}
<div class="bars">${bars}</div>
<div class="out"><img src="${u('logo.webp')}"><div class="c">Werbung, die <em>man sieht.</em></div><div class="k">masar-werbeagentur.de · 0178 514 3918</div><div class="btn">${v.cta}</div></div>
</body></html>`;
}

function htmlReel(v) {
  const u = p => 'file://' + path.join(ROOT, p);
  const T = INTRO + v.szenen.length * SZENE + OUTRO;
  const sc = v.szenen.map(([img, cap], i) => `<div class="sc" style="--t0:${INTRO + i * SZENE}s"><div class="ph"><img src="${u('referenzen/' + img + '.webp')}"></div><div class="cap">${cap}</div></div>`).join('');
  const satz = v.szenen.map(([, , s], i) => `<div class="satz" style="--t0:${INTRO + i * SZENE}s">${s}</div>`).join('');
  const bars = v.szenen.map((_, i) => `<i style="--t0:${INTRO + i * SZENE}s"></i>`).join('');
  return `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:BC;src:url(${u('fonts/barlow-condensed-black.woff2')})}
@font-face{font-family:BS;src:url(${u('fonts/barlow-semibold.woff2')})}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;overflow:hidden;background:#132e50;font-family:BS,sans-serif;color:#fff;position:relative}
.lines{position:absolute;inset:0;background:repeating-linear-gradient(115deg,rgba(88,208,189,.06) 0 3px,transparent 3px 70px)}
.top{position:absolute;left:80px;right:160px;top:210px}
.eb{font-size:30px;letter-spacing:5px;text-transform:uppercase;color:#58d0bd;opacity:0;animation:fadeup .6s ease-out .15s forwards}
h1{font-family:BC;font-size:132px;line-height:.92;text-transform:uppercase;margin:.2em 0 .25em;opacity:0;animation:fadeup .7s ease-out .3s forwards}
h1 em{font-style:normal;color:#58d0bd}
.sub{font-size:36px;color:#d1d3d4;opacity:0;animation:fadeup .6s ease-out .55s forwards}
.satz{position:absolute;left:80px;right:160px;top:700px;font-size:46px;line-height:1.2;opacity:0;animation:satz ${SZENE}s ease-in-out var(--t0) both}
.bars{position:absolute;left:80px;top:810px;display:flex;gap:12px}
.bars i{display:block;width:80px;height:6px;border-radius:3px;background:rgba(255,255,255,.18);position:relative;overflow:hidden}
.bars i::after{content:"";position:absolute;inset:0;background:#58d0bd;transform-origin:left;transform:scaleX(0);animation:bar ${SZENE}s linear var(--t0) forwards}
.right{position:absolute;left:0;right:0;top:870px;height:1050px}
.sc{position:absolute;inset:0;opacity:0;animation:sc ${SZENE + .5}s ease-in-out var(--t0) both}
.ph{position:absolute;inset:0;overflow:hidden;clip-path:polygon(0 7%,100% 0,100% 100%,0 100%)}
.ph img{width:100%;height:100%;object-fit:cover;animation:kb ${SZENE + .6}s linear var(--t0) both}
.cap{position:absolute;left:80px;top:110px;max-width:760px;background:rgba(14,35,64,.9);border-left:6px solid #58d0bd;padding:14px 22px;font-size:30px;border-radius:8px}
.out{position:absolute;inset:0;background:#132e50;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 90px 200px;opacity:0;animation:fadein .6s ease-out ${T - OUTRO}s forwards}
.out img{width:240px;height:240px;object-fit:contain;background:#fff;border-radius:36px;padding:16px;margin-bottom:44px}
.out .c{font-family:BC;font-size:118px;line-height:.95;text-transform:uppercase}.out .c em{font-style:normal;color:#58d0bd;display:block}
.out .k{font-size:40px;margin-top:30px;color:#d1d3d4;line-height:1.4}
.out .btn{margin-top:44px;background:#58d0bd;color:#132e50;font-size:42px;padding:22px 44px;border-radius:18px}
@keyframes fadeup{from{opacity:0;transform:translateY(36px)}to{opacity:1;transform:none}}
@keyframes fadein{from{opacity:0}to{opacity:1}}
@keyframes sc{0%{opacity:0}12%{opacity:1}88%{opacity:1}100%{opacity:0}}
@keyframes satz{0%{opacity:0;transform:translateY(20px)}14%{opacity:1;transform:none}86%{opacity:1}100%{opacity:0}}
@keyframes kb{from{transform:scale(1.02)}to{transform:scale(1.12)}}
@keyframes bar{to{transform:scaleX(1)}}
</style></head><body><div class="lines"></div><div class="right">${sc}</div>
<div class="top"><div class="eb">${v.eyebrow}</div><h1>${v.titel}</h1><div class="sub">${v.sub}</div></div>
${satz}<div class="bars">${bars}</div>
<div class="out"><img src="${u('logo.webp')}"><div class="c">Werbung, die <em>man sieht.</em></div><div class="k">masar-werbeagentur.de<br>0178 514 3918</div><div class="btn">${v.cta}</div></div>
</body></html>`;
}

const REEL = process.env.FORMAT === 'reel';
const nur = process.argv[2];
const b = await chromium.launch();
for (const v of VIDEOS.filter(x => !nur || x.name === nur)) {
  const T = INTRO + v.szenen.length * SZENE + OUTRO, N = Math.round(T * FPS);
  const dir = path.join(TMP, v.name + (REEL ? '-reel' : '')); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  const f = path.join(dir, 'video.html'); fs.writeFileSync(f, REEL ? htmlReel(v) : html(v));
  const p = await b.newPage({ viewport: REEL ? { width: 1080, height: 1920 } : { width: 1280, height: 720 } });
  await p.goto('file://' + f); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
  await p.evaluate(() => document.getAnimations().forEach(a => a.pause()));
  for (let i = 0; i < N; i++) {
    const ms = i * 1000 / FPS;
    await p.evaluate(t => document.getAnimations().forEach(a => { a.currentTime = t; }), ms);
    await p.screenshot({ path: path.join(dir, `f${String(i).padStart(4, '0')}.jpg`), type: 'jpeg', quality: 92 });
  }
  await p.close();
  if (REEL) {
    const rd = path.join(OUT, 'reels'); fs.mkdirSync(rd, { recursive: true });
    const stumm = path.join(dir, 'stumm.mp4'), wav = path.join(dir, 'musik.wav'), mp4 = path.join(rd, v.name + '-reel.mp4');
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(dir, 'f%04d.jpg'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '21', '-preset', 'slow', stumm]);
    execFileSync('python3', [path.join(ROOT, 'tools', 'video', 'musik.py'), wav, String(T), String(VIDEOS.indexOf(v))]);
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', stumm, '-i', wav, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', mp4]);
    console.log(v.name, N, 'Bilder →', mp4); continue;
  }
  const mp4 = path.join(OUT, v.name + '.mp4'), webm = path.join(OUT, v.name + '.webm'), poster = path.join(OUT, v.name + '.webp');
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(dir, 'f%04d.jpg'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '23', '-preset', 'slow', '-movflags', '+faststart', mp4]);
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(dir, 'f%04d.jpg'), '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '38', '-row-mt', '1', webm]);
  const pf = path.join(dir, `f${String(Math.round((INTRO + 1.2) * FPS)).padStart(4, '0')}.jpg`);
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', pf, '-q:v', '80', poster]);
  console.log(v.name, N, 'Bilder →', mp4);
}
await b.close();
