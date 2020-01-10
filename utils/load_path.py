import numpy as np
from utils import constants

def load_path():
    return np.loadtxt(constants.ROAD_MATRIX_PATH).astype(int)
