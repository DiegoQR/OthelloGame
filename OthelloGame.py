import sys
from termcolor import colored, cprint
from operator import index
import numpy as np
from sympy import false, primefactors, true


class Player:
    def __init__(self, tokenColor):
        self.tokenColor = tokenColor
    
    def do_a_movement(self, game, playerInput):
        movementAllowed = game.do_player_turn(self, playerInput)
        if(movementAllowed == False):
            print("Not a valid movement!")


class Game:
    def __init__(self, board):
        self.boardAnalyzer = BoardAnalyzer(board)
        self.board = board
    
    def get_player_score(self, player):
        playerScore = self.boardAnalyzer.get_quantity_tokens(player.tokenColor)
        return playerScore
    
    def copy(self):
        copyGame = Game(self.board.copy())
        return copyGame

    def initializate_default_game(self):
        self.board.place_token(3, 3, "white")
        self.board.place_token(4, 4, "white")
        self.board.place_token(4, 3, "black")
        self.board.place_token(3, 4, "black")
    
    def terminal_test(self, player):
        possibleActions = self.define_posible_actions(player)
        return len(possibleActions) == 0

    def define_posible_actions(self, player):
        possibleActions = self.boardAnalyzer.get_possible_actions(player.tokenColor)
        return possibleActions
    
    def do_player_turn(self, player, action):
        matrixOfCells = self.board.cells
        cellAction = matrixOfCells[action[1]][action[0]]
        possibleActions = self.define_posible_actions(player)
        if(cellAction not in possibleActions):
            return false
        self.board.place_token(action[0], action[1], player.tokenColor)
        self.boardAnalyzer.change_board(self.board)
        flankedFounded, cellsFlanked = self.boardAnalyzer.get_cells_flanked(player.tokenColor, cellAction)
        # Cambia las celdas con el color del rival al color del jugador
        if(flankedFounded):
            cellsWithEnemyToken = [cell for cell in cellsFlanked if (cell.contains != player.tokenColor and cell.contains != None)]
            for cell in cellsWithEnemyToken:
                cell.contains = player.tokenColor
        return true
    
    def board_status(self):
        return str(self.board)

class BoardAnalyzer:
    def __init__(self, board):
        self.board = board

    def change_board(self, board):
        self.board = board
    
    def get_quantity_tokens(self, tokenColor):
        matrixOfCells = self.board.cells
        tokenCells = []
        for list in matrixOfCells:
            for cell in list:
                if (cell.contains == tokenColor):
                    tokenCells.append(cell)
        return len(tokenCells)

    
    def check_limit_constrains(self, posX, posY):
        limitConstrainsInX = (posX >= 0) and (posX < self.board.size)
        limitConstrainsInY = (posY >= 0) and (posY < self.board.size)
        return limitConstrainsInX and limitConstrainsInY
    
    def get_cells_with_enemy_token(self, tokenColor):
        matrixOfCells = self.board.cells
        enemyTokenCells = []
        for list in matrixOfCells:
            for cell in list:
                if (cell.contains != tokenColor) and (cell.contains != None):
                    enemyTokenCells.append(cell)
        return enemyTokenCells
    
    def get_adyacent_free_cells(self, cell):
        adjacentCells = []
        matrixOfCells = self.board.cells
        iteratorX = -1
        # Funcion extraña que hize para obtener los adyacentes libres de una casilla XD
        while(iteratorX <= 1):
            iteratorY = -1
            while(iteratorY <= 1):
                adjacentPosX = cell.posX + iteratorX
                adjacentPosY = cell.posY + iteratorY
                withinLimit = self.check_limit_constrains(adjacentPosX, adjacentPosY)
                if(withinLimit and (matrixOfCells[cell.posY + iteratorY][cell.posX + iteratorX].contains == None)):
                    adjacentCells.append(matrixOfCells[cell.posY + iteratorY][cell.posX + iteratorX])
                iteratorY += 1
            iteratorX +=1
        
        return adjacentCells
    
    def get_cells_flanked(self, tokenColor, initialCell):
        cellsFlanked = []
        matrixOfCells = self.board.cells
        # Funcion extraña que hize para obtener la lista de casillas que flanquean dos fichas
        iteratorX = -1
        while(iteratorX <= 1):
            iteratorY = -1
            while(iteratorY <= 1):
                adjacentPosX = initialCell.posX + iteratorX
                adjacentPosY = initialCell.posY + iteratorY
                withinLimit = self.check_limit_constrains(adjacentPosX, adjacentPosY)
                endIteration = False
                cellsFlankedInDirection = []   
                while(withinLimit and endIteration == False):
                    if(iteratorX == 0 and iteratorY == 0):
                        endIteration = True 
                    if(matrixOfCells[adjacentPosY][adjacentPosX].contains == tokenColor):
                        cellsFlanked = cellsFlanked + cellsFlankedInDirection 
                        endIteration = True
                    cellsFlankedInDirection.append(matrixOfCells[adjacentPosY][adjacentPosX])
                    adjacentPosX += iteratorX
                    adjacentPosY += iteratorY
                    withinLimit = self.check_limit_constrains(adjacentPosX, adjacentPosY)
                iteratorY += 1
            iteratorX +=1
        
        enemyTokens = [cell for cell in cellsFlanked if(cell.contains != tokenColor and cell.contains != None)]
        cellsFlankedFounded = (len(cellsFlanked) != 0 and len(enemyTokens) > 0)
        return cellsFlankedFounded, cellsFlanked

        
    def get_possible_actions(self, tokenColor):
        possibleActionCells = []
        enemyTokensCells = self.get_cells_with_enemy_token(tokenColor)
        freeAdjacentCells = []
        for enemyTokenCell in enemyTokensCells:
            freeAdjacentCells = freeAdjacentCells + self.get_adyacent_free_cells(enemyTokenCell)
        for freeAdjacentCell in freeAdjacentCells:
            flankingFounded, cellsFlanked = self.get_cells_flanked(tokenColor, freeAdjacentCell)
            # print(f"cell: {freeAdjacentCell}, result : {flankingFounded}, cellsFlanked: {[str(cell) for cell in cellsFlanked]}")
            if(flankingFounded):
                possibleActionCells.append(freeAdjacentCell)
        return list(set(possibleActionCells))


class Cell:
    def __init__(self, posX, posY, contains):
        self.posX = posX
        self.posY = posY
        self.contains = contains
    
    def __str__(self):
        if(self.contains == None):
            return f"  ({self.posX}, {self.posY})  "
        if(self.contains == "white"):
            return colored(f"  ({self.posX}, {self.posY})  ","grey", "on_white", attrs=['bold'])
        if(self.contains == "black"):
            return colored(f"  ({self.posX}, {self.posY})  ","grey", attrs=['bold','reverse'])
        return f"Cell ({self.posX}, {self.posY}) - {str(self.contains)}   "

class Board:

    def __init__(self, size=8):
        self.cells = []
        self.size = size

    def __str__(self):
        table = ""
        for row in self.cells:
            for cell in row:
                table = table + str(cell)
            table = table + "\n"
        return table
    
    def copy(self):
        copyBoard = Board(self.size)
        copyBoard.cells = self.cells
        return copyBoard

    def initializate_board(self):
        for j in range(self.size):
            row = []
            for i in range(self.size):
               row.append(Cell(i, j, None))
            self.cells.append(row)

    def place_token(self, posX, posY, token):
        cellToPlace = self.cells[posY][posX]
        cellToPlace.contains = token