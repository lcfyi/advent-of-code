OPCODE_OFFSETS = {
    1: 4,
    2: 4,
    99: 1
}

OPCODE_OPS = {
    1: lambda a, b: a + b,
    2: lambda a, b: a * b
}


def crunch(list, noun, verb):
    copy_of_list = list.copy()
    copy_of_list[1] = noun
    copy_of_list[2] = verb
    index = 0
    curr = copy_of_list[index]
    while curr != 99:
        curr_index = index
        copy_of_list[copy_of_list[index + 3]] = OPCODE_OPS[curr](
            copy_of_list[copy_of_list[index + 1]], copy_of_list[copy_of_list[index + 2]])
        index = curr_index + OPCODE_OFFSETS[curr]
        curr = copy_of_list[index]
    return copy_of_list[0]

TARGET = 19690720

STRATEGIES = {
    "coarse": lambda noun, verb: (noun + 1, verb),
    "fine": lambda noun, verb: (noun, verb + 1)
}

with open("input.txt", "r") as file:
    data = file.read()
    inputs = list(map(lambda a: int(a), data.split(",")))
    output = 0
    noun = 0
    verb = 0
    strategy = STRATEGIES["coarse"]
    while output != TARGET:
        output = crunch(inputs, noun, verb)
        if output > TARGET:
            strategy = STRATEGIES["fine"]
            noun -= 1
        elif output == TARGET:
            break
        else:
            noun, verb = strategy(noun, verb)
    
    print(noun, verb)
    print("Solution:", 100 * noun + verb)