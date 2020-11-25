# Discord libraries
import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions

from datetime import datetime


class Moderation(commands.Cog):

    def __init__(self, client):
         self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation commands are ready")

    # Clears the last n messages
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        amount += 1
        await ctx.channel.purge(limit=amount)
        print(f"{ctx.author} in {ctx.message.guild.name} ({ctx.guild.id}) just attempted to clear {str(amount)} messages | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Kicks a specified user if the user calling the command has the right permission
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
       if reason == None:
           reason = f"{ctx.message.author.name}#{ctx.message.author.discriminator}"
       await member.kick(reason=reason)
       print(f"{ctx.message.author} in {ctx.message.guild.name} ({ctx.guild.id}) kicked {member} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
       await ctx.send(f'{ctx.message.author} kicked {member}')

    # Bans a specified user if the user calling the command has the right permission
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if reason == None:
           reason = f"{ctx.message.author.name}#{ctx.message.author.discriminator}"
        await member.ban(reason=reason)
        print(f"{ctx.message.author} in {ctx.message.guild.name} ({ctx.guild.id}) banned {member} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        await ctx.send(f"{ctx.message.author} banned {member}")

def setup(client):
    client.add_cog(Moderation(client))