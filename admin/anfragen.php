<?php
/**
 * Anfragen-Übersicht – Masar Werbeagentur
 * Aufruf: https://masar-werbeagentur.de/admin/anfragen.php
 *
 * Einrichtung (einmalig, in kontakt-config.php auf dem Server):
 *   'admin_pass_hash' => '…'   // auf dieser Seite erzeugen lassen
 *   'telegram_token'  => '…'   // optional, von @BotFather
 *   'telegram_chat'   => '…'   // optional, Chat-ID (auf dieser Seite suchen)
 */

declare(strict_types=1);

header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: no-store');
header('X-Frame-Options: DENY');
header('Referrer-Policy: no-referrer');

session_set_cookie_params(['lifetime' => 0, 'path' => '/admin/', 'secure' => !empty($_SERVER['HTTPS']), 'httponly' => true, 'samesite' => 'Strict']);
session_name('masar_anf');
session_start();

require_once dirname(__DIR__) . '/inc/anfragen.php';
$K = anf_konfig();
$HASH = (string) ($K['admin_pass_hash'] ?? '');

function h($s): string { return htmlspecialchars((string) $s, ENT_QUOTES, 'UTF-8'); }
function csrf(): string { if (empty($_SESSION['csrf'])) $_SESSION['csrf'] = bin2hex(random_bytes(24)); return $_SESSION['csrf']; }
function csrf_ok(): bool { return isset($_POST['csrf']) && hash_equals(csrf(), (string) $_POST['csrf']); }
function sperre_datei(): string { return sys_get_temp_dir() . '/masar_anf_login_' . md5($_SERVER['REMOTE_ADDR'] ?? 'x') . '.txt'; }
function fehlversuche(): array { $z = array_filter(array_map('intval', explode(',', (string) @file_get_contents(sperre_datei()))), fn($t) => $t > time() - 900); return array_values($z); }
function wa_nummer(string $tel): string
{
    $d = preg_replace('/\D+/', '', $tel) ?? '';
    if (str_starts_with($d, '00')) $d = substr($d, 2);
    elseif (str_starts_with($d, '0')) $d = '49' . substr($d, 1);
    return strlen($d) >= 9 ? $d : '';
}

function seite(string $titel, string $inhalt): void
{
    echo '<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
       . '<meta name="robots" content="noindex, nofollow"><title>' . h($titel) . ' | Masar Anfragen</title><style>'
       . ':root{--n:#132e50;--t:#58d0bd;--ti:#177567;--b:#dce6ee;--m:#5a7070;--bg:#f4f7fa}'
       . '*{box-sizing:border-box}body{margin:0;font-family:Arial,Helvetica,sans-serif;background:var(--bg);color:var(--n);font-size:15px}'
       . 'header{background:var(--n);color:#fff;padding:14px 18px;display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap}'
       . 'header b{color:var(--t);letter-spacing:.5px}header a{color:#fff;font-size:14px;margin-left:14px}'
       . 'main{max-width:1100px;margin:0 auto;padding:18px}.k{background:#fff;border:1px solid var(--b);border-radius:12px;padding:18px;margin-bottom:16px}'
       . 'h1{font-size:22px;margin:0 0 12px}h2{font-size:17px;margin:0 0 10px}table{width:100%;border-collapse:collapse}'
       . 'th,td{text-align:left;padding:10px 8px;border-bottom:1px solid var(--b);vertical-align:top;font-size:14px}th{font-size:12px;text-transform:uppercase;color:var(--m)}'
       . 'tr.neu td:first-child{border-left:4px solid var(--t)}a{color:var(--ti)}'
       . '.tag{display:inline-block;padding:3px 9px;border-radius:999px;font-size:12px;font-weight:700;background:#e8f8f5;color:var(--ti)}'
       . '.tag.neu{background:var(--t);color:var(--n)}.tag.verloren{background:#f3e6e6;color:#8a3030}.tag.erledigt{background:#e6eef7;color:var(--n)}'
       . 'input,select,textarea{font:inherit;padding:10px 12px;border:1px solid var(--b);border-radius:8px;width:100%;background:#fff;color:var(--n)}'
       . 'textarea{min-height:110px}button,.btn{display:inline-flex;align-items:center;gap:.4rem;border:0;border-radius:8px;padding:10px 14px;font:700 14px Arial;cursor:pointer;background:var(--n);color:#fff;text-decoration:none}'
       . '.btn.wa{background:#25d366;color:#08331a}.btn.l{background:#fff;color:var(--n);border:1px solid var(--b)}.btn.r{background:#b3261e}'
       . '.row{display:flex;gap:10px;flex-wrap:wrap;align-items:end}.row>*{flex:1;min-width:160px}.chips{display:flex;gap:6px;flex-wrap:wrap}'
       . '.chips a{padding:6px 12px;border-radius:999px;border:1px solid var(--b);background:#fff;text-decoration:none;font-size:13px;color:var(--n)}.chips a.on{background:var(--n);color:#fff}'
       . 'pre{white-space:pre-wrap;background:var(--bg);border-radius:8px;padding:12px;font:13px/1.55 Arial;margin:0}.m{color:var(--m);font-size:13px}'
       . '.ok{background:#e8f8f5;border:1px solid var(--t);padding:10px 12px;border-radius:8px;margin-bottom:12px}.err{background:#fbeaea;border:1px solid #e3a0a0;padding:10px 12px;border-radius:8px;margin-bottom:12px}'
       . '.grid{display:grid;grid-template-columns:2fr 1fr;gap:16px}@media(max-width:800px){.grid{grid-template-columns:1fr}.hide-m{display:none}th,td{padding:8px 5px}}'
       . '</style></head><body><header><div><b>MASAR</b> · Anfragen</div>'
       . (!empty($_SESSION['ok']) ? '<nav><a href="anfragen.php">Übersicht</a><a href="anfragen.php?ansicht=einstellungen">Einstellungen</a><a href="anfragen.php?export=csv">CSV</a><a href="anfragen.php?abmelden=1">Abmelden</a></nav>' : '')
       . '</header><main>' . $inhalt . '</main></body></html>';
    exit;
}

