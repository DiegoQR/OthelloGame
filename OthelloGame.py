import numpy as np

class Cell:
    def __init__(self, posX, posY, contains):
        self.posX = posX
        self.posY = posY
        self.contains = contains
    
    def __str__(self):
        return f"Cell ({self.posX}, {self.posY}) - {str(self.contains)}   "
    
class Board:

    def __init__(self, size):
        self.cells = []
        self.size = size
    
    def __str__(self):
        table = ""
        for row in self.cells:
            for cell in row:
                table = table + str(cell)
            table = table + "\n"
        return table
    
    def initializate_board(self):
        for j in range(self.size):
            row = []
            for i in range(self.size):
               row.append(Cell(i, j, None))
            self.cells.append(row)

    def place_token(self, posX, posY, token):
        cellToPlace = self.cells[posY][posX]
        cellToPlace.contains = token

board = Board(8)
board.initializate_board()
print(board)
board.place_token(3,0, "White")
print(board)