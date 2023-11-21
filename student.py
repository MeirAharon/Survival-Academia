class Student():
    def __init__(self):
        self.moveX = 0
        self.moveY = 0
        self.sprite = []
        spritestrip = openImage("assets/Swordsman_spritelist.png")
        for i in range(0, 5):
            sprite = CMUImage(spritestrip.crop((45*i, 0, 45+45*i, 75)))
            self.sprite.append(sprite)
    def control(self, x, y):
        self.moveX += x
        self.moveY += y

    def update(self):
        if self.move
