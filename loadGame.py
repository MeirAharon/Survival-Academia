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
    loadLevel(app)
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

        app.menuButtons.append(Button(x, y, imageWidth, imageHeight, i, buttonImage, app.buttonNames[i]))


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
    app.levelEditorScroll = 0
    app.levelEditorButtonNames = ["deselect", "back", "save", "delete"]
    app.background = rgb(122, 223, 253)
    app.editorRows = 12
    app.editorCols = 60
    app.editorTileButtons = []
    app.tileNumber = -1
    app.tileSelected = False
    app.tilesPlaced = []
    app.tileDictionary = dict()
    app.deleteTile = False
    # create empty level list
    for row in range(app.editorRows):
        app.tilesPlaced.append([20] * app.editorCols)
        

    for i in range(15):
        tileImage = openImage(f"assets\\levelEditorButtons\\Tile_{i}.png")
        tileWidth, tileHeight = 50, 50
        tileImage = CMUImage(tileImage)
        app.editorTileButtons.append(Button(900 + (i*60 )%180, 50 + (i//3)*100, tileWidth, tileHeight, i, tileImage))

    for i in range(4):
        buttonImage = openImage(f"assets\\levelEditorButtons\\button{i}.png" )   
        buttonWidth, buttonHeight = 100, 60
        buttonImage = CMUImage(buttonImage)
        imgName = app.levelEditorButtonNames[i]
        if i == 2:
            app.editorTileButtons.append(Button(50, 620, buttonWidth, buttonHeight, i, buttonImage, imgName))
        elif i == 3:
            app.editorTileButtons.append(Button(920 + buttonWidth, 520, buttonWidth, buttonHeight, i, buttonImage, imgName))        
        else:
            app.editorTileButtons.append(Button(900, 520 + i*(buttonHeight + 20), buttonWidth, buttonHeight, i, buttonImage, imgName))

def levelEditor_redrawAll(app):
    
    for row in range(app.editorRows):
        drawLine(0, row * 50, app.width, row * 50)
    for col in range(app.editorCols):
        drawLine(col * 50 + app.levelEditorScroll, 0, col * 50 + app.levelEditorScroll, app.height)
    for tile in app.tileDictionary:
        tileImage = openImage(f"assets\\levelEditorButtons\\Tile_{app.tileDictionary[tile]}.png")
        tileWidth, tileHeight = 50, 50
        tileImage = CMUImage(tileImage)
        row, col = tile
        x = int(col *50)
        y = int(row*50)
        if x + app.levelEditorScroll  < 880  and y < 600:
            drawImage(tileImage, x + app.levelEditorScroll, y, width = tileWidth, height = tileHeight )    
    drawRect(880,0,880,app.height, fill = rgb(122, 223, 253))
    drawRect(0, 600, 880, app.height, fill = rgb(122, 223, 253) )
    for tile in app.editorTileButtons:
        drawImage(tile.img, tile.x, tile.y, width = tile.width, height=tile.height)    

def levelEditor_onKeyHold(app, keys):
    if 'right' in keys:
        app.levelEditorScroll -= 5
    if 'left' in keys:
        app.levelEditorScroll += 5 
    if app.levelEditorScroll > 0:
        app.levelEditorScroll = 0   

def levelEditor_onMousePress(app, mouseX, mouseY):

    print('in mouse press')
    if app.tileSelected and mouseX < 880 and mouseY < 600 and not app.deleteTile:
        #list we are building for saving a level
        app.tilesPlaced[mouseY // 50][ (-1 *app.levelEditorScroll + mouseX) // 50 ] = app.tileNumber
        #dictionary for drawing in real time
        app.tileDictionary[(mouseY // 50, (-1 * app.levelEditorScroll + mouseX) // 50)] = app.tileNumber
    if app.deleteTile:
        if app.tileDictionary.get((mouseY // 50, (-1 * app.levelEditorScroll + mouseX) // 50)) != None:
            app.tilesPlaced[mouseY // 50][ (-1 *app.levelEditorScroll + mouseX) // 50 ] = 20 # THIS IS WHERE IM SETTING MAP VALUES GETTING DELETED
            popped = app.tileDictionary.pop((mouseY // 50, (-1 * app.levelEditorScroll + mouseX) // 50))
            print('indeletetile', popped)
        
        
    for tile in app.editorTileButtons:
        if tile.buttonClicked(mouseX, mouseY):
            if tile.imgName == "back":
                setActiveScreen("start")
            elif tile.imgName == "save":
                saveLevel(app) 
            elif tile.imgName == "delete":
                app.deleteTile = not app.deleteTile
                
            app.tileSelected = True
            app.tileNumber = tile.imgNum
            
def saveLevel(app):
    level = open("level1.txt", "w")
    for row in app.tilesPlaced:
        print(row)
        level.write(' '.join([str(item) for item in row])+'\n')
    level.close()
    level = open("level1.txt", "r")
    loadLevel(app)

def loadLevel(app):
    level = open("level1.txt", "r")
    for line in (level):           
            app.level.append([int(char) for char in line.split()])            
    level.close()
    level = open("level1.txt", "r")

#
# IN_GAME SCREEN
#
def createLevel(app):
    app.charList = []
    app.levelBackground = openImage("assets/sunsetBackgroundLevel.png")
    app.levelBackground = CMUImage(app.levelBackground)
    app.levelRows = 12
    app.levelCols = 60
    app.tileWidth =  60
    app.tileHeight = app.height // app.levelRows
    
    app.level =  []
    app.levelFile = open("level1.txt", "r")
    app.rectList = []
    app.tileList = []

    level = open("level1.txt", "r")
    for line in (level):           
        app.level.append([int(char) for char in line.split()])
        print(app.level)            
    level.close()
    level = open("level1.txt", "r")
    print(app.level)
    
    for row in range(len(app.level)):
        for col in range(len(app.level[row])):
            if app.level[row][col] != 20:
                x = int(col * app.tileWidth)
                y = int(row * app.tileHeight)
                app.tileList.append(Tile(x, y, app.level[row][col]))
            
def createFrame(app):
    app.frameRight = False
    app.frameLeft = False
    app.frameScroll = 0
    app.frameSpeed = 5
  
def createPlayer(app):
    app.meir = Player(100, 500, 10)    

def createCollisionBoard(app):
    
    app.tileDict = dict()
    
    for row in range(-80, 200):
        for col in range(-80, 200):
            app.tileDict[(row, col)] = []
             
    for tile in app.tileList:
        row = int(tile.y // Tile.height)
        col = int(tile.x  // Tile.width)
        app.tileDict[(row,col)].append(tile)
          
def setFrame(app):
    
    if app.frameRight:
        app.frameScroll -= app.frameSpeed
    if app.frameLeft and app.frameScroll > 0:
        app.frameScroll += app.frameSpeed 

def drawLevel(app):
       
    for i in range(5):
        drawImage(app.levelBackground,i * app.width + app.frameScroll, 0)
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