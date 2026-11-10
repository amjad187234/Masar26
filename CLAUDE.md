# Masar Werbeagentur – Projektgedächtnis

Website masar-werbeagentur.de: statisches HTML + PHP, Hosting Hostinger.
**Dieses Repository ist öffentlich** – keine Kundendaten, Angebote mit Namen, Stempel,
Unterschriften, Passwörter oder Tokens committen. `kontakt-config.php` liegt nur auf dem Server.

## Arbeitsweise

- Mit dem Inhaber Arabisch (levantinisch) schreiben; Website-Texte und Kundennachrichten auf Deutsch.
- Kundennachrichten immer als kopierbaren Codeblock (```) ausgeben, ohne Markdown-Formatierung im Text (Inhaber, 03.11.2026).
- Entwicklung auf dem zugewiesenen `claude/…`-Branch, danach zusätzlich nach `main` pushen
  (`git push -u origin <branch> && git push origin HEAD:main`). Der Inhaber klickt in Hostinger
  selbst auf „Bereitstellen“.
- Kein Force-Push, kein Umschreiben der Historie.
- Größere Änderungen an URLs, Navigation oder noindex nur nach Freigabe.
- **Vollmacht für die Website (Inhaber, 10.11.2026):** Preise, neue Seiten/Ratgeber, Rechts- und Leistungstexte darf Claude selbst entscheiden und umsetzen („entscheide du, du hast alle meine Infos“). Grenzen bleiben: nichts erfinden (Zahlen, Bewertungen, Referenzen, Fähigkeiten), Rechtliches mit Quelle prüfen, nur Leistungen nennen, die hier dokumentiert sind; jede Preis-/Leistungsentscheidung im Bericht nennen und hier festhalten. **Kundendateien, Kundenkartei, Belege (Drive, `tools/angebot/privat`, Anfragen-Datenbank) nie anfassen.**
- Nie Zahlen, Fähigkeiten, Bewertungen, Referenzen oder Rechtsaussagen erfinden; Rechtliches mit Quellen prüfen.
- Keine Bank-Zugangsdaten annehmen.
- Bei neuen Seiten immer Bilder einsetzen (auch mobil sichtbar, `<style id="hero-mobile">`) und auf
  einfache Bedienung achten.

## Unternehmen und Leistungsgebiet

- Ein Standort: Bristolstraße 19E, 13349 Berlin · Tel./WhatsApp 0178 514 3918 · info@masar-werbeagentur.de
- NRW: Team vor Ort, aber **keine Adresse/Filiale in NRW** behaupten. NRW-Seiten zeigen in
  Navigation/Mobilmenü WhatsApp/E-Mail statt Telefon.
- WhatsApp NRW-Team: 0178 2410682 (Inhaber, 28.10.2026) – in Nachrichten an NRW-Kunden nennen. Auf allen NRW-Seiten (`data-region="nrw"`) als WhatsApp-Link und im Assistenten (`tools/seo/nrw_whatsapp.py`); Telefon/Impressum/JSON-LD bleiben bei der Firmennummer.
- NRW-Team macht alles außer Foto/Video und Messebau. Messebau und Express nur Berlin.
  Ausnahme: In Essen gibt es eine Marketing-Kraft (Content, Video, „Gesicht“ für Kundenmarketing) – vom Inhaber am 17.10.2026 genannt.
- Hamburg (seit 23.10.2026, vom Inhaber bestätigt): eigenes Team vor Ort, **keine Adresse/Filiale**; Leistungen und Preise wie NRW
  (ohne Foto/Video, Messebau, Express). Seite `werbeagentur-hamburg.html` (Generator `tools/folien/hamburg_page.py`),
  Assistent `data-region="hamburg"`, Termin `?region=hamburg`, Region „Hamburg“ in den Anfragen. Genehmigung: bis 1 m²
  genehmigungsfrei nach Anlage 2 HBauO, sonst meist Baugenehmigung; zuständig ist das Bezirksamt.
- Keine Laternenwerbung anbieten.
- Genehmigung Werbeanlagen NRW: verfahrensfrei bis 1 m² (§ 62 Abs. 1 Nr. 12 BauO NRW, Flächen nebeneinander zusammengerechnet). Essen: Reklameaufsicht, Lindenallee 10, 45127 Essen, Tel. 0201 88-61114; Gestaltungssatzung Innenstadt in Aufstellung (seit 2025).
- Zahlung: Überweisung.
- Angebote (Inhaber, 27.10.2026): Anzahlung **immer 60 %**. Lieferzeit **3 Wochen nach Freigabe und Anzahlung nur bei Schildern/Leuchtreklame (Firmenschilder)** – bei Folien, Druck usw. keine 3 Wochen nennen (Inhaber, 04.11.2026).
- Sprachen der Beratung: Deutsch, Englisch, Arabisch, Türkisch (Türkisch vom Inhaber am 15.10.2026 bestätigt).
- Recht/Arbeitsweise (Inhaber, 05.11.2026): **keine eigene Werkstatt** behaupten – Masar hat ein Studio in Berlin-Wedding, gefertigt
  (Druck, Plott, Schilder, Folien) wird in einer **Partnerwerkstatt** (`tools/seo/partnerwerkstatt.py`); beleuchtete Anlagen bauen und
  montieren eingetragene Partnerbetriebe. Kunden: **B2B und Privatkunden** (AGB § 1, Widerrufsbelehrung § 8). Zahlung **60 % Anzahlung,
  40 % nach Lieferung/Montage** (7 Tage). **Keine Garantien** – nur gesetzliche Gewährleistung **2 Jahre** (AGB § 11). Inhaber hat
  Ausbildung als Mediengestalter (Abschluss vorhanden).

## Preise (netto, „ab“) – nur mit Freigabe ändern

Seit 05.11.2026 (Privatkunden, PAngV) steht neben jedem Netto-Preis automatisch der Bruttopreis: `tools/seo/brutto.py` (in `build_all.py`).
Preise im Text immer als netto schreiben, das Skript ergänzt „(… € brutto)“. Keine Reichweiten-Zahlen wie „70.000 Blickkontakte“ (ohne Quelle entfernt).

Leuchtbuchstaben (149/179 €) und Praxis-/Kanzleischild (290/339 €) seit 07.11.2026 nach Wettbewerbsvergleich gesenkt (Inhaber: „wie die Konkurrenz … mach das Passende“), Werkzeug `tools/seo/preise_2026_11.py` (einmalig), Berichte `docs/markt-2026-11/wettbewerb-*.md`.

Banner seit 03.11.2026 B2B-Preise (Inhaber: alte Preise ohne Gewinn); NRW-Werte im gleichen Abstand nach Marktrecherche. Werkzeug: `tools/seo/bannerpreise.py` (einmalig).

| Leistung | Berlin | NRW |
|---|---|---|
| Schilder | 45 € | 59 € |
| Tür-/Klingelschild | 69 € | 85 € |
| Firmenschild | 149 € | 179 € |
| Einzelbuchstaben | 119 € | 139 € |
| Acrylglasschild | 240 € | 289 € |
| Praxis-/Kanzleischild | 290 € | 339 € |
| Leuchtbuchstaben (je Buchstabe) | 149 € | 179 € |
| Schaufensterbeschriftung | 149 € | 179 € |
| Milchglas/Sichtschutz | 190 € | 229 € |
| Milchglas nach Maß | 240 € | 289 € |
| Aktionsfolie | 190 € | 229 € |
| Lochfolie (m²) | 45 € | 55 € |
| Fahrzeug-Teilbeschriftung | 290 € | 340 € |
| PVC-Banner (m²) | 29 € | 34 € |
| Mesh-Banner (m²) | 34 € | 39 € |
| Blockout-Banner (m²) | 42 € | 48 € |
| Banner-Mindestpreis | 79 € | 89 € |

Überall gleich: Logo ab 490 €, Social Media ab 490 €/Monat, LED-Neon innen ab 249 €.
Textildruck (Seite `textildruck-berlin.html`, Generator `tools/folien/textil_page.py`, 03.11.2026): nur Flex/Flock und DTF, **kein Stick**, Mindestbestellung 5 Stück;
T-Shirt ab 15 €, Polo ab 22 €, Hoodie ab 35 €, Stofftasche ab 8 €, eigene Textilien ab 7 €/Motiv (nach Marktrecherche); Berlin + Versand deutschlandweit.
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
- Telegram-Sekretär `inc/sekretaer.php` (Nachrichten auf Arabisch, ohne Personendaten): neue Anfrage/Termin
  mit Status-Tasten, Erinnerung 30 Min. vor Termin, Kunden-Erinnerungsmail 24 h vorher, „Wie war's?“ nach
  dem Termin, Tagesbericht 8 Uhr, Wochenbericht montags mit Vorschlägen (nur aus eigenen Zahlen).
  Befehle /heute /morgen /termine /offen /bericht /hilfe über Webhook `telegram.php` (Secret-Token +
  Chat-Prüfung). Zeitplan: `cron.php?k=…` per Hostinger-Cronjob alle 5 Min. (Schlüssel in Einstellungen).
- Kundenbindung: „Auf diesem Gerät merken“ (Häkchen, localStorage `masar-kunde`: Kontaktdaten + Anfragenummern)
  in Assistent und Terminbuchung → „Willkommen zurück“ und vorausgefüllte Felder. Anfrage-Status für Kunden:
  `status.html` + `status.js` + `status.php` (Nummer + Telefon/E-Mail, nur Status/Leistung/Ort/Termin,
  20 Abfragen/h je IP); Link in Bestätigungsmails, danke.html (?nr=), Terminbestätigung und Footer.
  Status in der Übersicht aktuell halten – Kunden sehen ihn. Seit 03.11.2026: Feld „Hinweis für den Kunden“ (auf der Status-Seite
  sichtbar), Kunde kann Termine > 2 h vorher auf status.html verschieben/absagen lassen (nur Wunsch:
  Spalte `termin_wunsch`, E-Mail + Telegram, Markierung in der Übersicht; Termin bleibt bis zur Bearbeitung).
  Erinnerungsmail 24 h vorher enthält den Status-Link. Keine zusätzlichen Status-E-Mails an Kunden (Inhaber, 03.11.2026).
- Abschluss-Animation `fertig.js` (auf allen Seiten): Ring 0→100 % gekoppelt an den echten Versand, dann Haken, „Danke!“, Anfragenummer, Farbregen. API `MasarFertig.start().done/fail`; genutzt in Assistent (WhatsApp-Knopf erst danach), Terminbuchung, danke.html und automatisch bei Formularen an /kontakt.php.
- Marke: Markenleitfaden `tools/brand/Masar_Markenleitfaden.pdf` (Navy #132E50, Teal #58D0BD, Teal dunkel #177567 für Teal-Text auf Weiß,
  Grau #D1D3D4, Off-White #F4F7F7, Text #1A2A2A; Barlow Condensed Black für Überschriften, Barlow für Text). Keine Gold-/Lila-Akzente;
  `tools/seo/marke.py` setzt das auf allen Seiten durch (am Ende der Pipeline ausführen). Claim (03.11.2026): **„Werbung, die man sieht.“** (Footer aller Seiten, E-Mail-Signatur).
- Lesbarkeit (03.11.2026, Inhaber): keine sichtbare Brotkrumen-Leiste (nur BreadcrumbList-JSON-LD), keine Silbentrennung/Trennstriche;
  zu lange Überschriften werden per Skript kleiner gesetzt, Bindestrich-Wörter in Überschriften nicht getrennt – `tools/seo/umbruch.py`
  (nach `marke.py` am Ende der Pipeline).
- KI-Leistungen (Inhaber, 03.11.2026): Chat- und WhatsApp-Assistent, Online-Termine mit Erinnerungen, E-Mails/Dokumente vorsortieren,
  dazu Marketing und Entwicklung – **keine Telefon-/Sprach-KI, keine Preise**. Seiten `ki-fuer-arztpraxen-berlin.html` und
  `ki-fuer-pflegedienste-berlin.html` (Generator `tools/folien/ki_pages.py`), Demo `ki-demo.js` (Chat im Hero `data-ki-demo="praxis|pflege"` mit freier Eingabe; Bausteine `data-ki-bausteine` = Online-Termin, Postfach, Unterlagen-Assistent; reine Vorführung),
  Ratgeber `blog/krankmeldung-pflegedienst-digital.html` (`tools/blog/ki_artikel.py`). Immer: KI-Hinweis (Art. 50 KI-VO, seit 02.08.2026),
  keine medizinische Beratung + Notfall 112/116 117, AV-Vertrag, § 203 StGB, EU-Hosting, WhatsApp nur Business Platform + Einwilligung;
  nicht „rechtssicher“/„zertifiziert“, keine Zeitersparnis-Zahlen. Akquise: keine Kalt-E-Mails (UWG § 7), Briefe per Post mit Art.-14/21-Hinweis.
- Marketing-Skills (Inhaber, 07.11.2026): 53 Skills aus github.com/coreyhaines31/marketingskills (MIT) in `.claude/skills/` (z. B. seo-audit, ai-seo, copywriting, cro, social, ads, local-relevante Ideen). Allgemein/SaaS-lastig – CLAUDE.md-Regeln gehen vor (keine Kalt-E-Mails, keine erfundenen Zahlen/Bewertungen, keine Garantien). `.claude/.htaccess` sperrt den Ordner auf dem Server.
- SEO/KI-Suche: JSON-LD `LocalBusiness` mit `@id https://masar-werbeagentur.de/#identity` in
  `index.html`, `llms.txt`, `sitemap.xml`, IndexNow über `/indexnow.php`, Seite `einsatzgebiete.html`
  (im Footer aller Seiten verlinkt).

## Getroffene Entscheidungen

- PVC-Banner-Städteseiten (Köln, Düsseldorf, Dortmund, Essen, Bochum) zu `pvc-banner-nrw.html`
  zusammengeführt (301 in `.htaccess`) – zu ähnlich (Doorway-Risiko). Keine neuen Städteseiten,
  die sich nur im Ortsnamen unterscheiden.
- Fensterfolie-Städteseiten (Köln, Düsseldorf, Dortmund, Essen, Bochum) am 24.10.2026 zu `fensterfolie-nrw.html`
  zusammengeführt (301 in `.htaccess`, 98 % gleicher Text). Die übrigen NRW-Städteseiten haben einen lokalen Abschnitt
  (`tools/seo/stadt_lokal.py`). Online-Preisrechner am 24.10.2026 auf Wunsch des Inhabers wieder entfernt – nicht neu einbauen.
- Umland-Seiten `werbeagentur-*` (Brandenburg + Herne, Mülheim, Bottrop) sind sich noch ähnlich –
  echte Projekte/Fotos je Stadt ergänzen, sobald vorhanden.

## Offen

- Phase 3: Angebote/Rechnungen aus der Anfragen-Übersicht; Phase 4: automatische Erinnerungen.
- Inhaber: `admin_pass_hash` und Telegram einrichten, E-Mail-Versand testen.

Kundennotizen (laufende Aufträge, Angebote) werden **nicht** hier, sondern privat geführt:
**Google Doc „Masar – Kundenkartei (privat)“** im Google Drive des Inhabers (Ordner „MASAR WERBEAGENTUR / Kunden & Belege (privat)“, darin „Masar – Belege (privat)“; seit 09.11.2026). Fragt der Inhaber nach einem
Kunden, zuerst dort nachlesen (Drive-Suche nach dem Titel); nach jedem neuen Angebot, Termin oder jeder Rechnung den Eintrag
dort ergänzen. Lokale Kopie nur in `tools/angebot/privat/KUNDENKARTEI.md` (nicht im Repository).
Seit 04.11.2026 aktuelle Fassung im selben Drive-Ordner: **„Masar – Kundenkartei (privat) – Stand 04.11.2026“** (Kundenkartei + Belegregister);
bei Änderungen eine neue Fassung „Stand <Datum>“ hochladen. Belegregister aller Angebote/Rechnungen (Nr., Datum, netto, brutto, Datei):
`python3 tools/angebot/privat/register.py` → `tools/angebot/privat/KUNDENREGISTER.md`. Fragt der Inhaber nach einem Kunden oder einer
Rechnung: Kundenkartei + Register lesen und alles zusammenfassen (Kontakt, Angebote, Rechnungen, Zahlungsstand, offene Punkte).
PDF-Sicherung aller Angebote/Rechnungen (Stand 04.11.2026) im Drive-Unterordner **„Masar – Belege (privat)“** als Masar_Belege_Teil1–6.zip
(Uploads von hier max. ca. 3 MB je Datei). Achtung: Der Cloud-Container ist flüchtig – privat/ geht verloren, wenn er neu startet; die PDFs müssen zusätzlich beim Inhaber liegen. **Seit 09.11.2026 (Inhaber verärgert über Datenverlust): jedes neue Angebot/jede Rechnung als PDF sofort in den Drive-Ordner „MASAR WERBEAGENTUR / Kunden & Belege (privat)“ hochladen und die Kundenkartei dort ergänzen (Nachtrag-Dokument), nicht erst am Ende.** Stempel muss nach einem Neustart neu vom Inhaber kommen (privat/stempel.png).

Belegablage (Inhaber, 09.11.2026): Vom Inhaber geschickte Belege getrennt im Drive-Ordner „MASAR WERBEAGENTUR / Kunden & Belege (privat)“ ablegen –
**Ausgaben/Eingangsrechnungen** → Unterordner „Ausgaben – Eingangsrechnungen (privat)“, **eigene Kundenrechnungen** → „Kundenrechnungen – Ausgangsrechnungen (privat)“.
Dateiname: `JJJJ-MM-TT_<Lieferant oder Kunde>_<Nr.>_<Betrag brutto>.pdf`. Auf Wunsch „gib mir die Belege“: je Ordner eine ZIP-Datei (Ausgaben.zip, Kundenrechnungen.zip) erzeugen und senden, optional nach Monat/Zeitraum.
**Nie Belege/Dateien im Drive löschen, verschieben in den Papierkorb oder überschreiben – nur auf ausdrücklichen Befehl des Inhabers (09.11.2026).** Korrigierte Fassungen als neue Datei daneben ablegen.
