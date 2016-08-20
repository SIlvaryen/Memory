import pygame, random
from settings import *

class Tile():
    backColor = white
    nextColor = None
    nextPattern = None

    @staticmethod
    def getExactPos(column, row):
        return int(leftMargin + column * (tileSize + gapSize)), int(topMargin + row * (tileSize + gapSize))

    def __init__(self, column, row):
        self.isOpen = False

        self.column = column
        self.row = row

        self.left, self.top = Tile.getExactPos(self.column, self.row)
        self.rect = pygame.Rect(self.left, self.top, tileSize, tileSize)

        if Tile.nextColor == None and Tile.nextPattern == None:
            self.comb = random.choice(random.choice(availableCombination))
            self.color = self.comb[0]
            self.pattern = self.comb[1]

            self.index = getIndex(self.color, self.pattern, availableCombination)
            del(availableCombination[self.index[0]][self.index[1]])

            if availableCombination[self.index[0]] == []:
                del(availableCombination[self.index[0]])

            Tile.nextColor = self.color
            Tile.nextPattern = self.pattern
        else:
            self.color = Tile.nextColor
            self.pattern = Tile.nextPattern

            Tile.nextColor = None
            Tile.nextPattern = None

    def drawPattern(self, surface, x, y):
        #'circle','square','triangle','stripedSquare','donut'
        if self.pattern == 'circle':
            pygame.draw.circle(surface, self.color, (x + round(tileSize / 2), y + round(tileSize / 2)), round(3 / 8 * tileSize))
        elif self.pattern == 'square':
            pygame.draw.rect(surface, self.color, (x + round(1 / 8 * tileSize), y + round(1 / 8 * tileSize), round(tileSize * 6 / 8), round(tileSize * 6 / 8)))
        elif self.pattern == 'triangle':
            pygame.draw.polygon(surface, self.color, ((x + round(1 / 8 * tileSize), y + round(7 / 8 * tileSize)),(x + round(1 / 2 * tileSize), y + round(1 / 8 * tileSize)), (x + round(7 / 8 * tileSize), y + round(7 / 8 * tileSize))))
        elif self.pattern == 'stripedSquare':
            for index in range(round(tileSize * 3 / 8)):
                pygame.draw.line(surface, self.color, (x + round(tileSize * 1 / 8) + index * 2, y + round(1 / 8 * tileSize)), (x + round(tileSize * 1 / 8) + index * 2, y + round(7 / 8 * tileSize)))
        elif self.pattern == 'donut':
            pygame.draw.circle(surface, self.color, (x + round(tileSize / 2), y + round(tileSize / 2)), round(3 / 8 * tileSize), round(3 / 16 * tileSize))
        else:
            pass

class Board():
    def __init__(self):
        self.board = []
        for i in range(columns):
            for j in range(rows):
                self.board.append(Tile(i,j))

        random.shuffle(self.board)
        self.board = devideIntoParts(self.board, rows)

    def drawBoard(self, surface):
        for i in range(columns):
            for j in range(rows):
                tile = self.board[i][j]
                pygame.draw.rect(surface, Tile.backColor, tile.rect)
                if tile.isOpen == False:
                    pass
                else:
                    posX, posY = Tile.getExactPos(i, j)
                    tile.drawPattern(surface, posX, posY)
