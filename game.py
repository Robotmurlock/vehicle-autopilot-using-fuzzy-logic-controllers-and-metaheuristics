# Taken from: https://github.com/rasmaxim/pygame-car-tutorial
import os
import pygame
import random
from math import sin, degrees
from pygame.math import Vector2
import time
import math
import copy

import path_generator
import decoder

IMAGE_DIR = "img"
IMAGE_NAME = "car.png"

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

CAR_WIDTH = 40
CAR_HEIGHT = 20
CAR_POS_X = 10
CAR_POS_Y = 400

PATH_COLOR = (0, 255, 0)

def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

class Car:
    def __init__(self, x, y, angle=0.0, length=4):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.left_sensor_input = 0
        self.front_sensor_input = 0
        self.right_sensor_input = 0

    def update(self, dt, dx, dy, drot):
        self.velocity += Vector2(dx, dy)

        turning_radius = self.length / sin(drot)
        angular_velocity = self.velocity.x / turning_radius

        self.position += self.velocity.rotate(-self.angle) * dt
        self.position.x = max(self.position.x, 0)
        self.position.y = max(self.position.y, 0)
        self.position.x = min(self.position.x, SCREEN_WIDTH - CAR_WIDTH)
        self.position.y = min(self.position.y, SCREEN_HEIGHT - CAR_HEIGHT)
        self.angle += degrees(drot) * dt


class Game:
    def __init__(self, path, closed_polygon):
        pygame.init()
        pygame.display.set_caption("Trained car")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        self.car = Car(CAR_POS_X, CAR_POS_Y)

        self.path = path
        self.closed_polygon = closed_polygon

    def run(self):
        car = Car(CAR_POS_X, CAR_POS_Y)

        while not self.exit:
            time.sleep(1)
            dt = self.clock.get_time() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            dx, dy, drot = decoder.get_movement_params(self.car)
            self.car.update(dt, dx, dy, drot)

            self.draw_screen()

            self.clock.tick(self.ticks)

        pygame.quit()

    def draw_screen(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, IMAGE_DIR, IMAGE_NAME)
        car_image = pygame.image.load(image_path)
        scaled = pygame.transform.scale(car_image, (CAR_WIDTH, CAR_HEIGHT))

        rotated_car = pygame.transform.rotate(scaled, self.car.angle)

        screen_color = (0, 0, 0)
        self.screen.fill(screen_color)

        self.draw_path()
        print('Car position: ' + str(self.car.position))
        self.car.left_sensor_input, self.car.front_sensor_input, self.car.right_sensor_input = self.sensors()

        self.screen.blit(rotated_car, self.car.position)
        pygame.display.flip()


    def draw_path(self):
        color = PATH_COLOR

        polygon = []
        for coords in self.path:
            polygon += coords

        pygame.draw.polygon(self.screen, color, polygon)

    def sensors(self):
        # front sensor
        pos_x = self.car.position.x
        pos_y = self.car.position.y
        while(pos_x < SCREEN_WIDTH and self.screen.get_at((int(pos_x), int(pos_y))) != PATH_COLOR):
            pos_x = pos_x + 1
        print('front sensor: ' + str(int(pos_x)) + ' ' + str(int(pos_y)))
        front_sensor_input = str(distance(self.car.position.x+CAR_WIDTH, self.car.position.y, pos_x, pos_y))
        print('front sensor input: ' + front_sensor_input)

        # left sensor
        pos_x = self.car.position.x
        pos_y = self.car.position.y
        while(pos_y > 0 and self.screen.get_at((int(pos_x), int(pos_y))) != PATH_COLOR):
            pos_y = pos_y - 1
        print('left sensor: ' + str(int(pos_x)) + ' ' + str(int(pos_y)))
        left_sensor_input = str(distance(self.car.position.x+CAR_WIDTH, self.car.position.y, pos_x, pos_y))
        print('front sensor input: ' + left_sensor_input)


        # right sensor
        pos_x = self.car.position.x
        pos_y = self.car.position.y
        while(pos_y < SCREEN_HEIGHT and self.screen.get_at((int(pos_x), int(pos_y))) != PATH_COLOR):
            pos_y = pos_y + 1
        print('right sensor: ' + str(int(pos_x)) + ' ' + str(int(pos_y)))
        right_sensor_input = str(distance(self.car.position.x+CAR_WIDTH, self.car.position.y, pos_x, pos_y))
        print('front sensor input: ' + right_sensor_input)

        return (left_sensor_input, front_sensor_input, right_sensor_input)


if __name__ == '__main__':
    # path, is_closed = path_generator.generate_convex_polygon()
    path, is_closed = path_generator.generate_sin_path()

    game = Game(path, is_closed)

    game.run()
