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
    #Match id index (newest game will be 0 and the oldest will be max index)
# PROCESS:!!!!!!!!!!!!!
    # 1. USE DTO TO CREATE JSON / DICT FILES THAT CAN THEN BE CONVERTED INTO EMBEDS
    # 2. CREATE AND PASS LIST OF THESE JSON TO EMBED OBJECTS INTO THE VIEW TO THE INTERACT WITH BUTTONS
    # 3. CREATE BUTTON FUNCTIONALITY

class MatchDisplayView(View):
    #◀️▶️
    def __init__(self, match_id_list,wrapper, summoner_name,context) -> None:
        super().__init__(timeout= 10)
        self.wrapper = wrapper
        self.match_id_list = match_id_list
        self.summoner_name = summoner_name
        self.context = context
        self.embed_list = []
        for match_id in self.match_id_list:
            self.embed_list.append(discord.Embed.from_dict(self.wrapper.getMatchDTOFromMatchID(match_id, self.summoner_name).MatchDTOToJSON()))
        self.max_index = len(self.embed_list)
        for index in range(len(self.embed_list)):
            self.embed_list[index].set_footer(text =f"Game: {index+1} / {self.max_index}")

        self.current_embed = self.embed_list[0]
        self.current_index = self.embed_list.index(self.current_embed)
        print(self.current_index)
        
        print(self.max_index)
        self.add_item(LeftMatchDisplayButton(self))
        self.add_item(RightMatchDisplayButton(self))
    
    async def on_timeout(self):
    
        await self.context.send(content = 'Timeout', embed =None)

class RightMatchDisplayButton(Button):
    def __init__(self, match_view: MatchDisplayView):
        super().__init__(style=discord.ButtonStyle.grey, label ='▶️', row = 0)
        self.match_view = match_view
    
    
    async def callback(self, interaction):
        self.match_view.current_index += 1
        if self.match_view.current_index == self.match_view.max_index - 1:
            self.disabled = True
        if self.match_view.children[0].disabled ==True:
            self.match_view.children[0].disabled = False
        self.match_view.current_embed = self.match_view.embed_list[self.view.current_index]
        await interaction.response.edit_message(content = "press test", embed = self.match_view.current_embed, view = self.match_view)
    
class LeftMatchDisplayButton(Button):
    def __init__(self, match_view: MatchDisplayView):
        super().__init__(style=discord.ButtonStyle.grey, label ='◀️', row = 0, disabled = True)
        self.match_view = match_view

    async def callback(self, interaction):
        self.match_view.current_index -= 1
        if self.match_view.current_index == 0:
            self.disabled = True
        
        if self.match_view.children[1].disabled ==True:
            self.match_view.children[1].disabled = False
        
        
        self.match_view.current_embed = self.match_view.embed_list[self.match_view.current_index]
        await interaction.response.edit_message(content = "test", embed = self.match_view.current_embed, view = self.match_view)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command()
async def lolmatch(called_channel, summoner_name):
    wrapper = RiotAPIWrapper(riottoken)
    view = MatchDisplayView(wrapper.SummonerNametoMatchList(amount = 10, name =summoner_name), wrapper, summoner_name, called_channel)
    await called_channel.send(embed = view.current_embed, view = view)


bot.run(os.environ["DISCORD_TOKEN_BOT"])    
