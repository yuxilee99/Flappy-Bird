#used template provided from Pygame PPT, by Lukas Peraza
#referenced David Shiffman, The Coding Train for logic
#flappy bird program that implements genetic algorithm on populations of AI birds with distinct neural networks

import pygame
import random
import copy
import sys
from Bird import Bird
from genetic import *

        
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
        
        self.total = 100
        self.rate = 0.2
        
        if birds != None:
            self.birds = birds
        else:
            self.birds = []
            for i in range(self.total):
                self.birds += [Bird(self.width, self.height)]
        
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
            self.init()
        if keyCode == 112:
            if self.bestBird != None:
                print('weightI', self.bestBird.network.weightsI)
                print('weightsO', self.bestBird.network.weightsO)
                print('biasI',self.bestBird.network.biasI)
                print('biasO',self.bestBird.network.biasO)
                
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
            self.birds = nextGeneration(self.allBirds, self.width, self.height, self.total, self.rate)
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