# Controling vehicle by using fuzzy logic with fuzzy parameters optimized via genetic algorithm

## Introduction

Purpose of this project was to try to optimize the fuzzy parameters of a fuzzy system via usage of the genetic algorithm. Fuzzy system is attached to a vehicle which is going through the predetermined path. Goal of the vehicle is to reach the end of the path.

## Setup

You'll need the following:

- `python3.x`
- `pygame` library
- `matplotlib` library
- `numpy` library

## Running the code

If you just want to generate matrices and polygons for training you can just run:

> `python3 display_matrix_generator.py `

If you want to run the simulation on a pretrained fuzzy you can just run:
 
> `python3 simulation.py --polygon [convex, sin]`

If you want to run the genetic algorithm you can just run:
 
> `python3 genetic_algorithm.py --polygon [convex, sin]`

## Documentation

You can find the documentation inside the `docs` folder.

## Result:

![result](https://github.com/Robotmurlock/vehicle-autopilot-using-fuzzy-logic-controllers-and-metaheuristics/blob/master/docs/result.gif)

