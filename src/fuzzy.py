# MFInput: Represents fuzzy membership function for input variable. 
#          Main role is to calculate belonging of element x to appropriate set. 
#
# MFOutput: Represents fuzzy membership function for output variable. 
#           Main role is to calculate belonging of element x to appropriate set 
#           based on declared rules (class Rule) and input variables. 
#
# Rule: Represents one rule for fuzzy system.
#
# FuzzyInput: Represents set of input variables (MFInput). 
#
# FuzzyOutput: Represents set of output variables (MFOutput).
#
# FuzzySystem: Represents Fuzzy system that contains set of inputs (FuzzyInput), 
#              one output (FuzzyOutput) and set of Rules (Rule). How it works (self.fit(X)):
#
# Process: 
# 1. For every F(i) in FuzzyInput: Calculate membership of element X(i) for every M(j) (MFInput) in F(i);
# 2. Apply rules. This calculates membership value for every MFOutput in FuzzyOutput;
# 3. Calculate final output value as centroid of all MFOutput values.


import numpy as np
import matplotlib.pyplot as plt
from utils import constants
import pickle

from enum import Enum, unique
@unique
class Logic(Enum):
    OR = 0
    AND = 1

class MFInput:
    def __init__(self, name, xs, ys):
        self.name = name
        self.points = np.array(list(zip(xs, ys)))
        self.size = xs.size
        self.x0 = None
        self.mi = None
    
    def setMi(self, x0):
        # x0 - input value
        self.x0 = x0
        self.mi = self.getMi()
        
    def getY(self, x1, y1, x2, y2):
        # Calculates y value using triangle similarity theorem
        if y1 == y2:
            return y1
        if y1 < y2:
            return (self.x0 - x1) / (x2 -x1)
        return (x2 - self.x0) / (x2 - x1)
        
    def getMi(self):
        if self.x0 <= self.points[0][0]: 
            return self.points[0][1]
        if self.x0 >= self.points[-1][0]:
            return self.points[-1][1]
        for i in range(1, self.size):
            x1 = self.points[i - 1][0]
            x2 = self.points[i][0]
            if self.x0 >= x1 and self.x0 < x2:
                y1 = self.points[i - 1][1]
                y2 = self.points[i][1]
                return self.getY(x1, y1, x2, y2)
        return None
        
    def __str__(self):
        out = '['
        for (x, y) in self.points:
            out = out + '(' + str(x) + ',' + str(y) + '), '
        out = out[:-2] + ']'
        return out
    
    def show_diagram(self):
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]
        print(self.name)
        print(xs)
        print(ys)
        
        plt.ylim(-0.1, 1.4)
        plt.xlabel('input value')
        plt.ylabel(self.name + ' value')
        plt.title('Fuzzy Diagram')
        plt.plot(xs, ys, 'k')
        
        plt.plot([self.x0, self.x0], [0, self.mi], 'ro--')

class MFOutput:
    def __init__(self, name, xs, ys):
        self.name = name
        self.points = np.array(list(zip(xs, ys)))
        self.size = xs.size
        
        # Calculates center position (used for centroid method)
        self.center = None
        sum1 = 0
        cnt1 = 0
        for i in range(0, self.size):
            if ys[i] == 1:
                sum1 = sum1 + xs[i]
                cnt1 = cnt1 + 1
        self.center = sum1/cnt1
        self.mi = 0

    def __str__(self):
        out = '['
        for (x, y) in self.points:
            out = out + '(' + str(x) + ',' + str(y) + '), '
        out = out[:-2] + ']'
        return out
        
    def show_diagram(self, solution):
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]

        plt.ylim(-0.1, 1.4)
        plt.xlabel('output')
        plt.ylabel(self.name + ' value')
        plt.title('Fuzzy Diagram')
        plt.plot(xs, ys, 'k')
        
        plt.plot([solution, solution], [0, 1], 'ro--')

