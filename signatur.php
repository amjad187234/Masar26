<?php
/**
 * E-Mail-Signatur – Masar Werbeagentur
 *
 * Eine Quelle fuer beide Verwendungen: die automatische Antwort aus
 * kontakt.php und die Kopiervorlage unter /email-signatur.php fuer
 * Webmail, Outlook oder Gmail. Aenderungen hier wirken an beiden Stellen.
 *
 * Hinweis: Name und ladungsfaehige Anschrift gehoeren auf Geschaeftsbriefe
 * (§ 15b GewO). Die Anschrift ist auf Wunsch des Inhabers vorerst entfernt
 * und soll spaeter wieder ergaenzt werden (ebenso Instagram/Facebook).
 *
 * Nur HTML-Tabellen und Inline-Styles: Mailprogramme ignorieren
 * Stylesheets, Webfonts und WebP-Bilder.
 */

declare(strict_types=1);

function masar_signatur_html(): string
{
    $navy  = '#132e50';
    $gruen = '#177567';
    $grau  = '#5a7070';
    $link  = 'color:' . $navy . ';text-decoration:none;';

    return '<table cellpadding="0" cellspacing="0" border="0" role="presentation" '
         . 'style="border-collapse:collapse;font-family:Arial,Helvetica,sans-serif;font-size:13px;line-height:1.55;color:' . $navy . ';">'
         . '<tr>'
         . '<td style="padding:0 14px 0 0;vertical-align:top;">'
         .   '<a href="https://masar-werbeagentur.de/" style="text-decoration:none;">'
         .     '<img src="https://masar-werbeagentur.de/email-logo.png" width="72" height="72" alt="Masar Werbeagentur" style="display:block;border:0;width:72px;height:72px;">'
         .   '</a>'
         . '</td>'
         . '<td style="padding:0 0 0 14px;vertical-align:top;border-left:3px solid #58d0bd;">'
         .   '<div style="font-size:15px;font-weight:bold;color:' . $navy . ';">Amjad Alblili</div>'
         .   '<div style="font-weight:bold;color:' . $gruen . ';">Masar Werbeagentur</div>'
         .   '<div style="font-size:12px;color:' . $grau . ';">Werbetechnik · Print · Design · Social Media</div>'
         .   '<div style="padding-top:8px;">Tel. / WhatsApp: <a href="tel:+491785143918" style="' . $link . '">0178 514 3918</a></div>'
         .   '<div><a href="mailto:info@masar-werbeagentur.de" style="' . $link . '">info@masar-werbeagentur.de</a>'
         .     ' · <a href="https://masar-werbeagentur.de/" style="' . $link . '">masar-werbeagentur.de</a></div>'
         . '</td>'
         . '</tr>'
         . '</table>';
}

function masar_signatur_text(): string
{
    return "-- \n"
         . "Amjad Alblili\n"
         . "Masar Werbeagentur – Werbetechnik · Print · Design · Social Media\n"
         . "Tel. / WhatsApp: 0178 514 3918\n"
         . "info@masar-werbeagentur.de · masar-werbeagentur.de\n";
}
