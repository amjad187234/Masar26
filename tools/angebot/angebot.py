"""Angebote als A4-PDF im Masar-Layout (eine Seite).

Aufruf:
  python3 tools/angebot/angebot.py <angebot.json> [ausgabe-ordner]
  → <nr>.html und <nr>.pdf (Standard-Ordner: tools/angebot/privat/ – nicht im Git)

Kundendaten und Stempel gehören NICHT ins Repository (öffentlich auf GitHub):
  • JSON-Dateien mit Kundendaten in tools/angebot/privat/ ablegen (per .gitignore ausgeschlossen)
  • Stempel als tools/angebot/privat/stempel.png (fehlt er, bleibt das Feld leer)
Beispiel ohne echte Daten: tools/angebot/beispiel.json

Felder (JSON):
  nr, datum, gueltig, titel, untertitel, kunde, ort, masse,
  box_titel, box_text, bild (optional, Pfad relativ zur JSON-Datei),
  positionen: [[Leistung, Beschreibung (Zeilen mit \\n), Netto], …],
  anzahlung: Prozent (Standard 60; 0 = Zahlung komplett nach Lieferung),
  zahlungsziel_tage (Standard 7), hinweise: [..], summe_zusatz (Zeile unter der MwSt.)
Rechnet Netto, 19 % MwSt., Brutto und Anzahlung/Rest selbst (auf Cent gerundet, Rest = Brutto − Anzahlung).
"""
import json, os, sys, html, shutil, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(HERE, '..', '..'))).rstrip('/') + '/'
PRIVAT = os.path.join(HERE, 'privat')
FIRMA = ('Amjad Alblili<br>Bristolstraße 19E · 13349 Berlin<br>'
         '0178 514 3918 · info@masar-werbeagentur.de<br>masar-werbeagentur.de')
HINWEISE = [
    'Vor der Produktion erhalten Sie die Reinzeichnung zur Freigabe.',
    'Montage außerhalb Berlins und Zusatzarbeiten nach Absprache und gesonderter Berechnung.',
    'Es gelten unsere AGB: masar-werbeagentur.de/agb.html',
]


def eur(c):
    """Cent → '1.234,56 €'"""
    s = f'{c / 100:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    return s + ' €'


def cent(v):
    if isinstance(v, str):
        v = v.replace('€', '').replace('.', '').replace(',', '.').strip()
    return round(float(v) * 100)


def e(t):
    return html.escape(str(t), quote=True)


def zeilen(t):
    return '<br>'.join(e(z) for z in str(t).split('\n'))


def bauen(d, aus):
    netto = sum(cent(p[2]) for p in d['positionen'])
    mwst = round(netto * 0.19)
    brutto = netto + mwst
    pz = int(d.get('anzahlung', 60))
    anz = round(brutto * pz / 100)
    rest = brutto - anz
    tage = int(d.get('zahlungsziel_tage', 7))

    rows = ''.join(
        f'<tr><td class="pos">{i:02d}</td><td class="l">{e(p[0])}</td><td>{zeilen(p[1])}</td>'
        f'<td class="r">{eur(cent(p[2]))}</td></tr>\n' for i, p in enumerate(d['positionen'], 1))

    bild = ''
    if d.get('bild'):
        src = os.path.join(os.path.dirname(d['_pfad']), d['bild'])
        ziel = os.path.join(aus, os.path.basename(src))
        if os.path.abspath(src) != os.path.abspath(ziel):
            shutil.copy(src, ziel)
        bild = (f'<img src="{e(os.path.basename(src))}" alt="Visualisierung" '
                'style="width:46mm;height:auto;display:block;border-radius:1mm">')

    stempel = ''
    if os.path.exists(os.path.join(PRIVAT, 'stempel.png')):
        shutil.copy(os.path.join(PRIVAT, 'stempel.png'), os.path.join(aus, 'stempel.png')) \
            if os.path.abspath(aus) != os.path.abspath(PRIVAT) else None
        stempel = '<img src="stempel.png" alt="Firmenstempel Masar Werbeagentur">'

    if pz > 0:
        pay = (f'<tr><td class="k">{pz} % Anzahlung</td><td>bei Auftragsfreigabe, vor Produktionsbeginn</td><td class="r">{eur(anz)}</td></tr>\n'
               f'<tr><td class="k">{100 - pz} % Restzahlung</td><td>nach Montage/Lieferung – zahlbar innerhalb von {tage} Tagen ohne Abzug</td><td class="r">{eur(rest)}</td></tr>')
        note = ('Beide Beträge verstehen sich brutto inkl. 19 % MwSt. Die Bankverbindung finden Sie auf der Anzahlungsrechnung, '
                'die Sie nach Auftragsfreigabe erhalten.')
    else:
        pay = f'<tr><td class="k">Zahlung</td><td>nach Lieferung/Montage – zahlbar innerhalb von {tage} Tagen ohne Abzug</td><td class="r">{eur(brutto)}</td></tr>'
        note = 'Betrag brutto inkl. 19 % MwSt. Die Bankverbindung finden Sie auf der Rechnung.'

    hinw = ''.join(f'<li>{e(h)}</li>' for h in d.get('hinweise', HINWEISE))
    css = open(os.path.join(HERE, 'angebot.css'), encoding='utf-8').read().replace('{ROOT}', ROOT)
    nr = e(d['nr'])
    return f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8">
