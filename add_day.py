#!/usr/local/bin/python3
import os
import sys

def create_files(starter, path):
    input = open(f'{path}/input.txt', "w")
    input.close()

    readme = open(f'{path}/README.md', "w")
    readme.close()

    sol = open(f'{path}/sol.py', "w")
    sol.write(starter)
    sol.close()

if __name__ == "__main__":
    starter = open("starter.py", "r").read()
    try:
        day_num = sys.argv[1]
        os.mkdir(f'day{day_num}')
        os.mkdir(f'day{day_num}/part1')
        create_files(starter, f'day{day_num}/part1')
        os.mkdir(f'day{day_num}/part2')
        create_files(starter, f'day{day_num}/part2')
    except OSError:
        print("OSError: Creation failed, does it already exist?")
    except IndexError:
        print("IndexEror: Did you forget to specify the day?")
