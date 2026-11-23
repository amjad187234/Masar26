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

## 13.11.2026 (Marketing-Runde)
- Saison Black Friday/Weihnachten (noch 2 Wochen): Hinweis-Kasten verlinkt die Saisonseite jetzt auch von `werbetechnik.html`, `werbung-gastronomie-berlin.html` und `werbung-kosmetikstudio-berlin.html` (beide neu mit Kasten, dazu Eröffnungs-Checkliste) – `tools/seo/ratgeber_hinweise.py`. Eingehende Links Saisonseite: 8 → 11.

## 13.11.2026 (mit dem Inhaber)
- Startseite: Leuchtlogo-Video aus dem Kopfbereich entfernt, Logo wieder eingesetzt.
- Referenzen: Foto „LED-Neonbuchstaben in der Fertigung“ entfernt; neu: 3D-Buchstaben über einem Saaleingang, The B-Side Events (Ausleger an der Fassade, montiert – vom Inhaber bearbeitetes Foto).
- Korrektur Fahrschule JAD: nur die Schaufensterfolie ist von uns – Foto in „Schaufenster & Folien“ verschoben, auf Leuchtreklame-/Außenwerbung-Seiten ersetzt, Werbevideo Leuchtreklame ohne diese Szene neu gerendert (Video-URLs `?v=2`).
- CRAVÉZ-Werbevideo beginnt direkt mit der Cookie-Szene (Vorspann mit Bildfehlern entfernt, 24 s).

## 14.11.2026 (Marketing-Runde)
- Saison Firmenfeiern: Hinweis-Kasten verlinkt den Ratgeber „Fotowand für die Firmenfeier“ jetzt von der Saisonseite (neu mit Kasten), Express-Druck (neu), Print und Messebeschriftung – `tools/seo/ratgeber_hinweise.py`. Eingehende Links: 3 → 7.

## 16.11.2026 (Marketing-Runde)
- `praxisbeschilderung-berlin.html`: neue FAQ „Wir übernehmen eine bestehende Praxis. Was muss an der Beschilderung geändert werden?“ (sichtbar und im FAQPage-JSON-LD, Link zum Ratgeber Praxisschild: Regeln & Kosten) – Anlass: viele Praxisübernahmen in Berlin (docs/markt-radar.md).

## 17.11.2026 (Marketing-Runde)
- `schaufensterbeschriftung-berlin.html`: neue FAQ „Kann eine Schaufensterbeschriftung auch im Winter montiert werden?“ (sichtbar und im FAQPage-JSON-LD; innen ganzjährig, außen trocken und laut Herstellerdatenblättern über +8 °C) – Saisonfrage vor Winterterminen (docs/markt-radar.md).

## 18.11.2026 (Marketing-Runde)
- Saison Januar-Sale: `schaufenster-weihnachten-black-friday.html` – neue FAQ „Wann beginnt der Winterschlussverkauf 2027?“ (sichtbar und im FAQPage-JSON-LD; kein gesetzlicher Termin, traditionell letzter Montag im Januar = 25.01.2027) – docs/markt-radar.md.

## 19.11.2026 (Marketing-Runde)
- `leuchtreklame-berlin.html`: neue FAQ „Können Sie ein vorhandenes Leuchtschild mit neuem Namen bekleben?“ (sichtbar und im FAQPage-JSON-LD; alte Folie entfernen, neues Motiv auf lichtdurchlässiger Folie, Gehäuse und Beleuchtung bleiben, Prüfung vor Ort; kein Preis) – Anlass: Anfragen nach Geschäftsübernahmen (docs/markt-radar.md).

## 20.11.2026 (Marketing-Runde)
- `express-druck-berlin.html`: neue FAQ „Kann ich einen Logo-Folienplott zur Selbstmontage abholen, zum Beispiel für ein Event?“ (sichtbar und im FAQPage-JSON-LD; Plott entgittert mit Übertragungsfolie, Vektordatei, ablösbare Folie auf Wunsch; kein Preis) – Anlass: kurzfristige Event-Anfrage (docs/markt-radar.md).

