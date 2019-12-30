import math
import random

def generate_polygon():
    xs = []
    ys = []
    
    width = 1280
    height = 720

    for i in range (10):
        xs.append(random.randrange(1280))
        ys.append(random.randrange(720))

    polygon = list(zip(xs, ys))
    

    print(polygon)

    return polygon

def main():
    pass

if __name__ == "__main__":
    main()