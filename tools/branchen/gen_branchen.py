"""Gemeinsame Bausteine für die Seiten-Generatoren (rekonstruiert am 15.10.2026).
Vorlage für Kopf, Navigation und Footer ist die Live-Seite schilder-berlin.html."""
import os, re, json, html, urllib.parse

ROOT = os.environ.get('MASAR_ROOT', os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))).rstrip('/') + '/'
BASE = 'https://masar-werbeagentur.de/'
T = open(ROOT + 'schilder-berlin.html', encoding='utf-8').read()
HEAD_A = T[:T.index('<title>')]
_h = T.index('</head>')
_ld = T.rindex('application/ld+json', 0, _h)
HEAD_B = T[T.index('</script>', _ld) + len('</script>\n'):T.index('<section class="hero"')]
# Die Vorlage hat seit a11y.py ein echtes <main> – die Generatoren setzen role="main" auf den Hero,
# a11y.py baut daraus wieder <main> … </main> (sonst bliebe <main> ohne Ende-Tag stehen).
HEAD_B = re.sub(r'<main id="main-content" tabindex="-1">\n?', '', HEAD_B)
# Kopf-Blöcke, die die Nachbearbeitung selbst setzt (hero_klar, schnell, a11y, umbruch), nicht aus der Vorlage
# übernehmen – sonst landen Seiten-Styles der Generatoren hinter ihnen und die Reihenfolge hängt vom Verlauf ab.
HEAD_B = re.sub(r'<style id="(?:kopf-klar|a11y-fix)">.*?</style>\n?', '', HEAD_B, flags=re.S)
HEAD_B = re.sub(r'<!-- (schnell|umbruch):start -->.*?<!-- \1:ende -->\n?', '', HEAD_B, flags=re.S)
FOOT = T[T.index('<footer>'):]

