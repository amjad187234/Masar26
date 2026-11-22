"""Illustrationen für schaufensterfolie-store-eroeffnung.html (neutrale Beispielmarke, keine echten Projekte).
Schreibt hero.html und phasen.html ins aktuelle Verzeichnis; mit Playwright als 1080×1350 bzw. 1600×960 fotografieren und als
opening-soon-front(.webp, -720, -540, -360) und opening-soon-phasen(.webp, -720) im Wurzelverzeichnis ablegen.
Ersetzen, sobald echte Projektfotos mit Erlaubnis des Kunden vorliegen."""
# Illustrationen für die Seite "Schaufensterfolie zur Store-Eröffnung" (keine echten Projekte, neutrale Beispielmarke)
FONT="font-family:'Barlow Condensed','Barlow',Arial,sans-serif"
def front(x,y,w,h,phase,label=True,scale=1.0):
    """Ladenfront: 2 Schaufenster + Tür, Oberlichter. phase: 'bau' (blickdicht/Ankündigung), 'soon' (Farbe+Schrift), 'offen' (Farbe ohne Schrift), 'frei' (Glas frei)"""
    g=[]; pad=w*0.035; top=h*0.20; base=h*0.07
    g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#e9e4dc"/>')                       # Fassade
    g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h*0.13}" fill="#132e50"/>')                    # Blende oben
    g.append(f'<rect x="{x}" y="{y+h-base}" width="{w}" height="{base}" fill="#c9c3b8"/>')              # Sockel
    ww=(w-4*pad)*0.38; dw=(w-4*pad)*0.24; gy=y+top; gh=h-top-base; ol=gh*0.24
    xs=[x+pad, x+2*pad+ww, x+3*pad+ww+dw]; ws=[ww,dw,ww]
    for i,(px,pw) in enumerate(zip(xs,ws)):
        tuer = i==1
        for (py,ph,ober) in ((gy,ol-8,True),(gy+ol,gh-ol,False)):
            g.append(f'<rect x="{px-5}" y="{py-5}" width="{pw+10}" height="{ph+10}" fill="#f6f4ef"/>')  # Rahmen
            innen = '#f3d9a8' if phase!='bau' else '#d9d4c8'
            g.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="url(#innen)"/>' if phase in('frei',) else f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="{innen}"/>')
            if phase=='frei':
                # Blick in den Laden
                if not ober:
                    g.append(f'<rect x="{px+pw*0.12}" y="{py+ph*0.55}" width="{pw*0.76}" height="{ph*0.06}" fill="#b98f5a"/>')
                    for k in range(3 if not tuer else 1):
                        cx=px+pw*(0.25+0.25*k) if not tuer else px+pw*0.5
                        g.append(f'<rect x="{cx-pw*0.06}" y="{py+ph*0.25}" width="{pw*0.12}" height="{ph*0.30}" rx="6" fill="#132e50" opacity=".75"/>')
            elif phase=='bau':
                g.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="#132e50"/>')
            else:
                g.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="#17a08d" opacity=".86"/>')
                g.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="url(#glanz)"/>')
            if tuer and not ober:
                g.append(f'<rect x="{px+pw*0.82}" y="{py+ph*0.42}" width="{pw*0.05}" height="{ph*0.16}" rx="3" fill="#8a8f96"/>')
        # Beschriftung
        cy=gy+ol+(gh-ol)*0.50; cx=px+pw/2
        if phase in('soon','bau') and not tuer:
            col='#0d2238' if phase=='soon' else '#ffffff'
            g.append(f'<text x="{cx}" y="{cy}" text-anchor="middle" style="{FONT};font-weight:800;font-size:{pw*0.150*scale}px;letter-spacing:{pw*0.012}px" fill="{col}">IHRE MARKE</text>')
            g.append(f'<text x="{cx}" y="{cy+pw*0.115}" text-anchor="middle" style="{FONT};font-weight:600;font-size:{pw*0.074*scale}px;letter-spacing:{pw*0.014}px" fill="{col}">OPENING SOON</text>')
            g.append(f'<text x="{cx}" y="{gy+gh-pw*0.07}" text-anchor="middle" style="{FONT};font-weight:500;font-size:{pw*0.040*scale}px;letter-spacing:{pw*0.010}px" fill="{col}" opacity=".9">IHREMARKE.DE</text>')
        if phase in('soon','bau') and tuer:
            col='#0d2238' if phase=='soon' else '#ffffff'
            r=pw*0.16
            g.append(f'<circle cx="{cx}" cy="{cy-r*0.4}" r="{r}" fill="none" stroke="{col}" stroke-width="{r*0.16}"/>')
            g.append(f'<path d="M{cx-r*0.45} {cy-r*0.4} l{r*0.32} {r*0.34} l{r*0.6} -{r*0.72}" fill="none" stroke="{col}" stroke-width="{r*0.16}" stroke-linecap="round" stroke-linejoin="round"/>')
        if phase=='offen' and not tuer:
            pass
    return '\n'.join(g)
