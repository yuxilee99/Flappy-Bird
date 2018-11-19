import pygame
import math
from GameObject import GameObject


class Bird(GameObject):
    @staticmethod
    def init():
        Bird.birdImage = pygame.image.load('images/bird.png')

    def __init__(self, x, y):
        super(Bird, self).__init__(x, y, Bird.birdImage, 30)
        self.speed = -50
        self.gravity = 50
        self.cx = x
        self.cy = y
        
    def update(self, keysDown, screenWidth, screenHeight):
        if keysDown(pygame.K_SPACE):
            self.cy += self.speed
        else:
            self.cy += self.gravity
        super(Bird, self).update(screenWidth, screenHeight)

        