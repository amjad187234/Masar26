<?php
/**
 * Zeitgesteuerte Aufgaben des Sekretärs (Erinnerungen, Tages- und Wochenbericht).
 * Hostinger → Erweitert → Cron-Jobs, alle 5 Minuten:
 *   wget -q -O /dev/null "https://masar-werbeagentur.de/cron.php?k=SCHLÜSSEL"
 * Den Schlüssel zeigt /admin/anfragen.php → Einstellungen. Auch per CLI aufrufbar: php cron.php
 */

declare(strict_types=1);

require_once __DIR__ . '/inc/sekretaer.php';

header('Content-Type: text/plain; charset=UTF-8');
header('X-Robots-Tag: noindex');
if (PHP_SAPI !== 'cli') {
    $k = sek_geheim('cron');
    if ($k === '' || !hash_equals($k, (string) ($_GET['k'] ?? ''))) { http_response_code(403); exit('403'); }
}
$log = sek_cron();
echo 'ok ' . date('d.m.Y H:i') . ($log ? ': ' . implode(', ', $log) : '') . "\n";
