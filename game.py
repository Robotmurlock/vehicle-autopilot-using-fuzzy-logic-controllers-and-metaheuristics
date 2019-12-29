# Taken from: https://github.com/rasmaxim/pygame-car-tutorial
import os
import pygame
from math import sin, radians, degrees, copysign
from pygame.math import Vector2


class Car:
    def __init__(self, x, y, angle=0.0, length=4, max_steering=30, max_acceleration=5.0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 20
        self.brake_deceleration = 10
        self.free_deceleration = 2

        self.acceleration = 0.0
        self.steering = 0.0

    def update(self, dt):
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car tutorial")
        width = 1280
        height = 720
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        self.car = Car(0, 0)

    def run(self):
        car = Car(0, 0)

        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User input
            self.handle_user_input(dt)

            # Logic
            self.car.update(dt)

            # Drawing
            self.draw_screen()

            self.clock.tick(self.ticks)
        
        pygame.quit()

    def draw_screen(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "img", "car.png")
        car_image = pygame.image.load(image_path)
        ppu = 32

        self.screen.fill((0, 0, 0))
        rotated = pygame.transform.rotate(car_image, self.car.angle)
        rect = rotated.get_rect()
        self.screen.blit(rotated, self.car.position * ppu - (rect.width / 2, rect.height / 2))
        pygame.display.flip()

    def handle_user_input(self, dt):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            if self.car.velocity.x < 0:
                self.car.acceleration = self.car.brake_deceleration
            else:
                self.car.acceleration += 1 * dt
        elif pressed[pygame.K_DOWN]:
            if self.car.velocity.x > 0:
                self.car.acceleration = -self.car.brake_deceleration
            else:
                self.car.acceleration -= 1 * dt
        elif pressed[pygame.K_SPACE]:
            if abs(self.car.velocity.x) > dt * self.car.brake_deceleration:
                self.car.acceleration = -copysign(self.car.brake_deceleration, self.car.velocity.x)
            else:
                self.car.acceleration = -self.car.velocity.x / dt
        else:
            if abs(self.car.velocity.x) > dt * self.car.free_deceleration:
                self.car.acceleration = -copysign(self.car.free_deceleration, self.car.velocity.x)
            else:
                if dt != 0:
                    self.car.acceleration = -self.car.velocity.x / dt
        self.car.acceleration = max(-self.car.max_acceleration, min(self.car.acceleration, self.car.max_acceleration))

        if pressed[pygame.K_RIGHT]:
            self.car.steering -= 30 * dt
        elif pressed[pygame.K_LEFT]:
            self.car.steering += 30 * dt
        else:
            self.car.steering = 0
        self.car.steering = max(-self.car.max_steering, min(self.car.steering, self.car.max_steering))


if __name__ == '__main__':
    game = Game()
    game.run()
