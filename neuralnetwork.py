#referenced David Shiffman, The Coding Train Neural Network video playlist to get logic of how neural network works
import numpy as np
import random
import math

class NeuralNetwork(object):
    def __init__(self, input, hidden, output):
        self.inputNum = input
        self.hiddenNum = hidden
        self.outputNum = output
        self.weightsI = np.random.uniform(-1, 1, (self.hiddenNum, self.inputNum))
        self.weightsO = np.random.uniform(-1, 1, (self.outputNum, self.hiddenNum))
        self.biasI = np.random.uniform(-1, 1, (self.hiddenNum, 1))
        self.biasO = np.random.uniform(-1, 1, (self.outputNum, 1))
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
        newFinal = sigmoidFunct(final)
        
        return newFinal.flatten() 
    
    def train(self, input, target):
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

        #make parameters into arrays
        targets = np.array([target])

        #get error = target - output
        errorO = np.subtract(targets, output)
        
        #get gradient by finding derivative of sigmoid
        outputD = output*(1 - output)
        gradientO = np.matmul(errorO, outputD)
        change = np.multiply(self.learningRate, gradientO)
        changeW = np.matmul(change, value.T)
        
        #change all weights by changeW
        self.weightsO = np.add(self.weightsO, changeW)
        
        #change bias by gradient
        self.biasO = np.add(self.biasO, gradientO)
        
        #transpose weightO, get hidden error
        weightOT = self.weightsO.T
        errorH = np.matmul(weightOT, errorO)
        
        #get hidden gradient
        hiddenD = value*(1 - value)
        gradientH = np.matmul(errorH, hiddenD.T)
        changeWO = np.multiply(self.learningRate, gradientH)
        
        #get hidden change in weight
        changeWO = np.matmul(changeWO, inputT)
        
        #change all weights by changeW
        self.weightsI = np.add(self.weightsI, changeWO)
        
        #change hidden bias by gradient
        self.biasI = np.add(self.biasI, gradientH)
    
    #The best way to do this is to create a method that sets each attribute of one instance to equal (a copy of) each attribute in another instance.
    def copy(self):
        return NeuralNetwork(self)
        
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
