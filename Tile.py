from cmu_graphics import *
from PIL import Image
import os, pathlib, time

class Tile():
    
    def __init__(self, row, col, imgNum):
        self.row = row
        self.col = col
        self.img = openImage(f"assets\\Tiles\\Tile_{imgNum}.png")
        self.img = CMUImage(self.img) 

def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))            