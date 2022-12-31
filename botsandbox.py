from discord.ext import commands
import os
import discord
import random
import json
import asyncio
from discord.ui import View, Button
myIntents = discord.Intents.default()
myIntents.message_content = True

bot = commands.Bot(command_prefix="!", intents=myIntents)
@bot.event
# I've been told from stack overflow to not add anything to on_ready
async def on_ready():

    print(f'We have logged in as {bot.user}')
    starting_channel = bot.get_channel(1046946242401415281)
    # Overspecified for the test discord server
    await starting_channel.send("SPICY TUNA - STATUS: ONLINE")



@bot.command()
async def rpg(called_channel):



bot.run(os.environ["DISCORD_TOKEN_BOT"])