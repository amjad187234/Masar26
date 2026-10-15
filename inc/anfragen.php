<?php
/**
 * Anfragen-Speicher – Masar Werbeagentur
 *
 * Jede Anfrage (Formular, E-Mail-Assistent, WhatsApp-Assistent) bekommt eine
 * Nummer (ANF-2026-0001) und wird in data/anfragen.sqlite gespeichert.
 * Die Datei liegt im gesperrten Ordner data/ und ist nicht im Git-Repository.
 *
 * Benachrichtigung per Telegram: bewusst OHNE personenbezogene Daten
 * (nur Nummer, Leistung, Ort, Quelle) – die Details stehen nur in der
 * geschützten Übersicht /admin/anfragen.php.
 *
 * Aufbewahrung: Anfragen werden nach 6 Monaten automatisch gelöscht (wie in der Datenschutzerklärung),
 * sofern sie nicht vorher gelöscht wurden (siehe Datenschutzerklärung).
 */

declare(strict_types=1);

const ANF_DB         = __DIR__ . '/../data/anfragen.sqlite';
const ANF_KONFIG     = __DIR__ . '/../kontakt-config.php';
const ANF_MONATE     = 6;
const ANF_STATUS     = ['neu' => 'Neu', 'kontakt' => 'In Kontakt', 'angebot' => 'Angebot gesendet', 'auftrag' => 'Auftrag', 'erledigt' => 'Erledigt', 'verloren' => 'Kein Auftrag'];

/** Fehlermeldung, falls kontakt-config.php einen Tippfehler enthält ('' = alles in Ordnung). */
function anf_konfig_fehler(): string
{
    anf_konfig();
    return $GLOBALS['ANF_KONFIG_FEHLER'] ?? '';
}

function anf_konfig(): array
{
    static $k = null;
    if ($k === null) {
        $k = [];
        if (is_readable(ANF_KONFIG)) {
            // Tippfehler in kontakt-config.php dürfen die Seite nicht lahmlegen
            try { $k = require ANF_KONFIG; } catch (Throwable $e) {
                error_log('kontakt-config.php: ' . $e->getMessage());
                $GLOBALS['ANF_KONFIG_FEHLER'] = $e->getMessage() . ' (Zeile ' . $e->getLine() . ')';
                $k = [];
            }
        }
        if (!is_array($k)) $k = [];
        // Beim Kopieren aus Telegram kommt oft Text mit – nur Token bzw. Chat-ID übernehmen
        if (preg_match('/\d{6,}:[A-Za-z0-9_-]{30,}/', (string) ($k['telegram_token'] ?? ''), $m)) $k['telegram_token'] = $m[0];
        if (preg_match('/-?\d{5,}/', (string) ($k['telegram_chat'] ?? ''), $m)) $k['telegram_chat'] = $m[0];
    }
    return $k;
}

