from discord.ext import commands
import os
import discord
import time
import random
import json
import asyncio
from discord.ui import Button, View
# import tictacto

# For some reason, it is good practice to use the asyncio library to create pauses in coroutines in python


myIntents = discord.Intents.default()
myIntents.message_content = True

bot = commands.Bot(command_prefix="!", intents=myIntents)

bot.sum = 0
bot.adding_status = False

@bot.event
# I've been told from stack overflow to not add anything to on_ready
async def on_ready():

    print(f'We have logged in as {bot.user}')
    starting_channel = bot.get_channel(1046946242401415281)
    # Overspecified for the test discord server
    await starting_channel.send("SPICY TUNA - STATUS: ONLINE")


@bot.command()
async def counting(called_channel, count_cap):

    if count_cap.isdigit():
        
        count_cap = int(count_cap)
        async with called_channel.typing():

            asyncio.sleep(.65)
            await called_channel.send(f"Counting to: {count_cap}?")
         
        counter = 1

        if not(count_cap == 0):

            while counter <= count_cap:
                
                async with called_channel.typing():
                    asyncio.sleep(1)
                    await called_channel.send(f'{counter}')
                    counter += 1

            else:

                await called_channel.send("Counting - status: finished")

    else:
        await called_channel.send('not valid input')

@bot.command()
async def rps(called_channel, player_hand):
    validHands = ["scissors", "paper", "rock"]

    try:
        
        bot_hand_dict = {1: 'scissors', 2: 'paper', 3: 'paper'}
        bot_hand  = bot_hand_dict[random.randint(1,3)]
        roshamboFile = open('roshambo.json')
        game_result_dict = json.load(roshamboFile)
        game_result = game_result_dict[f'{player_hand}, {bot_hand}']
        await called_channel.send(f"BOT MOVE - {bot_hand}")
        game_result_strings = {"W": "congrats", "T": "Tied", "L": "Better next time."}


        await called_channel.send(f'{game_result_strings[game_result]}')

    except:

        await called_channel.send('Please give a valid input')
        

@bot.command()
async def test(called_channel, arg):

    await called_channel.send(arg)

@bot.command()
async def hello(called_channel):

    await called_channel.send(f"Hi {called_channel.author.name}")


@bot.event
async def on_message(user_message):

    if not(user_message.author.bot):
        print(f'Message from {user_message.author}: {user_message.content}')

    await bot.process_commands(user_message)


@bot.command()
async def add(called_channel, added_number):
    if not(bot.adding_status):
        await called_channel.send("ADDING INTIALIZED\nNOTE: Be sure to type '!add done' when you're finished")
        bot.adding_status = True

    if added_number.isdigit():
        added_number = int(added_number)
        bot.sum += added_number
        await called_channel.send(f'{bot.sum}')
    
    if added_number == 'done':
        bot.sum = 0
        bot.adding_status = False
        await called_channel.send(f'Thank you for counting')
        
    else:
        await called_channel.send('this is not a proper input')

#⭕❌
class TicTacToeView(View):

    def __init__(self, context):
        super().__init__(timeout=180)
        self.context = context

        santas_lil_helper = 0
        for i in range(3):
            for j in range(3):
                self.add_item(TicTacToeButton(f'{i+j+1+santas_lil_helper}', f"button_{i+j+1+santas_lil_helper}", i, self))
                
            santas_lil_helper += 2

    async def isWinner(self):
        tictactoe_file = open('tictactoewinner.json')
        winning_combinations_list = json.load(tictactoe_file)    
        for combos in winning_combinations_list:
            if self.children[combos[0]].style == discord.ButtonStyle.green and self.children[combos[1]].style == discord.ButtonStyle.green and self.children[combos[2]].style == discord.ButtonStyle.green:
                await self.context.send('player wins')  


    def scanBoard(self):
        possible_moves = [button.custom_id for button in self.children if button.clicked == False]
        return possible_moves

    async def on_timeout(self):
        await self.context.send('Timeout')

    def availableMoves(self):
        possible_moves = []
        for button in self.children:
            if button.style == discord.ButtonStyle.grey:
                possible_moves.append(button.custom_id)
        return possible_moves

    def botMove(self, possible_moves):
        for player in [discord.ButtonStyle.green, discord.ButtonStyle.red]
            for move in possible_moves:
                boardCopy = self[:]
                

class TicTacToeButton(Button):
    def __init__(self, label, custom_id, row, board: TicTacToeView):
        super().__init__(label = label, style = discord.ButtonStyle.grey, custom_id=custom_id, row=row)
        self.board = board
        self.clicked = False

    async def callback(self, interaction):
        self.label = '❌'
        self.style = discord.ButtonStyle.green
        self.clicked = True
        self.disabled = True
        await interaction.response.edit_message(content = f'{TicTacToeView.scanBoard(self.board)}',view = self.board)
        await TicTacToeView.isWinner(self.board)

        






    

@bot.command()
async def ttt(called_channel):
    
    await called_channel.send('welcome to tic tac to')
    view = TicTacToeView(called_channel)
    await called_channel.send("tictactoe test", view = view)





@bot.command()
async def uwu(called_channel, message):
    pass


bot.run(os.environ["DISCORD_TOKEN_BOT"])




