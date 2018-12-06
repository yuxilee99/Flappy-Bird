#referenced David Shiffman, The Coding Train Neural Network video playlist to get logic of how neural network works
#neural network for easy and hard bird AI
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
        
        print(changeWH)
        print(value)
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
            