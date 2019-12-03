#/bin/zsh

if [ -z "$1" ]
    then echo "No day."
    exit 1
fi

starters[0]="starter.c"
starters[1]="starter.cpp"
starters[2]="starter.java"
starters[3]="starter.js"
starters[4]="starter.py"

sol[0]="sol.c"
sol[1]="sol.cpp"
sol[2]="sol.java"
sol[3]="sol.js"
sol[4]="sol.py"

choice=$[$RANDOM % ${#starters[@]}]

# Reroll
rm -rf "day$1"

# Make the directory
mkdir "day$1"

# # Create part 1
mkdir "day$1/part1"
touch "day$1/part1/README.md"
touch "day$1/part1/input.txt"
cp ${starters[choice]} "day$1/part1/${sol[choice]}"

# # Create part 2
mkdir "day$1/part2"
touch "day$1/part2/README.md"
touch "day$1/part2/input.txt"
cp ${starters[choice]} "day$1/part2/${sol[choice]}"

