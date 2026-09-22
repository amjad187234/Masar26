<?php
/**
 * Vorlage für die SMTP-Zugangsdaten des Kontaktformulars.
 *
 * SO WIRD SIE BENUTZT
 * 1. Im Hostinger-Dateimanager eine Kopie dieser Datei anlegen und
 *    kontakt-config.php nennen (im selben Ordner wie kontakt.php).
 * 2. Benutzername und Passwort des Postfachs eintragen.
 * 3. Speichern. Mehr ist nicht nötig – kontakt.php erkennt die Datei
 *    automatisch und verschickt ab dann über das Postfach.
 *
 * WICHTIG
 * Die fertige kontakt-config.php gehört NICHT ins Git-Repository und wird
 * dort auch bewusst ignoriert. Sie wird nur direkt auf dem Server angelegt,
 * damit das Passwort nirgendwo sonst auftaucht.
 */

return [
    // SMTP-Server des Postfachs (bei Hostinger üblicherweise smtp.hostinger.com)
    'host'   => 'smtp.hostinger.com',

    // 465 mit 'ssl' oder 587 mit 'tls'
    'port'   => 465,
    'secure' => 'ssl',

    // Vollständige E-Mail-Adresse des Postfachs und dessen Passwort
    'user'   => 'website@masar-werbeagentur.de',
    'pass'   => 'HIER-DAS-POSTFACH-PASSWORT-EINTRAGEN',

    // Absenderadresse; muss zum Postfach oben passen
    'from'   => 'website@masar-werbeagentur.de',
];
