# Audit KI-Suche und technische SEO – 27.11.2026

Ziel: bessere Sichtbarkeit, Zitate und Empfehlungen in ChatGPT Search, Google AI Mode / AI Overviews, Gemini,
Perplexity, Claude und Copilot – vor allem für Suchen ohne Markennamen (Werbeagentur Berlin, Werbetechnik Berlin,
Leuchtreklame Berlin, Fahrzeugbeschriftung Berlin).

Keine Zusage, dass eine KI Masar nennt. Nichts erfunden: keine Bewertungen, Projekte, Zahlen oder Profile.

## Grenzen dieser Prüfung

- Die Live-Website war aus der Arbeitsumgebung nicht erreichbar (Netzwerkregel). Geprüft wurde der Code im
  Repository, nicht die Auslieferung über Hostinger. Firewall/CDN, Antwortzeiten und echte Core Web Vitals
  sind deshalb **nicht gemessen** – siehe „Offen“.
- Offizielle Dokumentation: Anthropic direkt gelesen. Google, OpenAI, Perplexity und Bing ließen sich von hier
  nicht öffnen; deren Aussagen stammen aus Suchtreffern zu den offiziellen Seiten und aus Fachpresse. Vor
  weitreichenden Entscheidungen die verlinkte Originalseite lesen.

## Vorher / Nachher

| Bereich | Vorher | Nachher |
|---|---|---|
| Firmen-Datensatz (JSON-LD) | `LocalBusiness` mit `@id …/#identity`, `sameAs` (Instagram, Facebook), Katalog mit 9 Preisen; Inhaber ohne eigene @id, Titel „Geschäftsführer“ | zusätzlich `WebSite`-Knoten (`#website`), Inhaber als `Person` mit `@id …/#inhaber` („Inhaber, Mediengestalter“), Katalog mit 20 Listenpreisen |
| Widersprüche zwischen Seiten | 17 Seiten trugen im `provider` eigene Kopien von Öffnungszeiten, Gebiet, Bildern (teils abweichend) | `provider` überall nur noch Verweis auf `#identity` (Typ, Name, URL, Telefon, Adresse) |
| Vorschau-Rechte | 77 Seiten „index, follow“, 101 ohne Angabe | 176 indexierbare Seiten mit `max-snippet:-1, max-image-preview:large, max-video-preview:-1` |
| IndexNow | von Hand: nach jedem Bereitstellen `/indexnow.php` öffnen | automatisch über `cron.php`, sobald `sitemap.xml` neu ist; Handaufruf bleibt |
| `llms-full.txt` | FAQ-Fragen fehlten (standen in Knöpfen), Aufruf-Texte enthalten | Fragen als Überschrift vor der Antwort, Knopf-Texte entfernt |
| Suchabsicht „Was kostet eine Werbeagentur in Berlin?“ | auf keiner Seite beantwortet | FAQ auf der Startseite (sichtbar + `FAQPage`), nur Listenpreise |
| Messung | keine | `tools/seo/ki_logs.py`: Crawler-Abrufe und Besuche aus KI-Antworten aus dem Server-Protokoll |
| `robots.txt` | alle Crawler erlaubt | unverändert in den Regeln; Kommentar erklärt die Absicht |
| JSON-LD gesamt | 469 Blöcke | 469 + 1 (`WebSite`), alle gültig |

Prüfungen nach dem Umbau: `build_all.py --dry` 0 Änderungen · `check_site.py` keine Befunde ·
`seo_check.py` 187 Seiten, 178 indexierbar, 0 Fehler, 20 Hinweise (alle „ähnlich“, siehe Offen) ·
alle JSON-LD-Blöcke gültig · Startseite, Leuchtreklame, Über uns im Browser (mobil) ohne Fehler und ohne
seitliches Scrollen · `php -l` für `inc/indexnow.php`, `indexnow.php`, `cron.php` · `indexnow.php?test=1` läuft.

## Was offiziell gestützt ist und was Versuch

**Offiziell dokumentiert**

- Google: Für AI Overviews und AI Mode gelten die normalen Voraussetzungen der Suche (indexierbar, Snippet
  erlaubt); keine eigene Auszeichnung, keine Sonderdatei. Steuerung über `nosnippet`, `max-snippet`,
  `Google-Extended`. Messung in der Search Console im normalen Web-Bericht.
- OpenAI: `OAI-SearchBot` (Suche), `GPTBot` (Training), `ChatGPT-User` (Abruf auf Nutzerwunsch) – getrennt
  steuerbar; Änderungen an robots.txt wirken nach rund 24 Stunden.
- Anthropic: `Claude-SearchBot` (Suche), `Claude-User` (Nutzerabruf), `ClaudeBot` (Training); alle beachten
  robots.txt, `Crawl-delay` wird unterstützt.
- Perplexity: `PerplexityBot` (Index, beachtet robots.txt), `Perplexity-User` (Nutzerabruf).
- IndexNow (Bing, Yandex u. a.), `LocalBusiness`/`Organization`/`WebSite`-Auszeichnung, Sitemaps mit `lastmod`.

Stand auf der Website: alle genannten Crawler sind erlaubt (Wildcard), Trainings-Crawler ebenfalls – unverändert.

**Versuch / ohne Zusage eines Anbieters**

