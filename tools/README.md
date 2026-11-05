# Werkzeuge (nur für die Bearbeitung)

Der Ordner wird per `.htaccess` für Besucher gesperrt (`tools/`, `*.md`, `*.py`, `*.mjs`).
Alle Skripte arbeiten standardmäßig im Repository-Wurzelordner. Mit `MASAR_ROOT=/pfad/kopie`
lassen sie sich gefahrlos an einer Kopie testen.

Voraussetzungen: Python 3 (+ Pillow für `nrw_pages.py`), Node mit Playwright
(lokal oder global, `npm root -g`), Chromium unter `/opt/pw-browsers/chromium` oder Playwright-Standard.

## Ein Befehl: bauen und prüfen

```
python3 tools/build_all.py --check   # Probelauf in einer Kopie + zweiter Lauf: muss „Idempotent“ melden
python3 tools/build_all.py           # alles im Repository: Generatoren → OG erhalten → Nachbearbeitung
python3 tools/check_site.py          # Links, Anker, Bilder/Skripte, doppelte IDs, alt, <main>, Sitemap, ?v=, Blöcke
node tools/smoke_test.mjs            # Browser-Rauchtest 390/1280 px (startet php -S selbst)
```

- `build_all.py` führt alle Generatoren und die Nachbearbeitung in der Reihenfolge unten aus, bricht beim ersten
  Fehler ab und zeigt je Schritt, wie viele Dateien er geändert hat. `--dry` arbeitet nur in einer temporären Kopie
  und listet die Dateien, die sich ändern würden; `--check` macht danach einen zweiten Lauf und meldet Exit 1, wenn
  der noch etwas ändert (so fallen Skripte auf, die Blöcke bei jedem Lauf verschieben). `--only post` (nur
  Nachbearbeitung), `--only a11y,marke`, `--skip ki_artikel`, `--list`, `-v`. Der interne Schritt `og` setzt die
  OG-Vorschaubilder (og:image/twitter:image) wieder ein, die die Seiten vor dem Lauf hatten – die Generatoren
  kennen sie nicht. Nicht enthalten: `og_cards.py add` (neue Vorschaubilder), `bannerpreise.py` (einmalig), Angebote.
- Regel für alle Nachbearbeitungs-Skripte: einen vorhandenen Marker-Block **an Ort und Stelle** ersetzen und nur
  neu einsetzen, wenn er fehlt – nie „entfernen und am Ende wieder anhängen“ (sonst wandern Blöcke bei jedem Lauf).
- `check_site.py` ändert nichts und endet mit Exit 1 bei Befunden; `--nur links,ids`, `--max 20`, `--list`.
  Ausnahmen: die QR-Landingpages (`qr.html`, `qr/index.html`) haben eine eigene Mini-Fußzeile ohne Claim und ohne `<main>`.
- `smoke_test.mjs` prüft wichtige Seiten auf JS-Fehler, fehlende eigene Dateien, waagerechtes Scrollen (nennt das zu
  breite Element) und ob Assistent, Terminbuchung, Status, KI-Demo und KI-Bausteine aufgebaut werden und auf den ersten
  Klick reagieren. Externe Hosts werden blockiert. `--all` (alle Sitemap-Seiten), `--pages a.html,b.html`,
  `--base http://…` (vorhandener Server), `--shots ordner/` (Bildschirmfotos). PHP-Endpunkte laufen dabei echt –
  `termin.php`/`bewertung.php` können in `data/` Dateien anlegen (per `.gitignore` ausgeschlossen).

## Seitengeneratoren

Kette: `branchen/gen_branchen.py` (Grundgerüst: Kopf, Navigation, Fußzeile aus
`schilder-berlin.html`, Icons, Helfer `esc`, `wa`, `sec`) → `folien/gen_folien.py`
(`build_f`, Folien-Layout) → die Seiten-Generatoren lesen den Code der Vorgänger per `exec`.

