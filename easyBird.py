import pygame
import math
from birdneuralnetwork import BirdNetwork
import random 


weightsI = [[-0.00430682, 0.30090773, 0.68649782, 0.51641445, -0.12109569],
 [ 0.28453265, -0.24245107,  0.18618809,  0.46442997,  0.38037524],
 [ 0.73926177,  0.1783407,  -0.20246109,  0.17482314,  0.0184592 ],
 [-0.13875848, -0.02024739, -0.07369451, -0.01465726, -1.07647434],
 [ 0.17304342,  0.57962411,  0.60138582,  0.80238579,  0.2758194 ],
 [-1.02620264, -0.41083493,  0.95045871,  0.27598985, -0.457298  ],
 [ 0.35318073, -0.31090429, -0.82369588,  0.76708522, -0.11023456],
 [ 0.27966543,  1.19121681,  0.23814862, -0.14066213, -0.38856115]]
weightsO = [[-0.84339776, -0.46534869,  1.09074716, -0.25396256,  1.07985184, -0.34114963, 0.38659232,  0.54690692]]

biasI = [[-0.6508766 ],
 [ 0.75778626],
 [-0.85385323],
 [-1.13565269],
 [ 0.70506466],
 [-0.66044116],
 [ 0.46338748],
 [-1.28408854]]
 
biasO = [[-0.913795]]

#bird class
class EasyBird(object):
    def __init__(self, x, y, network = None):
        self.birds = [pygame.image.load('images/birdUpB.png'), pygame.image.load('images/birdB.png'), pygame.image.load('images/birdDownB.png')]  
        self.birdx = x//4
        self.birdy = y//2
        self.gravity = 0.8
        self.speed = -18
        self.velocity = 0
        self.birdImage = 1
        self.birdRadius = 32
        self.birdRadiusY = 16
        self.width = x
        self.height = y
        
        self.pipeHeight = 321
        self.pipeWidth = 52
        
        self.score = 0
        self.fitness = 0
        self.gameScore = 0
        
        self.network = BirdNetwork(5, 8, 1, weightsI, weightsO, biasI, biasO)

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
            currD = (pipe[0][0] + self.pipeWidth) - self.birdx
            if (currD < distance) and (currD > 0):
                close = pipe
                distance = currD
        
        inputs = [0, 0, 0, 0, 0]
        if close != None:
            #assign inputs
            inputs[0] = self.birdy/self.height
            inputs[1] = (close[0][1] + self.pipeHeight)/self.height
            inputs[2] = close[1][1]/self.height
            inputs[3] = close[0][0]/self.width
            inputs[4] = self.velocity
            
        #get output, decide to flap or not
        output = self.network.feedForward(inputs)
        # if (output[0] > 0.5) and (self.velocity >= 0):
        if output[0] > 0.5:
            self.flap()
            