from discord.ext import commands
import os
import discord
import random
import json
import asyncio
from discord.ui import View, Button, TextInput, Modal
# from rpgFiles.Classes.monsterLogic import Monster
import psycopg2
from rpgFiles.Classes.monsterLogic import Monster
from rpgFiles.gameLogic import discord_encounter

class RpgPlayer(discord.User): # This is the shell that will allow us to run the game logic and store information
    pass





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
class ClassSelect(discord.ui.Select):
    def __init__(self):
        super().__init__(placeholder="Choose a class!", value = ["Warrior", "Paladin", "Mage", "Undead"])
    
    async def callback(self, interaction):
        await interaction.response.edit_message(content = f"Your chosen class is: {self.value}")


@bot.command()
async def login(context_channel): #This command creates a new session as well as gives the opportunity to make an account
    yes_button = discord.ui.Button(label = 'Yes', style = discord.ButtonStyle.green)
    async def yes_button_callback(interaction):
        embed = discord.Embed(title = "You're logged in!", description="If this is your first time logging-in use the !class command to choose your class.")
        await interaction.response.edit_message(content ="You have an account yay!", embed = embed, view = None)
        #send the embed for the next part
    yes_button.callback = yes_button_callback

    no_button = discord.ui.Button(label = 'No', style = discord.ButtonStyle.red)
    async def no_button_callback(interaction):
        
        await interaction.response.send_modal(AccountModal())
    
    no_button.callback = no_button_callback
    view = discord.ui.View()

    async def interaction_check(interaction):
        if interaction.user != context_channel.author:
            await interaction.response.send_message(content = "This is not your instance!", ephemeral=True)
            return False
        else:
            return True
    view.interaction_check=interaction_check

    view.add_item(yes_button)
    view.add_item(no_button)
    await context_channel.send(embed=discord.Embed(title="Let's begin your journey", description="Already have an account?"),  view = view)




class AccountModal(discord.ui.Modal):
    def __init__(self, *, title: str = "Create a Account") -> None:
        super().__init__(title=title)

        self.add_item(discord.ui.TextInput(label = "Username"))
        self.add_item(discord.ui.TextInput(label = "Password", min_length=8, max_length=16,placeholder="Password must be between 8 to 16 characters"))

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title = "You're logged in!", description="If this is your first time logging-in use the !class command to choose your class.")
        embed.add_field(name="Username", value  = self.children[0].value)
        embed.add_field(name="Password", value = self.children[1].value)
        embed.add_field(name= "userid", value = interaction.user.id)
        # write if statements that see if the username is already in the database and return on_error
        await interaction.response.edit_message(embed=embed, view = None)
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, title  = "Modal via Buttom")

        self.add_item(discord.ui.TextInput(label="Short Input"))
        self.add_item(discord.ui.TextInput(label="Long Input", style=discord.TextStyle.long))
        

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Modal Results")
        embed.add_field(name="Short Input", value=self.children[0].value)
        embed.add_field(name="Long Input", value=self.children[1].value)
        await interaction.response.send_message(embeds=[embed])

class MyView(discord.ui.View):
    @discord.ui.button(label = "Login")
    async def button_callback(self, interaction, button):
        await interaction.response.send_modal(MyModal())


#------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Class_Select_Embed(discord.Embed):
    def __init__(self):
        super().__init__(title='Choose your class!')
        self.add_field(name="Warrior", value = 'Warrior',inline=False)
        self.add_field(name="Paladin", value = "Paladin",inline=False)
        self.add_field(name='Mage', value="Mage", inline =False)
        self.add_field(name = "Undead", value = "Undead", inline=False)


@bot.command()
async def classes(context_channel): # This is what allows the player to choose there class when initially starting an account
    class_select = discord.ui.Select(placeholder="Choose a class!", min_values=1, max_values=1, options=[discord.SelectOption(label = "Warrior", value = "Warrior"), discord.SelectOption(label = "Paladin", value = "Paladin")])
    async def class_select_callback(interaction):
        embed = discord.Embed(title = f"You chose the {class_select.values[0]} class!", description = "You're all set! Use the !hunt command to gain experience and level up.")
        embed.set_thumbnail(url = interaction.user.avatar)
        await interaction.response.edit_message(content = f'You chose to be a {class_select.values[0]}', view = None, embed = embed)

    class_select.callback = class_select_callback
    view = discord.ui.View()
    view.add_item(class_select)
    async def interaction_check(interaction):
        if interaction.user != context_channel.author:
            await interaction.response.send_message(content = "This is not your instance!", ephemeral=True)
            return False
        else:
            return True
    view.interaction_check=interaction_check

    await context_channel.send(embed = Class_Select_Embed(), view = view)

@bot.command() # Use this to look at current player inventory
async def inventory(context_channel):
    pass

@bot.command() # Use this to look at current player stats
async def profile(context_channel):
    pass

class FightEmbed(discord.Embed):
    def __init__(self, monster):
        super().__init__(title = "YOU'RE BEING ATTACKED!", description = f"You decided to fight the {monster.name}") #make the thumbnail a photo of the monster and the inlines your skills and etc

@bot.command()
async def hunt(context_channel): #This is what will allow you to hunt monsters

    # Need to create an if to see if the player already has a monster attached to them
        # Isekaid creates a new embed without deleting the old one which will ask to see if the current view is still active (commands are initialized via text to do this)
        # I want to see if i can do this with buttons but might not be possible since their method takes advantage of view timeouts most likely

    options = discord_encounter()
    monster_select_embed=discord.Embed(title = "You come across a large clearing", description = "You come across two monsters!")
    monster_select_embed.add_field(name = options[0].name, value = 1)
    monster_select_embed.add_field(name = options[1].name, value = 2)
    option_select=discord.ui.Select(placeholder="Which do you choose?", min_values=1, max_values=1, options = [discord.SelectOption(label = options[0].name, value = 1), discord.SelectOption(label = options[1].name, value = 2)])
    async def option_select_callback(): # This will create the embed that uses the information decided by the player to fight the monster
        pass
    
    
    view = discord.ui.View()
    view.add_item(option_select)

    await context_channel.send(embed = monster_select_embed, view = view)


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
async def logout(called_channel):

    logout_embed = discord.Embed(title = 'Thank you for playing!', description="You've been logged out")
    await called_channel.send(embed = logout_embed)



bot.run(os.environ["DISCORD_TOKEN_BOT"])