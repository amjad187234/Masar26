"""Werbevideos (tools/video/werbevideos.mjs → /videos/werbung-*.mp4|webm|webp) auf den passenden Leistungsseiten einbauen.
Abschnitt direkt nach dem Seitenkopf (vor dem ersten Inhaltsabschnitt), Video stumm, startet beim Sichtbarwerden,
bei „weniger Bewegung“ nur mit Bedienelementen. Marker werbevideo, Block wird an Ort und Stelle erneuert. Idempotent.
Aufruf: python3 tools/seo/werbevideo_einbau.py
"""
import os, re
ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))).rstrip('/')
A, Z = '<!-- werbevideo:start -->', '<!-- werbevideo:ende -->'
V = '2'   # nach neu gerenderten Videos erhöhen (Videos werden 6 Monate im Browser gehalten)
SEITEN = {
    'leuchtreklame-berlin.html': ('werbung-leuchtreklame-berlin', 'Leuchtreklame aus unseren Projekten', 'Fassadenanlagen, Leuchtausleger und Leuchtbuchstaben – geplant von uns, gebaut von eingetragenen Partnerbetrieben.', 'Video: Leuchtreklame-Projekte von Masar in Berlin'),
    'schaufensterbeschriftung-berlin.html': ('werbung-schaufenster-berlin', 'Schaufenster aus unseren Projekten', 'Beschriftung, Milchglas und bedruckte Folie – für Praxen, Fahrschulen, Pflegedienste und Läden.', 'Video: Schaufenster-Projekte von Masar in Berlin'),
    'fahrzeugbeschriftung-berlin.html': ('werbung-fahrzeugbeschriftung-berlin', 'Fahrzeuge aus unseren Projekten', 'Vom Transporter mit Leistungsübersicht bis zur Vollfolierung eines Imbisswagens.', 'Video: Fahrzeugbeschriftungen von Masar in Berlin'),
}
SKRIPT = ('<script>(function(){var vs=document.querySelectorAll(".mv-v");if(!vs.length)return;'
          'var rm=window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches;'
          'vs.forEach(function(v){if(rm||!("IntersectionObserver"in window)){v.controls=true;return;}'
          'new IntersectionObserver(function(e){e.forEach(function(x){if(x.isIntersecting){v.preload="auto";v.play().catch(function(){v.controls=true;});}else{v.pause();}});},{threshold:.3}).observe(v);});})();</script>')


def block(name, titel, text, label):
    return (f'{A}\n<section class="section" style="padding:3rem 0 1rem"><div class="container">\n'
            f'<figure style="margin:0 auto;max-width:1000px;border-radius:16px;overflow:hidden;background:#132e50;box-shadow:0 14px 40px rgba(19,46,80,.18)">'
            f'<video class="mv-v" poster="/videos/{name}.webp" width="1280" height="720" muted loop playsinline preload="none" aria-label="{label}" '
            f'style="display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover">'
            f'<source src="/videos/{name}.webm?v={V}" type="video/webm"><source src="/videos/{name}.mp4?v={V}" type="video/mp4"></video>'
            f'<figcaption style="padding:1rem 1.3rem;color:#fff;font-size:15px;line-height:1.6"><strong style="font-family:\'Barlow Condensed\',\'Barlow Condensed Fallback\',sans-serif;font-weight:900;text-transform:uppercase;letter-spacing:.3px;font-size:1.15rem;color:#58d0bd;display:block">{titel}</strong>{text}</figcaption>'
            f'</figure>\n</div></section>\n{SKRIPT}\n{Z}\n')


def main():
    n = 0
    for f, (name, titel, text, label) in SEITEN.items():
        p = os.path.join(ROOT, f)
        if not os.path.exists(p) or not os.path.exists(os.path.join(ROOT, 'videos', name + '.mp4')): continue
        s = open(p, encoding='utf-8').read(); alt = s; b = block(name, titel, text, label)
        s, k = re.subn(re.escape(A) + r'.*?' + re.escape(Z) + r'\n', lambda m: b, s, count=1, flags=re.S)
        if not k:
            h = re.search(r'<section[^>]*class="hero[^"]*"', s)
            if not h: print('kein Hero:', f); continue
            m = re.search(r'<section\b', s[h.end():])
            if not m: print('kein Abschnitt:', f); continue
            i = h.end() + m.start()
            s = s[:i] + b + s[i:]
        if s != alt: open(p, 'w', encoding='utf-8').write(s); n += 1
    print(n, 'Seiten mit Werbevideo')


if __name__ == '__main__':
    main()
