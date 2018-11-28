#used template provided from Pygame PPT, by Lukas Peraza

import pygame
import random
import copy
import sys
from Bird import Bird
# from genetic import genetic
def calcFitness(birds):
    #get total sum of birds scores
    sum = 0
    for bird in birds:
        sum += bird.score
        
    #get fitness of birds
    for bird in birds:
        bird.fitness = bird.score/sum
    
def nextGeneration(bird, width, height):
    calcFitness(bird)
    # birds = []
    # for i in range(100):
    #     birds += [Bird(width, height)]
        
class PygameGame(object):
    def init(self):
        self.over = False
        self.gameover = pygame.image.load("images/gameover.png")
        self.score = 0
        
        #load background for game
        self.display = pygame.display.set_mode((self.width,self.height))
        self.background = pygame.image.load("images/background.png")
        self.win = pygame.display.set_mode((288,500))
        
        #load pipes
        self.pipe = []
        self.topPipe = pygame.image.load('images/topPipe.png')
        self.bottomPipe = pygame.image.load('images/bottomPipe.png')
        self.gap = 100
        self.pipeHeight = 321
        self.pipeWidth = 52
        self.speed = -2
        self.time = 0
        
        self.birds = []
        for i in range(10):
            self.birds += [Bird(self.width, self.height)]
        self.allBirds = copy.copy(self.birds)
        
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
        # if keyCode == pygame.K_SPACE:
        #     self.bird.flap()
        if keyCode == 114:
            self.init()
        pass

    def timerFired(self, dt):
        if self.over == False:
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
                pipeY = random.randint(-200, 0)
                self.pipe.append([[pipeX, pipeY], [pipeX, pipeY + self.pipeHeight + self.gap]])
                
            #hit pipe & add score
            for bird in self.birds:
                for pipe in self.pipe:
                    if pipe[0][0] - bird.birdRadius < bird.birdx < pipe[0][0] + self.pipeWidth:
                        if (bird.birdy < pipe[0][1] + self.pipeHeight) or (bird.birdy + bird.birdRadiusY > pipe[1][1]):
                            self.birds.remove(bird)
                            break
                    if pipe[0][0] == bird.birdx:
                        self.score += 1
            if len(self.birds) == 0:
                nextGeneration(self.allBirds, self.width, self.height)
                self.over = True
        else:
            for bird in self.birds:
                bird.birdy += 10
                if bird.birdy > self.height:
                    bird.birdy = self.height
                    bird.velocity = 0
                
    def redrawAll(self, screen):
        self.win.blit(self.background, (0,0))
        for pipe in self.pipe:
            self.win.blit(self.topPipe, pipe[0])
            self.win.blit(self.bottomPipe, pipe[1])
        for bird in self.birds:
            self.win.blit(bird.birds[bird.birdImage], (bird.birdx, bird.birdy))
        myfont = pygame.font.SysFont('LCD Solid', 60)
        textsurface = myfont.render(str(int(self.score)), False, (255, 255, 255))
        screen.blit(textsurface,(self.width/2 - 20, 30))  
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