// ─── Tippfehler in kontakt-config.php ──────────────────────────────────
if (anf_konfig_fehler() !== '') {
    seite('Konfiguration', '<div class="k" style="max-width:560px"><h1>Fehler in kontakt-config.php</h1>'
        . '<div class="err">' . h(anf_konfig_fehler()) . '</div>'
        . '<p class="m">Meist fehlt ein Anführungszeichen <code>\'</code> oder ein Komma <code>,</code> am Zeilenende, '
        . 'oder beim Einfügen ist zusätzlicher Text mitgekommen. Jede Zeile muss so aussehen: <code>\'name\' => \'wert\',</code></p>'
        . '<p class="m">Das Kontaktformular funktioniert trotzdem weiter (Versand über den Server).</p></div>');
    exit;
}

// ─── Einrichtung: noch kein Passwort hinterlegt ─────────────────────────
if ($HASH === '') {
    $out = '';
    if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST' && csrf_ok()) {
        $pw = (string) ($_POST['pw'] ?? '');
        if (mb_strlen($pw) < 10) $out = '<div class="err">Bitte mindestens 10 Zeichen.</div>';
        else $out = '<div class="ok"><b>Fertig.</b> Diese Zeile in <code>kontakt-config.php</code> (im return-Array) einfügen und speichern:</div><textarea id="zeile" readonly rows="3" style="width:100%;font-family:monospace;font-size:13px" onclick="this.select()">\'admin_pass_hash\' => \'' . h(password_hash($pw, PASSWORD_DEFAULT)) . '\',</textarea><button type="button" style="margin:8px 0" onclick="var t=document.getElementById(\'zeile\');t.select();navigator.clipboard?navigator.clipboard.writeText(t.value).then(function(){this.textContent=\'✓ Kopiert\'}.bind(this)):document.execCommand(\'copy\')">Zeile kopieren</button><p class="m">Das Passwort selbst wird nirgends gespeichert. Danach diese Seite neu laden und anmelden.</p>';
    }
    seite('Einrichtung', '<div class="k" style="max-width:560px"><h1>Einrichtung</h1><p class="m">Für die Anfragen-Übersicht ist noch kein Passwort hinterlegt. Wählen Sie ein Passwort – die Seite erzeugt daraus eine verschlüsselte Zeile für <code>kontakt-config.php</code>.</p>'
        . $out . '<form method="post"><input type="hidden" name="csrf" value="' . h(csrf()) . '"><p><input type="password" name="pw" minlength="10" required placeholder="Neues Passwort (mind. 10 Zeichen)" autocomplete="new-password"></p><button>Zeile erzeugen</button></form></div>');
}