| Skript | Erzeugt |
|---|---|
| `folien/lkw_page.py` | LKW-/Fahrzeug-Seite |
| `folien/nrw_pages.py` | NRW-Leistungsseiten (Leuchtreklame, Schilder, Schaufenster, Fensterfolie, Webdesign) |
| `folien/nrw_staedte.py` | Städteseiten Köln, Düsseldorf, Dortmund, Essen, Bochum × 4 Leistungen |
| `folien/banner_pages.py` | `pvc-banner-berlin.html`, `pvc-banner-nrw.html` |
| `folien/umland_pages.py` | `werbeagentur-<stadt>.html` (15 Brandenburg + Herne, Mülheim, Bottrop) |
| `folien/einsatz_page.py` | `einsatzgebiete.html` |
| `folien/hamburg_page.py` | `werbeagentur-hamburg.html` (aus `werbeagentur-nrw.html`) |
| `folien/ki_pages.py` | `ki-fuer-arztpraxen-berlin.html`, `ki-fuer-pflegedienste-berlin.html` |
| `folien/textil_page.py` | `textildruck-berlin.html` |
| `blog/stadt_ratgeber.py`, `blog/ki_artikel.py` | Stadt-Ratgeber und KI-Ratgeber im Blog (siehe unten) |

Die Generatoren übernehmen Kopf, Navigation und Fußzeile aus `schilder-berlin.html`, aber ohne das offene `<main>` und
ohne die Kopf-Blöcke der Nachbearbeitung (`kopf-klar`, `a11y-fix`, `schnell`, `umbruch`) – die setzt die Kette selbst.
Am einfachsten alles über `build_all.py` laufen lassen.

Aufruf jeweils `python3 tools/folien/<skript>.py`. Danach immer:

1. `python3 tools/add_assistent.py` – baut den Anfrage-Assistenten ein (idempotent, `--dry` zum Prüfen)
   und `python3 tools/sticky_termin.py` – untere Leiste mit Link „Kostenlose Beratung buchen“ (Thema der Seite)
2. Vorschaubilder/Meta: `python3 tools/og/og_cards.py add <seite.html> <bild.webp|-> "<Kategorie>" "<Überschrift>" "<Unterzeile>"`
   (nur Meta-Tags: `og_cards.py meta <seite.html> "<Überschrift>"`)
3. Neue Seiten in `sitemap.xml`, ggf. `llms.txt` und `einsatzgebiete.html` eintragen, IndexNow melden.

Hinweis: Die Generatoren wurden am 15.10.2026 aus dem Verlauf wiederhergestellt und geprüft
(Inhalt identisch mit den Live-Seiten). Seit 05.11.2026 erzeugen sie die Lucide-Symbole der Live-Seiten,
`<style id="hero-mobile">` kommt aus der Vorlage, die OG-Angaben erhält `build_all.py` (Schritt `og`).
Ein kompletter Neuaufbau mit `build_all.py` ändert die Seiten nicht mehr inhaltlich (nur Leerraum/Reihenfolge im Kopf).
Nicht wiederhergestellt: die Datenmodule der älteren Seiten (`branchen/pages.py`,
`folien/folien_pages.py`) – `gen_branchen.py`/`gen_folien.py` dienen nur noch als Bibliothek.

## Angebote

```
python3 tools/angebot/angebot.py tools/angebot/privat/<kunde>.json
```

Erzeugt HTML + A4-PDF im Masar-Layout und rechnet Netto, MwSt., Brutto, Anzahlung/Rest.
Vorlage: `angebot/beispiel.json`. Kundendaten und Stempel (`privat/stempel.png`) nur in
`tools/angebot/privat/` – der Ordner ist in `.gitignore`, das Repository ist öffentlich.

## Blog: Stadt-Ratgeber

`python3 tools/blog/stadt_ratgeber.py` erzeugt `blog/werbeanlage-<stadt>.html` (19 Städte: NRW, Hamburg, Potsdam) mit belegten lokalen Regeln und Quellen; Vorlage ist `blog/aussenwerbung-berlin-ratgeber.html`.
Danach OG-Karten mit `og_cards.py add` erneuern. Die Stadtseiten verlinken per Hinweisbox auf ihren Ratgeber –
nach dem Neu-Erzeugen von `nrw_staedte.py`/`umland_pages.py` die Box wieder einsetzen (bei Hamburg macht das `hamburg_page.py`).

## Blog: Ratgeber Werbetechnik

