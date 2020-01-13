# Taken from: https://github.com/rasmaxim/pygame-car-tutorial
import os
import random
import time
import math
import copy
import sys
import numpy as np
import pickle

import pygame
from pygame.locals import *
from pygame.math import Vector2

from utils import constants, path_generator
import utils.load_path as lp

class Game:
    def __init__(self, path, closed_polygon):
        pygame.init()
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), DOUBLEBUF)
        self.screen.set_alpha(False)
        self.path = path
        self.closed_polygon = closed_polygon

        self.screen_matrix = None

    def run(self):
        self.draw_screen()        
        pygame.quit()
        return self.screen_matrix

    def draw_screen(self):
        self.screen.fill(constants.SCREEN_COLOR)
        self.draw_path()
        self.screen_matrix = pygame.surfarray.pixels_red(self.screen).astype(int)
    
    def draw_path(self):
        if not self.closed_polygon:
            pygame.draw.polygon(self.screen, constants.PATH_COLOR, self.path)
        else:
            for i, polygon in enumerate(self.path):
                if i % 2 == 0:
                    draw_color = constants.PATH_COLOR
                else:
                    draw_color = constants.SCREEN_COLOR
                pygame.draw.polygon(self.screen, draw_color, polygon)

def save_matrix(path, is_closed):
    
    screen_matrix = Game(path, is_closed).run().flatten()
    #? compare R values of the RGB
    screen_matrix[screen_matrix == constants.PATH_COLOR[0]] = 1 
    screen_matrix[screen_matrix == constants.SCREEN_COLOR[0]] = 0
    to_be_saved = np.reshape(screen_matrix, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if is_closed:
        path_matrix_to_be_saved = constants.PATH_MATRIX_CONVEX
        screen_matrix_to_be_saved = constants.SCREEN_MATRIX_CONVEX
    else:
        path_matrix_to_be_saved = constants.PATH_MATRIX_SIN
        screen_matrix_to_be_saved = constants.SCREEN_MATRIX_SIN

    path_matrix_path = os.path.join(current_dir, constants.MATRICES_DIR, path_matrix_to_be_saved)
    screen_matrix_path = os.path.join(current_dir, constants.MATRICES_DIR, screen_matrix_to_be_saved)
    
    print("PATH_MATRIX", np.array(path).shape)
    print("saving path matrix...")
    with open(path_matrix_path, 'wb') as f:
        pickle.dump(path, f)
    
    print("saving screen matrix...")
    print("SCREEN_MATRIX", to_be_saved.shape)
    np.savetxt(screen_matrix_path, to_be_saved)


    with open(path_matrix_path, 'rb') as f:
        test = pickle.load(f)

if __name__ == '__main__':
    path, is_closed = path_generator.generate_convex_polygon()
    print("saving convex polygon...")
    save_matrix(path, is_closed)
    
    path, is_closed = path_generator.generate_sin_path()
    print("saving sin path...")
    save_matrix(path, is_closed)

    
    