// ─── An-/Abmelden ───────────────────────────────────────────────────────
if (isset($_GET['abmelden'])) { $_SESSION = []; session_destroy(); header('Location: anfragen.php'); exit; }
if (empty($_SESSION['ok'])) {
    $msg = '';
    if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST' && csrf_ok()) {
        $fv = fehlversuche();
        if (count($fv) >= 5) $msg = '<div class="err">Zu viele Fehlversuche. Bitte 15 Minuten warten.</div>';
        elseif (password_verify((string) ($_POST['pw'] ?? ''), $HASH)) {
            session_regenerate_id(true); $_SESSION['ok'] = 1; @unlink(sperre_datei());
            header('Location: anfragen.php' . (isset($_GET['nr']) ? '?nr=' . rawurlencode((string) $_GET['nr']) : '')); exit;
        } else { $fv[] = time(); @file_put_contents(sperre_datei(), implode(',', $fv), LOCK_EX); $msg = '<div class="err">Passwort falsch.</div>'; }
    }
    seite('Anmelden', '<div class="k" style="max-width:420px;margin:40px auto"><h1>Anmelden</h1>' . $msg . '<form method="post"><input type="hidden" name="csrf" value="' . h(csrf()) . '"><p><input type="password" name="pw" required placeholder="Passwort" autocomplete="current-password" autofocus></p><button>Anmelden</button></form></div>');
}

$db = anf_db();
if (!$db) seite('Fehler', '<div class="err">Die Anfragen-Datenbank ist nicht verfügbar (PDO SQLite fehlt oder der Ordner data/ ist nicht beschreibbar).</div>');

// ─── Aktionen ───────────────────────────────────────────────────────────
$hinweis = '';
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST' && csrf_ok()) {
    $nr = (string) ($_POST['nr'] ?? '');
    $akt = (string) ($_POST['aktion'] ?? '');
    if ($akt === 'speichern' && $nr !== '') {
        $st = (string) ($_POST['status'] ?? 'neu'); if (!isset(ANF_STATUS[$st])) $st = 'neu';
        $db->prepare('UPDATE anfragen SET status = ?, notiz = ?, geaendert = ? WHERE nr = ?')->execute([$st, mb_substr((string) ($_POST['notiz'] ?? ''), 0, 5000), time(), $nr]);
        $neu = trim((string) ($_POST['stadt'] ?? ''));
        if ($neu !== '') {   // Stadt von Hand korrigieren – Region wird daraus neu bestimmt
            [$sname, $sreg] = anf_stadt($neu);
            if ($sreg === 'Sonstige') $sname = mb_substr($neu, 0, 60);
            $db->prepare('UPDATE anfragen SET stadt = ?, region = ? WHERE nr = ?')->execute([$sname, $sreg, $nr]);
        }
        header('Location: anfragen.php?nr=' . rawurlencode($nr) . '&ok=1'); exit;
    }
    if ($akt === 'loeschen' && $nr !== '') {
        $db->prepare('DELETE FROM anfragen WHERE nr = ?')->execute([$nr]);
        header('Location: anfragen.php?geloescht=' . rawurlencode($nr)); exit;
    }
    if ($akt === 'tg_test') {
        $ok = anf_telegram_senden((string) ($K['telegram_token'] ?? ''), (string) ($K['telegram_chat'] ?? ''), '✅ Test von masar-werbeagentur.de – Benachrichtigungen funktionieren.');
        $hinweis = $ok ? '<div class="ok">Testnachricht gesendet – bitte in Telegram prüfen.</div>' : '<div class="err">Senden fehlgeschlagen. Token und Chat-ID prüfen.</div>';
    }
}

// ─── CSV-Export ─────────────────────────────────────────────────────────
if (isset($_GET['export'])) {
    header('Content-Type: text/csv; charset=UTF-8');
    header('Content-Disposition: attachment; filename="anfragen-' . date('Y-m-d') . '.csv"');
    $o = fopen('php://output', 'w'); fwrite($o, "\xEF\xBB\xBF");
    fputcsv($o, ['Nr', 'Datum', 'Status', 'Quelle', 'Name', 'Firma', 'E-Mail', 'Telefon', 'Ort', 'Stadt', 'Region', 'Leistung', 'Notiz'], ';');
    foreach ($db->query('SELECT * FROM anfragen ORDER BY id DESC') as $r)
        fputcsv($o, [$r['nr'], date('d.m.Y H:i', (int) $r['erstellt']), ANF_STATUS[$r['status']] ?? $r['status'], $r['quelle'], $r['name'], $r['firma'], $r['email'], $r['telefon'], $r['ort'], $r['stadt'] ?? '', $r['region'] ?? '', $r['leistung'], $r['notiz']], ';');
    exit;
}

