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
        self.position.x = max(self.position.x, 0)
        self.position.y = max(self.position.y, 0)
        self.position.x = min(self.position.x, SCREEN_WIDTH/32)
        self.position.y = min(self.position.y, SCREEN_HEIGHT/32)
        self.angle += degrees(drot) * dt


class Game:
    def __init__(self, path, closed_polygon):
        pygame.init()
        pygame.display.set_caption("Trained car")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        self.car = Car(0, 0)

        self.path = path
        self.closed_polygon = closed_polygon

    def run(self):
        car = Car(0, 0)

        while not self.exit:
            dt = self.clock.get_time() / 1000

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
        scaled = pygame.transform.scale(car_image, (40, 20))

        self.screen.fill((0, 0, 0))
        
        rotated_car = pygame.transform.rotate(scaled, self.car.angle)

        self.draw_path()

        self.screen.blit(rotated_car, self.car.position)
        pygame.display.flip()

    def draw_path(self):
        color = (0, 255, 0)

        for coords in self.path:
            pygame.draw.lines(self.screen, color, self.closed_polygon, coords)


if __name__ == '__main__':
    path, is_closed = path_generator.generate_convex_polygon()
    # path, is_closed = path_generator.generate_sin_path()
    
    game = Game(path, is_closed)
    
    game.run()
