from cmu_graphics import *
from PIL import Image
import os, pathlib, time
from Tile import *
from Player import *
from button import *

app.height = 720
app.width = 1280
def onAppStart(app):
    createMenu(app)
    createLevel(app)
    createFrame(app)
    createPlayer(app)
    createCollisionBoard(app)
    createLevelEditor(app)
    app.playState = True
    app.spriteCounter = 0
    app.stepsPerSecond = 60
    app.moving = False
#
# MENU SCREEN
#
def createMenu(app):

    app.menuBackground = openImage("assets/menuBackground.png")
    app.menuBackground = CMUImage(app.menuBackground)

    app.menuButtons = []
    app.buttonNames = ["inGame", "options", "levelEditor", "character"]
    for i in range(4):
        buttonImage = openImage(f"assets\\menuButtons\\button{i}.png")
        imageWidth, imageHeight = buttonImage.width, buttonImage.height
        buttonImage = CMUImage(buttonImage)

        if i == 0:
            x = app.width // 2 - imageWidth // 2
            y = app.height // 3 + imageHeight // 2
        else:
            x = i * (app.width // 4) - imageWidth // 2
            y = app.height - app.height // 3

        app.menuButtons.append(Button(x, y, imageWidth, imageHeight, app.buttonNames[i], i, buttonImage))


def drawMenu(app):
    
    drawImage(app.menuBackground, 0,0)
    for button in app.menuButtons:
        drawImage(button.img, button.x, button.y)

def start_redrawAll(app):
        drawMenu(app)
        
def start_onMousePress(app, mouseX, mouseY):
    for button in app.menuButtons:
        if button.buttonClicked(mouseX, mouseY):
            setActiveScreen(button.imgName)
    
def start_onKeyHold(app, keys):
    pass  
         
def start_onKeyRelease(app, key):
    pass  

def start_onStep(app):
    pass 
    # app.meir.calculateVelocity()
#
#LEVEL EDITOR
#
def createLevelEditor(app):
    app.background = rgb(122, 223, 253)
def levelEditor_redrawAll(app):
    drawRect(0,0,30,30, fill = 'blue')

#
# IN_GAME SCREEN
#
def createLevel(app):
    
    app.levelBackground = openImage("assets/sunsetBackgroundLevel.png")
    app.levelBackground = CMUImage(app.levelBackground)
    app.levelRows = 12
    app.levelCols = 60
    app.tileWidth =  60
    app.tileHeight = app.height // app.levelRows
    # print(app.tileHeight)
    app.level =  []

    for row in range(app.levelRows):
        if row < app.levelRows - 1:
            app.level.append([-1] * app.levelCols)
        else:
            app.level.append([2] * app.levelCols)
    app.level[10][5] = 2 # this is random block for testing
    app.rectList = []
    app.tileList = []
    for row in range(len(app.level)):
        for col in range(len(app.level[row])):
            
            if app.level[row][col] != -1:
                x = int(col * app.tileWidth)
                y = int(row * app.tileHeight)
                
                app.tileList.append(Tile(x, y, app.level[row][col]))
                
                
def createFrame(app):
    app.frameRight = False
    app.frameLeft = False
    app.frameMoving = 0
    app.frameSpeed = 5
  
def createPlayer(app):
    app.meir = Player(100, 500, 10)    

def createCollisionBoard(app):
    
    app.tileDict = dict()
    
    for row in range(-5, 200):
        for col in range(-5, 200):
            app.tileDict[(row, col)] = []
             
    for tile in app.tileList:
        row = int(tile.y // Tile.height)
        col = int(tile.x // Tile.width)
        app.tileDict[(row,col)].append(tile)
          
def setFrame(app):
    
    if app.frameRight:
        app.frameMoving += app.frameSpeed
    if app.frameLeft and app.frameMoving > 0:
        app.frameMoving -= app.frameSpeed 

def drawLevel(app):
       
    for i in range(5):
        drawImage(app.levelBackground,i * app.width - app.frameMoving, 0)
    for i in range((app.levelRows)):
        drawLine(0, app.tileHeight * i, app.width, app.tileHeight * i)
    for i in range((app.levelCols)):
        drawLine(app.tileWidth * i, 0, app.tileWidth * i, app.height)     

    for tile in app.tileList:
        drawImage(tile.img, tile.x, tile.y, width=app.tileWidth, height=app.tileHeight, fill = 'yellow')    

def inGame_redrawAll(app):
    
    if not app.playState:
        drawMenu(app)
    else:
        drawLevel(app)
        app.meir.drawPlayer()   
        rectWidth, rectHeight = app.meir.playerRectSize[0]  
        drawLabel(f'v({app.meir.velocity} pixels per second)', app.meir.posX + rectWidth, app.meir.posY + rectHeight + 20, size = 30)
        
def inGame_onMousePress(app, mouseX, mouseY):
    if not app.playState and clickDistance(mouseX, mouseY, app.width//2 - app.startButtonWidth//2,
                                       app.height//2, app.startButtonWidth, app.startButtonHeight):
        app.playState = True

def inGame_onKeyHold(app, keys):
    app.meir.playerControls(keys, None)
    if 'right' in keys:
        app.frameRight = True
        
    elif 'left' in keys:
        app.frameLeft = True  
         
def inGame_onKeyRelease(app, key):
    app.meir.playerControls(dict(), key)
    if key == 'right':
        app.frameRight = False
    elif key == 'left':
        app.frameLeft = False  

def inGame_onStep(app):
    setFrame(app)
    app.meir.updatePlayer()           
    
    
def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))
 
def clickDistance(mouseX, mouseY, x, y, width, height):
    if (x <= mouseX <= x+width) and (y <= mouseY <= y+height):
        return True 
    
def main():
    runAppWithScreens("start", width=1280,height=720)    
    
main()    