// ─── Einstellungen ──────────────────────────────────────────────────────
if (($_GET['ansicht'] ?? '') === 'einstellungen') {
    $tok = (string) ($K['telegram_token'] ?? ''); $chat = (string) ($K['telegram_chat'] ?? '');
    $chats = '';
    if ($tok !== '' && isset($_GET['chatsuche'])) {
        $r = anf_telegram_abruf($tok, 'getUpdates');
        $j = $r ? json_decode($r, true) : null; $ids = [];
        foreach (($j['result'] ?? []) as $u) { $c = $u['message']['chat'] ?? null; if ($c) $ids[(string) $c['id']] = trim(($c['first_name'] ?? '') . ' ' . ($c['last_name'] ?? '') . ' ' . ($c['title'] ?? '')); }
        $chats = $ids ? '<div class="ok">Gefundene Chats:<br>' . implode('<br>', array_map(fn($id, $n) => '<code>' . h((string) $id) . '</code> – ' . h($n), array_keys($ids), $ids)) . '<br>Diese Zeile in kontakt-config.php einfügen: <code>\'telegram_chat\' => \'' . h((string) array_key_first($ids)) . '\',</code></div>'
                      : (!$r ? '<div class="err">Keine Verbindung zu Telegram möglich (Server blockiert ausgehende Verbindung).</div>'
                      : (empty($j['ok']) ? '<div class="err">Telegram meldet: ' . h((string) ($j['description'] ?? 'Fehler')) . ' – meist ist der Token falsch oder unvollständig eingefügt.</div>'
                      : '<div class="err">Kein Chat gefunden. Schreiben Sie Ihrem Bot in Telegram zuerst „/start“ und laden Sie diese Seite dann neu.</div>'));
    }
    $anz = (int) $db->query('SELECT COUNT(*) FROM anfragen')->fetchColumn();
    seite('Einstellungen', $hinweis . '<div class="k"><h1>Einstellungen</h1>'
        . '<p>Gespeicherte Anfragen: <b>' . $anz . '</b> · automatische Löschung nach ' . ANF_MONATE . ' Monaten</p>'
        . '<h2>Telegram-Benachrichtigung</h2>'
        . '<p>Token: ' . ($tok !== '' ? '✅ hinterlegt' : '❌ fehlt') . ' · Chat-ID: ' . ($chat !== '' ? '✅ hinterlegt' : '❌ fehlt') . '</p>'
        . '<ol class="m"><li>In Telegram <b>@BotFather</b> öffnen, <code>/newbot</code> senden, Namen wählen → Token kopieren.</li>'
        . '<li>In kontakt-config.php einfügen: <code>\'telegram_token\' => \'…\',</code></li>'
        . '<li>Dem neuen Bot in Telegram „/start“ schreiben, dann hier „Chat-ID suchen“.</li>'
        . '<li>Chat-ID eintragen, speichern, „Test senden“.</li></ol>'
        . '<p class="m">Die Telegram-Nachricht enthält nur Anfragenummer, Leistung, Ort und Quelle – keine Namen, Telefonnummern oder E-Mails.</p>'
        . $chats . '<div class="row" style="max-width:520px">' . ($tok !== '' ? '<a class="btn l" href="anfragen.php?ansicht=einstellungen&chatsuche=1">Chat-ID suchen</a>' : '')
        . ($tok !== '' && $chat !== '' ? '<form method="post"><input type="hidden" name="csrf" value="' . h(csrf()) . '"><input type="hidden" name="aktion" value="tg_test"><button>Test senden</button></form>' : '') . '</div></div>');
}

