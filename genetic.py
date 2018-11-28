from Bird import Bird
from flappy import PygameGame

def calcFitness(birds):
    #get total sum of birds scores
    sum = 0
    for bird in birds:
        sum += bird.score
    
    #get fitness of birds
    for bird in birds:
        bird.fitness = bird.score/sum
        print(bird.fitness)
    
def nextGeneration():
    calcFitness()
    birds = []
    for i in range(100):
        birds += [Bird(self.width, self.height)]
        