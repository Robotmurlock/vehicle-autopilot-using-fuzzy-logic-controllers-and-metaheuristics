import numpy as np
import random


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

def generate_function(left_boundary, right_boundary):
    return generate_trapezoidal_function(left_boundary, right_boundary)

def generate_trapezoidal_function(left_boundary, right_boundary):
    print("generate_trapezoidal_function...")

    xs = random.sample(range(left_boundary, right_boundary), 4)
    xs.sort()
    return xs

if __name__ == "__main__":
    print(generate_function(-30, 30))