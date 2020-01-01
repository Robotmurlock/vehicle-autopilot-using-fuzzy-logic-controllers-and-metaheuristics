def apply_scaling(sx, sy, coords):
    scaled_coords = []

    for x, y in coords:
        scaled_coords.append((x * sx, y * sy))
    
    return scaled_coords

def apply_translation(dx, dy, coords):
    translated_coords = []

    for x, y in coords:
        translated_coords.append((x + dx, y + dy))
    
    return translated_coords
def main():
    pass

if __name__ == "__main__":
    main()