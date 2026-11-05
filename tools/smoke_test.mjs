// Rauchtest im echten Browser (Playwright/Chromium): wichtige Seiten bei 390 px (Handy) und 1280 px (Desktop).
//
//   node tools/smoke_test.mjs                    wichtige Seiten (Liste SEITEN unten)
//   node tools/smoke_test.mjs --all              alle Seiten aus sitemap.xml
//   node tools/smoke_test.mjs --pages termin.html,status.html
//   node tools/smoke_test.mjs --base http://localhost:8000   vorhandenen Server nutzen statt php -S
//   node tools/smoke_test.mjs --shots DIR        Bildschirmfotos (ganze Seite) nach DIR schreiben
//
// Startet selbst `php -S 127.0.0.1:<freier Port>` im Repository (oder MASAR_ROOT). Prüft je Seite und Breite:
//   • keine JavaScript-Fehler (pageerror, console.error) – externe Hosts werden blockiert und nicht gezählt
//   • keine fehlenden eigenen Dateien (HTTP ≥ 400 vom lokalen Server)
//   • kein waagerechtes Scrollen (scrollWidth ≤ Fensterbreite), nennt die zu breiten Elemente
//   • Widgets sind aufgebaut: Anfrage-Assistent [data-assistent], Terminbuchung [data-termin],
//     Status [data-status], KI-Demo [data-ki-demo] und Bausteine [data-ki-bausteine]
//   • Assistent und Terminbuchung reagieren auf den ersten Klick (nächste Frage erscheint)
// Exit-Code 1 bei Befunden. Playwright: lokal, /opt/node-tools/node_modules oder global (npm root -g).
import fs from 'fs';
import net from 'net';
import path from 'path';
import { spawn, execSync } from 'child_process';
import { createRequire } from 'module';
import { fileURLToPath, pathToFileURL } from 'url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = (process.env.MASAR_ROOT || path.resolve(HERE, '..')).replace(/\/$/, '');

const SEITEN = [
  '', 'schilder-berlin.html', 'leuchtreklame-berlin.html', 'fahrzeugbeschriftung-berlin.html',
  'schaufensterbeschriftung-berlin.html', 'pvc-banner-berlin.html', 'textildruck-berlin.html',
  'werbeagentur-nrw.html', 'schilder-koeln.html', 'werbeagentur-hamburg.html', 'werbeagentur-bernau.html',
  'ki-fuer-arztpraxen-berlin.html', 'ki-fuer-pflegedienste-berlin.html', 'ki-loesungen/',
  'termin.html', 'status.html', 'einsatzgebiete.html', 'referenzen.html', 'blog/',
  'blog/werbeanlage-koeln.html', 'impressum.html', 'danke.html?nr=ANF-2026-0001',
];
const BREITEN = [390, 1280];

