from discord.ext import commands
import discord
from discord.ui import View, Button
from model.TicTacToeModel import TicTacToeModel

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


    #take current buttons in view and translate that to a board model
    #do logic on the model to update its board state
    #view reads new board state and updates its button based on it
            
    async def on_timeout(self):
        await self.context.send('Timeout')


class TicTacToeButton(Button):
    def __init__(self, label, custom_id, row, ttt_view: TicTacToeView):
        super().__init__(label = label, style = discord.ButtonStyle.grey, custom_id=custom_id, row=row)
        self.ttt_view = ttt_view
        self.clicked = False

    async def callback(self, interaction):
        self.label = '❌'
        self.style = discord.ButtonStyle.green
        self.clicked = True
        self.disabled = True
        ttt_model = TicTacToeModel(self.ttt_view.viewToModel())
        #If player wins
        if ttt_model.isWinner(1):
            for button in self.ttt_view.children:
                button.disabled = True
            await interaction.response.edit_message(content = "Player wins", view = self.ttt_view)
            self.ttt_view.stop()
        else:
            #Get the bot move index
            bot_move = ttt_model.botMove(ttt_model.availableSpace())
            if bot_move == None:
                for button in self.ttt_view.children:
                    button.disabled = True
                await interaction.response.edit_message(content="tie", view = self.ttt_view)
                self.ttt_view.stop()
            #bot_button = [button for button in self.ttt_view.children if button.custom_id == f'button_{bot_move}'][0]
            else:
                bot_button = self.ttt_view.children[bot_move]
                bot_button.label = '⭕'
                bot_button.clicked = True
                bot_button.disabled = True
                bot_button.style = discord.ButtonStyle.blurple
                ttt_model = TicTacToeModel(self.ttt_view.viewToModel())
                if ttt_model.isWinner(2):
                    for button in self.ttt_view.children:
                        button.disabled = True
                    await interaction.response.edit_message(content = "bot wins", view=self.ttt_view)
                    self.ttt_view.stop()
                else:
                    await interaction.response.edit_message(content = "player turn", view = self.ttt_view)
                    