import fuzzy

def generate_default_system():
    left = {
        "close"    : MFInput("close", np.array([0, 16]), np.array([1, 0])),
        "midrange" : MFInput("midrange", np.array([10, 14, 18, 24]), np.array([0, 1, 1, 0])),
        "far"      : MFInput("far", np.array([20, 36, 44]), np.array([0, 1, 0])),
        "very far" : MFInput("very far", np.array([32, 100]), np.array([0, 1]))
    }

    right = {
        "close"    : MFInput("close", np.array([0, 16]), np.array([1, 0])),
        "midrange" : MFInput("midrange", np.array([10, 16, 20, 28]), np.array([0, 1, 1, 0])),
        "far"      : MFInput("far", np.array([24, 40, 45]), np.array([0, 1, 0])),
        "very far" : MFInput("very far", np.array([35, 100]), np.array([0, 1]))
    }

    front = {
        "close"    : MFInput("close", np.array([0, 18]), np.array([1, 0])),
        "midrange" : MFInput("midrange", np.array([14, 20, 24, 28]), np.array([0, 1, 1, 0])),
        "far"      : MFInput("far", np.array([26, 34, 40]), np.array([0, 1, 0])),
        "very far" : MFInput("very far", np.array([35, 100]), np.array([0, 1])),
    }

    velocity = {
        "low"       : MFOutput("low", np.array([1, 2]), np.array([1, 0])),
        "middle"    : MFOutput("middle", np.array([1.5, 3, 3.5, 4]), np.array([0, 1, 1, 0])),
        "high"      : MFOutput("high", np.array([3.5, 4.5, 5.5]), np.array([0, 1, 0])),
        "very high" : MFOutput("very high", np.array([4, 8]), np.array([0, 1]))
    }

    angle = {
        "hard right" : MFOutput("hard right", np.array([25, 45]), np.array([1, 0])),
        "right"      : MFOutput("right", np.array([5, 22, 25]), np.array([0, 1, 0])),
        "forward"    : MFOutput("forward", np.array([-5, 0, 5]), np.array([0, 1, 0])),
        "left"       : MFOutput("left", np.array([-25, -22, -5]), np.array([0, 1, 0])),
        "hard left"  : MFOutput("hard left", np.array([-45, -25]), np.array([0, 1]))
    }

    left_sensor = FuzzyInput("left_sensor", np.array([
        left["close"],
        left["midrange"],
        left["far"],
        left["very far"]
    ]))

    right_sensor = FuzzyInput("right_sensor", np.array([
        right["close"],
        right["midrange"],
        right["far"],
        right["very far"]
    ]))

    front_sensor = FuzzyInput("front_sensor", np.array([
        front["close"],
        front["midrange"],
        front["far"],
        front["very far"] 
    ]))

    f_velocity = FuzzyOutput("velocity", np.array([
        velocity["low"],
        velocity["middle"],
        velocity["high"],
        velocity["very high"]
    ]))

    f_angle = FuzzyOutput("angle", np.array([
        angle["hard right"],
        angle["right"],
        angle["forward"],
        angle["left"],
        angle["hard left"]
    ]))

    return left_sensor, right_sensor, front_sensor, f_velocity, f_angle 