class Rule:
    def __init__(self, inputs, output, operator = Logic.AND):
        self.inputs = inputs
        self.output = output
        self.operator = operator
    
    def apply_rule(self):
        # Updates output variable based on given operator
        n = self.inputs.size
        if self.operator == Logic.OR:
            mi = 0
            for i in range(0, n):
                mi = max(mi, self.inputs[i].mi)
        else:
            mi = 1
            for i in range(0, n):
                mi = min(mi, self.inputs[i].mi)

        # Union of all rules    
        self.output.mi = max(self.output.mi, mi)
        
    def __str__(self):
        n = self.inputs.size
        out = ''
        for i in range(0, n-1):
            out = out + self.inputs[i].name + ' ' + str(self.operator) + ' '
        out = out + self.inputs[n-1].name
        return out

class FuzzyInput:
    def __init__(self, name, inputs):
        self.name = name
        self.inputs = inputs
        self.size = self.inputs.size
    
    def __getitem__(self, index):
         return self.inputs[index]
        
    def __str__(self):
        return self.name + " : " + str([str(element) for element in self.inputs])
    
    def show_diagram(self):
        for i in range(0, self.size):
            self.inputs[i].show_diagram()
        plt.ylabel(self.name)   
        plt.show()

class FuzzyOutput:
    def __init__(self, name, outputs):
        self.name = name
        self.outputs = outputs
        self.size = self.outputs.size
    
    def __getitem__(self, index):
         return self.outputs[index]
        
    def __str__(self):
        return self.name + " : " + str([str(element) for element in self.outputs])
    
    def show_diagram(self, solution):
        for i in range(0, self.size):
            self.outputs[i].show_diagram(solution)

        plt.ylabel(self.name)
        plt.show()

class FuzzyRules:
    def __init__(self, rules):
        self.rules = rules
        self.size = self.rules.size
        self.size = self.rules.size
    
    def __getitem__(self, index):
         return self.rules[index]
        
    def __str__(self):
        out = ''
        for i in range(0, self.size):
            out = out + str(self.rules[i]) + '\n'
        return out

class FuzzySystem:
    def __init__(self, inputs, output, rules):
        self.inputs = inputs
        self.output = output
        self.rules = rules
        self.solution = None
        
    def fit(self, x0s):
        # Restarting output mis
        for mfo in self.output:
            mfo.mi = 0

        # Fazzification
        # Calculate input membership values
        for i in range(0, self.inputs.size):
            x0 = x0s[i]
            for j in range(0, self.inputs[i].size):
                self.inputs[i][j].setMi(x0)
            
        # Apply rules
        for i in range(0, self.rules.size):
            self.rules[i].apply_rule()

        # Defazzifaction   
        # Calculate output membership value (centroid method)
        numerator = 0
        denominator = 0 
        for mfo in self.output:
            numerator += mfo.mi * mfo.center
            denominator += mfo.mi
        if denominator == 0:
            self.solution = 0
        else:
            self.solution = numerator/denominator
        
    def inputs_info(self):
        if self.solution == None:
            return
        for i in range(0, self.inputs.size):
            self.inputs[i].show_diagram()
            
    def output_info(self):
        if self.solution == None:
            return
        self.output.show_diagram(self.solution)
        
    def full_info(self):
        self.inputs_info()
        self.output_info()

    def __str__(self):
        out = ''
        for member in self.inputs:
            out = out + member.name + '\n'
            for m in member:
                out = out + '\t' + str(m)
                out = out + '\n'

        out = out + self.output.name + '\n'
        for m in self.output:
            out = out + '\t' + str(m) + '\n'
        return out

if __name__ == '__main__':
    with open(constants.PRETRAINED_FUZZY_PATH, 'rb') as f:
        fz = pickle.load(f)
    
    FSAngle, FSVelocity = fz

    FSInput = np.array([3, 30, 15])
    FSAngle.fit(FSInput)
    FSVelocity.fit(FSInput)
    print('Angle in degrees: ' + str(FSAngle.solution))
    print('Velocity: ' + str(FSVelocity.solution))
    FSAngle.full_info()
    FSVelocity.full_info()