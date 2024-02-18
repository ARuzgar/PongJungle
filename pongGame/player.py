import pygame

class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 3
        self.score = 0

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        

    def move(self, posY):
        if posY == -1:
            self.y -= self.vel
        if posY == 1:
            self.y += self.vel
        self.update()

    def move_sideways(self, posX):
        if posX == -1:
            self.x -= self.vel
        if posX == 1:
            self.x += self.vel
        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