<title>Angebot {nr} – {e(d['titel'])}</title>
<style>
{css}</style></head><body><div class="page">
<div class="head">
  <div class="brand"><b>MASAR</b><span>WERBEAGENTUR BERLIN</span></div>
  <div class="addr">{FIRMA}</div>
</div>
<div class="title"><h1>ANGEBOT</h1><div class="sub">{e(d['titel'])}<br>{e(d.get('untertitel', d['kunde']))}</div></div>
<table class="meta">
  <tr><td class="k">Kunde / Objekt</td><td>{e(d['kunde'])}</td><td class="k k2">Angebots-Nr.</td><td>{nr}</td></tr>
  <tr><td class="k">Montageort</td><td>{e(d.get('ort', ''))}</td><td class="k k2">Angebotsdatum</td><td>{e(d['datum'])}</td></tr>
  <tr><td class="k">Maße</td><td>{e(d.get('masse', ''))}</td><td class="k k2">Gültig bis</td><td><b>{e(d['gueltig'])}</b></td></tr>
</table>
<div class="box"><div class="lbl">{e(d.get('box_titel', 'Ihr Projekt'))}</div><div class="txt" style="display:flex;gap:3mm;align-items:center">
  {bild}<span>{e(d.get('box_text', ''))}</span>
</div></div>
<h2>Leistungsumfang</h2>
<table class="items">
  <tr><th>Pos.</th><th>Leistung</th><th>Beschreibung / Maße</th><th class="r">Netto</th></tr>
{rows}</table>
<div class="sum">
  <table>
    <tr class="b"><td>Angebotspreis netto</td><td class="r">{eur(netto)}</td></tr>
    <tr><td>19 % MwSt.</td><td class="r">{eur(mwst)}</td></tr>
    <tr><td>{e(d.get('summe_zusatz', 'inkl. Lieferung und Montage in Berlin'))}</td><td class="r">✓</td></tr>
  </table>
  <div class="total"><small>Gesamtpreis brutto</small><b>{eur(brutto)}</b></div>
</div>
<h2>Zahlungsbedingungen</h2>
<table class="pay">
{pay}
</table>
<p class="note">{note}</p>
<div class="foot">
  <div class="hinw"><b>Hinweise:</b><ul>{hinw}</ul></div>
  <div class="greet2">Mit freundlichen Grüßen<br>Masar Werbeagentur<br><b>Amjad Alblili</b></div>
</div>
<div class="sign2">
  <div class="col">
    <b>Auftragnehmer</b>
    <div class="row">
      <div class="fld"><div class="val">Berlin, {e(d['datum'])}</div><div class="cap">Ort, Datum</div></div>
      <div class="fld st">{stempel}<div class="cap">Unterschrift &amp; Stempel</div></div>
    </div>
  </div>
  <div class="col">
    <b>Auftraggeber – Auftragserteilung</b>
    <div class="hint">Hiermit beauftragen wir das Angebot {nr} zu den oben genannten Bedingungen.<br><b class="alt">Alternativ genügt Ihre Bestätigung per E-Mail oder WhatsApp.</b></div>
    <div class="row">
      <div class="fld"><div class="val"></div><div class="cap">Ort, Datum</div></div>
      <div class="fld"><div class="val"></div><div class="cap">Unterschrift &amp; Stempel</div></div>
    </div>
  </div>
</div>
</div></body></html>
''', (netto, mwst, brutto, anz, rest)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    p = sys.argv[1]
    d = json.load(open(p, encoding='utf-8'))
    d['_pfad'] = os.path.abspath(p)
    aus = sys.argv[2] if len(sys.argv) > 2 else PRIVAT
    os.makedirs(aus, exist_ok=True)
    h, (netto, mwst, brutto, anz, rest) = bauen(d, aus)
    f = os.path.join(aus, d['nr'] + '.html')
    open(f, 'w', encoding='utf-8').write(h)
    subprocess.run(['node', os.path.join(HERE, 'pdf.mjs'), f, f[:-5] + '.pdf'], check=True)
    print(f'{f[:-5]}.pdf  netto {eur(netto)} · MwSt {eur(mwst)} · brutto {eur(brutto)} · Anzahlung {eur(anz)} · Rest {eur(rest)}')
