from collections import deque

file = open("input.txt", "r")
data = [int(x) for x in file.read()]

# Generate the full sequence and get the offset
numbers = [n for _ in range(10000) for n in data]
offset = int("".join(map(lambda a: str(a), numbers[0:7])))


def calculate_phase(indata, iters):
    output = indata
    for _ in range(iters):
        curr_sum = 0
        for i, n in enumerate(output):
            curr_sum = (n + curr_sum) % 10
            output[i] = curr_sum
    return output


# Get the numbers after the offset; it's beyond the halfway mark
numbers = numbers[offset:]
numbers = list(reversed(numbers))

result = calculate_phase(numbers, 100)

print("Solution:", "".join(map(lambda a: str(a), list(reversed(result))[0:8])))
