import numpy as np
import random
import fz_fuzzy as fuzzy

ALL_FUZZY_FUNCS = {
    "left_sensor": {
        "name": "left_sensor",
        "left_boundary": 0,
        "right_boundary": 100,
        "mf_names": ["close", "midrange", "far", "very_far"],
        "is_input": True,
    },
    "right_sensor": {
        "name": "right_sensor",
        "left_boundary": 0,
        "right_boundary": 100,
        "mf_names": ["close", "midrange", "far", "very_far"],
        "is_input": True,
    },
    "front_sensor": {
        "name": "front_sensor",
        "left_boundary": 0,
        "right_boundary": 20,
        "mf_names": ["close", "midrange", "far", "very far"],
        "is_input": True,
    },
    "velocity": {
        "name": "velocity",
        "left_boundary": 1,
        "right_boundary": 20,
        "mf_names": ["low", "middle", "high", "very high"],
        "is_input": False,
    },
    "angle": {
        "name": "angle",
        "left_boundary": -45,
        "right_boundary": 45,
        "mf_names": ["hard right", "right", "forward", "left", "hard left"],
        "is_input": False,
    }
}

def get_ys(size):
    """
    generate 10|0110|...|0110|01 sequence of ys
    
    len(10|0110|...|0110|01) = size
    """
    ys = [1, 0]
    for i in range(2, size):
        #? if we are on the edges of the 0110
        #? here->0 110 or 011 0<-here
        if (i-2)%4 == 0 or (i-2)%4 == 3:
            ys.append(0)
        else:
            ys.append(1)
    return ys

def get_xs(size, left, right):
    """
    Generates key points for trapezoidal functions.

    Guarantees that there are no uncovered areas of the x-axis
    """
    number_of_points = 4*(size-1)
    #? split interval to parts within key_points represented by the key_points array 
    key_points = random.sample(range(left+1, right-1), size-1)
    key_points.append(left)
    key_points.append(right)
    key_points.sort()

    xs = []
    #? left most figure (isn't a trapeziod)
    xs.append(key_points[0])
    xs.append(key_points[1])

    for i in range(1, size-1):
        #? choose middle points for the trapezoid
        new_xs = random.sample(range(key_points[i]-1, key_points[i+1]+1), 2)
        new_xs.sort()

        #? choose left-most edge so that is for sure 'leftest' point in the trapezoid 
        xs.append(random.randint(key_points[i-1]+1, key_points[i]))
        
        #? append middle points
        xs.append(new_xs[0])
        xs.append(new_xs[1])
        
        #? choose right-most edge so that is for sure 'rightest' point in the trapezoid
        xs.append(random.randint(key_points[i+1], key_points[i+2]-1))
    
    #? right most figure (isn't a trapeziod)
    xs.append(key_points[-2])
    xs.append(key_points[-1])

    return xs
    

def xy_split(xs, ys, size):
    """
    Convert 10 0110... 01 to [ [1, 0], [0, 1, 1, 0], ... [0, 1]], same for x
    """
    #? first since it's only length of 2
    xs_split = [np.array([xs[0], xs[1]])]
    ys_split = [np.array([ys[0], ys[1]])]
    split_size = size-2
    
    for i in range(0, split_size):
        k = 4*i
        xs_split.append(np.array([xs[2+k], xs[3+k], xs[4+k], xs[5+k]]))
        ys_split.append(np.array([ys[2+k], ys[3+k], ys[4+k], ys[5+k]]))
    
    #? same as first since it's only length of 2
    xs_split.append(np.array([xs[-2], xs[-1]]))
    ys_split.append(np.array([ys[-2], ys[-1]]))
    
    return (xs_split, ys_split)
    
def random_fuzzy(name, func_names, left, right, is_input = True):
    size = len(func_names)
    number_of_points = 4*(size-1)
    
    #? generate_functions
    xs = get_xs(size, left, right)
    ys = get_ys(number_of_points)
    
    #? build_single_fuzzy_io
    xs_split, ys_split = xy_split(xs, ys, size)
    if is_input:
        return fuzzy.FuzzyInput(name, np.array([fuzzy.MFInput(func_names[i], np.array(xs_split[i]), np.array(ys_split[i])) for i in range(size)])) 
    else:
        return fuzzy.FuzzyOutput(name, np.array([fuzzy.MFOutput(func_names[i], np.array(xs_split[i]), np.array(ys_split[i])) for i in range(size)])) 

def set_rules(left_sensor, front_sensor, right_sensor, angle, velocity):
    angle_rules = fuzzy.FuzzyRules(np.array([
        fuzzy.Rule(np.array([left_sensor[0], front_sensor[0]]), angle[4]),
        fuzzy.Rule(np.array([right_sensor[0], front_sensor[0]]), angle[0]),
        fuzzy.Rule(np.array([front_sensor[1], left_sensor[1]]), angle[3]),
        fuzzy.Rule(np.array([front_sensor[1], right_sensor[1]]), angle[1]),
        fuzzy.Rule(np.array([front_sensor[0], left_sensor[3]]), angle[0]),
        fuzzy.Rule(np.array([front_sensor[0], right_sensor[3]]), angle[4]),
        fuzzy.Rule(np.array([left_sensor[0], right_sensor[1]]), angle[3]),
        fuzzy.Rule(np.array([left_sensor[1], right_sensor[0]]), angle[1])
    ]))

    velocity_rules = fuzzy.FuzzyRules(np.array([
        fuzzy.Rule(np.array([front_sensor[3]]), velocity[3]),
        fuzzy.Rule(np.array([front_sensor[2]]), velocity[2]),
        fuzzy.Rule(np.array([front_sensor[1]]), velocity[1]),
        fuzzy.Rule(np.array([front_sensor[0]]), velocity[0])
    ]))

    return angle_rules, velocity_rules

def build_random_fuzzy_system():
    fuzzy_inputs = {}
    fuzzy_outputs = {}
    
    for fuzzy_key in ALL_FUZZY_FUNCS:
        name = ALL_FUZZY_FUNCS[fuzzy_key]["name"]
        left = ALL_FUZZY_FUNCS[fuzzy_key]["left_boundary"]
        right = ALL_FUZZY_FUNCS[fuzzy_key]["right_boundary"]
        is_input = ALL_FUZZY_FUNCS[fuzzy_key]["is_input"]
        names = ALL_FUZZY_FUNCS[fuzzy_key]["mf_names"]
        
        if is_input:
            fuzzy_inputs[name] = random_fuzzy(name, names, left, right, is_input)
        else:
            fuzzy_outputs[name] = random_fuzzy(name, names, left, right, is_input)
          
    left_sensor = fuzzy_inputs["left_sensor"]
    front_sensor = fuzzy_inputs["front_sensor"]
    right_sensor = fuzzy_inputs["right_sensor"]
    angle = fuzzy_outputs["angle"]
    velocity = fuzzy_outputs["velocity"]
    
    angle_rules, velocity_rules = set_rules(left_sensor, front_sensor, right_sensor, angle, velocity)
    
    FSAngle = fuzzy.FuzzySystem(np.array(list(fuzzy_inputs.values())), fuzzy_outputs["angle"], angle_rules)
    FSVelocity = fuzzy.FuzzySystem(np.array(list(fuzzy_inputs.values())), fuzzy_outputs["velocity"], velocity_rules) 
    return FSAngle, FSVelocity

if __name__ == "__main__":
    get_ys(2)