`python3 tools/blog/werbetechnik_ratgeber.py` erzeugt 5 Ratgeber (Leuchtreklame Strom & Schaltzeiten, Werbung auf Autoscheiben,
Bauzaunbanner, Arbeitskleidung bedrucken, Logo-Dateien) aus der Vorlage `blog/fotowand-firmenfeier.html` und trägt sie
idempotent in `blog/index.html`, `sitemap.xml` und `llms.txt` ein. Vorschaubilder einmalig mit `og_cards.py add` (Werte im Feld `og`);
danach `blog_kurzbox.py` und `umbruch.py`.

## SEO: Suchergebnis-Snippets

`python3 tools/seo/snippets.py` setzt Titel und Beschreibung (inkl. og/twitter) für die Seiten mit den meisten
Impressionen laut Search Console (Titel ≤ 60 Zeichen, Beschreibung 110–160, nur echte „ab“-Preise).
`--dry` prüft nur die Längen. Nach dem Neu-Erzeugen von Seiten erneut ausführen.
`python3 tools/seo/stadt_lokal.py` fügt den 25 NRW-Städte-Leistungsseiten (schilder/leuchtreklame/schaufensterbeschriftung/
fensterfolie/werbeagentur × Köln, Düsseldorf, Dortmund, Essen, Bochum) einen Abschnitt „Vor Ort in <Stadt>“ mit den belegten
lokalen Regeln, Tipps und FAQ aus `tools/blog/stadt_ratgeber.py` hinzu (idempotent, Marker `<!-- lokal:start -->`).
Nach `nrw_staedte.py` erneut ausführen (die Fensterfolie-Städteseiten gibt es nicht mehr, dafür einen Städte-Abschnitt auf `fensterfolie-nrw.html`).

`python3 tools/seo/referenzen_einbau.py` zeigt drei echte Projektfotos („Aus unserer Arbeit“) auf Leuchtreklame-, Fahrzeug-,
Werbetechnik- und Regionsseiten.
`python3 tools/seo/hero_klar.py` setzt auf 14 Leistungsseiten oben „ab“-Preis + drei Zusagen (und echte Fotos bei Fahrzeug/Leuchtreklame Berlin).
`python3 tools/seo/wissen_abschnitte.py` setzt auf 8 Leistungsseiten (Leuchtreklame Berlin/NRW, Fahrzeugbeschriftung Berlin/NRW,
PVC-Banner Berlin/NRW, Textildruck, Grafikdesign) vor den FAQ einen belegten Wissens-Abschnitt mit Link zum passenden Ratgeber
(Marker `<!-- wissen:start -->`, idempotent) und einen Link-Chip in „Passend dazu“ (auch Schilder Berlin/NRW, LKW Berlin).
Hintergrund: `docs/wettbewerb-2026-11.md`.
Reihenfolge nach dem Neu-Erzeugen (so in `build_all.py`): Generatoren → OG erhalten → `add_assistent.py` → `sticky_termin.py` → `stadt_lokal.py` → `wissen_abschnitte.py` → `referenzen_slides.py` → `referenzen_einbau.py` → `hero_klar.py` → `snippets.py` → `blog_kurzbox.py` → `schnell.py` → `nrw_whatsapp.py` → `partner_hinweis.py` → `a11y.py` → `marke.py` (Farben nach Markenleitfaden, Claim) → `umbruch.py` (ohne Brotkrumen-Leiste und Silbentrennung) → `sitemap_lastmod.py` → zum Schluss `seo_check.py`.
`snippets.py` stellt am Ende auch die Vorschaubilder wieder her (`og_cards.py sync`: Seiten, die nach dem Neu-Erzeugen wieder `logo.png`
als og:image haben, bekommen ihr vorhandenes `og/<seite>.jpg`) und ruft `strukturdaten.py` auf (Artikel-JSON-LD mit Vorschaubild statt Logo,
`@id …/#identity` für author/publisher). `schnell.py` ergänzt außerdem `srcset` an Galerie-Bildern („Aus unserer Arbeit“) und entfernt das
Vorladen des Logos (Schriften und Hero-Bild haben Vorrang).

## SEO-Prüfung

