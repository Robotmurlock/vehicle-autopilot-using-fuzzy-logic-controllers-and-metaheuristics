import math
import random

import game
from gift_wrap_ch import gift_wrap



def generate_polygon(): 
    coords = []
    num_of_points = 20

    for i in range (num_of_points):
        x = random.randrange(game.SCREEN_WIDTH)
        y = random.randrange(game.SCREEN_HEIGHT)
        coords.append((x, y))

    polygon = gift_wrap(coords)
    
    print(polygon)

    return polygon

def main():
    pass

if __name__ == "__main__":
    main()