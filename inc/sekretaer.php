<?php
/**
 * Telegram-Sekretär – Masar Werbeagentur
 *
 * • Neue Anfrage / neuer Termin: Nachricht mit Status-Tasten
 * • 30 Min. vor jedem Termin: Erinnerung; 24 h vorher: Erinnerungs-E-Mail an den Kunden (falls E-Mail)
 * • Jeden Morgen 8 Uhr: Tagesbericht (Termine, neue Anfragen, was nachgefasst werden muss)
 * • Montags 8 Uhr: Wochenbericht mit Zahlen und Verbesserungsvorschlägen
 * • Befehle: /heute /morgen /termine /offen /bericht /hilfe   (Webhook: /telegram.php)
 *
 * Datenschutz: Telegram-Nachrichten enthalten KEINE Namen, Telefonnummern, E-Mails oder Adressen –
 * nur Anfragenummer, Leistung, Stadt, Quelle, Zeiten und Zahlen. Details stehen in /admin/anfragen.php.
 * Zeitgesteuerte Aufgaben laufen über /cron.php (Cronjob alle 5 Minuten).
 * Sprache der Nachrichten: Arabisch (für den Inhaber).
 */

declare(strict_types=1);

require_once __DIR__ . '/anfragen.php';

const SEK_ADMIN = 'https://masar-werbeagentur.de/admin/anfragen.php';
const SEK_TAGE  = ['', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت', 'الأحد'];
const SEK_STATUS_AR = ['neu' => 'جديد', 'kontakt' => 'تواصلنا', 'angebot' => 'انبعت عرض', 'auftrag' => 'صار شغل ✅', 'erledigt' => 'خلص', 'verloren' => 'ما صار شغل'];

function sek_e(string $s): string { return htmlspecialchars($s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); }

function sek_zugang(): array
{
    $k = anf_konfig();
    return [(string) ($k['telegram_token'] ?? ''), (string) ($k['telegram_chat'] ?? '')];
}

/** Bot-API aufrufen (POST JSON). Gibt die dekodierte Antwort zurück oder null. */
function sek_api(string $methode, array $daten): ?array
{
    [$token] = sek_zugang();
    if ($token === '') return null;
    $url = 'https://api.telegram.org/bot' . $token . '/' . $methode;
    $body = json_encode($daten, JSON_UNESCAPED_UNICODE);
    if (function_exists('curl_init')) {
        $ch = curl_init($url);
        curl_setopt_array($ch, [CURLOPT_POST => true, CURLOPT_POSTFIELDS => $body, CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 8,
                                CURLOPT_HTTPHEADER => ['Content-Type: application/json']]);
        $r = curl_exec($ch); curl_close($ch);
    } else {
        $r = @file_get_contents($url, false, stream_context_create(['http' => ['method' => 'POST', 'header' => "Content-Type: application/json\r\n", 'content' => $body, 'timeout' => 8, 'ignore_errors' => true]]));
    }
    $j = is_string($r) ? json_decode($r, true) : null;
    return is_array($j) ? $j : null;
}

/** Nachricht an den Inhaber (HTML-Format). $tasten = inline_keyboard */
function sek_senden(string $html, ?array $tasten = null, ?string $chat = null): bool
{
    [, $c] = sek_zugang();
    $chat = $chat ?? $c;
    if ($chat === '') return false;
    $d = ['chat_id' => $chat, 'text' => $html, 'parse_mode' => 'HTML', 'disable_web_page_preview' => true];
    if ($tasten) $d['reply_markup'] = ['inline_keyboard' => $tasten];
    $r = sek_api('sendMessage', $d);
    return !empty($r['ok']);
}

function sek_tasten(string $nr): array
{
    return [
        [['text' => '📞 تواصلنا', 'callback_data' => "st|$nr|kontakt"], ['text' => '📄 انبعت عرض', 'callback_data' => "st|$nr|angebot"]],
        [['text' => '✅ صار شغل', 'callback_data' => "st|$nr|auftrag"], ['text' => '❌ ما صار', 'callback_data' => "st|$nr|verloren"]],
        [['text' => '🔗 افتح الطلب', 'url' => SEK_ADMIN . '?nr=' . rawurlencode($nr)]],
    ];
}

function sek_wann(int $ts): string
{
    return SEK_TAGE[(int) date('N', $ts)] . ' ' . date('d.m.', $ts) . ' الساعة ' . date('H:i', $ts);
}

function sek_alter(int $ts): string
{
    $m = intdiv(max(0, time() - $ts), 60);
    if ($m < 60) return $m . ' دقيقة';
    if ($m < 1440) return intdiv($m, 60) . ' ساعة';
    return intdiv($m, 1440) . ' يوم';
}

/** Kurzzeile einer Anfrage ohne personenbezogene Daten */
function sek_zeile(array $r): string
{
    return '<b>' . sek_e((string) $r['nr']) . '</b> · ' . sek_e(anf_kurz((string) $r['leistung'], 50))
         . ' · 📍 ' . sek_e((string) ($r['stadt'] ?? '')) ;
}

/** Benachrichtigung bei neuer Anfrage bzw. neuem Termin */
function sek_neue_anfrage(string $nr): bool
{
    $db = anf_db(); if (!$db) return false;
    $st = $db->prepare('SELECT * FROM anfragen WHERE nr = ?'); $st->execute([$nr]); $r = $st->fetch();
    if (!$r) return false;
    $ort = (string) ($r['stadt'] ?? '') . (($r['region'] ?? '') !== '' && $r['region'] !== 'Sonstige' && $r['region'] !== $r['stadt'] ? ' (' . $r['region'] . ')' : '');
    if (!empty($r['termin'])) {
        $t = "📅 <b>موعد استشارة جديد</b>\n"
           . '🗓 ' . sek_e(sek_wann((int) $r['termin'])) . ' (' . (int) $r['termin_dauer'] . " د)\n"
           . '☎️ ' . sek_e((string) $r['termin_art']) . ' · 🗣 ' . sek_e((string) $r['sprache']) . "\n"
           . '📍 ' . sek_e($ort) . "\n"
           . '🔢 ' . sek_e($nr) . "\n\n"
           . '<i>بذكّرك قبل الموعد بنص ساعة.</i>';
    } else {
        $offen = (int) $db->query("SELECT COUNT(*) FROM anfragen WHERE status = 'neu'")->fetchColumn();
        $t = "🔔 <b>طلب جديد</b> " . sek_e($nr) . "\n"
           . '🛠 ' . sek_e(anf_kurz((string) $r['leistung'], 80)) . "\n"
           . '📍 ' . sek_e($ort) . "\n"
           . '📥 عن طريق: ' . sek_e((string) $r['quelle']) . "\n\n"
           . '<i>' . ($offen > 1 ? "عندك $offen طلبات ما انرد عليها. " : '') . 'يلي بيرد بأول ساعة غالباً بياخد الشغل.</i>';
    }
    return sek_senden($t, sek_tasten($nr));
}

/** Status setzen (Tasten in Telegram oder Übersicht); erste Reaktion merken */
function sek_status(string $nr, string $status): bool
{
    if (!isset(ANF_STATUS[$status])) return false;
    $db = anf_db(); if (!$db) return false;
    $st = $db->prepare("UPDATE anfragen SET status = ?, geaendert = ?, erste_reaktion = COALESCE(erste_reaktion, CASE WHEN ? <> 'neu' THEN ? END) WHERE nr = ?");
    $st->execute([$status, time(), $status, time(), $nr]);
    return $st->rowCount() > 0;
}

// ─── Berichte ───────────────────────────────────────────────────────────

function sek_termine(int $von, int $bis): array
{
    $db = anf_db(); if (!$db) return [];
    $st = $db->prepare("SELECT * FROM anfragen WHERE termin >= ? AND termin < ? AND status <> 'verloren' ORDER BY termin");
    $st->execute([$von, $bis]); return $st->fetchAll();
}

function sek_termin_liste(array $rows): string
{
    if (!$rows) return "ما في مواعيد.\n";
    $t = '';
    foreach ($rows as $r) $t .= '• <b>' . date('H:i', (int) $r['termin']) . '</b> ' . sek_e((string) $r['termin_art']) . ' · ' . sek_e((string) $r['sprache']) . ' · 📍 ' . sek_e((string) $r['stadt']) . ' · ' . sek_e((string) $r['nr']) . "\n";
    return $t;
}

/** Was muss heute erledigt werden? (unbeantwortet, nachfassen) */
function sek_aufgaben(): string
{
    $db = anf_db(); if (!$db) return '';
    $t = '';
    $neu = $db->query("SELECT * FROM anfragen WHERE status = 'neu' AND termin IS NULL ORDER BY erstellt")->fetchAll();
    $alt = array_filter($neu, static fn($r) => time() - (int) $r['erstellt'] > 86400);
    if ($neu) {
        $t .= "\n📥 <b>طلبات ما انرد عليها (" . count($neu) . "):</b>\n";
        foreach (array_slice($neu, 0, 8) as $r) $t .= '• ' . sek_zeile($r) . ' · من ' . sek_alter((int) $r['erstellt']) . (time() - (int) $r['erstellt'] > 86400 ? ' ⚠️' : '') . "\n";
    }
    $ang = $db->query("SELECT * FROM anfragen WHERE status = 'angebot' AND geaendert < " . (time() - 3 * 86400) . ' ORDER BY geaendert')->fetchAll();
    if ($ang) {
        $t .= "\n📄 <b>عروض لازم تتابعها (أكتر من 3 أيام بدون رد):</b>\n";
        foreach (array_slice($ang, 0, 8) as $r) $t .= '• ' . sek_zeile($r) . ' · من ' . sek_alter((int) $r['geaendert']) . "\n";
        $t .= "<i>نصيحة: رسالة قصيرة \"هل عندك أسئلة عن العرض؟\" بترجّع كتير زباين.</i>\n";
    }
    $kon = $db->query("SELECT * FROM anfragen WHERE status = 'kontakt' AND termin IS NULL AND geaendert < " . (time() - 2 * 86400) . ' ORDER BY geaendert')->fetchAll();
    if ($kon) {
        $t .= "\n📞 <b>تواصلت معهم بس ما انبعت عرض لسا (أكتر من يومين):</b>\n";
        foreach (array_slice($kon, 0, 8) as $r) $t .= '• ' . sek_zeile($r) . "\n";
    }
    if ($alt) $t .= "\n⚠️ <b>" . count($alt) . "</b> طلب عمرو أكتر من 24 ساعة بدون رد – هدول أهم شي اليوم.\n";
    return $t;
}

function sek_tagesbericht(): string
{
    $heute = strtotime('today');
    $db = anf_db();
    $gestern = $db ? (int) $db->query('SELECT COUNT(*) FROM anfragen WHERE erstellt >= ' . ($heute - 86400) . ' AND erstellt < ' . $heute)->fetchColumn() : 0;
    $t = "☀️ <b>صباح الخير! تقرير " . SEK_TAGE[(int) date('N')] . ' ' . date('d.m.Y') . "</b>\n\n"
       . "📅 <b>مواعيد اليوم:</b>\n" . sek_termin_liste(sek_termine($heute, $heute + 86400))
       . "\n🆕 طلبات مبارح: <b>$gestern</b>\n"
       . sek_aufgaben();
    $morgen = sek_termine($heute + 86400, $heute + 2 * 86400);
    if ($morgen) $t .= "\n🔜 بكرا عندك <b>" . count($morgen) . "</b> موعد.\n";
    return $t;
}

function sek_zaehlen(int $von, int $bis): array
{
    $db = anf_db(); if (!$db) return [];
    $st = $db->prepare('SELECT * FROM anfragen WHERE erstellt >= ? AND erstellt < ?'); $st->execute([$von, $bis]);
    return $st->fetchAll();
}

function sek_top(array $rows, string $feld, int $n = 5): string
{
    $z = [];
    foreach ($rows as $r) { $k = trim((string) ($r[$feld] ?? '')); if ($k === '') $k = '–'; $z[$k] = ($z[$k] ?? 0) + 1; }
    arsort($z);
    $t = [];
    foreach (array_slice($z, 0, $n, true) as $k => $v) $t[] = sek_e(anf_kurz((string) $k, 40)) . ' <b>' . $v . '</b>';
    return $t ? implode(' · ', $t) : '–';
}

function sek_wochenbericht(bool $bisJetzt = false): string
{
    // Montags-Bericht: die 7 vollen Tage bis heute 0 Uhr; auf Befehl: die letzten 7 Tage bis jetzt
    $bis = $bisJetzt ? time() : strtotime('today');
    $von = $bis - 7 * 86400;
    $w = sek_zaehlen($von, $bis); $vw = sek_zaehlen($von - 7 * 86400, $von);
    $n = count($w); $nv = count($vw);
    $auftrag = count(array_filter($w, static fn($r) => in_array($r['status'], ['auftrag', 'erledigt'], true)));
    $termine = count(array_filter($w, static fn($r) => !empty($r['termin'])));
    $reak = array_values(array_filter(array_map(static fn($r) => !empty($r['erste_reaktion']) ? (int) $r['erste_reaktion'] - (int) $r['erstellt'] : null, $w), static fn($x) => $x !== null));
    $offen = count(array_filter($w, static fn($r) => $r['status'] === 'neu' && empty($r['termin'])));
    $diff = $nv > 0 ? (int) round(($n - $nv) / $nv * 100) : null;

    $t = "📊 <b>تقرير الأسبوع</b> (" . date('d.m.', $von) . ' – ' . date('d.m.', $bis - 1) . ")\n\n"
       . "📥 الطلبات: <b>$n</b>" . ($diff !== null ? ' (' . ($diff >= 0 ? '+' : '') . $diff . '% عن الأسبوع يلي قبلو)' : '') . "\n"
       . "📅 مواعيد استشارة: <b>$termine</b>\n"
       . "✅ صارو شغل: <b>$auftrag</b>" . ($n ? ' (' . round($auftrag / $n * 100) . '%)' : '') . "\n";
    if ($reak) { sort($reak); $med = $reak[intdiv(count($reak), 2)]; $t .= '⏱ سرعة الرد (الوسط): <b>' . sek_dauer($med) . "</b>\n"; }
    $t .= "\n🗺 <b>المناطق:</b> " . sek_top($w, 'region') . "\n"
        . '🏙 <b>المدن:</b> ' . sek_top($w, 'stadt') . "\n"
        . '🛠 <b>الخدمات:</b> ' . sek_top($w, 'leistung', 4) . "\n"
        . '📲 <b>من وين إجو:</b> ' . sek_top($w, 'quelle') . "\n";

    // Vorschläge – nur aus den eigenen Zahlen abgeleitet
    $tipps = [];
    if ($offen > 0) $tipps[] = "في <b>$offen</b> طلب من هالأسبوع لسا حالتو \"جديد\". رد عليهم أو غيّر حالتهم، هيك التقارير بتصير أدق.";
    if ($reak && $med > 4 * 3600) $tipps[] = 'سرعة الرد أكتر من 4 ساعات. الزبون يلي بيستنى كتير بيطلب من غيرك – جرّب ترد خلال ساعة ولو برسالة قصيرة.';
    if ($reak && $med <= 3600) $tipps[] = 'سرعة الرد ممتازة (أقل من ساعة) 👏 كمّل هيك.';
    $ang = count(array_filter($w, static fn($r) => $r['status'] === 'angebot'));
    if ($ang >= 2) $tipps[] = "في <b>$ang</b> عروض ناطرة جواب. اتصل أو ابعت رسالة متابعة بعد 3 أيام من العرض.";
    $nrw = count(array_filter($w, static fn($r) => ($r['region'] ?? '') === 'NRW'));
    if ($n >= 4 && $nrw / $n >= 0.4) $tipps[] = "حوالي " . round($nrw / $n * 100) . "% من الطلبات من NRW. صور شغل حقيقي من NRW بتقوّي صفحات المدن هناك كتير.";
    if ($n > 0 && $termine === 0) $tipps[] = 'ولا حدا حجز استشارة هالأسبوع. انشر رابط masar-werbeagentur.de/termin.html بالإنستغرام والفيسبوك وبتوقيع الإيميل.';
    if ($n === 0) $tipps[] = 'ما إجا ولا طلب هالأسبوع. شوف Google Search Console، وانشر شغل جديد عالسوشيال ميديا.';
    $sonst = count(array_filter($w, static fn($r) => ($r['region'] ?? '') === 'Sonstige'));
    if ($sonst >= 2) $tipps[] = "$sonst طلبات بدون مدينة واضحة. صحّح المدينة بصفحة الطلب، هيك بتعرف من وين بيجيك الشغل.";
    $t .= "\n💡 <b>اقتراحات لتحسين الشغل:</b>\n" . ($tipps ? '• ' . implode("\n• ", $tipps) : '• كل شي ماشي منيح هالأسبوع.') . "\n";
    $t .= "\n📅 <b>مواعيد الأسبوع الجاي:</b> " . count(sek_termine(strtotime('today'), strtotime('today') + 7 * 86400)) . "\n";
    return $t;
}

function sek_dauer(int $s): string
{
    if ($s < 3600) return max(1, intdiv($s, 60)) . ' دقيقة';
    if ($s < 86400) return round($s / 3600, 1) . ' ساعة';
    return round($s / 86400, 1) . ' يوم';
}

function sek_hilfe(): string
{
    return "🤖 <b>أنا سكرتيرك بمصار.</b> شو بعمل:\n"
         . "• ببعتلك كل طلب أو موعد جديد، وتحتو أزرار لتغيّر حالتو.\n"
         . "• بذكّرك قبل كل موعد بنص ساعة، وببعت للزبون إيميل تذكير قبل يوم.\n"
         . "• كل يوم الساعة 8 الصبح ببعتلك تقرير اليوم.\n"
         . "• كل يوم اثنين ببعتلك تقرير الأسبوع مع اقتراحات.\n\n"
         . "<b>الأوامر:</b>\n"
         . "/heute – مواعيد ومهام اليوم\n/morgen – مواعيد بكرا\n/termine – مواعيد 7 أيام\n/offen – الطلبات المفتوحة\n/bericht – تقرير الأسبوع هلأ\n/hilfe – هالرسالة\n\n"
         . "<i>ما ببعت أسماء ولا أرقام زباين هون (حماية البيانات). التفاصيل بصفحة الطلبات.</i>";
}

function sek_befehl(string $cmd): string
{
    $heute = strtotime('today');
    switch ($cmd) {
        case '/heute':   return "📅 <b>اليوم " . SEK_TAGE[(int) date('N')] . ' ' . date('d.m.') . "</b>\n" . sek_termin_liste(sek_termine($heute, $heute + 86400)) . sek_aufgaben();
        case '/morgen':  $m = $heute + 86400; return "📅 <b>بكرا " . SEK_TAGE[(int) date('N', $m)] . ' ' . date('d.m.', $m) . "</b>\n" . sek_termin_liste(sek_termine($m, $m + 86400));
        case '/termine':
            $rows = sek_termine(time(), $heute + 8 * 86400); if (!$rows) return '📅 ما في مواعيد بالأيام الـ 7 الجاية.';
            $t = "📅 <b>المواعيد الجاية:</b>\n";
            foreach ($rows as $r) $t .= '• ' . sek_e(sek_wann((int) $r['termin'])) . ' · ' . sek_e((string) $r['termin_art']) . ' · ' . sek_e((string) $r['sprache']) . ' · 📍 ' . sek_e((string) $r['stadt']) . "\n";
            return $t;
        case '/offen':   $a = sek_aufgaben(); return $a !== '' ? '📋 <b>الشغل المفتوح</b>' . $a : '🎉 ما في شي مفتوح. كل الطلبات انرد عليها.';
        case '/bericht': return sek_wochenbericht(true);
        default:         return sek_hilfe();
    }
}

// ─── Zeitgesteuerte Aufgaben (cron.php) ────────────────────────────────

/** Führt $tun genau einmal pro Schlüssel aus – vermerkt wird erst, wenn es geklappt hat (sonst neuer Versuch beim nächsten Lauf). */
function sek_einmal(string $schluessel, callable $tun): bool
{
    $db = anf_db(); if (!$db) return false;
    $db->exec('CREATE TABLE IF NOT EXISTS sek_log (schluessel TEXT PRIMARY KEY, zeit INTEGER)');
    $db->exec("DELETE FROM sek_log WHERE zeit < " . (time() - 60 * 86400) . " AND schluessel <> 'cron:letzter'");
    $st = $db->prepare('SELECT 1 FROM sek_log WHERE schluessel = ?'); $st->execute([$schluessel]);
    if ($st->fetchColumn()) return false;
    if (!$tun()) return false;
    $db->prepare('INSERT OR IGNORE INTO sek_log (schluessel, zeit) VALUES (?, ?)')->execute([$schluessel, time()]);
    return true;
}

function sek_cron(): array
{
    $log = [];
    $db = anf_db(); if (!$db) return ['keine Datenbank'];
    [$token, $chat] = sek_zugang();
    $tg = $token !== '' && $chat !== '';
    $jetzt = time();

    // 1) Erinnerung 30 Min. vor dem Termin
    foreach (sek_termine($jetzt, $jetzt + 35 * 60) as $r) {
        if ($tg && sek_einmal('erinnerung:' . $r['nr'], static fn() => sek_senden("⏰ <b>بعد " . max(1, intdiv((int) $r['termin'] - $jetzt, 60)) . " دقيقة عندك موعد</b>\n"
                . '🗓 ' . date('H:i', (int) $r['termin']) . ' · ' . sek_e((string) $r['termin_art']) . ' · 🗣 ' . sek_e((string) $r['sprache']) . "\n📍 " . sek_e((string) $r['stadt']) . "\n"
                . "<i>الرقم والتفاصيل بصفحة الطلب.</i>", [[['text' => '🔗 افتح الموعد', 'url' => SEK_ADMIN . '?nr=' . rawurlencode((string) $r['nr'])]]]))) {
            $log[] = 'Erinnerung ' . $r['nr'];
        }
    }

    // 2) Erinnerungs-E-Mail an den Kunden ~24 h vorher (nur wenn mit Vorlauf gebucht)
    foreach (sek_termine($jetzt + 2 * 3600, $jetzt + 24 * 3600) as $r) {
        if ((string) $r['email'] === '' || (int) $r['termin'] - (int) $r['erstellt'] < 26 * 3600) continue;
        $wann = anf_termin_text((int) $r['termin']);
        if (sek_einmal('kundenmail:' . $r['nr'], static fn() => anf_mail((string) $r['email'], "Erinnerung: Ihre Beratung am {$wann} – Masar Werbeagentur",
                'Guten Tag ' . $r['name'] . ",\n\nwir freuen uns auf Ihre kostenlose Beratung:\n\n  {$wann}\n  " . $r['termin_art'] . ' · ' . $r['sprache'] . "\n  Terminnummer: " . $r['nr'] . "\n\n"
                . "Falls etwas dazwischenkommt, antworten Sie einfach auf diese E-Mail oder schreiben Sie uns per WhatsApp: https://wa.me/491785143918\n\n"
                . "Mit freundlichen Grüßen\nMasar Werbeagentur\nBristolstraße 19E · 13349 Berlin · 0178 514 3918\n"))) {
            $log[] = 'Kundenmail ' . $r['nr'];
        }
    }

    // 3) Nach dem Termin: „Wie war's?“ mit Status-Tasten (1 Stunde nach Ende, solange Status noch „neu“)
    $st = $db->prepare("SELECT * FROM anfragen WHERE termin IS NOT NULL AND status = 'neu' AND termin + 60 * COALESCE(termin_dauer, 30) + 3600 < ? AND termin > ?");
    $st->execute([$jetzt, $jetzt - 2 * 86400]);
    foreach ($st->fetchAll() as $r) {
        if ($tg && sek_einmal('nachher:' . $r['nr'], static fn() => sek_senden("📝 <b>كيف كان الموعد؟</b>\n" . sek_e(sek_wann((int) $r['termin'])) . ' · ' . sek_e((string) $r['termin_art']) . ' · 📍 ' . sek_e((string) $r['stadt']) . ' · ' . sek_e((string) $r['nr'])
                . "\n\n<i>اختار شو صار، هيك بيضل التقرير مزبوط وبذكّرك تتابع.</i>", sek_tasten((string) $r['nr'])))) {
            $log[] = 'Nachfrage ' . $r['nr'];
        }
    }

    // 4) Tagesbericht ab 8 Uhr, montags zusätzlich Wochenbericht
    if ($tg && (int) date('G') >= 8 && (int) date('G') < 12) {
        if (sek_einmal('tag:' . date('Y-m-d'), static fn() => sek_senden(sek_tagesbericht()))) $log[] = 'Tagesbericht';
        if (date('N') === '1' && sek_einmal('woche:' . date('o-W'), static fn() => sek_senden(sek_wochenbericht()))) $log[] = 'Wochenbericht';
    }

    $db->exec('CREATE TABLE IF NOT EXISTS sek_log (schluessel TEXT PRIMARY KEY, zeit INTEGER)');
    $db->prepare('INSERT OR REPLACE INTO sek_log (schluessel, zeit) VALUES (?, ?)')->execute(['cron:letzter', $jetzt]);
    return $log;
}

function sek_letzter_cron(): int
{
    $db = anf_db(); if (!$db) return 0;
    try { return (int) $db->query("SELECT zeit FROM sek_log WHERE schluessel = 'cron:letzter'")->fetchColumn(); } catch (Throwable $e) { return 0; }
}

/** Geheimnis für Webhook und Cron – aus dem Bot-Token abgeleitet, steht nirgends im Klartext. */
function sek_geheim(string $zweck): string
{
    [$token] = sek_zugang();
    return $token === '' ? '' : substr(hash_hmac('sha256', 'masar-' . $zweck, $token), 0, 32);
}
