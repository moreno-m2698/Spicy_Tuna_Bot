from discord.ext import commands
from discord import Embed
from discord.ui import View, Button
from riotapiwrapper import RiotAPIWrapper
import os

riottoken = os.environ["RIOT_API_TOKEN"]

class MatchEmbed(Embed):
    def __init__(self) -> None:
        super().__init__()

class MatchDisplayView(View):
    def __init__(self) -> None:
        super().__init__()

class MatchDisplayButton(Button):
    def __init__(self) -> None:
        super().__init__()