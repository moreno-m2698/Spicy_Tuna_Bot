from discord.ext import commands
import os
import discord
import random
import json
import asyncio
from discord.ui import View, Button, TextInput, Modal
# from rpgFiles.Classes.monsterLogic import Monster
import psycopg2


myIntents = discord.Intents.default()
myIntents.message_content = True

bot = commands.Bot(command_prefix="!", intents=myIntents)

@bot.event
async def on_ready():

    print(f'We have logged in as {bot.user}')
    starting_channel = bot.get_channel(1046946242401415281)
    # Overspecified for the test discord server
    await starting_channel.send("SPICY TUNA - STATUS: ONLINE - IN TESTING")

#This creates the rpg account

@bot.command()
async def start(called_channel):
    account = True
    if account: # This checks to see if the discord profile already has an account tied to it
        test_modal = discord.ui.Modal(title = "This is a modal test", timeout = 180)
        password1 = discord.ui.TextInput(label = "TextInput test")
        test_modal.add_item(password1)

    # This one is to verify that the user typed in the correct password
        
    # Think about if we want a seperate embed object, a quickly generated one, or one stored in the view
        await called_channel.send(test_modal)

        # After creating password we can then go into the hero choice part of the program



    # implement class system 

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, title  = "Modal via Bittpm")

        self.add_item(discord.ui.TextInput(label="Short Input"))
        self.add_item(discord.ui.TextInput(label="Long Input", style=discord.TextStyle.long))
        

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Modal Results")
        embed.add_field(name="Short Input", value=self.children[0].value)
        embed.add_field(name="Long Input", value=self.children[1].value)
        await interaction.response.send_message(embeds=[embed])

class MyView(discord.ui.View):
    @discord.ui.button(label = "Send Modal")
    async def button_callback(self, interaction, button):
        await interaction.response.send_modal(MyModal())

@bot.command()
async def modal(ctx):
    await ctx.send(view=MyView())

#------------------------------------------------------------------------------------------------------------------------------------------------------------------

@bot.command()
async def testing(called_channel):
    # sending the modal on an interaction (can be slash, buttons, or select menus)
    modal = MyModal()
    await called_channel.send(modal)

def create_monster_choice_embed() -> discord.ui.View:
    
    fileInUse = 'JSON/slime.json'
    monster1 = Monster.generateMonsterJSON(fileInUse)
    monster2 = Monster.generateMonsterJSON(fileInUse)
    while monster1.name == monster2.name:
        monster2 = Monster.generateMonsterJSON(fileInUse)

    # We can try and create a folder to accompany this so we can try and make it more visual.


    choose1 = discord.ui.Button()
        #Call back will return a monster and also delete embed

    choose2 = discord.ui.Button()
        #Call back will return a monster and also delete embed

    choice_embed = discord.Embed(title = 'You come across a clearing' , description = f"") # Make it a list with A/B description on buttons

    return choice_embed


@bot.command()
async def rpg(called_channel):
    monster = None # use something to scan the monster and see if it exists
    if monster == None:
        pass
        # we will create a respite command, but the respite in nonencounters will be the same thing and the 3 button will call to it

    attackbutton = discord.ui.Button() # make this look like a attack button

    skillbutton = discord.ui.Button()
    # This button will take u to a new embed with a drop down menu for the input

    invbutton = discord.ui.Button()
    # This button will be similar to the skills button 
            # Honestly can probably get both to use the same parent object

    escapebutton = discord.ui.Button()
    # This button will delete the monster encounter and put u in the respite zone
        # Perhaps think of respites as town areas which can then lock the player into and adventuring state and a safe state where they can buy and sell equipment



@bot.command()
async def login(called_channel):
    # This function is going to mostly be a flex to make the db feel like a traditional login experience 
    #   We can legacy this later if we want since realistically we can tie the account information to the discord account instead and use that to transfer to the cloud

    # We can also maybe just have an account password so that u can itll check to see if uve done its safe
    # see if we can create a private view
    login_embed = discord.Embed(title = 'Login', description = 'Please give us your password')

    # use a modal

    password = discord.ui.TextInput()

    # Do some logic to see if the user actually got the correct password
    # Include account recovery step here
    # Change state of the account to a logged-in state
    # See if we can create an afk timer where if there is no activity in 90 mins itll auto-logout

    pass



@bot.command()
async def logout(called_channel):

    logout_embed = discord.Embed(title = 'Thank you for playing')




    pass


bot.run(os.environ["DISCORD_TOKEN_BOT"])