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
    def __init__(self, colour, title, description, wrapper: RiotAPIWrapper) -> None:
        super().__init__(colour = colour, title = title, description=description)
        self.wrapper = wrapper

    def getSummoner_information(self, summoner_name):
        information = self.wrapper.SummonertoMatchList(1, summoner_name)[0]
        summoner_list = information['info']['participants']
        summoner_information = [summoner for summoner in summoner_list if summoner['puuid'] == f'{self.wrapper.getSummonerInformation(summoner_name)["puuid"]}'][0]
        return summoner_information

    def getChampionName(self, summoner_information):
        champion_name = summoner_information["championName"]
        self.description = f'{summoner_information["summonerName"]}: {champion_name}'

    def getKDA(self, summoner_information):
        player_kills = summoner_information["kills"]
        player_deaths = summoner_information["deaths"]
        player_assists = summoner_information["assists"]
        kda = f'{player_kills}/{player_deaths}/{player_assists}'
        self.description = f'KDA: {kda}'

    def getGold(self, summoner_information):
        gold_earned = summoner_information["goldEarned"]
        self.description = f'Gold Earned: {gold_earned}'

    def getGamemode(self,summoner_name):
        information = self.wrapper.SummonertoMatchList(1, summoner_name)[0]
        gamemode = information['info']['gameMode']
        self.description = f'Gamemode: {gamemode}'
        
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
    
    embed = MatchEmbed(colour = 1, title = 'TEST',description = None, wrapper=wrapper) # Will display information for the game
    summoner_information =embed.getSummoner_information(summoner_name)
    embed.getGamemode(summoner_name)

    view = discord.ui.View() # will be used to switch between games
    button1 = discord.ui.Button(label = 1, row=1)
    button2 =discord.ui.Button(label = 2, row = 1)
    view.add_item(button1)
    view.add_item(button2)
   
    await called_channel.send(embed = embed, view = view)

bot.run(os.environ["DISCORD_TOKEN_BOT"])    
