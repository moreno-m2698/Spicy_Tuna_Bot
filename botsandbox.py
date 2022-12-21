from discord.ext import commands
import os
import discord
import random
import json
import asyncio
from view.TicTacToeView import TicTacToeView
from discord.ui import View, Button
from riotapiwrapper import RiotAPIWrapper, getBinaryFromSummonerInfo

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
    def __init__(self, summoner_name: str, champion:str, kills: int, assists: int, deaths: int, gold: int, puuid: str) -> None:
        self.summoner_name=summoner_name
        print(self.summoner_name)
        self.champion = champion
        self.kills = kills
        self.assists = assists
        self.deaths = deaths
        self.gold = gold
        self.puuid = puuid
        self.kda = round((self.kills + self.assists) / 1, 2) if self.deaths == 0 else round((self.kills + self.assists) / self.deaths, 2)
    
    def __str__(self) -> str:
        return f'{self.summoner_name}'
    
class TeamDTO():
    def __init__(self,team: list) -> None:
        self.team = team
        self.player_list = []
        for player in self.team:
            self.player_list.append(PlayerDTO(player["summonerName"],player['championName'],player["kills"],player["assists"], player["deaths"], player['goldEarned'], player["puuid"]))

    def __str__(self) -> str:
        result = ''
        for player in self.team:
            result+=f'{player}\n'
        return result

class MatchDTO(): 
    def __init__(self,data:tuple) -> None:
        self.data = data
        self.match = []
        for team in self.data:
            self.match.append(TeamDTO(team))
    
    def __str__(self) -> str:
        return f'{self.match}'

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
    result = MatchDTO(wrapper.getWantedTeamData(wrapper.getWantedGameData(wrapper.SummonerNametoMatchList(1, summoner_name))))
    description = ''
    for team in result.match:
        for player in team.player_list:
            description+=f'{player}\n'
            

    embed = MatchEmbed(colour = 1, title = 'TEST',description = description) # Will display information for the game
    view = discord.ui.View() # will be used to switch between games
    button1 = discord.ui.Button(label = 1, row=1)
    button2 =discord.ui.Button(label = 2, row = 1)
    view.add_item(button1)
    view.add_item(button2)
   
    await called_channel.send(embed = embed, view = view)

bot.run(os.environ["DISCORD_TOKEN_BOT"])    
