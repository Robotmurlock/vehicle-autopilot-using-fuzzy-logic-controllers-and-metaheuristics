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

from generator_functions import path_generator
from utils import constants

class Game:
    def __init__(self, path, closed_polygon):
        pygame.init()
        pygame.display.set_caption("Trained car")
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), DOUBLEBUF)
        self.screen.set_alpha(False)
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        self.path = path
        self.closed_polygon = closed_polygon

        self.screen_matrix = None
        self.is_screen_saved = False

    def run(self):
        while not self.exit:
            dt = self.clock.get_time() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            self.draw_screen()        
            self.clock.tick(self.ticks)

            if self.is_screen_saved:
                break

        pygame.quit()
        return self.screen_matrix

    def draw_screen(self):
        self.screen.fill(constants.SCREEN_COLOR)
        
        self.draw_path()
        self.save_display_matrix()

        pygame.display.flip()
    
    def save_display_matrix(self):
        self.screen_matrix = pygame.surfarray.pixels_red(self.screen).astype(int)
        self.is_screen_saved = True
        

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

if __name__ == '__main__':
    # path, is_closed = path_generator.generate_convex_polygon()
    path, is_closed = path_generator.generate_sin_path()

    screen_matrix = Game(path, is_closed).run().flatten()
    #? compare R values of the RGB
    screen_matrix[screen_matrix == constants.PATH_COLOR[0]] = 1 
    screen_matrix[screen_matrix == constants.SCREEN_COLOR[0]] = 0
    to_be_saved = np.reshape(screen_matrix, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    all_values = []

    print(all_values)
    print(to_be_saved.shape)
    np.savetxt('screen_matrix.txt', to_be_saved)

    check_matrix = np.loadtxt('screen_matrix.txt')
    print("check_matrix: ", check_matrix.shape)