import random
import numpy as np

import game
import math

import utils.convex_hull as ch 
import utils.linear_transformations as lt
from utils import constants

def generate_convex_polygon(): 
    coords = []
    num_of_points = 20
    
    for i in range (num_of_points):
        x = random.randrange(game.SCREEN_WIDTH)
        y = random.randrange(game.SCREEN_HEIGHT)
        coords.append((x, y))

    coords1 = ch.gift_wrap(coords)

    scaling_factor = 0.8
    offset = 75
    coords2 = lt.apply_scaling(scaling_factor, scaling_factor, coords1)
    coords2 = lt.apply_translation(offset, offset, coords2)

    polygon = [coords1, coords2]
    
    is_closed = True
    return polygon, is_closed


def generate_sin_path():
    coords1 = []
    coords2 = []
    offset = 200
    num_of_points = 20

    for i in range(constants.SCREEN_WIDTH):
        coords1.append((i, math.sin(0.01*i) * 200 + 250))

    coords2 = lt.apply_translation(0, offset, coords1)
    coords2.reverse() #? in order to properly match coords for polygon

    polygon = coords1 + coords2
    
    is_closed = False
    return polygon, is_closed

def main():
    pass

if __name__ == "__main__":
    main()