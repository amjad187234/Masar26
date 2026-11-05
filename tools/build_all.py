"""Ein Befehl für die ganze Seiten-Kette: Generatoren → Nachbearbeitung (Reihenfolge laut tools/README.md).

  python3 tools/build_all.py                 alles (Generatoren + Nachbearbeitung) im Repository
  python3 tools/build_all.py --dry           alles in einer temporären Kopie – zeigt nur, welche Dateien sich ändern würden
  python3 tools/build_all.py --check         wie --dry, danach ein zweiter Lauf: Fehler (Exit 1), wenn er noch etwas ändert
  python3 tools/build_all.py --only post     nur die Nachbearbeitung (Gruppen: gen, post; oder Schritte, mit Komma)
  python3 tools/build_all.py --only a11y,marke,umbruch
  python3 tools/build_all.py --skip ki_artikel
  python3 tools/build_all.py --list          Schritte anzeigen
  -v / --verbose                             vollständige Ausgabe jedes Skripts

Bricht beim ersten Fehler ab (Exit-Code ≠ 0 oder Traceback). Jeder Schritt meldet, wie viele Dateien er geändert hat.
Die Generatoren kennen keine OG-Vorschaubilder (og_cards.py) – der Schritt „og“ setzt deshalb die og:image-/twitter:image-
Angaben, die die Seiten vor dem Lauf hatten, unverändert wieder ein. Nicht enthalten (bewusst): og_cards.py add (braucht
Chromium und Texte je Seite), bannerpreise.py (einmalig), angebot.py.
Mit MASAR_ROOT=/pfad/kopie arbeitet das Skript (wie alle Werkzeuge) an einer Kopie.
"""
import argparse, hashlib, os, re, shutil, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(HERE, '..'))).rstrip('/')

