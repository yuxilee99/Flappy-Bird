#used template provided from Pygame PPT, by Lukas Peraza
#referenced David Shiffman, The Coding Train for logic

import pygame
import random
import copy
import sys
from Bird import Bird
from genetic import *
from neuralnetwork import NeuralNetwork
import numpy as np
       
weightsI = [[-0.00430682, 0.30090773, 0.68649782, 0.51641445, -0.12109569],
 [ 0.28453265, -0.24245107,  0.18618809,  0.46442997,  0.38037524],
 [ 0.73926177,  0.1783407,  -0.20246109,  0.17482314,  0.0184592 ],
 [-0.13875848, -0.02024739, -0.07369451, -0.02465726, -1.07647434],
 [ 0.17304342,  0.57962411,  0.60138582,  0.80238579,  0.2758194 ],
 [-1.02620264, -0.41083493,  0.96045871,  0.2598985, -0.457298  ],
 [ 0.35318073, -0.31090429, -0.82369588,  0.76708522, -0.11023456],
 [ 0.27966543,  1.19121681,  0.23814862, -0.14066213, -0.38856115]]
weightsO = [[-0.84339776, -0.46534869,  1.09074716, -0.25396256,  1.07985184, -0.34114963, 0.38659232,  0.54690692]]

biasI = [[-0.6508766 ],
 [ 0.76778626],
 [-0.85385323],
 [-1.13566269],
 [ 0.70506466],
 [-0.66044116],
 [ 0.46338748],
 [-1.28408854]]
 
biasO = [[-0.913795]]
 
network = NeuralNetwork(5, 8, 1, np.array([weightsI]), np.array([weightsO]), np.array([biasI]), np.array([biasO]))

class PygameGame(object):
    def init(self, birds = None, generation = None, allBirds = None, bestBird = None, allBestBirds = None):
        self.over = False
        self.gameover = pygame.image.load("images/gameover.png")
        self.score = 0
        
        if generation != None:
            self.generation = generation
        else:
            self.generation = 0
        
        #load background for game
        self.display = pygame.display.set_mode((self.width,self.height))
        self.background = pygame.image.load("images/background.png")
        self.win = pygame.display.set_mode((288,500))
        
        #load pipes
        self.pipe = []
        self.topPipe = pygame.image.load('images/topPipe.png')
        self.bottomPipe = pygame.image.load('images/bottomPipe.png')
        self.gap = 120
        self.pipeHeight = 317
        self.pipeWidth = 52
        self.speed = -2
        self.time = 0
        
        self.total = 200

        if birds != None:
            self.birds = birds
        else:
            self.birds = []
            for i in range(self.total):
                self.birds += [Bird(self.width, self.height, network)]
        if allBirds != None:
            self.allBirds = allBirds
        else:
            self.allBirds = []
        
        if bestBird != None:
            self.bestBird = bestBird
        else:
            self.bestBird = None
        
        if allBestBirds != None:
            self.allBestBirds = allBestBirds
        else:
            self.allBestBirds = []
        
    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass
         
    def keyReleased(self, keyCode, modifier):
        pass

    def keyPressed(self, keyCode, modifier):
        if keyCode == 114:
            print('weightI', self.birds[0].network.weightsI)
            print('weightsO', self.birds[0].network.weightsO)
            print('biasI',self.birds[0].network.biasI)
            print('biasO',self.birds[0].network.biasO)
            input()

    def timerFired(self, dt):
        self.time += 1
        
        for bird in self.birds:
            #move bird
            bird.update()
            
            #neural network
            bird.think(self.pipe)
        
        #move pipe
        for pipe in self.pipe:
            pipe[0][0] += self.speed
            pipe[1][0] += self.speed
            if pipe[0][0] < -50 and pipe[1][0] < -50:
                self.pipe.remove(pipe)
                break
            
        #add pipe
        if self.time % 80 == 0:
            pipeX = self.width
            pipeY = random.randint(-200, -20)
            self.pipe.append([[pipeX, pipeY], [pipeX, pipeY + self.pipeHeight + self.gap]])
            
        #hit pipe & add score
        for bird in self.birds:
            for pipe in self.pipe:
                if (bird.birdy < pipe[0][1] + self.pipeHeight) or (bird.birdy + bird.birdRadiusY > pipe[1][1]):
                    if pipe[0][0] - bird.birdRadius < bird.birdx < pipe[0][0] + self.pipeWidth:
                        bird.score -= (abs(bird.birdy - (pipe[0][1] + self.pipeHeight + self.gap/2)))/4
                        # bird.score -= (abs((pipe[0][0] + self.pipeWidth) - bird.birdx))/10
                        if len(self.birds) == 1:
                            print('weightI', self.bestBird.network.weightsI)
                            print('weightsO', self.bestBird.network.weightsO)
                            print('biasI',self.bestBird.network.biasI)
                            print('biasO',self.bestBird.network.biasO)
                            print("------------------------") 
                        self.allBirds += [bird]
                        self.birds.remove(bird)
                        break
                if (pipe[0][0] + self.pipeWidth) == (bird.birdx + bird.birdRadius):
                    self.score += 1
                    bird.gameScore += 1
                    bird.score += 150
        if len(self.birds) == 1:
            tempBest = self.birds[0]
            if self.bestBird == None:
                self.bestBird = Bird(self.width, self.height, tempBest.network)
                self.allBestBirds += [Bird(self.width, self.height, tempBest.network)]
            if tempBest.gameScore > self.bestBird.gameScore:
                self.bestBird = Bird(self.width, self.width, tempBest.network)
                self.allBestBirds += [Bird(self.width, self.height, tempBest.network)]
                if tempBest.network.biasO[0] != self.bestBird.network.biasO[0]:
                    print('weightI', self.bestBird.network.weightsI)
                    print('weightsO', self.bestBird.network.weightsO)
                    print('biasI',self.bestBird.network.biasI)
                    print('biasO',self.bestBird.network.biasO)
                    print("#######################")
        elif len(self.birds) == 0:
            self.birds = nextGeneration(self.allBirds, self.width, self.height, self.total)
            self.generation += 1
            PygameGame.init(self, self.birds, self.generation, self.allBirds, self.bestBird, self.allBestBirds)   
    def redrawAll(self, screen):
        self.win.blit(self.background, (0,0))
        for pipe in self.pipe:
            self.win.blit(self.topPipe, pipe[0])
            self.win.blit(self.bottomPipe, pipe[1])
        for bird in self.birds:
            self.win.blit(bird.birds[bird.birdImage], (bird.birdx, bird.birdy))
        myfont = pygame.font.SysFont('LCD Solid', 60)
        textsurface = myfont.render(str(int(self.score)), False, (255, 255, 255))
        if len(str(self.score)) == 1:
            screen.blit(textsurface,(self.width/2 - 20, 30))
        if len(str(self.score)) == 2:
            screen.blit(textsurface,(self.width/2 - 40, 30))
        if len(str(self.score)) == 3:
            screen.blit(textsurface,(self.width/2 - 60, 30))
        if len(str(self.score)) == 4:
            screen.blit(textsurface,(self.width/2 - 80, 30))
        myfont = pygame.font.SysFont('LCD Solid', 10)
        textsurface = myfont.render("Generation " + str(int(self.generation)), False, (255, 255, 255))
        screen.blit(textsurface,(self.width/2 - 40, 10))  
        if self.over:
            self.win.blit(self.gameover, (self.width/6 , self.height/2))

    def isKeyPressed(self, key):
        return self._keys.get(key, False)

    def __init__(self, width=288, height=490, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()

    def run(self):
        pygame.font.init() 
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()
        sys.exit()


def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()