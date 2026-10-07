<?php
/**
 * Kundenbewertungen – Masar Werbeagentur
 *
 * Ablauf
 * 1. Kunde füllt /bewerten.html aus (Link bekommt er persönlich nach dem Auftrag).
 * 2. Die Bewertung wird als „wartet“ in data/bewertungen.json gespeichert und
 *    per E-Mail mit zwei Links (Freigeben / Löschen) an uns geschickt.
 * 3. Erst nach der Freigabe erscheint sie auf der Website
 *    (abgerufen über bewertung.php?liste=1 von /bewertungen.js).
 *
 * Die Links in der Mail öffnen nur eine Bestätigungsseite; ausgeführt wird
 * erst per Klick (POST). Mail-Programme und Virenscanner rufen Links oft
 * automatisch auf – so wird nichts versehentlich freigegeben.
 *
 * data/ ist per .htaccess gesperrt und die JSON-Datei steht nicht im Git,
 * damit ein Deployment die gespeicherten Bewertungen nicht überschreibt.
 */

declare(strict_types=1);

date_default_timezone_set('Europe/Berlin');

// ─────────────────────────── Konfiguration ───────────────────────────

const EMPFAENGER     = 'info@masar-werbeagentur.de';
const ABSENDER       = 'website@masar-werbeagentur.de';
const KONFIG_DATEI   = __DIR__ . '/kontakt-config.php';
const DATEI          = __DIR__ . '/data/bewertungen.json';
const SEITE          = '/bewerten.html';
const SITE           = 'https://masar-werbeagentur.de';
const MAX_PRO_STUNDE = 3;
const MIN_SEKUNDEN   = 5;

// ─────────────────────────── Hilfsfunktionen ───────────────────────────

function weiter(string $ziel)
{
    header('Location: ' . $ziel, true, 303);
    exit;
}

function einzeilig(string $wert): string
{
    return trim(preg_replace('/\s+/u', ' ', str_replace("\0", '', $wert)) ?? '');
}

function feld(string $name): string
{
    return isset($_POST[$name]) && is_string($_POST[$name]) ? trim($_POST[$name]) : '';
}

function laenge(string $wert): int
{
    return mb_strlen($wert, 'UTF-8');
}

