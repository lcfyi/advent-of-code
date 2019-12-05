inputs = []

OPCODE_OFFSETS = {
    "01": 4,
    "02": 4,
    "03": 2,
    "04": 2,
    "05": 3,
    "06": 3,
    "07": 4,
    "08": 4,
    "99": 1,
}

OPCODE_PARAM_COUNT = {
    "01": 3,
    "02": 3,
    "03": 1,
    "04": 1,
    "05": 2,
    "06": 2,
    "07": 3,
    "08": 3,
    "99": 1
}

def standardize_opcode(opcode):
    opcode = str(opcode)
    if len(opcode) != 2:
        opcode = "0" + opcode
    return opcode

def get_input(location):
    inputs[int(location)] = input("Input:")

def get_value(value):
    print("Value was:", value)

def position_mode(value):
    return inputs[value]

def immediate_mode(value):
    return value

OPCODE_OPS = {
    "01": lambda a, b: int(a) + int(b),
    "02": lambda a, b: int(a) * int(b),
    "03": get_input,
    "04": get_value,
    "05": lambda a: int(a) != 0,
    "06": lambda a: int(a) == 0,
    "07": lambda a, b: int(a) < int(b),
    "08": lambda a, b: int(a) == int(b)
}

PARAMETER_MODES = {
    "0": position_mode,
    "1": immediate_mode
}

def pad_positions(raw, opcode):
    ret = raw
    while len(ret) != OPCODE_PARAM_COUNT[opcode]:
        ret = "0" + ret
    return ret


def process_opcode(opcode, position):
    temp = str(opcode)
    opcode = standardize_opcode(temp[-2:])
    positions = pad_positions(temp[:-2], opcode)

    params = []
    offset = 1
    while positions != "":
        pos = positions[-1:]
        params.append(PARAMETER_MODES[pos](inputs[position + offset]))
        offset += 1
        positions = positions[:-1]

    if opcode == "01":
        inputs[inputs[position + 3]] = OPCODE_OPS[opcode](params[0], params[1])

    if opcode == "02":
        inputs[inputs[position + 3]] = OPCODE_OPS[opcode](params[0], params[1])

    if opcode == "03":
        OPCODE_OPS[opcode](inputs[position + 1])

    if opcode == "04":
        OPCODE_OPS[opcode](params[0])

    if opcode == "05":
        return params[1] if OPCODE_OPS[opcode](params[0]) else -1

    if opcode == "06":
        return params[1] if OPCODE_OPS[opcode](params[0]) else -1

    if opcode == "07":
        inputs[inputs[position + 3]] = 1 if OPCODE_OPS[opcode](params[0], params[1]) else 0

    if opcode == "08":
        inputs[inputs[position + 3]] = 1 if OPCODE_OPS[opcode](params[0], params[1]) else 0

    if opcode == "99":
        pass

    return -1

def crunch():
    index = 0
    curr = inputs[index]
    while curr != 99:
        opcode = standardize_opcode(str(curr)[-2:])
        result = process_opcode(curr, index)
        if result != -1:
            index = result
        else:
            index = index + OPCODE_OFFSETS[opcode]
        curr = inputs[index]


STRATEGIES = {
    "coarse": lambda noun, verb: (noun + 1, verb),
    "fine": lambda noun, verb: (noun, verb + 1)
}

with open("input.txt", "r") as file:
    data = file.read()
    inputs = list(map(lambda a: int(a), data.split(",")))
    crunch()
