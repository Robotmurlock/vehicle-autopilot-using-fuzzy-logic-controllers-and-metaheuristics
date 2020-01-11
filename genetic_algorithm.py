import fz_fuzzy_generator
from generator_functions import path_generator
import game
import numpy as np
import copy
import random
import simulation
from utils import load_path as lp
from utils import constants
import os
from game import Game

path, path_is_closed = path_generator.generate_sin_path()

def swap(a, b):
    tmp = a
    a = b
    b = tmp

ROAD_MATRIX = lp.load_path()
TOURNAMENT_SIZE = 10
POPULATION_SIZE = 100
MAX_ITERATIONS = 10

memory = {}

class Chromosome:
    def __init__(self):
        self.FSAngle, self.FSVelocity = fz_fuzzy_generator.build_random_fuzzy_system()
        self.fitness = self.get_fitness()
        

    def get_fitness(self):
        # return game.simulate(path, path_is_closed, self.FSAngle, self.FSVelocity)
        return simulation.run(self.FSAngle, self.FSVelocity, ROAD_MATRIX, memory)
    def update_fitness(self):
        self.fitness = self.get_fitness()

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __str__(self):
        return 'fitness: ' + str(self.fitness)

    def save(self, filename):
        file = open(filename, 'w')
        file.write(str(self.FSAngle))
        file.write(str(self.FSVelocity))

def init_population(size): 
    population = []
    for i in range(size):
        population.append(Chromosome())
    return np.array(population)

def get_best_chromosome(population):
    result = None
    for chromosome in population:
        if result == None or chromosome < result:
            result = copy.deepcopy(chromosome)
    return result

def create_group(population, group_size = TOURNAMENT_SIZE):
    ids = random.sample(range(0, population.size), group_size)
    return population[ids]

def select(population):
    # tournament selection
    group = create_group(population)
    result = group[0]
    for i in range(1, group.size):
        if group[i] < result:
            result = group[i]
    return result

def crossover(p1, p2):
    c1 = copy.deepcopy(p1)
    c2 = copy.deepcopy(p2)
    for i in range(c1.FSAngle.inputs.size):
        for j in range(c1.FSAngle.inputs[i].inputs.size):
            r = random.random()
            if r < 0.5:
                swap(c1.FSAngle.inputs[i].inputs[j], c2.FSAngle.inputs[i].inputs[j])

    for i in range(c1.FSVelocity.inputs.size):
        for j in range(c1.FSVelocity.inputs[i].inputs.size):
            r = random.random()
            if r < 0.5:
                swap(c1.FSVelocity.inputs[i].inputs[j], c2.FSAngle.inputs[i].inputs[j])
                
    return c1, c2

def mutate(c, mutation_rate = 0.01):
    for i in range(c.FSAngle.inputs.size):
        for j in range(c.FSAngle.inputs[i].inputs.size):
            for k in range(c.FSAngle.inputs[i].inputs[j].size):
                r = random.random()
                if r < mutation_rate:
                    c.FSAngle.inputs[i].inputs[j].points[k][0] = c.FSAngle.inputs[i].inputs[j].points[k][0] + random.randint(-2, 2)
    return c
                
def run_game(result):
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % constants.SCREEN_POSITION
    game = Game(path, path_is_closed)
    game.run(result.FSAngle, result.FSVelocity)


def optimize(size = POPULATION_SIZE, max_iteration = MAX_ITERATIONS):
    print("optimize...")
    population = init_population(size)
    
    for iteration in range(max_iteration):
        print('current iteration: ', iteration)
        new_population = []
        for i in range(size//2):
            p1 = select(population)
            p2 = select(population)
            c1, c2 = crossover(p1, p2)
            c1 = mutate(c1)
            c2 = mutate(c2)
            c1.update_fitness()
            c2.update_fitness()
            new_population.append(c1)
            new_population.append(c2)
        population = np.array(new_population)
    result = get_best_chromosome(population)
    result.save('result.txt')

    run_game(result)

if __name__ == '__main__':
    optimize()