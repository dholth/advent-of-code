#!/usr/bin/env python
# In which the elves play a choosing game

from pathlib import Path
from collections import defaultdict
import math

# part 1
# 12 red cubes, 13 green cubes, and 14 blue cubes.

loadout = {"red": 12, "green": 13, "blue": 14}


def possibles():
    for i, line in enumerate(open("sample.txt"), start=1):
        _, cubes = line.strip().split(":", 1)
        # print(i, ":", cubes)
        game_possible = True
        for part in cubes.split(";"):
            part_summary = defaultdict(int)
            for color in part.split(","):
                color = color.strip()
                num, color = color.split(" ")
                part_summary[color] += int(num)

            for color in loadout:
                if part_summary[color] > loadout[color]:
                    game_possible = False

        yield (i * game_possible)


print("sum possible", sum(possibles()))

# part 2
# fewest cubes to make a game possible


def fewests():
    for i, line in enumerate(open("input.txt"), start=1):
        _, cubes = line.strip().split(":", 1)

        game_summary = defaultdict(int)

        for part in cubes.split(";"):
            part_summary = defaultdict(int)
            for color in part.split(","):
                color = color.strip()
                num, color = color.split(" ")
                part_summary[color] += int(num)

            for color in part_summary:
                game_summary[color] = max(part_summary[color], game_summary[color])

        print(i, dict(game_summary))
        yield math.prod(game_summary.values())


print()
print("fewest", sum(fewests()))
