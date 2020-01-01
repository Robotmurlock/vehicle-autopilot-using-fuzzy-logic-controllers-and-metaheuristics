import random
import fuzzy
import numpy as np
import math

def get_movement_params(car):
    left_sensor_input = 30
    front_sensor_input = 30
    right_sensor_input = 30

    FSInput = np.array([left_sensor_input, front_sensor_input, right_sensor_input])
    fuzzy.FSAngle.fit(FSInput)
    fuzzy.FSVelocity.fit(FSInput)
    print("fuzzy:")
    print("\tinput" + str(FSInput))
    print("\tvelocity: " + str(fuzzy.FSVelocity.solution))
    print("\tangle: " + str(fuzzy.FSAngle.solution))

    dx = (fuzzy.FSVelocity.solution/20) * math.cos(car.angle)
    dy = (fuzzy.FSVelocity.solution/20) * math.sin(car.angle)
    drot = (fuzzy.FSAngle.solution)/20 + 0.000001

    return (dx, dy, drot)

def main():
    pass

if __name__ == "__main__":
    main()