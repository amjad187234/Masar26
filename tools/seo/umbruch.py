"""Sauberer Text auf dem Handy (Wunsch Inhaber 03.11.2026):
1. Sichtbare Brotkrumen-Leiste („Home / Leistungen / …“) entfernen – das BreadcrumbList-JSON-LD für Google bleibt.
2. Keine Trennstriche in Wörtern: &shy; entfernen, hyphens:auto → manual.
3. Überschriften, deren längstes Wort nicht in die Zeile passt, werden per Skript kleiner gesetzt (statt zu trennen).
Idempotent (Marker). Am Ende der Pipeline ausführen: python3 tools/seo/umbruch.py
"""
import os, re, glob

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
AUSNAHMEN = ('admin/', 'tools/', 'node_modules/', 'data/')
A, Z = '<!-- umbruch:start -->', '<!-- umbruch:ende -->'
BLOCK = (A + '\n<style>h1,h2,h3,h4,h5,p,li,a,span,figcaption,td,th,.sec-title,.ph-title{-webkit-hyphens:manual!important;hyphens:manual!important}.nw{white-space:nowrap}'
         'h1,h2,h3,h4,.sec-title,.ph-title{overflow-wrap:normal!important;word-break:normal!important}</style>\n'
         '<script>(function(){function fit(){document.querySelectorAll("h1,h2,h3,.sec-title,.ph-title,.hero h1").forEach(function(h){'
         'h.style.fontSize="";if(h.clientWidth<40)return;var s=parseFloat(getComputedStyle(h).fontSize),min=s*0.45,n=0;'
         'while(h.scrollWidth>h.clientWidth+1&&s>min&&n<30){s*=0.94;h.style.fontSize=s+"px";n++;}});}'
         'var t;window.addEventListener("resize",function(){clearTimeout(t);t=setTimeout(fit,150);});'
         'if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fit);'
         'document.addEventListener("DOMContentLoaded",fit);window.addEventListener("load",fit);})();</script>\n' + Z + '\n')
WORT = re.compile(r'(?<![\w-])([A-Za-zÄÖÜäöüß0-9]+(?:-[A-Za-zÄÖÜäöüß0-9]+)+)(?![\w-])')
H = re.compile(r'(<h[1-4]\b[^>]*>)(.*?)(</h[1-4]>)', re.S)


def zusammen(m):
    teile = re.split(r'(<[^>]+>)', m.group(2)); offen = False
    for i, t in enumerate(teile):
        if t.startswith('<'):
            if t.startswith('<span class="nw"'): offen = True
            elif offen and t == '</span>': offen = False
            continue
        if not offen: teile[i] = WORT.sub(r'<span class="nw">\1</span>', t)
    return m.group(1) + ''.join(teile) + m.group(3)


BC = re.compile(r'[ \t]*<nav aria-label="Breadcrumb"[^>]*>.*?</nav>\n?', re.S)


def main():
    n = 0
    for p in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
        if os.path.relpath(p, ROOT).startswith(AUSNAHMEN): continue
        s = open(p, encoding='utf-8').read()
        neu = BC.sub('', s)
        neu = H.sub(zusammen, neu)   # Bindestrich-Wörter (Berlin-Wedding) in Überschriften nicht am Strich umbrechen
        neu = neu.replace('&shy;', '').replace('­', '')
        neu = re.sub(r'(-webkit-)?hyphens:\s*auto', lambda m: (m.group(1) or '') + 'hyphens:manual', neu)
        neu = re.sub(re.escape(A) + r'.*?' + re.escape(Z) + r'\n?', '', neu, flags=re.S)
        if '</head>' in neu:
            neu = neu.replace('</head>', BLOCK + '</head>', 1)
        if neu != s:
            open(p, 'w', encoding='utf-8').write(neu); n += 1
    print(n, 'Seiten angepasst')


if __name__ == '__main__':
    main()
