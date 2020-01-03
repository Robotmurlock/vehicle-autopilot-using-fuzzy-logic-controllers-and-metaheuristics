import random
import fuzzy
import numpy as np
import math

def get_movement_params(car):
    left_sensor_input = float(car.left_sensor_input)/7
    front_sensor_input = float(car.front_sensor_input)/5
    right_sensor_input = float(car.right_sensor_input)/7

    FSInput = np.array([left_sensor_input, front_sensor_input, right_sensor_input])
    fuzzy.FSAngle.fit(FSInput)
    fuzzy.FSVelocity.fit(FSInput)
    #print("fuzzy:")
    #print("\tinput" + str(FSInput))
    #print("\tvelocity: " + str(fuzzy.FSVelocity.solution))
    #print("\tangle: " + str(fuzzy.FSAngle.solution))

    ds = (fuzzy.FSVelocity.solution*5)
    drot = (fuzzy.FSAngle.solution)/180*math.pi + 0.000001

    return (ds, drot)

def main():
    pass

if __name__ == "__main__":
    main()