import pygame as pg
import random
from settings import *
from sprites import *

class Game():
    def __init__(self):
        #initialize game
        pg.init()
        pg.mixer.init()

        self.running = True

        self.surface = pg.display.set_mode(screenSize)
        pg.display.set_caption(title)


    def new(self):
        #makes a new Game
        self.playing = True
        self.allSprites = pg.sprite.LayeredUpdates()
        self.pause = False
        self.mouseClickPos = None

        self.board = Board()

        self.mousePos = (0,0)

        self.firstFlip = None
        self.secondFlip = None
        self.flipOpenTiles = None
        self.timeFlipOpenTilesSetTrue = 0

    def run(self):
        #Runs the game permanently until self.running not is equal to True
        while self.playing:
            #Declaring the Delay
            clock.tick(FPS)
            self.events()
            self.update()
            self.render()
            if self.pause:
                self.showPauseScreen()

    def update(self):
        #Updates all Sprites
        self.allSprites.update()

        for c in range(columns):
            for r in range(rows):
                left, top = Tile.getExactPos(c,r)
                if self.board.board[c][r].rect.collidepoint(self.mousePos) and not self.board.board[c][r].isOpen:
                    self.board.board[c][r].rect.top = top - 5
                    self.board.board[c][r].rect.left = left - 5
                    self.board.board[c][r].rect.width = tileSize + 10
                    self.board.board[c][r].rect.height = tileSize + 10
                else:
                    self.board.board[c][r].rect.top = top
                    self.board.board[c][r].rect.left = left
                    self.board.board[c][r].rect.width = tileSize
                    self.board.board[c][r].rect.height = tileSize
                if self.mouseClickPos != None:
                    if self.board.board[c][r].rect.collidepoint(self.mouseClickPos) and not self.board.board[c][r].isOpen:
                        if self.firstFlip == None:
                            self.firstFlip = (c,r)
                        else:
                            self.secondFlip = (c,r)

        if self.firstFlip != None and self.secondFlip != None:
            if self.board.board[self.firstFlip[0]][self.firstFlip[1]].color == self.board.board[self.secondFlip[0]][self.secondFlip[1]].color and \
            self.board.board[self.firstFlip[0]][self.firstFlip[1]].pattern == self.board.board[self.secondFlip[0]][self.secondFlip[1]].pattern:
                self.board.board[self.firstFlip[0]][self.firstFlip[1]].isOpen = True
                self.board.board[self.secondFlip[0]][self.secondFlip[1]].isOpen = True
            else:
                self.board.board[self.secondFlip[0]][self.secondFlip[1]].isOpen = True
                self.flipOpenTiles = ((self.firstFlip[0],self.firstFlip[1]),(self.secondFlip[0],self.secondFlip[1]))
                self.timeFlipOpenTilesSetTrue = pg.time.get_ticks()

            self.firstFlip = None
            self.secondFlip = None

        elif self.firstFlip != None:
            self.flipTiles()
            self.board.board[self.firstFlip[0]][self.firstFlip[1]].isOpen = True

        if self.flipOpenTiles != None and (pg.time.get_ticks() - self.timeFlipOpenTilesSetTrue) > 1500:
            self.flipTiles()

        self.mouseClickPos = None

    def events(self):
        #Tracks all events and reacts on 'em'
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    self.pause = True

        self.mousePos = pg.mouse.get_pos()
        if pg.mouse.get_pressed()[0]:
            self.mouseClickPos = self.mousePos

    def render(self):
        #Render all sprites
        self.surface.fill(darkaqua)
        self.allSprites.draw(self.surface)
        self.board.drawBoard(self.surface)
        pg.display.update()

    def showGOScreen(self):
        #Show Game Over Screen
        pass

    def showStartScreen(self):
        #Show Start Screen
        pass

    def showPauseScreen(self):
        #Show Pause Screen
        self.playing = False
        self.running = False
        self.pause = False

    def flipTiles(self):
        if self.flipOpenTiles != None:
            self.board.board[self.flipOpenTiles[0][0]][self.flipOpenTiles[0][1]].isOpen = False
            self.board.board[self.flipOpenTiles[1][0]][self.flipOpenTiles[1][1]].isOpen = False
            self.flipOpenTiles = None

game = Game()
game.showStartScreen()
while game.running:
    game.new()
    game.run()
    game.showGOScreen()

pg.quit()
