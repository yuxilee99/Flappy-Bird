class Matrix(object):
    
    make matrix
    scalar multiply matrix
    scalar add matrix
    element wise addition
    matrix multiply
    transpose
    use numpy
    
    
# 
# #define hyperparameters
# actions = 2 #flap, no flap
# 
# # learning rate
# gamma = 0.99
# 
# #update training over time
# initialEpsilon = 1.0
# finalEpsilon = 0.05
# 
# #how many frames to anneal epsilon
# explore = 500000
# observe = 50000
# replayMemory = 50000
# 
# #batch size
# batch = 100
# 
# #create TF graph
# def createGraph():
#     #first convlutional layer, bias vector
#     WConv1 = tf.Variable(tf.zeros([))
#     BConv2 = tf.Variable(tf.zeros())
#     
#     #second
#     WConv1 = tf.Variable(tf.zeros())
#     BConv2 = tf.Variable(tf.zeros())
#     
#     #last
#     WConv1 = tf.Variable(tf.zeros())
#     BConv2 = tf.Variable(tf.zeros())


# 
# class NeuralNetwork(object):
#     
# 
# 
# if output > 0.5:
#     flap()

# import numpy as np
# 
# # sigmoid function
# def nonlin(x,deriv=False):
#     if(deriv==True):
#         return x*(1-x)
#     return 1/(1+np.exp(-x))
#     
# # input dataset
# X = np.array([  [0,0,1],
#                 [0,1,1],
#                 [1,0,1],
#                 [1,1,1] ])
#     
# # output dataset            
# y = np.array([[0,0,1,1]]).T
# 
# # seed random numbers to make calculation
# # deterministic (just a good practice)
# np.random.seed(1)
# 
# # initialize weights randomly with mean 0
# syn0 = 2*np.random.random((3,1)) - 1
# 
# for iter in range(10000):
# 
#     # forward propagation
#     l0 = X
#     l1 = nonlin(np.dot(l0,syn0))
# 
#     # how much did we miss?
#     l1_error = y - l1
# 
#     # multiply how much we missed by the 
#     # slope of the sigmoid at the values in l1
#     l1_delta = l1_error * nonlin(l1,True)
# 
#     # update weights
#     syn0 += np.dot(l0.T,l1_delta)
# 
# print ("Output After Training:")
# print (l1)


# class NeuralNetwork(object):
#     def __init__(self):
#         #parameters
#         self.inputSize = 2
#         self.outputSize = 1
#         self.hiddenSize = 6
#         
#     def sigmoid(x):
#         return 1/(1+np.exp(-x))
#     
#     def sigmoidDerivative(x):
#         return x*(1-x)

#parameters
# input = 2
# output = 1
# hidden = 6
# 
# X = tf.placeHolder(tf.float32)
# Y = tf.placeHOlder(tf.float32)
# 
# #weights
# W1 = tf.Variable(tf.random_uniform([input, hidden], -1, 1))
# W2 = tf.Variable(tf.random_uniform([hidden, output], -1, 1))
# 
# #bias
# B1 = tf.Variable(tf.zeros([hidden]), name = "bias1")
# B2 = tf.Variable(tf.zeros([output]), name = "bias2")    
# 
# L2 = tf.sigmoid(tf.matmul(