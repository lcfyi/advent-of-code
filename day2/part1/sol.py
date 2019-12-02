OPCODE_OFFSETS = {
    1: 4,
    2: 4,
    99: 1
}

OPCODE_OPS = {
    1: lambda a, b: a + b, 
    2: lambda a, b: a * b
}

with open("input.txt", "r") as file:
    data = file.read()
    inputs = list(map(lambda a: int(a), data.split(",")))
    inputs[1] = 12
    inputs[2] = 2
    index = 0
    curr = inputs[index]
    while curr != 99:
        curr_index = index
        inputs[inputs[index + 3]] = OPCODE_OPS[curr](inputs[inputs[index + 1]], inputs[inputs[index + 2]])
        index = curr_index + OPCODE_OFFSETS[curr]
        curr = inputs[index]

    print(inputs[0])
