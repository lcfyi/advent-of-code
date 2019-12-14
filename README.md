# Make a new day

```bash
./start.sh <day_num>
```

It'll randomly choose either a `C`, `C++`, `Java`, `Python`, or `JavaScript` starter. 

# Notes

## Day 1: The Tyranny of the Rocket Equation (Python)

Calculation of fuel. Done recursively.

## Day 2: 1202 Program Alarm (Python)

IntCode part 1. Simple parse and modify array.

## Day 3: Crossed Wires (Python)

Finding the closest intersection.
Finding the least Manhattan distance between the origin and crosses. Looked for horizontal and vertical slices and tracked their intersections to calculate the min distance. 

For part 1, the intersection with the least Manhattan distance was determined by creating a map of horizontal slices, then determining the intersections per vertical slice. The closest distance was tracked and returned.

For part 2, the same was done but with some additional logic to track the least raw distance instead of Manhattan distance.

## Day 4: Secure Container (C, Python)

Cracking the code.

For part 1, the range was simply bruteforced to count the number of valid passwords.

For part 2, the same was done but with new constraints. 

## Day 5: Sunny with a Chance of Asteroids (Python)

IntCode part 2. Added inputs and parameter intermediate mode.

## Day 6: Universal Orbit Map (Java)

Orbits. For part 1, a tree was built using a map of the parent to the orbiting planets, then traversed the tree to count the orbits. For part 2, the tree was traversed and the path from `YOU` to `SAN` was calculated at each node to find the shortest distance.

Could be optimized using a LCA approach to eliminate unnecessary traversals, or using sets to track the path to each element and taking the size of the intersection. 

## Day 7: Amplification Circuit (JavaScript)

IntCode part 3. Multiple instances of the IntCode computers were connected together.

## Day 8: Space Image Format (C++)

Images represented by a string were parsed for each image, with their attributes tracked during parse. 

Part 1 simply tracked the section of the input that had the least 0s, before returning the count of 1s and 2s.

Part 2 began with the same parsed dataset, but with each image string iterated on to generate a "running total" for the final string; any `2` was replaced with the current string's value at that same location. The final string was then printed based on the dimensions.

## Day 9: Sensor Boost (JavaScript)

IntCode part 4. Added support for relative mode. 

## Day 10: Monitoring Station (Java)

Finding the best asteroid to sit on and blasting them out of space. 

For part 1, the asteroid field was read into a 2D array. Each asteroid was then assigned a visible asteroid count by doing a BFS from its location to scan for the other asteroids in the field, assigning them their raw angle components (x, y). If that angle already exists, the visible asteroid count isn't incremented. The max count was returned.

For part 2, part 1 was repeated to determine the best asteroid to put the monitoring station. Another BFS was then done to create a map of the raw angle components (x, y) to a queue of the asteroids (they will be appended in order at which we grow outward). Finally, we determine the order at which we pop from those lists (one from a list at a time) by sorting the queues by their angle until there aren't any elements left. 

## Day 11: Space Police (Java)

Using the IntCode computer to draw on your ship.

For part 1, the computer was run, and the number of unique (x, y) coordinates were tracked. 

For part 2, the computer simply drew to a 2D array that was printed after the computer halted.

## Day 12: The N-Body Problem (JavaScript)

The universe, simulated.

For part 1, a Moon object was created, which exposed a method to allow another moon to influence its parameters. The final energy value was then printed for the answer.

For part 2, the x,y,z components were independent, so the moons tracked their respective axes' periods (at which they returned to equilibrium). The simulation was run until the intersection of all the moon's axes (x for all the moons, y for all the moons, z for all the moons) had at least one element. The result then came from the LCM of the least elements of each set (for x, y, z).

## Day 13: Care Package (Java)

Block breaker! 

For part 1, the IntCode computer was run until completion, and the number of block tiles were tracked.

For part 2, the game was played by tracking the ball's position, and giving the corresponding input (move left, move right, stay) to keep the paddle under the ball. The game was played to completion before printing out the score. 

## Day 14: Space Stoichiometry (JavaScript)

Factorio, basically. 

For part 1, the file was parsed into a map of the element to the amount produced and the components required. The target element (in this case, FUEL) was then passed into a recursive function that tracked the number of excess materials we had; we continue to create elements (unless we had excess) until we hit the base case (the resource being ORE).

For part 2, part 1 was repeated many times until we found the right fuel amount to create. This was done by doing a binary search on a large search space.