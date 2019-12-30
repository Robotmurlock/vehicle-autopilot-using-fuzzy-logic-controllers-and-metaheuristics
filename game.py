# Taken from: https://github.com/rasmaxim/pygame-car-tutorial
import os
import pygame
import random
from math import sin, radians, degrees, copysign
from pygame.math import Vector2

import path_generator
import decoder

IMAGE_DIR = "img"
IMAGE_NAME = "car.png"

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class Car:
    def __init__(self, x, y, angle=0.0, length=4):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length

    def update(self, dt, dx, dy, drot):
        self.velocity += Vector2(dx, dy)

        turning_radius = self.length / sin(drot)
        angular_velocity = self.velocity.x / turning_radius

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(drot) * dt


class Game:
    def __init__(self, path):
        pygame.init()
        pygame.display.set_caption("Trained car")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        self.car = Car(100, 100)

        self.path = path

    def run(self):
        car = Car(0, 0)

        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            dx, dy, drot = decoder.get_movement_params()
            self.car.update(dt, dx, dy, drot)

            print("Car position", self.car.position)
            self.draw_screen()

            self.clock.tick(self.ticks)
        
        pygame.quit()

    def draw_screen(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, IMAGE_DIR, IMAGE_NAME)
        car_image = pygame.image.load(image_path)

        self.screen.fill((0, 0, 0))
        rotated = pygame.transform.rotate(car_image, self.car.angle)
        pygame.draw.lines(self.screen, (0, 255, 0), True, self.path)
        self.screen.blit(rotated, self.car.position)
        pygame.display.flip()

if __name__ == '__main__':
    path = path_generator.generate_polygon()
    game = Game(path)
    
    game.run()
