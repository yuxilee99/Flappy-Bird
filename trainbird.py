#bird class for easy AI bird

import pygame
import math
import random 
import numpy as np


weightsI = [[-0.00430682, 0.30090773, 0.68649782, 0.51641445, -0.12109569],
 [ 0.28453265, -0.24242107,  0.18618809,  0.46442997,  0.38037524],
 [ 0.73926177,  0.1783407,  -0.21248109,  0.17482314,  0.0284592 ],
 [-0.13875848, -0.02014739, -0.07369451, -0.11465726, -1.07647434],
 [ 0.17304342,  0.57922411,  0.60132582,  0.80238579,  0.2758194 ],
 [-1.02620264, -0.41083493,  0.95045871,  0.27598985, -0.457298  ],
 [ 0.35318073, -0.31090429, -0.82469588,  0.76718522, -0.11023456],
 [ 0.27966543,  1.19121681,  0.23914862, -0.14066213, -0.38856115]]
weightsO = [[-0.84339776, -0.46534869,  1.09074716, -0.25396256,  1.07985184, -0.34114963, 0.38659232,  0.54690692]]

biasI = [[-0.6508766 ],
 [ 0.75778626],
 [-0.85385323],
 [-1.13565269],
 [ 0.70506466],
 [-0.66044116],
 [ 0.46338748],
 [-1.28408854]]
 
biasO = [[-0.910795]]

#bird class
class TrainBird(object):
    def __init__(self, x, y, network = None):
        self.birds = [pygame.image.load('images/birdUp.png'), pygame.image.load('images/bird.png'), pygame.image.load('images/birdDown.png')]  
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
        
        if network != None:
            self.network = network
        else:
            self.network = TrainBirdNetwork(5, 8, 1, weightsI, weightsO, biasI, biasO)

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

    #get inputs, use neural network to get output
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
    
    #get input and target values to train birds neural network        
    def learn(self, pipes, target):
        #get closest pipe
        close = None
        distance = self.width
        for pipe in pipes:
            currD = (pipe[0][0] + self.pipeWidth) - self.birdx
            if 0 < currD < distance:
                close = pipe
                distance = currD
        
        inputs = [0, 0, 0, 0, 0]
        if close != None:
            #assign inputs
            inputs[0] = self.birdy/self.height
            inputs[1] = (close[0][1] + self.pipeHeight)/self.height
            inputs[2] = close[1][1]/self.height
            inputs[3] = close[0][0]/self.width
            inputs[4] = self.velocity/10
            
        #get output, decide to flap or not
        output = self.network.train(inputs, target)     

#genetic algorithm functions used to find the best AI bird

from Bird import Bird
import random
#referenced David Shiffman, The Coding Train to get logic of genetic algorithms

def calcFitness(birds):
    #get total sum of birds scores
    sum = 0
    for bird in birds:
        sum += bird.score
    #get fitness of birds
    for bird in birds:
        bird.fitness = bird.score/sum
        
# select birds that are most fit based on probability
# higher fitness has higher probability of getting chosen
def pick(bird, width, height, i):
    index = 0
    randNum = random.uniform(0,1)
    while randNum > 0:
        randNum -= bird[index].fitness
        index += 1
    index -= 1
    pickBird = bird[index]
    newBird = TrainBird(width, height, pickBird.network) 
    newBird.network.mutate(0.2)
    return newBird
 
#create next generation of birds    
def nextGeneration(bird, width, height, total):
    calcFitness(bird)
    birds = []
    for i in range(total):
        birds += [pick(bird, width, height, i)]
    bird = []
    return birds
        

