# Taken from: https://github.com/rasmaxim/pygame-car-tutorial
import os
import random
import time
import math
import copy
import sys
import numpy as np

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
    all_values = []

    print(to_be_saved.shape)
    np.savetxt(constants.ROAD_MATRIX_PATH, to_be_saved.astype(int))

    check_matrix = lp.load_path()
    print("matrix has ones: ", 1 in check_matrix)

if __name__ == '__main__':
    # path, is_closed = path_generator.generate_convex_polygon()
    path, is_closed = path_generator.generate_sin_path()
    
    save_matrix(path, is_closed)