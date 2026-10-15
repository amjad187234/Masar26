// Rendert Vorschaubilder: node render.mjs jobs.json  (jobs: [{out, html}])
// Playwright wird lokal oder aus der globalen npm-Installation geladen.
import fs from 'fs';
import os from 'os';
import path from 'path';
import { pathToFileURL } from 'url';
import { createRequire } from 'module';
import { execSync } from 'child_process';

let pw;
try { pw = await import('playwright'); }
catch {
  const root = execSync('npm root -g').toString().trim();
  pw = createRequire(root + '/')('playwright');
}
const { chromium } = pw;
const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const exe = fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined;
const b = await chromium.launch(exe ? { executablePath: exe } : {});
const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
for (const j of jobs) {
  // als Datei laden, damit file://-Schriften und -Bilder erlaubt sind
  const tmp = path.join(os.tmpdir(), 'og-' + process.pid + '.html');
  fs.writeFileSync(tmp, j.html);
  await p.goto(pathToFileURL(tmp).href, { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: j.out, type: 'jpeg', quality: 86 });
  fs.unlinkSync(tmp);
}
await b.close();
