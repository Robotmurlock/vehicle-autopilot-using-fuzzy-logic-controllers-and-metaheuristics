import random
import fz_fuzzy
import numpy as np
import math
import sys

class Decoder:
    def __init__(self, FSAngle, FSVelocity, car, debug = False):
        self.FSAngle = FSAngle
        self.FSVelocity = FSVelocity
        self.car = car
        self.debug = debug

    def get_movement_params(self):
        left_sensor_input = float(self.car.left_sensor_input)/7
        front_sensor_input = float(self.car.front_sensor_input)/5
        right_sensor_input = float(self.car.right_sensor_input)/7

        FSInput = np.array([left_sensor_input, right_sensor_input, front_sensor_input])
        self.FSAngle.fit(FSInput)
        self.FSVelocity.fit(FSInput)

        ds = (self.FSVelocity.solution*5)
        drot = (self.FSAngle.solution)/180*math.pi + 0.000001

        if(self.debug):
            print('left: ' + str(left_sensor_input))
            print('right: ' + str(right_sensor_input))
            print('front: ' + str(front_sensor_input))

            for x in self.FSAngle.inputs:
                print(x.name)
                for y in x.inputs:
                    print('\t' + ("%1.2f" % y.mi) + ' | ' + str(y))

            print(self.FSAngle.output.name)
            for y in self.FSAngle.output:
                print('\t' + ("%1.2f" % y.mi) + ' | ' + str(y))

            print('angle solution:' + str(self.FSAngle.solution))

        return (ds, drot)