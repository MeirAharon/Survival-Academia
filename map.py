from cmu_graphics import *

def onAppStart(app):
    app.stepsPerSecond = 10
    app.grid = []
    
    pass
def distance(mouseX, mouseY, x, y, width, height):
    if (x <= mouseX <= x+width) and (y <= mouseY <= y+height):
        return True
    
    
    