class TrainBirdNetwork(object):
    def __init__(self, input, hidden, output, weightsI, weightsO, biasI, biasO):
        self.inputNum = input
        self.hiddenNum = hidden
        self.outputNum = output
        self.weightsI = np.array(weightsI)
        self.weightsO = np.array(weightsO)
        self.biasI = np.array(biasI)
        self.biasO = np.array(biasO)
        self.learningRate = 0.1
    
    #send inputs, multiply by weights, add bias, apply sigmoid function
    def feedForward(self, input):
        #hidden output
        inputA = np.array([input])
        inputT = inputA.T
        value = np.matmul(self.weightsI, inputT)
        value = np.add(value, self.biasI)
        
        #sigmoid function to put values between [-1, 1]
        def sigmoid(x):
            return 1 / (1 + math.exp(-x))
            
        #use numpy to be able to apply sigmoid function to every element in array
        sigmoidFunct = np.vectorize(sigmoid)
        
        #apply sigmoid function to new value
        value = sigmoidFunct(value)
        
        #final output
        final = np.matmul(self.weightsO, value)
        final = np.add(final, self.biasO)

        #apply sigmoid function to final
        output = sigmoidFunct(final)
        return output.flatten() 
    
    def train(self, input, target):
        #feedforward code, repeated to have all values while getting output network would get from input
        #hidden output
        inputA = np.array([input])
        inputT = inputA.T
        value = np.matmul(self.weightsI, inputT)
        value = np.add(value, self.biasI)
         
        #sigmoid function to put values between [-1, 1]
        def sigmoid(x):
            return 1 / (1 + math.exp(-x))
            
        #use numpy to be able to apply sigmoid function to every element in array
        sigmoidFunct = np.vectorize(sigmoid)
        
        #apply sigmoid function to new value
        value = sigmoidFunct(value)
        
        #final output
        final = np.matmul(self.weightsO, value)
        final = np.add(final, self.biasO)

        #apply sigmoid function to final
        output = sigmoidFunct(final)
        output = output.flatten()
        #end of feedforward code

        
        #make target into array
        targets = np.array([target])
        
        #calculate change in weights
        #change output weightHO = learning rate * output error * gradient * transposed hidden
        #change output weightIH = learning rate * hidden error * gradient * transposed input
        #gradient = derivative of sigmoid function on output
        
        #get error = target - output
        errorO = np.subtract(targets, output)
        
        #get derivative of sigmoid, where x is a value that already went through sigmoid funct
        def derivativeSigmoid(x):
            return x * (1 - x)
        
        #use numpy to be able to apply sigmoid function to every element in array
        dSigmoidFunct = np.vectorize(derivativeSigmoid)
        
        #get gradient by applying derivative sigmoid
        outputSigD = dSigmoidFunct(output)
        
        #multiply rest of values from change output weightHO formula
        gradientO = np.multiply(outputSigD, errorO)
        changeWH = np.multiply(gradientO, self.learningRate)
        # value = np.squeeze(value)
        # value = np.array([value])
        
        changeWH = np.matmul(changeWH, value.T)
        #change all weights by changeW
        self.weightsO = np.add(self.weightsO, changeWH)
        
        #change bias by gradient
        self.biasO = np.add(self.biasO, gradientO)
        
        #transpose weightO, get hidden error
        weightOT = self.weightsO.T
        errorOT = errorO.T
        errorOT = np.array([errorOT])
        errorH = np.matmul(weightOT, errorOT)
        
        #get hidden gradient
        hiddenD = dSigmoidFunct(value)
        gradientH = np.multiply(hiddenD, errorH)
        changeWO = np.multiply(gradientH, self.learningRate)

        #get hidden change in weight
        changeWO = np.matmul(changeWO, inputA)
        
        #change all weights by changeW
        self.weightsI = np.add(self.weightsI, changeWO)
        
        #change hidden bias by gradient
        self.biasI = np.add(self.biasI, gradientH)
        
    #accept an arbitrary function for mutation
    def mutate(self, rate):
        def mutateFunct(rate, n):
            if random.uniform(0,1) < rate:
                return n + np.random.normal(0, 0.1)
            else:
                return n
        #apply mutation to weight and bias values
        funct = np.vectorize(mutateFunct)
        self.weightsI = funct(rate, self.weightsI)
        self.weightsO = funct(rate, self.weightsO)    
        self.biasI = funct(rate, self.biasI)  
        self.biasO = funct(rate, self.biasO)  
        
    #make a copy of the neural network
    def copy(self):
        return [self.inputNum, self.hiddenNum, self.outputNum, self.weightsI, self.weightsO, self.biasI, self.biasO]