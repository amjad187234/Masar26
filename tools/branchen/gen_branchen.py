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
FOOT = T[T.index('<footer>'):]

I = {
 "star": "<svg class=\"i-inline\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><path d=\"m12 3.5 2.6 5.6 6 .8-4.4 4.2 1.1 6-5.3-3-5.3 3 1.1-6L3.4 9.9l6-.8Z\"/></svg>",
 "check": "<svg class=\"i-inline\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><circle cx=\"12\" cy=\"12\" r=\"9\"/><path d=\"m8 12.3 2.7 2.7L16 9.5\"/></svg>",
 "wa": "<svg class=\"i-inline\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M21 11.5a8 8 0 0 1-11.6 7.1L4 20.5l1.9-5.1A8 8 0 1 1 21 11.5Z\"/><path d=\"M9 11h6M9 14h4\"/></svg>",
 "mail": "<svg class=\"i-inline\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M3 9.5 12 4l9 5.5V19a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z\"/><path d=\"m3 10 9 6 9-6\"/></svg>",
 "link": "<svg class=\"i-inline\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M10 13.5a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1.5 1.5\"/><path d=\"M14 10.5a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1.5-1.5\"/></svg>",
 "faq": "<svg class=\"i-inline\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><circle cx=\"12\" cy=\"12\" r=\"9\"/><path d=\"M9.5 9.2A2.6 2.6 0 0 1 14.5 10c0 1.7-2.5 2-2.5 3.8\"/><circle cx=\"12\" cy=\"17\" r=\".9\" fill=\"currentColor\" stroke=\"none\"/></svg>",
 "tag": "<svg class=\"i-inline\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><circle cx=\"12\" cy=\"12\" r=\"9\"/><path d=\"M15.5 8.8a4.5 4.5 0 1 0 0 6.4M7.5 11h6M7.5 13.5h6\"/></svg>",
 "doc": "<svg class=\"i-inline\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><rect x=\"5\" y=\"4\" width=\"14\" height=\"17\" rx=\"2\"/><path d=\"M9 4V3a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v1\"/><path d=\"M9 11h6M9 15h4\"/></svg>"
}
SVC = {
 "glas": "<rect x=\"3\" y=\"3\" width=\"18\" height=\"18\" rx=\"2\"/><path d=\"M3 12h18M12 3v18\"/>",
 "stern": "<path d=\"m12 3.5 2.6 5.6 6 .8-4.4 4.2 1.1 6-5.3-3-5.3 3 1.1-6L3.4 9.9l6-.8Z\"/>",
 "karte": "<rect x=\"3\" y=\"6\" width=\"18\" height=\"12\" rx=\"2\"/><path d=\"M3 10h18M7 14h4\"/>",
 "schild": "<rect x=\"3\" y=\"4\" width=\"18\" height=\"10\" rx=\"2\"/><path d=\"M12 14v7M8 21h8\"/>",
 "web": "<rect x=\"2.5\" y=\"4\" width=\"19\" height=\"14\" rx=\"2\"/><path d=\"M2.5 8h19M8 21h8M12 18v3\"/>",
 "schutz": "<path d=\"M12 3 20 6v6c0 4.5-3.4 7.8-8 9-4.6-1.2-8-4.5-8-9V6Z\"/><path d=\"m8.5 12 2.5 2.5 4.5-5\"/>",
 "weg": "<path d=\"M12 3v18\"/><path d=\"M12 6h7l2 2-2 2h-7M12 13H5l-2 2 2 2h7\"/>",
 "thermo": "<path d=\"M14 14.8V5a2 2 0 0 0-4 0v9.8a4 4 0 1 0 4 0Z\"/><path d=\"M12 9v7\"/>",
 "auge": "<path d=\"M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12Z\"/><path d=\"M4 4l16 16\"/>",
 "phone": "<rect x=\"7\" y=\"2\" width=\"10\" height=\"20\" rx=\"2\"/><path d=\"M11 18h2\"/>",
 "tuer": "<path d=\"M5 21V4a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v17\"/><path d=\"M3 21h18\"/><circle cx=\"15\" cy=\"12.5\" r=\"1\"/>",
 "licht": "<path d=\"M9 18h6M10 21h4\"/><path d=\"M12 3a6 6 0 0 0-3.6 10.8c.5.4.8 1 .9 1.6l.1.6h5.2l.1-.6c.1-.6.4-1.2.9-1.6A6 6 0 0 0 12 3Z\"/>",
 "druck": "<rect x=\"6\" y=\"3\" width=\"12\" height=\"6\" rx=\"1\"/><path d=\"M6 14H4a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2h-2\"/><rect x=\"6\" y=\"14\" width=\"12\" height=\"7\" rx=\"1\"/>",
 "sonne": "<circle cx=\"12\" cy=\"12\" r=\"4\"/><path d=\"M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4\"/>",
 "neon": "<path d=\"M4 15c2-6 4-6 6 0s4 6 6 0 3-6 4-3\"/><path d=\"M3 20h18\"/>",
 "spiegel": "<rect x=\"4\" y=\"3\" width=\"16\" height=\"18\" rx=\"2\"/><path d=\"m8 9 3-3M8 14l7-7M12 16l4-4\"/>"
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
