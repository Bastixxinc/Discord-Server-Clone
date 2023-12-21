# Discord-Server-Clone

## Beschreibung
Dieser Discord-Bot ermöglicht es, die Struktur eines Discord-Servers zu speichern und auf andere Server zu übertragen. Er bietet Funktionen zum Archivieren alter Kanäle und Kategorien sowie das Löschen des Archivs. Der Bot berücksichtigt auch Discord-Rate-Limits, um sicherzustellen, dass Anfragen entsprechend den Discord-API-Beschränkungen verarbeitet werden.

## Bedienung

### Befehle
- `!save`: Speichert die aktuelle Serverstruktur in einer JSON-Datei.
- `!list`: Listet alle gespeicherten Serverstrukturen auf.
- `!load <Nummer>`: Lädt eine gespeicherte Serverstruktur basierend auf der nummerierten Liste, die durch `!list` angezeigt wird. Archiviert vorhandene Kanäle.
- `!clear`: Löscht das Archiv mit allen darin enthaltenen Kanälen und Kategorien.

## Einrichtung

1. **Bot Token**: Um den Bot auszuführen, benötigen Sie einen Discord Bot Token, den Sie im Discord Developer Portal erhalten können. Setzen Sie diesen Token am Ende des Skripts ein.
2. **Abhängigkeiten**: Dieses Skript verwendet die `discord.py` Bibliothek. Installieren Sie die erforderlichen Bibliotheken mit `pip install -r requirements.txt`.
3. **Ausführung**: Führen Sie das Skript in Ihrer Python-Umgebung aus. Der Bot sollte sich dann in Ihrem Discord-Server einloggen.

## Code-Segmente

### Initialisierung
Der Bot wird mit spezifischen Intents initialisiert, um auf Serverinformationen und Nachrichteninhalte zugreifen zu können.

### Ereignishandler
- `on_ready()`: Wird aufgerufen, wenn der Bot sich erfolgreich eingeloggt hat und bereit ist.

### Hilfsfunktionen
- `save_guild_structure(guild_id)`: Speichert die Struktur des angegebenen Servers.
- `load_guild_structure(guild_id, structure_file)`: Lädt eine gespeicherte Serverstruktur und archiviert vorhandene Kanäle, wobei Discord-Rate-Limits berücksichtigt werden.
- `archive_guild_channels(guild)`: Verschiebt alle Kanäle in eine Archiv-Kategorie und beachtet dabei Discord-Rate-Limits.
- `list_saved_guilds()`: Listet alle gespeicherten Serverstrukturen auf.

### Befehlsfunktionen
- `save_command(ctx)`: Behandelt den `!save` Befehl.
- `load_command(ctx, number)`: Behandelt den `!load` Befehl mit einer Nummer als Argument.
- `list_command(ctx)`: Behandelt den `!list` Befehl.
- `clear_command(ctx)`: Behandelt den `!clear` Befehl.

### Bot-Ausführung
Am Ende des Skripts wird der Bot mit dem angegebenen Token gestartet.

## Lizenz
Dieser Bot ist unter der GNU General Public License v2.0 veröffentlicht.
