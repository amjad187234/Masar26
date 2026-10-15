<?php
/**
 * Telegram-Webhook des Sekretärs: Status-Tasten und Befehle (/heute, /offen …).
 * Nimmt nur Nachrichten an, die (1) das geheime Webhook-Token tragen und (2) aus dem
 * hinterlegten Chat des Inhabers kommen. Einrichtung: /admin/anfragen.php → Einstellungen.
 */

declare(strict_types=1);

require_once __DIR__ . '/inc/sekretaer.php';

header('Content-Type: application/json');
$geheim = sek_geheim('webhook');
if ($geheim === '' || !hash_equals($geheim, (string) ($_SERVER['HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN'] ?? ''))) {
    http_response_code(403); exit('{}');
}
[, $chat] = sek_zugang();
$u = json_decode((string) file_get_contents('php://input'), true);
if (!is_array($u)) exit('{}');

// Status-Taste
if (isset($u['callback_query'])) {
    $q = $u['callback_query'];
    $von = (string) ($q['message']['chat']['id'] ?? '');
    if ($von !== $chat) exit('{}');
    $teile = explode('|', (string) ($q['data'] ?? ''));
    $antwort = 'تمام';
    if (count($teile) === 3 && $teile[0] === 'st' && isset(ANF_STATUS[$teile[2]])) {
        $ok = sek_status($teile[1], $teile[2]);
        $antwort = $ok ? '✔️ ' . $teile[1] . ': ' . SEK_STATUS_AR[$teile[2]] : 'ما لقيت الطلب (يمكن انمسح).';
        if ($ok && isset($q['message']['message_id'])) {
            $text = (string) ($q['message']['text'] ?? '');
            $text = preg_replace('/\n\n✔️ الحالة: .*$/su', '', $text) ?? $text;
            sek_api('editMessageText', ['chat_id' => $chat, 'message_id' => $q['message']['message_id'],
                'text' => $text . "\n\n✔️ الحالة: " . SEK_STATUS_AR[$teile[2]] . ' (' . date('H:i') . ')',
                'reply_markup' => ['inline_keyboard' => sek_tasten($teile[1])]]);
        }
    }
    sek_api('answerCallbackQuery', ['callback_query_id' => $q['id'], 'text' => $antwort]);
    exit('{}');
}

// Befehl oder Text
if (isset($u['message'])) {
    $m = $u['message'];
    if ((string) ($m['chat']['id'] ?? '') !== $chat) exit('{}');
    $cmd = strtolower(explode('@', explode(' ', trim((string) ($m['text'] ?? '')))[0])[0]);
    sek_senden(sek_befehl($cmd));
}
echo '{}';
