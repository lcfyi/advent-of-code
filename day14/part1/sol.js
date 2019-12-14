const fs = require("fs");

let file = fs.readFileSync("input.txt");

let data = file.toString().split("\n");

// Keep track of the resource, its yield, and output
let resourceToCost = new Map();

// Parse the file
data.forEach(line => {
  line = line.split("=>");

  let resource = line[1].split(" ").filter(e => e.length !== 0);

  let key = resource[1];
  key[resource[1]] = parseInt(resource[0]);

  let cost = line[0]
    .split(",")
    .map(e => e.split(" ").filter(e => e.length !== 0));

  let value = { amount: resource[0], cost: [] };

  cost.forEach(e => {
    let elem = {};
    elem[e[1]] = parseInt(e[0]);
    value.cost.push(elem);
  });

  resourceToCost.set(key, value);
});

// Recursively find the resources we need
let getOreCount = (currentResources, resource, amount) => {
  // Base case
  if (resource === "ORE") return amount;

  let count = 0;

  // Get yield of resource
  let resYield = parseInt(resourceToCost.get(resource).amount);

  // Get the number of times we'll have to repeat this resource
  let iters = 1;

  // Check if we have excess of this resource
  if (currentResources.has(resource)) {
    let avail = currentResources.get(resource);

    // Do we have any available?
    if (avail - amount >= 0) {
      currentResources.set(resource, avail - amount);
      return count;
    } else {
      if (avail + resYield * iters - amount < 0) {
        iters = Math.floor((amount - avail) / resYield);
      }
      while (avail + resYield * iters - amount < 0) {
        iters++;
      }
      currentResources.set(resource, avail + resYield * iters - amount);
    }
  } else {
    if (resYield * iters - amount < 0) {
      iters = Math.floor(amount / resYield);
    }
    while (resYield * iters - amount < 0) {
      iters++;
    }
    currentResources.set(resource, resYield * iters - amount);
  }

  // If we get to this point, then make more of this resource
  resourceToCost.get(resource).cost.forEach(res => {
    for (let r in res) {
      count += getOreCount(currentResources, r, res[r] * iters);
    }
  });

  return count;
};

console.log("Total ore:", getOreCount(new Map(), "FUEL", 1));
