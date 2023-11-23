from cmu_graphics import *
from PIL import Image
import os, pathlib, time
from Tile import *
from Player import *


def onAppStart(app):
    createMenu(app)
    createLevel(app)
    createFrame(app)
    createPlayer(app)
    
    app.playState = True
    app.spriteCounter = 0
    app.stepsPerSecond = 60
    app.moving = False

def createMenu(app):

    
    app.menuBackground = openImage("assets/menuBackground.png")
    app.startButton = openImage("assets/startButton.png")
    app.startButtonWidth, app.startButtonHeight = app.startButton.width, app.startButton.height
    app.menuBackground = CMUImage(app.menuBackground)
    app.startButton = CMUImage(app.startButton)

def createLevel(app):
    
    app.levelBackground = openImage("assets/sunsetBackgroundLevel.png")
    app.levelBackground = CMUImage(app.levelBackground)
    app.levelRows = 10
    app.levelCols = 25
    app.tileWidth =  app.width / app.levelCols
    app.tileHeight = app.height / app.levelRows
    app.level =  []

    for row in range(app.levelRows):
        if row < app.levelRows - 1:
            app.level.append([-1] * app.levelCols)
        else:
            app.level.append([2] * app.levelCols)
    
    app.tileDict = dict()
    app.tileList = []
    for row in range(len(app.level)):
        for col in range(len(app.level[row])):
            if app.level[row][col] != -1:
                app.tileDict[(row, col)] = Tile(row, col, app.level[row][col])
                app.tileList.append(Tile(row, col, app.level[row][col]))

     
def createFrame(app):
    app.frameRight = False
    app.frameLeft = False
    app.frameMoving = 0
    app.frameSpeed = 5
  

def createPlayer(app):
    app.meir = Player(10, 0, 5)    
            
def collisions(app):
    pass
     
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
    for i in range((app.levelRows)):
        drawLine(0, app.tileHeight * i, 1280, app.tileHeight * i)
    for i in range((app.levelCols)):
        drawLine(app.tileWidth * i, 0, app.tileWidth * i, 720)     

    for tile in app.tileList:
        
        drawImage(tile.img, tile.col * app.tileWidth, tile.row * app.tileHeight, width=app.tileWidth, height=app.tileHeight, fill = 'yellow')    

def redrawAll(app):
    
    if not app.playState:
        drawMenu(app)
    else:
        drawLevel(app)
        app.meir.drawPlayer()   
        rectWidth, rectHeight = app.meir.playerRectSize[0]  
        drawLabel(f'v({app.meir.velocity} pixels per second)', app.meir.posX + rectWidth, app.meir.posY + rectHeight + 20, size = 30)
        
      
def onMousePress(app, mouseX, mouseY):
    if not app.playState and clickDistance(mouseX, mouseY, app.width//2 - app.startButtonWidth//2,
                                       app.height//2, app.startButtonWidth, app.startButtonHeight):
        app.playState = True

def onKeyHold(app, keys):
    app.meir.playerControls(keys, None)
    if 'right' in keys:
        app.frameRight = True
        print('ji')
    elif 'left' in keys:
        app.frameLeft = True  
        print('plo') 

def onKeyRelease(app, key):
    app.meir.playerControls(dict(), key)
    if key == 'right':
        app.frameRight = False
    elif key == 'left':
        app.frameLeft = False  

def onStep(app):
    setFrame(app)
    app.meir.updatePlayer() 
    app.meir.calculateVelocity()
    

def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName)) 
 
def clickDistance(mouseX, mouseY, x, y, width, height):
    if (x <= mouseX <= x+width) and (y <= mouseY <= y+height):
        return True 
    
def main():
    runApp(width=1280,height=720)    

    # def position(self, x, y):
            
    #     self.posX += x
    #     self.posY += y
    #     self.spriteNum = (1 + self.spriteNum) % len(self.sprites)
    #     self.sprite = self.sprites[self.spriteNum]

   
        
    
main()    