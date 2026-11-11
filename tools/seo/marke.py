"""Markenleitfaden auf die Website anwenden (tools/brand/brand_guide.html):
nur Navy, Teal, Teal dunkel, Grau, Off-White und Textfarbe – keine Gold- und Lila-Akzente mehr.
Ersetzt Farbwerte in allen öffentlichen HTML-Seiten (idempotent). Farbwahl-Muster (z. B. Messestand-Farben)
bleiben unberührt, weil sie Kundenfarben zeigen, nicht unsere Marke. Setzt außerdem den Claim „Werbung, die man sieht.“ über den Footer-Text.
Aufruf: python3 tools/seo/marke.py
"""
import os, re, glob

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
AUSNAHMEN = ('admin/', 'tools/', 'node_modules/', 'data/')
CLAIM = '<p class="foot-claim" style="font:900 21px/1.1 \'Barlow Condensed\',sans-serif;text-transform:uppercase;letter-spacing:.5px;color:#fff;margin:0 0 .55rem">Werbung, die <span style="color:#58d0bd">man sieht.</span></p>'

ERSETZEN = [
    # Gold-Akzent → Teal (Token-Wert, so bleiben alle var(--gold)-Stellen markenkonform)
    (re.compile(r'--gold:\s*#f5[bc][0-9a-f]00', re.I), '--gold:#58d0bd'),
    # Lila (früher „Digital“-Bereich) → Teal dunkel / Navy
    (re.compile(r'--purple:\s*#7c3aed', re.I), '--purple:#177567'),
    (re.compile(r'--purple-d:\s*#6d28d9', re.I), '--purple-d:#0e6455'),
    (re.compile(r'rgba\(124,\s*58,\s*237,', re.I), 'rgba(23,117,103,'),
    (re.compile(r'#1a0050', re.I), '#0e2340'),
    (re.compile(r'#2e1065', re.I), '#132e50'),
    (re.compile(r'#4c1d95', re.I), '#0d4a4a'),
    (re.compile(r'#7c3aed', re.I), '#177567'),
    (re.compile(r'#c4b5fd', re.I), '#a8eadf'),
    # Gelbe Hinweis-Etiketten → Teal
    (re.compile(r'background:#e8b931', re.I), 'background:#58d0bd'),
    # Brauner Verlauf (Druck-Kachel leistungen.html) → Navy/Teal dunkel
    (re.compile(r'linear-gradient\(135deg,\s*#451a03,\s*#854d0e\)', re.I), 'linear-gradient(135deg,#132e50,#177567)'),
    # Footer-Social: color für Icons mit stroke="currentColor" (Instagram) ergänzen, damit sie wie Facebook/WhatsApp (fill) aussehen – idempotent
    (re.compile(r'fill:rgba\(255,255,255,\.45\);\s*transition:fill \.25s;'),
     'fill:rgba(255,255,255,.45);color:rgba(255,255,255,.45);transition:fill .25s,color .25s;'),
    (re.compile(r'fill:rgba\(255,255,255,\.45\);\}'), 'fill:rgba(255,255,255,.45);color:rgba(255,255,255,.45);}'),
    (re.compile(r'\.fsoc:hover svg\s*\{\s*fill:var\(--teal\);\s*\}'), '.fsoc:hover svg{fill:var(--teal);color:var(--teal)}'),
]


def main():
    n = 0
    for p in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
        if os.path.relpath(p, ROOT).startswith(AUSNAHMEN): continue
        s = open(p, encoding='utf-8').read(); neu = s
        for muster, ersatz in ERSETZEN:
            neu = muster.sub(ersatz, neu)
        if 'foot-claim' not in neu and '<p class="foot-desc">' in neu:   # Claim (festgelegt 03.11.2026) im Footer
            neu = neu.replace('<p class="foot-desc">', CLAIM + '\n        <p class="foot-desc">', 1)
        if 'foot-claim' not in neu:   # schlichter Footer der Rechtsseiten (Impressum, Datenschutz, AGB): <div class="fb"> … <p>
            neu = re.sub(r'(<footer[^>]*>\s*<div class="fi">\s*<div class="fb">\s*<div class="fl">.*?</div>\s*)<p>',
                         lambda m: m.group(1) + CLAIM + '\n      <p>', neu, count=1, flags=re.S)
        if neu != s:
            open(p, 'w', encoding='utf-8').write(neu); n += 1
    print(n, 'Seiten an den Markenleitfaden angepasst')


if __name__ == '__main__':
    main()
