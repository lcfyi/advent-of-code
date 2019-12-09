class Computer {
    OFFSETS = {
      1: 4,
      2: 4,
      3: 2,
      4: 2,
      5: 3,
      6: 3,
      7: 4,
      8: 4,
      9: 2,
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
      9: 1,
      99: 1
    };
  
    PARAM_WHITELIST = [1, 2, 3, 4, 7, 8];
  
    ADDITIONAL_MEM = 5000;
  
    constructor(code, mode) {
      this.code = code.slice();
      for (let i = 0; i < this.ADDITIONAL_MEM; i++) {
        this.code.push(0);
      }
      this.ptr = 0;
      this.relativeBase = 0;
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
        if (this.PARAM_WHITELIST.includes(opc) && i === this.PARAMS[opc]) {
          params.push(
            {
              0: () => {
                return this.code[this.ptr + i];
              },
              1: () => {
                return this.ptr + i;
              },
              2: () => {
                return this.code[this.ptr + i] + this.relativeBase;
              }
            }[pos]()
          );
        } else {
          params.push(
            {
              0: () => {
                return this.code[this.code[this.ptr + i]];
              },
              1: () => {
                return this.code[this.ptr + i];
              },
              2: () => {
                return this.code[this.code[this.ptr + i] + this.relativeBase];
              }
            }[pos]()
          );
        }
        positions = Math.floor(positions / 10);
      }
  
      switch (opc) {
        case 1:
          this.code[params[2]] = params[0] + params[1];
          break;
        case 2:
          this.code[params[2]] = params[0] * params[1];
          break;
        case 3:
          // Wait for input
          if (this.input !== undefined) {
            this.code[params[0]] = this.input;
            this.input = undefined;
            break;
          } else {
            return -1;
          }
        case 4:
          this.output = this.code[params[0]];
          console.log("output", this.code[params[0]]);
          break;
        case 5:
          this.ptr = params[0] !== 0 ? params[1] : this.ptr + this.OFFSETS[opc];
          return;
        case 6:
          this.ptr = params[0] === 0 ? params[1] : this.ptr + this.OFFSETS[opc];
          return;
        case 7:
          this.code[params[2]] = params[0] < params[1] ? 1 : 0;
          break;
        case 8:
          this.code[params[2]] = params[0] === params[1] ? 1 : 0;
          break;
        case 9:
          this.relativeBase += params[0];
          break;
        default:
          break;
      }
  
      this.ptr += this.OFFSETS[opc];
    };
  
    crunch = () => {
      let curr = this.code[this.ptr];
  
      while (curr != 99) {
        this.process(curr);
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
  
  let c = new Computer(data, 2);
  console.log("final", c.get());