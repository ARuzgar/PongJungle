import pygame

class Ball:
    VEL = 5
    COLOR = (255, 255, 255)

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.VEL
        self.y_vel = 0
        self.winner = -1

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self, direction):
        self.x = self.original_x
        self.y = self.original_y
        self.VEL = 5
        if direction == "left":
            self.x_vel = self.VEL
            self.y_vel = 0
        elif direction == "right":
            self.x_vel = -self.VEL
            self.y_vel = 0
        elif direction == "up":
            self.x_vel = 0
            self.y_vel = self.VEL
        elif direction == "down":
            self.x_vel = 0
            self.y_vel = -self.VEL