import fuzzy

def generate_default_system():
    left_sensor = fuzzy.FuzzyInput("left_sensor", np.array([
        fuzzy.MFInput("close", np.array([0, 12]), np.array([1, 0])),
        fuzzy.MFInput("midrange", np.array([10, 16, 20, 28]), np.array([0, 1, 1, 0])),
        fuzzy.MFInput("far", np.array([24, 40, 45]), np.array([0, 1, 0])),
        fuzzy.MFInput("very far", np.array([35, 100]), np.array([0, 1])),
    ]))

    right_sensor = fuzzy.FuzzyInput("right_sensor", np.array([
        fuzzy.MFInput("close", np.array([0, 12]), np.array([1, 0])),
        fuzzy.MFInput("midrange", np.array([10, 16, 20, 28]), np.array([0, 1, 1, 0])),
        fuzzy.MFInput("far", np.array([24, 40, 45]), np.array([0, 1, 0])),
        fuzzy.MFInput("very far", np.array([35, 100]), np.array([0, 1])),
    ]))

    front_sensor = fuzzy.FuzzyInput("front_sensor", np.array([
        fuzzy.MFInput("close", np.array([0, 10]), np.array([1, 0])),
        fuzzy.MFInput("midrange", np.array([6, 10, 12, 14]), np.array([0, 1, 1, 0])),
        fuzzy.MFInput("far", np.array([12, 20]), np.array([0, 1])),
    ]))

    velocity = fuzzy.FuzzyOutput("velocity", np.array([
        fuzzy.MFOutput("low", np.array([0.5, 1.5]), np.array([1, 0])),
        fuzzy.MFOutput("middle", np.array([1, 1.5, 2, 2.5]), np.array([0, 1, 1, 0])),
        fuzzy.MFOutput("high", np.array([2, 3]), np.array([0, 1])),
    ]))

    angle = fuzzy.FuzzyOutput("angle", np.array([
        fuzzy.MFOutput("left", np.array([10, 45]), np.array([1, 0])),
        fuzzy.MFOutput("forward", np.array([-10, 0, 10]), np.array([0, 1, 0])),
        fuzzy.MFOutput("right", np.array([-45, -10]), np.array([0, 1])),
    ]))
    return left_sensor, right_sensor, front_sensor, velocity, angle 