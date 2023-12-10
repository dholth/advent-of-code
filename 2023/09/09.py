#!/usr/bin/env python
# Sensor readings.

import pprint
import re

import aocd
from rich.console import Console

console = Console()
print = console.print


def parse(lines):
    return [(tuple(map(int, re.findall(r"[-\d]+", line)))) for line in lines]


readings = parse(aocd.data.splitlines())

example = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

example_readings = parse(example.splitlines())


def differences(sequence):
    for i, j in zip(sequence, sequence[1:]):
        yield j - i


example = (0, 3, 6, 9, 12, 15)
print(list(differences((0, 3, 6, 9, 12, 15))))


def diffstack(readings):
    stack = [readings]
    while True:
        spam = tuple(differences(stack[-1]))
        stack.append(spam)  # type: ignore
        if not any(spam):
            break
    return stack


stack = diffstack(example)
print("stack is", stack)


def spamtrapolate(stack, sign=1):
    for j in reversed(range(len(stack))):
        try:
            plus1 = stack[j + 1][-1]
        except IndexError:
            plus1 = 0
        stack[j] = stack[j] + (stack[j][-1] + plus1 * sign,)
    return stack


spamtrapolate(diffstack(example))
print("Example stack", stack)


def part1(readings):
    for reading in readings:
        trapolated = spamtrapolate(diffstack(reading))
        yield trapolated[0][-1]


print(sum(part1(example_readings)))

print("Part 1", sum(part1(readings)))


def part2(readings):
    for reading in readings:
        stack = [tuple(reversed(q)) for q in diffstack(reading)]
        # print("Reversed", reading)
        # pprint.pprint(stack)
        trapolated = spamtrapolate(stack, -1)
        # print("New values")
        # pprint.pprint(trapolated)
        # print()
        yield trapolated[0][-1]


print("Part 2 Examples")
pprint.pprint(example_readings)
print("Part 2 Example Answer", sum(part2(example_readings)))

print("Part 2 Answer", part2 := sum(part2(readings)))
print(part2)