DEFS='''<defs>
<linearGradient id="glanz" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".10"/></linearGradient>
<linearGradient id="innen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbe7c2"/><stop offset="1" stop-color="#f1cf96"/></linearGradient>
<linearGradient id="himmel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#132e50"/><stop offset="1" stop-color="#1d4a63"/></linearGradient>
</defs>'''
def seite(svg,w,h): return f'<html><head><style>@font-face{{font-family:"Barlow Condensed";font-weight:800;src:url("file:///home/user/Masar26/fonts/barlow-condensed-black.woff2")}}@font-face{{font-family:"Barlow";font-weight:500;src:url("file:///home/user/Masar26/fonts/barlow-medium.woff2")}}@font-face{{font-family:"Barlow";font-weight:600;src:url("file:///home/user/Masar26/fonts/barlow-semibold.woff2")}}html,body{{margin:0}}</style></head><body><svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}{svg}</svg></body></html>'
# 1) Hero 1080x1350
W,H=1080,1350
s=f'<rect width="{W}" height="{H}" fill="url(#himmel)"/>'
s+=f'<rect x="0" y="{H-210}" width="{W}" height="210" fill="#2b3f52"/><rect x="0" y="{H-210}" width="{W}" height="14" fill="#3b566c"/>'
s+=front(60,300,960,850,'soon')
s+=f'<text x="{W/2}" y="150" text-anchor="middle" style="{FONT};font-weight:800;font-size:64px;letter-spacing:3px" fill="#58d0bd">VOR DER ERÖFFNUNG</text>'
s+=f'<text x="{W/2}" y="215" text-anchor="middle" style="font-family:Barlow,Arial,sans-serif;font-weight:500;font-size:30px" fill="#d8e6ee">Farbige Folie innen · Logo und Schrift außen</text>'
s+=f'<text x="{W/2}" y="{H-70}" text-anchor="middle" style="font-family:Barlow,Arial,sans-serif;font-weight:500;font-size:24px" fill="#9fb4c2">Illustration – Beispielmarke</text>'
open('hero.html','w').write(seite(s,W,H))
# 2) Phasen 1600x960
W,H=1600,960
s=f'<rect width="{W}" height="{H}" fill="#f4f7f7"/>'
titel=[('1 · Vor der Eröffnung','Farbfläche mit Logo und Schriftzug','soon'),('2 · Eröffnung','Schriftzug ab, Farbfläche bleibt','offen'),('3 · Danach','Folie entfernt, Glas wieder frei','frei')]
bw=470; gap=(W-3*bw)/4
for i,(t,u,ph) in enumerate(titel):
    x=gap+i*(bw+gap)
    s+=f'<rect x="{x-14}" y="150" width="{bw+28}" height="650" rx="18" fill="#fff" stroke="#dfe7ea"/>'
    s+=front(x,230,bw,440,ph)
    s+=f'<text x="{x+bw/2}" y="205" text-anchor="middle" style="{FONT};font-weight:800;font-size:40px;letter-spacing:1px" fill="#132e50">{t.upper()}</text>'
    s+=f'<text x="{x+bw/2}" y="735" text-anchor="middle" style="font-family:Barlow,Arial,sans-serif;font-weight:600;font-size:25px" fill="#177567">{u}</text>'
    if i<2: s+=f'<path d="M{x+bw+gap*0.5-16} 450 l28 22 l-28 22" fill="none" stroke="#58d0bd" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'
s+=f'<text x="{W/2}" y="90" text-anchor="middle" style="{FONT};font-weight:800;font-size:54px;letter-spacing:2px" fill="#132e50">EINE FRONT, DREI PHASEN</text>'
s+=f'<text x="{W/2}" y="890" text-anchor="middle" style="font-family:Barlow,Arial,sans-serif;font-weight:500;font-size:24px" fill="#5b6b7a">Illustration – Beispielmarke</text>'
open('phasen.html','w').write(seite(s,W,H))
