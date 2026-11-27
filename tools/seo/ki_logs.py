"""KI-Sichtbarkeit aus dem Server-Protokoll messen – ohne Tracking im Browser.

Liest ein Apache-/LiteSpeed-Zugriffsprotokoll (Hostinger → Dateien/Erweitert → Zugriffsprotokolle,
auch .gz) und zählt:
  1. Abrufe durch Such- und KI-Crawler (welche Seiten sie holen, ob sie 200 bekommen),
  2. Besuche von Menschen, die über eine KI-Antwort kamen (Referrer oder utm_source).
Es werden keine IP-Adressen ausgegeben oder gespeichert.

Aufruf:  python3 tools/seo/ki_logs.py access.log [weitere.log.gz ...]
Die Protokolldatei nicht ins Repository legen (enthält IP-Adressen).
"""
import sys, re, gzip, collections

# Kennung im User-Agent -> (Anbieter, Zweck). Zweck: Suche = Index für Antworten,
# Nutzer = Abruf auf Wunsch eines Nutzers, Training = Modelltraining.
BOTS = [
    ('OAI-SearchBot', 'OpenAI', 'Suche'), ('ChatGPT-User', 'OpenAI', 'Nutzer'), ('GPTBot', 'OpenAI', 'Training'),
    ('Claude-SearchBot', 'Anthropic', 'Suche'), ('Claude-User', 'Anthropic', 'Nutzer'), ('ClaudeBot', 'Anthropic', 'Training'),
    ('PerplexityBot', 'Perplexity', 'Suche'), ('Perplexity-User', 'Perplexity', 'Nutzer'),
    ('Google-Extended', 'Google', 'Training'), ('GoogleOther', 'Google', 'Sonstiges'), ('Googlebot', 'Google', 'Suche'),
    ('bingbot', 'Microsoft', 'Suche'), ('Applebot-Extended', 'Apple', 'Training'), ('Applebot', 'Apple', 'Suche'),
    ('DuckAssistBot', 'DuckDuckGo', 'Nutzer'), ('MistralAI-User', 'Mistral', 'Nutzer'), ('meta-externalagent', 'Meta', 'Training'),
    ('Amazonbot', 'Amazon', 'Suche'), ('CCBot', 'Common Crawl', 'Training'), ('Bytespider', 'ByteDance', 'Training'),
]
# Herkunft von Besuchern aus KI-Antworten (Referrer-Host oder utm_source)
QUELLEN = {
    'chatgpt.com': 'ChatGPT', 'chat.openai.com': 'ChatGPT', 'perplexity.ai': 'Perplexity', 'claude.ai': 'Claude',
    'gemini.google.com': 'Gemini', 'copilot.microsoft.com': 'Copilot', 'copilot.com': 'Copilot',
    'chat.mistral.ai': 'Mistral', 'you.com': 'You.com', 'duckduckgo.com/?ia=chat': 'DuckDuckGo KI',
}
ZEILE = re.compile(r'"(?:GET|HEAD|POST) (\S+) [^"]*" (\d{3}) \S+ "([^"]*)" "([^"]*)"')


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    bot_n, bot_seiten, bot_status = collections.Counter(), collections.defaultdict(collections.Counter), collections.defaultdict(collections.Counter)
    ref_n, ref_seiten = collections.Counter(), collections.defaultdict(collections.Counter)
    zeilen = 0
    for pfad in sys.argv[1:]:
        auf = gzip.open if pfad.endswith('.gz') else open
        with auf(pfad, 'rt', encoding='utf-8', errors='replace') as f:
            for z in f:
                m = ZEILE.search(z)
                if not m: continue
                zeilen += 1
                url, status, ref, ua = m.groups()
                seite = url.split('?')[0]
                bot = next((b for b in BOTS if b[0].lower() in ua.lower()), None)
                if bot:
                    bot_n[bot] += 1; bot_seiten[bot][seite] += 1; bot_status[bot][status] += 1
                    continue
                if re.search(r'\.(css|js|png|jpe?g|webp|svg|woff2?|ico|mp4|json)$', seite): continue
                quelle = next((n for h, n in QUELLEN.items() if h in ref.lower()), None)
                u = re.search(r'utm_source=([^&\s]+)', url)
                if not quelle and u:
                    quelle = next((n for h, n in QUELLEN.items() if u.group(1).lower() in h or h in u.group(1).lower()), None)
                if quelle:
                    ref_n[quelle] += 1; ref_seiten[quelle][seite] += 1

    print(f'{zeilen} Protokollzeilen ausgewertet\n')
    print('1. Crawler-Abrufe')
    if not bot_n: print('   keine erkannt')
    for (name, firma, zweck), n in bot_n.most_common():
        st = ', '.join(f'{k}: {v}' for k, v in sorted(bot_status[(name, firma, zweck)].items()))
        print(f'   {name:18} {firma:11} {zweck:9} {n:6}  (Status {st})')
        for s, k in bot_seiten[(name, firma, zweck)].most_common(5): print(f'      {k:5}  {s}')
    gesperrt = [b[0] for b, c in bot_status.items() if any(k in ('403', '429', '503') for k in c)]
    if gesperrt:
        print('\n   Achtung – diese Crawler bekamen 403/429/503 (Firewall oder CDN prüfen): ' + ', '.join(sorted(set(gesperrt))))
    print('\n2. Besuche aus KI-Antworten (Referrer / utm_source)')
    if not ref_n: print('   keine erkannt')
    for q, n in ref_n.most_common():
        print(f'   {q:12} {n:5}')
        for s, k in ref_seiten[q].most_common(5): print(f'      {k:5}  {s}')


if __name__ == '__main__':
    main()
