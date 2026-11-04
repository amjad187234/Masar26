"""SEO-Prüfung aller öffentlichen Seiten – nur lesen, nichts ändern.

    python3 tools/seo/seo_check.py            alle Befunde
    python3 tools/seo/seo_check.py --kurz     nur Zusammenfassung je Regel
    python3 tools/seo/seo_check.py --regel og-logo,img-dim   nur bestimmte Regeln
    python3 tools/seo/seo_check.py seite.html blog/x.html    nur diese Seiten

Geprüft (Google Search Essentials, Richtlinien für strukturierte Daten, Core Web Vitals):
Titel (vorhanden, ≤ 60 Zeichen, eindeutig), Beschreibung (70–160, eindeutig), genau eine H1,
Canonical (absolut, zeigt auf die eigene URL), hreflang (de + x-default, gleiche URL wie Canonical),
Open Graph (Bild vorhanden/lokal, nicht nur Logo), JSON-LD (gültiges JSON, @context, LocalBusiness-@id,
FAQPage nur bei sichtbaren Fragen, BreadcrumbList-Ziele vorhanden), Bilder (alt, width/height, lazy unterhalb,
kein lazy beim ersten Bild, Datei vorhanden, WebP-Variante), interne Links (Ziel vorhanden), verwaiste Seiten,
sitemap.xml (vollständig, keine noindex-/fehlenden Seiten, lastmod), robots.txt, llms.txt (Links gültig).
Exit-Code 1 bei Fehlern (F), 0 wenn nur Hinweise (H).
"""
import os, re, sys, json, glob, html, subprocess
from html.parser import HTMLParser
from collections import defaultdict, Counter
from urllib.parse import urlparse, unquote

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
SITE = 'https://masar-werbeagentur.de'
IDENTITY = SITE + '/#identity'
# 301-Weiterleitungen aus .htaccess (Ziele gelten als vorhanden)
REDIRECTS = {}


def lade_redirects():
    p = os.path.join(ROOT, '.htaccess')
    if not os.path.exists(p): return
    for m in re.finditer(r'RewriteRule \^([^\s]+)\$ (/[^\s]+) \[R=301', open(p, encoding='utf-8').read()):
        pat = m.group(1).replace('\\.', '.')
        alts = re.match(r'(.*)\(([^)]*)\)(.*)', pat)
        if alts:
            for a in alts.group(2).split('|'): REDIRECTS[alts.group(1) + a + alts.group(3)] = m.group(2).lstrip('/')
        else:
            REDIRECTS[pat] = m.group(2).lstrip('/')


def seiten():
    out = sorted(glob.glob(os.path.join(ROOT, '*.html')) + glob.glob(os.path.join(ROOT, 'blog', '*.html'))
                 + glob.glob(os.path.join(ROOT, '*', 'index.html')))
    return [os.path.relpath(p, ROOT) for p in out if not os.path.relpath(p, ROOT).startswith(('tools', 'admin'))]


def url_von(rel):
    if rel == 'index.html': return SITE + '/'
    if rel.endswith('/index.html'): return SITE + '/' + rel[:-len('index.html')]
    return SITE + '/' + rel


def rel_von_url(u):
    """URL/Pfad → Datei relativ zu ROOT (oder None bei extern)."""
    p = urlparse(u)
    if p.scheme in ('mailto', 'tel', 'javascript', 'data', 'sms', 'whatsapp'): return None
    if p.netloc and p.netloc not in ('masar-werbeagentur.de', 'www.masar-werbeagentur.de'): return None
    path = unquote(p.path)
    if not path: return ''
    return path


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = None; self._in = []; self.metas = []; self.links = []; self.h1 = []
        self.imgs = []; self.anchors = []; self.ldjson = []; self._buf = None; self._kind = None
        self.text = []; self.skip = 0; self.headings = []; self.sources = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'title': self._buf = []; self._kind = 'title'
        elif tag == 'meta': self.metas.append(a)
        elif tag == 'link': self.links.append(a)
        elif tag in ('h1', 'h2', 'h3'):
            self._buf = []; self._kind = tag
        elif tag == 'img': self.imgs.append((a, self.getpos()[0]))
        elif tag == 'source': self.sources.append(a)
        elif tag == 'a': self.anchors.append(a)
        elif tag == 'script':
            if a.get('type') == 'application/ld+json': self._buf = []; self._kind = 'ld'
            else: self.skip += 1
        elif tag in ('style', 'template'): self.skip += 1

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'template') and self._kind != 'ld' and self.skip: self.skip -= 1; return
        if self._buf is not None and (tag == self._kind or (tag == 'script' and self._kind == 'ld')):
            t = ''.join(self._buf)
            if self._kind == 'title': self.title = t.strip()
            elif self._kind == 'ld': self.ldjson.append(t)
            else:
                self.headings.append((self._kind, ' '.join(t.split())))
                if self._kind == 'h1': self.h1.append(' '.join(t.split()))
            self._buf = None; self._kind = None

    def handle_data(self, d):
        if self._buf is not None: self._buf.append(d)
        if not self.skip and self._kind != 'ld': self.text.append(d)


