# Werkzeuge (nur für die Bearbeitung)

Der Ordner wird per `.htaccess` für Besucher gesperrt (`tools/`, `*.md`, `*.py`, `*.mjs`).
Alle Skripte arbeiten standardmäßig im Repository-Wurzelordner. Mit `MASAR_ROOT=/pfad/kopie`
lassen sie sich gefahrlos an einer Kopie testen.

Voraussetzungen: Python 3 (+ Pillow für `nrw_pages.py`), Node mit Playwright
(lokal oder global, `npm root -g`), Chromium unter `/opt/pw-browsers/chromium` oder Playwright-Standard.

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

Aufruf jeweils `python3 tools/folien/<skript>.py`. Danach immer:

1. `python3 tools/add_assistent.py` – baut den Anfrage-Assistenten ein (idempotent, `--dry` zum Prüfen)
   und `python3 tools/sticky_termin.py` – untere Leiste mit Link „Kostenlose Beratung buchen“ (Thema der Seite)
2. Vorschaubilder/Meta: `python3 tools/og/og_cards.py add <seite.html> <bild.webp|-> "<Kategorie>" "<Überschrift>" "<Unterzeile>"`
   (nur Meta-Tags: `og_cards.py meta <seite.html> "<Überschrift>"`)
3. Neue Seiten in `sitemap.xml`, ggf. `llms.txt` und `einsatzgebiete.html` eintragen, IndexNow melden.

Hinweis: Die Generatoren wurden am 15.10.2026 aus dem Verlauf wiederhergestellt und geprüft
(Inhalt identisch mit den Live-Seiten; die Live-Seiten haben zusätzlich OG-Meta und
`<style id="hero-mobile">` – diese nach dem Neu-Erzeugen erhalten bzw. wieder einsetzen).
Nicht wiederhergestellt: die Datenmodule der älteren Seiten (`branchen/pages.py`,
`folien/folien_pages.py`) – `gen_branchen.py`/`gen_folien.py` dienen nur noch als Bibliothek.

## Angebote

```
python3 tools/angebot/angebot.py tools/angebot/privat/<kunde>.json
```

Erzeugt HTML + A4-PDF im Masar-Layout und rechnet Netto, MwSt., Brutto, Anzahlung/Rest.
Vorlage: `angebot/beispiel.json`. Kundendaten und Stempel (`privat/stempel.png`) nur in
`tools/angebot/privat/` – der Ordner ist in `.gitignore`, das Repository ist öffentlich.
