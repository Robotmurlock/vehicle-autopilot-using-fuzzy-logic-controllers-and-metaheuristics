# Taken from: https://github.com/rasmaxim/pygame-car-tutorial
import os
import pygame
import random
from math import sin, degrees
from pygame.math import Vector2
import time
import math
import copy
import sys
from fuzzy import fuzzy_generator
from generator_functions import path_generator
import decoder
from vehicle import vehicle
from utils import constants

class Game:
    def __init__(self, path, closed_polygon):
        pygame.init()
        pygame.display.set_caption("Trained car")
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        self.car = vehicle.Car(constants.CAR_POS_X, constants.CAR_POS_Y, constants.CAR_ANGLE)

        self.path = path
        self.closed_polygon = closed_polygon

    def run(self, FSAngle, FSVelocity):
        car = vehicle.Car(constants.CAR_POS_X, constants.CAR_POS_Y, constants.CAR_ANGLE)

        iteration = 0
        last_position = None
        dec = decoder.Decoder(FSAngle, FSVelocity, self.car)

        while not self.exit:
            dt = self.clock.get_time() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            ds, drot = dec.get_movement_params()
            self.car.update(dt, ds, drot)

            current_pixel_color = self.draw_screen()
            iteration = iteration + 1
            if self.car.is_idle(iteration) or self.car.is_collided(current_pixel_color):
                break

            self.clock.tick(self.ticks)

        pygame.quit()
        return vehicle.distance(self.car.center_position().x, self.car.center_position().y, constants.GOAL.x, constants.GOAL.y)

    def draw_screen(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, constants.IMAGE_DIR, constants.IMAGE_NAME)
        car_image = pygame.image.load(image_path)
        scaled = pygame.transform.scale(car_image, (constants.CAR_WIDTH, constants.CAR_HEIGHT))

        rotated_car = pygame.transform.rotate(scaled, self.car.angle)

        self.screen.fill(constants.SCREEN_COLOR)
        self.draw_path()

        current_pixel_value = self.screen.get_at((int(self.car.center_position().x), int(self.car.center_position().y)))
        self.car.left_sensor_input, self.car.front_sensor_input, self.car.right_sensor_input = self.car.get_sensors(self.screen)
        self.screen.blit(rotated_car, self.car.position)
        pygame.display.flip()
        return current_pixel_value

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

def simulate(path, is_closed, FSAngle, FSVelocity):
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % constants.SCREEN_POSITION
    game = Game(path, is_closed)
    return(game.run(FSAngle, FSVelocity))

if __name__ == '__main__':
    # path, is_closed = path_generator.generate_convex_polygon()
    path, is_closed = path_generator.generate_sin_path()
    FSAngle, FSVelocity = fuzzy_generator.build_random_fuzzy_system(1)

    for i in range(0, 20):
        print(simulate(path, is_closed, FSAngle, FSVelocity))