import pygame, os, sys, random

black    = (   0,   0,   0)
white    = ( 255, 255, 255)
red      = ( 255,   0,   0)
lime     = (   0, 255,   0)
blue     = (   0,   0, 255)
yellow   = ( 255, 255,   0)
cyan     = (   0, 255, 255)
magenta  = ( 255,   0, 255)
silver   = ( 192, 192, 192)
gray     = ( 128, 128, 128)
darkred  = ( 128,   0,   0)
olive    = ( 128, 128,   0)
green    = (   0, 128,   0)
purple   = ( 128,   0, 128)
darkaqua = (   0, 128, 128)
navyblue = (   0,   0, 128)
orange   = ( 255, 140,   0)

screenSize = (640,480)
title = 'Platformer'

clock = pygame.time.Clock()

FPS = 60

gameFolder = os.path.dirname(__file__)
imgFolder = os.path.join(gameFolder, 'img')
sndFolder = os.path.join(gameFolder, 'snd')

#board Preferences
columns = 8
rows = 6
leftMargin = screenSize[0] / 8
tileSize = int((screenSize[0] - 2 * leftMargin) / columns * 3/4)
gapSize =  int((screenSize[0] - 2 * leftMargin) / columns * 1/4)
topMargin = (screenSize[1] - (rows * (tileSize + gapSize))) / 2
#TODO There is one gap which is not needed, try to adjust values

allColors = [yellow,green,darkred,navyblue,purple,orange]
allPatterns = ['circle','square','triangle','stripedSquare','donut']

availableCombination = []
for c in allColors:
    availableCombination.append([])
    for p in allPatterns:
        availableCombination[allColors.index(c)].append([c,p])

def waitForPlayerInput():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYUP:
                return

def terminate():
    pygame.quit()
    sys.exit()

def drawText(text, color, x, y, pos, size = 32):
    font = pygame.font.match_font('arial')
    font = pygame.font.Font(font, size)

    textobj = font.render(text, True, color)
    textRect = textobj.get_rect()

    if pos == 'topleft':
        textRext.topleft = (x,y)
    elif pos == 'topright':
        textRect.topright = (x,y)
    elif pos == 'topmid':
        textRect.centerx = x
        textRect.top = y
    elif pos == 'bottomleft':
        textRect.bottomleft = (x,y)
    elif pos == 'bottomright':
        textRext.bottomright = (x,y)
    elif pos == 'bottommid':
        textRect.centerx = x
        textRect.bottom = y
    elif pos == 'midleft':
        textRect.left = x
        textRect.centery = y
    elif pos == 'center':
        textRect.center = (x,y)
    elif pos == 'midright':
        textRect.centery = y
        textRect.right = x
    else:
        print('something went wrong! your input was ' + pos)

    surface.blit(textobj, textRect)

def devideIntoParts(List, lengthOfChunks):
    returnedList = []
    for index in range(len(List)):
        if index % lengthOfChunks == 0:
            returnedList.append([])
        returnedList[-1].append(List[index])

    return returnedList

def generateList(color):
    returnedList = []
    for index in allPatterns:
        returnedList.append([color, index])
    return returnedList

def getIndex(color, pattern, List):
    for cNum,cElem in enumerate(List):
        for pNum, pElem in enumerate(List[cNum]):
            if color == List[cNum][pNum][0] and pattern == List[cNum][pNum][1]:
                return (cNum,pNum)

#[[color,patter],[color,pattern]]
