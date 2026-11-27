<?php
/**
 * IndexNow – geänderte Seiten an Bing & Co. melden (gemeinsame Logik).
 *
 * Genutzt von /indexnow.php (von Hand im Browser) und von cron.php (automatisch,
 * sobald sich sitemap.xml geändert hat). Gemeldet werden nur URLs, deren <lastmod>
 * sich seit der letzten Meldung geändert hat; der Stand liegt in data/indexnow.json.
 * Der Schlüssel ist öffentlich (so verlangt es IndexNow).
 */

declare(strict_types=1);

const INDEXNOW_HOST     = 'masar-werbeagentur.de';
const INDEXNOW_KEY      = '016f0c80ae1bc78d09f7ee8a1473682a';
const INDEXNOW_ENDPOINT = 'https://api.indexnow.org/indexnow';
const INDEXNOW_SITEMAP  = __DIR__ . '/../sitemap.xml';
const INDEXNOW_STAND    = __DIR__ . '/../data/indexnow.json';
const INDEXNOW_PAUSE    = 600;

/**
 * @return array{status:string,urls:array<int,string>,code:int,antwort:string,zeit:int,gesamt:int}
 * status: fehler_sitemap | aktuell | test | pause | gemeldet | fehler
 */
function indexnow_melden(bool $alle = false, bool $test = false): array
{
    $erg = ['status' => 'fehler_sitemap', 'urls' => [], 'code' => 0, 'antwort' => '', 'zeit' => 0, 'gesamt' => 0];
    $xml = @simplexml_load_file(INDEXNOW_SITEMAP);
    if ($xml === false) { return $erg; }
    $aktuell = [];
    foreach ($xml->url as $u) {
        $loc = trim((string) $u->loc);
        if ($loc !== '' && parse_url($loc, PHP_URL_HOST) === INDEXNOW_HOST) { $aktuell[$loc] = trim((string) $u->lastmod); }
    }
    $stand = ['zeit' => 0, 'urls' => [], 'sitemap' => 0];
    if (is_readable(INDEXNOW_STAND)) {
        $d = json_decode((string) file_get_contents(INDEXNOW_STAND), true);
        if (is_array($d)) { $stand = array_merge($stand, $d); }
    }
    $neu = [];
    foreach ($aktuell as $loc => $lastmod) {
        if ($alle || !isset($stand['urls'][$loc]) || $stand['urls'][$loc] !== $lastmod) { $neu[] = $loc; }
    }
    $erg['urls'] = $neu; $erg['zeit'] = (int) $stand['zeit']; $erg['gesamt'] = count($aktuell);
    if (!$neu)  { $erg['status'] = 'aktuell'; indexnow_stand_sitemap($stand); return $erg; }
    if ($test)  { $erg['status'] = 'test'; return $erg; }
    if (time() - (int) $stand['zeit'] < INDEXNOW_PAUSE) { $erg['status'] = 'pause'; return $erg; }

    // max. 10.000 URLs pro Anfrage laut IndexNow
    $body = json_encode([
        'host'        => INDEXNOW_HOST,
        'key'         => INDEXNOW_KEY,
        'keyLocation' => 'https://' . INDEXNOW_HOST . '/' . INDEXNOW_KEY . '.txt',
        'urlList'     => array_values(array_slice($neu, 0, 10000)),
    ], JSON_UNESCAPED_SLASHES);

    $code = 0; $antwort = '';
    if (function_exists('curl_init')) {
        $ch = curl_init(INDEXNOW_ENDPOINT);
        curl_setopt_array($ch, [
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => $body,
            CURLOPT_HTTPHEADER => ['Content-Type: application/json; charset=utf-8'],
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 20,
        ]);
        $antwort = (string) curl_exec($ch);
        $code = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
    } else {
        $ctx = stream_context_create(['http' => ['method' => 'POST', 'header' => "Content-Type: application/json; charset=utf-8\r\n", 'content' => $body, 'timeout' => 20, 'ignore_errors' => true]]);
        $antwort = (string) @file_get_contents(INDEXNOW_ENDPOINT, false, $ctx);
        if (isset($http_response_header[0]) && preg_match('/\s(\d{3})\s/', $http_response_header[0], $m)) { $code = (int) $m[1]; }
    }
    $erg['code'] = $code; $erg['antwort'] = $antwort;

    // Stand immer mit Zeit schreiben, damit ein Fehler nicht alle 5 Minuten wiederholt wird
    $stand['zeit'] = time();
    if ($code === 200 || $code === 202) {   // 202 = angenommen, Schlüssel wird noch geprüft
        foreach ($neu as $loc) { $stand['urls'][$loc] = $aktuell[$loc]; }
        $erg['status'] = 'gemeldet';
        indexnow_stand_sitemap($stand);
    } else {
        $erg['status'] = 'fehler';
        @file_put_contents(INDEXNOW_STAND, json_encode($stand, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT), LOCK_EX);
    }
    return $erg;
}

/** Merkt sich, für welchen Stand der sitemap.xml zuletzt alles gemeldet war. */
function indexnow_stand_sitemap(array $stand): void
{
    $stand['sitemap'] = (int) @filemtime(INDEXNOW_SITEMAP);
    @file_put_contents(INDEXNOW_STAND, json_encode($stand, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT), LOCK_EX);
}

/**
 * Für cron.php: meldet nur, wenn sitemap.xml seit der letzten vollständigen Meldung neu ist.
 * Kostet im Normalfall einen Dateizugriff. Gibt eine kurze Logzeile zurück oder ''.
 */
function indexnow_auto(): string
{
    $m = (int) @filemtime(INDEXNOW_SITEMAP);
    if ($m === 0) { return ''; }
    if (is_readable(INDEXNOW_STAND)) {
        $d = json_decode((string) file_get_contents(INDEXNOW_STAND), true);
        if (is_array($d) && (int) ($d['sitemap'] ?? 0) === $m) { return ''; }
    }
    $e = indexnow_melden();
    if ($e['status'] === 'gemeldet') { return 'IndexNow: ' . count($e['urls']) . ' URL(s) gemeldet'; }
    if ($e['status'] === 'fehler')   { return 'IndexNow: Fehler ' . $e['code']; }
    return '';
}
