from cmu_graphics import *
from PIL import Image
import os, pathlib, time
app.height = 720
app.width = 1280
class Tile():
    width = 60
    height = 60
    def __init__(self, x, y, imgNum):
        self.x = x
        self.y = y
        self.img = openImage(f"assets/Tiles/Tile_{imgNum}.png")
        self.img = CMUImage(self.img) 
        self.height = 60
        self.width = 60

    def bottom(self):
        return self.y + self.height  
       
    def top(self):
        return self.y
    
    def right(self):
        return self.x + self.width
    
    def left(self):
        return self.x  
    # def draw(self):
    #      drawImage(self.img, self.x , self.y, width = self.width, height = self.height)
        

def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))            