- `llms.txt`, `llms-full.txt`, `preise.md`: Google nutzt sie laut eigener Aussage nicht für die Suche. Sie
  bleiben, weil Assistenten und Agenten sie beim direkten Abruf lesen können und sie nichts kosten.
- Markdown-Auslieferung per `Accept: text/markdown`: **nicht umgesetzt**. Auf dem Hostinger-Cache wäre das
  Risiko, dass Besucher Markdown statt der Seite sehen, größer als der belegte Nutzen. Ersatz: `llms-full.txt`.
- WebMCP: **nicht umgesetzt**. Laut Fachpresse nur Chrome-Testphase (Origin Trial), API noch in Bewegung,
  kein Browser schaltet es standardmäßig ein. Wieder prüfen, wenn es stabil ist – Kandidat wäre der Anfrage-Assistent.
- `FAQPage`: bleibt als Auszeichnung der sichtbaren Fragen; ein besonderes Suchergebnis dafür ist für
  Firmenseiten nicht zu erwarten.

## Geänderte Dateien

- Neu: `tools/seo/entitaet.py`, `tools/seo/vorschau.py`, `tools/seo/ki_logs.py`, `inc/indexnow.php`, dieses Dokument
- Geändert: `indexnow.php`, `cron.php`, `robots.txt` (nur Kommentar), `tools/seo/ki_dateien.py`,
  `tools/build_all.py`, `tools/README.md`, `index.html` (Schema, FAQ), `llms-full.txt`
- Durch die Pipeline: 176 Seiten (Robots-Angabe), davon 17 mit gekürztem `provider`

## Offen – braucht den Inhaber, ein Konto oder Zugangsdaten

1. **Bereitstellen** in Hostinger. Danach einmal `/indexnow.php` öffnen oder prüfen, dass der Cronjob läuft.
2. **Erreichbarkeit für Crawler live prüfen**: Server-Protokoll bei Hostinger laden und
   `python3 tools/seo/ki_logs.py access.log` ausführen. Bekommt ein Crawler 403/429, sperrt Hostinger/CDN ihn.
3. **Google-Unternehmensprofil**: vorhanden (Bewertungslink `/google-bewertung`). Fehlt im Schema: die
   Karten-Adresse des Profils für `sameAs`/`hasMap` – bitte den „Teilen“-Link des Profils schicken.
   Profil vollständig halten: Leistungen, Fotos echter Projekte, Öffnungszeiten wie auf der Website.
4. **Bing Places** und **Apple Business Connect** anlegen (gleiche Schreibweise: Masar Werbeagentur,
   Bristolstraße 19E, 13349 Berlin, 0178 514 3918). **Bing Webmaster Tools** und **Search Console** für die Messung.
5. **Bewertungen** echter Kunden auf Google; **Verzeichnisse** (Gelbe Seiten, Das Örtliche, 11880, Cylex, wlw),
   LinkedIn-Unternehmensseite. Jede neue Profil-Adresse kommt danach in `sameAs`.
6. **Dresden**: steht im Leistungsgebiet von 19 Seiten, aber nicht im Firmen-Datensatz, in den Einsatzgebieten
   und in `llms.txt`. Widerspruch – Entscheidung des Inhabers (schon in CLAUDE.md offen).
7. **Umland-Seiten** `werbeagentur-*` (83–87 % gleicher Text): Zusammenführen empfohlen, braucht Freigabe (URL-Änderung).
8. **Core Web Vitals** aus echten Nutzerdaten (Search Console / PageSpeed) – von hier nicht messbar.

## Plan nach Wirkung

1. Bereitstellen, Protokoll prüfen (Punkte 1–2) – ohne das wirkt nichts davon.
2. Unternehmensprofil pflegen, Bing Places, Apple (3–4) – bei lokalen Fragen die wichtigste Quelle der Assistenten.
3. Bewertungen und Verzeichnisse (5) – unabhängige Nennungen.
4. Dresden und Umland-Seiten entscheiden (6–7).
5. Monatlich messen: die 12 Fragen in `docs/ki-sichtbarkeit.md`, dazu `ki_logs.py` und Search Console.
6. Je Quartal WebMCP und Markdown-Auslieferung neu bewerten.

## Quellen

- Google, AI features and your website: https://developers.google.com/search/docs/appearance/ai-features
- Google, Optimizing your website for generative AI features: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- Google, Top ways to ensure your content performs well in AI experiences: https://developers.google.com/search/blog/2025/05/succeeding-in-ai-search
- OpenAI, Overview of OpenAI Crawlers: https://developers.openai.com/api/docs/bots
- Anthropic, Crawler: https://support.claude.com/en/articles/8896518-anthropic-crawlers (direkt gelesen)
- Search Engine Journal zu Anthropics Crawlern: https://www.searchenginejournal.com/anthropic-claude-bots-robots-txt-ai-decisions/568253/
- Perplexity-Crawler (Sekundärquelle): https://mbsearch.co/blog/perplexity-crawlers/
- llms.txt und Google (Sekundärquelle): https://llmstxt.studio/docs/what-google-says-about-llmstxt
- WebMCP-Stand (Sekundärquellen): https://www.spronta.com/blog/state-of-webmcp-july-2026/ · https://mcpplaygroundonline.com/blog/what-is-webmcp
