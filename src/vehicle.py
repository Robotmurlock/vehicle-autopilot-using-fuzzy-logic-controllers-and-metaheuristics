import random
from math import sin, degrees
from pygame.math import Vector2
import math
from utils import constants

def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def valid_position(x, y):
    return x > 0 and y > 0 and x < constants.LEFT_SCREEN_WIDTH and y < constants.SCREEN_HEIGHT

class Car:
    def __init__(self, x, y, angle=0.0, length=4):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.left_sensor_input = 0
        self.front_sensor_input = 0
        self.right_sensor_input = 0
        self.last_position = None

    def update(self, dt, ds, drot):
        self.velocity = Vector2(ds, 0)

        self.position += self.velocity.rotate(-self.angle) * dt
        self.check_borders()
        self.check_collision()
        self.angle += degrees(drot) * dt

    def check_borders(self):
        self.position.x = max(self.position.x, 0)
        self.position.y = max(self.position.y, 0)
        self.position.x = min(self.position.x, constants.SCREEN_WIDTH - constants.CAR_WIDTH)
        self.position.y = min(self.position.y, constants.SCREEN_HEIGHT - constants.CAR_HEIGHT)

    def check_collision(self):
        return 

    def center_position(self):
        return Vector2(self.position.x + constants.CAR_WIDTH/2, self.position.y + constants.CAR_HEIGHT/2)

    def sensor(self, name, screen, angle_direction):
        angle = -self.angle/180*math.pi
        pos_x = self.center_position().x
        pos_y = self.center_position().y
        z = 0
        while(valid_position(int(pos_x), int(pos_y)) and screen.get_at((int(pos_x), int(pos_y))) == constants.PATH_COLOR):
            z = z + 1
            pos_x = self.center_position().x + z*math.cos(angle - angle_direction)
            pos_y = self.center_position().y + z*math.sin(angle - angle_direction)
            
        sensor_input = str(distance(self.center_position().x, self.center_position().y, pos_x, pos_y))
        return sensor_input

    def get_sensors(self, screen):
        front_sensor_input = self.sensor('front', screen, 0)
        left_sensor_input = self.sensor('left', screen, math.pi/2)
        right_sensor_input = self.sensor('right', screen, -math.pi/2)
        return (left_sensor_input, front_sensor_input, right_sensor_input)

    def sensor2(self, name, matrix, angle_direction):
        angle = -self.angle/180*math.pi
        pos_x = self.center_position().x
        pos_y = self.center_position().y
        z = 0
        while(valid_position(int(pos_x), int(pos_y)) and matrix[int(pos_x)][int(pos_y)] != constants.OFFROAD):
            z = z + 1
            pos_x = self.center_position().x + z*math.cos(angle - angle_direction)
            pos_y = self.center_position().y + z*math.sin(angle - angle_direction)
            
        sensor_input = str(distance(self.center_position().x, self.center_position().y, pos_x, pos_y))
        return sensor_input

    def get_sensors2(self, matrix):
        front_sensor_input = self.sensor2('front', matrix, 0)
        left_sensor_input = self.sensor2('left', matrix, math.pi/2)
        right_sensor_input = self.sensor2('right', matrix, -math.pi/2)
        return (left_sensor_input, front_sensor_input, right_sensor_input)

    def is_idle(self, iteration):
        result = False
        if self.last_position == self.center_position():
            result = True
        if iteration%40 == 0:
            self.last_position = self.center_position()
        return result

    def is_collided(self, current_pixel_color):
        return current_pixel_color == constants.SCREEN_COLOR

    def is_collided2(self, road_matrix):
        x, y = self.center_position()
        x = int(x)
        y = int(y)
        return road_matrix[x, y] == constants.OFFROAD

