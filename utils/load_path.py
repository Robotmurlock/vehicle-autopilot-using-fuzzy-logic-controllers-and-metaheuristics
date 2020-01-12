import numpy as np
from utils import constants
import pickle
import os

def load_sin_params():
    
    current_dir = os.path.dirname(os.curdir)
    path_matrix_path = os.path.join(current_dir, constants.MATRICES_DIR, constants.PATH_MATRIX_SIN)
    screen_matrix_path = os.path.join(current_dir, constants.MATRICES_DIR, constants.SCREEN_MATRIX_SIN)

    with open(path_matrix_path, 'rb') as f:
        path_matrix = pickle.load(f)

    screen_matrix = np.loadtxt(screen_matrix_path).astype(int)

    return path_matrix, screen_matrix

def load_convex_params():    
    current_dir = os.path.dirname(os.curdir)
    path_matrix_path = os.path.join(current_dir, constants.MATRICES_DIR, constants.PATH_MATRIX_CONVEX)
    screen_matrix_path = os.path.join(current_dir, constants.MATRICES_DIR, constants.SCREEN_MATRIX_CONVEX)

    with open(path_matrix_path, 'rb') as f:
        path_matrix = pickle.load(f)

    screen_matrix = np.loadtxt(screen_matrix_path).astype(int)

    return path_matrix, screen_matrix
