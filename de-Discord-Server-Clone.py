MAX_CHANNELS_PER_CATEGORY = 50
BOT_TOKEN = ''  # TOKEN # TOKEN # TOKEN # TOKEN # TOKEN # TOKEN # TOKEN # TOKEN # TOKEN # TOKEN # TOKEN # TOKEN # TOKEN # TOKEN # TOKEN
BOT_COMMAND_PREFIX = '!'
BOT_HELP_COMMAND = None
EMBED_COLOR = 0x000000
EMBED_FOOTER_TEXT = "Erstellt von @Bastiix"
ARCHIVE_PREFIX = "B-Archiv"
NON_DELETABLE_PREFIX = "Nicht Löschbar"
MSG_LOGGED_IN = 'Eingeloggt als: {bot.user}'
MSG_ERROR_SERVER_NOT_FOUND = "Fehler: Server nicht gefunden."
MSG_ALL_CHANNELS_MOVED = "Alle Kanäle wurden entsprechend verschoben."
MSG_STRUCTURE_SAVED = "Struktur des Servers '{guild.name}' wurde erfolgreich gespeichert."
MSG_ERROR_SAVING_STRUCTURE = "Fehler beim Speichern der Serverstruktur: {e}"
CMD_HELP = 'help'
CMD_SAVE = 'save'
CMD_LOAD = 'load'
CMD_LIST = 'list'
CMD_CLEAR = 'clear'
MSG_HELP_SECTION = "Hilfebereich"
MSG_HELP_DESCRIPTION = "Hier ist eine Übersicht über die verfügbaren Befehle und wie man sie benutzt."
MSG_HELP_COMMANDS = [("!save", "Speichert die aktuelle Serverstruktur."),
                     ("!load [Nummer]", "Lädt eine gespeicherte Serverstruktur basierend auf der Nummerierung bei !list."),
                     ("!list", "Listet alle gespeicherten Serverstrukturen auf."),
                     ("!clear", "Löscht das B-Archiv.")]
MSG_COMMAND_ERROR = "Du scheinst einen Befehl falsch genutzt zu haben. Hier ist etwas Hilfe:"
MSG_SAVING_STRUCTURE = "Speichere Serverstruktur..."
MSG_STRUCTURE_LOADED = "Struktur erfolgreich auf Server '{guild.name}' geladen. {archive_message}"
MSG_ERROR_FILE_NOT_FOUND = "Fehler: Datei '{structure_file}' nicht gefunden."
MSG_ERROR_INVALID_FORMAT = "Fehler: Ungültiges Format in der Strukturdatei."
MSG_UNKNOWN_ERROR_LOADING = "Unbekannter Fehler beim Laden der Struktur: {e}"
MSG_NO_SAVED_STRUCTURES = "Keine gespeicherten Serverstrukturen gefunden."
MSG_SAVED_STRUCTURES_LIST = "Gespeicherte Serverstrukturen:\n"
MSG_INVALID_NUMBER = "Ungültige Nummer. Bitte eine gültige Nummer aus der Liste verwenden."
MSG_LOADING_STRUCTURE = "Lade Struktur aus Datei '{structure_file}'..."
MSG_ARCHIVE_CLEARED = "Das B-Archiv wurde erfolgreich gelöscht."
MSG_RATE_LIMIT_REACHED = "Rate-Limit erreicht, bitte versuche es später erneut."

import discord
import json
import os
import asyncio
from discord.ext import commands

intents = discord.Intents.all()
intents.guilds = True
intents.messages = True  
intents.message_content = True 

bot = commands.Bot(command_prefix=BOT_COMMAND_PREFIX, intents=intents, help_command=BOT_HELP_COMMAND)

@bot.event
async def on_ready():
    print(MSG_LOGGED_IN.format(bot=bot))

async def get_or_create_category(guild, base_name):
    categories = [c for c in guild.categories if c.name.startswith(base_name)]
    categories.sort(key=lambda c: int(c.name.split('-')[-1]))

    if categories and len(categories[-1].channels) < MAX_CHANNELS_PER_CATEGORY:
        return categories[-1]
    else:
        new_index = len(categories) + 1
        return await guild.create_category(f"{base_name}-{new_index}")

async def archive_guild_channels(guild):
    for channel in guild.channels:
        if isinstance(channel, discord.TextChannel) or isinstance(channel, discord.VoiceChannel):
            if not channel.category or not (channel.category.name.startswith(ARCHIVE_PREFIX) or channel.category.name.startswith(NON_DELETABLE_PREFIX)):
                try:
                    if isinstance(channel, discord.TextChannel) and (channel.is_nsfw() or channel.is_news()):
                        category = await get_or_create_category(guild, NON_DELETABLE_PREFIX)
                    else:
                        category = await get_or_create_category(guild, ARCHIVE_PREFIX)
                    
                    await channel.edit(category=category)
                    await asyncio.sleep(1)
                except discord.errors.HTTPException as e:
                    if e.status == 429:
                        await asyncio.sleep(e.retry_after)
                    else:
                        raise
    return MSG_ALL_CHANNELS_MOVED

