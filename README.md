# Controling vehicle by using fuzzy logic with fuzzy parameters generated via genetic algorithm

## Introduction

Purpose of this project was to try to optimize the fuzzy parameters of a fuzzy system via usage of the genetic algorithm. Fuzzy system is attached to a vehicle which is going through the predetermined path. Goal of the vehcile is to reach the end of the path.

## Setup

Path was represented as a boolean matrix with 1 for valid and 0 for invalid path.  
Vehicle is represented as a material point in the system, but it's visualized like a sprite in the simulation.  

## Fuzzy System

Fuzzy system contains 3 inputs and 2 outputs.

Inputs are: 
- `left_sensor` - Measures distance from the left side of the road  
- `right_sensor` - Measures distance from the right side of the road  
- `front_sensor` - Measures distance from the front side of the road  

Membership functions for all input functions are: `close`, `midrange`, `far`, `very far` 

Outputs are:
- `velocity` - Speed change
- `angle` - Change of the steering angle

Membership functions for `velocity` are: `low`, `middle`, `high`, `very high`   
Membership functions for `angle` are: `hard right`, `right`, `left`, `hard left`   

### Membership functions

All of the membership functions are trapezoidal, except the far left and far right ones. Those are most similar to ramp functions

Final position of critical points for each of the functions is determined by the genetic algorithm.

### Rules
???

## Genetic algorithm

Genetic algorithm used here works with discrete numbers.

### Chromosome

Single chromome contains fuzzy systems for both angle and velocity

### Fitness

Fitness of the unit calculated as ` 1 / distance_traveled`, goal is to minimize the fitness function

### Selection

Selection is tournament based.

### Crossover

Uniform crossover was used, where for each sensor, single trapezoidal functions were "crossovered"

### Mutation ???

Each of the angle membership functions had the possibility to randomly change critical points

## Results

## 
