# Masar Werbeagentur – Projektgedächtnis

Website masar-werbeagentur.de: statisches HTML + PHP, Hosting Hostinger.
**Dieses Repository ist öffentlich** – keine Kundendaten, Angebote mit Namen, Stempel,
Unterschriften, Passwörter oder Tokens committen. `kontakt-config.php` liegt nur auf dem Server.

## Arbeitsweise

- Mit dem Inhaber Arabisch (levantinisch) schreiben; Website-Texte und Kundennachrichten auf Deutsch.
- Entwicklung auf dem zugewiesenen `claude/…`-Branch, danach zusätzlich nach `main` pushen
  (`git push -u origin <branch> && git push origin HEAD:main`). Der Inhaber klickt in Hostinger
  selbst auf „Bereitstellen“.
- Kein Force-Push, kein Umschreiben der Historie.
- Größere Änderungen an URLs, Navigation oder noindex nur nach Freigabe.
- Nie Zahlen, Fähigkeiten, Bewertungen, Referenzen oder Rechtsaussagen erfinden; Rechtliches mit Quellen prüfen.
- Keine Bank-Zugangsdaten annehmen.
- Bei neuen Seiten immer Bilder einsetzen (auch mobil sichtbar, `<style id="hero-mobile">`) und auf
  einfache Bedienung achten.

## Unternehmen und Leistungsgebiet

- Ein Standort: Bristolstraße 19E, 13349 Berlin · Tel./WhatsApp 0178 514 3918 · info@masar-werbeagentur.de
- NRW: Team vor Ort, aber **keine Adresse/Filiale in NRW** behaupten. NRW-Seiten zeigen in
  Navigation/Mobilmenü WhatsApp/E-Mail statt Telefon.
- NRW-Team macht alles außer Foto/Video und Messebau. Messebau und Express nur Berlin.
- Keine Laternenwerbung anbieten.
- Zahlung: Überweisung.
- Sprachen der Beratung: Deutsch, Englisch, Arabisch, Türkisch (Türkisch vom Inhaber am 15.10.2026 bestätigt).

## Preise (netto, „ab“) – nur mit Freigabe ändern

| Leistung | Berlin | NRW |
|---|---|---|
| Schilder | 45 € | 59 € |
| Tür-/Klingelschild | 69 € | 85 € |
| Firmenschild | 149 € | 179 € |
| Einzelbuchstaben | 119 € | 139 € |
| Acrylglasschild | 240 € | 289 € |
| Praxis-/Kanzleischild | 390 € | 459 € |
| Leuchtbuchstaben (je Buchstabe) | 199 € | 229 € |
| Schaufensterbeschriftung | 149 € | 179 € |
| Milchglas/Sichtschutz | 190 € | 229 € |
| Milchglas nach Maß | 240 € | 289 € |
| Aktionsfolie | 190 € | 229 € |
| Lochfolie (m²) | 45 € | 55 € |
| Fahrzeug-Teilbeschriftung | 290 € | 340 € |
| PVC-Banner (m²) | 19 € | 22 € |
| Mesh-Banner (m²) | 22 € | 25 € |
| Blockout-Banner (m²) | 29 € | 33 € |
| Banner-Mindestpreis | 39 € | 49 € |

Überall gleich: Logo ab 490 €, Social Media ab 490 €/Monat, LED-Neon innen ab 249 €.
Der Inhaber hat NRW-Preise und Preise neuer Produkte „nach Marktrecherche“ freigegeben – jede
solche Festlegung im Bericht nennen.

## Aufbau der Website

- Seiten-Generatoren, Vorschaubilder, Angebots-PDF: siehe `tools/README.md`.
- Anfrage-Assistent `assistent.js` (Leistung → Auswahl → Details → Zeit & Ort → Kontakt →
  Zusammenfassung; Versand per WhatsApp oder E-Mail). Attribute: `data-start`, `data-region="nrw"`,
  `data-ort`, Karten öffnen ihn mit `data-as-open`. Altes Formular bleibt in `<details class="as-classic">`.
  Einbau mit `tools/add_assistent.py`.
- Anfragen-System: `inc/anfragen.php` (SQLite `data/anfragen.sqlite`, Nummern `ANF-JJJJ-NNNN`,
  Löschung nach 6 Monaten), `kontakt.php`, `anfrage-log.php` (WhatsApp-Weg), Übersicht
  `/admin/anfragen.php`. Telegram-Hinweise **ohne personenbezogene Daten**.
  Einrichtung auf dem Server in `kontakt-config.php`: `admin_pass_hash`, `telegram_token`,
  `telegram_chat` (siehe `kontakt-config.sample.php`). Datenschutzerklärung Abschnitt 6 beschreibt das.
- Anfragen haben Stadt + Region (Berlin/Brandenburg/NRW/Sonstige), automatisch aus Ortsangabe, PLZ
  oder Herkunftsseite (`anf_stadt()`), in der Detailansicht korrigierbar. Zeiten in Europe/Berlin.
- Terminbuchung „Kostenlose Beratung“: `termin.html` + `termin.js` + `termin.php`. Arten Telefon,
  WhatsApp-Video, Vor Ort (nur Berlin, 60 Min.); sonst 30 Min.; Mo–Fr 9–18, Sa 10–14; ab morgen,
  21 Tage im Voraus; Feiertage Berlin gesperrt, weitere Sperrtage per `termin_gesperrt` in
  kontakt-config.php. Termin = Anfrage mit Spalte `termin`; Status „Kein Auftrag“ oder Löschen gibt
  die Zeit frei. Footer-Link „Kostenlose Beratung buchen“ auf allen Seiten.
- SEO/KI-Suche: JSON-LD `LocalBusiness` mit `@id https://masar-werbeagentur.de/#identity` in
  `index.html`, `llms.txt`, `sitemap.xml`, IndexNow über `/indexnow.php`, Seite `einsatzgebiete.html`
  (im Footer aller Seiten verlinkt).

## Getroffene Entscheidungen

- PVC-Banner-Städteseiten (Köln, Düsseldorf, Dortmund, Essen, Bochum) zu `pvc-banner-nrw.html`
  zusammengeführt (301 in `.htaccess`) – zu ähnlich (Doorway-Risiko). Keine neuen Städteseiten,
  die sich nur im Ortsnamen unterscheiden.
- Umland-Seiten `werbeagentur-*` (Brandenburg + Herne, Mülheim, Bottrop) sind sich noch ähnlich –
  echte Projekte/Fotos je Stadt ergänzen, sobald vorhanden.

## Offen

- Phase 3: Angebote/Rechnungen aus der Anfragen-Übersicht; Phase 4: automatische Erinnerungen.
- Inhaber: `admin_pass_hash` und Telegram einrichten, E-Mail-Versand testen.

Kundennotizen (laufende Aufträge, Angebote) werden **nicht** hier, sondern privat geführt.