# (Name, Gruppe, Skript relativ zu tools/, Beschreibung)
SCHRITTE = [
    ('lkw', 'gen', 'folien/lkw_page.py', 'LKW-Beschriftung Berlin + NRW'),
    ('nrw_pages', 'gen', 'folien/nrw_pages.py', 'NRW-Leistungsseiten'),
    ('nrw_staedte', 'gen', 'folien/nrw_staedte.py', 'NRW-Städteseiten (Köln, Düsseldorf, Dortmund, Essen, Bochum)'),
    ('banner', 'gen', 'folien/banner_pages.py', 'PVC-Banner Berlin + NRW'),
    ('umland', 'gen', 'folien/umland_pages.py', 'werbeagentur-<stadt>.html (Brandenburg, Herne, Mülheim, Bottrop)'),
    ('einsatz', 'gen', 'folien/einsatz_page.py', 'einsatzgebiete.html'),
    ('hamburg', 'gen', 'folien/hamburg_page.py', 'werbeagentur-hamburg.html (aus werbeagentur-nrw.html)'),
    ('ki_pages', 'gen', 'folien/ki_pages.py', 'KI für Arztpraxen / Pflegedienste'),
    ('textil', 'gen', 'folien/textil_page.py', 'textildruck-berlin.html'),
    ('konfigurator', 'gen', 'folien/konfigurator_page.py', 'leuchtbuchstaben-konfigurator.html (kostenloses Werkzeug)'),
    ('druckcheck', 'gen', 'folien/druckcheck_page.py', 'druckdaten-check.html (kostenloses Werkzeug)'),
    ('stadt_ratgeber', 'gen', 'blog/stadt_ratgeber.py', 'blog/werbeanlage-<stadt>.html'),
    ('ki_artikel', 'gen', 'blog/ki_artikel.py', 'KI-Ratgeber im Blog'),
    ('werbetechnik_ratgeber', 'gen', 'blog/werbetechnik_ratgeber.py', '5 Ratgeber Werbetechnik'),
    ('og', 'gen', None, 'OG-Vorschaubilder der Seiten von vor dem Lauf wieder einsetzen'),
    ('add_assistent', 'post', 'add_assistent.py', 'Anfrage-Assistent in den Kontaktbereich'),
    ('sticky_termin', 'post', 'sticky_termin.py', 'Untere Leiste → „Kostenlose Beratung buchen“'),
    ('stadt_lokal', 'post', 'seo/stadt_lokal.py', 'Abschnitt „Vor Ort in <Stadt>“'),
    ('wissen_abschnitte', 'post', 'seo/wissen_abschnitte.py', 'Belegte Wissens-Abschnitte vor den FAQ'),
    ('referenzen_slides', 'post', 'seo/referenzen_slides.py', 'Bilderstrecken auf referenzen.html'),
    ('referenzen_einbau', 'post', 'seo/referenzen_einbau.py', '„Aus unserer Arbeit“ auf Leistungsseiten'),
    ('hero_klar', 'post', 'seo/hero_klar.py', '„ab“-Preis + Zusagen im Seitenkopf'),
    ('snippets', 'post', 'seo/snippets.py', 'Titel und Beschreibung'),
    ('blog_kurzbox', 'post', 'seo/blog_kurzbox.py', 'Kurze Angebotsbox in Ratgebern'),
    ('schnell', 'post', 'seo/schnell.py', 'Speculation Rules + View Transitions'),
    ('nrw_whatsapp', 'post', 'seo/nrw_whatsapp.py', 'WhatsApp NRW-Team auf NRW-Seiten'),
    ('partnerwerkstatt', 'post', 'seo/partnerwerkstatt.py', 'Keine eigene Werkstatt behaupten (Partnerwerkstatt)'),
    ('partner_hinweis', 'post', 'seo/partner_hinweis.py', 'Offenlegung Partnerbetriebe'),
    ('druckcheck_links', 'post', 'seo/druckcheck_links.py', 'Hinweise auf Druckdaten-Check und Konfigurator'),
    ('a11y', 'post', 'seo/a11y.py', 'Barrierefreiheit (main, Landmarks, Überschriften)'),
    ('marke', 'post', 'seo/marke.py', 'Farben nach Markenleitfaden + Claim'),
    ('umbruch', 'post', 'seo/umbruch.py', 'Ohne Brotkrumen-Leiste und Silbentrennung'),
    ('sitemap_lastmod', 'post', 'seo/sitemap_lastmod.py', 'lastmod nur bei geändertem Haupttext'),
]
NAMEN = [s[0] for s in SCHRITTE]
# Dateien, deren Änderungen gezählt werden (Bilder erzeugen nur referenzen_einbau.py, die zählen mit)
ZAEHLEN = ('.html', '.xml', '.txt', '.webp', '.jpg', '.png')
OHNE = ('.git', 'node_modules', '__pycache__', os.path.join('tools', 'angebot', 'privat'))

OG = re.compile(r'<meta property="og:image[^>]*>\n?')
TW = re.compile(r'<meta name="twitter:image" content="[^"]*">')


def farbe(t, c):
    return f'\033[{c}m{t}\033[0m' if sys.stdout.isatty() else t


def dateien(root):
    """{relativer Pfad: sha1} aller gezählten Dateien."""
    out = {}
    for d, ds, fs in os.walk(root):
        rel_d = os.path.relpath(d, root)
        ds[:] = [x for x in ds if os.path.normpath(os.path.join(rel_d, x)) not in OHNE and x not in OHNE]
        for f in fs:
            if f.endswith(ZAEHLEN):
                p = os.path.join(d, f)
                with open(p, 'rb') as fh:
                    out[os.path.normpath(os.path.join(rel_d, f))] = hashlib.sha1(fh.read()).hexdigest()
    return out


def unterschied(a, b):
    neu = sorted(set(b) - set(a)); weg = sorted(set(a) - set(b))
    geaendert = sorted(k for k in set(a) & set(b) if a[k] != b[k])
    return geaendert, neu, weg