## 21.11.2026 (Marketing-Runde)
- `schaufensterbeschriftung-berlin.html`: neue FAQ „Bekleben Sie Schaufenster auch vor einer Neueröffnung („Opening Soon“)?“ (sichtbar und im FAQPage-JSON-LD; vollflächige Abdeckung während des Umbaus, Schriftzug, Entfernen zur Eröffnung auch in zwei Schritten; Berlin, NRW, Hamburg; kein Preis) – docs/markt-radar.md.

## 22.11.2026 (mit dem Inhaber)
- Neue Zielgruppen-Seite `schaufensterfolie-store-eroeffnung.html` („Schaufensterfolie zur Store-Eröffnung – Opening Soon“): für Marken, Filialisten, Visual Merchandising und Ladenbau; Leistung, Ablauf, Checkliste „Was wir vorab brauchen“, englischer Abschnitt für internationale Marken, 7 FAQ (FAQPage), Service-Schema, Vorschaubild. Generator `tools/folien/store_eroeffnung_page.py`.
- Verlinkt aus Hinweis-Kästen auf Schaufensterbeschriftung Berlin, Saisonseite, Werbeagentur Hamburg und NRW sowie aus der FAQ „Opening Soon“; eingetragen in sitemap.xml und llms.txt. Nicht in der Navigation.
- Bilder der neuen Seite auf Wunsch des Inhabers ersetzt: statt Referenzfotos zwei eigene Illustrationen mit Beispielmarke (Front vor der Eröffnung; „Eine Front, drei Phasen“), auch im Vorschaubild. Echte Projektfotos folgen erst nach Zustimmung des Kunden.

## 23.11.2026 (Marketing-Runde)
- Interne Links zur neuen Seite `schaufensterfolie-store-eroeffnung.html`: Hinweis-Kasten jetzt auch auf Werbetechnik, Außenwerbung Berlin, Sichtschutzfolie Berlin und Schaufensterbeschriftung NRW (`tools/seo/ratgeber_hinweise.py`). Eingehende Links: 4 → 8.

## 23.11.2026 (mit dem Inhaber)
- WhatsApp überall auf die Firmennummer 0178 514 3918 umgestellt: 32 NRW-Seiten, Anfrage-Assistent, Terminbuchung, Leuchtbuchstaben-Konfigurator und Genehmigungs-Check (vorher Nummer des NRW-Teams). `tools/seo/nrw_whatsapp.py` hält das fest; Skript-Versionen erhöht (assistent.js v14, termin.js v11, konfigurator.js v3, genehmigung.js v2).
- Referenz Oscar Jacobson, Hamburg (Erlaubnis des Kunden vom 23.11.2026, Fotos vom Inhaber): fünf bearbeitete Projektfotos auf `referenzen.html` (Schaufenster & Folien, an erster Stelle), `werbeagentur-hamburg.html` („Aus unserem Projekt in Hamburg“ statt Berliner Beispielen), erstes Bild auf Schaufensterbeschriftung und Fensterfolie Berlin; auf `schaufensterfolie-store-eroeffnung.html` ersetzen die Fotos die Illustrationen (Hero, Projektkasten, Vorschaubild), die Phasen-Grafik bleibt beim Ablauf.
- Projektvideo Oscar Jacobson, Hamburg: aus drei Handyvideos des Inhabers ein 14-Sekunden-Clip (hochkant, ohne Ton; Übertragungsfolie wird vom Schriftzug abgezogen) – `videos/folienplott-store-hamburg.mp4` + Standbild. Eingebaut als „Projekt im Fokus“ oben auf `referenzen.html` und auf der Store-Eröffnungsseite. Das Projekt steht jetzt als erste Karte in allen 13 „Aus unserer Arbeit“-Blöcken (Leuchtreklame, Fahrzeuge, Druck, Werbetechnik, NRW, Hamburg, Schaufenster, Fensterfolie).
