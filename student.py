from cmu_graphics import *

def onAppStart(app):
    app.studentX = 20
    app.studentY = 20
    app.studentWidth = 30
    app.studentHeight = 50
    pass

def redrawAll(app):
    drawRect(app.studentX, app.studentY, app.studentWidth, app.studentHeight, fill = 'cyan' )
runApp()    
