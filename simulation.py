import numpy as np

from vehicle import vehicle
from utils import constants
from utils import load_path as lp
import decoder

def run(FSAngle, FSVelocity, road_matrix):
    """
    Runs a single simulation, movement params are calculated based on the fuzzy systems FSAngle and FSVelocity
    """
    car = vehicle.Car(constants.CAR_POS_X, constants.CAR_POS_Y, constants.CAR_ANGLE)

    iteration = 0
    last_position = car.center_position()


    dec = decoder.Decoder(FSAngle, FSVelocity, car)
    dt = 1

    #while not car.is_idle(iteration) and not car.is_collided2(road_matrix):
    while not car.is_collided2(road_matrix):
        ds, drot = dec.get_movement_params()
        car.update(dt, ds, drot)
        iteration += 1 

        if iteration % 40 == 0:
            if car.center_position == last_position:
                break
            else:
                last_position = car.center_position()




    car_x, car_y = car.center_position()
    return vehicle.distance(car_x, car_y, constants.GOAL.x, constants.GOAL.y)