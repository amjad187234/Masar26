"""Städteseiten NRW: Leuchtreklame + Schilder für Köln, Düsseldorf, Dortmund, Essen, Bochum."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'nrw_pages.py'), encoding='utf-8').read()
exec(src[:src.index("\nif __name__")])

def q(url, label):
    return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{label}</a>'

# Lokale Fakten nur aus offiziellen bzw. geprüften Quellen (Stand Oktober 2026)
C = {
 'koeln': dict(name='Köln', hub='werbeagentur-koeln.html', veedel='Ehrenfeld, Nippes, Sülz, Deutz, Kalk oder Porz',
   lagen='Schildergasse, Hohe Straße und Ehrenstraße', gewerbe='im Industriegebiet Niehl', ph='Köln-Ehrenfeld',
   regel=f'''<p><strong>Werbesatzungen in Köln:</strong> Köln hat für einzelne Bereiche eigene Werbesatzungen. Für die Kölner Ringe hat der Rat 2023 und 2024 neue Satzungen für die einzelnen Ring-Abschnitte beschlossen; daneben gibt es Satzungen etwa für das Kwartier Latäng und die Luxemburger Straße. Sie regeln, wo Werbeanlagen angebracht werden dürfen und wie groß und wie gestaltet sie sein dürfen. In diesen Bereichen braucht eine Werbeanlage eine Genehmigung der Bauaufsicht.</p>
<p><strong>Ausleger und Gehweg:</strong> Wer den öffentlichen Straßenraum über den normalen Gemeingebrauch hinaus nutzt, braucht nach der Kölner Sondernutzungssatzung vorher eine Erlaubnis. Den Bauantrag stellen Sie in Köln online über das Bauportal.NRW – wir bereiten die Unterlagen für Ihre Werbeanlage vor.</p>
<p style="font-size:13px;">Quellen: {q("https://www.stadt-koeln.de/politik-und-verwaltung/presse/mitteilungen/24916/index.html", "Stadt Köln – Werbesatzungen Kölner Ringe")}, {q("https://www.stadt-koeln.de/mediaasset/content/satzungen/sondernutzungssatzung_10_06_2024.pdf", "Sondernutzungssatzung Köln")}, {q("https://www.stadt-koeln.de/service/produkte/00139/index.html", "Stadt Köln – Baugenehmigung")}. Allgemeine Hinweise, keine Rechtsberatung.</p>''',
   faq_lokal=('Gilt in Köln eine Werbesatzung für meine Adresse?', 'Das hängt von der Lage ab. Für die Kölner Ringe, das Kwartier Latäng, die Luxemburger Straße und weitere Bereiche gibt es eigene Werbesatzungen. Wir prüfen Ihre Adresse, bevor Sie ein Angebot unterschreiben.')),
 'duesseldorf': dict(name='Düsseldorf', hub='werbeagentur-duesseldorf.html', veedel='Bilk, Flingern, Oberkassel, Pempelfort, Gerresheim oder Benrath',
   lagen='Königsallee und Schadowstraße', gewerbe='am Reisholzer Hafen und rund um den Flughafen', ph='Düsseldorf-Bilk',
   regel=f'''<p><strong>Altstadt Düsseldorf:</strong> Für den Altstadtbereich gilt eine eigene Satzung über Werbeanlagen. Dort sind Werbeanlagen genehmigungspflichtig – auch kleine Anlagen, die anderswo in NRW verfahrensfrei wären. Welche Straßen dazugehören, legt die Satzung mit Straßenliste und Plan fest.</p>
<p><strong>Wechselndes und bewegtes Licht:</strong> Für Werbeanlagen mit wechselndem oder bewegtem Licht hat Düsseldorf eine eigene Satzung für das Stadtgebiet. Bei blinkenden oder animierten Leuchtreklamen prüfen wir deshalb besonders genau, was an Ihrer Adresse möglich ist.</p>
<p style="font-size:13px;">Quellen: {q("https://www.duesseldorf.de/stadtrecht/6/63/63-202/", "Düsseldorf Ortsrecht 63.202 – Werbeanlagen Altstadtbereich")}, {q("https://www.duesseldorf.de/stadtrecht/6/63/63-201", "Ortsrecht 63.201 – wechselndes und bewegtes Licht")}. Allgemeine Hinweise, keine Rechtsberatung.</p>''',
   faq_lokal=('Brauche ich in der Düsseldorfer Altstadt eine Genehmigung?', 'Ja, in der Regel. Im Altstadtbereich gilt eine eigene Satzung, nach der auch kleine Werbeanlagen genehmigt werden müssen. Wir prüfen, ob Ihre Adresse dazugehört, und bereiten den Antrag vor.')),
 'dortmund': dict(name='Dortmund', hub='werbeagentur-dortmund.html', veedel='Hörde, Kreuzviertel, Aplerbeck, Brackel, Hombruch oder Huckarde',
   lagen='Westenhellweg und Ostenhellweg', gewerbe='auf PHOENIX West', ph='Dortmund-Hörde',
   regel=f'''<p><strong>Gestaltungssatzungen in Dortmund:</strong> Liegt Ihr Geschäft im Bereich einer Gestaltungssatzung – die Stadt nennt als Beispiel den Westenhellweg –, braucht jede Werbeanlage eine Baugenehmigung, auch eine kleine. Außerhalb solcher Bereiche gilt die 1-m²-Grenze der BauO NRW.</p>
<p><strong>Öffentlicher Raum:</strong> Ragt eine Werbeanlage in den öffentlichen Raum, etwa als Ausleger über den Gehweg, ist zusätzlich eine Vereinbarung mit dem Tiefbauamt nötig. Zuständig für die Baugenehmigung ist das Stadtplanungs- und Bauordnungsamt.</p>
<p style="font-size:13px;">Quellen: {q("https://www.dortmund.de/services/bauantrag-werbeanlagen.html", "Stadt Dortmund – Bauantrag Werbeanlagen")}, {q("https://www.dortmund.de/dortmund/projekte/rathaus/verwaltung/stadtplanungs-und-bauordnungsamt/downloads/bauordnung/infoblaetter/infoblatt_werbeanlagen.pdf", "Infoblatt Werbeanlagen")}. Allgemeine Hinweise, keine Rechtsberatung.</p>''',
   faq_lokal=('Brauche ich am Westenhellweg eine Genehmigung?', 'Ja. Laut Stadt Dortmund brauchen Werbeanlagen im Bereich einer Gestaltungssatzung, zum Beispiel am Westenhellweg, immer eine Baugenehmigung. Wir bereiten die Unterlagen vor.')),
 'essen': dict(name='Essen', hub='werbeagentur-essen.html', veedel='Rüttenscheid, Steele, Werden, Kettwig, Borbeck oder Frohnhausen',
   lagen='Kettwiger Straße und Limbecker Straße', gewerbe='im Essener Norden', ph='Essen-Rüttenscheid',
   regel=f'''<p><strong>Gestaltungssatzung Innenstadt:</strong> Die Stadt Essen arbeitet an einer Gestaltungssatzung für die Innenstadt; die Bürgerbeteiligung dazu hat im Juni 2025 begonnen. Als ein Problem nennt die Stadt überladene Werbung. Wer in der Innenstadt eine neue Leuchtreklame oder ein großes Schild plant, sollte deshalb vorher prüfen lassen, welche Regeln aktuell gelten.</p>
<p><strong>Außerhalb der Innenstadt:</strong> In den Stadtteilen gilt in der Regel die BauO NRW: bis 1&nbsp;m² Ansichtsfläche meist verfahrensfrei, größere Anlagen genehmigungspflichtig – vorbehaltlich Bebauungsplan und Denkmalschutz.</p>
<p style="font-size:13px;">Quelle: {q("https://www.essen.de/leben/planen_bauen_und_wohnen/innenstadt/innenstadt___gestaltung.de.html", "Stadt Essen – Gestaltung der Innenstadt")}. Allgemeine Hinweise, keine Rechtsberatung.</p>''',
   faq_lokal=('Gibt es in Essen Regeln für Werbung in der Innenstadt?', 'Die Stadt Essen bereitet eine Gestaltungssatzung für die Innenstadt vor. Wir prüfen vor jedem Auftrag, welche Regeln für Ihre Adresse gelten.')),
 'bochum': dict(name='Bochum', hub='werbeagentur-bochum.html', veedel='Wattenscheid, Langendreer, Linden, Weitmar, Gerthe oder Querenburg',
   lagen='Kortumstraße und rund um das Bermuda3eck', gewerbe='auf MARK 51°7', ph='Bochum-Wattenscheid',
   regel=f'''<p><strong>Gestaltungssatzung Innenstadt:</strong> Für die Bochumer Innenstadt gilt eine Gestaltungssatzung; die überarbeitete Fassung ist seit April 2024 in Kraft. Sie regelt unter anderem Fassaden und Werbeanlagen, dazu gibt es ein Gestaltungshandbuch der Stadt. Für Leuchtreklame und Schilder in der City lohnt deshalb ein Blick in diese Regeln, bevor produziert wird.</p>
<p><strong>Außerhalb der Innenstadt:</strong> In den Stadtteilen gilt in der Regel die BauO NRW: bis 1&nbsp;m² Ansichtsfläche meist verfahrensfrei, größere Anlagen genehmigungspflichtig.</p>
<p style="font-size:13px;">Quellen: {q("https://www.ihk.de/bochum/hauptnavigation/branchenbetreuung/stadtentwicklung/stadt-und-quartiersentwicklung/gestaltungssatzung-bochum-6656476", "IHK Mittleres Ruhrgebiet – Gestaltungssatzung Bochum")}, {q("https://www.bochum.de/C125830C0042AB74/vwContentByKey/W2DFADVN491BOCMDE/$FILE/Satzungstext.PDF", "Satzungstext Stadt Bochum")}. Allgemeine Hinweise, keine Rechtsberatung.</p>''',
   faq_lokal=('Was gilt für Werbung in der Bochumer Innenstadt?', 'Für die Innenstadt gilt seit April 2024 die überarbeitete Gestaltungssatzung, die auch Werbeanlagen regelt. Wir richten Entwurf und Größe danach aus.')),
}

def city_links(service, cur):
    return [(f'/{service}-{k}.html', v['name']) for k, v in C.items() if k != cur]

PAGES_C = []
for k, c in C.items():
    n = c['name']
    # ------------------------------------------------ Leuchtreklame {Stadt}
    p = dict(L)
    p.update(file=f'leuchtreklame-{k}.html', crumb=f'Leuchtreklame {n}', parent=(f'Werbeagentur {n}', c['hub']),
     area=[{"@type": "City", "name": n}],
     img_alt=f'Beispiel-Visualisierung: Leuchtreklame mit beleuchteten Buchstaben an einer Ladenfassade in {n}',
     title=f'Leuchtreklame {n}: Leuchtbuchstaben & Leuchtkästen | Masar',
     desc=f'Leuchtreklame in {n}: LED-Leuchtbuchstaben ab 229 € netto, Leuchtkästen und Ausleger – Genehmigung geprüft, Montage durch unser Team vor Ort.',
     schema_name=f'Leuchtreklame in {n}', badge=f'Leuchtreklame · {n}', h1=f'Leuchtreklame <em>{n}</em>',
     sub=f'Leuchtbuchstaben, Leuchtkästen und Ausleger für Läden, Praxen und Restaurants in {n} – von {c["lagen"]} bis {c["veedel"]}. Wir gestalten, klären die Genehmigung und unser Team in NRW montiert bei Ihnen vor Ort.',
     trust=f'LED-Leuchtbuchstaben ab 229 € / Buchstabe netto · Montage in {n}',
     wa=f'Hallo, ich interessiere mich für eine Leuchtreklame in {n}. Ich schicke Ihnen ein Foto der Fassade.',
     angles_h2=f'Sichtbar in {n} – <em>auch am Abend</em>',
     angles_sub=f'In {c["lagen"]} konkurrieren viele Geschäfte um Aufmerksamkeit. Licht macht den Unterschied.',
     angles=[L['angles'][0],
      ('Passend zur Lage', f'Einkaufsstraße, Wohnviertel wie {c["veedel"].split(",")[0]} oder Gewerbebetrieb {c["gewerbe"]}: Wir wählen Bauart und Größe so, dass die Reklame zur Umgebung und zu den örtlichen Regeln passt.'),
      L['angles'][2], L['angles'][3]],
     recht_h2=f'Genehmigung <em>in {n}</em>',
     recht_html=BAUO + c['regel'],
     faq_h2=f'Leuchtreklame {n} – <em>Fragen &amp; Antworten</em>',
     faq=[(f'Montieren Sie Leuchtreklame in ganz {n}?', f'Ja. Unser Team in NRW kommt für Aufmaß und Montage zu Ihnen – zum Beispiel nach {c["veedel"]}. Unser Firmensitz ist in Berlin.'),
          c['faq_lokal'],
          ('Was kostet eine Leuchtreklame?', 'LED-Leuchtbuchstaben beginnen in NRW ab 229 € pro Buchstabe netto zzgl. 19 % MwSt. Leuchtkästen und Ausleger kalkulieren wir nach Größe. Den Festpreis inklusive Montage bekommen Sie nach einem Foto der Fassade.')] + L['faq'][2:5],
     links=[('/leuchtreklame-nrw.html', 'Leuchtreklame NRW'), (f'/schilder-{k}.html', f'Schilder {n}'), (f'/schaufensterbeschriftung-{k}.html', f'Schaufenster {n}'), ('/fensterfolie-nrw.html', 'Fensterfolie NRW'), ('/' + c['hub'], f'Werbeagentur {n}')] + [(u, f'Leuchtreklame {t}') for u, t in city_links('leuchtreklame', k)],
     form_sub=f'Schicken Sie uns ein Foto der Fassade und Ihr Logo – Sie bekommen innerhalb von 24 Stunden ein Angebot. Unser Team montiert bei Ihnen in {n}.',
     subject=f'Anfrage Leuchtreklame {n} (Website)', msg_ph=f'z. B. Leuchtbuchstaben über dem Eingang, Fassade ca. 5 m breit, Ladenlokal in {c["ph"]}',
     sticky=(f'Leuchtreklame {n}', 'ab 229 € / Buchstabe netto'), ph=c['ph'])
    p['top'] = price_top(f'Was kostet <em>Leuchtreklame in {n}?</em>', None, ROWS_L, PRICE_NOTE)
    PAGES_C.append(p)
    # ------------------------------------------------ Schilder {Stadt}
    p = dict(S)
    p.update(file=f'schilder-{k}.html', crumb=f'Schilder {n}', parent=(f'Werbeagentur {n}', c['hub']),
     area=[{"@type": "City", "name": n}],
     img_alt=f'Beispiel-Visualisierung: Firmenschild aus Acryl mit Abstandshaltern – Schilder für Unternehmen in {n}',
     title=f'Schilder {n}: Firmen-, Praxis- & Türschilder | Masar',
     desc=f'Schilder in {n}: Firmenschilder ab 179 € netto, Praxis-, Tür- und Klingelschilder aus Alu-Dibond, Acryl und Edelstahl – gefertigt und vor Ort montiert.',
     schema_name=f'Schilder in {n}', badge=f'Schilder · {n}', h1=f'Schilder <em>{n}</em>',
     sub=f'Firmenschild am Eingang, Praxisschild neben der Klingel, Wegweiser im Treppenhaus: Wir gestalten und fertigen Schilder für Betriebe in {n} – in {c["veedel"]} und überall dazwischen. Unser Team in NRW bringt sie bei Ihnen an.',
     trust=f'Firmenschild ab 179 € netto · Türschild ab 85 € · Montage in {n}',
     wa=f'Hallo, ich brauche ein Schild in {n}. Ich schicke Ihnen ein Foto der Stelle.',
     angles_h2=f'Der erste Eindruck <em>in {n}</em>',
     angles=[('Gefunden werden', f'Ob Bürohaus in der City, Hinterhof in {c["veedel"].split(",")[0]} oder Halle {c["gewerbe"]}: Ein klares Schild am richtigen Platz erspart Kunden die Suche und Ihnen die Anrufe.')] + S['angles'][1:],
     recht_h2=f'Was bei Schildern <em>in {n} gilt</em>',
     recht_html=BAUO + c['regel'] + '<p><strong>Mietobjekt:</strong> Im Mietobjekt sollten Sie vor der Montage mit dem Vermieter oder der Hausverwaltung klären, wo und wie gebohrt werden darf. Wir richten uns nach diesen Vorgaben.</p>',
     faq_h2=f'Schilder {n} – <em>Fragen &amp; Antworten</em>',
     faq=[(f'Montieren Sie Schilder in ganz {n}?', f'Ja. Unser Team in NRW bringt die Schilder bei Ihnen an – zum Beispiel in {c["veedel"]}. Unser Firmensitz ist in Berlin.'),
          ('Was kostet ein Firmenschild?', 'Ein Firmenschild aus Alu-Dibond bis 1 m² beginnt in NRW ab 179 € netto zzgl. 19 % MwSt., Tür- und Klingelschilder ab 85 €, Acrylglasschilder ab 289 €. Den Festpreis mit Montage bekommen Sie nach einem Foto der Stelle.'),
          c['faq_lokal']] + S['faq'][1:3] + S['faq'][4:5],
     links=[('/schilder-nrw.html', 'Schilder NRW'), (f'/leuchtreklame-{k}.html', f'Leuchtreklame {n}'), (f'/schaufensterbeschriftung-{k}.html', f'Schaufenster {n}'), ('/' + c['hub'], f'Werbeagentur {n}')] + [(u, f'Schilder {t}') for u, t in city_links('schilder', k)],
     form_sub=f'Schicken Sie uns ein Foto der Stelle und Ihr Logo – Sie bekommen innerhalb von 24 Stunden ein Angebot. Unser Team montiert bei Ihnen in {n}.',
     subject=f'Anfrage Schilder {n} (Website)', msg_ph=f'z. B. Praxisschild aus Acryl, ca. 60 × 40 cm, neben dem Hauseingang in {c["ph"]}, Montage gewünscht',
     sticky=(f'Schilder {n}', 'Firmenschild ab 179 € netto'), ph=c['ph'])
    p['top'] = price_top(f'Was kostet <em>ein Schild in {n}?</em>', None, ROWS_S, PRICE_NOTE)
    PAGES_C.append(p)
    # ------------------------------------------------ Schaufensterbeschriftung {Stadt}
    p = dict(W)
    p.update(file=f'schaufensterbeschriftung-{k}.html', crumb=f'Schaufensterbeschriftung {n}', parent=(f'Werbeagentur {n}', c['hub']),
     area=[{"@type": "City", "name": n}],
     img_alt=f'Beispiel-Visualisierung: Schaufenster mit Folienbeschriftung, Logo und Öffnungszeiten – Schaufensterbeschriftung in {n}',
     title=f'Schaufensterbeschriftung {n}: Folie & Milchglas | Masar',
     desc=f'Schaufensterbeschriftung in {n} ab 179 € netto: Logo, Öffnungszeiten, Milchglas und Lochfolie für Läden und Praxen – vor Ort montiert.',
     schema_name=f'Schaufensterbeschriftung in {n}', badge=f'Schaufenster · {n}', h1=f'Schaufenster&shy;beschriftung <em>{n}</em>',
     sub=f'Ihr Schaufenster ist die Werbefläche, an der jeden Tag Menschen vorbeigehen – in {c["lagen"]} genauso wie in {c["veedel"]}. Wir gestalten und produzieren Folien für Logo, Öffnungszeiten, Sichtschutz und große Motive, unser Team in NRW klebt sie bei Ihnen vor Ort.',
     trust=f'Beschriftung ab 179 € netto · Milchglas ab 229 € · Montage in {n}',
     wa=f'Hallo, ich interessiere mich für eine Schaufensterbeschriftung in {n}. Ich schicke Ihnen ein Foto der Fenster.',
     angles_h2=f'Ihre Fenster in {n} <em>arbeiten für Sie</em>',
     angles=[('Sofort erkennbar', f'Wer durch {c["lagen"].split(" und ")[0]} oder durch Ihr Viertel geht, sieht in Sekunden, was Sie anbieten. Logo, Leistungen und Öffnungszeiten auf dem Glas sagen das ohne Worte.')] + W['angles'][1:],
     recht_h2=f'Was Sie in {n} <em>wissen sollten</em>',
     recht_html=c['regel'] + W['recht_html'].split('</p>', 1)[1],
     faq_h2=f'Schaufenster {n} – <em>Fragen &amp; Antworten</em>',
     faq=[(f'Kommen Sie für die Montage nach {n}?', f'Ja. Unser Team in NRW montiert bei Ihnen vor Ort – zum Beispiel in {c["veedel"]}. Unser Firmensitz ist in Berlin.'),
          ('Was kostet eine Schaufensterbeschriftung?', 'Eine einfache Beschriftung mit Logo, Öffnungszeiten und Kontakt beginnt in NRW ab 179 € netto zzgl. 19 % MwSt., Milchglas-Sichtschutz ab 229 €, Lochfolie ab 55 € pro m². Den Festpreis mit Montage bekommen Sie nach einem Foto der Fenster.'),
          c['faq_lokal']] + W['faq'][1:3] + W['faq'][4:5],
     links=[('/schaufensterbeschriftung-nrw.html', 'Schaufenster NRW'), ('/fensterfolie-nrw.html', 'Fensterfolie NRW'), (f'/schilder-{k}.html', f'Schilder {n}'), (f'/leuchtreklame-{k}.html', f'Leuchtreklame {n}'), ('/fensterfolie-nrw.html', 'Fensterfolie NRW')] + [(u, f'Schaufenster {t}') for u, t in city_links('schaufensterbeschriftung', k)],
     form_sub=f'Schicken Sie uns ein Foto der Fenster und Ihr Logo – Sie bekommen innerhalb von 24 Stunden ein Angebot. Unser Team montiert bei Ihnen in {n}.',
     subject=f'Anfrage Schaufensterbeschriftung {n} (Website)', msg_ph=f'z. B. 3 Schaufenster je ca. 1,2 × 2 m, Logo und Leistungen, Milchglas unten, Laden in {c["ph"]}',
     sticky=(f'Schaufenster {n}', 'Beschriftung ab 179 € netto'), ph=c['ph'])
    p['top'] = price_top(f'Was kostet <em>eine Schaufensterbeschriftung in {n}?</em>', None, ROWS_W, PRICE_NOTE)
    PAGES_C.append(p)
    # ------------------------------------------------ Fensterfolie {Stadt}
    p = dict(F)
    p.update(file=f'fensterfolie-{k}.html', crumb=f'Fensterfolie {n}', parent=(f'Werbeagentur {n}', c['hub']),
     area=[{"@type": "City", "name": n}],
     img_alt=f'Beispiel-Visualisierung: Bürofenster mit Sonnenschutz- und Sichtschutzfolie – Fensterfolie in {n}',
     title=f'Fensterfolie {n}: Sonnenschutz & Sichtschutz | Masar',
     desc=f'Fensterfolie in {n}: Sonnenschutz gegen Hitze, Sichtschutz ab 229 € netto, Spiegel- und Sicherheitsfolie – mit Glasprüfung und Montage vor Ort.',
     schema_name=f'Fensterfolie in {n}', badge=f'Fensterfolie · {n}', h1=f'Fensterfolie <em>{n}</em>',
     sub=f'Zu heiß im Büro, zu viel Einblick in die Praxis oder Sorge um Glasbruch? Für Büros, Praxen, Läden und Wohnungen in {n} – von {c["veedel"]} bis zu den Gewerbeflächen {c["gewerbe"]}: Wir prüfen Ihr Glas, empfehlen die passende Folie und unser Team in NRW montiert sie bei Ihnen.',
     trust=f'Sichtschutz ab 229 € netto · Glas geprüft · Montage in {n}',
     wa=f'Hallo, ich interessiere mich für Fensterfolie in {n}. Ich schicke Ihnen ein Foto der Fenster.',
     angles_h2=f'Ein Problem am Fenster in {n} – <em>eine passende Folie</em>',
     angles=[F['angles'][0], ('Blicke von außen', f'Erdgeschoss an einer belebten Straße in {c["veedel"].split(",")[0]} oder Praxis in der Innenstadt: Milchglas- oder Spiegelfolie schützt Ihre Räume vor Blicken.')] + F['angles'][2:],
     recht_html=F['recht_html'] + f'<p><strong>Folie mit Werbung:</strong> Trägt die Folie Logo oder Werbung und ist von außen sichtbar, kann sie in {n} als Werbeanlage gelten – dann gelten die örtlichen Regeln wie bei einer <a href="/schaufensterbeschriftung-{k}.html">Schaufensterbeschriftung in {n}</a>. Reine Sicht- und Sonnenschutzfolie ohne Werbung ist davon nicht betroffen.</p>',
     faq_h2=f'Fensterfolie {n} – <em>Fragen &amp; Antworten</em>',
     faq=[(f'Montieren Sie Fensterfolie in ganz {n}?', f'Ja. Unser Team in NRW kommt zu Ihnen – zum Beispiel nach {c["veedel"]}. Unser Firmensitz ist in Berlin.'),
          ('Was kostet Fensterfolie?', 'Sichtschutzfolie für eine Fensterfläche beginnt in NRW ab 229 € netto zzgl. 19 % MwSt., Milchglasfolie nach Maß ab 289 €. Sonnenschutz-, Spiegel- und Sicherheitsfolie kalkulieren wir nach Fläche und Glas. Den Festpreis mit Montage bekommen Sie nach Fotos der Fenster.')] + F['faq'][1:5],
     links=[('/fensterfolie-nrw.html', 'Fensterfolie NRW'), (f'/schaufensterbeschriftung-{k}.html', f'Schaufenster {n}'), ('/blog/sonnenschutzfolie-innen-oder-aussen.html', 'Sonnenschutzfolie innen oder außen'), ('/' + c['hub'], f'Werbeagentur {n}')] + [(u, f'Fensterfolie {t}') for u, t in city_links('fensterfolie', k)],
     form_sub=f'Schicken Sie uns Fotos der Fenster und sagen Sie uns, was stört – Sie bekommen innerhalb von 24 Stunden ein Angebot. Unser Team montiert bei Ihnen in {n}.',
     subject=f'Anfrage Fensterfolie {n} (Website)', msg_ph=f'z. B. Büro mit 6 Fenstern nach Süden, je ca. 1,5 × 2 m, zu heiß im Sommer, 2. OG in {c["ph"]}',
     sticky=(f'Fensterfolie {n}', 'Sichtschutz ab 229 € netto'), ph=c['ph'])
    p['top'] = price_top(f'Was kostet <em>Fensterfolie in {n}?</em>', None, ROWS_F, PRICE_NOTE)
    # 24.10.2026: Fensterfolie-Städteseiten in fensterfolie-nrw.html zusammengeführt (301 in .htaccess) – nicht mehr bauen
    # PAGES_C.append(p)

if __name__ == '__main__':
    for p in PAGES_C:
        r = build_f(p); nrw_fix(p)
        h = open(ROOT + p['file'], encoding='utf-8').read().replace('placeholder="z. B. Köln-Ehrenfeld"', f'placeholder="z. B. {p["ph"]}"')
        open(ROOT + p['file'], 'w', encoding='utf-8').write(h)
        print(r)
