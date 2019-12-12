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
    this.position.x += this.velocity.x;
    this.position.y += this.velocity.y;
    this.position.z += this.velocity.z;
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
  let args = [];
  line
    .replace("<", "")
    .replace(">", "")
    .split(",")
    .forEach(e => args.push(parseInt(e.split("=")[1])));
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

for (let i = 0; i < 1000; i++) {
  step(moons);
}

let tot = 0;

moons.forEach(moon => {
  tot += moon.energy();
});

console.log("Total energy:", tot);
