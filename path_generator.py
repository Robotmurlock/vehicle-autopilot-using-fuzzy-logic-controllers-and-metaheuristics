import random

import game
import math

from gift_wrap_ch import gift_wrap


def generate_convex_polygon(): 
    coords = []
    num_of_points = 20

    for i in range (num_of_points):
        x = random.randrange(game.SCREEN_WIDTH)
        y = random.randrange(game.SCREEN_HEIGHT)
        coords.append((x, y))

    polygon = gift_wrap(coords)
    
    return polygon


def generate_sin_path():
    coords = []
    num_of_points = 20
    for i in range(game.SCREEN_WIDTH):
        coords.append((i, math.sin(0.01*i) * 300 + 400))

    return coords

def main():
    pass

if __name__ == "__main__":
    main()