# Marketing-Log (Website)

## 05.11.2026
- Saisonseite Schaufenster: Termine um Valentinstag (14.02.2027) und Ostern (28.03.2027) ergänzt, Raster 3 × 2.
- Saisonseite: „drei Wochen ab Freigabe“ entfernt (3 Wochen gelten nur für Schilder/Leuchtreklame, CLAUDE.md) → „Lieferzeit verbindlich mit dem Angebot“.
- Meta-Beschreibungen gekürzt (KI-Verordnung, Werbung auf Autoscheiben) – seo_check ohne Längen-Hinweis.
- Markt-Radar angelegt (`docs/markt-radar.md`).

## 05.11.2026 (Nacht, Marktrecherche mit 4 Agenten)
- Berichte: docs/markt-2026-11/ (Fehler & Kosten, Wettbewerber-Lücken, Suchnachfrage, Rechtsfallen).
- 6 neue Ratgeber (tools/blog/markt_ratgeber.py): Kundenstopper-Erlaubnis, Leuchtreklame-Kosten + 7 Prüfpunkte, Teure Fehler in der Werbung,
  Ladeneröffnung-Checkliste, Werbeschild am Mietobjekt, Google-Profil-Abzocke; Hinweis-Kästen auf 10 Leistungsseiten (tools/seo/ratgeber_hinweise.py).
- Ausweichschriften gegen CLS (tools/seo/schrift_fallback.py), Bruttopreis gleich groß wie netto, Kennzeichen auf Referenzfoto unkenntlich,
  Bußgeldangabe im Außenwerbung-Ratgeber mit Paragraf, Genehmigungs-FAQ Schaufenster/Außenwerbung präzisiert, Thermobruch-FAQ Sichtschutzfolie.

## 06.11.2026
- Hamburg-Seite: FAQ Genehmigung um Kundenstopper ergänzt (laut Stadt grundsätzlich nicht gestattet, Alternative Schaufenster).
- Bauzaunbanner-Ratgeber: Berlin – Gerüst-/Bauzaunwerbung seit 2010 nicht verfahrensfrei (Merkblatt BA Neukölln, Quelle ergänzt).
- Digital Signage: FAQ Preisverzeichnis am Eingang (§ 13 PAngV).

## 07.11.2026
- Hinweis-Kasten „Leasingrückgabe: Beschriftung richtig entfernen“ auf Fahrzeugbeschriftung Berlin/NRW, LKW-Beschriftung, Werbung Handwerker.
- Fahrzeugbeschriftung NRW: FAQ Handwerkerparkausweis (Quelle Stadt Köln).

## 07.–08.11.2026 (mit dem Inhaber)
- Preise Leuchtbuchstaben 149/179 €, Praxis-/Kanzleischild 290/339 € (Freigabe Inhaber), „Was im Preis enthalten ist“ auf drei Seiten.
- Neue Seiten: Ratgeber `blog/firmenschild-kosten-berlin.html`, `werbung-gastronomie-berlin.html`; Abschnitte Reparatur/LED-Umrüstung und Leuchtkasten/Ausleger (Leuchtreklame), Banner zur Neueröffnung; FAQs Kosten-/Eröffnungs-Ratgeber, NRW, Hamburg; FAQ beleuchtete Hausnummer.
- Liefer-/Zahlungs-FAQ auf 9 Seiten korrigiert, „eigener Plotter“ → Partnerwerkstatt; Startseite Leuchtlogo-Video; Referenz Türbeschriftung (Praxis).
- Eigenständige Kundenseite `/destadsmuur/` (noindex, von der Pipeline ausgenommen).

## 09.11.2026
- Interne Links zu den neuen Seiten: Gastronomie-Seite von Leuchtreklame, Print, Digital Signage und Werbetechnik; Firmenschild-Kosten-Ratgeber von Schilder Berlin und Werbetechnik (`tools/seo/ratgeber_hinweise.py`).

## 10.11.2026
- Saisonseite Schaufenster Black Friday & Weihnachten: FAQ „Rabatt-Angaben auf dem Schaufenster“ mit § 11 PAngV (Quelle) inkl. FAQPage-JSON-LD.

## 10.11.2026 (Technik-Audit)
- Vollprüfung aller 185 Seiten (mobil + Desktop): keine Konsolenfehler, keine 404, kein Überlauf, axe ohne Verstöße auf 20 Kernseiten, interne Links/Anker/Canonicals/JSON-LD in Ordnung; Assistent, Terminbuchung, Status, Werkzeuge laden fehlerfrei.
- Ladezeit: Startseite mobil 3,1 MB → 1,1 MB (Video 640×800, lädt erst bei Sichtbarkeit), Referenzen 2,5 MB → 0,5 MB (720er-Vorschauen), Umland-Seiten 0,8 → 0,4 MB (Kategorie-Bilder neu komprimiert, 3,7 → 2,4 MB gesamt).
- Lesbarkeit: Kacheltext 11 → 12,5 px (10 Seiten), Footer-Links Mindestgröße, zwei Hero-Bilder mit srcset.
- Startseite mobil: Anfrage-Tasten auf dem ersten Bildschirm (vor den Zusagen), Überschrift 33 px; LocalBusiness-Schema um Beratungssprachen ergänzt; Arbeitsliste Verzeichnis-Einträge (docs/markt-2026-11/verzeichnisse-eintraege.md).

## 11.11.2026 (Marketing-Runde)
- Marktbeobachtung: kein Berliner Werbetechnik-Wettbewerber mit Black-Friday-/Weihnachts-Aktion online (Saisonseite bleibt Alleinstellung); niedrige Bewertungsfrequenz der Wettbewerber → Bewertungsbitte als Chance (docs/markt-radar.md).
- `blog_kurzbox.py`: Angebotsbox übernimmt jetzt den Beschreibungssatz des jeweiligen Ratgebers aus der `.article-cta` statt des festen „Gestaltung, Fertigung und Montage“ – passt nun auch zu KI-, Textildruck- und Logo-Ratgebern (Punkt 7 aus wettbewerb-2026-11.md, 69 Ratgeber).
- Dortmund-Infoblatt-URL vereinheitlicht: `stadt_ratgeber.py` auf `infoblatt_werbeanlagen.pdf` (per Websuche als aktuelle Fassung bestätigt) statt der veralteten `informationsblatt-werbeanlagen.pdf` (Punkt 6 aus wettbewerb-2026-11.md); Seite werbeanlage-dortmund neu erzeugt.

## 12.11.2026 (Marketing-Runde)
- Saison Grüne Woche (15.–24.01.2027): Hinweis-Kasten „Gut zu wissen“ verlinkt jetzt `messestand-berlin-2027.html` von PVC-Banner Berlin, Print, Werbetechnik und Messebeschriftung (neu mit Kasten); `textildruck-berlin.html` von Fahrzeugbeschriftung Berlin, Werbung Handwerker, Print und Messebeschriftung (`tools/seo/ratgeber_hinweise.py`). Eingehende Links: Messestand 4 → 8, Textildruck 5 → 8.
