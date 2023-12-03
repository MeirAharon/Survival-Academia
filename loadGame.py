from cmu_graphics import *
from PIL import Image
import os, pathlib, time
from Tile import *
from Player import *
from button import *
from Enemy import *

app.height = 720
app.width = 1280
def onAppStart(app):
    
    start_createMenu(app)
    inGame_createLevel(app)
    inGame_createFrame(app)
    inGame_createPlayer(app)
    inGame_createEnemies(app)
    inGame_createCollisionBoard(app)
    levelEditor_createLevelEditor(app)
    gameOver_createScreen(app)
    app.playState = True
    app.spriteCounter = 0
    app.stepsPerSecond = 60
    app.moving = False
#
# MENU SCREEN
#
def start_createMenu(app):

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
def levelEditor_createLevelEditor(app):
    app.levelBackground = openImage("assets/sunsetBackgroundLevel.png")
    app.levelBackground = CMUImage(app.levelBackground)
    app.levelEditorScroll = 0
    app.levelEditorButtonNames = ["deselect", "back", "save", "delete", "load"]
    app.background = rgb(122, 223, 253)
    app.editorRows = 12
    app.editorCols = 60
    app.editorTileButtons = []
    app.tileNumber = -1
    app.tileSelected = False
    app.tilesPlaced = []
    app.worldCollisionDictionary = dict()
    app.deleteTile = False
    # create empty level list
    for row in range(app.editorRows):
        app.tilesPlaced.append([20] * app.editorCols)
        

    for i in range(15):
        tileImage = openImage(f"assets\\levelEditorButtons\\Tile_{i}.png")
        tileWidth, tileHeight = 50, 50
        tileImage = CMUImage(tileImage)
        app.editorTileButtons.append(Button(900 + (i*60 )%180, 50 + (i//3)*100, tileWidth, tileHeight, i, tileImage))

    for i in range(5):
        buttonImage = openImage(f"assets\\levelEditorButtons\\button{i}.png" )   
        buttonWidth, buttonHeight = 100, 60
        buttonImage = CMUImage(buttonImage)
        imgName = app.levelEditorButtonNames[i]
        if i == 2:
            app.editorTileButtons.append(Button(50, 620, buttonWidth, buttonHeight, i, buttonImage, imgName))
        elif i == 3:
            app.editorTileButtons.append(Button(920 + buttonWidth, 520, buttonWidth, buttonHeight, i, buttonImage, imgName)) 
        elif i == 4:
            app.editorTileButtons.append(Button(70 + buttonWidth, 620, buttonWidth, buttonHeight, i, buttonImage, imgName))      
        else:
            app.editorTileButtons.append(Button(900, 520 + i*(buttonHeight + 20), buttonWidth, buttonHeight, i, buttonImage, imgName))

def levelEditor_redrawAll(app):
    for i in range(5):
        drawImage(app.levelBackground,i * app.width + app.levelEditorScroll, 0)
    
    for row in range(app.editorRows):
        drawLine(0, row * 50, app.width, row * 50)
    for col in range(app.editorCols):
        drawLine(col * 50 + app.levelEditorScroll, 0, col * 50 + app.levelEditorScroll, app.height)
    for tile in app.worldCollisionDictionary:
        tileImage = openImage(f"assets\\levelEditorButtons\\Tile_{app.worldCollisionDictionary[tile]}.png")
        tileWidth, tileHeight = 50, 50
        tileImage = CMUImage(tileImage)
        row, col = tile
        x = int(col *50)
        y = int(row*50)
        if x + app.levelEditorScroll  < 880  and y < 600:
            drawImage(tileImage, x + app.levelEditorScroll, y, width = tileWidth, height = tileHeight )    
    drawRect(880,0,880,app.height, fill = rgb(85, 51, 51))
    drawRect(0, 600, 880, app.height, fill = rgb(85, 51, 51) )
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

    
    if app.tileSelected and mouseX < 880 and mouseY < 600 and not app.deleteTile:
        #list we are building for saving a level
        app.tilesPlaced[mouseY // 50][ (-1 *app.levelEditorScroll + mouseX) // 50 ] = app.tileNumber
        #dictionary for drawing in real time
        app.worldCollisionDictionary[(mouseY // 50, (-1 * app.levelEditorScroll + mouseX) // 50)] = app.tileNumber
    if app.deleteTile:
        if app.worldCollisionDictionary.get((mouseY // 50, (-1 * app.levelEditorScroll + mouseX) // 50)) != None:
            app.tilesPlaced[mouseY // 50][ (-1 *app.levelEditorScroll + mouseX) // 50 ] = 20 # THIS IS WHERE IM SETTING MAP VALUES GETTING DELETED
            popped = app.worldCollisionDictionary.pop((mouseY // 50, (-1 * app.levelEditorScroll + mouseX) // 50))
            
        
        
    for tile in app.editorTileButtons:
        if tile.buttonClicked(mouseX, mouseY):
            if tile.imgName == "back":
                setActiveScreen("start")
            elif tile.imgName == "save":
                levelEditor_saveLevel(app) 
            elif tile.imgName == "delete":
                app.deleteTile = not app.deleteTile
            elif tile.imgName == "load":
                levelEditor_loadLevel(app)    
                
            app.tileSelected = True
            app.tileNumber = tile.imgNum
            
def levelEditor_saveLevel(app):
    open('level1.txt', 'w').close()
    level = open("level1.txt", "w")
    
    for row in app.tilesPlaced:
        
        level.write(' '.join([str(item) for item in row])+'\n')
    level.close()
    level = open("level1.txt", "r")
    

def levelEditor_loadLevel(app):
    app.tilesPlaced = []
    level = open("level1.txt", "r")
    for row, line in enumerate(level):
        # for col, char in enumerate(line.split()):

        app.tilesPlaced.append([int(char) for char in line.split()])            
    level.close()
    level = open("level1.txt", "r")

    # for row in range(len(app.level)):
    #     for col in range(len(app.level[row])):
    #         if app.level[row][col] != 20:
    #             x = int(col * app.tileWidth)
    #             y = int(row * app.tileHeight)
    #             app.tileList.append(Tile(x, y, app.level[row][col]))

#
# IN_GAME SCREEN
#
def inGame_createLevel(app):
    app.scrollMargin = 600
    app.gameStartTime = int(time.time())
    app.gameTimeLimit = 450
    app.stepsPerSecond = 60
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
    app.worldDrawData = []
    app.enemyList = []

    level = open("level1.txt", "r")
    for line in (level):           
        app.level.append([int(char) for char in line.split()])
                    
    level.close()
    level = open("level1.txt", "r")

    
    for row in range(len(app.level)):
        for col in range(len(app.level[row])):
            if app.level[row][col] != 20 and app.level[row][col] != 14:
                x = int(col * app.tileWidth)
                y = int(row * app.tileHeight)
                app.worldDrawData.append(Tile(x, y, app.level[row][col]))
                
                        
def inGame_createFrame(app):
    app.frameRight = False
    app.frameLeft = False
    app.frameScroll = 0
    app.frameSpeed = 5
  
def inGame_createPlayer(app):
    app.meir = Player(100, 500, 10)    
def inGame_createEnemies(app):
    for row in range(len(app.level)):
        for col in range(len(app.level[row])):
            if app.level[row][col] == 14:
                x = int(col * app.tileWidth)
                y = int(row * app.tileHeight)
                app.enemyList.append(Enemy(x, y, 5)) 

def inGame_createCollisionBoard(app):
    
    app.worldCollisionDict = dict()
    
    for row in range(-8, 20):
        for col in range(-8, 65):
            app.worldCollisionDict[(row, col)] = []
             
    for tile in app.worldDrawData:
        row = int(tile.y // Tile.height)
        col = int(tile.x  // Tile.width)
        app.worldCollisionDict[(row,col)].append(tile)
    for enemy in app.enemyList:
        row = int(enemy.posY // 60)
        col = int(enemy.posX // 60)
        app.worldCollisionDict[(row, col)].append(enemy)
        

          
def inGame_setFrame(app):
    if app.meir.posX < app.frameScroll + app.scrollMargin and app.frameScroll - app.scrollMargin > -1:
        app.frameScroll = app.meir.posX - app.scrollMargin
    if app.meir.posX > app.frameScroll + app.width - app.scrollMargin:
        app.frameScroll = (app.meir.posX - app.width) + app.scrollMargin

def inGame_drawLevel(app):
     
    for i in range(5):
        drawImage(app.levelBackground,i * app.width - app.frameScroll, 0)
    for i in range((app.levelRows)):
        drawLine(0, app.tileHeight * i, app.width, app.tileHeight * i)
    for i in range((app.levelCols)):
        drawLine(app.tileWidth * i, 0, app.tileWidth * i, app.height)     

    for item in app.worldDrawData: 
        if item.x >= app.frameScroll - 50 and item.x <= app.width + app.frameScroll:
            drawImage(item.img, item.x - app.frameScroll, item.y, width=app.tileWidth, height=app.tileHeight)
    for enemy in app.enemyList:
        enemy.drawEnemy(app.frameScroll) 
    app.meir.drawPlayer(app.frameScroll)           
                 
    drawLabel(f'Distance to Win: {2500 - app.meir.posX}', 1100, 20, fill = 'white', size = 36)       
    drawLabel(f'Time Left: {app.gameTimeLimit - (int(time.time()) - app.gameStartTime)}', 1140, 60, fill = 'white', size = 36)

    
def inGame_redrawAll(app):

        inGame_drawLevel(app)

def inGame_onMousePress(app, mouseX, mouseY):
    if not app.playState and clickDistance(mouseX, mouseY, app.width//2 - app.startButtonWidth//2,
                                       app.height//2, app.startButtonWidth, app.startButtonHeight):
        app.playState = True
    for value in app.worldCollisionDict.values():
        if isinstance(value, Enemy):
            print(value)
            

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
# def inGame_updateWorldData(app):
#     row, col = app.meir.posY // 50, app.meir.posX // 50
#     app.worldData[row][col] = 19
#     for enemy in app.enemyList:
#         row, col = enemy.posY // 50, enemy.posX // 50
#         app.worldData[row][col] = 14

def inGame_onStep(app):
    
    # inGame_updateWorldData(app)
    inGame_setFrame(app)
    app.meir.updatePlayer()
    
    app.level[int(app.meir.posY // 60) - 1][int(app.meir.posX // 60)] = 8
    app.level[int(app.meir.prevPosY // 60) - 1][int(app.meir.prevPosX // 60)] = 20
    
    for enemy in app.enemyList:
        if enemy.posX >= app.frameScroll - 50 and enemy.posX <= app.width + app.frameScroll: # for efficiency only making the ones in frame attack
            enemy.updateEnemy(app.level)
    if app.meir.alive == False:
        setActiveScreen("gameOver")
    if app.meir.posX > 2500:
        setActiveScreen("gameOver")
    if time.time() - app.gameStartTime > app.gameTimeLimit:
        app.meir.alive = False
        setActiveScreen("gameOver")
#
# GAME OVER SCREEN
# 
def gameOver_createScreen(app):
    app.gameOverBackground = openImage("assets/sunsetBackgroundLevel.png")
    app.gameOverBackground = CMUImage(app.gameOverBackground)
    app.gameOverText = openImage("assets/gameOver.png")
    app.gameOverText = CMUImage(app.gameOverText)              
def gameOver_redrawAll(app):
    
    drawImage(app.gameOverBackground, 0, 0)
    drawImage(app.gameOverText, 0, 0)    
    
def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))
 
def clickDistance(mouseX, mouseY, x, y, width, height):
    if (x <= mouseX <= x+width) and (y <= mouseY <= y+height):
        return True 
      

def main():
    runAppWithScreens("start", width=1280,height=720)    
    
main()    