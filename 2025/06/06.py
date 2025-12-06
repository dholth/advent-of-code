#!/usr/bin/env python
"""
Day 6: Trash Compactor
"""

import re
import aocd
import pprint
from functools import reduce
from operator import add, mul

sample = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
"""


def parse(data: str):
    lines = data.splitlines()
    values = []
    for line in lines[:-1]:
        values.append(tuple(int(x) for x in re.findall(r"\d+", line)))
    operators = lines[-1].split()
    return values, operators


pprint.pprint(parse(sample))

values, operators = parse(sample)

ops = {"*": mul, "+": add}


def math(values, operators):
    total = 0
    for column in range(len(values[0])):
        total += reduce(ops[operators[column]], (row[column] for row in values))
    return total


print(math(values, operators))

print("Part 1", math(*parse(aocd.data)))

# Part 2


def transpose(data: str):
    lines = data.splitlines()
    for i in range(len(lines[0]) - 1, -1, -1):
        yield "".join(line[i] for line in lines)


print("\n".join(transpose(sample)))


def part_2(data: str):
    """
    Now the numbers are given right to left in columns, with the most
    significant digit on top and the least significant digit at the bottom.
    """
    values = []
    for line in transpose(data):
        numbers = re.findall(r"\d+", line)
        if not numbers:
            continue

        values.append(int(numbers[0]))

        if (op := line[-1]) in ops:
            ans = reduce(ops[op], values)
            print(op, values, "=", ans)
            values.clear()
            yield ans


print("Sample Part 2", sum(part_2(sample)))

print("Part 2", sum(part_2(aocd.data)))
