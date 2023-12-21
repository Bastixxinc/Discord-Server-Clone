# Discord-Server-Clone
For english version, scroll down.

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



### English

## Description
This Discord bot enables the saving and transferring of a Discord server's structure to other servers. It provides functionalities for archiving old channels and categories, as well as deleting the archive. The bot also considers Discord rate limits to ensure that requests are processed in accordance with Discord API restrictions.

## Operation

### Commands
- `!save`: Saves the current server structure in a JSON file.
- `!list`: Lists all saved server structures.
- `!load <Number>`: Loads a saved server structure based on the numbered list shown by `!list`. Archives existing channels.
- `!clear`: Deletes the archive with all its contained channels and categories.

## Setup

1. **Bot Token**: To run the bot, you need a Discord Bot Token, which you can obtain from the Discord Developer Portal. Insert this token at the end of the script.
2. **Dependencies**: This script uses the `discord.py` library. Install the required libraries using `pip install -r requirements.txt`.
3. **Execution**: Run the script in your Python environment. The bot should then log into your Discord server.

## Code Segments

### Initialization
The bot is initialized with specific intents to access server information and message content.

### Event Handlers
- `on_ready()`: Called when the bot has successfully logged in and is ready.

### Helper Functions
- `save_guild_structure(guild_id)`: Saves the structure of the specified server.
- `load_guild_structure(guild_id, structure_file)`: Loads a saved server structure and archives existing channels, considering Discord rate limits.
- `archive_guild_channels(guild)`: Moves all channels into an archive category, taking into account Discord rate limits.
- `list_saved_guilds()`: Lists all saved server structures.

### Command Functions
- `save_command(ctx)`: Handles the `!save` command.
- `load_command(ctx, number)`: Handles the `!load` command with a number as an argument.
- `list_command(ctx)`: Handles the `!list` command.
- `clear_command(ctx)`: Handles the `!clear` command.

### Bot Execution
At the end of the script, the bot is started with the specified token.

## License
This bot is released under the GNU General Public License v2.0.

