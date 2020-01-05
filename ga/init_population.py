"""
Population  follows the following rules
- left_sensor - 4 MFInput functions (close, midrange, far, very far)
    each function has codes for:
    - range
    - critical_points
    - function shape (trapezoid / triangular)

- right_sensor - 4 MFInput functions (close, midrange, far, very far)
    each function has codes for:
    - range
    - critical_points
    - function shape (trapezoid / triangular)

- front_sensor - 3 MFInput functions (close, midrange, far)
    each function has codes for:
    - range
    - critical_points
    - function shape (trapezoid / triangular)

- angle - 3 MFOutput functions (left, forward, right)
    each function has codes for:
    - range
    - critical_points
    - function shape (trapezoid / triangular)

- velocity - 3 MFOutput functions (low, middle, high)
    each function has codes for:
    - range
    - critical_points
    - function shape (trapezoid / triangular)
"""
import random
import numpy as np
import fuzzy_mf_generator


ALL_FUZZY_FUNCS = {
    "left_sensor": {
        "num_of_mf_functions" : 4,
        "left_boundary": 0,
        "right_boundary": 100
    },
    "right_sensor": {
        "num_of_mf_functions" : 4,
        "left_boundary": 0,
        "right_boundary": 100
    },
    "front_sensor": {
        "num_of_mf_functions" : 3,
        "left_boundary": 0,
        "right_boundary": 20
    },
    "velocity": {
        "num_of_mf_functions" : 3,
        "left_boundary": 0,
        "right_boundary": 10
    },
    "angle": {
        "num_of_mf_functions" : 3,
        "left_boundary": -45,
        "right_boundary": 45
    }
}
NUM_OF_ALL_MF_FUNCTIONS = 4 + 4 + 3 + 3 +3

def generate_valid_boundaries(left_boundary, right_boundary):
    bounds = random.sample(range(left_boundary, right_boundary), 2)
    bounds.sort()

    left, right = bounds
    return left, right

def generate_code_for_single_function(left_boundary, right_boundary):
    code = fuzzy_mf_generator.generate_function(left_boundary, right_boundary)
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

if __name__ == "__main__":
    print(generate_code_for_all_fuzzy_functions())



