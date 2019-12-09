class Amplifier {
  OFFSETS = {
    1: 4,
    2: 4,
    3: 2,
    4: 2,
    5: 3,
    6: 3,
    7: 4,
    8: 4,
    99: 1
  };

  PARAMS = {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
    99: 1
  };

  constructor(code, mode) {
    this.code = code.slice();
    this.ptr = 0;
    this.input = mode;
    this.output = undefined;
    this.crunch();
  }

  send = val => {
    if (val !== undefined) {
      this.input = val;
      return this.crunch();
    }
  };

  process = opcode => {
    let opc = opcode % 100;
    let positions = Math.floor(opcode / 100);

    let params = [];

    for (let i = 1; i <= this.PARAMS[opc]; i++) {
      let pos = positions % 10;
      params.push(
        {
          0: () => {
            return this.code[this.code[this.ptr + i]];
          },
          1: () => {
            return this.code[this.ptr + i];
          }
        }[pos]()
      );
      positions = Math.floor(positions / 10);
    }

    switch (opc) {
      case 1:
        this.code[this.code[this.ptr + 3]] = params[0] + params[1];
        break;
      case 2:
        this.code[this.code[this.ptr + 3]] = params[0] * params[1];
        break;
      case 3:
        // Wait for input
        if (this.input !== undefined) {
          this.code[this.code[this.ptr + 1]] = this.input;
          this.input = undefined;
          break;
        } else {
          return -1;
        }
      case 4:
        this.ptr = this.ptr + this.OFFSETS[opc];
        this.output = params[0];
        return params[0];
      case 5:
        this.ptr = params[0] !== 0 ? params[1] : this.ptr + this.OFFSETS[opc];
        return;
      case 6:
        this.ptr = params[0] === 0 ? params[1] : this.ptr + this.OFFSETS[opc];
        return;
      case 7:
        this.code[this.code[this.ptr + 3]] = params[0] < params[1] ? 1 : 0;
        break;
      case 8:
        this.code[this.code[this.ptr + 3]] = params[0] === params[1] ? 1 : 0;
        break;
      default:
        break;
    }

    this.ptr += this.OFFSETS[opc];
  };

  crunch = () => {
    let curr = this.code[this.ptr];

    while (curr != 99) {
      let result = this.process(curr);
      if (result) {
        if (result === -1) {
          break;
        } else {
          return result;
        }
      }
      curr = this.code[this.ptr];
    }
  };

  halted = () => {
    return this.code[this.ptr] === 99;
  };

  get = () => {
    return this.output;
  };
}

const fs = require("fs");

let file = fs.readFileSync("input.txt");

let data = file
  .toString()
  .split(",")
  .map(e => parseInt(e));

let computeValues = seq => {
  let amps = seq.map(s => new Amplifier(data, s));

  return amps.reduce((last, curr) => {
    return curr.send(last);
  }, 0);
};

let perm = arr => {
  let ret = [];

  for (let i = 0; i < arr.length; i++) {
    let rest = perm([...arr.slice(0, i), ...arr.slice(i + 1)]);

    if (!rest.length) {
      ret.push([arr[i]]);
    } else {
      for (let j = 0; j < rest.length; j++) {
        ret.push([arr[i], ...rest[j]]);
      }
    }
  }

  return ret;
};

let max = 0;

perm([0, 1, 2, 3, 4]).map(s => {
  let m = computeValues(s);
  if (m > max) {
    max = m;
  }
});

console.log(max);
