class Tuple {
  constructor(x, y, z) {
    this.x = x;
    this.y = y;
    this.z = z;
  }
}

class Moon {
  constructor(x, y, z) {
    this.position = new Tuple(x, y, z);
    this.velocity = new Tuple(0, 0, 0);
    this.x = x;
    this.y = y;
    this.z = z;
    this.xSet = new Set();
    this.ySet = new Set();
    this.zSet = new Set();
    this.count = 0;
  }

  // For the velocity changes, position influencing
  influence(moon) {
    if (this.position.x < moon.position.x) {
      this.velocity.x += 1;
    } else if (this.position.x > moon.position.x) {
      this.velocity.x -= 1;
    }
    if (this.position.y < moon.position.y) {
      this.velocity.y += 1;
    } else if (this.position.y > moon.position.y) {
      this.velocity.y -= 1;
    }
    if (this.position.z < moon.position.z) {
      this.velocity.z += 1;
    } else if (this.position.z > moon.position.z) {
      this.velocity.z -= 1;
    }
  }

  // For the position movements based on velocity
  move() {
    this.count++;
    this.position.x += this.velocity.x;
    this.position.y += this.velocity.y;
    this.position.z += this.velocity.z;
    if (this.position.x === this.x && this.velocity.x === 0) {
      this.xSet.add(this.count);
    }
    if (this.position.y === this.y && this.velocity.y === 0) {
      this.ySet.add(this.count);
    }
    if (this.position.z === this.z && this.velocity.z === 0) {
      this.zSet.add(this.count);
    }
  }

  energy() {
    let pot =
      Math.abs(this.position.x) +
      Math.abs(this.position.y) +
      Math.abs(this.position.z);
    let kin =
      Math.abs(this.velocity.x) +
      Math.abs(this.velocity.y) +
      Math.abs(this.velocity.z);
    return pot * kin;
  }
}

const fs = require("fs");

let file = fs.readFileSync("input.txt");

// Read lines
let data = file.toString().split("\n");

let moons = [];

data.forEach(line => {
  let args = line
    .replace("<", "")
    .replace(">", "")
    .split(",")
    .map(e => parseInt(e.split("=")[1]));
  moons.push(new Moon(args[0], args[1], args[2]));
});

let step = m => {
  m.forEach(m1 => {
    m.forEach(m2 => {
      m1.influence(m2);
    });
  });
  m.forEach(m1 => m1.move());
};

let lcm = (first, second) => {
  let r;
  let a = first;
  let gcd = second;
  while (a % gcd > 0) {
    r = a % gcd;
    a = gcd;
    gcd = r;
  }

  return (first * second) / gcd;
};

let x;
let y;
let z;

while (true) {
  step(moons);

  // Find the intersection of all the sets
  x = moons.reduce((prev, m) => {
    return new Set([...prev].filter(e => m.xSet.has(e)));
  }, moons[0].xSet);
  y = moons.reduce((prev, m) => {
    return new Set([...prev].filter(e => m.ySet.has(e)));
  }, moons[0].ySet);
  z = moons.reduce((prev, m) => {
    return new Set([...prev].filter(e => m.zSet.has(e)));
  }, moons[0].zSet);

  if (x.size > 0 && y.size > 0 && z.size > 0) {
    break;
  }
}

let sets = [x, y, z];

let mins = sets.map(s => {
  let min = Number.MAX_VALUE;
  s.forEach(e => {
    if (e < min) {
      min = e;
    }
  });
  return min;
});

let result = mins.reduce((prev, curr) => {
  return lcm(prev, curr);
}, 1);

console.log("Period:", result);
