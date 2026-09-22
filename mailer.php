<?php
/**
 * Minimaler SMTP-Versand ohne externe Bibliothek.
 *
 * Wird von kontakt.php benutzt, sobald kontakt-config.php vorhanden ist.
 * Der Versand über das eigene Postfach sorgt dafür, dass SPF und DKIM
 * greifen – das ist der eigentliche Grund, warum Formularmails sonst im
 * Spam-Ordner landen.
 */

declare(strict_types=1);

/**
 * @param array<string,mixed> $cfg  host, port, user, pass, secure ('ssl'|'tls')
 * @param string $von_adresse       Briefumschlag-Absender
 * @param string $an                Empfänger
 * @param string $kopf              fertige Header-Zeilen, mit \r\n getrennt
 * @param string $rumpf             Mailinhalt
 */
function masar_smtp_senden(array $cfg, string $von_adresse, string $an, string $kopf, string $rumpf): bool
{
    $host   = (string) ($cfg['host'] ?? '');
    $port   = (int)    ($cfg['port'] ?? 465);
    $user   = (string) ($cfg['user'] ?? '');
    $pass   = (string) ($cfg['pass'] ?? '');
    $secure = (string) ($cfg['secure'] ?? 'ssl');

    if ($host === '' || $user === '' || $pass === '') {
        return false;
    }

    $ziel = ($secure === 'ssl' ? 'ssl://' : '') . $host . ':' . $port;
    $fp = @stream_socket_client($ziel, $errno, $errstr, 15);
    if (!$fp) {
        return false;
    }
    stream_set_timeout($fp, 15);

    $lesen = static function ($fp): string {
        $antwort = '';
        while (($zeile = fgets($fp, 515)) !== false) {
            $antwort .= $zeile;
            if (strlen($zeile) < 4 || $zeile[3] !== '-') {
                break;
            }
        }
        return $antwort;
    };

    $senden = static function ($fp, string $befehl) use ($lesen): string {
        fwrite($fp, $befehl . "\r\n");
        return $lesen($fp);
    };

    $code = static fn(string $antwort): int => (int) substr(trim($antwort), 0, 3);

    if ($code($lesen($fp)) !== 220) {
        fclose($fp);
        return false;
    }

    $ehlo = $senden($fp, 'EHLO masar-werbeagentur.de');
    if ($code($ehlo) !== 250) {
        fclose($fp);
        return false;
    }

    if ($secure === 'tls') {
        if ($code($senden($fp, 'STARTTLS')) !== 220
            || !stream_socket_enable_crypto($fp, true, STREAM_CRYPTO_METHOD_TLS_CLIENT)) {
            fclose($fp);
            return false;
        }
        if ($code($senden($fp, 'EHLO masar-werbeagentur.de')) !== 250) {
            fclose($fp);
            return false;
        }
    }

    if ($code($senden($fp, 'AUTH LOGIN')) !== 334
        || $code($senden($fp, base64_encode($user))) !== 334
        || $code($senden($fp, base64_encode($pass))) !== 235) {
        fclose($fp);
        return false;
    }

    if ($code($senden($fp, 'MAIL FROM:<' . $von_adresse . '>')) !== 250
        || $code($senden($fp, 'RCPT TO:<' . $an . '>')) !== 250
        || $code($senden($fp, 'DATA')) !== 354) {
        fclose($fp);
        return false;
    }

    // Punkte am Zeilenanfang verdoppeln (SMTP-Vorgabe)
    $daten = $kopf . "\r\n\r\n" . preg_replace('/^\./m', '..', $rumpf);
    fwrite($fp, $daten . "\r\n.\r\n");
    $ok = $code($lesen($fp)) === 250;

    $senden($fp, 'QUIT');
    fclose($fp);

    return $ok;
}