// ─── Detailansicht ──────────────────────────────────────────────────────
if (isset($_GET['nr'])) {
    $st = $db->prepare('SELECT * FROM anfragen WHERE nr = ?'); $st->execute([(string) $_GET['nr']]); $r = $st->fetch();
    if (!$r) seite('Nicht gefunden', '<div class="err">Anfrage nicht gefunden.</div><a class="btn l" href="anfragen.php">← Übersicht</a>');
    $vor = trim((string) $r['name']);
    $anrede = 'Guten Tag' . ($vor !== '' ? ' ' . $vor : '') . ',';
    $sig = "\n\nViele Grüße\nAmjad Alblili\nMasar Werbeagentur";
    $vorlagen = [
        'Fotos & Maße erbitten' => "$anrede\n\nvielen Dank für Ihre Anfrage {$r['nr']}! Damit ich Ihnen schnell ein Festpreis-Angebot machen kann, schicken Sie mir bitte ein Foto vom Ort und die ungefähren Maße (Breite × Höhe). Haben Sie schon ein Logo oder Design?$sig",
        'Angebot kommt heute' => "$anrede\n\nvielen Dank für Ihre Anfrage {$r['nr']}. Ich bereite Ihr Angebot vor – Sie bekommen es heute noch per E-Mail.$sig",
        'Termin vorschlagen' => "$anrede\n\nzu Ihrer Anfrage {$r['nr']}: Gern komme ich zum Aufmaß vorbei. Wann passt es Ihnen in den nächsten Tagen?$sig",
        'Nach Angebot nachfragen' => "$anrede\n\nich wollte kurz nachfragen, ob Sie unser Angebot zu Ihrer Anfrage {$r['nr']} erhalten haben und ob noch Fragen offen sind.$sig",
        'Nach Abschluss: Bewertung' => "$anrede\n\nvielen Dank für Ihren Auftrag! Wenn Sie zufrieden sind, würden wir uns sehr über eine kurze Google-Bewertung freuen: https://masar-werbeagentur.de/google-bewertung$sig",
    ];
    $wa = wa_nummer((string) $r['telefon']);
    $btn = '';
    foreach ($vorlagen as $titel => $text) {
        $btn .= $wa !== '' ? '<a class="btn wa" target="_blank" rel="noopener" href="https://wa.me/' . h($wa) . '?text=' . h(rawurlencode($text)) . '">' . h($titel) . '</a> ' : '';
    }
    if ($r['email'] !== '') $btn .= '<a class="btn l" href="mailto:' . h($r['email']) . '?subject=' . h(rawurlencode('Ihre Anfrage ' . $r['nr'] . ' – Masar Werbeagentur')) . '&body=' . h(rawurlencode($vorlagen['Fotos & Maße erbitten'])) . '">E-Mail schreiben</a> ';
    if ($r['telefon'] !== '') $btn .= '<a class="btn l" href="tel:' . h(preg_replace('/[^\d+]/', '', (string) $r['telefon'])) . '">Anrufen</a>';
    $opt = ''; foreach (ANF_STATUS as $k => $v) $opt .= '<option value="' . $k . '"' . ($r['status'] === $k ? ' selected' : '') . '>' . $v . '</option>';
    seite($r['nr'], (isset($_GET['ok']) ? '<div class="ok">Gespeichert.</div>' : '')
        . '<p><a href="anfragen.php">← Übersicht</a></p><div class="grid"><div>'
        . '<div class="k"><h1>' . h($r['nr']) . ' <span class="tag">📍 ' . h(($r['stadt'] ?? '') . (($r['region'] ?? '') !== '' && ($r['region'] ?? '') !== ($r['stadt'] ?? '') ? ' · ' . $r['region'] : '')) . '</span> <span class="tag ' . h($r['status']) . '">' . h(ANF_STATUS[$r['status']] ?? $r['status']) . '</span></h1>'
        . '<p class="m">' . date('d.m.Y H:i', (int) $r['erstellt']) . ' · ' . h($r['quelle']) . ($r['seite'] ? ' · <a href="' . h($r['seite']) . '" target="_blank" rel="noopener">Seite</a>' : '') . '</p>'
        . '<table>' . (!empty($r['termin']) ? '<tr><th>Termin</th><td><b>📅 ' . h(anf_termin_text((int) $r['termin'])) . '</b> (' . (int) $r['termin_dauer'] . ' Min.)<br>' . h($r['termin_art'] ?? '') . ' · ' . h($r['sprache'] ?? '') . '</td></tr>' : '') . '<tr><th>Name</th><td>' . h($r['name']) . ($r['firma'] ? ' (' . h($r['firma']) . ')' : '') . '</td></tr><tr><th>Telefon</th><td>' . h($r['telefon']) . '</td></tr><tr><th>E-Mail</th><td>' . h($r['email']) . '</td></tr><tr><th>Ort</th><td>' . h($r['ort']) . '</td></tr><tr><th>Leistung</th><td>' . h($r['leistung']) . '</td></tr></table></div>'
        . '<div class="k"><h2>Antworten</h2><div class="chips" style="gap:8px">' . ($btn ?: '<span class="m">Keine Telefonnummer oder E-Mail angegeben.</span>') . '</div></div>'
        . '<div class="k"><h2>Anfrage</h2><pre>' . h($r['zusammenfassung']) . '</pre></div></div>'
        . '<div><div class="k"><h2>Bearbeiten</h2><form method="post"><input type="hidden" name="csrf" value="' . h(csrf()) . '"><input type="hidden" name="nr" value="' . h($r['nr']) . '"><input type="hidden" name="aktion" value="speichern">'
        . '<p><label class="m">Status</label><select name="status">' . $opt . '</select></p><p><label class="m">Stadt (bei Bedarf korrigieren)</label><input name="stadt" value="' . h($r['stadt'] ?? '') . '" placeholder="z. B. Köln oder 44137"></p><p><label class="m">Notiz</label><textarea name="notiz" placeholder="z. B. Preis genannt, Termin 26.10., Datei fehlt …">' . h($r['notiz']) . '</textarea></p><button>Speichern</button></form></div>'
        . '<div class="k"><h2>Löschen</h2><p class="m">Auf Wunsch des Kunden oder wenn die Anfrage erledigt ist (Datenschutz).</p><form method="post" onsubmit="return confirm(\'Anfrage endgültig löschen?\')"><input type="hidden" name="csrf" value="' . h(csrf()) . '"><input type="hidden" name="nr" value="' . h($r['nr']) . '"><input type="hidden" name="aktion" value="loeschen"><button class="btn r">Endgültig löschen</button></form></div></div></div>');
}

