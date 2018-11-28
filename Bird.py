import pygame
import math
from neuralnetwork import NeuralNetwork

#bird class
class Bird(object):
    def __init__(self, x, y, network = None):
        self.birds = [pygame.image.load('images/birdUp.png'), pygame.image.load('images/bird.png'), pygame.image.load('images/birdDown.png')]  
        self.birdx = x//4
        self.birdy = y//2
        self.gravity = 0.8
        self.speed = -18
        self.velocity = 0
        self.birdImage = 1
        self.birdRadius = 32
        self.birdRadiusY = 13
        self.width = x
        self.height = y
        self.pipeHeight = 321
        
        self.score = 0
        self.fitness = 0
        
        if network != None:
            self.network = network
        else:
            self.network = NeuralNetwork(4, 4, 1)

    #apply gravity to bird    
    def update(self):
        self.score += 1
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
    
    def flap(self):
        self.velocity += self.speed 
        self.birdImage = 2

    def think(self, pipes):
        #get closest pipe
        close = None
        distance = self.width
        for pipe in pipes:
            currD = pipe[0][0] - self.birdx
            if (currD < distance) and (currD > 0):
                close = pipe
                distance = currD
        
        inputs = [0, 0, 0, 0]
        if close != None:
            #assign inputs
            inputs[0] = self.birdy/self.height
            inputs[1] = (close[0][1] + self.pipeHeight)/self.height
            inputs[2] = close[1][1]/self.height
            inputs[3] = close[0][0]/self.width
          
        #get output, decide to flap or not
        output = self.network.feedForward(inputs)
        # print(inputs, output)
        if output > 0.5:
            self.flap()
        