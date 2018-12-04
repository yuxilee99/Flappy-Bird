#referenced David Shiffman, The Coding Train Neural Network video playlist to get logic of how neural network works
import numpy as np
import random
import math

class NeuralNetwork(object):
    def __init__(self, input, hidden, output, weightsI=None, weightsO=None, biasI=None, biasO=None):
        self.inputNum = input
        self.hiddenNum = hidden
        self.outputNum = output
        if isinstance(weightsI, np.ndarray):
            self.weightsI = np.copy(weightsI)
            self.weightsO = np.copy(weightsO)
            self.biasI = np.copy(biasI)
            self.biasO = np.copy(biasO)
        else:
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
            
    #make a copy of the neural network
    def copy(self):
        return NeuralNetwork(self.inputNum, self.hiddenNum, self.outputNum, self.weightsI, self.weightsO, self.biasI, self.biasO)
    
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
    
    def printValue(self):
        print(self.inputNum, self.hiddenNum, self.outputNum, self.weightsI, self.weightsO, self.biasI, self.biasO)
