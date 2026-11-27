# KI-Sichtbarkeit Masar – Fallbeispiel

Ziel: Masar Werbeagentur soll in KI-Antworten (ChatGPT, Perplexity, Google AI Overviews/Gemini, Copilot, Claude) erscheinen.
Das Projekt dient zugleich als dokumentiertes Beispiel für eine spätere Leistung „KI-Sichtbarkeit für lokale Betriebe“.
Keine Garantien: Ob eine KI ein Unternehmen nennt, kann niemand zusagen. Gemessen wird nur, was sich beobachten lässt.

## Ausgangslage (Baseline, 27.11.2026)

Messung über Websuche (gleiche Datenbasis, die KI-Suchen nutzen); KI-Chats selbst sind aus dem Container nicht abfragbar.

| Suche | Masar gefunden? | Was stattdessen erscheint |
|---|---|---|
| „Masar Werbeagentur“ Berlin (Markenname) | nein | eine andere Agentur „MASAR / مسار“ aus Bagdad (DesignRush), allgemeine Agentur-Listen |
| Werbeagentur Berlin Wedding Schilder Leuchtreklame Schaufensterbeschriftung | nein | Behrendt Werbetechnik (Wedding), Verzeichnisse (Gelbe Seiten, kennstdueinen, sellwerk, goyellow) |
| Schaufensterfolie Opening Soon Store-Eröffnung Berlin Hamburg | nein | Online-Shops (myfolie), MBE, hamburg.de-Branchenbuch |

**Befund:**
1. Selbst der Markenname führt nicht zur Website → Markenwiedererkennung (Entität) fehlt; Verwechslungsgefahr mit „MASAR“ Bagdad.
2. Die Technik der Website ist gut (robots.txt lässt alle KI-Crawler zu, llms.txt mit Preisen, LocalBusiness-Schema mit @id, FAQ-Schema auf vielen Seiten, Sitemap, IndexNow).
3. Es fehlt die **Präsenz außerhalb der Website**: KI-Antworten für lokale Anbieter stützen sich stark auf Verzeichnisse, Kartenprofile und Bewertungen. Masar ist dort kaum vertreten (Arbeitsliste `docs/markt-2026-11/verzeichnisse-eintraege.md`, Stand 27.11. alle offen).

## Umgesetzt auf der Website

| Datum | Änderung |
|---|---|
| 27.11.2026 | `ueber-uns.html`: Abschnitt „Auf einen Blick“ – ein Absatz, der Masar als Firma eindeutig beschreibt (Name, Adresse, Leistungen, Fertigung über Partnerwerkstatt) plus Faktenliste (Inhaber, Standort, Einsatzgebiet, Sprachen, Preise, Kontakt, Stand-Datum). |
| 27.11.2026 | `index.html` LocalBusiness-Schema: `alternateName` („Masar“, „Masar Werbeagentur Berlin“) und `slogan` („Werbung, die man sieht.“). |

## Außerhalb der Website (Inhaber, wichtigster Hebel)

Reihenfolge nach Wirkung, Firmendaten überall exakt gleich (siehe Verzeichnis-Arbeitsliste):
1. **Google Unternehmensprofil** vollständig: alle Leistungen, Fotos echter Projekte, Öffnungszeiten, Beiträge.
2. **Bing Places** – Bing-Daten speisen Copilot und die ChatGPT-Suche.
3. **Apple Business Connect**.
4. **Bewertungen echter Kunden** (ohne Gegenleistung) auf Google; zufriedene Firmenkunden der letzten Wochen gezielt freundlich fragen.
5. Gelbe Seiten, Das Örtliche, 11880, Cylex, wlw.
6. **LinkedIn-Unternehmensseite** und Instagram/Facebook mit identischen Daten; Profil-URLs danach in `sameAs` im Schema ergänzen.
7. Echte Nennungen von Partnern und Kunden (z. B. Projektseiten, Partnerlisten).

## Monatliche Messung

Jeden Monat dieselben Fragen in ChatGPT (mit Suche), Perplexity und Google stellen, je 3-mal, und notieren: genannt ja/nein, welche Quelle, welche Mitbewerber.

1. Welche Werbeagentur in Berlin-Wedding macht Firmenschilder?
2. Wer macht Schaufensterbeschriftung in Berlin?
3. Leuchtreklame für mein Geschäft in Berlin – wen kann ich fragen?
4. Fahrzeugbeschriftung Berlin Anbieter
5. Praxisschild Berlin – wer fertigt das?
6. Schaufensterfolie für eine Store-Eröffnung (Opening Soon) in Berlin oder Hamburg
7. Werbeagentur in Berlin mit Beratung auf Arabisch
8. Werbetechnik Berlin mit Beratung auf Türkisch
9. Brauche ich eine Genehmigung für ein Werbeschild in Berlin?
10. Was ist Masar Werbeagentur?
11. Masar Werbeagentur Berlin Erfahrungen
12. Fotowand mit Ausschnitt für ein Firmenevent in Berlin

| Monat | genannt (von 36 Abfragen je Plattform) | Bemerkung |
|---|---|---|
| Nov. 2026 | Baseline per Websuche: 0 von 3 Testsuchen | siehe oben |
