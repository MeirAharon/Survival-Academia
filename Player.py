from cmu_graphics import *
from PIL import Image
import os, pathlib, time

class Player():
    def __init__(self, x, y, movementSpeed):
        self.movementSpeed = movementSpeed
        self.moving = False
        self.moveRight = False
        self.moveLeft = False
        self.gravity = True
        self.gravityStrength = 3
        self.prevPosX = x
        self.prevPosY = y
        self.posX = x
        self.posY = y
        self.futurePosX = 0
        self.futurePosY = 0
        self.vX = 0
        self.vY = 0
        self.gX = 0
        self.gY = 1
        self.velocity = 0
        self.width = 45
        self.height = 75
        self.spriteNum = 0
        self.sprites = []
        self.playerRectSize = []
        spritestrip = openImage("assets/Swordsman_spritelist.png")

        for i in range(0, 5):
            sprite = CMUImage(spritestrip.crop((45*i, 0, 45+45*i, 75)))
            self.sprites.append(sprite)
            self.playerRectSize.append((sprite.image.width, sprite.image.height))
            self.sprite = self.sprites[0]

        self.width, self.height = self.playerRectSize[0]
            

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
        elif 'left' in keys:    
            self.moving = True
            self.moveLeft = True
        elif 'down' in keys: 
            self.moving = True
            self.crouch = True
        elif 'up' in keys:
            self.moving = True
            self.jumping = True
        # checking if player has released the key
        if 'right' == key:
            self.moving = False
            self.moveRight = False
        elif 'left' == key:    
            self.moving = False
            self.moveLeft = False
        elif 'down' == key: 
            self.moving = False
            self.crouch = False
        elif 'up' == key:
            self.moving = False
            self.jumping = False  
    
    def updatePlayer(self):
        #checking posY
        if Player.checkCollisions(self, 'y'):
            if self.gravity == True:
                self.posY += self.gravityStrength 
        if Player.checkCollisions(self, 'x'):        
            if self.moveRight == True:
                self.posX += self.movementSpeed
            elif self.moveLeft == True:
                self.posX -= self.movementSpeed   

    def checkCollisions(self, axis):
        if axis == 'y':
            Player.futurePosition(self, 'y')
            if ((int(self.futurePosY // app.tileHeight), int(self.posX // app.tileWidth)) in app.tileDict
                    or int((self.futurePosY + self.height)// app.tileHeight), int((self.posX + self.width) // app.tileWidth)) in app.tileDict:
                return False
            print(int(self.futurePosY // app.tileHeight), int(self.futurePosX // app.tileWidth), self.posY // app.tileHeight, self.posX // app.tileWidth, self.posX, self.posY)
            return True
        if axis == 'x':
            Player.futurePosition(self, 'x')
            if ((int(self.posY // app.tileHeight), int(self.futurePosX // app.tileWidth)) in app.tileDict
                    or int((self.posY + self.height)// app.tileHeight), int((self.futurePosX + self.width) // app.tileWidth)) in app.tileDict:
                return False
            return True
        
    def futurePosition(self, axis):
        if axis == 'y':
            if self.gravity == True:
                self.futurePosY = self.posY + self.gravityStrength
        elif axis == 'x':        
            if self.moveRight == True:
                self.futurePosX = self.posX + self.movementSpeed
            elif self.moveLeft == True:
                self.futurePosX = self.posX - self.movementSpeed

    def drawPlayer(self):
        #player sprite
        drawImage(self.sprite, self.posX, self.posY)
        #rect for logic like collisions
        rectWidth, rectHeight = self.playerRectSize[0]
        drawRect(self.posX, self.posY, rectWidth, rectHeight, fill = None ) 

                

def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))                

# def calculateVelocity(app):
#             #this is called from onstep() so time is accounted for 
#             self.vX = (self.prevPosX - self.posX) 
#             self.vY = (self.prevPosY - self.posY)  
#             self.prevPosX = self.posX
#             self.prevPosY = self.posY