from fuzzy import fuzzy_generator
from generator_functions import path_generator
import game
import numpy as np
import copy
import random

path, path_is_closed = path_generator.generate_sin_path()

def swap(a, b):
    tmp = a
    a = b
    b = tmp

class Chromosome:
    def __init__(self):
        self.FSAngle, self.FSVelocity = fuzzy_generator.build_random_fuzzy_system()
        self.fitness = self.get_fitness()

    def get_fitness(self):
        return game.simulate(path, path_is_closed, self.FSAngle, self.FSVelocity)

    def update_fitness(self):
        self.fitness = self.get_fitness()

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __str__(self):
        return 'fitness: ' + str(self.fitness)

def init_population(size):
    return np.array([Chromosome() for i in range(size)])

def get_best_chromosome(population):
    result = None
    for chromosome in population:
        if result == None or chromosome < result:
            result = copy.deepcopy(chromosome)
    return result

def create_group(population, group_size = 3):
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

def optimize(size = 10, max_iteration = 5):
    population = init_population(size)
    for iteration in range(max_iteration):
        new_population = []
        for i in range(size//2):
            p1 = select(population)
            p2 = select(population)
            c1, c2 = crossover(p1, p2)
            c1.update_fitness()
            c2.update_fitness()
            new_population.append(c1)
            new_population.append(c2)
        population = np.array(new_population)
    print('DONE')
    x = None
    input(x)
    result = get_best_chromosome(population)
    print(result)
    result.update_fitness()
            

if __name__ == '__main__':
    optimize()