import math

with open("input.txt", "r") as file:
    data = file.readlines()
    count = 0
    for x in data:
        count += math.floor(int(x) / 3) - 2
    print(count)