# ── OG-Angaben sichern / wieder einsetzen ────────────────────────────────────────────────────────────
def og_sichern(root):
    alt = {}
    for d, ds, fs in os.walk(root):
        ds[:] = [x for x in ds if x not in OHNE and x not in ('tools', 'admin', 'data')]
        for f in fs:
            if not f.endswith('.html'): continue
            p = os.path.join(d, f)
            s = open(p, encoding='utf-8').read()
            og = OG.findall(s)
            if any('/og/' in m for m in og):
                tw = TW.search(s)
                alt[p] = (og, tw.group(0) if tw else None)
    return alt


def og_einsetzen(alt):
    n = 0
    for p, (og, tw) in alt.items():
        if not os.path.exists(p): continue
        s = open(p, encoding='utf-8').read()
        if OG.findall(s) == og and (tw is None or tw in s): continue
        m = OG.search(s)
        pos = m.start() if m else (s.find('<meta property="og:locale"') if '<meta property="og:locale"' in s else s.find('</head>'))
        if pos < 0: continue
        rest = OG.sub('', s[pos:])
        s = s[:pos] + ''.join(x if x.endswith('\n') else x + '\n' for x in og) + rest
        if tw: s = TW.sub(lambda _m: tw, s, count=1)
        open(p, 'w', encoding='utf-8').write(s); n += 1
    return n


# ── Ausführen ────────────────────────────────────────────────────────────────────────────────────────
def auswahl(only, skip):
    gew = []
    for teil in (only or 'gen,post').split(','):
        teil = teil.strip()
        if teil in ('gen', 'post', 'alle', 'all'):
            gew += [n for n, g, _, _ in SCHRITTE if teil in ('alle', 'all') or g == teil]
        elif teil in NAMEN:
            gew.append(teil)
        elif teil:
            raise SystemExit(f'Unbekannter Schritt „{teil}“ – mögliche: gen, post, ' + ', '.join(NAMEN))
    weg = {s.strip() for s in (skip or '').split(',') if s.strip()}
    for s in weg:
        if s not in NAMEN: raise SystemExit(f'Unbekannter Schritt „{s}“')
    return [n for n in NAMEN if n in gew and n not in weg]   # immer in der festen Reihenfolge


def lauf(root, namen, verbose=False, titel=''):
    """Führt die Schritte in root aus. Gibt (ok, Liste geänderter Dateien) zurück."""
    tools = os.path.join(root, 'tools')
    env = dict(os.environ, MASAR_ROOT=root, PYTHONDONTWRITEBYTECODE='1')
    vorher = dateien(root); start = vorher
    og_alt = og_sichern(root) if any(n != 'og' and dict((s[0], s[1]) for s in SCHRITTE)[n] == 'gen' for n in namen) else {}
    if titel: print(farbe(titel, '1'))
    for name in namen:
        _, gruppe, skript, text = next(s for s in SCHRITTE if s[0] == name)
        t0 = time.time()
        if skript is None:   # interner Schritt „og“
            n = og_einsetzen(og_alt); ausgabe = f'{n} Seiten mit OG-Bild von vor dem Lauf'; rc = 0
        else:
            r = subprocess.run([sys.executable, os.path.join(tools, skript)], cwd=root, env=env, capture_output=True, text=True)
            ausgabe = (r.stdout + r.stderr).strip(); rc = r.returncode
            if 'Traceback (most recent call last)' in ausgabe and rc == 0: rc = 1
        nachher = dateien(root)
        g, neu, weg = unterschied(vorher, nachher); vorher = nachher
        zahl = len(g) + len(neu) + len(weg)
        zeit = f'{time.time() - t0:4.1f}s'
        status = farbe('FEHLER', '31;1') if rc else (farbe(f'{zahl:3d} geändert', '33') if zahl else farbe('  – ', '2'))
        print(f'  [{gruppe:4}] {name:18} {status}  {zeit}  {text}')
        zeilen = [z for z in ausgabe.splitlines() if z.strip()]
        if rc or verbose:
            for z in zeilen[-40:] if rc else zeilen: print('         │ ' + z)
        else:
            # kurze Zusammenfassung: Warnungen + letzte Zeile, Routine-Meldungen („schon“) weglassen
            wichtig = [z for z in zeilen if re.search(r'fehlt|kein |Warn|Hinweis|nicht gefunden', z, re.I)]
            for z in (wichtig[:8] + zeilen[-1:]) if zeilen else []:
                print('         │ ' + z[:160])
        if rc:
            print(farbe(f'Abbruch: Schritt „{name}“ ist fehlgeschlagen (Exit {r.returncode}).', '31;1'))
            return False, []
    g, neu, weg = unterschied(start, vorher)
    return True, [('M', f) for f in g] + [('A', f) for f in neu] + [('D', f) for f in weg]


