import math

def fuel_counter(input):
    if input <= 6:
        return 0
    new_amount = math.floor(input / 3) - 2
    return new_amount + fuel_counter(new_amount)

with open("input.txt", "r") as file:
    data = file.readlines()
    count = 0
    for x in data:
        count += fuel_counter(int(x))
    print(count)