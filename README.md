
# Discord Server Management Bot

## Einleitung

Dieser Bot bietet Funktionen zur Verwaltung von Discord-Serverstrukturen. Er ermöglicht Benutzern, die Struktur eines Servers - einschließlich aller Kategorien und Kanäle - zu speichern, zu archivieren und wiederherzustellen.

## Einrichtung

### Voraussetzungen
- Python 3.8 oder höher
- discord.py Bibliothek
- Ein gültiger Discord-Bot Token

### Installation
1. Repository klonen: `git clone [Repository-URL]`.
2. Benötigte Bibliotheken installieren: `pip install -r requirements.txt`.
3. Discord-Bot Token in die Variable `BOT_TOKEN` im Code einfügen.

## Bedienung

### Befehle
- `!save`: Speichert die aktuelle Serverstruktur in einer JSON-Datei.
- `!load [Nummer]`: Lädt eine gespeicherte Serverstruktur basierend auf der Liste aus `!list`.
- `!list`: Listet alle gespeicherten Serverstrukturen auf.
- `!clear`: Löscht alle archivierten Kategorien und deren Kanäle.

## Detaillierte Code-Erklärung

### Bot Initialisierung
```python
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=BOT_COMMAND_PREFIX, intents=intents, help_command=BOT_HELP_COMMAND)
```
Der Bot wird mit einem Befehlsprefix initialisiert und nutzt Discord-Intents, um auf Server- und Nachrichtenereignisse reagieren zu können.

### Event `on_ready`
```python
@bot.event
async def on_ready():
    print(MSG_LOGGED_IN.format(bot=bot))
```
Dieses Ereignis bestätigt, dass der Bot online und betriebsbereit ist.

### Funktion `save_guild_structure`
```python
async def save_guild_structure(guild_id):
    guild = bot.get_guild(guild_id)
    if not guild:
        return MSG_ERROR_SERVER_NOT_FOUND
    
    # Struktur des Servers wird in einem Dictionary gespeichert
    structure = {'name': guild.name, 'categories': []}

    # Durchläuft alle Kategorien und speichert Informationen zu Kanälen
    for category in guild.categories:
        category_info = {'name': category.name, 'position': category.position, 'channels': []}
        for channel in category.channels:
            channel_info = {'name': channel.name, 'type': str(channel.type), 'position': channel.position}
            category_info['channels'].append(channel_info)
        structure['categories'].append(category_info)

    # Speichert die Struktur in einer JSON-Datei
    with open(f'{guild.name}_structure.json', 'w', encoding='utf-8') as f:
        json.dump(structure, f, ensure_ascii=False, indent=4)
    return MSG_STRUCTURE_SAVED.format(guild=guild)
```
Diese Funktion speichert die gesamte Struktur eines Servers, inklusive Kategorien und Kanäle, in einer JSON-Datei.

### Funktion `load_guild_structure`
```python
async def load_guild_structure(guild_id, structure_file):
    guild = bot.get_guild(guild_id)
    if not guild:
        return MSG_ERROR_SERVER_NOT_FOUND

    # Archiviert bestehende Kanäle
    archive_message = await archive_guild_channels(guild)

    # Lädt die Struktur aus der angegebenen Datei
    with open(structure_file, 'r', encoding='utf-8') as f:
        structure = json.load(f)
    
    # Erstellt neue Kategorien und Kanäle basierend auf der geladenen Struktur
    category_mapping = {}
    for category_info in structure['categories']:
        new_category = await guild.create_category(category_info['name'])
        category_mapping[category_info['name']] = new_category

        for channel_info in category_info['channels']:
            if channel_info['type'] == 'text':
                await new_category.create_text_channel(channel_info['name'])
            elif channel_info['type'] == 'voice':
                await new_category.create_voice_channel(channel_info['name'])

    return MSG_STRUCTURE_LOADED.format(guild=guild, archive_message=archive_message)
```
Diese Funktion lädt die Struktur eines Servers aus einer JSON-Datei und stellt diese auf dem Discord-Server wieder her.

### Funktion `archive_guild_channels`
```python
async def archive_guild_channels(guild):
    for channel in guild.channels:
        if isinstance(channel, discord.TextChannel) or isinstance(channel, discord.VoiceChannel):
            # Bestimmt die K

ategorie für den Kanal
            if not channel.category or not (channel.category.name.startswith(ARCHIVE_PREFIX) or channel.category.name.startswith(NON_DELETABLE_PREFIX)):
                try:
                    category = await get_or_create_category(guild, ARCHIVE_PREFIX)
                    await channel.edit(category=category)
                    await asyncio.sleep(1)
                except discord.errors.HTTPException as e:
                    if e.status == 429:
                        await asyncio.sleep(e.retry_after)
                    else:
                        raise
    return MSG_ALL_CHANNELS_MOVED
```
Archiviert alle Kanäle in spezielle Archivkategorien, um Platz für die neue Struktur zu schaffen.

---

## Funktion `clear_command`

### Zweck und Funktionsweise
Die `clear_command` Funktion wird durch den `!clear` Befehl ausgelöst. Ihr Hauptzweck ist es, alle archivierten Kategorien und die darin enthaltenen Kanäle zu löschen. Dies ist nützlich, um Platz zu schaffen und alte, nicht mehr benötigte Strukturen zu entfernen.

### Code-Erklärung

```python
@bot.command(name=CMD_CLEAR)
async def clear_command(ctx):
    guild = ctx.guild
    try:
        # Durchläuft alle Kategorien des Guilds
        for category in guild.categories:
            # Überprüft, ob die Kategorie zum Archiv gehört
            if category.name.startswith(ARCHIVE_PREFIX):
                # Löscht jeden Kanal innerhalb der Kategorie
                for channel in category.channels:
                    try:
                        await channel.delete()
                        await asyncio.sleep(1)
                    except discord.errors.HTTPException as e:
                        if e.status == 429:
                            await asyncio.sleep(e.retry_after)
                        else:
                            raise
                # Löscht die Kategorie selbst
                try:
                    await category.delete()
                    await asyncio.sleep(1)
                except discord.errors.HTTPException as e:
                    if e.status == 429:
                        await asyncio.sleep(e.retry_after)
                    else:
                        raise
        # Sendet eine Bestätigungsnachricht
        await ctx.author.send(MSG_ARCHIVE_CLEARED)
    except discord.errors.HTTPException as e:
        if e.status == 429:
            await asyncio.sleep(e.retry_after)
            await ctx.author.send(MSG_RATE_LIMIT_REACHED)
        else:
            raise
```

### Funktionsdetails

- Die Funktion durchläuft alle Kategorien des Servers (`guild`).
- Für jede Kategorie, die mit dem Archivprefix (`ARCHIVE_PREFIX`) beginnt, werden alle darin enthaltenen Kanäle gelöscht.
- Die Funktion behandelt Rate-Limits von Discord durch Abfangen von `HTTPException` und Anpassen der Wartezeiten entsprechend `retry_after`.
- Nach dem Löschen der Kategorien und Kanäle wird eine Bestätigungsnachricht an den Benutzer gesendet.

---

## Lizenz

[Informationen zur Lizenz]

---
