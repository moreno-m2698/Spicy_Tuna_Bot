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

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
    monster_select_embed.add_field(name = options[0].name, value = options[0].name)
    monster_select_embed.add_field(name = options[1].name, value = options[1].name)
    option_select=discord.ui.Select(placeholder="Which do you choose?", min_values=1, max_values=1, options = [discord.SelectOption(label = options[0].name, value = options[0].name), discord.SelectOption(label = options[1].name, value = options[1].name)])
    async def option_select_callback(interaction): # This will create the embed that uses the information decided by the player to fight the monster
        await interaction.response.edit_message(content = "This is where the magic happens!", embed = None, view = BattleView(option_select.values[0]))

    option_select.callback = option_select_callback
    view = discord.ui.View()
    view.add_item(option_select)

    await context_channel.send(embed = monster_select_embed, view = view)



class BattleView(discord.ui.View):
    def __init__(self, enemy):
        super().__init__(timeout=180)
        self.enemy = enemy
        attack = discord.SelectOption(label = "Attack", value=1)
        skills = discord.SelectOption(label = "Specials", value = 2)
        player_inventory = discord.SelectOption(label = "Inventory", value = 3)
        run_away = discord.SelectOption(label = "Run away", value = 4)
        choices = discord.ui.Select(placeholder="What will you do?", min_values=1, max_values=1, options = [attack, skills, player_inventory, run_away] )
        async def player_choices_callback(interaction):
            if int(choices.values[0]) == 1:
                await interaction.response.edit_message(content = "You attacked!", view = None, embed = FightEmbed(interaction.user,self.enemy))
        
        choices.callback = player_choices_callback
        self.add_item(choices)

class FightEmbed(discord.Embed):
    def __init__(self, user, enemy):

        title = f"Battle between {user} and {enemy}"
        description = f"Your health: \n{enemy}'s health:\n--------------------------------"
        super().__init__(title = title,description=description)


    pass

        



@bot.command()
async def logout(called_channel):

    logout_embed = discord.Embed(title = 'Thank you for playing!', description="You've been logged out")
    await called_channel.send(embed = logout_embed)

# class RpgPlayer(discord.User): # This is the shell that will allow us to run the game logic and store information
#     def __init__(self, *, state: ConnectionState, data: Union[UserPayload, PartialUserPayload]) -> None:
#         super().__init__(state=state, data)
#     pass



bot.run(os.environ["DISCORD_TOKEN_BOT"])