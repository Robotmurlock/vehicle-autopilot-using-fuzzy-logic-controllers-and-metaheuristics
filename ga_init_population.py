import random
import numpy as np
import random

import fuzzy

ALL_FUZZY_FUNCS = {
    "left_sensor": {
        "name": "left_sensor",
        "num_of_mf_functions" : 4,
        "left_boundary": 0,
        "right_boundary": 100,
        "mf_names": ["close", "midrange", "far", "very_far"],
        "is_input": True,
        "left_pos_in_chromosome": 0,
        "right_pos_in_chromosome": 4,
    },
    "right_sensor": {
        "name": "right_sensor",
        "num_of_mf_functions" : 4,
        "left_boundary": 0,
        "right_boundary": 100,
        "mf_names": ["close", "midrange", "far", "very_far"],
        "is_input": True,
        "left_pos_in_chromosome": 4,
        "right_pos_in_chromosome": 8,
    },
    "front_sensor": {
        "name": "front_sensor",
        "num_of_mf_functions" : 3,
        "left_boundary": 0,
        "right_boundary": 20,
        "mf_names": ["close", "midrange", "far"],
        "is_input": True,
        "left_pos_in_chromosome": 8,
        "right_pos_in_chromosome": 11,
    },
    "velocity": {
        "name": "velocity",
        "num_of_mf_functions" : 3,
        "left_boundary": 0,
        "right_boundary": 10,
        "mf_names": ["low", "middle", "high"],
        "is_input": False
    },
    "angle": {
        "name": "angle",
        "num_of_mf_functions" : 3,
        "left_boundary": -45,
        "right_boundary": 45,
        "mf_names": ["left", "forward", "right"],
        "is_input": False
    }
}

NUM_OF_ALL_MF_FUNCTIONS = 4 + 4 + 3 + 3 + 3

def generate_valid_boundaries(left_boundary, right_boundary):
    bounds = random.sample(range(left_boundary, right_boundary), 2)
    bounds.sort()

    left, right = bounds
    return left, right

def generate_function(left_boundary, right_boundary):
    print("generate_function...")

    xs = random.sample(range(left_boundary, right_boundary), 4)
    xs.sort()
    return xs

def generate_code_for_all_fuzzy_functions():
    
    code = []

    for keys in ALL_FUZZY_FUNCS:  
        print("current ff: " , keys)      
        
        ff = ALL_FUZZY_FUNCS[keys]
        single_function_code = []
        for i in range(ff["num_of_mf_functions"]):
            code.append(generate_function(ff["left_boundary"], ff["right_boundary"]))
    
    return code


def build_chromosome():
    chromosome = generate_code_for_all_fuzzy_functions()

def build_single_fuzzy_io(mf_trapezoids, ff):
    
    mfs = []
    current_name = 0
    for i in range(ff["left_pos_in_chromosome"], ff["right_pos_in_chromosome"]):
        xs = mf_trapezoids[i]
        ys = [0, 1, 1, 0]
        
        
        if i == ff["left_pos_in_chromosome"]:
            xs = mf_trapezoids[i][2], mf_trapezoids[i][3]
            ys = [1, 0]
        
        if i == ff["right_pos_in_chromosome"]-1:
            xs = mf_trapezoids[i][0], mf_trapezoids[i][1]
            ys = [0, 1]

        if ff["is_input"]:
            mfs.append(fuzzy.MFInput(ff["mf_names"][current_name], np.array(xs), np.array(ys)))
        else:
            mfs.append(fuzzy.MFOutput(ff["mf_names"][current_name], np.array(xs), np.array(ys)))
    
        current_name += 1
    
    if ff["is_input"]:
        return fuzzy.FuzzyInput(ff["name"], np.array(mfs))
    else:
        return fuzzy.FuzzyOutput(ff["name"], np.array(mfs))


if __name__ == "__main__":
    mf_trapezoids = generate_code_for_all_fuzzy_functions()
    ff = ALL_FUZZY_FUNCS["left_sensor"]
    single_fuzzy_io = build_single_fuzzy_io(mf_trapezoids, ff)
    print(single_fuzzy_io.__str__())


