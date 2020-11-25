# Discord libraries
import discord
from discord.ext import commands
from discord.ext.commands import cooldown, command, BucketType

import io
import os

import random

import time
from datetime import datetime

# For downloading stuff via http request
import requests

# A module made by me specifically for MonkeBot
import simpImage as sI

class Fun_Stuff(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun commands are ready")

    # User asks question after the "monkeBall" command and the client replies with comedic answer
    @command(aliases=["eightball", "ball"])
    @cooldown(1, 5, BucketType.guild)
    async def 8ball(self, ctx, *, question):
        try:
            responses = ["It is certain",
               "It is decidedly so",
               "Without a doubt",
               "Yes definitely",
               "You may rely on it",
               "You can count on it",
               "As I see it, yes",
               "Most likely",
               "Outlook good",
               "Yes",
               "Signs point to yes",
               "Absolutely",
               "Reply hazy try again",
               "Ask again later",
               "Better not tell you now",
               "Cannot predict now",
               "Concentrate and ask again",
               "Don't count on it",
               "My reply is no",
               "My sources say no",
               "Outlook not so good",
               "Very doubtful",
               "Chances aren't good"]
            ans = random.choice(responses)
            embed = discord.Embed(title="8 Ball :8ball:", description="----------", color=0x0000ff)
            print(f"Question by {ctx.author} in {ctx.message.guild.name} ({ctx.guild.id}): {question}\nAnswer: {ans} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Prevents the message from being too long for the embed
            if(len(ctx.message.content) < 1024):
                embed.add_field(name=f"Question by {ctx.author}", value=question, inline=False)
            else:
                embed.add_field(name=f"Question by {ctx.author}", value="Question too long", inline=False)
            embed.add_field(name="Prediction", value=ans, inline=False)
            await ctx.send(embed=embed)
        except:
            await ctx.send("There was an error. Make sure you're not in a dm")

    # Rolls the dice
    @command()
    @cooldown(1, 5, BucketType.guild)
    async def dice(self, ctx, ran="6"):
    
        # Prevents answer from being too large for an embed. Defaults to 1-6
        if(ran.isdigit() and int(ran) > 1 and len(ctx.message.content) < 1010):
            num = random.randrange(1, int(ran)+1)
        else:
            num = random.randrange(1, 6)
            
        print(f"{ctx.author.name} in {ctx.message.guild.name} ({ctx.guild.id}) rolled a: {str(num)} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        embed=discord.Embed(title="Dice :game_die:", description="----------", color=0xff0000)
        embed.add_field(name="Roll", value=f"You rolled a {num}", inline=False)
        await ctx.send(embed=embed)

    # Sends an awesome fact
    # The facts that it sends can be found in ./text_files/facts.txt
    @command()
    @cooldown(1, 5, BucketType.guild)
    async def fact(self, ctx, line=None):
        print(f"{ctx.author} in {ctx.message.guild.name} ({ctx.guild.id}) requested a fact | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines = open("./text_files/monkeFacts.txt").read().splitlines()
        fact = lines[0]
        
        # Users can request a specific line in the text file
        if(line != None):
            try:
                choice = int(line)
                if(choice < len(lines)):
                    fact = lines[choice]
            except:
                pass
        else:
            fact = random.choice(lines)
        
        embed = discord.Embed(title="Fun Fact", description="----------", color=0xffff00)
        embed.add_field(name="Fact:", value=fact, inline=False)
        await ctx.send(embed=embed)

    # Sends the avatar of a requested user
    @command()
    @cooldown(1, 5, BucketType.guild)
    async def getpfp(self, ctx):
        
        if (ctx.message.mentions.__len__()>0):
            for user in ctx.message.mentions:
                print(f"{ctx.author} in {ctx.message.guild.name} ({ctx.guild.id}) requested avatar of {user} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                url = str(user.avatar_url)
        else:
            print(f"{ctx.author} in {ctx.message.guild.name} ({ctx.guild.id}) requested avatar of self | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            url = str(ctx.author.avatar_url)

        if ("getpfp" in ctx.message.content.lower()):
            url = url.replace("?size=1024", "")
            print(f"{url}")
            filename = url.split("/")[-1]
            r = requests.get(url, allow_redirects=True)
            dir = "getpfpImages/"
            open(dir+filename, 'wb').write(r.content)
            path = sI.convertImage(dir, filename)

            with open(path, 'rb') as f:
                await ctx.message.channel.send(file=discord.File(path))

            # Deletes the original file from the drive
            os.remove(dir+filename)

            # Deletes the altered file from the drive 
            os.remove(path)

def setup(client):
    client.add_cog(Fun_Stuff(client))