// ─── Übersicht ──────────────────────────────────────────────────────────
$filter = (string) ($_GET['status'] ?? 'offen');
$such = trim((string) ($_GET['q'] ?? ''));
$reg = (string) ($_GET['region'] ?? ''); if (!isset(ANF_REGIONEN[$reg])) $reg = '';
$stadt = trim((string) ($_GET['stadt'] ?? ''));
$sql = 'SELECT * FROM anfragen WHERE 1'; $par = [];
if ($filter === 'termine') $sql .= " AND termin >= " . (strtotime('today')) . " AND status <> 'verloren'";
elseif ($filter === 'offen') $sql .= " AND status IN ('neu','kontakt','angebot')";
elseif (isset(ANF_STATUS[$filter])) { $sql .= ' AND status = ?'; $par[] = $filter; }
if ($reg !== '') { $sql .= ' AND region = ?'; $par[] = $reg; }
if ($stadt !== '') { $sql .= ' AND stadt = ?'; $par[] = $stadt; }
if ($such !== '') { $sql .= ' AND (nr LIKE ? OR name LIKE ? OR firma LIKE ? OR ort LIKE ? OR leistung LIKE ? OR telefon LIKE ? OR email LIKE ?)'; $par = array_merge($par, array_fill(0, 7, '%' . $such . '%')); }
$sql .= $filter === 'termine' ? ' ORDER BY termin ASC LIMIT 300' : ' ORDER BY id DESC LIMIT 300';
$st = $db->prepare($sql); $st->execute($par); $rows = $st->fetchAll();
$zahl = []; foreach ($db->query('SELECT status, COUNT(*) c FROM anfragen GROUP BY status') as $z) $zahl[$z['status']] = (int) $z['c'];
$offen = ($zahl['neu'] ?? 0) + ($zahl['kontakt'] ?? 0) + ($zahl['angebot'] ?? 0);
$tz = (int) $db->query("SELECT COUNT(*) FROM anfragen WHERE termin >= " . strtotime('today') . " AND status <> 'verloren'")->fetchColumn();
$chips = '<a href="?status=termine" class="' . ($filter === 'termine' ? 'on' : '') . '">📅 Termine (' . $tz . ')</a>';
$chips .= '<a href="?status=offen" class="' . ($filter === 'offen' ? 'on' : '') . '">Offen (' . $offen . ')</a>';
foreach (ANF_STATUS as $k => $v) $chips .= '<a href="?status=' . $k . '" class="' . ($filter === $k ? 'on' : '') . '">' . $v . ' (' . ($zahl[$k] ?? 0) . ')</a>';
$chips .= '<a href="?status=alle" class="' . ($filter === 'alle' ? 'on' : '') . '">Alle</a>';
// Regionen und Städte (Zählung über alle Anfragen)
$url = static fn(array $p) => '?' . http_build_query(array_filter(array_merge(['status' => $filter, 'q' => $such, 'region' => $reg, 'stadt' => $stadt], $p), static fn($v) => $v !== ''));
$rz = []; foreach ($db->query('SELECT region, COUNT(*) c FROM anfragen GROUP BY region') as $z) $rz[(string) $z['region']] = (int) $z['c'];
$rchips = '<a href="' . h($url(['region' => '', 'stadt' => ''])) . '" class="' . ($reg === '' && $stadt === '' ? 'on' : '') . '">Alle Orte</a>';
foreach (ANF_REGIONEN as $k => $v) $rchips .= '<a href="' . h($url(['region' => $k, 'stadt' => ''])) . '" class="' . ($reg === $k ? 'on' : '') . '">' . h($v) . ' (' . ($rz[$k] ?? 0) . ')</a>';
$sq = 'SELECT stadt, region, COUNT(*) c FROM anfragen' . ($reg !== '' ? ' WHERE region = ?' : '') . ' GROUP BY stadt ORDER BY c DESC, stadt';
$ss = $db->prepare($sq); $ss->execute($reg !== '' ? [$reg] : []);
$opt = '<option value="">– alle Städte –</option>';
foreach ($ss->fetchAll() as $z) $opt .= '<option value="' . h($z['stadt']) . '"' . ($stadt === (string) $z['stadt'] ? ' selected' : '') . '>' . h($z['stadt']) . ' (' . (int) $z['c'] . ')</option>';
$stadtform = '<form method="get" class="row" style="margin-top:10px">'
    . '<input type="hidden" name="status" value="' . h($filter) . '"><input type="hidden" name="q" value="' . h($such) . '"><input type="hidden" name="region" value="' . h($reg) . '">'
    . '<select name="stadt" onchange="this.form.submit()">' . $opt . '</select></form>';
