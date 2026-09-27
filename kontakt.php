<?php
/**
 * Kontaktformular-Handler – Masar Werbeagentur
 *
 * Nimmt die Formulare der Website entgegen und schickt sie an das eigene
 * Postfach. Es ist kein externer Dienst beteiligt: Die Daten verlassen die
 * Hostinger-Umgebung nicht, deshalb ist auch kein Auftragsverarbeitungs-
 * vertrag mit einem Formularanbieter nötig.
 *
 * Schutz gegen Spam: Honeypot-Feld, Mindestzeit zwischen Seitenaufruf und
 * Absenden, einfache Begrenzung pro IP-Adresse. Kein Captcha.
 */

declare(strict_types=1);

// ─────────────────────────── Konfiguration ───────────────────────────

const EMPFAENGER      = 'info@masar-werbeagentur.de';
const ABSENDER        = 'website@masar-werbeagentur.de';   // muss als Postfach existieren
const KONFIG_DATEI    = __DIR__ . '/kontakt-config.php';
const DANKE_SEITE     = '/danke.html';
const FEHLER_SEITE    = '/kontakt-fehler.html';
const MAX_UPLOAD_MB   = 10;
const MAX_PRO_STUNDE  = 6;      // Anfragen je IP-Adresse
const MIN_SEKUNDEN    = 3;      // schneller ausgefüllt = mit hoher Wahrscheinlichkeit ein Bot

const ERLAUBTE_ENDUNGEN = [
    'jpg', 'jpeg', 'png', 'webp', 'heic', 'gif',
    'pdf', 'svg', 'ai', 'eps', 'zip',
];

// Diese Felder werden nicht als Inhalt ausgegeben
const INTERNE_FELDER = ['_subject', '_honey', '_t', 'consent'];

// Hübsche Beschriftungen für die Mail
const BESCHRIFTUNG = [
    'firma'      => 'Firma',
    'dienst'     => 'Pflegedienst',
    'praxis'     => 'Praxis',
    'name'       => 'Ansprechpartner',
    'email'      => 'E-Mail',
    'telefon'    => 'Telefon / WhatsApp',
    'ort'        => 'Ort / Standort',
    'branche'    => 'Branche',
    'thema'      => 'Thema',
    'produkt'    => 'Produkt',
    'wann'       => 'Zeitrahmen',
    'groesse'    => 'Größe',
    'nachricht'  => 'Nachricht',
    'betreff'    => 'Betreff',
    'bereich'    => 'Bereich',
    'art'        => 'Art',
    'leistung'   => 'Leistung',
    'anzahl'     => 'Anzahl Bildschirme',
    'anzahl_fahrzeuge' => 'Anzahl Fahrzeuge',
    'folie'      => 'Folien-Art',
    'design'     => 'Design-Leistung',
    'schild'     => 'Schild-Art',
    'beschreibung' => 'Beschreibung',
    'bestehende_seite' => 'Bestehende Website',
    'anlass'     => 'Häufigster Anlass',
    'pvs'        => 'Praxisverwaltungssystem',
    'daten'      => 'Personenbezogene Daten betroffen',
];

// ─────────────────────────── Hilfsfunktionen ───────────────────────────

function weiter(string $ziel)
{
    header('Location: ' . $ziel, true, 303);
    exit;
}

/** Entfernt Zeilenumbrüche – schützt vor Header-Injection. */
function einzeilig(string $wert): string
{
    return trim(str_replace(["\r", "\n", "\0"], ' ', $wert));
}

function feldwert(string $name): string
{
    return isset($_POST[$name]) && is_string($_POST[$name]) ? trim($_POST[$name]) : '';
}