def meta(p, key, attr):
    for m in p.metas:
        if m.get(attr) == key: return m.get('content')
    return None


def norm(s):
    # ohne Leerraum vergleichen: Text in <span>s (z. B. <span class="nw">) wird stückweise geliefert
    return re.sub(r'\s+', '', html.unescape(s or '')).lower()


def ld_objekte(d):
    """Alle Objekte (auch in @graph und verschachtelt) liefern."""
    if isinstance(d, list):
        for x in d: yield from ld_objekte(x)
    elif isinstance(d, dict):
        yield d
        for k, v in d.items():
            if isinstance(v, (dict, list)): yield from ld_objekte(v)


def typen(o):
    t = o.get('@type', [])
    return t if isinstance(t, list) else [t]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    kurz = '--kurz' in sys.argv
    regeln = None
    for a in sys.argv:
        if a.startswith('--regel'):
            regeln = set(sys.argv[sys.argv.index(a) + 1].split(',')) if a == '--regel' else set(a.split('=', 1)[1].split(','))
            if a == '--regel': args = [x for x in args if x != sys.argv[sys.argv.index(a) + 1]]
    lade_redirects()
    alle = seiten()
    nur = set(args) if args else None
    befunde = []  # (stufe, regel, seite, text)

    def B(stufe, regel, seite, text):
        if regeln and regel not in regeln: return
        if nur and seite not in nur and seite != '*': return
        befunde.append((stufe, regel, seite, text))

    daten = {}
    for rel in alle:
        s = open(os.path.join(ROOT, rel), encoding='utf-8').read()
        p = Parser(); p.feed(s)
        daten[rel] = (s, p)

    def existiert(path, von):
        """path: URL-Pfad (absolut oder relativ)."""
        if path is None: return True
        if path == '': return True
        if not path.startswith('/'):
            path = '/' + os.path.normpath(os.path.join(os.path.dirname(von), path)).replace('\\', '/')
        q = path.lstrip('/')
        if q in REDIRECTS: return True
        f = os.path.join(ROOT, q)
        if os.path.isdir(f): return os.path.exists(os.path.join(f, 'index.html')) or os.path.exists(os.path.join(f, 'index.php'))
        return os.path.exists(f)

    titel = defaultdict(list); beschr = defaultdict(list); eingehend = Counter(); indexierbar = set()
    for rel, (s, p) in daten.items():
        robots = (meta(p, 'robots', 'name') or '').lower()
        noindex = 'noindex' in robots
        if not noindex: indexierbar.add(rel)
        # Titel
        t = html.unescape(p.title or '')
        if not t: B('F', 'titel', rel, 'kein <title>')
        else:
            if len(t) > 60 and not noindex: B('H', 'titel-lang', rel, f'Titel {len(t)} Zeichen: {t}')
            if len(t) < 20 and not noindex: B('H', 'titel-kurz', rel, f'Titel {len(t)} Zeichen: {t}')
            if not noindex: titel[t].append(rel)
        d = html.unescape(meta(p, 'description', 'name') or '')
        if not noindex:
            if not d: B('F', 'beschreibung', rel, 'keine meta description')
            elif not (50 <= len(d) <= 160): B('H', 'beschreibung-laenge', rel, f'Beschreibung {len(d)} Zeichen')
            if d: beschr[d].append(rel)
        # H1
        if len(p.h1) != 1: B('F' if not noindex else 'H', 'h1', rel, f'{len(p.h1)} H1: {p.h1[:3]}')
        if noindex: continue
        # Canonical
        can = [l.get('href') for l in p.links if (l.get('rel') or '').lower() == 'canonical']
        if len(can) != 1: B('F', 'canonical', rel, f'{len(can)} canonical')
        elif can[0] != url_von(rel): B('F', 'canonical', rel, f'canonical {can[0]} ≠ {url_von(rel)}')
        # hreflang
        hl = {l.get('hreflang'): l.get('href') for l in p.links if l.get('hreflang')}
        if hl:
            if set(hl) - {'de', 'x-default', 'de-DE'}: B('H', 'hreflang', rel, f'unerwartete hreflang {sorted(hl)}')
            for k, v in hl.items():
                if can and v != can[0]: B('F', 'hreflang', rel, f'hreflang {k} → {v} ≠ canonical')
            if 'x-default' not in hl: B('H', 'hreflang', rel, 'hreflang ohne x-default')
        # Open Graph
        og = meta(p, 'og:image', 'property')
        if not og: B('F', 'og-bild', rel, 'kein og:image')
        else:
            if og.rstrip('/').endswith(('logo.png', 'logo.webp')): B('H', 'og-logo', rel, 'og:image ist nur das Logo')
            r = rel_von_url(og)
            if r and not existiert(r, rel): B('F', 'og-bild', rel, f'og:image fehlt lokal: {og}')
            if not og.startswith('https://'): B('F', 'og-bild', rel, f'og:image nicht absolut: {og}')
            elif r and existiert(r, rel):
                fp = os.path.join(ROOT, r.lstrip('/'))
                if os.path.getsize(fp) > 300_000: B('H', 'og-bild', rel, f'og:image {os.path.getsize(fp) // 1000} KB (> 300 KB)')
                ogw, ogh = meta(p, 'og:image:width', 'property'), meta(p, 'og:image:height', 'property')
                if ogw and ogh:
                    try:
                        from PIL import Image
                        iw, ih = Image.open(fp).size
                        if (str(iw), str(ih)) != (ogw, ogh): B('F', 'og-bild', rel, f'og:image:width/height {ogw}×{ogh} ≠ Datei {iw}×{ih}')
                    except ImportError: pass
        for k in ('og:title', 'og:description', 'og:url'):
            if not meta(p, k, 'property'): B('H', 'og-meta', rel, f'{k} fehlt')
        ogu = meta(p, 'og:url', 'property')
        if ogu and can and ogu != can[0]: B('H', 'og-meta', rel, f'og:url {ogu} ≠ canonical')
        if not meta(p, 'twitter:card', 'name'): B('H', 'og-meta', rel, 'twitter:card fehlt')
        # JSON-LD
        sichtbar = norm(''.join(p.text))
        hat_lb = False
        for i, raw in enumerate(p.ldjson):
            try: j = json.loads(raw)
            except Exception as e:
                B('F', 'jsonld', rel, f'JSON-LD #{i + 1} ungültig: {e}'); continue
            for top in (j if isinstance(j, list) else [j]):
                if isinstance(top, dict) and '@context' not in top: B('F', 'jsonld', rel, f'JSON-LD #{i + 1} ohne @context')
            for o in ld_objekte(j):
                ty = typen(o)
                if any(x in ('LocalBusiness', 'ProfessionalService', 'HomeAndConstructionBusiness', 'Organization') for x in ty):
                    if o.get('@id') == IDENTITY: hat_lb = True
                    elif o.get('@id') and 'masar-werbeagentur.de/#' in str(o.get('@id')) and o.get('name'):
                        B('H', 'jsonld-id', rel, f'Firmenobjekt mit abweichender @id {o.get("@id")}')
                    elif not o.get('@id') and o.get('name', '').lower().startswith('masar'):
                        B('H', 'jsonld-id', rel, f'Firmenobjekt {ty} ohne @id {IDENTITY}')
                if 'FAQPage' in ty:
                    fr = [q.get('name', '') for q in o.get('mainEntity', []) if isinstance(q, dict)]
                    unsichtbar = [q for q in fr if norm(q)[:45] not in sichtbar]
                    if not fr: B('F', 'faq', rel, 'FAQPage ohne Fragen')
                    if unsichtbar: B('F', 'faq', rel, f'{len(unsichtbar)}/{len(fr)} FAQ-Fragen nicht sichtbar, z. B. „{unsichtbar[0][:70]}“')
                if 'BreadcrumbList' in ty:
                    for it in o.get('itemListElement', []):
                        u = it.get('item')
                        if isinstance(u, dict): u = u.get('@id')
                        if u:
                            r = rel_von_url(u)
                            if r is not None and not existiert(r, rel): B('F', 'breadcrumb', rel, f'Brotkrumen-Ziel fehlt: {u}')
                        elif it is not o.get('itemListElement', [])[-1]:
                            B('F', 'breadcrumb', rel, f'Brotkrumen-Eintrag ohne item: {it.get("name")}')
                if 'Service' in ty and not o.get('provider') and not o.get('serviceType') and not o.get('name'):
                    B('H', 'jsonld', rel, 'Service ohne name/provider')
                if any(x in ('BlogPosting', 'Article', 'NewsArticle') for x in ty):
                    bild = o.get('image')
                    if isinstance(bild, list): bild = bild[0] if bild else None
                    if isinstance(bild, dict): bild = bild.get('url')
                    if not bild: B('H', 'artikel-bild', rel, f'{ty[0]} ohne image')
                    elif str(bild).endswith(('logo.png', 'logo.webp')): B('H', 'artikel-bild', rel, f'{ty[0]}-Bild ist nur das Logo')
                    for k in ('datePublished', 'headline', 'author'):
                        if k not in o: B('H', 'artikel', rel, f'{ty[0]} ohne {k}')
                    if len(o.get('headline', '')) > 110: B('H', 'artikel', rel, 'headline > 110 Zeichen')
                if 'VideoObject' in ty:
                    for k in ('name', 'thumbnailUrl', 'uploadDate'):
                        if not o.get(k): B('F', 'video', rel, f'VideoObject ohne {k} (Pflichtfeld für Google)')
                adr = o.get('address')
                if isinstance(adr, dict) and adr.get('streetAddress') and (
                        'Bristolstraße 19E' not in adr.get('streetAddress', '') or adr.get('postalCode') != '13349'):
                    B('F', 'adresse', rel, f'Adresse ≠ Bristolstraße 19E, 13349 Berlin (einziger Standort): {adr}')
                tel = o.get('telephone')
                if tel and re.sub(r'\D', '', str(tel)).lstrip('0').replace('49', '', 1) != '1785143918':
                    B('H', 'telefon', rel, f'abweichende Telefonnummer im JSON-LD: {tel}')
                for k in ('aggregateRating', 'review'):
                    if k in o: B('H', 'jsonld-bewertung', rel, f'{k} in JSON-LD – nur mit echten, sichtbaren Bewertungen')
        if not p.ldjson and rel not in ('impressum.html', 'datenschutz.html', 'agb.html'): B('H', 'jsonld', rel, 'kein JSON-LD')
        # Kopf: render-blockierende Skripte, Sprache, Viewport
        kopf = s.split('</head>', 1)[0]
        for m in re.findall(r'<script\b[^>]*\bsrc=[^>]*>', kopf):
            if not re.search(r'\b(defer|async)\b|type="module"', m): B('H', 'blockierend', rel, f'Skript im Kopf ohne defer/async: {m[:80]}')
        css = re.findall(r'<link\b[^>]*rel="stylesheet"[^>]*>', kopf)
        if len(css) > 3: B('H', 'blockierend', rel, f'{len(css)} Stylesheets im Kopf')
        if not re.search(r'<html[^>]*\blang="de', s): B('F', 'html-lang', rel, '<html lang="de"> fehlt')
        if 'name="viewport"' not in kopf: B('F', 'viewport', rel, 'meta viewport fehlt')
        # Bilder
        for n, (a, zeile) in enumerate(p.imgs):
            if a.get('fetchpriority') == 'high' and a.get('loading') == 'lazy':
                B('F', 'img-lcp', rel, f'fetchpriority=high und loading=lazy (Z. {zeile}): {a.get("src")}')
            if 'hero' in (a.get('class') or '') and a.get('loading') == 'lazy':
                B('H', 'img-lcp', rel, f'Hero-Bild mit loading=lazy (Z. {zeile}): {a.get("src")}')
            try: w = int(a.get('width') or 0)
            except ValueError: w = 0
            src0 = a.get('src') or ''
            if w >= 1000 and not a.get('srcset') and re.search(r'\.webp$', src0):
                v = re.sub(r'\.webp$', '-720.webp', src0)
                if existiert(rel_von_url(v), rel): B('H', 'img-srcset', rel, f'großes Bild ohne srcset, obwohl {v} existiert (Z. {zeile})')
            src = a.get('src') or ''
            if src.startswith('data:'): continue
            if 'alt' not in a: B('F', 'img-alt', rel, f'Bild ohne alt (Z. {zeile}): {src}')
            if not (a.get('width') and a.get('height')) and 'aspect-ratio' not in (a.get('style') or ''):
                B('H', 'img-dim', rel, f'Bild ohne width/height (Z. {zeile}): {src}')
            r = rel_von_url(src)
            if r and not r.startswith('{') and not existiert(r, rel): B('F', 'img-fehlt', rel, f'Bild fehlt (Z. {zeile}): {src}')
            if re.search(r'\.(png|jpe?g)$', src, re.I) and r:
                stamm = re.sub(r'\.(png|jpe?g)$', '.webp', r, flags=re.I)
                if existiert(stamm, rel): B('H', 'img-webp', rel, f'PNG/JPG obwohl WebP vorhanden (Z. {zeile}): {src}')
            if n == 0 and a.get('loading') == 'lazy' and 'logo' not in src: pass
        # Links
        for a in p.anchors:
            h = a.get('href')
            if not h or h.startswith('#'): continue
            r = rel_von_url(h.split('#')[0].split('?')[0]) if not h.startswith(('mailto:', 'tel:')) else None
            if r is None: continue
            if r.startswith(('/api/', '/admin/')) or r.endswith('.php'): continue
            if not existiert(r, rel): B('F', 'link-kaputt', rel, f'interner Link ins Leere: {h}')
            else:
                ziel = r if r.startswith('/') else '/' + os.path.normpath(os.path.join(os.path.dirname(rel), r))
                ziel = ziel.lstrip('/')
                ziel = REDIRECTS.get(ziel, ziel)
                if ziel == '' or ziel.endswith('/'): ziel += 'index.html'
                if ziel != rel: eingehend[ziel] += 1
                if ziel in REDIRECTS: B('H', 'link-redirect', rel, f'Link auf Weiterleitung: {h}')
        if re.search(r'href="[^"]*(werbetechnik-(nrw|koeln|duesseldorf|dortmund|essen|bochum)|pvc-banner-(koeln|duesseldorf|dortmund|essen|bochum)|fensterfolie-(koeln|duesseldorf|dortmund|essen|bochum))\.html', s):
            B('H', 'link-redirect', rel, 'Link auf 301-weitergeleitete Seite')
        if not hat_lb and rel == 'index.html': B('F', 'jsonld-id', rel, f'LocalBusiness mit @id {IDENTITY} fehlt')

    for t, r in titel.items():
        if len(r) > 1: B('F', 'titel-doppelt', r[0], f'gleicher Titel auf {len(r)} Seiten: {", ".join(r)}')
    for t, r in beschr.items():
        if len(r) > 1: B('F', 'beschreibung-doppelt', r[0], f'gleiche Beschreibung auf {len(r)} Seiten: {", ".join(r)}')
    for rel in sorted(indexierbar):
        if eingehend[rel] == 0 and rel != 'index.html': B('H', 'verwaist', rel, 'keine internen Links auf diese Seite')

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import sitemap_lastmod

    # Fast gleiche Seiten (Doorway-Risiko): Jaccard-Ähnlichkeit des Haupttexts über 5-Wort-Folgen
    if not regeln or 'aehnlich' in regeln:
        sh = {}
        for rel in indexierbar:
            tp = sitemap_lastmod.Text(); tp.feed(daten[rel][0])
            w = re.findall(r'\w+', ' '.join(tp.teile).lower())
            sh[rel] = {' '.join(w[i:i + 5]) for i in range(max(0, len(w) - 4))}
        rs = sorted(sh); paare = defaultdict(list)
        for i, a in enumerate(rs):
            for b in rs[i + 1:]:
                A_, B_ = sh[a], sh[b]
                if len(A_) < 50 or len(B_) < 50: continue
                j = len(A_ & B_) / len(A_ | B_)
                if j >= 0.6: paare[a].append((j, b)); paare[b].append((j, a))
        for a in sorted(paare):   # je Seite nur der ähnlichste Partner + Anzahl
            j, b = max(paare[a])
            B('H', 'aehnlich', a, f'{round(j * 100)} % gleicher Haupttext wie {b}' + (f' (+{len(paare[a]) - 1} weitere ≥ 60 %)' if len(paare[a]) > 1 else ''))

    # Sitemap
    try: lastmod_speicher = json.load(open(sitemap_lastmod.SPEICHER, encoding='utf-8'))
    except (OSError, ValueError): lastmod_speicher = None
    sm = os.path.join(ROOT, 'sitemap.xml')
    if os.path.exists(sm):
        x = open(sm, encoding='utf-8').read()
        eintraege = re.findall(r'<url>\s*<loc>([^<]+)</loc>(?:\s*<lastmod>([^<]+)</lastmod>)?', x)
        locs = Counter(l for l, _ in eintraege)
        for l, c in locs.items():
            if c > 1: B('F', 'sitemap', 'sitemap.xml', f'doppelt: {l}')
        im_sm = set()
        for l, lm in eintraege:
            r = l.replace(SITE + '/', '', 1)
            if r == '' or r.endswith('/'): r += 'index.html'
            im_sm.add(r)
            if r in REDIRECTS: B('F', 'sitemap', 'sitemap.xml', f'Weiterleitung in Sitemap: {l}')
            elif r not in daten and not os.path.exists(os.path.join(ROOT, r)): B('F', 'sitemap', 'sitemap.xml', f'Seite fehlt: {l}')
            elif r in daten and r not in indexierbar: B('F', 'sitemap', 'sitemap.xml', f'noindex-Seite in Sitemap: {l}')
            if not lm: B('H', 'sitemap-lastmod', 'sitemap.xml', f'ohne lastmod: {l}')
            elif r in daten and lastmod_speicher is not None:
                # nur Änderungen am Haupttext zählen (siehe sitemap_lastmod.py), nicht Technik/Fußzeile
                alt = lastmod_speicher.get(r)
                if not alt: B('H', 'sitemap-lastmod', 'sitemap.xml', f'noch kein Inhalts-Hash – sitemap_lastmod.py ausführen: {r}')
                elif alt[0] != sitemap_lastmod.inhalt_hash(daten[r][0]):
                    B('H', 'sitemap-lastmod', 'sitemap.xml', f'Inhalt geändert, lastmod {lm} veraltet – sitemap_lastmod.py ausführen: {r}')
            if lm and not re.match(r'^\d{4}-\d{2}-\d{2}', lm): B('F', 'sitemap', 'sitemap.xml', f'lastmod kein W3C-Datum: {lm}')
        for rel in sorted(indexierbar - im_sm):
            if rel not in ('404.html', '500.html'): B('F', 'sitemap', rel, 'indexierbare Seite fehlt in sitemap.xml')
    else:
        B('F', 'sitemap', '*', 'sitemap.xml fehlt')

    # robots.txt
    rb = os.path.join(ROOT, 'robots.txt')
    if os.path.exists(rb):
        t = open(rb, encoding='utf-8').read()
        if 'Sitemap: ' + SITE + '/sitemap.xml' not in t: B('F', 'robots', 'robots.txt', 'Sitemap-Zeile fehlt')
        for m in re.finditer(r'^Disallow:\s*(\S+)', t, re.M):
            d = m.group(1).lstrip('/')
            for rel in indexierbar:
                if d and rel.startswith(d) and d not in ('',): B('F', 'robots', 'robots.txt', f'indexierbare Seite gesperrt: {rel} ({m.group(1)})')
        if re.search(r'^Disallow:\s*/(css|js|fonts)/', t, re.M): B('F', 'robots', 'robots.txt', 'CSS/JS gesperrt')
    else: B('F', 'robots', '*', 'robots.txt fehlt')

    # llms.txt
    lt = os.path.join(ROOT, 'llms.txt')
    if os.path.exists(lt):
        t = open(lt, encoding='utf-8').read()
        if not t.startswith('# '): B('H', 'llms', 'llms.txt', 'beginnt nicht mit „# Titel“ (llmstxt.org)')
        for u in re.findall(r'\]\((https?://[^)\s]+|/[^)\s]*)\)', t):
            r = rel_von_url(u)
            if r is not None and not existiert(r, 'llms.txt'): B('F', 'llms', 'llms.txt', f'Link ins Leere: {u}')
            rr = (r or '').lstrip('/')
            if rr in REDIRECTS: B('H', 'llms', 'llms.txt', f'Link auf Weiterleitung: {u}')
    else: B('H', 'llms', '*', 'llms.txt fehlt')

    # Ausgabe
    befunde.sort(key=lambda b: (b[0], b[1], b[2]))
    zahl = Counter((b[0], b[1]) for b in befunde)
    if not kurz:
        for st, rg, se, tx in befunde: print(f'{st} {rg:22} {se:48} {tx}')
        print()
    for (st, rg), c in sorted(zahl.items()): print(f'{st} {rg:22} {c}')
    f = sum(c for (st, _), c in zahl.items() if st == 'F'); h = sum(c for (st, _), c in zahl.items() if st == 'H')
    print(f'{len(daten)} Seiten, {len(indexierbar)} indexierbar – {f} Fehler, {h} Hinweise')
    return 1 if f else 0


if __name__ == '__main__':
    sys.exit(main())
