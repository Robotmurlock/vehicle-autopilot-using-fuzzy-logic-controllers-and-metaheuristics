import random
import fuzzy
import numpy as np
import math
import sys
import os
import subprocess as sp
from utils import constants

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
        self.fuzzy_text = None

    def get_info(self):
        out = ' SENSOR INPUTS:\n'
        out += ' left sensor input: ' + ("%1.2f" % self.left_sensor_input) + "\n"
        out += ' right sensor input: ' + ("%1.2f" % self.right_sensor_input) + '\n'
        out += ' front sensor input: ' + ("%1.2f" % self.front_sensor_input) + '\n'
        out += '\n'

        out += ' FUZZY INPUTS:\n'
        for x in self.FSAngle.inputs:
            out += ' ' + x.name + ':\n'
            for y in x.inputs:
                out += constants.TAB + ("%1.2f" % y.mi) + ' | ' + y.name + ' | ' + str(y) + '\n'
        out += '\n'

        out += ' FUZZY OUTPUTS:\n'
        out += ' ' + self.FSAngle.output.name + ':\n'
        for y in self.FSAngle.output:
            out += constants.TAB + ("%1.2f" % y.mi) + ' | ' + y.name + ' | ' + str(y) + '\n'

        out += ' ' + self.FSVelocity.output.name + ':\n'
        for y in self.FSVelocity.output:
            out += constants.TAB + ("%1.2f" % y.mi) + ' | ' + y.name + ' | ' + str(y) + '\n'

        out += '\n'
        out += ' angle solution: ' + ("%1.2f" % self.FSAngle.solution) +'\n'
        out += ' velocity solution: ' + ("%1.2f" % self.FSVelocity.solution) +'\n\n'
        return out
        
        
 
    def show_info(self):
        clear()
        print(self.get_info())

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
        self.fuzzy_text = self.get_info()

        return (ds, drot)