import pygame
import random
import sys

class Pipe(object):
    def __init__(self):
        self.pipe = []
        self.topPipe = pygame.image.load('images/topPipe.png')
        self.bottomPipe = pygame.image.load('images/bottomPipe.png')
        self.gap = 100
        self.pipeHeight = 321
        self.pipeWidth = 52
        self.speed = -2
        self.time = 0
        
    def add(self):
        
    def move(self):
        for pipe in self.pipe:
            pipe[0][0] += self.speed
            pipe[1][0] += self.speed
            if pipe[0][0] < -50 and pipe[1][0] < -50:
                self.pipe.remove(pipe)
                break
        