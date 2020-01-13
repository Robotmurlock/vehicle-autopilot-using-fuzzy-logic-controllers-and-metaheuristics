import random
import fuzzy
import numpy as np
import math
import sys
import os
import subprocess as sp

clear = lambda: os.system('clear')

# Scale parameter
ALPHA = 0.15
BETA = 5

EPS = 0.000001

def degree_to_radian(angle):
    return angle/180*math.pi

class Decoder:
    def __init__(self, FSAngle, FSVelocity, car, debug = False):
        self.FSAngle = FSAngle
        self.FSVelocity = FSVelocity
        self.car = car
        self.debug = debug

        self.left_sensor_input = None
        self.right_sensor_input = None
        self.front_sensor_input = None
        self.FSInput = None

    def show_info(self):
        clear()
        print('left: ' + str(self.left_sensor_input))
        print('right: ' + str(self.right_sensor_input))
        print('front: ' + str(self.front_sensor_input))

        for x in self.FSAngle.inputs:
            print(x.name)
            for y in x.inputs:
                print('\t' + ("%1.2f" % y.mi) + ' | ' + ("%10s" % y.name) + ' | ' + str(y))

        print(self.FSAngle.output.name)
        for y in self.FSAngle.output:
            print('\t' + ("%1.2f" % y.mi) + ' | ' + ("%10s" % y.name) + ' | ' + str(y))

        print('angle solution: ' + str(self.FSAngle.solution))
        print()

    def get_movement_params(self):
        self.left_sensor_input = float(self.car.left_sensor_input)*ALPHA
        self.front_sensor_input = float(self.car.front_sensor_input)*ALPHA
        self.right_sensor_input = float(self.car.right_sensor_input)*ALPHA

        self.FSInput = np.array([self.left_sensor_input, self.right_sensor_input, self.front_sensor_input])
        self.FSAngle.fit(self.FSInput)
        self.FSVelocity.fit(self.FSInput)

        ds = (self.FSVelocity.solution*BETA)
        drot = degree_to_radian(self.FSAngle.solution) + EPS

        if self.debug:
            self.show_info()

        return (ds, drot)