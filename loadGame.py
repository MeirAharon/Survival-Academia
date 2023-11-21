from cmu_graphics import *
from map import *
from PIL import Image
import os, pathlib, time

def onAppStart(app):
    setMenu(app)
    setMap(app)
    setTiles(app)
    setLevel(app)
    app.playState = False
    
def setMenu(app):

    #get files for main menu
    app.menuBackground = openImage("assets/menuBackground.png")
    app.startButton = openImage("assets/startButton.png")
    #get sizes before casting as cmu image
    app.startButtonWidth, app.startButtonHeight = app.startButton.width, app.startButton.height
    #make cmu image for faster drawing
    app.menuBackground = CMUImage(app.menuBackground)
    app.startButton = CMUImage(app.startButton)

def setMap(app):
    #create map for game. making a 2d list of -1 then 
    # changing bottom row to 0s 
    
    app.mapRows = 10
    app.mapCols = 100
    app.map = []

    for row in range(app.mapRows):
        app.map.append([-1] * app.mapCols)
    #making bottom row of tiles 
    for tile in range(app.mapCols):
        app.map[app.mapRows - 1][tile] = 0   
    print(app.map)     

def setTiles(app):
    # getting map tiles and assigning them to variables
    app.tile = []
    app.tileHeight = app.height // app.mapRows
    app.tileWidth = app.width // app.mapCols 
    
    for i in range(5):
        app.tile.append(openImage(f"assets\\Tiles\\Tile_{i}.png"))
        app.tile[i] = CMUImage(app.tile[i])


def setLevel(app):
    app.levelBackground = openImage("assets/sunsetBackgroundLevel.png")
    # Cast image type to CMUImage to allow for faster drawing
    app.levelBackground = CMUImage(app.levelBackground)

def drawMenu(app):

    drawImage(app.menuBackground, 0,0)
    drawImage(app.startButton, app.width//2 - app.startButtonWidth//2, app.height//2)

def drawLevel(app):
    drawImage(app.levelBackground, 0, 0)
    for row in range(len(app.map)):
        for col in range(len(app.map[row])):
            if app.map[row][col] != -1:
                drawImage(app.tile[app.map[row][col]], col * app.tileWidth, row * app.tileHeight)

def redrawAll(app):
    
    if not app.playState:
        drawMenu(app)
    else:
        drawLevel(app)   
          
def onMousePress(app, mouseX, mouseY):
    if not app.playState and distance(mouseX, mouseY, app.width//2 - app.startButtonWidth//2,
                                       app.height//2, app.startButtonWidth, app.startButtonHeight):
        app.playState = True

def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))   
      
def main():
    runApp(width=1200,height=720)     
main()    