$tr = '';
foreach ($rows as $r) {
    $alt = time() - (int) $r['erstellt']; $warn = $r['status'] === 'neu' && $alt > 86400 ? ' ⚠️' : '';
    $tr .= '<tr class="' . h($r['status']) . '"><td><a href="?nr=' . h(rawurlencode($r['nr'])) . '"><b>' . h($r['nr']) . '</b></a><br><span class="tag">📍 ' . h($r['stadt'] ?? '') . '</span>' . (!empty($r['termin']) ? '<br><span class="tag neu">📅 ' . h(anf_termin_text((int) $r['termin'])) . '</span>' : '') . '<br><span class="m">' . date('d.m. H:i', (int) $r['erstellt']) . $warn . '</span></td>'
         . '<td>' . h($r['name']) . ($r['firma'] ? '<br><span class="m">' . h($r['firma']) . '</span>' : '') . '</td><td>' . h($r['leistung']) . '<br><span class="m">' . h($r['ort']) . '</span></td>'
         . '<td class="hide-m">' . h($r['quelle']) . '</td><td><span class="tag ' . h($r['status']) . '">' . h(ANF_STATUS[$r['status']] ?? $r['status']) . '</span></td></tr>';
}
seite('Übersicht', (isset($_GET['geloescht']) ? '<div class="ok">Anfrage ' . h((string) $_GET['geloescht']) . ' gelöscht.</div>' : '')
    . '<div class="k"><h1>Anfragen</h1><form class="row" method="get"><input type="hidden" name="status" value="' . h($filter) . '"><input name="q" value="' . h($such) . '" placeholder="Suchen: Name, Ort, Nummer, Leistung …"><button style="flex:0">Suchen</button></form><div class="chips" style="margin-top:12px">' . $chips . '</div><div class="chips" style="margin-top:10px">' . $rchips . '</div>' . $stadtform . '</div>'
    . '<div class="k">' . ($tr ? '<table><tr><th>Nr / Datum</th><th>Kunde</th><th>Leistung / Ort</th><th class="hide-m">Quelle</th><th>Status</th></tr>' . $tr . '</table>' : '<p class="m">Keine Anfragen in dieser Ansicht.</p>') . '<p class="m">⚠️ = seit über 24 Stunden unbeantwortet</p></div>');
