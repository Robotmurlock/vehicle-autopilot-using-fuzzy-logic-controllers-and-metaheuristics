COORD_X = 0
COORD_Y = 1

def far_left(coords):
    left_point = coords[0]
    idx = 0

    for i in range(1, len(coords)):
        if(coords[i][COORD_X] < left_point[COORD_X] or (coords[i][COORD_X] == left_point[COORD_X] and coords[i][COORD_Y] < left_point[COORD_Y])):
            left_point = coords[i]
            idx = i
    return idx

def orientation(A, B, C):

    dist = (B[COORD_X] - A[COORD_X]) * (C[COORD_Y] - A[COORD_Y]) - (C[COORD_X] - A[COORD_X]) * (B[COORD_Y] - A[COORD_Y])
    return dist

def gift_wrap(coords):
    left_point_idx = far_left(coords)
    current_point_idx = left_point_idx

    polygon = []
    
    first_iteration = True
    while True:
        first_iteration = False
        polygon.append(coords[current_point_idx])

        next_point_idx = (current_point_idx + 1) % len(coords)

        for i in range(len(coords)):
            if orientation(coords[current_point_idx], coords[next_point_idx], coords[i]) < 0:
                next_point_idx = i
        
        current_point_idx = next_point_idx

        if(current_point_idx == left_point_idx):
            break
    
    return polygon
    

