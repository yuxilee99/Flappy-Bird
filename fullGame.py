#used template provided from Pygame PPT, by Lukas Peraza
#flappy bird game that combines all the features: AI, easy, hard, play original game, teach AI how to play
import pygame
import random
import sys 
from easyBird import EasyBird
from hardBird import BestBird
from Bird import Bird 
from trainbird import TrainBird
from genetic import *

class PygameGame(object):
    def init(self, bird = None, train = None, learn = None, birds = None, generation = None, allBirds = None, genetic = None, total = None, rate = None):
        self.gameover = pygame.image.load("images/gameover.png")
        self.startPage = pygame.image.load("images/message.png")
        self.tap = pygame.image.load("images/tap.png")
        self.ready = pygame.image.load("images/ready.png")
        self.score = 0
        self.overCount = 0
        
        #gamepages
        if train != None:
            self.start = False
            self.train = True
        else:
            self.start = True
            self.train = False
        self.over = False
        self.play = False
        self.easy = False
        self.hard = False
        self.ai = False
        if genetic != None:
            self.start = False
            self.genetic = True
        else:
            if train == None:
                self.start = True
                self.genetic = False
            else:
                self.start = False
                self.genetic = False
        
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
        
        #for train
        self.flapped = False
        if learn != None:
            self.learn = learn
        else:
            self.learn = True
        
        #for hard, easy
        self.playerbird = Bird(self.width, self.height)
        self.birdOver = False

        #load bird
        if bird == None:
            self.trainbird = TrainBird(self.width, self.height)
        else:
            self.trainbird = bird
        
        self.bird = Bird(self.width, self.height)
        self.easybird = EasyBird(self.width, self.height)
        self.hardbird = BestBird(self.width, self.height)
        self.bird = Bird(self.width, self.height)
        
        #for genetic
        if generation != None:
            self.generation = generation
        else:
            self.generation = 0
        
        if total != None:
            self.total = total
        else:
            self.total = 100
        if rate != None:
            self.rate = rate
        else:
            self.rate = 0.2
        self.input = False
        self.totalB = False
        self.rateB = False
        
        if birds != None:
            self.birds = birds
        else:
            self.birds = []
            for i in range(self.total):
                self.birds += [TrainBird(self.width, self.height)]
        
        if allBirds != None:
            self.allBirds = allBirds
        else:
            self.allBirds = []
        
        self.change = False
        self.num = ""
        self.dotcount = 0
        
    def mousePressed(self, x, y):
        if self.start:
            if self.input == False:
                if (95 < x < 185) and (90 < y < 125):
                    self.start = False
                    self.play = True
                    self.birdy = 0
                if (84 < x < 190) and (140 < y < 175):
                    self.start = False
                    self.train = True
                    self.birdy = 0
                if (95 < x < 190) and (190 < y < 275):
                    self.start = False
                    self.easy = True
                    self.birdy = 0
                if (94 < x < 190) and (240 < y < 275):
                    self.start = False
                    self.hard = True
                    self.easy = False
                    self.birdy = 0
                if (120 < x < 155) and (290 < y < 330):
                    self.ai = True
                    self.start = False
                if (65 < x < 220) and (341 < y < 375):
                    self.input = True
        if self.input:
            if (70 < x < 220) and (400 < y < 445):
                self.input = False
                self.genetic = True
                self.start = False
            if (35 < x < 240) and (45 < y < 75):
                self.totalB = True
            if (45 < x < 240) and (160 < y < 185):
                self.rateB = True
                
    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass
         
    def keyReleased(self, keyCode, modifier):
        pass

    def keyPressed(self, keyCode, modifier):
        if keyCode == pygame.K_SPACE:
            if self.train:
                if self.learn == True:
                    self.trainbird.flap()
                    self.flapped = True
            else:
                self.bird.flap()
                self.playerbird.flap()
        if keyCode == 114:
            self.init()
        if self.train:
            if keyCode == 108:
                self.learn = not self.learn
        if self.input:
            if self.totalB:
                if 47 < int(keyCode) < 58:
                    if self.change:
                        self.num += chr(keyCode)
                    else:
                        self.num = ""
                        self.num += chr(keyCode)
                        self.change = True
                if keyCode == 13:
                    try:
                        self.change = False
                        self.total = int(self.num)
                        self.num = ""
                        self.totalB = False
                    except:
                        self.change = False
                        self.num = ""
                        self.totalB = False
            if self.rateB:
                if (47 < int(keyCode) < 58) or keyCode == 46:
                    if self.change:
                        if keyCode == 46:
                           self.dotcount += 1 
                        if self.dotcount < 2:
                            self.num += chr(keyCode)
                    else:
                        self.num = ""
                        self.num += chr(keyCode)
                        self.change = True
                if keyCode == 13:
                    self.dotcount = 0
                    if 0 <= float(self.num) <= 1:
                        try:
                            self.rate = float(self.num)
                            self.num = ""
                            self.change = False
                            self.rateB = False
                        except:
                            self.num = ""
                            self.change = False
                            self.rateB = False
                    else:
                        self.num = ""
                        self.change = False
                        self.rateB = False
        
    def timerFired(self, dt):
        if self.start:
            self.bird.velocity += self.bird.gravity
            self.bird.velocity *= 0.9
            self.bird.birdy += self.bird.velocity
            self.bird.birdImage = 0
            if self.bird.birdy > 430:
                self.bird.birdy = 430
                self.bird.velocity = 0
            elif self.bird.birdy < 0:
                self.bird.birdy = 0
                self.bird.velocity = 0
        else:
            if self.over == False:
                self.time += 1
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
                
                if self.play:    
                    #move bird
                    self.bird.update()
                        
                    #hit pipe & add score
                    for pipe in self.pipe:
                        if pipe[0][0] - self.bird.birdRadius < self.bird.birdx < pipe[0][0] + self.pipeWidth:
                            if (self.bird.birdy < pipe[0][1] + self.pipeHeight) or (self.bird.birdy + self.bird.birdRadiusY > pipe[1][1]):
                                self.over = True
                        if pipe[0][0] == self.bird.birdx:
                            self.score += 1
                if self.train:
                    #move bird
                    self.trainbird.update()
                    
                    #train neural network
                    if self.learn == True:
                        if self.flapped == True:
                            target = random.uniform(0.5, 0.504)
                            self.flaptime = 0
                        else:
                            if len(self.pipe) == 0:
                                target = random.uniform(0.425, 0.4299)
                            else:
                                target = random.uniform(0.49, 0.4999999)
                        self.trainbird.learn(self.pipe, target)
                        self.flapped = False
                    else:
                        self.trainbird.think(self.pipe)
                        
                    #hit pipe & add score
                    for pipe in self.pipe:
                        if pipe[0][0] - self.trainbird.birdRadius < self.trainbird.birdx < pipe[0][0] + self.pipeWidth:
                            if (self.trainbird.birdy < pipe[0][1] + self.pipeHeight) or (self.trainbird.birdy + self.trainbird.birdRadiusY > pipe[1][1]):
                                PygameGame.init(self, self.trainbird, True, self.learn) 
                        if pipe[0][0] == self.trainbird.birdx:
                            self.score += 1
                if self.easy:
                    #move bird
                    self.playerbird.update()
                    
                    if self.birdOver == False:
                        self.easybird.update()
                        self.easybird.think(self.pipe)
                    else:
                        self.easybird.birdy += 10
                        if self.easybird.birdy > self.height:
                            self.easybird.birdy = self.height
                            self.easybird.velocity = 0
                    
                    #hit pipe & add score
                    for pipe in self.pipe:
                        if pipe[0][0] - self.easybird.birdRadius < self.easybird.birdx < pipe[0][0] + self.pipeWidth:
                            if (self.easybird.birdy < pipe[0][1] + self.pipeHeight) or (self.easybird.birdy + self.easybird.birdRadiusY > pipe[1][1]):
                                self.birdOver = True
                            if (self.playerbird.birdy < pipe[0][1] + self.pipeHeight) or (self.playerbird.birdy + self.playerbird.birdRadiusY > pipe[1][1]):
                                self.over = True
                        if pipe[0][0] == self.playerbird.birdx:
                            self.score += 1
                if self.hard:
                    #move bird
                    self.playerbird.update()
                    
                    if self.birdOver == False:
                        self.hardbird.update()
                        self.hardbird.think(self.pipe)
                    else:
                        self.hardbird.birdy += 10
                        if self.hardbird.birdy > self.height:
                            self.hardbird.birdy = self.height
                            self.hardbird.velocity = 0
                    
                    #hit pipe & add score
                    for pipe in self.pipe:
                        if pipe[0][0] - self.hardbird.birdRadius < self.hardbird.birdx < pipe[0][0] + self.pipeWidth:
                            if (self.hardbird.birdy < pipe[0][1] + self.pipeHeight) or (self.hardbird.birdy + self.hardbird.birdRadiusY > pipe[1][1]):
                                self.birdOver = True
                            if (self.playerbird.birdy < pipe[0][1] + self.pipeHeight) or (self.playerbird.birdy + self.playerbird.birdRadiusY > pipe[1][1]):
                                self.over = True
                        if pipe[0][0] == self.playerbird.birdx:
                            self.score += 1
                if self.ai:
                    #move bird
                    self.hardbird.update()
                    
                    #neural network
                    self.hardbird.think(self.pipe)
                    
                    #hit pipe & add score
                    for pipe in self.pipe:
                        if pipe[0][0] - self.hardbird.birdRadius < self.hardbird.birdx < pipe[0][0] + self.pipeWidth:
                            if (self.hardbird.birdy < pipe[0][1] + self.pipeHeight) or (self.hardbird.birdy + self.hardbird.birdRadiusY > pipe[1][1]):
                                self.birdOver = True
                        if pipe[0][0] == self.hardbird.birdx:
                            self.score += 1
                if self.genetic:
                    for bird in self.birds:
                        #move bird
                        bird.update()
                        
                        #neural network
                        bird.think(self.pipe)
                        
                    #hit pipe & add score
                    for bird in self.birds:
                        for pipe in self.pipe:
                            if (bird.birdy < pipe[0][1] + self.pipeHeight) or (bird.birdy + bird.birdRadiusY > pipe[1][1]):
                                if pipe[0][0] - bird.birdRadius < bird.birdx < pipe[0][0] + self.pipeWidth:
                                    bird.score -= (abs(bird.birdy - (pipe[0][1] + self.pipeHeight + self.gap/2)))/4
                                    self.allBirds += [bird]
                                    self.birds.remove(bird)
                                    break
                            if self.birds[0] == bird:
                                if (pipe[0][0] + self.pipeWidth) == (bird.birdx + bird.birdRadius):
                                    self.score += 1
                                    bird.gameScore += 1
                                    bird.score += 150
                    if len(self.birds) == 0:
                        self.birds = nextGeneration(self.allBirds, self.width, self.height, self.total, self.rate)
                        self.generation += 1
                        PygameGame.init(self, None, None, None, self.birds, self.generation, self.allBirds, True, self.total, self.rate) 
            else:
                self.overCount += 1
                if self.play:
                    self.bird.birdy += 10
                    if self.bird.birdy > self.height:
                        self.bird.birdy = self.height
                        self.bird.velocity = 0
                if self.easy or self.hard:        
                    self.playerbird.birdy += 10
                    if self.playerbird.birdy > self.height:
                        self.playerbird.birdy = self.height
                        self.playerbird.velocity = 0
                if self.ai:
                    self.hardbird.birdy += 10
                    if self.hardbird.birdy > self.height:
                        self.hardbird.birdy = self.height
                        self.hardbird.velocity = 0
                if self.overCount == 100:
                    self.start = True
                    self.play = False
                    self.easy = False
                    self.hard = False
                    self.ai = False
                    self.genetic = False
                    self.over = False
                    self.init()
                
    def redrawAll(self, screen):
        self.win.blit(self.background, (0,0))
        if self.start == False:
            #draw pipes
            for pipe in self.pipe:
                self.win.blit(self.topPipe, pipe[0])
                self.win.blit(self.bottomPipe, pipe[1])
            
            #draw score
            myfont = pygame.font.SysFont('04B_19', 60)
            textsurface = myfont.render(str(int(self.score)), False, (255, 255, 255))
            if len(str(self.score)) == 1:
                screen.blit(textsurface,(self.width/2 - 20, 30))
            if len(str(self.score)) == 2:
                screen.blit(textsurface,(self.width/2 - 30, 30))
            if len(str(self.score)) == 3:
                screen.blit(textsurface,(self.width/2 - 45, 30))
            if len(str(self.score)) == 4:
                screen.blit(textsurface,(self.width/2 - 60, 30))
                
            #draw birds
            if self.play:
                self.win.blit(self.bird.birds[self.bird.birdImage], (self.bird.birdx, self.bird.birdy))
            if self.train:
                myfont = pygame.font.SysFont('04B_19', 14)
                textsurface = myfont.render("Press \"r\" to return to the start page", False, (92, 64, 51))
                screen.blit(textsurface,(5, 480))
                textsurface = myfont.render("Press \"l\" to switch modes", False, (92, 64, 51))
                screen.blit(textsurface,(50, 10))
                self.win.blit(self.trainbird.birds[self.trainbird.birdImage], (self.trainbird.birdx, self.trainbird.birdy))
            if self.easy:
                self.win.blit(self.easybird.birds[self.easybird.birdImage], (self.easybird.birdx, self.easybird.birdy))
                self.win.blit(self.playerbird.birds[self.playerbird.birdImage], (self.playerbird.birdx, self.playerbird.birdy))
            if self.hard:
                self.win.blit(self.hardbird.birds[self.hardbird.birdImage], (self.hardbird.birdx, self.hardbird.birdy))
                self.win.blit(self.playerbird.birds[self.playerbird.birdImage], (self.playerbird.birdx, self.playerbird.birdy))
            if self.ai:
                self.win.blit(self.hardbird.birds[self.hardbird.birdImage], (self.hardbird.birdx, self.hardbird.birdy))
                myfont = pygame.font.SysFont('04B_19', 14)
                textsurface = myfont.render("Press \"r\" to return to the start page", False, (92, 64, 51))
                screen.blit(textsurface,(5, 480))
            if self.genetic:
                myfont = pygame.font.SysFont('04B_19', 14)
                textsurface = myfont.render("Press \"r\" to return to the start page", False, (92, 64, 51))
                screen.blit(textsurface,(5, 480))
                for bird in self.birds:
                    self.win.blit(bird.birds[bird.birdImage], (bird.birdx, bird.birdy))
                myfont = pygame.font.SysFont('LCD Solid', 10)
                textsurface = myfont.render("Generation " + str(int(self.generation)), False, (255, 255, 255))
                screen.blit(textsurface,(self.width/2 - 40, 10))  
            #gameover
            if self.over:
                self.win.blit(self.gameover, (self.width/6 , self.height/2))
        else:
            self.win.blit(self.startPage, (51, 30))
            self.win.blit(self.tap, (47, 210))
            myfont = pygame.font.SysFont('04B_19', 14)
            textsurface = myfont.render("Press \"r\" to return to the start page", False, (92, 64, 51))
            screen.blit(textsurface,(5, 480))
            myfont = pygame.font.SysFont('04B_19', 44)
            textsurface = myfont.render("PLAY", False, (92, 64, 51))
            screen.blit(textsurface,(self.width/2-49, 89))
            textsurface = myfont.render("TRAIN", False, (92, 64, 51))
            screen.blit(textsurface,(self.width/2-60, 139))
            textsurface = myfont.render("EASY", False, (92, 64, 51))
            screen.blit(textsurface,(self.width/2-49, 189))
            textsurface = myfont.render("HARD", False, (92, 64, 51))
            screen.blit(textsurface,(self.width/2-49, 239))
            myfont = pygame.font.SysFont('04B_19', 46)
            textsurface = myfont.render("AI", False, (92, 64, 51))
            screen.blit(textsurface,(self.width/2-25, 289))
            myfont = pygame.font.SysFont('04B_19', 43)
            textsurface = myfont.render("GENETIC", False, (92, 64, 51))
            screen.blit(textsurface,(self.width/2-80, 339))
            myfont = pygame.font.SysFont('04B_19', 40)
            textsurface = myfont.render("PLAY", False, (255, 255, 255))
            screen.blit(textsurface,(self.width/2-45, 90))
            textsurface = myfont.render("TRAIN", False, (255, 255, 255))
            screen.blit(textsurface,(self.width/2-55, 140))
            textsurface = myfont.render("EASY", False, (255, 255, 255))
            screen.blit(textsurface,(self.width/2-45, 190))
            textsurface = myfont.render("HARD", False, (255, 255, 255))
            screen.blit(textsurface,(self.width/2-45, 240))  
            textsurface = myfont.render("AI", False, (255, 255, 255))
            screen.blit(textsurface,(self.width/2-23, 290)) 
            textsurface = myfont.render("GENETIC", False, (255, 255, 255))
            screen.blit(textsurface,(self.width/2-75, 339))
            self.win.blit(self.bird.birds[1], (self.width/2 - self.bird.birdRadius/2, self.bird.birdy))
            #draw splash screen for population size and mutation rate
            if self.input:
                self.win.blit(self.background, (0,0))
                self.win.blit(self.background, (0,0))
                myfont = pygame.font.SysFont('04B_19', 25)
                textsurface = myfont.render("POPULATION SIZE:", False, (255,255,255))
                screen.blit(textsurface,(40, 50))
                textsurface = myfont.render(str(self.total), False, (255,255,255))
                screen.blit(textsurface,(120, 80))
                textsurface = myfont.render("MUTATION RATE:", False, (255,255,255))
                screen.blit(textsurface,(50, 160))
                textsurface = myfont.render(str(self.rate), False, (255,255,255))
                screen.blit(textsurface,(125, 190))
                
                myfont = pygame.font.SysFont('04B_19', 10)
                textsurface = myfont.render("Click the word to type in a new population", False, (255,255,255))
                screen.blit(textsurface,(25, 230))
                textsurface = myfont.render("or mutation rate", False, (255,255,255))
                screen.blit(textsurface,(95, 245))
                textsurface = myfont.render("Press enter once you have typed your number", False, (255,255,255))
                screen.blit(textsurface,(25, 280))
                textsurface = myfont.render("Note: mutation rate must between 0 and 1", False, (255,255,255))
                screen.blit(textsurface,(25, 295))

                
                myfont = pygame.font.SysFont('04B_19', 50)
                textsurface = myfont.render("START", False, (255,255,255))
                screen.blit(textsurface,(75, 400))

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