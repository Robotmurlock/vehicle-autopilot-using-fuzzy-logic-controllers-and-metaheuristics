from pygame.math import Vector2
import math

IMAGE_DIR = "img"
IMAGE_NAME = "car.png"

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_POSITION = (0, 100)

CAR_WIDTH = 40
CAR_HEIGHT = 20
CAR_POS_X = 10
CAR_POS_Y = 400
CAR_ANGLE = -45

PATH_COLOR = (155, 100, 200, 255)
SCREEN_COLOR = (100, 100, 100, 255)
GOAL = Vector2(SCREEN_WIDTH-10, SCREEN_HEIGHT/2)

OFFROAD = 0

MATRICES_DIR = "matrices"
PATH_MATRIX_SIN = "path_matrix_sin.pickle"
SCREEN_MATRIX_SIN = "screen_matrix_sin.txt"

PATH_MATRIX_CONVEX = "path_matrix_convex.pickle"
SCREEN_MATRIX_CONVEX = "screen_matrix_convex.txt"

USE_CONVEX_POLYGON = False
USE_SIN_POLYGON = True