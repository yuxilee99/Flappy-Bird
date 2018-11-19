import pygame
from Bird import Bird
from pygamegame import PygameGame
import random

class Game(PygameGame):
    def init(self):
        #load background for game
        self.display = pygame.display.set_mode((self.width,self.height))
        self.background = pygame.image.load("images/background.png")
        self.win = pygame.display.set_mode((288,522))
        
        #load bird
        Bird.init()
        bird = Bird(self.width/4, self.height/2)
        self.bird = pygame.sprite.GroupSingle(bird)   
        #load pipes
        
    def keyPressed(self, code, mod):
        pass
        
    def timerFired(self, dt):
        self.bird.update(self.isKeyPressed, self.width, self.height)

    def redrawAll(self, screen):
        #load background
        background = pygame.transform.scale(self.background,(288,522))
        self.win.blit(background, (0,0))
        
        #draw bird
        self.bird.draw(screen)
        
        
Game(288, 522).run()
