#!/usr/bin/env python
"""
Any (multi-digit) number adjacent to a symbol is a "part number" and should be
summed.
"""

import re
from math import prod
from pathlib import Path

from rich.console import Console

console = Console()

INPUT = Path(__file__).parent / "input.txt"
INPUT = INPUT.open().readlines()

EXAMPLE = """Time:      7  15   30
Distance:  9  40  200
""".splitlines()


def all_numbers(line):
    return [int(x) for x in re.findall(r"\d+", line)]


def part1(input):
    times = all_numbers(input[0])
    distance = all_numbers(input[1])

    for t, d in zip(times, distance):
        ways = 0
        for n in range(t):
            travel = (t - n) * n
            # print(t, d, travel)
            if travel > d:
                ways += 1
        yield ways


answer = prod(part1(INPUT))
print("Ans", answer)

# submit(answer)

times2 = int("".join(c for c in INPUT[0] if c.isdigit()))
dist2 = int("".join(c for c in INPUT[1] if c.isdigit()))

print("".join(INPUT), times2, dist2)


def part2(t, d):
    print("t", t, "d", d)
    ways = 0
    for n in range(42522903, 42934734):
        # for n in range(1, 1000):
        travel = (t - n) * n
        if travel > d:
            ways += 1
    return ways


# first true
first_true = 42522904
# first false
first_false = 42934734

ans2wrong = first_false - first_true
print(ans2wrong)

print(part2(times2, dist2))


def brute2(t, d):
    print("t", t, "d", d)
    ways = 0
    for n in range(t):
        travel = (t - n) * n
        if travel > d:
            ways += 1
    return ways


print("Brute example", brute2(71530, 940200))

print("Brute real", brute2(times2, dist2))
