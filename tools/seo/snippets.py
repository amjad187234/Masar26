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
   'Fensterfolie in Berlin – auch Neukölln, Tempelhof, Schöneberg: Sonnenschutz, Sichtschutz ab 190 €, Sicherheitsfolie. Glasprüfung, Montage, Festpreis.'),
 'pvc-banner-berlin.html': ('Banner drucken Berlin: PVC-Banner ab 29 €/m² | Masar',
   'PVC-, Mesh- und Blockout-Banner in Berlin drucken lassen: ab 29 €/m² netto, wetterfest, mit Ösen – Gestaltung und Montage auf Wunsch. Angebot in 24 h.'),
 'aussenwerbung-berlin.html': ('Außenwerbung Berlin: Fassade & Leuchtreklame | Masar',
   'Außenwerbung in Berlin aus einer Hand: Leuchtbuchstaben ab 199 €, Fassadenschilder und Banner – mit Genehmigungs-Check und Montage. Angebot in 24 h.'),
 'leuchtreklame-berlin.html': ('Leuchtreklame Berlin: Leuchtbuchstaben ab 199 € | Masar',
   'Leuchtreklame in Berlin: LED-Leuchtbuchstaben ab 199 € je Buchstabe, Leuchtkästen und LED-Neon ab 249 € – Entwurf, Genehmigung und Montage.'),
 'messebau-berlin.html': ('Messebau Berlin: Messestand planen & bauen lassen | Masar',
   'Messebau in Berlin: Konzept, 3D-Entwurf, Standbau, Messegrafik sowie Auf- und Abbau aus einer Hand – für Messen in Berlin und Brandenburg.'),
 'sicherheitsfolie-berlin.html': ('Sicherheitsfolie Berlin: Einbruch- & Splitterschutz | Masar',
   'Sicherheitsfolie in Berlin: Einbruchschutz- und Splitterschutzfolie für Schaufenster, Glastüren und Erdgeschoss – Beratung zu Prüfklassen, Montage vor Ort.'),
 'sichtschutzfolie-berlin.html': ('Sichtschutzfolie Berlin: Milchglas ab 190 € | Masar',
   'Sichtschutzfolie in Berlin: Milchglas, Streifen, Spiegelfolie oder Dekor mit Logo – für Büro, Praxis, Bad und Erdgeschoss. Ab 190 € netto, Angebot in 24 h.'),
 'foliendruck-berlin.html': ('Foliendruck Berlin: Aufkleber & Klebefolie | Masar',
   'Foliendruck in Berlin: Aufkleber, Klebefolie, Bodenaufkleber und Fensterfolie ab 45 € – wetterfest und in Ihrem Design. Angebot in 24 h.'),
 'praxisbeschilderung-berlin.html': ('Praxisschilder Berlin: Schild, Tür & Sichtschutz | Masar',
   'Praxisschild, Türschild, Sprechzeiten und Sichtschutz am Fenster für Arzt- und Therapiepraxen in Berlin – gestaltet und montiert. Pakete ab 699 € netto.'),
 'referenzen.html': ('Referenzen: Leuchtreklame & Fahrzeugbeschriftung Berlin',
   'Echte Projekte aus unserer Werkstatt: Leuchtreklame, Fahrzeugbeschriftung und Vollfolierung, Schaufenster, Digital Signage – Fotos aus Berlin.'),
 'werbetechnik-potsdam.html': ('Werbetechnik Potsdam: Schilder, Banner & Fahrzeuge | Masar',
   'Werbetechnik in Potsdam: Schilder ab 45 €, Banner, Fahrzeugbeklebung, Leuchtreklame und Schaufenster – Werbesatzung geprüft, Montage vor Ort.'),
 'werbeagentur-koeln.html': ('Werbeagentur & Werbetechnik Köln | Masar',
   'Werbetechnik in Köln mit Team vor Ort: Firmenschilder ab 179 €, Leuchtbuchstaben ab 229 €, Schaufenster und Fahrzeuge – Werbesatzung geprüft.'),
 'werbeagentur-duesseldorf.html': ('Werbeagentur Düsseldorf: Schilder & Leuchtreklame | Masar',
   'Werbetechnik in Düsseldorf mit Team vor Ort: Firmenschilder ab 179 €, Leuchtbuchstaben ab 229 €, Schaufenster und Fahrzeuge. Angebot in 24 h.'),
 'werbeagentur-dortmund.html': ('Werbeagentur & Werbetechnik Dortmund | Masar',
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
 'schaufensterbeschriftung-duesseldorf.html': ('Schaufensterbeschriftung Düsseldorf ab 179 € | Masar',
   'Schaufensterbeschriftung in Düsseldorf ab 179 € netto: Logo, Öffnungszeiten, Milchglas und Lochfolie für Läden und Praxen – vor Ort montiert.'),
 'schaufensterbeschriftung-bochum.html': ('Schaufensterbeschriftung Bochum ab 179 € | Masar',
   'Schaufensterbeschriftung in Bochum ab 179 € netto: Logo, Öffnungszeiten, Milchglas und Lochfolie – passend zur Gestaltungssatzung, vor Ort montiert.'),
 'schilder-nrw.html': ('Schilder NRW: Firmen-, Praxis- & Türschilder ab 59 € | Masar',
   'Schilder in NRW ab 59 €: Firmen-, Praxis- und Türschilder aus Alu-Dibond, Acryl und Edelstahl – gefertigt und montiert in Düsseldorf, Köln und im Ruhrgebiet.'),
 'pvc-banner-nrw.html': ('Banner drucken NRW: PVC-Banner ab 34 €/m² | Masar',
   'PVC-Banner in NRW ab 34 €/m² netto: wetterfest, mit oder ohne Ösen, Mesh-Banner für Gerüst und Bauzaun – Düsseldorf, Köln, Ruhrgebiet, Montage vor Ort.'),
 'fahrzeugbeschriftung-nrw.html': ('Fahrzeugbeschriftung NRW ab 340 € | Transporter & Flotte',
   'Fahrzeugbeschriftung in NRW mit Team vor Ort: Teil- und Vollbeschriftung für Transporter, Pkw und Flotten ab 340 € – Düsseldorf, Köln, Ruhrgebiet.'),
 'webdesign-nrw.html': ('Webdesign NRW: Firmen-Websites zum Festpreis | Masar',
   'Webdesign für Unternehmen in NRW: schnelle, mobile Websites und Landingpages mit Texten und SEO-Grundlagen – Festpreis nach Umfang. Angebot in 24 h.'),
 'blog/fensterfolie-mietwohnung.html': ('Fensterfolie in der Mietwohnung: Ohne Vermieter erlaubt?',
   'Darf ich Sichtschutz- oder Sonnenschutzfolie in der Mietwohnung anbringen? Wann der Vermieter zustimmen sollte und was beim Auszug gilt – kurz erklärt.'),
 'blog/werbung-kosmetikstudio.html': ('Werbung fürs Kosmetikstudio: Ideen, die Termine bringen',
   'Werbung fürs Kosmetikstudio: Schaufenster, LED-Neon und Reels, die Termine bringen – und was das Heilmittelwerbegesetz bei Vorher-nachher-Bildern sagt.'),
 'blog/werbung-fahrschule.html': ('Fahrschule Werbung: Ideen, Beispiele & was erlaubt ist',
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
 # 04.11.2026 (seo_check.py): Titel > 60 bzw. Beschreibung > 160 Zeichen gekürzt – Inhalt unverändert, nur Fakten von der Seite
 'ki-fuer-arztpraxen-berlin.html': ('KI für Arztpraxen Berlin: Chat-Assistent & Online-Termine',
   'Digitaler Assistent für Berliner Praxen: Fragen beantworten, Termine und Rezeptwünsche online aufnehmen, E-Mails vorsortieren – mit KI-Hinweis und EU-Hosting.'),
 'ki-fuer-pflegedienste-berlin.html': ('KI für Pflegedienste Berlin: Krankmeldungen & Anfragen',
   'Digitaler Assistent für Pflegedienste in Berlin: Krankmeldungen, Angehörigen-Fragen und Neuanfragen per Chat aufnehmen, E-Mails vorsortieren – Sie entscheiden.'),
 'textildruck-berlin.html': ('Textildruck Berlin: T-Shirts & Hoodies mit Logo | Masar',
   'Textildruck in Berlin für Firmen: T-Shirts, Hoodies, Polos und Taschen mit Logo – Flex- und DTF-Druck ab 5 Stück, Gestaltung inklusive, Versand deutschlandweit.'),
 'foto-video-berlin.html': ('Foto & Video Berlin – Drohne, Produkt- & Food-Fotografie',
   'Foto- und Videoproduktion für Unternehmen in Berlin: Drohnenaufnahmen, Social-Media-Content, Food- und Produktfotos, Werbefilme und Schnitt. Angebot in 24 h.'),
 'lkw-beschriftung-berlin.html': ('LKW-Beschriftung Berlin: Plane, Koffer & Fahrerhaus | Masar',
   'LKW-Beschriftung in Berlin: Fahrerhaus, Kofferaufbau, bedruckte Plane oder Vollfolierung – mit Gestaltung, Produktion und Montage bei Ihnen vor Ort.'),
 'webdesign-berlin.html': ('Webdesign Berlin – Websites & Online-Shops | Masar',
   'Websites, Landingpages und Online-Shops für Berliner Firmen – direkt programmiert oder mit WordPress. Barrierearm, DSGVO-konform und zur Übergabe in Ihre Hand.'),
 'ueber-uns.html': ('Über uns – Ein Team, alle Gewerke | Masar Werbeagentur',
   'Gestalter, Handwerker und Entwickler unter einem Dach in Berlin-Wedding: Werbetechnik, Druck, Design, Web und KI – ein Ansprechpartner für alles.'),
 'blog/angehoerige-kommunikation-pflegedienst.html': ('Kommunikation mit Angehörigen im Pflegedienst',
   'Wie ambulante Pflegedienste Fragen von Angehörigen geordnet aufnehmen: mit Schweigepflicht, festen Wegen und digitalem Assistenten – ohne Dauertelefon.'),
 'blog/digitale-menuetafel-gestalten.html': ('Digitale Menütafel gestalten: Was funktioniert | Masar',
   'Digitale Menütafeln in der Gastronomie: wie viele Positionen auf eine Seite gehören, wie lange sie stehen bleiben muss und welche Fehler oft passieren.'),
 'blog/krankmeldung-pflegedienst-digital.html': ('Krankmeldungen im Pflegedienst digital aufnehmen',
   'Krankmeldung um sechs, Tour um sieben: Wie ambulante Pflegedienste Krankmeldungen per Chat oder WhatsApp aufnehmen – schnell, vollständig, datenschutzgerecht.'),
 'blog/postfach-pflegedienst-ordnen.html': ('E-Mail-Postfach im Pflegedienst ordnen – mit KI',
   'Kassen, Arztpraxen, Bewerbungen, Angehörige: Wie Pflegedienste ihr Postfach vorsortieren und Antworten vorbereiten lassen – die Freigabe bleibt beim Team.'),
 'blog/whatsapp-arztpraxis-datenschutz.html': ('WhatsApp in der Arztpraxis: Was ist erlaubt?',
   'WhatsApp für Terminerinnerungen und Patientenfragen: warum die normale App problematisch ist, was die WhatsApp Business Platform ändert und was gilt.'),
 'blog/fahrzeugbeschriftung-tipps.html': ('Fahrzeugbeschriftung: 7 Tipps zu Folie, Schrift & Montage',
   'Cast- oder Kalanderfolie, wie groß die Schrift sein muss, Profi oder selbst kleben: 7 Tipps aus der Berliner Werkstatt – mit Checkliste und Kostenüberblick.'),
}
# Nur den Titel kürzen (Beschreibung bleibt wörtlich – Rechtsthema)
NUR_TITEL = {
 'blog/ki-verordnung-praxis-pflege.html': 'KI-Verordnung: Was Praxen und Pflegedienste beachten müssen',
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
    for f, t in NUR_TITEL.items():
        if len(t) > 60: print(f'LÄNGE {len(t):3}/---  {f}'); fehler += 1
        p = os.path.join(ROOT, f)
        if dry or not os.path.exists(p): continue
        s = open(p, encoding='utf-8').read()
        s = re.sub(r'<title>.*?</title>', '<title>' + html.escape(t, quote=False) + '</title>', s, count=1, flags=re.S)
        s = setze(s, 'og:title', t, 'property'); s = setze(s, 'twitter:title', t)
        open(p, 'w', encoding='utf-8').write(s)
    print(len(S) + len(NUR_TITEL), 'Seiten', 'geprüft' if dry else 'aktualisiert', '–', fehler, 'Längenhinweise')
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
    # Vorschaubilder und strukturierte Daten nach dem Neu-Erzeugen wiederherstellen (beides idempotent)
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'og'))
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import og_cards, strukturdaten
    print(og_cards.sync(dry), 'Seiten: og:image vom Logo auf eigenes Vorschaubild')
    strukturdaten.main(dry)


if __name__ == '__main__':
    main('--dry' in sys.argv)
