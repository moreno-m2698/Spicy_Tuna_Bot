import random
import copy
import json


class TicTacToeModel():
    def __init__(self,board):
        self.board = board

    def botMove(self, possible_moves):
        #Checking for win conditions
        for player in [2,1]:
            for move in possible_moves:
                boardCopy = copy.copy(self.board)
                boardCopy[move] = player
                if self.isWinner(player):
                    return move
        
        #If center is available take the center
        if 4 in possible_moves:
            return 4
        
        #Checks for available corners and populate the list
        available_corners = []
        for move in possible_moves:
            if move in [0,2,6,8]:
                available_corners.append(move)
                
        #Make move based on available corners
        if len(available_corners) > 0:
            move = random.choice(available_corners)
            return move

        #Check for available edges and populate list
        available_edges = []
        for move in possible_moves:
            if move in [1,3,5,7]:
                available_edges.append(move)
        
        #Make move based on available edges
        if len(available_edges) > 0:
            move = random.choice(available_edges)
            return move 
    
    def isWinner(self, player: int):
        tictactoe_file = open('tictactoewinner.json')
        winning_combinations_list = json.load(tictactoe_file)    
        for combo in winning_combinations_list:
            return self.board[combo[0]] == player and self.board[combo[1]] == player and self.board[combo[2]] == player  

    def availableSpace(self):
        possible_moves = []
        for i in range(len(self.board)):
            if self.board[i] == 0:
                possible_moves.append(i)
        return possible_moves