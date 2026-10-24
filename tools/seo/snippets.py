"""Suchergebnis-Snippets (Titel + Beschreibung) für Seiten mit vielen Impressionen, aber wenig Klicks.

Grundlage: Search-Console-Export vom 24.10.2026. Regeln: Titel ≤ 60 Zeichen (Suchbegriff vorne,
dann Nutzen/Preis), Beschreibung 120–158 Zeichen mit „ab“-Preis aus der Preisliste, Ort und Handlungsaufforderung.
Nur Preise und Zusagen, die auch auf der Seite stehen. Nach dem Neu-Erzeugen von Seiten erneut ausführen:
    python3 tools/seo/snippets.py          (--dry zeigt nur Längen)
"""
import os, re, sys, html

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

S = {
 'index.html': ('Werbeagentur Berlin: Schilder, Leuchtreklame & Folie | Masar',
   'Werbetechnik aus Berlin-Wedding: Schilder ab 45 €, Leuchtreklame, Fahrzeug- und Schaufensterbeschriftung. Festpreis nach Fotos, Angebot in 24 h.'),
 'werbetechnik.html': ('Werbetechnik Berlin: Schilder, Leuchtreklame & Montage',
   'Werbetechnik für Berliner Firmen: Schilder ab 45 €, Leuchtbuchstaben ab 199 €, Fahrzeug- und Schaufensterbeschriftung – Entwurf, Fertigung, Montage.'),
 'fahrzeugbeschriftung-berlin.html': ('Fahrzeugbeschriftung Berlin ab 290 € | Transporter & Flotte',
   'Auto, Transporter oder ganze Flotte in Berlin beschriften lassen: Entwurf inklusive, Montage in unserer Werkstatt im Wedding, Festpreis nach Fotos.'),
 'fensterfolie-berlin.html': ('Fensterfolie Berlin: Sonnen- & Sichtschutz ab 190 € | Masar',
   'Fensterfolie in Berlin anbringen lassen: Sonnenschutz, Sichtschutz ab 190 €, Spiegel- und Sicherheitsfolie – mit Glasprüfung, Montage und Festpreis.'),
 'pvc-banner-berlin.html': ('Banner drucken Berlin: PVC-Banner ab 19 €/m² | Masar',
   'PVC-, Mesh- und Blockout-Banner in Berlin drucken lassen: ab 19 €/m² netto, wetterfest, mit Ösen – Gestaltung und Montage auf Wunsch. Angebot in 24 h.'),
 'aussenwerbung-berlin.html': ('Außenwerbung Berlin: Fassade & Leuchtreklame | Masar',
   'Außenwerbung in Berlin aus einer Hand: Leuchtbuchstaben ab 199 €, Fassadenschilder und Banner – mit Genehmigungs-Check und Montage. Angebot in 24 h.'),
 'leuchtreklame-berlin.html': ('Leuchtreklame Berlin: Leuchtbuchstaben ab 199 € | Masar',
   'Leuchtreklame in Berlin: LED-Leuchtbuchstaben ab 199 € je Buchstabe, Leuchtkästen und LED-Neon ab 249 € – Entwurf, Genehmigung und Montage.'),
 'messebau-berlin.html': ('Messebau Berlin: Messestand planen & bauen lassen | Masar',
   'Messebau in Berlin: Konzept, 3D-Entwurf, Standbau, Messegrafik sowie Auf- und Abbau aus einer Hand – für Messen in Berlin und Brandenburg.'),
 'sicherheitsfolie-berlin.html': ('Splitterschutz- & Sicherheitsfolie Berlin | Masar',
   'Sicherheitsfolie in Berlin: Splitterschutz für Glastüren und Glaswände, durchwurfhemmende Folie fürs Erdgeschoss – Beratung zu Prüfklassen und Montage.'),
 'sichtschutzfolie-berlin.html': ('Sichtschutzfolie Berlin: Milchglas ab 190 € | Masar',
   'Sichtschutzfolie in Berlin: Milchglas, Streifen, Spiegelfolie oder Dekor mit Logo – für Büro, Praxis, Bad und Erdgeschoss. Ab 190 € netto, Angebot in 24 h.'),
 'foliendruck-berlin.html': ('Foliendruck Berlin: Aufkleber & Klebefolie | Masar',
   'Foliendruck in Berlin: Aufkleber, Klebefolie, Bodenaufkleber und Fensterfolie ab 45 € – wetterfest und in Ihrem Design. Angebot in 24 h.'),
 'praxisbeschilderung-berlin.html': ('Praxisschilder Berlin: Schild, Tür & Sichtschutz | Masar',
   'Praxisschild, Türschild, Sprechzeiten und Sichtschutz am Fenster für Arzt- und Therapiepraxen in Berlin – gestaltet und montiert. Pakete ab 699 € netto.'),
 'werbetechnik-potsdam.html': ('Werbetechnik Potsdam: Schilder & Leuchtreklame | Masar',
   'Werbetechnik in Potsdam: Schilder ab 45 €, Leuchtreklame, Schaufenster- und Fahrzeugbeschriftung – Werbesatzung geprüft, Montage vor Ort. Angebot in 24 h.'),
 'werbeagentur-koeln.html': ('Werbeagentur Köln: Schilder, Leuchtreklame & Folie | Masar',
   'Werbetechnik in Köln mit Team vor Ort: Firmenschilder ab 179 €, Leuchtbuchstaben ab 229 €, Schaufenster und Fahrzeuge – Werbesatzung geprüft.'),
 'werbeagentur-duesseldorf.html': ('Werbeagentur Düsseldorf: Schilder & Leuchtreklame | Masar',
   'Werbetechnik in Düsseldorf mit Team vor Ort: Firmenschilder ab 179 €, Leuchtbuchstaben ab 229 €, Schaufenster und Fahrzeuge. Angebot in 24 h.'),
 'werbeagentur-dortmund.html': ('Werbeagentur Dortmund: Schilder & Leuchtreklame | Masar',
   'Werbetechnik in Dortmund mit Team vor Ort: Firmenschilder ab 179 €, Leuchtbuchstaben ab 229 €, Schaufenster und Fahrzeuge. Angebot in 24 h.'),
 'werbeagentur-essen.html': ('Werbeagentur Essen: Schilder & Leuchtreklame | Masar',
   'Werbetechnik in Essen mit Team vor Ort: Firmenschilder ab 179 €, Leuchtbuchstaben ab 229 €, Schaufenster und Fahrzeuge. Angebot in 24 h.'),
 'werbeagentur-bochum.html': ('Werbeagentur Bochum: Schilder & Leuchtreklame | Masar',
   'Werbetechnik in Bochum mit Team vor Ort: Firmenschilder ab 179 €, Leuchtbuchstaben ab 229 €, Schaufenster und Fahrzeuge. Angebot in 24 h.'),
 'werbeagentur-nrw.html': ('Werbeagentur NRW: Schilder, Leuchtreklame & Folie | Masar',
   'Werbetechnik in ganz NRW mit eigenem Team vor Ort: Schilder ab 59 €, Leuchtbuchstaben ab 229 €, Schaufenster- und Fahrzeugbeschriftung. Angebot in 24 h.'),
 'schilder-koeln.html': ('Schilder Köln: Firmenschild ab 179 € | Masar',
   'Schilder in Köln: Firmenschilder ab 179 € netto, Praxis-, Tür- und Klingelschilder aus Alu-Dibond, Acryl und Edelstahl – gefertigt und vor Ort montiert.'),
 'leuchtreklame-koeln.html': ('Leuchtreklame Köln: Leuchtbuchstaben ab 229 € | Masar',
   'Leuchtreklame in Köln: LED-Leuchtbuchstaben ab 229 € netto, Leuchtkästen und Ausleger – Werbesatzung geprüft, Montage durch unser Team vor Ort.'),
 'fensterfolie-koeln.html': ('Fensterfolie Köln: Sicht- & Sonnenschutz ab 229 € | Masar',
   'Fensterfolie in Köln: Sonnenschutz gegen Hitze, Sichtschutz ab 229 € netto, Spiegel- und Sicherheitsfolie – mit Glasprüfung und Montage vor Ort.'),
 'fensterfolie-duesseldorf.html': ('Fensterfolie Düsseldorf: Sichtschutz ab 229 € | Masar',
   'Fensterfolie in Düsseldorf: Sonnenschutz gegen Hitze, Sichtschutz ab 229 € netto, Spiegel- und Sicherheitsfolie – mit Glasprüfung und Montage vor Ort.'),
 'schaufensterbeschriftung-duesseldorf.html': ('Schaufensterbeschriftung Düsseldorf ab 179 € | Masar',
   'Schaufensterbeschriftung in Düsseldorf ab 179 € netto: Logo, Öffnungszeiten, Milchglas und Lochfolie für Läden und Praxen – vor Ort montiert.'),
 'schaufensterbeschriftung-bochum.html': ('Schaufensterbeschriftung Bochum ab 179 € | Masar',
   'Schaufensterbeschriftung in Bochum ab 179 € netto: Logo, Öffnungszeiten, Milchglas und Lochfolie – passend zur Gestaltungssatzung, vor Ort montiert.'),
 'schilder-nrw.html': ('Schilder NRW: Firmen-, Praxis- & Türschilder ab 59 € | Masar',
   'Schilder in NRW ab 59 €: Firmen-, Praxis- und Türschilder aus Alu-Dibond, Acryl und Edelstahl – gefertigt und montiert in Düsseldorf, Köln und im Ruhrgebiet.'),
 'pvc-banner-nrw.html': ('Banner drucken NRW: PVC-Banner ab 22 €/m² | Masar',
   'PVC-Banner in NRW ab 22 €/m² netto: wetterfest, mit oder ohne Ösen, Mesh-Banner für Gerüst und Bauzaun – Düsseldorf, Köln, Ruhrgebiet, Montage vor Ort.'),
 'fahrzeugbeschriftung-nrw.html': ('Fahrzeugbeschriftung NRW ab 340 € | Transporter & Flotte',
   'Fahrzeugbeschriftung in NRW mit Team vor Ort: Teil- und Vollbeschriftung für Transporter, Pkw und Flotten ab 340 € – Düsseldorf, Köln, Ruhrgebiet.'),
 'webdesign-nrw.html': ('Webdesign NRW: Firmen-Websites zum Festpreis | Masar',
   'Webdesign für Unternehmen in NRW: schnelle, mobile Websites und Landingpages mit Texten und SEO-Grundlagen – Festpreis nach Umfang. Angebot in 24 h.'),
 'blog/fensterfolie-mietwohnung.html': ('Fensterfolie in der Mietwohnung: Muss der Vermieter zustimmen?',
   'Sichtschutz- oder Sonnenschutzfolie in der Mietwohnung: wann Sie den Vermieter fragen sollten, worauf beim Auszug zu achten ist und warum das Glas zählt.'),
 'blog/werbung-kosmetikstudio.html': ('Werbung fürs Kosmetikstudio: Ideen, die Termine bringen',
   'Werbung fürs Kosmetikstudio: Schaufenster, LED-Neon und Reels, die Termine bringen – und was das Heilmittelwerbegesetz bei Vorher-nachher-Bildern sagt.'),
 'blog/werbung-fahrschule.html': ('Werbung für Fahrschulen: Ideen & was erlaubt ist (2026)',
   'Werbung für Fahrschulen: Fahrschulwagen, Schaufenster, TikTok und Preisaushang – und was Fahrlehrergesetz und DV-FahrlG zu Schild und Preisen sagen.'),
 'blog/fahrzeugbeschriftung-pflegedienst.html': ('Fahrzeugbeschriftung Pflegedienst: 7 Tipps & Kosten',
   'Fahrzeugbeschriftung für ambulante Pflegedienste: was aufs Auto gehört, wie Recruiting auf dem Heck funktioniert, Leasing, Diskretion und Kosten.'),
 'blog/aussenwerbung-berlin-ratgeber.html': ('Außenwerbung Berlin: Genehmigung & Kosten (2026)',
   'Bis 1 m², am eigenen Geschäft bis 2,5 m², ist Werbung in Berlin verfahrensfrei. Was darüber gilt, wer entscheidet und was Folie oder LED-Schrift kostet.'),
 'blog/sonnenschutzfolie-schaufenster.html': ('Sonnenschutzfolie fürs Schaufenster: UV-Schutz für Ware',
   'Ausgebleichte Ware im Schaufenster? Wie Sonnenschutz- und UV-Folie Verkaufsräume kühler halten und Ware schützen – ohne dass das Schaufenster dunkel wirkt.'),
 'blog/werbung-immobilienmakler.html': ('Werbung für Immobilienmakler: Eigentümer gewinnen | Masar',
   'Werbung für Makler: Objektschilder, Schaufenster, Exposé, Fotos und Social Media – und welche Pflichtangaben § 87 GEG in Immobilienanzeigen verlangt.'),
 'blog/index.html': ('Werbetechnik-Blog: Ratgeber, Preise & Regeln | Masar',
   'Ratgeber zu Schildern, Leuchtreklame, Folien und Fahrzeugbeschriftung: ehrliche Preise, Genehmigungen in Berlin, NRW und Hamburg – mit Quellen.'),
}


