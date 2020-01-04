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


def generate_valid_boundaries(far_left, far_right):
    bounds = random.sample(range(far_left, far_right), 2)
    bounds.sort()

    left, right = bounds
    return left, right

def generate_code_for_single_function(far_left, far_right):
    code = []
    left_boundary, right_boundary = generate_valid_boundaries(far_left, far_right)

    (xs, ys), is_trapezoidal = fuzzy_mf_generator.generate_function(left_boundary, right_boundary)

    if is_trapezoidal:
        code += [0]
    else:
        code += [1]

    code += [left_boundary, right_boundary]
    code += xs.tolist()
    code += ys.tolist()
    return code
def generate_left_sensor_code():
    num_of_mf_functions = 4
    far_left = 0
    far_right = 100

    code = []
    for i in range(num_of_mf_functions):
        code += generate_code_for_single_function(far_left, far_right)
    return code

def build_chromosome():
    left_sensor_code = generate_left_sensor_code()

if __name__ == "__main__":
    print(generate_left_sensor_code())