`python3 tools/seo/seo_check.py` prüft alle öffentlichen Seiten und ändert nichts (`--kurz` nur Zusammenfassung, `--regel og-logo,faq`
nur bestimmte Regeln, Seitennamen als Argument nur diese Seiten). F = Fehler (Exit-Code 1), H = Hinweis. Regeln u. a.: Titel ≤ 60 Zeichen
und eindeutig, Beschreibung 50–160 und eindeutig, genau eine H1, Canonical = eigene URL, hreflang = Canonical, og:image vorhanden/kein Logo/
Maße stimmen, JSON-LD gültig (FAQ-Fragen sichtbar, Brotkrumen-Ziele vorhanden, Artikel mit Bild, VideoObject-Pflichtfelder, Adresse nur
Bristolstraße 19E, Firmen-`@id`), Bilder (alt, width/height, Datei vorhanden, srcset, kein lazy am Hero), interne Links ohne tote Ziele,
verwaiste Seiten, fast gleiche Seiten (`aehnlich`, ≥ 60 % gleicher Haupttext – Doorway-Risiko), Sitemap vollständig/ohne noindex,
lastmod aktuell, robots.txt, llms.txt-Links.
`python3 tools/seo/sitemap_lastmod.py` setzt `<lastmod>` nur, wenn sich der sichtbare Haupttext einer Seite geändert hat (Hash-Speicher
`tools/seo/inhalt_hashes.json`; Technik-, Farb- oder Fußzeilen-Änderungen zählen nicht). `--dry` zeigt nur an, `--git` berechnet die Startwerte neu.
`python3 tools/seo/partner_hinweis.py` legt offen, wer was ausführt (Inhaber, 05.11.2026): Footer-Zeile auf allen Seiten, Hinweis-Kasten vor dem
Kontaktformular auf Leuchtreklame-, Messe-, Fahrzeug-, Schilder- und Regionsseiten, und auf Leuchtreklame-Seiten keine eigene Herstellung/Montage
beleuchteter Anlagen (Bau/Montage durch in die Handwerksrolle eingetragene Partnerbetriebe, Anschluss durch eingetragenen Elektrofachbetrieb).
Neue Seiten mit Montage-Versprechen hier eintragen (`art_fuer`). Impressum-Abschnitt `#leistungserbringung`, AGB § 3.4.
`python3 tools/seo/a11y.py` sorgt für Barrierefreiheit nach WCAG (axe ohne Befund am 02.11.2026): echtes `<main>`, WhatsApp-Knopf/Sticky-Leiste als Landmark, Überschriftenfolge (Footer h2, Karten h3).
`python3 tools/seo/blog_kurzbox.py` setzt in jedem Ratgeber nach der Einleitung eine kurze Angebotsbox (Text/Link aus der `.article-cta` des Artikels) – nach neuen Ratgebern ausführen.
`python3 tools/seo/nrw_whatsapp.py` stellt die WhatsApp-Links auf NRW-Seiten (`data-region="nrw"`) auf das NRW-Team (0178 2410682) um; der Assistent nutzt dort dieselbe Nummer.
`python3 tools/seo/schnell.py` fügt allen öffentlichen Seiten Speculation Rules (Vorladen interner Links) und weiche Seitenübergänge (View Transitions) hinzu – auch nach neuen Seiten ausführen.

## Markenleitfaden
`tools/brand/brand_guide.html` → `Masar_Markenleitfaden.pdf` (2 Seiten: Logo, Farben, Schrift, Sprache, Bildsprache, Anwendung).
Neu erzeugen: `node tools/angebot/pdf.mjs tools/brand/brand_guide.html tools/brand/Masar_Markenleitfaden.pdf`.
`logo_transparent.png` / `logo_negativ.png` (weiß auf Navy) liegen daneben. Claims sind nur Vorschläge, nicht festgelegt.

## Referenzen als Bilderstrecken
`python3 tools/seo/referenzen_slides.py` baut auf `referenzen.html` je Leistung eine Slideshow (Leuchtreklame, Schaufenster & Folien,
Fahrzeuge, Druck & Gastro-Werbung, Aus der Werkstatt, Digital Signage, Grafikdesign) – Bilder, Texte und Reihenfolge stehen in `KATEGORIEN`.
Neue Fotos: farbkorrigiert als `referenzen/<name>.webp` (max. 1600 px) + `<name>-720.webp` ablegen, Eintrag ergänzen, Skript ausführen,
danach `referenzen_einbau.py` (Leistungsseiten) und `a11y.py`. Nur echte, fertige Arbeiten – Visualisierungen/Mockups nicht als Referenz.