def setze(s, name, wert, attr='name'):
    return re.sub(rf'(<meta {attr}="{re.escape(name)}" content=")[^"]*', lambda m: m.group(1) + html.escape(wert, quote=True), s, count=1)


def main(dry=False):
    fehler = 0
    for f, (t, d) in S.items():
        if len(t) > 62 or not (110 <= len(d) <= 160):
            print(f'LÄNGE {len(t):3}/{len(d):3}  {f}'); fehler += 1
        p = os.path.join(ROOT, f)
        if not os.path.exists(p): print('fehlt', f); continue
        if dry: continue
        s = open(p, encoding='utf-8').read()
        s = re.sub(r'<title>.*?</title>', '<title>' + html.escape(t, quote=False) + '</title>', s, count=1, flags=re.S)
        s = setze(s, 'description', d)
        s = setze(s, 'og:title', t, 'property'); s = setze(s, 'og:description', d, 'property')
        s = setze(s, 'twitter:title', t); s = setze(s, 'twitter:description', d)
        open(p, 'w', encoding='utf-8').write(s)
    print(len(S), 'Seiten', 'geprüft' if dry else 'aktualisiert', '–', fehler, 'Längenhinweise')
    # Zweiter Durchgang: übrige Titel über 60 Zeichen – Markenzusatz „ | Masar“ weglassen
    import glob
    gekuerzt = 0
    for p in glob.glob(os.path.join(ROOT, '*.html')) + glob.glob(os.path.join(ROOT, 'blog', '*.html')):
        s = open(p, encoding='utf-8').read()
        m = re.search(r'<title>(.*?)</title>', s, re.S)
        if not m: continue
        t = html.unescape(m.group(1).strip())
        if len(t) <= 60 or not t.endswith(' | Masar'): continue
        neu = t[:-len(' | Masar')]
        gekuerzt += 1
        if dry: print('kürzen', os.path.relpath(p, ROOT), len(t), '→', len(neu)); continue
        e = html.escape(neu, quote=False)
        s = s.replace(m.group(0), f'<title>{e}</title>', 1)
        for n, a in [('og:title', 'property'), ('twitter:title', 'name')]:
            s = re.sub(rf'(<meta {a}="{n}" content=")[^"]*', lambda mm: mm.group(1) + html.escape(neu, quote=True), s, count=1)
        open(p, 'w', encoding='utf-8').write(s)
    print(gekuerzt, 'weitere Titel gekürzt')


if __name__ == '__main__':
    main('--dry' in sys.argv)
