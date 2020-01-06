import random
from fuzzy import fuzzy
import numpy as np
import math
import sys

class Decoder:
    def __init__(self, FSAngle, FSVelocity, car):
        self.FSAngle = FSAngle
        self.FSVelocity = FSVelocity
        self.car = car

    def get_movement_params(self):
        left_sensor_input = float(self.car.left_sensor_input)/7
        front_sensor_input = float(self.car.front_sensor_input)/5
        right_sensor_input = float(self.car.right_sensor_input)/7

        FSInput = np.array([left_sensor_input, front_sensor_input, right_sensor_input])
        self.FSAngle.fit(FSInput)
        self.FSVelocity.fit(FSInput)
        #print("fuzzy:")
        #print("\tinput" + str(FSInput))
        #print("\tvelocity: " + str(fuzzy.FSVelocity.solution))
        #print("\tangle: " + str(fuzzy.FSAngle.solution))

        ds = (self.FSVelocity.solution*5)
        drot = (self.FSAngle.solution)/180*math.pi + 0.000001

        return (ds, drot)