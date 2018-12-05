from neuralnetwork import NeuralNetwork

input = [[0,0],[0,1],[1,0],[1,1]]
output = [[0],[1],[1],[0]]
n = NeuralNetwork(2,2,1)

for i in range(10000):
    for j in range(len(input)):
        n.train(input[j], output[j])

print('hi')

for x in range(len(input)):
    print(n.feedForward(input[x]))