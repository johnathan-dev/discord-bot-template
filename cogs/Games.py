# Discord libraries
import discord
from discord.ext import commands
from discord.ext.commands import cooldown, command, BucketType

import random
from random import randrange

from datetime import datetime

class Games(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Games commands are ready")


    # Plays rock paper scissors
    @command(aliases=["rockpaperscissors"])
    @cooldown(1, 5, BucketType.guild)
    async def rps(self, ctx, choice=None): 
        print(f"{ctx.message.author} in {ctx.message.guild.name} ({ctx.guild.id}) played rock, paper, scissors | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # A small method for detecting a win
        def playerWin(bot_choice, player_choice):
            return (bot_choice == "rock" and player_choice == "scissors") or (bot_choice == "scissors" and player_choice == "paper") or (bot_choice == "paper" and player_choice == "rock"
        
        if(choice == None):
            await ctx.send(f"rps means rock, paper, scissors. You must have a choice after the command.")
            return
        options = ["rock", "paper", "scissors", "gun"]
        player_choice = choice.lower()
        bot_choice = random.choice(options)
            
        elif(bot_choice == player_choice):
            await ctx.send(f"Bot chose {bot_choice}. It's a draw")
        elif(playerWin(bot_choice, player_choice)):
            await ctx.send(f"Bot chose {bot_choice}. {ctx.author.display_name} loses.")
        else:
            await ctx.send(f"Bot chose {bot_choice}. {ctx.author.display_name} wins.")

def setup(client):
    client.add_cog(Games(client))