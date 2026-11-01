"""Kurze Angebotsbox direkt nach der Einleitung jedes Ratgebers (vor der ersten Zwischenüberschrift).
Ratgeber haben die meisten Impressionen; die große Box steht erst am Ende. Text und Link kommen aus der
vorhandenen .article-cta des Artikels (keine neuen Preise/Zusagen). Idempotent (Marker).
Aufruf: python3 tools/seo/blog_kurzbox.py
"""
import os, re, glob, html

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
A, Z = '<!-- kurzbox:start -->', '<!-- kurzbox:ende -->'
CSS = ('<style id="kurzbox">.kurzbox{display:flex;align-items:center;justify-content:space-between;gap:.8rem 1.2rem;flex-wrap:wrap;'
       'background:rgba(88,208,189,.1);border:1px solid rgba(88,208,189,.45);border-left:4px solid #58d0bd;border-radius:10px;'
       'padding:.9rem 1.1rem;margin:1.6rem 0}.kurzbox p{margin:0!important;font-size:15px;color:var(--navy,#132e50);line-height:1.5}'
       '.kurzbox p span{display:block;color:var(--muted,#5a7070);font-size:13.5px}.kurzbox .kb-btns{display:flex;gap:.5rem;flex-wrap:wrap}'
       '.kurzbox a{display:inline-block;padding:9px 14px;border-radius:8px;font-weight:700;font-size:14px;text-decoration:none;white-space:nowrap}'
       '.kurzbox .kb-go{background:#58d0bd;color:#132e50}.kurzbox .kb-wa{background:#25d366;color:#fff}</style>')


def main():
    n = 0
    for p in glob.glob(os.path.join(ROOT, 'blog', '*.html')):
        s = open(p, encoding='utf-8').read()
        s = re.sub(re.escape(A) + r'.*?' + re.escape(Z) + r'\n?', '', s, flags=re.S)
        cta = re.search(r'<div class="article-cta">\s*<h3>(.*?)</h3>.*?<a href="(/[^"]+)"[^>]*class="btn-teal"[^>]*>.*?(?:<a href="(https://wa\.me/[^"]+)")?', s, re.S)
        body = s.find('<main class="article-body">')
        if not cta or body < 0: continue
        h2 = s.find('<h2', body)
        if h2 < 0: continue
        titel, link = cta.group(1).strip(), cta.group(2)
        wa = re.search(r'<div class="article-cta">.*?<a href="(https://wa\.me/[^"]+)"', s, re.S)
        wa_btn = f'<a class="kb-wa" href="{wa.group(1)}" target="_blank" rel="noopener noreferrer">WhatsApp</a>' if wa else ''
        box = (f'{A}<aside class="kurzbox" aria-label="Angebot"><p><b>{titel}</b>'
               f'<span>Wir übernehmen Gestaltung, Fertigung und Montage – Festpreis nach Fotos, Angebot in der Regel in 24 Stunden.</span></p>'
               f'<div class="kb-btns"><a class="kb-go" href="{link}">Mehr erfahren →</a>{wa_btn}</div></aside>{Z}\n    ')
        s = s[:h2] + box + s[h2:]
        if 'id="kurzbox"' not in s:
            s = s.replace('</head>', CSS + '\n</head>', 1)
        open(p, 'w', encoding='utf-8').write(s); n += 1
    print(n, 'Ratgeber mit Kurzbox')


if __name__ == '__main__':
    main()
