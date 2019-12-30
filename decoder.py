import random

def get_movement_params():
    dx = random.uniform(-1, 1)
    dy = random.uniform(-1, 1)
    drot = random.uniform(1, 10)

    return (dx, dy, drot)

def main():
    pass

if __name__ == "__main__":
    main()