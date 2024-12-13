#!/usr/bin/env python

import aocd
import itertools
import re

example = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""


def parse(data: str):
    groups = data.split("\n\n")
    return (map(int, re.findall("\d+", group)) for group in groups)


def search(ax, ay, bx, by, px, py):
    for b in reversed(range(100)):
        if (px - (bx * b)) % ax == 0 and (py - (by * b)) % ay == 0:
            result = {"B": b, "A": ((px - (bx * b)) / ax, (py - (by * b)) / ay)}
            if result["A"][0] > 0 and result["A"][0] == result["A"][1]:
                yield result


tokens = 0
for nums in parse(aocd.data):
    for result in search(*nums):
        tokens += result["A"][0] * 3 + result["B"] * 1

print("Part 1", tokens)

## Part 2

# Add 10000000000000 to the X and Y locations of each prize.
# Unfortunately, it will take many more than 100 presses to win.
