from functools import reduce

def verify_monotonic(a, b):
    if a == -1:
        return -1
    elif int(a) <= int(b):
        return b
    else:
        return -1

def verify_number(num):
    result = reduce(verify_monotonic, str(num))

    if result == -1:
        return False

    counts = []
    last = None
    count = 0
    for n in str(num):
        if not last:
            last = n
            count = 1
        elif n == last:
            count += 1
            last = n
        else:
            counts.append(count)
            last = n
            count = 1
    counts.append(count)
    
    for count in counts:
        if count == 2:
            return True

    return False
    
with open("input.txt", "r") as file:
    data = file.read()
    start, end = map(lambda a: int(a), data.split("-"))

    count = 0

    for n in range(start, end + 1):
        if verify_number(n):
            count += 1
    
    print(count)