function anf_db(): ?PDO
{
    static $pdo = null;
    if ($pdo instanceof PDO) return $pdo;
    if (!class_exists('PDO') || !in_array('sqlite', PDO::getAvailableDrivers(), true)) return null;
    try {
        $pdo = new PDO('sqlite:' . ANF_DB, null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
        $pdo->exec('PRAGMA journal_mode = WAL');
        $pdo->exec('CREATE TABLE IF NOT EXISTS anfragen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nr TEXT UNIQUE,
            erstellt INTEGER NOT NULL,
            geaendert INTEGER NOT NULL,
            quelle TEXT,
            seite TEXT,
            status TEXT NOT NULL DEFAULT "neu",
            name TEXT, firma TEXT, email TEXT, telefon TEXT, ort TEXT,
            leistung TEXT, zusammenfassung TEXT, daten TEXT,
            notiz TEXT DEFAULT ""
        )');
        $pdo->exec('CREATE INDEX IF NOT EXISTS i_status ON anfragen(status)');
        // Aufbewahrungsfrist
        $pdo->prepare('DELETE FROM anfragen WHERE erstellt < ?')->execute([time() - ANF_MONATE * 30 * 86400]);
    } catch (Throwable $e) {
        error_log('Anfragen-DB: ' . $e->getMessage());
        $pdo = null;
    }
    return $pdo;
}

function anf_kurz(string $s, int $n): string
{
    $s = trim(str_replace(["\r", "\0"], '', $s));
    return mb_substr($s, 0, $n);
}

/**
 * Speichert eine Anfrage und gibt die Anfragenummer zurück (oder '' bei Fehler).
 * $f: name, firma, email, telefon, ort, leistung, zusammenfassung, daten (array), quelle, seite
 */
function anf_speichern(array $f): string
{
    $db = anf_db();
    if (!$db) return '';
    try {
        $jetzt = time();
        $st = $db->prepare('INSERT INTO anfragen (erstellt, geaendert, quelle, seite, name, firma, email, telefon, ort, leistung, zusammenfassung, daten)
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)');
        $st->execute([
            $jetzt, $jetzt,
            anf_kurz((string) ($f['quelle'] ?? 'Formular'), 30),
            anf_kurz((string) ($f['seite'] ?? ''), 200),
            anf_kurz((string) ($f['name'] ?? ''), 120),
            anf_kurz((string) ($f['firma'] ?? ''), 120),
            anf_kurz((string) ($f['email'] ?? ''), 160),
            anf_kurz((string) ($f['telefon'] ?? ''), 60),
            anf_kurz((string) ($f['ort'] ?? ''), 120),
            anf_kurz((string) ($f['leistung'] ?? ''), 200),
            anf_kurz((string) ($f['zusammenfassung'] ?? ''), 6000),
            json_encode($f['daten'] ?? [], JSON_UNESCAPED_UNICODE),
        ]);
        $id = (int) $db->lastInsertId();
        $nr = sprintf('ANF-%s-%04d', date('Y', $jetzt), $id);
        $db->prepare('UPDATE anfragen SET nr = ? WHERE id = ?')->execute([$nr, $id]);
        anf_telegram($nr, (string) ($f['leistung'] ?? ''), (string) ($f['ort'] ?? ''), (string) ($f['quelle'] ?? 'Formular'));
        return $nr;
    } catch (Throwable $e) {
        error_log('Anfrage speichern: ' . $e->getMessage());
        return '';
    }
}

/** Telegram-Hinweis ohne personenbezogene Daten. */
function anf_telegram(string $nr, string $leistung, string $ort, string $quelle): bool
{
    $k = anf_konfig();
    $token = (string) ($k['telegram_token'] ?? '');
    $chat  = (string) ($k['telegram_chat'] ?? '');
    if ($token === '' || $chat === '') return false;
    $text = "🔔 Neue Anfrage {$nr}\n"
          . ($leistung !== '' ? "Leistung: " . anf_kurz($leistung, 80) . "\n" : '')
          . ($ort !== '' ? "Ort: " . anf_kurz($ort, 60) . "\n" : '')
          . "Über: {$quelle}\n"
          . "https://masar-werbeagentur.de/admin/anfragen.php?nr=" . rawurlencode($nr);
    return anf_telegram_senden($token, $chat, $text);
}

/** GET-Abruf der Bot-API (gibt die Antwort auch bei HTTP-Fehlern zurück, '' wenn keine Verbindung). */
function anf_telegram_abruf(string $token, string $methode): string
{
    $url = 'https://api.telegram.org/bot' . $token . '/' . $methode;
    if (function_exists('curl_init')) {
        $ch = curl_init($url);
        curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 8]);
        $r = curl_exec($ch); curl_close($ch);
        return is_string($r) ? $r : '';
    }
    $r = @file_get_contents($url, false, stream_context_create(['http' => ['timeout' => 8, 'ignore_errors' => true]]));
    return is_string($r) ? $r : '';
}

function anf_telegram_senden(string $token, string $chat, string $text): bool
{
    $url = 'https://api.telegram.org/bot' . $token . '/sendMessage';
    $body = http_build_query(['chat_id' => $chat, 'text' => $text, 'disable_web_page_preview' => 'true']);
    if (function_exists('curl_init')) {
        $ch = curl_init($url);
        curl_setopt_array($ch, [CURLOPT_POST => true, CURLOPT_POSTFIELDS => $body, CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 6]);
        $r = curl_exec($ch); $code = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE); curl_close($ch);
        return $r !== false && $code === 200;
    }
    $ctx = stream_context_create(['http' => ['method' => 'POST', 'header' => "Content-Type: application/x-www-form-urlencoded\r\n", 'content' => $body, 'timeout' => 6, 'ignore_errors' => true]]);
    return @file_get_contents($url, false, $ctx) !== false;
}
