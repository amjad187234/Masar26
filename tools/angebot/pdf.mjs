// HTML → A4-PDF: node pdf.mjs <eingabe.html> <ausgabe.pdf>
import fs from 'fs';
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
const [, , inp, out] = process.argv;
const exe = fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined;
const b = await pw.chromium.launch(exe ? { executablePath: exe } : {});
const p = await b.newPage();
await p.goto(pathToFileURL(path.resolve(inp)).href, { waitUntil: 'load' });
await p.evaluate(() => document.fonts.ready);
await p.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true });
await b.close();
