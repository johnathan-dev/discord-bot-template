# Discord libraries
import discord
from discord.ext import commands

import os

import math

from datetime import datetime

# HTTP requests
import requests

# Allows access to .json files
import json

# Allows access to .env files
from dotenv import load_dotenv

# Enviroment stuff
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Determines what info the bot can access
intents = discord.Intents(messages=True, guilds=True)

name = "YOUR_BOT_NAME"

# Gets a guild's custom prefix
def get_prefix(client, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

# Checks if guild is in the list of prefixes and, if it's not, adds it to the list with the default prefix
def prefix_check(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    if not str(guild.id) in prefixes:
        prefixes[str(guild.id)] = "~"

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

# Sets up the command prefix and bot description
client = commands.Bot(command_prefix = get_prefix, description = "", help_command=None, case_insensitive=True)

@client.event
async def on_ready():
    print()
    print(f"MonkeBot is ready ({client.user.id}) {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    total_guilds = 0
    avg_members = 0
    total_members = 0
    owner_list = []
    duplicate_owners = 0

    # List every guild that the bot is in, the guild's id, the region, etc.
    print("----------- Guild list -----------")
    for guild in client.guilds:
        total_guilds += 1
        owner = str(guild.owner_id)

        # Checks if the owner of the current guild is also the owner of a previous guild
        if str(owner) in owner_list:
            duplicate_owners += 1
        else:
            owner_list.append(owner)

        # Guild's specific stats
        print(f"{guild.name} ({guild.id})\nOwner ID: {owner} Members: {guild.member_count} Region: {guild.region} Features: {guild.features}", end="\n------------\n")
        total_members += int(guild.member_count)
        prefix_check(guild)

    # General guild stats
    avg_members = total_members / total_guilds
    print()
    print(f"Total guilds: {total_guilds}")
    print(f"Total members: {total_members}")
    print(f"Average members: {math.ceil(avg_members)}")
    print(f"Duplicate owners: {duplicate_owners} ")
    print(f"Total guilds sans duplicate owners: {total_guilds - duplicate_owners}")
    
    # Changes the bot's status and activity
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f"in {len(client.guilds)} servers"))
    print()
    print("----------- Commands -----------")

# Runs when bot is added to a guild
@client.event
async def on_guild_join(guild):
    print(f"{name} has joined {guild.name} ({guild.id}) Members: {guild.member_count} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f"in {len(client.guilds)} servers"))

    # Adds the guild to the prefix list with the default prefix
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = "~"

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

# Runs when bot is removed from guild
@client.event
async def on_guild_remove(guild):
    print(f"{name} has been removed from {guild.name} ({guild.id}) | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f"in {len(client.guilds)} servers"))

    # Removes the guild from the prefix list
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

# Changes prefix
@client.command()
@commands.has_role("changeprefix")
async def changeprefix(ctx, prefix):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

    print(f"{ctx.message.author.name} in {ctx.message.guild} changed the prefix to {prefix} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    await ctx.send(f"Changed prefix to {prefix}")

# Loads the different collections of commands in the cogs folder
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")
        print(f"{filename} loaded")

# Starts the bot
client.run(TOKEN)