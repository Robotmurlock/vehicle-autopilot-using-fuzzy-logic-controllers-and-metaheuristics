import numpy as np
from utils import constants
import pickle
import os

def load_path():
    return np.loadtxt(constants.ROAD_MATRIX_PATH).astype(int)

def load_sin_params():
    
    current_dir = os.path.dirname(os.curdir)
    print("par_dir", os.path.abspath(os.curdir))
    path_matrix_path = os.path.join(current_dir, constants.MATRICES_DIR, constants.PATH_MATRIX_SIN)
    screen_matrix_path = os.path.join(current_dir, constants.MATRICES_DIR, constants.SCREEN_MATRIX_SIN)

    with open(path_matrix_path, 'rb') as f:
        path_matrix = pickle.load(f)

    screen_matrix = np.loadtxt(screen_matrix_path).astype(int)

    print("SCREEN_MATRIX", screen_matrix.shape)

    return path_matrix, screen_matrix
