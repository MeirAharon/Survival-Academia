from cmu_graphics import *
from map import *
from PIL import Image
import os, pathlib

def onAppStart(app):
    app.gameBackground = openImage("assets/gameBackground.png")
    
    app.startButton = openImage("assets/startButton.png")
    app.startButtonWidth, app.startButtonHeight = app.startButton.width, app.startButton.height

    # Cast image type to CMUImage to allow for faster drawing
    app.gameBackground = CMUImage(app.gameBackground)
    app.startButton = CMUImage(app.startButton)

def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))
    
def redrawAll(app):
    
    drawImage(app.gameBackground, 0,0)
    drawImage(app.startButton, app.width//2 - app.startButtonWidth//2, app.height//2)

def onMousePress(app, mouseX, mouseY):
    if distance(mouseX, mouseY, app.width//2, app.height//2, app.startButtonWidth, app.startButtonHeight):
        app.gameBackground = openImage("assets/gameStarted.png")
        app.gameBackground = CMUImage(app.gameBackground)
         
def main():
    runApp(width=1280,height=720)     
main()    