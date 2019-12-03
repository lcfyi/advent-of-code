from math import inf

# Path is a tuple from the starting to end


def get_least_timing(timing, place, path, orthogo_paths):
    least_timing = inf
    additional_timing = -1
    modifier = -1 if path[0] > path[1] else 1
    for num in range(path[0], path[1] + modifier, modifier):
        additional_timing += 1
        if num in orthogo_paths:
            # Normal
            if orthogo_paths[num][0] < orthogo_paths[num][1]:
                if orthogo_paths[num][0] <= place and orthogo_paths[num][1] >= place:
                    potential_timing = timing + additional_timing + \
                        orthogo_paths[num][2] + place - orthogo_paths[num][0]
                    if potential_timing != 0 and potential_timing < least_timing:
                        least_timing = potential_timing
            # Reversed
            else:
                if orthogo_paths[num][1] <= place and orthogo_paths[num][0] >= place:
                    potential_timing = timing + additional_timing + \
                        orthogo_paths[num][2] + orthogo_paths[num][0] - place
                    if potential_timing != 0 and potential_timing < least_timing:
                        least_timing = potential_timing
    return least_timing


def process_first_wire(horizontal, vertical, first_wire_path):
    point = [0, 0]  # x, y
    timing = 0
    for path in first_wire_path:
        direction = path[0]
        magnitude = int(path[1:])
        if direction == "L":
            new_x = point[0] - magnitude
            horizontal[point[1]] = (point[0], new_x, timing)
            point[0] = new_x
        if direction == "R":
            new_x = point[0] + magnitude
            horizontal[point[1]] = (point[0], new_x, timing)
            point[0] = new_x
        if direction == "U":
            new_y = point[1] + magnitude
            vertical[point[0]] = (point[1], new_y, timing)
            point[1] = new_y
        if direction == "D":
            new_y = point[1] - magnitude
            vertical[point[0]] = (point[1], new_y, timing)
            point[1] = new_y
        timing += magnitude


def get_closest_crossing_timing(horizontal, vertical, second_wire_path):
    point = [0, 0]  # x, y
    timing = 0
    least_timing = inf
    for path in second_wire_path:
        direction = path[0]
        magnitude = int(path[1:])
        if direction == "L":
            new_x = point[0] - magnitude
            potential_timing = get_least_timing(
                timing, point[1], (point[0], new_x), vertical)
            point[0] = new_x
        if direction == "R":
            new_x = point[0] + magnitude
            potential_timing = get_least_timing(
                timing, point[1], (point[0], new_x), vertical)
            point[0] = new_x
        if direction == "U":
            new_y = point[1] + magnitude
            potential_timing = get_least_timing(
                timing, point[0], (point[1], new_y), horizontal)
            point[1] = new_y
        if direction == "D":
            new_y = point[1] - magnitude
            potential_timing = get_least_timing(
                timing, point[0], (point[1], new_y), horizontal)
            point[1] = new_y
        timing += magnitude
        if potential_timing < least_timing:
            least_timing = potential_timing
    return least_timing


if __name__ == "__main__":
    # These dictionaries specify the points at which there's a wire,
    # and maps to a tuple that specifies the range and also timing
    # For example, if there's a vertical line from 10 to 50 at y = 10,
    # while having a timing of 25 to the START of that leg, then we'll
    # get a dict entry of {10: (10, 50, 25)}
    # It also differs slightly because start and end are not by magnitude anymore
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
        print(get_closest_crossing_timing(first_wire_horizontal,
                                          first_wire_vertical, second_wire_path))