// ── Argumente ───────────────────────────────────────────────────────────────────────────────────
const args = process.argv.slice(2);
const arg = (k) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : undefined; };
let seiten = SEITEN;
if (args.includes('--all')) {
  const sm = fs.readFileSync(path.join(ROOT, 'sitemap.xml'), 'utf8');
  seiten = [...sm.matchAll(/<loc>\s*https:\/\/masar-werbeagentur\.de\/([^<\s]*)\s*<\/loc>/g)].map((m) => m[1]);
}
if (arg('--pages')) seiten = arg('--pages').split(',').map((s) => s.trim().replace(/^\//, ''));
const shots = arg('--shots');
if (shots) fs.mkdirSync(shots, { recursive: true });

// ── Playwright laden ────────────────────────────────────────────────────────────────────────────
async function ladePlaywright() {
  const kandidaten = ['playwright', '/opt/node-tools/node_modules/playwright/index.mjs'];
  for (const k of kandidaten) {
    try { return await import(k.startsWith('/') ? pathToFileURL(k).href : k); } catch {}
  }
  const root = execSync('npm root -g').toString().trim();
  return createRequire(root + '/')('playwright');
}

function freierPort() {
  return new Promise((res, rej) => {
    const s = net.createServer();
    s.listen(0, '127.0.0.1', () => { const p = s.address().port; s.close(() => res(p)); });
    s.on('error', rej);
  });
}

async function warteAufServer(url, ms = 8000) {
  const t0 = Date.now();
  while (Date.now() - t0 < ms) {
    try { const r = await fetch(url); if (r.status < 500) return; } catch {}
    await new Promise((r) => setTimeout(r, 150));
  }
  throw new Error('Server antwortet nicht: ' + url);
}

// ── Prüfungen im Browser ────────────────────────────────────────────────────────────────────────
const WIDGETS = [
  ['[data-assistent]', 'Anfrage-Assistent'],
  ['[data-termin]', 'Terminbuchung'],
  ['[data-status]', 'Status-Abfrage'],
  ['[data-ki-demo]', 'KI-Demo'],
  ['[data-ki-bausteine]', 'KI-Bausteine'],
];

async function pruefeSeite(browser, base, seite, breite) {
  const befunde = [];
  const ctx = await browser.newContext({
    viewport: { width: breite, height: breite < 600 ? 844 : 900 },
    deviceScaleFactor: 1, isMobile: breite < 600, hasTouch: breite < 600,
    locale: 'de-DE', timezoneId: 'Europe/Berlin', serviceWorkers: 'block',
  });
  const page = await ctx.newPage();
  const host = new URL(base).host;
  await page.route('**/*', (route) => {
    const u = new URL(route.request().url());
    if (u.host === host || u.protocol === 'data:' || u.protocol === 'blob:') return route.continue();
    return route.abort();   // extern (Fonts, Karten, Analytics …): offline testen
  });
  page.on('pageerror', (e) => befunde.push('JS-Fehler: ' + String(e.message || e).split('\n')[0]));
  page.on('console', (m) => {
    if (m.type() !== 'error') return;
    const t = m.text();
    if (/net::ERR_FAILED|ERR_BLOCKED|Failed to load resource/.test(t)) return;   // blockierte externe Anfragen
    befunde.push('console.error: ' + t.split('\n')[0].slice(0, 200));
  });
  page.on('response', (r) => {
    const u = new URL(r.url());
    if (u.host === host && r.status() >= 400 && !u.pathname.endsWith('.php')) befunde.push(`HTTP ${r.status()}: ${u.pathname}`);
  });

  const url = base + '/' + seite;
  try {
    const r = await page.goto(url, { waitUntil: 'load', timeout: 30000 });
    if (!r || r.status() >= 400) befunde.push(`Seite selbst: HTTP ${r ? r.status() : '–'}`);
  } catch (e) { befunde.push('Laden fehlgeschlagen: ' + e.message.split('\n')[0]); await ctx.close(); return befunde; }
  await page.waitForTimeout(600);

  // Widgets aufgebaut?
  for (const [sel, name] of WIDGETS) {
    const n = await page.locator(sel).count();
    if (!n) continue;
    try {
      await page.waitForFunction((s) => [...document.querySelectorAll(s)].every((el) => el.children.length > 0 && el.getBoundingClientRect().height > 20), sel, { timeout: 5000 });
    } catch { befunde.push(`${name} (${sel}) wurde nicht aufgebaut`); }
  }

  // Erste Interaktion: Assistent / Terminbuchung
  await interaktion(page, befunde);

  // Waagerechtes Scrollen
  const ov = await page.evaluate(() => {
    const vw = document.documentElement.clientWidth;
    const sw = Math.max(document.documentElement.scrollWidth, document.body ? document.body.scrollWidth : 0);
    if (sw <= vw + 1) return null;
    const zu = [];
    for (const el of document.body.querySelectorAll('*')) {
      const r = el.getBoundingClientRect();
      if (r.width && r.right > vw + 1 && getComputedStyle(el).position !== 'fixed') {
        // nur das äußerste zu breite Element melden
        let p = el.parentElement, innen = false;
        while (p && p !== document.body) { if (p.getBoundingClientRect().right > vw + 1) { innen = true; break; } p = p.parentElement; }
        if (!innen) zu.push(el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '') + ` (${Math.round(r.right)}px)`);
      }
      if (zu.length >= 4) break;
    }
    return { vw, sw, zu };
  });
  if (ov) befunde.push(`waagerechtes Scrollen: Seite ${ov.sw}px bei ${ov.vw}px Fenster – ${ov.zu.join(', ') || 'Element unklar'}`);

  if (shots) {
    const name = (seite || 'index').replace(/[/?=&]+/g, '_').replace(/_$/, '') + `-${breite}.png`;
    await page.screenshot({ path: path.join(shots, name), fullPage: true }).catch(() => {});
  }
  await ctx.close();
  return befunde;
}

async function interaktion(page, befunde) {
  // Assistent: erste Auswahl anklicken → es muss sich etwas ändern
  const as = page.locator('[data-assistent]').first();
  if (await as.count()) {
    let knopf = as.locator('button.as-opt:visible, button.as-card:visible').first();
    if (!(await knopf.count())) knopf = as.locator('button:visible').first();
    if (await knopf.count()) {
      const vorher = await as.innerHTML().catch(() => '');
      await knopf.scrollIntoViewIfNeeded().catch(() => {});
      await knopf.click({ timeout: 3000 }).catch((e) => befunde.push('Assistent: Klick nicht möglich – ' + e.message.split('\n')[0]));
      await page.waitForTimeout(400);
      const nachher = await as.innerHTML().catch(() => '');
      if (vorher === nachher) befunde.push('Assistent: erster Klick ändert nichts');
    }
  }
  const tm = page.locator('[data-termin]').first();
  if (await tm.count()) {
    const knopf = tm.locator('button:visible').first();
    if (await knopf.count()) {
      const vorher = await tm.innerHTML().catch(() => '');
      await knopf.scrollIntoViewIfNeeded().catch(() => {});
      await knopf.click({ timeout: 3000 }).catch((e) => befunde.push('Terminbuchung: Klick nicht möglich – ' + e.message.split('\n')[0]));
      await page.waitForTimeout(400);
      const nachher = await tm.innerHTML().catch(() => '');
      if (vorher === nachher) befunde.push('Terminbuchung: erster Klick ändert nichts');
    }
  }
}

// ── Ablauf ──────────────────────────────────────────────────────────────────────────────────────
let server = null;
let base = arg('--base');
const aufraeumen = () => { if (server) { try { server.kill('SIGTERM'); } catch {} server = null; } };
process.on('exit', aufraeumen);
process.on('SIGINT', () => { aufraeumen(); process.exit(130); });

let fehler = 0;
try {
  if (!base) {
    const port = await freierPort();
    base = `http://127.0.0.1:${port}`;
    // Mehrere Worker: Chromium öffnet Verbindungen im Voraus (preconnect), ein einzelner php -S hängt sonst daran
    server = spawn('php', ['-S', `127.0.0.1:${port}`, '-t', ROOT], { cwd: ROOT, stdio: ['ignore', 'ignore', 'ignore'], env: { ...process.env, PHP_CLI_SERVER_WORKERS: '6' } });
    server.on('error', (e) => { console.error('php -S konnte nicht starten:', e.message); process.exit(2); });
    await warteAufServer(base + '/robots.txt');
  }
  base = base.replace(/\/$/, '');
  const pw = await ladePlaywright();
  const chromium = pw.chromium || (pw.default && pw.default.chromium);
  const exe = fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined;
  const browser = await chromium.launch(exe ? { executablePath: exe } : {});
  console.log(`Rauchtest: ${seiten.length} Seiten × ${BREITEN.join(' / ')} px gegen ${base}`);
  for (const seite of seiten) {
    for (const b of BREITEN) {
      const t0 = Date.now();
      const bef = await pruefeSeite(browser, base, seite, b);
      const uniq = [...new Set(bef)];
      fehler += uniq.length;
      const name = ('/' + seite).padEnd(42);
      console.log(`  ${uniq.length ? 'FEHLER' : 'ok    '} ${name} ${String(b).padStart(4)} px  ${((Date.now() - t0) / 1000).toFixed(1)}s`);
      for (const x of uniq) console.log('         │ ' + x);
    }
  }
  await browser.close();
} catch (e) {
  console.error('Abbruch:', e.message);
  aufraeumen();
  process.exit(2);
}
aufraeumen();
console.log(fehler ? `\n${fehler} Befund(e).` : '\nKeine Befunde.');
process.exit(fehler ? 1 : 0);
