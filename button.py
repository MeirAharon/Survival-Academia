class Button:
    def __init__(self, x, y, width, height,imgNum, img, imgName='none'):
        self.x = x
        self.y = y
        self.width = width 
        self.height = height
        self.imgName = imgName
        self.imgNum = imgNum
        self.img = img

    def buttonClicked(self, mouseX, mouseY):
        if (self.x <= mouseX <= self.x+self.width) and (self.y <= mouseY <= self.y + self.height):
            return True

