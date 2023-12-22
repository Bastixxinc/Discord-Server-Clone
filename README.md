---

# Discord Server Clone Bot

## Introduction

This bot provides features for managing Discord server structures. It enables users to save, archive, and restore the structure of a server, including all categories and channels.

## Setup

### Requirements
- Python 3.8 or higher
- discord.py library
- A valid Discord Bot Token

### Installation
1. Clone the repository: `git clone [Repository-URL]`.
2. Install required libraries: `pip install -r requirements.txt`.
3. Insert the Discord Bot Token into the `BOT_TOKEN` variable in the code.

## Operation

### Commands
- `!save`: Saves the current server structure in a JSON file.
- `!load [Number]`: Loads a saved server structure based on the list from `!list`.
- `!list`: Lists all saved server structures.
- `!clear`: Deletes all archived categories and their channels.

## Detailed Code Explanation

### Bot Initialization
```python
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=BOT_COMMAND_PREFIX, intents=intents, help_command=BOT_HELP_COMMAND)
```
The bot is initialized with a command prefix and uses Discord Intents to respond to server and message events.

### Event `on_ready`
```python
@bot.event
async def on_ready():
    print(MSG_LOGGED_IN.format(bot=bot))
```
This event confirms that the bot is online and operational.

### Function `save_guild_structure`
```python
async def save_guild_structure(guild_id):
    guild = bot.get_guild(guild_id)
    if not guild:
        return MSG_ERROR_SERVER_NOT_FOUND
    
    # Saves the server structure in a dictionary
    structure = {'name': guild.name, 'categories': []}

    # Iterates through all categories and saves information about channels
    for category in guild.categories:
        category_info = {'name': category.name, 'position': category.position, 'channels': []}
        for channel in category.channels:
            channel_info = {'name': channel.name, 'type': str(channel.type), 'position': channel.position}
            category_info['channels'].append(channel_info)
        structure['categories'].append(category_info)

    # Saves the structure in a JSON file
    with open(f'{guild.name}_structure.json', 'w', encoding='utf-8') as f:
        json.dump(structure, f, ensure_ascii=False, indent=4)
    return MSG_STRUCTURE_SAVED.format(guild=guild)
```
This function saves the entire structure of a server, including categories and channels, in a JSON file.

### Function `load_guild_structure`
```python
async def load_guild_structure(guild_id, structure_file):
    guild = bot.get_guild(guild_id)
    if not guild:
        return MSG_ERROR_SERVER_NOT_FOUND

    # Archives existing channels
    archive_message = await archive_guild_channels(guild)

    # Loads the structure from the specified file
    with open(structure_file, 'r', encoding='utf-8') as f:
        structure = json.load(f)
    
    # Creates new categories and channels based on the loaded structure
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
This function loads a server's structure from a JSON file and restores it on the Discord server.

### Function `archive_guild_channels`
```python
async def archive_guild_channels(guild):
    for channel in guild.channels:
        if isinstance(channel, discord.TextChannel) or isinstance(channel, discord.VoiceChannel):
            # Determines the category for the channel
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
Archives all channels in special archive categories, making room for the new structure.

---

## Function `clear_command`

### Purpose and Functionality
The `clear_command` function is triggered by the `!clear` command. Its main purpose is to delete all archived categories and the channels contained within them. This is useful for clearing space and removing old,

 no longer needed structures.

### Code Explanation

```python
@bot.command(name=CMD_CLEAR)
async def clear_command(ctx):
    guild = ctx.guild
    try:
        # Iterates through all categories of the Guild
        for category in guild.categories:
            # Checks if the category belongs to the archive
            if category.name.startswith(ARCHIVE_PREFIX):
                # Deletes each channel within the category
                for channel in category.channels:
                    try:
                        await channel.delete()
                        await asyncio.sleep(1)
                    except discord.errors.HTTPException as e:
                        if e.status == 429:
                            await asyncio.sleep(e.retry_after)
                        else:
                            raise
                # Deletes the category itself
                try:
                    await category.delete()
                    await asyncio.sleep(1)
                except discord.errors.HTTPException as e:
                    if e.status == 429:
                        await asyncio.sleep(e.retry_after)
                    else:
                        raise
        # Sends a confirmation message
        await ctx.author.send(MSG_ARCHIVE_CLEARED)
    except discord.errors.HTTPException as e:
        if e.status == 429:
            await asyncio.sleep(e.retry_after)
            await ctx.author.send(MSG_RATE_LIMIT_REACHED)
        else:
            raise
```

### Function Details

- Iterates through all categories on the server (`guild`).
- Deletes categories and channels that belong to the archive.
- Handles Discord's rate limits by catching `HTTPException` and adjusting wait times according to `retry_after`.
- Sends a confirmation message after deleting the categories and channels.

---

## License

This project is licensed under the GNU General Public License, version 2.

---

