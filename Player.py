from cmu_graphics import *
from PIL import Image
import os, pathlib, time

class Player():
    def __init__(self, x, y, movementSpeed):
        self.movementSpeed = movementSpeed
        self.moving = False
        self.moveRight = False
        self.moveLeft = False
        self.jumping = False
        self.gravity = True
        self.jumpHeight = -40
        self.gravityStrength = 15
        self.prevPosX = x
        self.prevPosY = y
        self.posX = x
        self.posY = y
        self.futurePosX = 0
        self.futurePosY = 0
        self.movementBufferX = 3
        self.vX = 0
        self.vY = 0
        self.gX = 0
        self.gY = 1
        self.velocity = 0
        self.width = 40
        self.height = 70
        self.spriteDirection = 'right'
        self.spriteCounter = 0
        self.sprites = []
        self.playerRectSize = []
        self.spritestrip = openImage("assets/Swordsman_spritelist2.png")

        for i in range(0, 8):
            sprite = CMUImage(self.spritestrip.crop((45*i, 0, 45+45*i, 75)))
            self.sprites.append(sprite)
            self.playerRectSize.append((sprite.image.width, sprite.image.height))
            self.sprite = self.sprites[0]    

        # self.width, self.height = self.playerRectSize[0]

    def calculateVelocity(self):
        #this is called from onstep() so time is accounted for 
        self.vX = (self.posX - self.prevPosX)
        self.vY = (self.posY - self.prevPosY)
        self.velocity = ((self.prevPosX - self.posX)**2 + (self.prevPosY - self.posY)**2)**0.5
        self.prevPosX = self.posX
        self.prevPosY = self.posY  

    def playerControls(self, keys, key):
        if 'right' in keys:
            self.moving = True
            self.moveRight = True
        if 'left' in keys:    
            self.moving = True
            self.moveLeft = True
        if 'down' in keys: 
            self.moving = True
            self.crouch = True
        if 'up' in keys:
            self.moving = True
            self.jumping = True
        # checking if player has released the key
        if 'right' == key:
            self.moving = False
            self.moveRight = False
        if 'left' == key:    
            self.moving = False
            self.moveLeft = False
        if 'down' == key: 
            self.moving = False
            self.crouch = False
        if 'up' == key:
            self.moving = False
            self.jumping = False  
    
    def updatePlayer(self):
    
        if Player.checkCollisions(self, 'right'):        
            if self.moveRight == True:
                self.spriteCounter = (1 + self.spriteCounter) % len(self.sprites)
                self.posX += self.movementSpeed
        if Player.checkCollisions(self, 'right'):        
            if self.moveLeft == True:
                self.spriteCounter = (1 + self.spriteCounter) % len(self.sprites)
                self.posX -= self.movementSpeed   
        if Player.checkCollisions(self, 'bottom'):
            if self.gravity == True:
                self.posY += self.gravityStrength
        if Player.checkCollisions(self, 'top'):        
            if self.jumping == True:
                self.posY += self.jumpHeight         

    def checkCollisions(self, axis):

        if axis == 'right' or axis == 'left':
            Player.futurePosition(self, 'x')
            for tile in app.tileList:
                if Player.rectanglesOverlap(self.futurePosX, self.posY, self.width, self.height, 
                                         tile.x, tile.y, app.tileWidth, app.tileHeight):
                    return False
            return True    
        if axis == 'top' or axis == 'bottom':
            Player.futurePosition(self, 'y')
            for tile in app.tileList:
                if Player.rectanglesOverlap(self.posX, self.futurePosY, self.width, self.height, 
                                         tile.x, tile.y, app.tileWidth, app.tileHeight):
                    return False
            return True    
    
    def rectanglesOverlap(left1, top1, width1, height1,
                            left2, top2, width2, height2):
        bottom1 = top1 + height1
        bottom2 = top2 + height2
        right1 = left1 + width1
        right2 = left2 + width2
        return bottom1 >= top2 and bottom2 >= top1 and right1 >= left2 and right2 >= left1
        
    def futurePosition(self, axis):

        if axis == 'x':        
            if self.moveRight == True:
                self.futurePosX = self.posX + self.movementSpeed
            elif self.moveLeft == True:
                self.futurePosX = self.posX - self.movementSpeed 
        
        elif axis == 'y':
            if self.gravity == True:
                self.futurePosY = self.posY + self.gravityStrength
            if self.jumping == True:
                self.futurePosY = self.posY + self.jumpHeight + self.gravityStrength    

    def drawPlayer(self):
        
        drawImage(self.sprites[self.spriteCounter], self.posX, self.posY)
        # drawRect(self.posX, self.posY, self.width, self.height, fill = None, border = 'black' ) 

def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))                
