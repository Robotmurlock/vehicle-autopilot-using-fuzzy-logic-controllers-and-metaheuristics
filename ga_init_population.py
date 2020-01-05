import random
import numpy as np
import ga_fuzzy_mf_generator

ALL_FUZZY_FUNCS = {
    "left_sensor": {
        "num_of_mf_functions" : 4,
        "left_boundary": 0,
        "right_boundary": 100,
        "mf_names": ["close", "midrange", "far"]
    },
    "right_sensor": {
        "num_of_mf_functions" : 4,
        "left_boundary": 0,
        "right_boundary": 100,
        "mf_names": ["close", "midrange", "far"]
    },
    "front_sensor": {
        "num_of_mf_functions" : 3,
        "left_boundary": 0,
        "right_boundary": 20,
        "mf_names": ["close", "midrange", "far"]
    },
    "velocity": {
        "num_of_mf_functions" : 3,
        "left_boundary": 0,
        "right_boundary": 10,
        "mf_names": ["low", "middle", "high"]
    },
    "angle": {
        "num_of_mf_functions" : 3,
        "left_boundary": -45,
        "right_boundary": 45,
        "mf_names": ["left", "forward", "right"]
    }
}

NUM_OF_ALL_MF_FUNCTIONS = 4 + 4 + 3 + 3 +3

def generate_valid_boundaries(left_boundary, right_boundary):
    bounds = random.sample(range(left_boundary, right_boundary), 2)
    bounds.sort()

    left, right = bounds
    return left, right

def generate_code_for_single_function(left_boundary, right_boundary):
    code = ga_fuzzy_mf_generator.generate_function(left_boundary, right_boundary)
    print(code)
    return code

def generate_code_for_all_fuzzy_functions():
    
    code = []

    for keys in ALL_FUZZY_FUNCS:  
        print("current ff: " , keys)      
        ff = ALL_FUZZY_FUNCS[keys]
        single_function_code = []
        for i in range(ff["num_of_mf_functions"]):
            code.append(generate_code_for_single_function(ff["left_boundary"], ff["right_boundary"]))
    
    return code


def build_chromosome():
    chromosome = generate_code_for_all_fuzzy_functions()




# TODO See how to move this to fuzzy, probably ditch the whole directories thing and use prefixes (eg. ga_init_population) or sth
def buiild_single_fuzzy_io(mf_trapezoids, is_input, mf_names):
    
    mfs = []
    for i in range(mf_trapezoids):
        xs = np.array(mf_trapezoids[i])
        ys = np.array([0, 1, 1, 0])
        
        if i == 0:
            xs = np.array(mf_trapezoids[i][3], mf_trapezoids[i][2])
            ys = np.array([1, 0])
        if i == len(mf_trapezoids):
            xs = np.array(mf_trapezoids[i][0], mf_trapezoids[i][1])
            ys = np.array([0, 1])

        mfs.append(mf_names[i], xs, ys)


if __name__ == "__main__":
    print(generate_code_for_all_fuzzy_functions())



