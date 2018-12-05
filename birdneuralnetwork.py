#referenced David Shiffman, The Coding Train Neural Network video playlist to get logic of how neural network works
import numpy as np
import random
import math

class BirdNetwork(object):
    def __init__(self, input, hidden, output, weightsI, weightsO, biasI, biasO):
        self.inputNum = input
        self.hiddenNum = hidden
        self.outputNum = output
        self.weightsI = np.array([weightsI])
        self.weightsO = np.array([weightsO])
        self.biasI = np.array([biasI])
        self.biasO = np.array([biasO])
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
            