I = {
 "star": "<svg class=\"i-inline\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z\"/></svg>",
 "check": "<svg class=\"i-inline\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><circle cx=\"12\" cy=\"12\" r=\"10\"/><path d=\"m9 12 2 2 4-4\"/></svg>",
 "wa": "<svg class=\"i-inline\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M7.9 20A9 9 0 1 0 4 16.1L2 22Z\"/></svg>",
 "mail": "<svg class=\"i-inline\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M21.2 8.4c.5.38.8.97.8 1.6v10a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V10a2 2 0 0 1 .8-1.6l8-6a2 2 0 0 1 2.4 0l8 6Z\"/><path d=\"m22 10-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 10\"/></svg>",
 "link": "<svg class=\"i-inline\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71\"/><path d=\"M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71\"/></svg>",
 "faq": "<svg class=\"i-inline\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><circle cx=\"12\" cy=\"12\" r=\"10\"/><path d=\"M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3\"/><path d=\"M12 17h.01\"/></svg>",
 "tag": "<svg class=\"i-inline\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z\"/><path d=\"M7 12h5\"/><path d=\"M15 9.4a4 4 0 1 0 0 5.2\"/></svg>",
 "doc": "<svg class=\"i-inline\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><rect width=\"8\" height=\"4\" x=\"8\" y=\"2\" rx=\"1\" ry=\"1\"/><path d=\"M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2\"/><path d=\"M12 11h4\"/><path d=\"M12 16h4\"/><path d=\"M8 11h.01\"/><path d=\"M8 16h.01\"/></svg>"
}
SVC = {
 "glas": "<rect width=\"18\" height=\"18\" x=\"3\" y=\"3\" rx=\"2\"/><path d=\"M3 12h18\"/><path d=\"M12 3v18\"/>",
 "stern": "<path d=\"M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z\"/>",
 "karte": "<path d=\"M16 10h2\"/><path d=\"M16 14h2\"/><path d=\"M6.17 15a3 3 0 0 1 5.66 0\"/><circle cx=\"9\" cy=\"11\" r=\"2\"/><rect x=\"2\" y=\"5\" width=\"20\" height=\"14\" rx=\"2\"/>",
 "schild": "<path d=\"M2 3h20\"/><path d=\"M21 3v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V3\"/><path d=\"m7 21 5-5 5 5\"/>",
 "web": "<rect width=\"20\" height=\"14\" x=\"2\" y=\"3\" rx=\"2\"/><line x1=\"8\" x2=\"16\" y1=\"21\" y2=\"21\"/><line x1=\"12\" x2=\"12\" y1=\"17\" y2=\"21\"/>",
 "schutz": "<path d=\"M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z\"/><path d=\"m9 12 2 2 4-4\"/>",
 "weg": "<path d=\"M12 13v8\"/><path d=\"M12 3v3\"/><path d=\"M18 6a2 2 0 0 1 1.387.56l2.307 2.22a1 1 0 0 1 0 1.44l-2.307 2.22A2 2 0 0 1 18 13H6a2 2 0 0 1-1.387-.56l-2.306-2.22a1 1 0 0 1 0-1.44l2.306-2.22A2 2 0 0 1 6 6z\"/>",
 "thermo": "<path d=\"M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z\"/>",
 "auge": "<path d=\"M10.733 5.076a10.744 10.744 0 0 1 11.205 6.575 1 1 0 0 1 0 .696 10.747 10.747 0 0 1-1.444 2.49\"/><path d=\"M14.084 14.158a3 3 0 0 1-4.242-4.242\"/><path d=\"M17.479 17.499a10.75 10.75 0 0 1-15.417-5.151 1 1 0 0 1 0-.696 10.75 10.75 0 0 1 4.446-5.143\"/><path d=\"m2 2 20 20\"/>",
 "phone": "<rect width=\"14\" height=\"20\" x=\"5\" y=\"2\" rx=\"2\" ry=\"2\"/><path d=\"M12 18h.01\"/>",
 "tuer": "<path d=\"M18 20V6a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v14\"/><path d=\"M2 20h20\"/><path d=\"M14 12v.01\"/>",
 "licht": "<path d=\"M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5\"/><path d=\"M9 18h6\"/><path d=\"M10 22h4\"/>",
 "druck": "<path d=\"M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2\"/><path d=\"M6 9V3a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v6\"/><rect x=\"6\" y=\"14\" width=\"12\" height=\"8\" rx=\"1\"/>",
 "sonne": "<circle cx=\"12\" cy=\"12\" r=\"4\"/><path d=\"M12 2v2\"/><path d=\"M12 20v2\"/><path d=\"m4.93 4.93 1.41 1.41\"/><path d=\"m17.66 17.66 1.41 1.41\"/><path d=\"M2 12h2\"/><path d=\"M20 12h2\"/><path d=\"m6.34 17.66-1.41 1.41\"/><path d=\"m19.07 4.93-1.41 1.41\"/>",
 "neon": "<path d=\"M2 6c.6.5 1.2 1 2.5 1C7 7 7 5 9.5 5c2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1\"/><path d=\"M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1\"/><path d=\"M2 18c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1\"/>",
 "spiegel": "<path d=\"m3 7 5 5-5 5V7\"/><path d=\"m21 7-5 5 5 5V7\"/><path d=\"M12 20v2\"/><path d=\"M12 14v2\"/><path d=\"M12 8v2\"/><path d=\"M12 2v2\"/>"
}

def svg(name):
    return '<svg class="i-svg" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' + SVC[name] + '</svg>'

def esc(s):
    return html.escape(str(s), quote=True)

def wa(text):
    return 'https://wa.me/491785143918?text=' + urllib.parse.quote(text, safe='')

def sec(title_eyebrow, h2, sub, body, alt=False, sid=None, icon='check'):
    i = f' id="{sid}"' if sid else ''
    s = f'\n      <p class="sec-sub">{sub}</p>' if sub else ''
    return f'''<section class="section{' bg-alt' if alt else ''}"{i}>
  <div class="container">
    <div class="sec-head reveal">
      <span class="eyebrow">{I[icon]}{title_eyebrow}</span>
      <h2 class="sec-title">{h2}</h2>{s}
    </div>
{body}
  </div>
</section>
'''

import pages  # Ende des gemeinsamen Teils (die Generatoren lesen nur bis hier)
