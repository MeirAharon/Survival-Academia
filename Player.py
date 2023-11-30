from cmu_graphics import *
from PIL import Image
import os, pathlib, time
from Tile import *
app.height = 720
app.width = 1280
class Player():
    
    width = 40
    height = 70
    def __init__(self, x, y, movementSpeed):
        self.movementSpeed = movementSpeed
        self.moving = False
        self.moveRight = False
        self.moveLeft = False
        self.jump = False
        self.gravityBoolean = True
        self.jumpHeight = -5
        self.gravityStrength = .5
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
        self.terminalVelocityY = 5
        self.terminalVelocityX = 5
        self.width = 40
        self.height = 70
        self.spriteDirection = 'right'
        self.flip = 0
        self.spriteCounter = 0
        self.sprites = []
        self.playerRectSize = []
        self.spritestrip = openImage("assets/Swordsman_spritelist2.png")
        self.yCollide = 0
        self.alive = True
        self.onGround = False

        for i in range(0, 8):
            sprite = CMUImage(self.spritestrip.crop((45*i, 0, 45+45*i, 75)))
            self.sprites.append(sprite)
            self.playerRectSize.append((sprite.image.width, sprite.image.height))
            self.sprite = self.sprites[0]    

        # self.width, self.height = self.playerRectSize[0]

    # def calculateVelocity(self):
    #     #this is called from onstep() so time is accounted for 
    #     self.vX = (self.posX - self.prevPosX)
    #     self.vY = (self.posY - self.prevPosY)
    #     self.velocity = ((self.prevPosX - self.posX)**2 + (self.prevPosY - self.posY)**2)**0.5
    #     self.prevPosX = self.posX
    #     self.prevPosY = self.posY  

    def playerControls(self, keys, key):
        if 'right' in keys:
            self.moveRight = True
        if 'left' in keys:    
            self.moveLeft = True
        if 'down' in keys: 
            self.crouch = True
        if 'up' in keys and self.onGround:
            self.jump = True
        # checking if player has released the key
        if 'right' == key:
            self.moveRight = False
        if 'left' == key:    
            self.moveLeft = False
        if 'down' == key:
            self.crouch = False
        if 'up' == key:
            self.jump = False  
    
    def updatePlayer(self):
        
        
        self.dx = 0
        self.dy = 0
        if self.alive:
            if self.moveRight:
                self.dx = self.movementSpeed
            if self.moveLeft:
                self.dx = -self.movementSpeed
            if self.jump:
                self.vY = self.jumpHeight
                self.jump = False

            self.vY += self.gravityStrength 
            if self.vY > self.terminalVelocityY:
                self.vY = self.terminalVelocityY 
                           
            self.dy += self.vY

            Player.checkCollisions(self, 'right')
            Player.checkCollisions(self, 'left')
            Player.checkCollisions(self, 'top')
            Player.checkCollisions(self, 'bottom')
            print('up hi dy',self.dy, self.dy + self.posY)
            self.posX += self.dx
            self.posY += self.dy
            Player.checkCollisions(self, 'bottom')
            
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

        if axis == 'right' or axis == 'left':
            
            col = int((self.posX + self.dx) // app.tileWidth)
            row = int(self.posY // app.tileHeight)
            Player.getRange(self,row,col)
            
            for i in range(self.rangeStartRows, self.rangeEndRows):
                for j in range(self.rangeStartCols, self.rangeEndCols):
                    for object in app.tileDict[(row + i, col + j)]:
                        if isinstance(object, Tile):
                                if Player.rectanglesOverlap(self.posX + self.dx, self.posY, self.width, self.height, 
                                                            object.x, object.y, object.width, object.height):
                                    
                                    # self.dx = 0
                                    # not done here
                                    if self.vX < 0:
                                        print('collided, moving left')
                                        self.dx = object.left() - self.posX
                                    elif self.vX > 0:
                                        print('collided, moving right')
                                        self.dx = object.right() - self.posX  + self.width  
                                    self.vx = 0
                                       
                                    
                
        if axis == 'top' or axis == 'bottom':
            col = int(self.posX // app.tileWidth)
            row = int((self.posY + self.dy) // app.tileHeight)
            
            Player.getRange(self,row,col)

            for i in range(self.rangeStartRows, self.rangeEndRows):
                for j in range(self.rangeStartCols, self.rangeEndCols):
                    for object in app.tileDict[(row + i, col + j)]:
                        if isinstance(object, Tile):
                                if Player.rectanglesOverlap(self.posX, self.posY + self.dy, self.width, self.height, 
                                                            object.x, object.y, object.width, object.height):
                                    print('vy',self.vY)
                                    if self.vY < 0:
                                        self.vY = 0
                                        self.dy = object.bottom() - self.posY
                                        
                                    elif self.vY >= 0:
                                        print(self.height)
                                        print('bob', object.top(), (self.posY), 'y tile', object.y, 'self y', self.posY + self.height )
                                        self.vY = 0
                                        self.dy = object.top() - (self.posY + self.height)
                                        self.onGround = True
                                else:        
                                    print('didnt collide', 'vy', self.vY, 'dy', self.dy )        
                                        
                                    
                
    
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
            

    def drawPlayer(self):
        if self.flip:
            drawImage(self.sprites[self.spriteCounter], self.posX, self.posY)
            drawRect(self.posX, self.posY, self.width, self.height, fill = None, border = 'black' ) 
        else:
            drawImage(self.sprites[self.spriteCounter], self.posX, self.posY)
            drawRect(self.posX, self.posY, self.width, self.height, fill = None, border = 'black' )

def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))                
