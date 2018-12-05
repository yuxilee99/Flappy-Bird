#used template provided from Pygame PPT, by Lukas Peraza
import pygame
import random
import sys 
from neuralflappy import NetworkPygameGame
from easyBirdGameWithPlayer import EasyPygameGame
from hardBirdGameWithPlayer import HardPygameGame
from Bird import Bird 

class PygameGame(object):
    def init(self):
        self.over = False
        self.gameover = pygame.image.load("images/gameover.png")
        self.start = True
        self.startPage = pygame.image.load("images/message.png")
        self.tap = pygame.image.load("images/tap.png")
        self.ready = pygame.image.load("images/ready.png")
        self.score = 0
        self.overCount = 0
        
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
        
        #load bird
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
        if self.over:
            if keyCode == 114:
                self.start = True
                self.over = False
        if self.start:
            if keyCode == 112:
                self.start = False
                self.birdy = 0
            if keyCode == 116:
                NetworkPygameGame()
            if keyCode == 101:
                EasyPygameGame()
            if keyCode == 104:
                EasyPygameGame()

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
                    
                #move bird
                self.bird.update()
                    
                #hit pipe & add score
                for pipe in self.pipe:
                    if pipe[0][0] - self.bird.birdRadius < self.bird.birdx < pipe[0][0] + self.pipeWidth:
                        if (self.bird.birdy < pipe[0][1] + self.bird.pipeHeight) or (self.birdy + self.bird.birdRadiusY > pipe[1][1]):
                            self.over = True
                    if pipe[0][0] == self.bird.birdx:
                        self.score += 1
            else:
                self.overCount += 1
                self.bird.birdy += 10
                if self.bird.birdy > self.height:
                    self.bird.birdy = self.height
                    self.bird.velocity = 0
                if self.overCount == 100:
                    self.start = True
                    self.over = False
                    PygameGame.init(self)
                
    def redrawAll(self, screen):
        self.win.blit(self.background, (0,0))
        if self.start == False:
            for pipe in self.pipe:
                self.win.blit(self.topPipe, pipe[0])
                self.win.blit(self.bottomPipe, pipe[1])
            self.win.blit(self.bird.birds[self.bird.birdImage], (self.bird.birdx, self.bird.birdy))
            myfont = pygame.font.SysFont('04B_19', 60)
            textsurface = myfont.render(str(int(self.score)), False, (255, 255, 255))
            screen.blit(textsurface,(self.width/2 - 20, 30))  
            if self.over:
                self.win.blit(self.gameover, (self.width/6 , self.height/2))
        else:
            self.win.blit(self.startPage, (51, 30))
            self.win.blit(self.tap, (51, 210))
            myfont = pygame.font.SysFont('04B_19', 44)
            textsurface = myfont.render("PLAY", False, (92, 64, 51))
            screen.blit(textsurface,(self.width/2-49, 109))
            textsurface = myfont.render("TRAIN", False, (92, 64, 51))
            screen.blit(textsurface,(self.width/2-60, 159))
            textsurface = myfont.render("EASY", False, (92, 64, 51))
            screen.blit(textsurface,(self.width/2-49, 209))
            textsurface = myfont.render("HARD", False, (92, 64, 51))
            screen.blit(textsurface,(self.width/2-49, 259))
            myfont = pygame.font.SysFont('04B_19', 40)
            textsurface = myfont.render("PLAY", False, (255, 255, 255))
            screen.blit(textsurface,(self.width/2-45, 110))
            textsurface = myfont.render("TRAIN", False, (255, 255, 255))
            screen.blit(textsurface,(self.width/2-55, 160))
            textsurface = myfont.render("EASY", False, (255, 255, 255))
            screen.blit(textsurface,(self.width/2-45, 210))
            textsurface = myfont.render("HARD", False, (255, 255, 255))
            screen.blit(textsurface,(self.width/2-45, 260))  
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