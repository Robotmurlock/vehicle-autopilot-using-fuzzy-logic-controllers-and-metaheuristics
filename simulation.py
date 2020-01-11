import numpy as np

from vehicle import vehicle
from utils import constants
from utils import load_path as lp
import decoder

MAX_ITERATIONS = 10_000
TIME_STEP = 0.1

def run(FSAngle, FSVelocity, road_matrix):
    """
    Runs a single simulation, movement params are calculated based on the fuzzy systems FSAngle and FSVelocity
    """
    car = vehicle.Car(constants.CAR_POS_X, constants.CAR_POS_Y, constants.CAR_ANGLE)

    iteration = 0

    dec = decoder.Decoder(FSAngle, FSVelocity, car)
    dt = TIME_STEP

    total_distance = 0

    while not car.is_idle(iteration) and not car.is_collided2(road_matrix) and iteration <= MAX_ITERATIONS:
        car.left_sensor_input, car.front_sensor_input, car.right_sensor_input = car.get_sensors2(road_matrix)
        ds, drot = dec.get_movement_params()
        total_distance += ds
        car.update(dt, ds, drot)
        iteration += 1 

    car_x, car_y = car.center_position()
    #return vehicle.distance(car_x, car_y, constants.GOAL.x, constants.GOAL.y)
    return 1/total_distance