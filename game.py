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

screen_width = 1280
screen_height = 720

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
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Trained car")
        width = 1280
        height = 720
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        self.car = Car(10, 10)

    def run(self):
        car = Car(10, 10)

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
        ppu = 32

        self.screen.fill((0, 0, 0))
        scaled = pygame.transform.scale(car_image, (20, 10))
        rotated = pygame.transform.rotate(scaled, self.car.angle)
        rect = rotated.get_rect()
        pygame.draw.polygon(self.screen, (0, 255, 0), path_generator.generate_polygon())
        self.screen.blit(rotated, self.car.position * ppu - (rect.width / 2, rect.height / 2))
        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run()
