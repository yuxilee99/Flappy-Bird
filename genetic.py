#genetic algorithm functions used to find the best AI bird

from Bird import Bird
import random
from trainbird import TrainBird
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
def pick(bird, width, height, i, rate):
    index = 0
    randNum = random.uniform(0,1)
    while randNum > 0:
        randNum -= bird[index].fitness
        index += 1
    index -= 1
    pickBird = bird[index]
    newBird = TrainBird(width, height, pickBird.network) 
    newBird.network.mutate(rate)
    return newBird
 
#create next generation of birds    
def nextGeneration(bird, width, height, total, rate):
    calcFitness(bird)
    birds = []
    for i in range(total):
        birds += [pick(bird, width, height, i, rate)]
    bird = []
    return birds
        