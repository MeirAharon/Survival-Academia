from cmu_graphics import *
from PIL import Image
import os, pathlib, time

class Tile():
    
    def __init__(self, x, y, imgNum):
        self.x = x
        self.y = y
        self.img = openImage(f"assets\\Tiles\\Tile_{imgNum}.png")
        self.img = CMUImage(self.img) 

def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))            