#used template provided from Pygame PPT, by Lukas Peraza
import pygame
import random
import sys 
from easyBird import EasyBird
from hardBird import BestBird
from Bird import Bird 

class PygameGame(object):
    def init(self, bird = None, train = None):
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
        self.learn = True
        
        #for hard, easy
        self.playerbird = Bird(self.width, self.height)
        self.birdOver = False

        #load bird
        if bird == None:
            self.bird = Bird(self.width, self.height)
        else:
            self.bird = bird
            
        self.easybird = EasyBird(self.width, self.height)
        self.hardbird = BestBird(self.width, self.height)
        self.bird = Bird(self.width, self.height)
            
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
        if keyCode == pygame.K_SPACE:
            self.bird.flap()
            self.playerbird.flap()
        if keyCode == 114:
            self.init()
        if self.start:
            if keyCode == 112:
                self.start = False
                self.play = True
                self.birdy = 0
            if keyCode == 116:
                self.start = False
                self.train = True
                self.birdy = 0
            if keyCode == 101:
                self.start = False
                self.easy = True
                self.birdy = 0
            if keyCode == 104:
                self.start = False
                self.hard = True
                self.birdy = 0
            if keyCode == 97:
                self.ai = True
                self.start = False
                
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
                    self.bird.update()
                    
                    #train neural network
                    if self.learn == True:
                        if self.flapped == True:
                            target = random.uniform(0.5,1)
                        else:
                            target = random.uniform(0,0.49)
                        self.bird.learn(self.pipe, target)
                        self.flapped = False
                    else:
                        self.bird.think(self.pipe)
                        
                    #hit pipe & add score
                    for pipe in self.pipe:
                        if pipe[0][0] - self.bird.birdRadius < self.bird.birdx < pipe[0][0] + self.pipeWidth:
                            if (self.bird.birdy < pipe[0][1] + self.pipeHeight) or (self.bird.birdy + self.bird.birdRadiusY > pipe[1][1]):
                                self.over = True
                        if pipe[0][0] == self.bird.birdx:
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
            else:
                if self.train:
                    self.bird.birdy += 10
                    if self.bird.birdy > self.height:
                        self.bird.birdy = self.height
                        self.bird.velocity = 0
                    PygameGame.init(self, self.bird, True)
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
                        self.over = False
                        PygameGame.init(self)
                
    def redrawAll(self, screen):
        self.win.blit(self.background, (0,0))
        if self.start == False:
            #draw pipes
            for pipe in self.pipe:
                self.win.blit(self.topPipe, pipe[0])
                self.win.blit(self.bottomPipe, pipe[1])
            
            #draw birds
            if self.play:
                self.win.blit(self.bird.birds[self.bird.birdImage], (self.bird.birdx, self.bird.birdy))
            if self.train:
                myfont = pygame.font.SysFont('04B_19', 14)
                textsurface = myfont.render("Press \"r\" to return to the start page", False, (92, 64, 51))
                screen.blit(textsurface,(5, 480))
                self.win.blit(self.bird.birds[self.bird.birdImage], (self.bird.birdx, self.bird.birdy))
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
            
            #gameover
            if self.over:
                print('SUP')
                self.win.blit(self.gameover, (self.width/6 , self.height/2))
        else:
            self.win.blit(self.startPage, (51, 30))
            self.win.blit(self.tap, (47, 210))
            myfont = pygame.font.SysFont('04B_19', 15)
            textsurface = myfont.render("Press the key of the first letter", False, (92, 64, 51))
            screen.blit(textsurface,(23, 9))
            myfont = pygame.font.SysFont('04B_19', 14)
            textsurface = myfont.render("Press \"r\" to return to the start page", False, (92, 64, 51))
            screen.blit(textsurface,(5, 480))
            myfont = pygame.font.SysFont('04B_19', 44)
            textsurface = myfont.render("PLAY", False, (92, 64, 51))
            screen.blit(textsurface,(self.width/2-49, 109))
            textsurface = myfont.render("TRAIN", False, (92, 64, 51))
            screen.blit(textsurface,(self.width/2-60, 159))
            textsurface = myfont.render("EASY", False, (92, 64, 51))
            screen.blit(textsurface,(self.width/2-49, 209))
            textsurface = myfont.render("HARD", False, (92, 64, 51))
            screen.blit(textsurface,(self.width/2-49, 259))
            myfont = pygame.font.SysFont('04B_19', 46)
            textsurface = myfont.render("AI", False, (92, 64, 51))
            screen.blit(textsurface,(self.width/2-25, 309))
            myfont = pygame.font.SysFont('04B_19', 40)
            textsurface = myfont.render("PLAY", False, (255, 255, 255))
            screen.blit(textsurface,(self.width/2-45, 110))
            textsurface = myfont.render("TRAIN", False, (255, 255, 255))
            screen.blit(textsurface,(self.width/2-55, 160))
            textsurface = myfont.render("EASY", False, (255, 255, 255))
            screen.blit(textsurface,(self.width/2-45, 210))
            textsurface = myfont.render("HARD", False, (255, 255, 255))
            screen.blit(textsurface,(self.width/2-45, 260))  
            textsurface = myfont.render("AI", False, (255, 255, 255))
            screen.blit(textsurface,(self.width/2-23, 310)) 
            self.win.blit(self.bird.birds[1], (self.width/2 - self.bird.birdRadius/2, self.bird.birdy))


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