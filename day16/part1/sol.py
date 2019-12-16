file = open("input.txt", "r")
numbers = [int(x) for x in file.read()]
pattern = [0, 1, 0, -1]


def pattern_gen(iter, pattern):
    first = True
    while True:
        for n in pattern:
            for _ in range(iter + 1):
                if first:
                    first = False
                    continue
                yield n


def calculate_phase(indata, pattern, iters):
    output = indata
    for _ in range(iters):
        temp = []
        for i in range(len(output)):
            total = 0
            for val, pat in zip(output, pattern_gen(i, pattern)):
                total += val * pat
            temp.append(abs(total) % 10)
        output = temp
    return output


result = calculate_phase(numbers, pattern, 100)
print("Output:", "".join(map(lambda a: str(a), result[0:8])))
