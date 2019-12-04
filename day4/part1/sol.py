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
    
    last = None
    for n in str(num):
        if not last:
            last = n
        elif n == last:
            return True
        else:
            last = n

    return False
    
with open("input.txt", "r") as file:
    data = file.read()
    start, end = map(lambda a: int(a), data.split("-"))

    count = 0

    for n in range(start, end + 1):
        if verify_number(n):
            count += 1
    
    print(count)
