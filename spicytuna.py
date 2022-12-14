from discord.ext import commands
import os
import discord
import time
import random
import json
import asyncio
from discord.ui import Button, View
import copy
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

    def viewToModel(self):
        model = []
        for button in self.children:
            if button.style == discord.ButtonStyle.grey:
                model_button = 0

            elif button.style == discord.ButtonStyle.green:
                model_button = 1

            else:
                model_button = 2
            model.append(model_button)

        return model
            
    async def on_timeout(self):
        await self.context.send('Timeout')

class TicTacToeModel():
    def __init__(self,board):
        self.board = board

    def botMove(self, possible_moves):
        for player in [2,1]:
            for move in possible_moves:
                boardCopy = copy.deepcopy(self)
                boardCopy[move] = player
                if TicTacToeModel.WinnerStatic(boardCopy, player):
                    bot_move = move
                    return move
        
        if 4 in possible_moves:
            return 4
        
        available_corners = []
        for move in possible_moves:
            if move in [0,2,4,8]:
                available_corners.append(move)
        
        if len(available_corners) > 0:
            move = random.choice(available_corners)
            return move

        available_edges = []
        for move in possible_moves:
            if move in [1,3,5,7]:
                available_edges.append(move)
        
        if len(available_edges) > 0:
            move = random.choice(available_edges)
            return move 
    
    def isWinner(self, player):
        tictactoe_file = open('tictactoewinner.json')
        winning_combinations_list = json.load(tictactoe_file)    
        for combos in winning_combinations_list:
            if self[combos[0]] == player and self[combos[1]] == player and self[combos[2]] == player:
                return True

    def availableSpace(self):
        possible_moves = []
        for i in range(len(self)):
            if self[i] == 0:
                possible_moves.append(i)
        
        return possible_moves

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
        self.model = TicTacToeModel(TicTacToeView.viewToModel(self.board))
        if TicTacToeModel.isWinner(self.model, 1):
            for button in self.board.children:
                button.disabled = True
            await interaction.response.edit_message(content = "Player wins", view =self.board)
    
        else:
            bot_move = TicTacToeModel.botMove(self.model, TicTacToeModel.availableSpace(self.model))
            bot_button = [button for button in self.board.children if button.custom_id == f'button_{bot_move}'][0]
            bot_button.label = '⭕'
            bot_button.clicked = True
            bot_button.disabled = True
            bot_button.style = discord.ButtonStyle.blurple
            if TicTacToeModel.isWinner(self.model, 2):
                for button in self.board.children:
                    button.disabled = True
                await interaction.response.edit_message(content = "bot wins", view =self.board)

            else:
                await interaction.response.edit_message(content = "player turn", view = self.view)

@bot.command()
async def ttt(called_channel):
    
    await called_channel.send('welcome to tic tac to')
    view = TicTacToeView(called_channel)
    await called_channel.send("tictactoe test", view = view)

@bot.command()
async def uwu(called_channel, message):
    pass

bot.run(os.environ["DISCORD_TOKEN_BOT"])




