import numpy as np
import random



def generate_function(left_boundary, right_boundary):
    if random.random() > 0.5:
        return generate_trapezoidal_function(left_boundary, right_boundary)
    else:
        return generate_triangluar_function(left_boundary, right_boundary)


def generate_trapezoidal_function(left_boundary, right_boundary):
    print("generate_trapezoidal_function...")

    ys = np.array([0, 1, 1, 0])
    xs = np.array(random.sample(range(left_boundary, right_boundary), ys.shape[0]))
    xs = np.sort(xs)
    return xs, ys

def generate_triangluar_function(left_boundary, right_boundary):
    print("generate_triangluar_function...")

    ys = np.array([0, 1, 0])
    xs = np.array(random.sample(range(left_boundary, right_boundary), ys.shape[0]))
    xs = np.sort(xs)
    return xs, ys

if __name__ == "__main__":
    print(generate_trapezoidal_function(-30, 30))
    print(generate_triangluar_function(-30, 30))