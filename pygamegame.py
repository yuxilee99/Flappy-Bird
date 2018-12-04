#used template provided from Pygame PPT, by Lukas Peraza

import pygame
import random
import sys 

class PygameGame(object):
    def init(self):
        self.over = False
        self.gameover = pygame.image.load("images/gameover.png")
        self.start = True
        self.startPage = pygame.image.load("images/message.png")
        self.score = 0
        
        #load background for game
        self.display = pygame.display.set_mode((self.width,self.height))
        self.background = pygame.image.load("images/background.png")
        self.win = pygame.display.set_mode((288,500))
        
        #load bird
        self.bird = [pygame.image.load('images/birdUp.png'), pygame.image.load('images/bird.png'), pygame.image.load('images/birdDown.png')]  
        self.birdx = self.width//4
        self.birdy = self.height//2
        self.gravity = 0.8
        self.flap = -18
        self.velocity = 0
        self.birdImage = 1
        self.birdRadius = 32
        self.birdRadiusY = 26
        
        #load pipes
        self.pipe = []
        self.topPipe = pygame.image.load('images/topPipe.png')
        self.bottomPipe = pygame.image.load('images/bottomPipe.png')
        self.gap = 100
        self.pipeHeight = 321
        self.pipeWidth = 52
        self.speed = -2
        self.time = 0
        
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
            self.velocity += self.flap 
            self.birdImage = 2
        if self.over:
            if keyCode == 114:
                self.start = True
                self.over = False
                PygameGame.init(self)
        if self.start:
            if keyCode == 115:
                self.start = False
                self.birdy = 0

    def timerFired(self, dt):
        if self.start:
            self.velocity += self.gravity
            self.velocity *= 0.9
            self.birdy += self.velocity
            self.birdImage = 0
            if self.birdy > 3*self.height/4:
                self.birdy = 3*self.height/4
                self.velocity = 0
            elif self.birdy < 0:
                self.birdy = 0
                self.velocity = 0
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
                self.velocity += self.gravity
                self.velocity *= 0.9
                self.birdy += self.velocity
                self.birdImage = 0
                if self.birdy > self.height:
                    self.birdy = self.height
                    self.velocity = 0
                elif self.birdy < 0:
                    self.birdy = 0
                    self.velocity = 0
                    
                #hit pipe & add score
                for pipe in self.pipe:
                    if pipe[0][0] - self.birdRadius < self.birdx < pipe[0][0] + self.pipeWidth:
                        if (self.birdy < pipe[0][1] + self.pipeHeight) or (self.birdy + self.birdRadiusY > pipe[1][1]):
                            self.over = True
                            # print(self.birdy, 'top', pipe[0][1] + self.pipeHeight, self.birdy + self.birdRadiusY, 'bottom',pipe[1][1])
                    if pipe[0][0] == self.birdx:
                        self.score += 1
            else:
                self.birdy += 10
                if self.birdy > self.height:
                    self.birdy = self.height
                    self.velocity = 0
                
    def redrawAll(self, screen):
        self.win.blit(self.background, (0,0))
        if self.start == False:
            for pipe in self.pipe:
                self.win.blit(self.topPipe, pipe[0])
                self.win.blit(self.bottomPipe, pipe[1])
            self.win.blit(self.bird[self.birdImage], (self.birdx, self.birdy))
            myfont = pygame.font.SysFont('LCD Solid', 60)
            textsurface = myfont.render(str(int(self.score)), False, (255, 255, 255))
            screen.blit(textsurface,(self.width/2 - 20, 30))  
            if self.over:
                self.win.blit(self.gameover, (self.width/6 , self.height/2))
        else:
            self.win.blit(self.startPage, (51, self.height/4))
            self.win.blit(self.bird[1], (self.width/2 - self.birdRadius/2, self.birdy))


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