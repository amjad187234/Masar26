<?php
/**
 * Schnittstelle des KI-Chatbot-Generators (Versuch). Logik und Schutz: inc/ki_generator.php
 *   GET  ?a=status                 → {an: true|false}
 *   POST {a:"start", url:"…", ok:true}  → Vorführung anlegen
 *   POST {a:"chat", id:"…", text:"…"}   → Antwort
 */

declare(strict_types=1);

require_once __DIR__ . '/inc/ki_generator.php';

header('Content-Type: application/json; charset=UTF-8');
header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: no-store');

function kg_aus(array $d, int $code = 200): void { http_response_code($code); echo json_encode($d, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES); exit; }

if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'GET') {
    kg_aus(['an' => (($_GET['a'] ?? '') === 'status') && kg_gesperrt() === '']);
}
if ($_SERVER['REQUEST_METHOD'] !== 'POST') kg_aus(['ok' => false, 'fehler' => 'Nicht erlaubt.'], 405);

// Nur Aufrufe von der eigenen Website
$eigen = strtolower((string) ($_SERVER['HTTP_HOST'] ?? ''));
$herkunft = strtolower((string) parse_url((string) ($_SERVER['HTTP_ORIGIN'] ?? ($_SERVER['HTTP_REFERER'] ?? '')), PHP_URL_HOST));
$port = parse_url((string) ($_SERVER['HTTP_ORIGIN'] ?? ($_SERVER['HTTP_REFERER'] ?? '')), PHP_URL_PORT);
if ($herkunft === '' || ($herkunft !== $eigen && $herkunft . ':' . $port !== $eigen)) kg_aus(['ok' => false, 'fehler' => 'Nicht erlaubt.'], 403);
if (stripos((string) ($_SERVER['CONTENT_TYPE'] ?? ''), 'application/json') !== 0) kg_aus(['ok' => false, 'fehler' => 'Nicht erlaubt.'], 415);

$roh = (string) file_get_contents('php://input', false, null, 0, 4000);
$d = json_decode($roh, true);
if (!is_array($d)) kg_aus(['ok' => false, 'fehler' => 'Ungültige Anfrage.'], 400);

try {
    switch ((string) ($d['a'] ?? '')) {
        case 'start':
            if (empty($d['ok'])) kg_aus(['ok' => false, 'fehler' => 'Bitte bestätigen Sie den Hinweis.']);
            kg_aus(kg_start((string) ($d['url'] ?? '')));
        case 'chat':
            kg_aus(kg_chat((string) ($d['id'] ?? ''), (string) ($d['text'] ?? '')));
        default:
            kg_aus(['ok' => false, 'fehler' => 'Ungültige Anfrage.'], 400);
    }
} catch (Throwable $e) {
    error_log('ki-generator: ' . $e->getMessage());
    kg_aus(['ok' => false, 'fehler' => 'Das hat leider nicht geklappt. Bitte noch einmal versuchen.'], 500);
}
