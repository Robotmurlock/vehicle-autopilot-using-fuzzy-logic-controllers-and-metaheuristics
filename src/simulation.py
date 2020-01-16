import os
import random
import time
import math
import copy
import sys
import numpy as np
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from pygame.locals import *
from pygame.math import Vector2

import fuzzy_generator
import decoder
import vehicle
from utils import constants, path_generator
import pickle 
import argparse


class Simulation:
    def __init__(self, path, closed_polygon):
        pygame.init()
        pygame.display.set_caption("Trained car")
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), DOUBLEBUF)
        self.screen.set_alpha(False)
        self.left_screen = pygame.Surface((constants.LEFT_SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.right_screen = pygame.Surface((constants.RIGHT_SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.SysFont('Times New Roman', constants.FONT_SIZE)
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        self.car = vehicle.Car(constants.CAR_POS_X, constants.CAR_POS_Y, constants.CAR_ANGLE)

        self.path = path
        self.closed_polygon = closed_polygon

    def run(self, FSAngle, FSVelocity):
        car = vehicle.Car(constants.CAR_POS_X, constants.CAR_POS_Y, constants.CAR_ANGLE)

        iteration = 0
        dec = decoder.Decoder(FSAngle, FSVelocity, self.car, False)

        while not self.exit:
            dt = self.clock.get_time() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            ds, drot = dec.get_movement_params()
            fuzzy_text = dec.fuzzy_text
            self.car.update(dt, ds, drot)

            current_pixel_color = self.draw_screen(fuzzy_text)
            iteration = iteration + 1
            if self.car.is_idle(iteration) or self.car.is_collided(current_pixel_color):
                break

            self.clock.tick(self.ticks)

        pygame.quit()
        return vehicle.distance(self.car.center_position().x, self.car.center_position().y, constants.GOAL.x, constants.GOAL.y)

    def draw_screen(self, fuzzy_text):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, constants.IMAGE_DIR, constants.IMAGE_NAME)
        car_image = pygame.image.load(image_path)
        scaled = pygame.transform.scale(car_image, (constants.CAR_WIDTH, constants.CAR_HEIGHT))

        rotated_car = pygame.transform.rotate(scaled, self.car.angle)

        self.left_screen.fill(constants.SCREEN_COLOR)
        self.draw_path(self.left_screen)

        current_pixel_value = self.left_screen.get_at((int(self.car.center_position().x), int(self.car.center_position().y)))
        self.car.left_sensor_input, self.car.front_sensor_input, self.car.right_sensor_input = self.car.get_sensors(self.left_screen)
        self.left_screen.blit(rotated_car, self.car.position)

        self.screen.blit(self.left_screen, (0, 0))
        self.right_screen.fill(constants.RIGHT_SCREEN_COLOR)
        self.screen.blit(self.right_screen, (constants.LEFT_SCREEN_WIDTH, 0))

        lines = fuzzy_text.split('\n')
        x = 0
        for line in lines:
            text = self.font.render(line, False, (0, 0, 0))
            self.screen.blit(text, (constants.LEFT_SCREEN_WIDTH, constants.FONT_SIZE*x))
            x += 1
        
        pygame.display.flip()
        
        return current_pixel_value

    def draw_path(self, screen):
        if not self.closed_polygon:
            pygame.draw.polygon(screen, constants.PATH_COLOR, self.path)
        else:
            for i, polygon in enumerate(self.path):
                if i % 2 == 0:
                    draw_color = constants.PATH_COLOR
                else:
                    draw_color = constants.SCREEN_COLOR
                pygame.draw.polygon(screen, draw_color, polygon)

def simulate(path, is_closed, FSAngle, FSVelocity):
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % constants.SCREEN_POSITION
    game = Simulation(path, is_closed)
    return(game.run(FSAngle, FSVelocity))

if __name__ == '__main__':
    """
    Set up game with pretrained fuzzy system
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--polygon', choices=['convex', 'sin'], help='Runs the simulation with pretrained fuzzy system on a choosen polygon', required=True)

    args = parser.parse_args()
    polygon = args.polygon

    if polygon != "convex":
        path, is_closed = path_generator.generate_sin_path()
    else:
        path, is_closed = path_generator.generate_convex_polygon()
    

    with open(constants.PRETRAINED_FUZZY_PATH, 'rb') as f:
        fz = pickle.load(f)

    pygame.font.init() 
    
    FSAngle, FSVelocity = fz
    print(FSAngle)
    print(FSVelocity)

    simulate(path, is_closed, FSAngle, FSVelocity)