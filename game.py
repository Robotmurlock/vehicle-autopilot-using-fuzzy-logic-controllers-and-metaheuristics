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
SCREEN_COLOR = (100, 100, 100)

def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def valid_position(x, y):
    return x > 0 and y > 0 and x < SCREEN_WIDTH and y < SCREEN_HEIGHT

class Car:
    def __init__(self, x, y, angle=0.0, length=4):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.left_sensor_input = 0
        self.front_sensor_input = 0
        self.right_sensor_input = 0

    def update(self, dt, ds, drot):
        self.velocity = Vector2(ds, 0)

        self.position += self.velocity.rotate(-self.angle) * dt
        self.check_borders()
        self.check_collision()
        self.angle += degrees(drot) * dt

    def check_borders(self):
        self.position.x = max(self.position.x, 0)
        self.position.y = max(self.position.y, 0)
        self.position.x = min(self.position.x, SCREEN_WIDTH - CAR_WIDTH)
        self.position.y = min(self.position.y, SCREEN_HEIGHT - CAR_HEIGHT)

    def check_collision(self):
        return '#TODO'

    def center_position(self):
        return Vector2(self.position.x + CAR_WIDTH/2, self.position.y + CAR_HEIGHT/2)

    def sensor(self, name, screen, angle_direction):
        angle = -self.angle/180*math.pi
        pos_x = self.center_position().x
        pos_y = self.center_position().y
        z = 0
        while(valid_position(int(pos_x), int(pos_y)) and screen.get_at((int(pos_x), int(pos_y))) == PATH_COLOR):
            z = z + 1
            pos_x = self.center_position().x + z*math.cos(angle - angle_direction)
            pos_y = self.center_position().y + z*math.sin(angle - angle_direction)
            
        sensor_input = str(distance(self.center_position().x, self.center_position().y, pos_x, pos_y))
        return sensor_input


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
            dt = self.clock.get_time() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            ds, drot = decoder.get_movement_params(self.car)
            self.car.update(dt, ds, drot)
            self.draw_screen()
            self.clock.tick(self.ticks)

        pygame.quit()

    def draw_screen(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, IMAGE_DIR, IMAGE_NAME)
        car_image = pygame.image.load(image_path)
        scaled = pygame.transform.scale(car_image, (CAR_WIDTH, CAR_HEIGHT))

        rotated_car = pygame.transform.rotate(scaled, self.car.angle)

        self.screen.fill(SCREEN_COLOR)
        self.draw_path()
        self.car.left_sensor_input, self.car.front_sensor_input, self.car.right_sensor_input = self.sensors()
        self.screen.blit(rotated_car, self.car.position)
        pygame.display.flip()


    def draw_path(self):

        if not self.closed_polygon:
            pygame.draw.polygon(self.screen, PATH_COLOR, self.path)
        else:
            for i, polygon in enumerate(self.path):
                if i % 2 == 0:
                    draw_color = PATH_COLOR
                else:
                    draw_color = SCREEN_COLOR
                pygame.draw.polygon(self.screen, draw_color, polygon)

    def sensors(self):
        front_sensor_input = self.car.sensor('front', self.screen, 0)
        left_sensor_input = self.car.sensor('left', self.screen, math.pi/2)
        right_sensor_input = self.car.sensor('right', self.screen, -math.pi/2)
        return (left_sensor_input, front_sensor_input, right_sensor_input)


if __name__ == '__main__':
    # path, is_closed = path_generator.generate_convex_polygon()
    path, is_closed = path_generator.generate_sin_path()

    game = Game(path, is_closed)

    game.run()