function h(string $wert): string
{
    return htmlspecialchars($wert, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

/**
 * Liest die Bewertungen, lässt $aendern optional Änderungen vornehmen und
 * schreibt zurück – alles unter einer Dateisperre.
 *
 * @param callable|null $aendern  function(array &$liste): mixed
 * @return mixed  Rückgabe von $aendern bzw. die Liste
 */
function mit_datei(?callable $aendern = null)
{
    $fp = @fopen(DATEI, 'c+');
    if (!$fp) {
        return $aendern ? false : [];
    }
    flock($fp, $aendern ? LOCK_EX : LOCK_SH);
    $inhalt = stream_get_contents($fp);
    $liste = json_decode($inhalt !== false && $inhalt !== '' ? $inhalt : '[]', true);
    if (!is_array($liste)) {
        $liste = [];
    }

    $ergebnis = $liste;
    if ($aendern) {
        $ergebnis = $aendern($liste);
        ftruncate($fp, 0);
        rewind($fp);
        fwrite($fp, json_encode(array_values($liste), JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
        fflush($fp);
    }
    flock($fp, LOCK_UN);
    fclose($fp);

    return $ergebnis;
}

function zu_viele_anfragen(): bool
{
    $ip = $_SERVER['REMOTE_ADDR'] ?? 'unbekannt';
    $datei = sys_get_temp_dir() . '/masar_bew_' . md5($ip) . '.txt';
    $jetzt = time();
    $zeiten = [];
    if (is_readable($datei)) {
        foreach (explode(',', (string) file_get_contents($datei)) as $t) {
            if ((int) $t > $jetzt - 3600) {
                $zeiten[] = (int) $t;
            }
        }
    }
    if (count($zeiten) >= MAX_PRO_STUNDE) {
        return true;
    }
    $zeiten[] = $jetzt;
    @file_put_contents($datei, implode(',', $zeiten), LOCK_EX);
    return false;
}

/** Öffentlich angezeigter Name: voll oder „Vorname N.“ */
function anzeigename(array $b): string
{
    $name = (string) $b['name'];
    if (($b['anzeige'] ?? 'kurz') === 'voll') {
        return $name;
    }
    $teile = preg_split('/\s+/u', $name) ?: [$name];
    $kurz = $teile[0];
    if (count($teile) > 1) {
        $kurz .= ' ' . mb_strtoupper(mb_substr((string) end($teile), 0, 1, 'UTF-8'), 'UTF-8') . '.';
    }
    return $kurz;
}

function mail_senden(string $betreff, string $text): bool
{
    $betreff_kodiert = '=?UTF-8?B?' . base64_encode($betreff) . '?=';
    $kopf = [
        'From: Masar Website <' . ABSENDER . '>',
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: 8bit',
    ];

    if (is_readable(KONFIG_DATEI)) {
        $konfig = require KONFIG_DATEI;
        if (is_array($konfig)) {
            require_once __DIR__ . '/mailer.php';
            $ok = masar_smtp_senden(
                $konfig,
                (string) ($konfig['from'] ?? ABSENDER),
                EMPFAENGER,
                implode("\r\n", array_merge(['To: ' . EMPFAENGER, 'Subject: ' . $betreff_kodiert], $kopf)),
                $text
            );
            if ($ok) {
                return true;
            }
        }
    }
    return @mail(EMPFAENGER, $betreff_kodiert, $text, implode("\r\n", $kopf), '-f' . ABSENDER);
}

function seite(string $titel, string $inhalt): void
{
    header('Content-Type: text/html; charset=UTF-8');
    header('X-Robots-Tag: noindex, nofollow');
    header('Cache-Control: no-store');
    echo '<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8">'
       . '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
       . '<meta name="robots" content="noindex, nofollow"><title>' . h($titel) . '</title>'
       . '<style>body{font-family:Arial,Helvetica,sans-serif;background:#f4f7fa;color:#132e50;margin:0;padding:24px}'
       . '.k{max-width:560px;margin:0 auto;background:#fff;border:1px solid #dce6ee;border-radius:12px;padding:24px}'
       . 'h1{font-size:22px;margin:0 0 12px}blockquote{margin:16px 0;padding:12px 16px;background:#f4f7fa;border-left:4px solid #58d0bd;white-space:pre-wrap}'
       . 'button{font-size:16px;font-weight:700;padding:12px 22px;border-radius:8px;border:0;cursor:pointer;margin:6px 8px 0 0}'
       . '.ja{background:#58d0bd;color:#132e50}.nein{background:#c0392b;color:#fff}.m{color:#5a6b7d;font-size:14px}</style>'
       . '</head><body><div class="k">' . $inhalt . '</div></body></html>';
    exit;
}

// ─────────────────────────── 1. Öffentliche Liste ───────────────────────────

if (($_SERVER['REQUEST_METHOD'] ?? '') === 'GET' && isset($_GET['liste'])) {
    $aus = [];
    foreach (mit_datei() as $b) {
        if (($b['status'] ?? '') !== 'frei') {
            continue;
        }
        $aus[] = [
            'name'     => anzeigename($b),
            'firma'    => (string) ($b['firma'] ?? ''),
            'leistung' => (string) ($b['leistung'] ?? ''),
            'sterne'   => (int) $b['sterne'],
            'text'     => (string) $b['text'],
            'datum'    => substr((string) $b['datum'], 0, 10),
        ];
    }
    // Neueste zuerst
    usort($aus, static fn($a, $b) => strcmp($b['datum'], $a['datum']));

    header('Content-Type: application/json; charset=UTF-8');
    header('Cache-Control: public, max-age=300');
    header('X-Robots-Tag: noindex');
    echo json_encode($aus, JSON_UNESCAPED_UNICODE);
    exit;
}

// ─────────────────────────── 2. Freigeben / Löschen ───────────────────────────

$aktion = (string) ($_GET['aktion'] ?? $_POST['aktion'] ?? '');
if (in_array($aktion, ['freigeben', 'loeschen'], true)) {
    $id    = (string) ($_GET['id'] ?? $_POST['id'] ?? '');
    $token = (string) ($_GET['token'] ?? $_POST['token'] ?? '');

    $treffer = null;
    foreach (mit_datei() as $b) {
        if (hash_equals((string) $b['id'], $id) && hash_equals((string) $b['token'], $token)) {
            $treffer = $b;
            break;
        }
    }
    if ($treffer === null || $token === '') {
        http_response_code(404);
        seite('Nicht gefunden', '<h1>Bewertung nicht gefunden</h1><p class="m">Der Link ist ungültig oder die Bewertung wurde bereits gelöscht.</p>');
    }

    $vorschau = '<p><strong>' . h(anzeigename($treffer)) . '</strong>'
              . ($treffer['firma'] !== '' ? ' · ' . h($treffer['firma']) : '')
              . ' · ' . str_repeat('★', (int) $treffer['sterne']) . str_repeat('☆', 5 - (int) $treffer['sterne']) . '</p>'
              . '<blockquote>' . h($treffer['text']) . '</blockquote>'
              . '<p class="m">Status: ' . ($treffer['status'] === 'frei' ? 'veröffentlicht' : 'wartet auf Freigabe')
              . ' · eingegangen am ' . h(substr($treffer['datum'], 0, 10)) . '</p>';

    if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
        $knopf = $aktion === 'freigeben'
            ? '<button class="ja" type="submit">Jetzt veröffentlichen</button>'
            : '<button class="nein" type="submit">Endgültig löschen</button>';
        seite('Bewertung prüfen', '<h1>' . ($aktion === 'freigeben' ? 'Bewertung veröffentlichen?' : 'Bewertung löschen?') . '</h1>'
            . $vorschau
            . '<form method="post" action="/bewertung.php">'
            . '<input type="hidden" name="aktion" value="' . h($aktion) . '">'
            . '<input type="hidden" name="id" value="' . h($id) . '">'
            . '<input type="hidden" name="token" value="' . h($token) . '">'
            . $knopf . '</form>');
    }

    mit_datei(static function (array &$liste) use ($aktion, $id): bool {
        foreach ($liste as $i => $b) {
            if ($b['id'] === $id) {
                if ($aktion === 'freigeben') {
                    $liste[$i]['status'] = 'frei';
                    $liste[$i]['freigegeben'] = date('c');
                } else {
                    unset($liste[$i]);
                }
                return true;
            }
        }
        return false;
    });

    seite('Erledigt', $aktion === 'freigeben'
        ? '<h1>Veröffentlicht ✓</h1><p>Die Bewertung ist jetzt auf der Website sichtbar (spätestens nach 5 Minuten).</p><p class="m">Zum späteren Entfernen den Löschen-Link aus derselben E-Mail benutzen.</p>'
        : '<h1>Gelöscht ✓</h1><p>Die Bewertung wurde vollständig entfernt.</p>');
}

// ─────────────────────────── 3. Neue Bewertung ───────────────────────────

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    weiter(SEITE);
}

// Honeypot und Mindestzeit: Bots bekommen die Erfolgsseite und merken nichts
if (feld('_honey') !== '') {
    weiter(SEITE . '?gesendet=1');
}
$start = feld('_t');
if ($start !== '' && ctype_digit($start)) {
    $sek = (microtime(true) * 1000 - (int) $start) / 1000;
    if ($sek >= 0 && $sek < MIN_SEKUNDEN) {
        weiter(SEITE . '?gesendet=1');
    }
}
if (zu_viele_anfragen()) {
    weiter(SEITE . '?fehler=limit');
}

$name     = einzeilig(feld('name'));
$firma    = einzeilig(feld('firma'));
$leistung = einzeilig(feld('leistung'));
$sterne   = (int) feld('sterne');
$text     = trim(preg_replace("/\r\n?/", "\n", feld('text')) ?? '');
$text     = preg_replace("/\n{3,}/", "\n\n", $text) ?? $text;
$anzeige  = feld('anzeige') === 'voll' ? 'voll' : 'kurz';

if (laenge($name) < 2 || laenge($name) > 60
    || laenge($firma) > 80 || laenge($leistung) > 60
    || $sterne < 1 || $sterne > 5
    || laenge($text) < 20 || laenge($text) > 1500
    || feld('einwilligung') !== 'ja') {
    weiter(SEITE . '?fehler=angaben');
}

$neu = [
    'id'       => bin2hex(random_bytes(6)),
    'token'    => bin2hex(random_bytes(16)),
    'status'   => 'wartet',
    'datum'    => date('c'),
    'name'     => $name,
    'firma'    => $firma,
    'leistung' => $leistung,
    'sterne'   => $sterne,
    'text'     => $text,
    'anzeige'  => $anzeige,
];

$gespeichert = mit_datei(static function (array &$liste) use ($neu): bool {
    $liste[] = $neu;
    return true;
});
if ($gespeichert !== true) {
    weiter(SEITE . '?fehler=technik');
}

$link = SITE . '/bewertung.php?id=' . $neu['id'] . '&token=' . $neu['token'] . '&aktion=';
mail_senden(
    'Neue Bewertung: ' . $sterne . ' Sterne von ' . $name,
    "Neue Bewertung über die Website (noch NICHT veröffentlicht):\n\n"
    . "Name:      {$name}\n"
    . 'Angezeigt: ' . anzeigename($neu) . "\n"
    . 'Firma:     ' . ($firma !== '' ? $firma : '–') . "\n"
    . 'Leistung:  ' . ($leistung !== '' ? $leistung : '–') . "\n"
    . 'Sterne:    ' . str_repeat('★', $sterne) . str_repeat('☆', 5 - $sterne) . " ({$sterne}/5)\n\n"
    . $text . "\n\n"
    . "Bitte prüfen, ob die Person wirklich Kunde war.\n\n"
    . "Veröffentlichen:\n{$link}freigeben\n\n"
    . "Löschen (auch später, wenn schon veröffentlicht):\n{$link}loeschen\n\n"
    . "Diese E-Mail aufbewahren – nur mit diesen Links lässt sich die Bewertung verwalten.\n"
);

weiter(SEITE . '?gesendet=1');
