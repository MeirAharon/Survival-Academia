from cmu_graphics import *
from PIL import Image
import os, pathlib, time
from Tile import *
from aiAlgorithm import *
import copy

app.height = 720
app.width = 1280
class Enemy():
    
    width = 40
    height = 70
    def __init__(self, x, y, movementSpeed):
        self.movementSpeed = movementSpeed
        self.moving = False
        self.moveRight = False
        self.moveLeft = False
        self.jump = False
        self.gravityBoolean = True
        self.jumpHeight = -8
        self.gravityStrength = 2.2
        self.prevPosX = x
        self.prevPosY = y
        self.posX = x
        self.posY = y
        self.dx = 0
        self.dy = 0
        self.futurePosX = 0
        self.futurePosY = 0
        self.movementBufferX = 3
        self.vX = 0
        self.vY = 0
        self.gX = 0
        self.gY = 1
        self.velocity = 0
        self.terminalVelocityY = 8
        self.terminalVelocityX = 5
        self.width = 40
        self.height = 50
        self.spriteDirection = 'right'
        self.flip = 0
        self.spriteCounter = 0
        self.sprites = []
        self.EnemyRectSize = []
        self.image = openImage("assets/Tiles/Tile_14.png")
        self.image = CMUImage(self.image)
        self.yCollide = 0
        self.alive = True
        self.onGround = False
        self.row = self.posY // 60
        self.col = self.posX // 60

    
    def updateEnemy(self, levelList):
         
        self.movesList = aStarAlgorithm(levelList, (int(self.posY // 60),int(self.posX // 60)), (int(app.meir.posY // 60),int(app.meir.posX // 60)))
        if self.movesList != None and len(self.movesList) > 1:
            x = tuple(x - y for x, y in zip(self.movesList[1], self.movesList[0]))
            if x == (0,1):
                # moving right
                self.moving = True
                self.dx = self.movementSpeed
                self.vX = self.movementSpeed
            elif x == (0,-1):  
                # moving left  
                self.moving = True
                self.dx = -self.movementSpeed
                self.vX = -self.movementSpeed  
            elif x == (-1,0):
                if self.onGround:
                    self.vY = self.jumpHeight
                    self.onGround = False    
            elif x == (-1,1):
                if self.onGround:
                    self.vY = self.jumpHeight
                    self.onGround = False
                self.moving = True
                self.dx = self.movementSpeed
                self.vX = self.movementSpeed
            elif x == (-1,1):
                if self.onGround:
                    self.vY = self.jumpHeight
                    self.onGround = False
                self.moving = True
                self.dx = -self.movementSpeed
                self.vX = -self.movementSpeed    



            
        
        # self.dx = 0
        # self.dy = 0
        
        # if self.jump and self.onGround:
        #     self.vY = self.jumpHeight
        #     self.onGround = False

        self.vY += self.gravityStrength 
        if self.vY > self.terminalVelocityY:
            self.vY = self.terminalVelocityY 
                        
        self.dy += self.vY

        Enemy.checkCollisions(self, 'right')
        Enemy.checkCollisions(self, 'top')
        self.prevPosX  = self.posX
        self.prevPosY = self.posY
        self.posX += self.dx
        self.posY += self.dy
        if self.posX < 0:
            self.posX = 0 
        if self in app.worldCollisionDict[(int(self.prevPosY // 60), int(self.prevPosX // 60))]:  
            app.worldCollisionDict[(int(self.prevPosY // 60), int(self.prevPosX // 60))].pop(0)    
        
        app.worldCollisionDict[(int(self.posY // 60), int(self.posX // 60))].append(self) 
            
    def getRange(self, row, col):
        if row == 0 and col == 0:
            self.rangeStartRows = 0
            self.rangeEndRows = 2
            self.rangeStartCols = 0
            self.rangeEndCols = 2
        elif row == 0 and col > 0:
            self.rangeStartRows = 0
            self.rangeEndRows = 2
            self.rangeStartCols = -1
            self.rangeEndCols = 2
        elif row > 0 and col == 0:
            self.rangeStartRows = -1
            self.rangeEndRows = 2
            self.rangeStartCols = 0
            self.rangeEndCols = 2
        elif row > 0 and col > 0:
            self.rangeStartRows = -1
            self.rangeEndRows = 2
            self.rangeStartCols = -1
            self.rangeEndCols = 2
    def checkCollisions(self, axis):

        if axis == 'right':
            
            col = int((self.posX + self.dx) // app.tileWidth)
            row = int(self.posY // app.tileHeight)
            Enemy.getRange(self,row,col)
            
            for i in range(self.rangeStartRows, self.rangeEndRows):
                for j in range(self.rangeStartCols, self.rangeEndCols):
                    for object in app.worldCollisionDict[(row + i, col + j)]:
                        if isinstance(object, Tile):
                                if Enemy.rectanglesOverlap(self.posX + self.dx, self.posY, self.width, self.height, 
                                                            object.x, object.y, object.width, object.height):
                                    

                                    self.dx = 0
                                    
                                    return True
                        if int(self.posX + self.dx) // 60 != (self.posX // 60):
                            app.worldCollisionDict[(int(self.posY // 60),int(self.posX + self.dx // 60))] = self
                            app.worldCollisionDict[(int(self.posY // 60),int(self.posX // 60))] = []                       
                                       
        if axis == 'top':
            col = int((self.posX)// app.tileWidth)
            row = int((self.posY + self.dy) // app.tileHeight)
            
            Enemy.getRange(self,row,col)

            for i in range(self.rangeStartRows, self.rangeEndRows):
                for j in range(self.rangeStartCols, self.rangeEndCols):
                    for object in app.worldCollisionDict[(row + i, col + j)]:
                        if isinstance(object, Tile):
                                if Enemy.rectanglesOverlap(self.posX, self.posY + self.dy, self.width, self.height, 
                                                            object.x, object.y, object.width, object.height):
                                    
                                    self.dy = 0
                                    self.onGround = True
                                    
        
                                
    def rectanglesOverlap(left1, top1, width1, height1,
                            left2, top2, width2, height2):
        bottom1 = top1 + height1
        bottom2 = top2 + height2
        right1 = left1 + width1
        right2 = left2 + width2
        return bottom1 >= top2 and bottom2 >= top1 and right1 >= left2 and right2 >= left1
    def distanceBetweenRects(x1, y1, x2, y2):
        distance = max(((x2 - x1)/2 , (y2 - y1)/2))
        
        return distance
            

    def drawEnemy(self, scroll):
        if self.flip:
            drawImage(self.image, self.posX - scroll, self.posY, self.width, self.height)
            drawRect(self.posX - scroll, self.posY, self.width, self.height, fill = None, border = 'black' ) 
        else:
            drawImage(self.image, self.posX - scroll, self.posY, height = 50)
            drawRect(self.posX - scroll, self.posY, self.width, self.height, fill = None, border = 'black' )

def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))                
