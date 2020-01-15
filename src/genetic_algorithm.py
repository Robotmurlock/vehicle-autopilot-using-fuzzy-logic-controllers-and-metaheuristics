import fuzzy_generator
from simulation import Simulation
import numpy as np
import copy
import random
import ga_fitness
from utils import load_path as lp
from utils import constants, path_generator
import os
import pickle # Rick
import argparse

path = None
path_is_closed = None
road_matrix = None

TOURNAMENT_SIZE = 5
POPULATION_SIZE = 1000 # Must be even
ELITISM_RATIO = 0.05
MAX_ITERATIONS = 20
MUTATION_SPAN = 2
MUTATION_RATE = 0.1
MUTATION_GENOM_RATE = 0.1

def swap(a, b):
    tmp = a
    a = b
    b = tmp
    return a, b

memory = {}

class Chromosome:
    def __init__(self):
        self.FSAngle, self.FSVelocity = fuzzy_generator.build_random_fuzzy_system()
        self.fitness = self.get_fitness()
        
    def get_fitness(self):
        return ga_fitness.evaluate(self.FSAngle, self.FSVelocity, road_matrix, memory)

    def update_fitness(self):
        self.fitness = self.get_fitness()

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __str__(self):
        return 'fitness: ' + str(self.fitness)

    def save(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self.FSAngle))
            f.write(str(self.FSVelocity))
            f.write("Fitness: " + str(self.fitness))

        with open(constants.PRETRAINED_FUZZY_PATH, 'wb') as f:
            pickle.dump([self.FSAngle, self.FSVelocity], f)

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
        fuzzy_output1 = c1.FSAngle.inputs[i]
        fuzzy_output2 = c2.FSAngle.inputs[i]

        for j in range(fuzzy_output1.inputs.size):
            mf_output1 = fuzzy_output1[j]
            mf_output2 = fuzzy_output2[j]

            r = random.random()
            if r < 0.5:
                swap(mf_output1, mf_output2)

    for i in range(c1.FSVelocity.inputs.size):
        fuzzy_output1 = c1.FSVelocity.inputs[i]
        fuzzy_output2 = c2.FSVelocity.inputs[i]

        for j in range(fuzzy_output1.inputs.size):
            mf_output1 = fuzzy_output1[j]
            mf_output2 = fuzzy_output2[j]

            r = random.random()
            if r < 0.5:
                swap(mf_output1, mf_output2)
                
    return c1, c2

def mutate(c, mutation_rate = MUTATION_RATE):
    r = random.random()
    if r > mutation_rate:
        return c

    for i in range(c.FSAngle.inputs.size):
        fuzzy_input = c.FSAngle.inputs[i]
        for j in range(fuzzy_input.inputs.size):
            mf_input = fuzzy_input[j]
            for k in range(fuzzy_input.inputs[j].size):
                
                r = random.random()
                if r < MUTATION_GENOM_RATE:
                    number_of_points = int(mf_input.size)
                    right_boundary = fuzzy_generator.ALL_FUZZY_FUNCS[fuzzy_input.name]["right_boundary"]
                    left_boundary = fuzzy_generator.ALL_FUZZY_FUNCS[fuzzy_input.name]["left_boundary"]

                    shift_value = random.randint(-MUTATION_SPAN, MUTATION_SPAN)

                    if number_of_points == 2 and mf_input.points[0][1] == 1:
                        new_value = mf_input.points[0][0] + shift_value
                        mf_input.points[0][0] = min(right_boundary, new_value)

                    elif number_of_points == 2 and mf_input.points[0][1] == 0:
                        new_value = mf_input.points[1][0] + shift_value
                        mf_input.points[1][0] = max(left_boundary, new_value)

                    else:
                        left = mf_input.points[0][0] + shift_value
                        shift_value = random.randint(-MUTATION_SPAN, MUTATION_SPAN)
                        right = mf_input.points[-1][0] + shift_value

                        if left < left_boundary:
                            left = left_boundary
                        
                        if right > right_boundary:
                            right = right_boundary
                        
                        if left > right:
                            swap(left, right_boundary)

                        if abs(left - right) <= 2:
                            right += 2 

                        mid_1 = mf_input.points[1][0] + shift_value
                        shift_value = random.randint(-MUTATION_SPAN, MUTATION_SPAN)
                        mid_2 = mf_input.points[2][0] + shift_value
                        
                        if mid_1 > mid_2:
                            mid_1, mid2 = swap(mid_1, mid_2)

                        new_xs = [left, mid_1, mid_2, right]

                        for t in range(4):
                            mf_input.points[t][0] = new_xs[t]
    return c
                
def run_game(result):
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % constants.SCREEN_POSITION
    game = Simulation(path, path_is_closed)
    game.run(result.FSAngle, result.FSVelocity)


def load_initial_params(is_sin_path):
    if is_sin_path:
        path_is_closed = False
        path, road_matrix = lp.load_sin_params()
    else:
        path_is_closed = True
        path, road_matrix = lp.load_convex_params()

    return path, path_is_closed, road_matrix

def optimize(size = POPULATION_SIZE, max_iteration = MAX_ITERATIONS, elitism_ratio = ELITISM_RATIO):
    print("Starting optimization!")

    population = init_population(size)
    print('Initialized population.')
    
    for iteration in range(max_iteration):
        print('Current iteration: %3d' % iteration)
        population.sort()
        elites = int(population.size * elitism_ratio)
        new_population = [population[i] for i in range(0, elites)]

        for i in range((size-elites)//2):
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
        print('\tFitness: {}'.format(get_best_chromosome(population).fitness))

    result = get_best_chromosome(population)
    print('Finished optimization!')
    print('Best solution fitness: {}'.format(result.fitness))

    results_path = os.path.join(os.path.curdir, "results", "results.txt") 
    result.save(results_path)

    usr = input("Press any key to start the simulation")

    run_game(result)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--polygon', choices=['convex', 'sin'], help='Runs the GA on a choosen polygon', required=True)

    args = parser.parse_args()
    polygon = args.polygon

    if polygon == "convex":
        target_polygon = constants.USE_CONVEX_POLYGON
    else:
        target_polygon = constants.USE_SIN_POLYGON

    path, path_is_closed, road_matrix = load_initial_params(target_polygon)
    optimize()