from cmu_graphics import *
from PIL import Image
import os, pathlib, time


def onAppStart(app):
    createMenu(app)
    createLevel(app)
    createFrame(app)

    app.playState = False
    app.spriteCounter = 0

def createMenu(app):

    #get files for main menu
    app.menuBackground = openImage("assets/menuBackground.png")
    app.startButton = openImage("assets/startButton.png")
    #get sizes before casting as cmu image
    app.startButtonWidth, app.startButtonHeight = app.startButton.width, app.startButton.height
    #make cmu image for faster drawing
    app.menuBackground = CMUImage(app.menuBackground)
    app.startButton = CMUImage(app.startButton)

def createLevel(app):
    #level background
    app.levelBackground = openImage("assets/sunsetBackgroundLevel.png")
    # Cast image type to CMUImage to allow for faster drawing
    app.levelBackground = CMUImage(app.levelBackground)

    #create level for game. making a 2d list of -1 then 
    # changing bottom row to 0s 
    
    app.levelRows = 10
    app.levelCols = 30
    app.level = []

    for row in range(app.levelRows):
        app.level.append([-1] * app.levelCols)
    #making bottom row of tiles 
    for tile in range(app.levelCols):
        app.level[app.levelRows - 1][tile] = 2  


    # getting level tile assets and putting in a list
    app.tile = []
    app.tileHeight = app.height // app.levelRows
    app.tileWidth = app.width // app.levelCols 
    
    for i in range(5):
        app.tile.append(openImage(f"assets\\Tiles\\Tile_{i}.png"))
        app.tile[i] = CMUImage(app.tile[i])           

def createFrame(app):
    app.frameRight = False
    app.frameLeft = False
    app.frameMoving = 0
    app.frameSpeed = 20
     
def setFrame(app):
    
    if app.frameRight:
        app.frameMoving += app.frameSpeed
    if app.frameLeft and app.frameMoving > 0:
        app.frameMoving -= app.frameSpeed

def drawMenu(app):

    drawImage(app.menuBackground, 0,0)
    drawImage(app.startButton, app.width//2 - app.startButtonWidth//2, app.height//2)

def drawLevel(app):
    for i in range(5):
        drawImage(app.levelBackground,i * app.width - app.frameMoving, 0)
    for row in range(len(app.level)):
        for col in range(len(app.level[row])):
            if app.level[row][col] != -1:
                drawImage(app.tile[app.level[row][col]], col * app.tileWidth, row * app.tileHeight)

def redrawAll(app):
    
    if not app.playState:
        drawMenu(app)
    else:
        drawLevel(app) 
      
def onMousePress(app, mouseX, mouseY):
    if not app.playState and distance(mouseX, mouseY, app.width//2 - app.startButtonWidth//2,
                                       app.height//2, app.startButtonWidth, app.startButtonHeight):
        app.playState = True

def onKeyHold(app, keys):

    if 'right' in keys:
        app.frameRight = True
        print('ji')
    elif 'left' in keys:
        app.frameLeft = True  
        print('plo') 
def onKeyRelease(app, key):
    if key == 'right':
        app.frameRight =- False
    elif key == 'left':
        app.frameLeft = False  

def onStep(app):
    setFrame(app) 

def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName)) 
 
def distance(mouseX, mouseY, x, y, width, height):
    if (x <= mouseX <= x+width) and (y <= mouseY <= y+height):
        return True 
      
def main():
    runApp(width=1000,height=500)     
main()    