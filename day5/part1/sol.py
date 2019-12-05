inputs = []

OPCODE_OFFSETS = {
    "01": 4,
    "02": 4,
    "03": 2,
    "04": 2,
    "99": 1
}

OPCODE_PARAM_COUNT = {
    "01": 3,
    "02": 3,
    "03": 1,
    "04": 1,
    "99": 1
}

def standardize_opcode(opcode):
    opcode = str(opcode)
    if len(opcode) != 2:
        opcode = "0" + opcode
    return opcode

def get_input(location):
    inputs[int(location)] = input()

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
    "04": get_value
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

    if opcode == "99":
        return

def crunch():
    index = 0
    curr = inputs[index]
    while curr != 99:
        opcode = standardize_opcode(str(curr)[-2:])
        process_opcode(curr, index)
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