def kopie(src):
    ziel = tempfile.mkdtemp(prefix='masar-build-')
    dst = os.path.join(ziel, 'site')
    def ign(d, names):
        rel = os.path.relpath(d, src)
        return [n for n in names if n in ('.git', 'node_modules', '__pycache__') or os.path.normpath(os.path.join(rel, n)) == os.path.join('tools', 'angebot', 'privat')]
    shutil.copytree(src, dst, ignore=ign, symlinks=True)
    return ziel, dst


def liste(aend, max_n=60):
    for k, f in aend[:max_n]: print(f'    {k} {f}')
    if len(aend) > max_n: print(f'    … und {len(aend) - max_n} weitere')


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--dry', action='store_true', help='in einer temporären Kopie laufen, Repository bleibt unverändert')
    ap.add_argument('--check', action='store_true', help='--dry + zweiter Lauf; Exit 1, wenn der zweite Lauf etwas ändert')
    ap.add_argument('--only', help='Gruppen (gen, post) oder Schritte, mit Komma getrennt')
    ap.add_argument('--skip', help='Schritte auslassen, mit Komma getrennt')
    ap.add_argument('--list', action='store_true', help='Schritte anzeigen')
    ap.add_argument('--keep', action='store_true', help='temporäre Kopie bei --dry/--check behalten')
    ap.add_argument('-v', '--verbose', action='store_true')
    a = ap.parse_args()
    if a.list:
        for n, g, s, t in SCHRITTE: print(f'{n:18} {g:5} {s or "(intern)":28} {t}')
        return 0
    namen = auswahl(a.only, a.skip)
    if not namen: raise SystemExit('Keine Schritte ausgewählt.')
    if not (a.dry or a.check):
        ok, aend = lauf(ROOT, namen, a.verbose, f'Build in {ROOT} ({len(namen)} Schritte)')
        if not ok: return 1
        print(farbe(f'Fertig: {len(aend)} Dateien geändert.', '32;1'))
        liste(aend)
        return 0
    tmp, site = kopie(ROOT)
    try:
        ok, aend = lauf(site, namen, a.verbose, f'Probelauf in einer Kopie ({len(namen)} Schritte) – das Repository bleibt unverändert')
        if not ok: return 1
        print(farbe(f'Erster Lauf: {len(aend)} Dateien würden sich ändern.', '1'))
        liste(aend)
        if not a.check: return 0
        ok, aend2 = lauf(site, namen, a.verbose, 'Zweiter Lauf (Idempotenz)')
        if not ok: return 1
        if aend2:
            print(farbe(f'NICHT idempotent: der zweite Lauf ändert {len(aend2)} Dateien:', '31;1'))
            liste(aend2)
            return 1
        print(farbe('Idempotent: der zweite Lauf ändert nichts.', '32;1'))
        return 0
    finally:
        if a.keep: print('Kopie behalten:', site)
        else: shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