/** Einfache Mengenbegrenzung je IP-Adresse, ohne Datenbank. */
function zu_viele_anfragen(): bool
{
    $ip = $_SERVER['REMOTE_ADDR'] ?? 'unbekannt';
    $datei = sys_get_temp_dir() . '/masar_form_' . md5($ip) . '.txt';

    $jetzt = time();
    $zeiten = [];
    if (is_readable($datei)) {
        $inhalt = (string) file_get_contents($datei);
        foreach (explode(',', $inhalt) as $t) {
            $t = (int) $t;
            if ($t > $jetzt - 3600) {
                $zeiten[] = $t;
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

// ─────────────────────────── Ablauf ───────────────────────────

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    weiter('/');
}

// 1. Honeypot: von Menschen nie ausgefüllt
if (feldwert('_honey') !== '') {
    weiter(DANKE_SEITE);   // Bots bekommen die Erfolgsseite, merken nichts
}

// 2. Mindestzeit (nur prüfen, wenn das Feld per JavaScript gesetzt wurde)
$start = feldwert('_t');
if ($start !== '' && ctype_digit($start)) {
    // Millisekunden auf beiden Seiten: mit time() (volle Sekunden) ergab ein
    // sofortiges Absenden einen negativen Wert und wurde nie erkannt.
    $sekunden = (microtime(true) * 1000 - (int) $start) / 1000;
    if ($sekunden >= 0 && $sekunden < MIN_SEKUNDEN) {
        weiter(DANKE_SEITE);
    }
}

// 3. Mengenbegrenzung
if (zu_viele_anfragen()) {
    weiter(FEHLER_SEITE);
}

// 4. Pflichtangaben
$email = einzeilig(feldwert('email'));
$name  = einzeilig(feldwert('name'));

if ($email === '' || !filter_var($email, FILTER_VALIDATE_EMAIL) || $name === '') {
    weiter(FEHLER_SEITE);
}
if (feldwert('consent') === '') {
    weiter(FEHLER_SEITE);
}

// 5. Betreff
$betreff = einzeilig(feldwert('_subject'));
if ($betreff === '') {
    $betreff = 'Anfrage über die Website';
}
$betreff = mb_substr($betreff, 0, 120);

// 6. Inhalt zusammenstellen
$zeilen = [];
foreach ($_POST as $schluessel => $wert) {
    if (!is_string($schluessel) || in_array($schluessel, INTERNE_FELDER, true)) {
        continue;
    }
    if (!is_string($wert) || trim($wert) === '') {
        continue;
    }
    $titel = BESCHRIFTUNG[$schluessel] ?? ucfirst($schluessel);
    $inhalt = trim(str_replace("\r\n", "\n", $wert));
    $zeilen[] = $titel . ': ' . $inhalt;
}

$herkunft = einzeilig((string) ($_SERVER['HTTP_REFERER'] ?? ''));
$zeilen[] = '';
$zeilen[] = '---';
$zeilen[] = 'Gesendet über: ' . ($herkunft !== '' ? $herkunft : 'masar-werbeagentur.de');
$zeilen[] = 'Zeitpunkt: ' . date('d.m.Y H:i') . ' Uhr';
$zeilen[] = 'Einwilligung Datenschutz: erteilt (Art. 6 Abs. 1 lit. b DSGVO)';

$text = implode("\n", $zeilen) . "\n";

// 7. Datei-Anhang prüfen
$anhang = null;
if (isset($_FILES['attachment']) && is_array($_FILES['attachment'])
    && (int) $_FILES['attachment']['error'] === UPLOAD_ERR_OK) {

    $tmp    = (string) $_FILES['attachment']['tmp_name'];
    $roh    = (string) $_FILES['attachment']['name'];
    $groesse = (int) $_FILES['attachment']['size'];
    $endung = strtolower(pathinfo($roh, PATHINFO_EXTENSION));

    if (is_uploaded_file($tmp)
        && $groesse > 0
        && $groesse <= MAX_UPLOAD_MB * 1024 * 1024
        && in_array($endung, ERLAUBTE_ENDUNGEN, true)) {

        // Dateiname säubern, damit nichts Unerwartetes in die Mail wandert
        $basis = preg_replace('/[^A-Za-z0-9._-]/', '_', pathinfo($roh, PATHINFO_FILENAME)) ?? 'datei';
        $basis = mb_substr(trim($basis, '._-'), 0, 60);
        if ($basis === '') {
            $basis = 'datei';
        }

        $anhang = [
            'name'    => $basis . '.' . $endung,
            'daten'   => (string) file_get_contents($tmp),
            'typ'     => 'application/octet-stream',
        ];
        $text .= "\nAnhang: " . $anhang['name'] . ' ('
               . round($groesse / 1024) . " KB)\n";
    } else {
        $text .= "\nHinweis: Es wurde eine Datei angehängt, die nicht übernommen werden konnte "
               . "(Typ oder Größe). Bitte beim Kunden nachfragen.\n";
    }
}

// 8. Mail bauen und senden
$absender_name = '=?UTF-8?B?' . base64_encode('Masar Website') . '?=';
$nachricht_id = '<' . bin2hex(random_bytes(12)) . '@masar-werbeagentur.de>';
$kopf = [
    'From: ' . $absender_name . ' <' . ABSENDER . '>',
    'Reply-To: ' . einzeilig($name) . ' <' . $email . '>',
    'Date: ' . date('r'),
    'Message-ID: ' . $nachricht_id,
    'X-Mailer: Masar Kontaktformular',
    'Auto-Submitted: auto-generated',
    'MIME-Version: 1.0',
];

if ($anhang === null) {
    $kopf[] = 'Content-Type: text/plain; charset=UTF-8';
    $kopf[] = 'Content-Transfer-Encoding: 8bit';
    $rumpf = $text;
} else {
    $grenze = 'masar_' . bin2hex(random_bytes(12));
    $kopf[] = 'Content-Type: multipart/mixed; boundary="' . $grenze . '"';

    $rumpf  = "--{$grenze}\r\n";
    $rumpf .= "Content-Type: text/plain; charset=UTF-8\r\n";
    $rumpf .= "Content-Transfer-Encoding: 8bit\r\n\r\n";
    $rumpf .= $text . "\r\n";
    $rumpf .= "--{$grenze}\r\n";
    $rumpf .= 'Content-Type: ' . $anhang['typ'] . '; name="' . $anhang['name'] . "\"\r\n";
    $rumpf .= "Content-Transfer-Encoding: base64\r\n";
    $rumpf .= 'Content-Disposition: attachment; filename="' . $anhang['name'] . "\"\r\n\r\n";
    $rumpf .= chunk_split(base64_encode($anhang['daten'])) . "\r\n";
    $rumpf .= "--{$grenze}--\r\n";
}

$betreff_kodiert = '=?UTF-8?B?' . base64_encode($betreff) . '?=';

$erfolg = false;

// Bevorzugt über das eigene Postfach versenden: nur so greifen SPF und DKIM,
// und die Mail landet zuverlässig im Posteingang statt im Spam-Ordner.
if (is_readable(KONFIG_DATEI)) {
    $konfig = require KONFIG_DATEI;
    if (is_array($konfig)) {
        require_once __DIR__ . '/mailer.php';
        $smtp_kopf = array_merge(
            ['To: ' . EMPFAENGER, 'Subject: ' . $betreff_kodiert],
            $kopf
        );
        $erfolg = masar_smtp_senden(
            $konfig,
            (string) ($konfig['from'] ?? ABSENDER),
            EMPFAENGER,
            implode("\r\n", $smtp_kopf),
            $rumpf
        );
    }
}

if (!$erfolg) {
    $erfolg = @mail(
        EMPFAENGER,
        $betreff_kodiert,
        $rumpf,
        implode("\r\n", $kopf),
        '-f' . ABSENDER
    );
}

// 9. Eingangsbestaetigung an den Absender
// Fester Text ohne Angaben aus dem Formular: Wer eine fremde Adresse
// eintraegt, kann so keine eigenen Inhalte an Dritte verschicken. Scheitert
// der Versand, bleibt die Anfrage trotzdem erfolgreich.
if ($erfolg) {
    require_once __DIR__ . '/signatur.php';

    $a_text = "Guten Tag,\n\n"
            . "vielen Dank für Ihre Anfrage – sie ist bei uns angekommen. Wir melden uns "
            . "innerhalb von 24 Stunden bei Ihnen, an Werktagen meist schneller.\n\n"
            . "Wenn es eilt, erreichen Sie uns telefonisch oder per WhatsApp unter 0178 514 3918.\n\n"
            . "Mit freundlichen Grüßen\n\n"
            . masar_signatur_text()
            . "\nDiese E-Mail wurde automatisch versendet. Sie können direkt darauf antworten.\n";

    $a_html = '<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8"></head>'
            . '<body style="margin:0;padding:24px;background:#ffffff;">'
            . '<div style="max-width:560px;font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:1.6;color:#1a2a2a;">'
            . '<p style="margin:0 0 14px;">Guten Tag,</p>'
            . '<p style="margin:0 0 14px;">vielen Dank für Ihre Anfrage – sie ist bei uns angekommen. '
            . 'Wir melden uns innerhalb von 24 Stunden bei Ihnen, an Werktagen meist schneller.</p>'
            . '<p style="margin:0 0 14px;">Wenn es eilt, erreichen Sie uns telefonisch oder per WhatsApp unter '
            . '<a href="tel:+491785143918" style="color:#132e50;font-weight:bold;text-decoration:none;">0178 514 3918</a>.</p>'
            . '<p style="margin:0 0 18px;">Mit freundlichen Grüßen</p>'
            . masar_signatur_html()
            . '<p style="margin:22px 0 0;font-size:11px;color:#5a7070;">Diese E-Mail wurde automatisch versendet. '
            . 'Sie können direkt darauf antworten.</p>'
            . '</div></body></html>';

    $a_grenze  = 'masar_alt_' . bin2hex(random_bytes(12));
    $a_betreff = '=?UTF-8?B?' . base64_encode('Ihre Anfrage bei Masar Werbeagentur') . '?=';
    $a_kopf = [
        'From: =?UTF-8?B?' . base64_encode('Masar Werbeagentur') . '?= <' . ABSENDER . '>',
        'Reply-To: ' . EMPFAENGER,
        'Date: ' . date('r'),
        'Message-ID: <' . bin2hex(random_bytes(12)) . '@masar-werbeagentur.de>',
        'Auto-Submitted: auto-replied',
        'X-Auto-Response-Suppress: All',
        'MIME-Version: 1.0',
        'Content-Type: multipart/alternative; boundary="' . $a_grenze . '"',
    ];
    $a_rumpf = "--{$a_grenze}\r\n"
             . "Content-Type: text/plain; charset=UTF-8\r\n"
             . "Content-Transfer-Encoding: base64\r\n\r\n"
             . chunk_split(base64_encode($a_text)) . "\r\n"
             . "--{$a_grenze}\r\n"
             . "Content-Type: text/html; charset=UTF-8\r\n"
             . "Content-Transfer-Encoding: base64\r\n\r\n"
             . chunk_split(base64_encode($a_html)) . "\r\n"
             . "--{$a_grenze}--\r\n";

    $a_ok = false;
    if (isset($konfig) && is_array($konfig)) {
        $a_ok = masar_smtp_senden(
            $konfig,
            (string) ($konfig['from'] ?? ABSENDER),
            $email,
            implode("\r\n", array_merge(['To: ' . $email, 'Subject: ' . $a_betreff], $a_kopf)),
            $a_rumpf
        );
    }
    if (!$a_ok) {
        @mail($email, $a_betreff, $a_rumpf, implode("\r\n", $a_kopf), '-f' . ABSENDER);
    }
}

weiter($erfolg ? DANKE_SEITE : FEHLER_SEITE);