async def save_guild_structure(guild_id):
    guild = bot.get_guild(guild_id)
    if not guild:
        return MSG_ERROR_SERVER_NOT_FOUND
    
    structure = {
        'name': guild.name,
        'categories': []
    }

    try:
        for category in guild.categories:
            category_info = {
                'name': category.name,
                'position': category.position,
                'channels': []
            }

            for channel in category.channels:
                channel_info = {
                    'name': channel.name,
                    'type': str(channel.type),
                    'position': channel.position
                }
                category_info['channels'].append(channel_info)
            
            structure['categories'].append(category_info)

        with open(f'{guild.name}_structure.json', 'w', encoding='utf-8') as f:
            json.dump(structure, f, ensure_ascii=False, indent=4)

        return MSG_STRUCTURE_SAVED.format(guild=guild)
    except Exception as e:
        return MSG_ERROR_SAVING_STRUCTURE.format(e=e)
    
@bot.command(name=CMD_HELP)
async def help_command(ctx):
    embed = discord.Embed(
        title=MSG_HELP_SECTION,
        description=MSG_HELP_DESCRIPTION,
        color=EMBED_COLOR 
    )
    embed.set_footer(text=EMBED_FOOTER_TEXT)
    for command, description in MSG_HELP_COMMANDS:
        embed.add_field(name=command, value=description, inline=False)
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        embed = discord.Embed(
            title=MSG_HELP_SECTION,
            description=MSG_HELP_DESCRIPTION,
            color=EMBED_COLOR
        )
        embed.set_footer(text=EMBED_FOOTER_TEXT)
        for command, description in MSG_HELP_COMMANDS:
            embed.add_field(name=command, value=description, inline=False)
        await ctx.send(MSG_COMMAND_ERROR, embed=embed)

@bot.command(name=CMD_SAVE)
async def save_command(ctx):
    await ctx.send(MSG_SAVING_STRUCTURE)
    response = await save_guild_structure(ctx.guild.id)
    await ctx.send(response)

async def load_guild_structure(guild_id, structure_file):
    guild = bot.get_guild(guild_id)
    if not guild:
        return MSG_ERROR_SERVER_NOT_FOUND

    try:
        archive_message = await archive_guild_channels(guild)

        for category in list(guild.categories):
            if not category.name.startswith(ARCHIVE_PREFIX) and not category.name.startswith(NON_DELETABLE_PREFIX):
                for channel in category.channels:
                    await channel.delete()
                    await asyncio.sleep(1)
                await category.delete()
                await asyncio.sleep(1)

        with open(structure_file, 'r', encoding='utf-8') as f:
            structure = json.load(f)

        category_mapping = {}
        for category_info in structure['categories']:
            new_category = await guild.create_category(category_info['name'])
            category_mapping[category_info['name']] = new_category

            for channel_info in category_info['channels']:
                if channel_info['type'] == 'text':
                    await new_category.create_text_channel(channel_info['name'])
                elif channel_info['type'] == 'voice':
                    await new_category.create_voice_channel(channel_info['name'])

        for category_info in structure['categories']:
            if category_info['name'] in category_mapping:
                await category_mapping[category_info['name']].edit(position=category_info['position'])

        return MSG_STRUCTURE_LOADED.format(guild=guild, archive_message=archive_message)
    except FileNotFoundError:
        return MSG_ERROR_FILE_NOT_FOUND.format(structure_file=structure_file)
    except json.JSONDecodeError:
        return MSG_ERROR_INVALID_FORMAT
    except Exception as e:
        return MSG_UNKNOWN_ERROR_LOADING.format(e=e)

async def list_saved_guilds():
    files = [f for f in os.listdir('.') if f.endswith('_structure.json')]
    return files

@bot.command(name=CMD_LIST)
async def list_command(ctx):
    files = await list_saved_guilds()
    if not files:
        await ctx.send(MSG_NO_SAVED_STRUCTURES)
        return

    response = MSG_SAVED_STRUCTURES_LIST
    response += "\n".join(f"{i+1}. {files[i]}" for i in range(len(files)))
    await ctx.send(response)

@bot.command(name=CMD_LOAD)
async def load_command(ctx, number: int):
    files = await list_saved_guilds()
    if number <= 0 or number > len(files):
        await ctx.send(MSG_INVALID_NUMBER)
        return

    structure_file = files[number - 1]
    await ctx.send(MSG_LOADING_STRUCTURE.format(structure_file=structure_file))
    response = await load_guild_structure(ctx.guild.id, structure_file)
    await ctx.send(response)

@bot.command(name=CMD_CLEAR)
async def clear_command(ctx):
    guild = ctx.guild
    try:
        for category in guild.categories:
            if category.name.startswith(ARCHIVE_PREFIX):
                for channel in category.channels:
                    try:
                        await channel.delete()
                        await asyncio.sleep(1)
                    except discord.errors.HTTPException as e:
                        if e.status == 429:
                            await asyncio.sleep(e.retry_after)
                        else:
                            raise
                try:
                    await category.delete()
                    await asyncio.sleep(1)
                except discord.errors.HTTPException as e:
                    if e.status == 429:
                        await asyncio.sleep(e.retry_after)
                    else:
                        raise
        await ctx.author.send(MSG_ARCHIVE_CLEARED)
    except discord.errors.HTTPException as e:
        if e.status == 429:
            await asyncio.sleep(e.retry_after)
            await ctx.author.send(MSG_RATE_LIMIT_REACHED)
        else:
            raise
    return

bot.run(BOT_TOKEN)
