from discord.ext import commands
import discord
from discord.ui import View, Button
from riotapiwrapper import RiotAPIWrapper, MatchDTO
from discord.ui import View, Button
class MatchDisplayView(View):
    #◀️▶️
    def __init__(self, match_id_list,wrapper, summoner_name,context) -> None:
        super().__init__()
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
        self.add_item(LeftMatchDisplayButton(self))
        self.add_item(RightMatchDisplayButton(self))
    
    async def on_timeout(self):
        await self.context.send(content = "Session Over")

class RightMatchDisplayButton(Button):
    def __init__(self, match_view: MatchDisplayView):
        super().__init__(style=discord.ButtonStyle.grey, label ='▶️', row = 0)
        self.match_view = match_view
    
    
    async def callback(self, interaction):
        self.match_view.current_index += 1
        if self.match_view.current_index == self.match_view.max_index - 1:
            self.disabled = True
        if self.match_view.children[0].disabled:
            self.match_view.children[0].disabled = False
        self.match_view.current_embed = self.match_view.embed_list[self.view.current_index]
        await interaction.response.edit_message(content = "", embed = self.match_view.current_embed, view = self.match_view)
    
class LeftMatchDisplayButton(Button):
    def __init__(self, match_view: MatchDisplayView):
        super().__init__(style=discord.ButtonStyle.grey, label ='◀️', row = 0, disabled = True)
        self.match_view = match_view

    async def callback(self, interaction):
        self.match_view.current_index -= 1
        if self.match_view.current_index == 0:
            self.disabled = True
        
        if self.match_view.children[1].disabled:
            self.match_view.children[1].disabled = False
        
        
        self.match_view.current_embed = self.match_view.embed_list[self.match_view.current_index]
        await interaction.response.edit_message(content = "", embed = self.match_view.current_embed, view = self.match_view)