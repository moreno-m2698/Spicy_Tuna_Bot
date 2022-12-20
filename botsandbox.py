from discord.ext import commands
import os
import discord
import random
import json
import asyncio
from view.TicTacToeView import TicTacToeView
from discord.ui import View, Button
from riotapiwrapper import RiotAPIWrapper

myIntents = discord.Intents.default()
myIntents.message_content = True
bot = commands.Bot(command_prefix="!", intents=myIntents)
@bot.event
async def on_ready():

    print(f'We have logged in as {bot.user}')
    starting_channel = bot.get_channel(1046946242401415281)
    # Overspecified for the test discord server
    await starting_channel.send("SPICY TUNA - STATUS: ONLINE\nCURRENTLY IN TESTING MODE")
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

riottoken = os.environ["RIOT_API_TOKEN"]
#team id = 100[blue] 200[red]

class MatchEmbed(discord.Embed):
    def __init__(self, colour, title, description) -> None:
        super().__init__(colour = colour, title = title, description=description)  
    #Match id index (newest game will be 0 and the oldest will be max index)

class PlayerDTO():
    def __init__(self, summoner_name, game_information: RiotAPIWrapper) -> None:

        # combine these variable calls into a single list to stop parsing json multiple times
        self.summoner_name = summoner_name
        self.game_information = game_information
        self.information_list = self.game_information.getPlayerGameStats(self.game_information.getSummonerGameInformation(self.game_information.SummonertoMatchList(1,summoner_name),summoner_name))

    def __str__(self) -> str:
        strresult = ''
        for keys in self.information_list:
            strresult += f'{keys}: {self.information_list[keys]}\n'
        return strresult

class TeamDTO():
    def __init__(self, game_information: RiotAPIWrapper) -> None:
        pass
        

class GameDTO():
    def __init__(self, game_information:RiotAPIWrapper) -> None:
        self.game_information = game_information
        

class MatchDisplayView(View):

    def __init__(self) -> None:
        super().__init__()

class MatchDisplayButton(Button):
    def __init__(self) -> None:
        super().__init__()

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command()
async def lolmatch(called_channel, summoner_name):
    wrapper = RiotAPIWrapper(riottoken)
    
    embed = MatchEmbed(colour = 1, title = 'TEST',description = PlayerDTO(summoner_name, wrapper)) # Will display information for the game
    view = discord.ui.View() # will be used to switch between games
    button1 = discord.ui.Button(label = 1, row=1)
    button2 =discord.ui.Button(label = 2, row = 1)
    view.add_item(button1)
    view.add_item(button2)
   
    await called_channel.send(embed = embed, view = view)

bot.run(os.environ["DISCORD_TOKEN_BOT"])    
