"""Folien-Landingpages (Fensterfolie-Hub, Sonnenschutz, Sicherheit, Sichtschutz).
Nutzt die Helfer aus branchen/gen_branchen.py (Vorlage schilder-berlin.html), aber ohne Pakete."""
import os, re, json, sys
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, '..', 'branchen', 'gen_branchen.py'), encoding='utf-8').read()
exec(src[:src.index('\nimport pages')])  # HEAD_A, HEAD_B, FOOT, I, SVC, svg, esc, wa, sec …

SVC.update({
 'sonne': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
 'schutz': '<path d="M12 3 20 6v6c0 4.5-3.4 7.8-8 9-4.6-1.2-8-4.5-8-9V6Z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
 'thermo': '<path d="M14 14.8V5a2 2 0 0 0-4 0v9.8a4 4 0 1 0 4 0Z"/><path d="M12 9v7"/>',
 'spiegel': '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="m8 9 3-3M8 14l7-7M12 16l4-4"/>',
})

def head_f(p):
    url = BASE + p['file']; t = esc(p['title']); d = esc(p['desc'])
    svc = {"@context": "https://schema.org", "@type": "Service", "serviceType": p['service_type'], "name": p['schema_name'],
           "description": p['desc'], "url": url, "areaServed": p.get('area', [{"@type": "City", "name": "Berlin"}]),
           "provider": {"@type": "LocalBusiness", "@id": BASE + "#identity", "name": "Masar Werbeagentur", "telephone": "+49 178 5143918",
                        "address": {"@type": "PostalAddress", "streetAddress": "Bristolstraße 19E", "postalCode": "13349", "addressLocality": "Berlin", "addressCountry": "DE"}}}
    items = [("Home", BASE), ("Leistungen", BASE + "leistungen.html")]
    if p['file'] != 'fensterfolie-berlin.html':
        pn, pf = p.get('parent', ('Fensterfolien', 'fensterfolie-berlin.html'))
        items.append((pn, BASE + pf))
    items.append((p['crumb'], url))
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
          {"@type": "ListItem", "position": i, "name": n, "item": u} for i, (n, u) in enumerate(items, 1)]}
    fq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
          {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', a)}} for q, a in p['faq']]}
    js = lambda o: '<script type="application/ld+json">\n' + json.dumps(o, ensure_ascii=False, indent=2) + '\n</script>\n'
    meta = f'''<title>{t}</title>
<meta name="description" content="{d}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="robots" content="index, follow">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://masar-werbeagentur.de/logo.png">
<meta property="og:locale" content="de_DE">
<meta property="og:site_name" content="Masar Werbeagentur Berlin">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="https://masar-werbeagentur.de/logo.png">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="de" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
'''
    return HEAD_A + meta + js(svc) + js(bc) + js(fq) + HEAD_B

def table(caption, cols, rows):
    th = ''.join(f'<th scope="col">{c}</th>' for c in cols)
    tr = ''.join('\n          <tr>' + ''.join(f'<td data-label="{cols[i]}">{v}</td>' for i, v in enumerate(r)) + '</tr>' for r in rows)
    return f'''    <div class="price-scroll">
      <table class="price-table rt">
        <caption class="sr-only" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);">{esc(caption)}</caption>
        <thead><tr>{th}</tr></thead>
        <tbody>{tr}
        </tbody>
      </table>
    </div>'''

def items(lst):
    return ''.join(f'''
      <div class="why-item">
        <div class="why-num">{n}</div>
        <div><h4>{h}</h4><p>{t}</p></div>
      </div>''' for n, (h, t) in enumerate(lst, 1))

def build_f(p):
    w = wa(p['wa'])
    crumbs = '<li><a href="/">Home</a></li>\n      <li class="bc-sep">/</li>\n      <li><a href="/leistungen.html">Leistungen</a></li>\n      <li class="bc-sep">/</li>\n      '
    if p['file'] != 'fensterfolie-berlin.html':
        pn, pf = p.get('parent', ('Fensterfolien', 'fensterfolie-berlin.html'))
        crumbs += f'<li><a href="/{pf}">{pn}</a></li>\n      <li class="bc-sep">/</li>\n      '
    crumbs += f'<li><span class="bc-cur">{p["crumb"]}</span></li>'
    hero = f'''<section class="hero" id="main-content" role="main" tabindex="-1">
  <div class="hero-lines"></div>
  <div class="container">
    <div class="hero-inner">
      <div>
        <div class="hero-badge">{I['star']}{p['badge']}</div>
        <h1>{p['h1']}</h1>
        <p class="hero-sub">{p['sub']}</p>
        <div class="hero-btns">
          <a href="#kontakt" class="btn btn-teal">Angebot anfordern</a>
          <a href="{w}" target="_blank" rel="noopener noreferrer" class="btn btn-outline">{I['wa']}Foto per WhatsApp schicken</a>
        </div>
        <div class="hero-trust">
          <span class="hero-trust-txt">{p['trust']}</span>
        </div>
      </div>
      <div class="hero-visual">
        <img class="hero-shot" src="/{p['img']}-720.webp{p.get('img_q', '')}" srcset="/{p['img']}-360.webp{p.get('img_q', '')} 360w, /{p['img']}-540.webp{p.get('img_q', '')} 540w, /{p['img']}-720.webp{p.get('img_q', '')} 720w, /{p['img']}.webp{p.get('img_q', '')} 1080w" sizes="360px" width="1080" height="1350" alt="{esc(p['img_alt'])}" loading="eager" fetchpriority="high">
      </div>
    </div>
  </div>
</section>

<nav aria-label="Breadcrumb" class="bc-bar">
  <div class="container">
    <ol class="bc-list">
      {crumbs}
    </ol>
  </div>
</nav>

<div style="background:var(--teal);padding:.9rem 0;">
  <div class="container">
    <div class="usp-row">{''.join(f'<span>{I["check"]}{u}</span>' for u in p['usp'])}</div>
  </div>
</div>
'''
    out = hero
    if p['file'] == 'fensterfolie-berlin.html':
        out += f'''<section class="section bg-alt" id="finder">
  <div class="container">
    <div class="sec-head center reveal">
      <span class="eyebrow">{I['star']}Folien-Finder</span>
      <h2 class="sec-title">Welche Folie <em>brauchen Sie?</em></h2>
      <p class="sec-sub">Zwei Fragen, und Sie wissen, welche Folie passt – Ihre Anfrage schicken Sie danach direkt per WhatsApp oder E-Mail.</p>
    </div>
    <div data-assistent data-start="fensterfolie"></div>
  </div>
</section>
'''
    elif p.get('finder_strip', True):
        out += '''<div style="background:var(--off);border-bottom:1px solid var(--border);padding:1rem 0;">
  <div class="container" style="text-align:center;font-size:15px;color:var(--muted);">
    Nicht sicher, ob das die richtige Folie ist? <a href="/fensterfolie-berlin.html#finder" style="color:var(--teal-ink);font-weight:700;">Zum Folien-Finder →</a>
  </div>
</div>
'''
    if p.get('top'):
        ey, h2, sub, body = p['top']
        out += sec(ey, h2, sub, body, sid='preise', icon='tag')
    out += sec(p['angles_ey'], p['angles_h2'], p['angles_sub'], f'    <div class="why-grid">{items(p["angles"])}\n    </div>')
    if p.get('ref'):
        r = p['ref']
        out = out[:out.rindex('  </div>\n</section>')] + f'''    <figure class="reveal" style="margin:2.5rem auto 0;max-width:900px;display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:1.5rem;align-items:center;background:#fff;border:1px solid var(--border);border-radius:var(--r);overflow:hidden" id="referenz">
      <a href="/referenzen.html" style="display:block"><img src="{r['src720']}" srcset="{r['src720']} 720w, {r['src']} 1200w" sizes="(max-width:700px) 100vw, 500px" width="{r['w']}" height="{r['h']}" alt="{esc(r['alt'])}" loading="lazy" style="width:100%;height:auto;display:block"></a>
      <figcaption style="padding:1.5rem 1.5rem 1.5rem 0;color:var(--muted);font-size:15px;line-height:1.65">
        <span class="eyebrow" style="margin-bottom:.6rem">Aus unserer Arbeit</span>
        <strong style="display:block;color:var(--navy);font-size:1.15rem;margin-bottom:.4rem">{r['title']}</strong>
        {r['text']}
        <a href="/referenzen.html" style="display:block;margin-top:.8rem;color:var(--teal-ink);font-weight:700">Weitere Referenzen ansehen →</a>
      </figcaption>
    </figure>
    <style>@media(max-width:700px){{#referenz{{grid-template-columns:1fr!important;gap:0!important}}#referenz figcaption{{padding:1.25rem!important}}}}</style>
''' + out[out.rindex('  </div>\n</section>'):]
    if p.get('gallery'):
        g = p['gallery']
        figs = ''.join(f'''
      <figure style="margin:0;background:#fff;border:1px solid var(--border);border-radius:var(--r);overflow:hidden;display:flex;flex-direction:column">
        <img src="{src}" width="{w}" height="{h}" alt="{esc(alt)}" loading="lazy" decoding="async" style="width:100%;aspect-ratio:4/3;object-fit:cover;display:block{';object-position:top' if top else ''}">
        <figcaption style="padding:.9rem 1.1rem;font-size:14.5px;line-height:1.55;color:var(--muted)">{cap}</figcaption>
      </figure>''' for src, w, h, alt, cap, top in g['items'])
        out += sec(g.get('ey', 'Aus unserer Arbeit'), g['h2'], g.get('sub'), f'''    <div class="reveal" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1.25rem">{figs}
    </div>
    <p class="price-note" style="text-align:center;margin-top:1.25rem">{g.get('note', '<a href="/referenzen.html">Alle Referenzen ansehen →</a>')}</p>''', alt=True, icon='star')
    out += sec(p.get('tab_ey', 'Folienarten'), p['tab_h2'], p['tab_sub'], table(p['crumb'] + ' – Folienarten', p['tab_cols'], p['tab_rows'])
               + (f'\n    <p class="price-note">{p["tab_note"]}</p>' if p.get('tab_note') else ''), alt=True, icon='tag')
    if p.get('extra'):
        ey, h2, sub, body = p['extra']
        out += sec(ey, h2, sub, body, icon='check')
    cards = ''.join(f'''
      <a href="{h}" class="svc-card" style="text-decoration:none;color:inherit;display:block;">
        <div class="svc-icon">{svg(ic)}</div>
        <h3>{t}</h3>
        <p>{d}</p>
      </a>''' for ic, t, d, h in p['services'])
    out += sec('Einsatzbereiche', p['svc_h2'], p['svc_sub'], f'    <div class="svc-grid"' + (' style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr));"' if len(p['services']) == 4 else '') + f'>{cards}\n    </div>')
    out += sec('Preise', p['preis_h2'], None, f'''    <div class="blog-prose" style="max-width:820px;margin:0 auto;">
{p['preis_html']}
    </div>''', alt=True, sid='kosten' if p.get('top') else 'preise', icon='tag')
    out += sec(p['recht_ey'], p['recht_h2'], p['recht_sub'], f'''    <div class="blog-prose" style="max-width:820px;margin:0 auto;">
{p['recht_html']}
    </div>''', icon='doc')
    out += sec('Ablauf', 'So läuft es <em>ab</em>', None, f'    <div class="why-grid">{items(p["ablauf"])}\n    </div>', alt=True)
    fq = ''.join(f'\n      <div class="faq-item"><button class="faq-q">{q}</button><div class="faq-a"><p>{a}</p></div></div>' for q, a in p['faq'])
    out += sec('Häufige Fragen', p['faq_h2'], None, f'    <div class="faq-wrap">{fq}\n    </div>', icon='faq')
    chips = ''.join(f'\n      <a href="{h}" class="chip">{t}</a>' for h, t in p['links'])
    out += f'''<section class="section bg-alt" style="padding:2.5rem 0;">
  <div class="container">
    <div class="sec-head reveal" style="margin-bottom:1.5rem;">
      <span class="eyebrow">{I['link']}Passend dazu</span>
      <h2 class="sec-title" style="font-size:clamp(1.5rem,3vw,2.2rem);">Ratgeber &amp; <em>Leistungen</em></h2>
    </div>
    <div class="chip-row">{chips}
    </div>
  </div>
</section>
'''
    opts = ''.join(f'\n            <option>{o}</option>' for o in p['form_opts'])
    FL = p.get('form_labels', ('Welche Folie?', 'Fenster &amp; Wunsch', 'Foto der Fenster (optional)', 'Ein Foto pro Fenster und ungefähre Maße reichen für eine erste Einschätzung. Gut ist auch ein Foto vom Stempel in der Scheibenecke, falls vorhanden.'))
    out += f'''<section class="section" id="kontakt">
  <div class="container">
    <div class="sec-head reveal">
      <span class="eyebrow">{I['mail']}Anfrage</span>
      <h2 class="sec-title">Kostenloses Angebot <em>anfordern</em></h2>
      <p class="sec-sub">{p['form_sub']}</p>
    </div>
    <div class="form-wrap">
      <form action="/kontakt.php" method="POST" enctype="multipart/form-data">
        <input type="hidden" name="_subject" value="{esc(p['subject'])}">
        <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
        <div class="form-grid">
          <div class="fg"><label for="fo-name">Name *</label><input type="text" id="fo-name" name="name" autocomplete="name" placeholder="Vor- und Nachname" required></div>
          <div class="fg"><label for="fo-firma">Firma <span style="font-weight:400;color:var(--muted);">(falls gewerblich)</span></label><input type="text" id="fo-firma" name="firma" autocomplete="organization" placeholder="optional"></div>
        </div>
        <div class="form-grid">
          <div class="fg"><label for="fo-email">E-Mail *</label><input type="email" id="fo-email" name="email" autocomplete="email" placeholder="info@beispiel.de" required></div>
          <div class="fg"><label for="fo-telefon">Telefon / WhatsApp</label><input type="tel" id="fo-telefon" name="telefon" autocomplete="tel" placeholder="+49 ..."></div>
        </div>
        <div class="form-grid">
          <div class="fg">
            <label for="fo-folie">{FL[0]}</label>
            <select id="fo-folie" name="folie">
              <option value="">Bitte wählen...</option>{opts}
              <option>Noch nicht entschieden – bitte beraten</option>
            </select>
          </div>
          <div class="fg"><label for="fo-ort">Ort / Bezirk</label><input type="text" id="fo-ort" name="ort" placeholder="z. B. Berlin-Mitte"></div>
        </div>
        <div class="fg"><label for="fo-nachricht">{FL[1]}</label><textarea id="fo-nachricht" name="nachricht" placeholder="{esc(p['msg_ph'])}"></textarea></div>
        <div class="fg"><label for="fo-datei">{FL[2]}</label><input type="file" id="fo-datei" name="attachment" accept="image/*,.pdf" style="background:#fff;border:1px dashed var(--border);border-radius:8px;padding:11px 14px;color:var(--muted);font-family:'Barlow',sans-serif;font-size:14px;width:100%;cursor:pointer;"><p style="font-size:12.5px;color:var(--muted);line-height:1.6;margin-top:.45rem;">{FL[3]}</p></div>
        <div class="consent-row">
          <input type="checkbox" id="fo-consent" name="consent" required>
          <label for="fo-consent">Ich habe die <a href="/datenschutz.html">Datenschutzerklärung</a> zur Kenntnis genommen und stimme der Verarbeitung meiner Daten zu (Art.&nbsp;6 Abs.&nbsp;1 lit.&nbsp;b DSGVO). *</label>
        </div>
        <button type="submit" class="submit-btn">✓ Anfrage senden – kostenlos &amp; unverbindlich</button>
        <p style="text-align:center;font-size:12px;color:var(--muted);margin-top:.6rem;">Kein Spam. Ihre Daten werden vertraulich behandelt. Antwort innerhalb von 24 Stunden.</p>
      </form>
    </div>
  </div>
</section>
'''
    html_out = head_f(p) + out + '\n' + FOOT
    if p.get('hero_mobile'):
        html_out = html_out.replace('</head>', '<style>@media(max-width:900px){.hero-visual{display:block!important;margin-top:1.8rem}.hero-visual .hero-shot{width:100%;max-width:340px;height:auto;margin:0 auto;display:block;transform:none}}</style>\n</head>', 1)
    if p['file'] == 'fensterfolie-berlin.html':
        html_out = html_out.replace('</body>', '<script src="/assistent.js?v=6" defer></script>\n</body>', 1)
    html_out = re.sub(r'<div class="scta-txt">.*?</div>', f'<div class="scta-txt">{I["star"]}<span>{p["sticky"][0]}</span> – {p["sticky"][1]}</div>', html_out, count=1, flags=re.S)
    html_out = html_out.replace('<a href="tel:01785143918" class="scta-btn primary">', f'<a href="{w}" target="_blank" rel="noopener noreferrer" class="scta-btn primary">', 1)
    html_out = re.sub(r'(<a href="https://wa\.me/[^"]*" target="_blank" rel="noopener noreferrer" class="scta-btn primary">)<svg.*?</svg>0178 514 3918', lambda m: m.group(1) + I['wa'] + 'WhatsApp', html_out, count=1, flags=re.S)
    open(ROOT + p['file'], 'w', encoding='utf-8').write(html_out)
    try:
        import importlib.util as _u
        _sp = _u.spec_from_file_location('add_assistent', os.path.join(os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else HERE, '..', 'add_assistent.py'))
        _m = _u.module_from_spec(_sp); _sp.loader.exec_module(_m)
        if p['file'] in _m.M: _m.inject(p['file'], *_m.M[p['file']])
    except Exception as _e:
        print('Assistent-Einbau übersprungen:', _e)
    return p['file'], len(html_out)

if __name__ == '__main__':
    sys.path.insert(0, HERE)
    import folien_pages
    for p in folien_pages.PAGES:
        print(build_f(p))
