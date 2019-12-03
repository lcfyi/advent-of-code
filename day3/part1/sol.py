from math import inf

# Manhatten distance doesn't matter if x,y or y,x
def get_distance(crossing):
    return abs(crossing[0]) + abs(crossing[1])

# Path is a tuple from the starting to end
def get_least_distance(place, path, orthogo_paths):
    least_distance = inf
    for num in range(path[0], path[1] + 1):
        if num in orthogo_paths:
            if orthogo_paths[num][0] <= place and orthogo_paths[num][1] >= place:
                distance = get_distance((place, num))
                if distance < least_distance:
                    least_distance = distance
    return least_distance


def process_first_wire(horizontal, vertical, first_wire_path):
    point = [0, 0]  # x, y
    for path in first_wire_path:
        direction = path[0]
        magnitude = int(path[1:])
        if direction == "L":
            new_x = point[0] - magnitude
            horizontal[point[1]] = (new_x, point[0])
            point[0] = new_x
        if direction == "R":
            new_x = point[0] + magnitude
            horizontal[point[1]] = (point[0], new_x)
            point[0] = new_x
        if direction == "U":
            new_y = point[1] + magnitude
            vertical[point[0]] = (point[1], new_y)
            point[1] = new_y
        if direction == "D":
            new_y = point[1] - magnitude
            vertical[point[0]] = (new_y, point[1])
            point[1] = new_y


def get_closest_crossing_distance(horizontal, vertical, second_wire_path):
    point = [0, 0]  # x, y
    least_distance = inf
    for path in second_wire_path:
        direction = path[0]
        magnitude = int(path[1:])
        distance = None
        if direction == "L":
            new_x = point[0] - magnitude
            distance = get_least_distance(point[1], (new_x, point[0]), vertical)
            point[0] = new_x
        if direction == "R":
            new_x = point[0] + magnitude
            distance = get_least_distance(point[1], (point[0], new_x), vertical)
            point[0] = new_x
        if direction == "U":
            new_y = point[1] + magnitude
            distance = get_least_distance(point[0], (point[1], new_y), horizontal)
            point[1] = new_y
        if direction == "D":
            new_y = point[1] - magnitude
            distance = get_least_distance(point[0], (new_y, point[1]), horizontal)
            point[1] = new_y
        if distance < least_distance:
            least_distance = distance
    return least_distance



if __name__ == "__main__":
    # These dictionaries specify the points at which there's a wire,
    # and maps to a tuple that specifies the range
    # For example, if there's a vertical line from 10 to 50 at y = 10,
    # then we'll get a dict entry {10: (10, 50)}
    first_wire_vertical = dict()
    first_wire_horizontal = dict()

    first_wire_path = None
    second_wire_path = None

    with open("input.txt", "r") as file:
        data = file.readlines()

        first_wire_path = data[0].split(",")
        second_wire_path = data[1].split(",")
        process_first_wire(first_wire_horizontal,
                           first_wire_vertical, first_wire_path)
        print(get_closest_crossing_distance(first_wire_horizontal,
                                   first_wire_vertical, second_wire_path))
