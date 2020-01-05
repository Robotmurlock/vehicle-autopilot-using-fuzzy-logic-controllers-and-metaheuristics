import numpy as np
import random

def generate_function(left_boundary, right_boundary):
    return generate_trapezoidal_function(left_boundary, right_boundary)

def generate_trapezoidal_function(left_boundary, right_boundary):
    print("generate_trapezoidal_function...")

    xs = random.sample(range(left_boundary, right_boundary), 4)
    xs.sort()
    return xs

def generate_triangluar_function(left_boundary, right_boundary):
    print("generate_triangluar_function...")

    xs = random.sample(range(left_boundary, right_boundary), 3)#? -1 because of the triangluar function
    xs.insert(4, xs[2]) #? we need 2 same values for the two y=1 values in order to emulate a triangle 
    xs.sort()
    return xs

if __name__ == "__main__":
    print(generate_function(-30, 30))