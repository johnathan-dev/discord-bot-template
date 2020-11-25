# Discord libraries
import discord
from discord.ext import commands
from discord.ext.commands import cooldown, command, BucketType

from datetime import datetime

# Allows asynchronous I/O
import asyncio

# Allows access to .json files
import json

class Misc(commands.Cog):

    def __init__(self, client):
         self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Misc commands are ready")

    # Responds with the bot's latency
    @command()
    @cooldown(1, 5, BucketType.guild)
    async def ping(self, ctx):
        print(f"{ctx.author} in {ctx.message.guild.name} ({ctx.guild.id}) pinged the bot | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        await ctx.send(f"Pong: {round(self.client.latency * 1000)}ms")

    # Responds with a help embed
    @command()
    @cooldown(1, 10, BucketType.guild)
    async def help(self, ctx):

        embed = discord.Embed(title="Help", colour=discord.Colour(0xd99e1f), description="----------")

        embed.set_author(name="Bot")

        embed.add_field(name="**Fun Stuff**", value="------------", inline=False)
        embed.add_field(name="*8ball*", value="Takes in a question a returns an answer.")
        embed.add_field(name="*dice*", value="Returns a number 1-6. If no range is specified or the range is too big, it will default to 1-6.")
        embed.add_field(name="*fact*", value="Returns a cool fact.")
        embed.add_field(name="*getpfp*", value="Returns the avatar of a specified user. If no user is specified, It will return the avatar of the user who called the command.")
        embed.add_field(name="​", value="​", inline=False)
        embed.add_field(name="**Moderation**", value="------------", inline=False)
        embed.add_field(name="*clear*", value="Clears a specified amount of messages. If no amount is specified, 5 messages will be cleared.")
        embed.add_field(name="*kick*", value="Kicks a specified user.")
        embed.add_field(name="*ban*", value="Bans a specified user.")
        embed.add_field(name="​", value="​", inline=False)
        embed.add_field(name="**Games**", value="------------", inline=False)
        embed.add_field(name="*rps*", value="Plays rock paper scissors with the bot.")
        embed.add_field(name="​", value="​", inline=False)
        embed.add_field(name="**Misc**", value="------------", inline=False)
        embed.add_field(name="*help*", value="I think you can figure this one out")
        embed.add_field(name="*info*", value="Returns information about the bot, the guild, and the user that called the command.")
        embed.add_field(name="*changeprefix*", value="Changes prefix. You need the **changeprefix** role to do this.")

        await ctx.message.author.send(embed=embed)
        await ctx.send(f"Check your dms, {ctx.message.author} :wink:")

    # Responds with an info embed
    @command()
    @cooldown(1, 5, BucketType.guild)
    async def info(self, ctx):
        print(f"{ctx.author} in {ctx.message.guild.name} ({ctx.guild.id}) requested info | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        try:
            embed = discord.Embed(title="Info", colour=discord.Colour(0xffaaaa), description="Information about the bot, the guild, and the user that called the command")

            embed.set_author(name="Bot")

            embed.add_field(name="__***Bot info***__", value="------------", inline=False)
            embed.add_field(name="Name:", value=f"```{self.client.user}```")
            embed.add_field(name="ID:", value=f"```{self.client.user.id}```")
            embed.add_field(name="Servers:", value=f"```{len(self.client.guilds)}```")
            embed.add_field(name="Latency:", value=f"```{round(self.client.latency*1000)}```")

            embed.add_field(name="*Guild info*", value="------------", inline=False)
            embed.add_field(name="Name:", value=f"```{ctx.guild.name}```")
            embed.add_field(name="ID:", value=f"```{ctx.guild.id}```")
            embed.add_field(name="Member count:", value=f"```{ctx.guild.member_count}```")

            embed.add_field(name="*Member info*", value="------------", inline=False)
            embed.add_field(name="Name:", value=f"```{ctx.message.author}```")
            embed.add_field(name="ID:", value=f"```{ctx.message.author.id}```")
            embed.add_field(name="Nick:", value=f"```{ctx.message.author.nick}```")
            embed.add_field(name="Account created:", value=f"```{ctx.message.author.created_at}```")
        except:
            await ctx.send("There was an error. Make sure you're not in a dm")
            return

        await ctx.send(embed=embed)

    #------------------------------------------------ Errors Section ------------------------------------------------

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            print(f"There was an error in {ctx.message.guild} caused by {ctx.message.author} | {error}")
            if isinstance(error, commands.CommandOnCooldown):
                await ctx.send(f"This command is on a cooldown. Please wait {round(error.retry_after)} seconds")
            elif isinstance(error, commands.BadArgument):
                await ctx.send(f"Error: Improper arguments")
            elif isinstance(error, commands.MissingPermissions):
                await ctx.send(f"Error: You or the bot don't have the proper permissions to do carry out that command")
            elif isinstance(error, commands.CommandNotFound):
                pass
            elif isinstance(error, commands.DiscordException):
                await ctx.send(f"Error: There was an error")
            else:
                await ctx.send(f"There was an unknown error.")
        except:
            print(f"There was an error in {ctx.message.guild} caused by {ctx.message.author} | {error}")

def setup(client):
    client.add_cog(Misc(client)) 