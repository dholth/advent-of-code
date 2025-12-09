#!/usr/bin/env python
"""
Day 7: Laboratories
"""

from itertools import starmap
from operator import add

import aocd

example = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""

# using dash for visited splitter
PRETTY = {
    ".": "\N{FULLWIDTH FULL STOP}",
    "S": "\N{GLOWING STAR}",
    "^": "🌲",
    "-": "\N{CHRISTMAS TREE}",
    "|": "｜",
}


def parse(lines: str, ignore=()):
    parsed = {}
    for row, line in enumerate(lines.splitlines()):
        for column, char in enumerate(line):
            if char in ignore:
                continue
            parsed[(column, row)] = char
    return parsed


def display(parsed):
    max_x = 0
    max_y = 0
    for x, y in parsed:
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    for y in range(max_y + 1):
        row = "".join([PRETTY[parsed.get((x, y))] for x in range(max_x + 1)])
        print(row)


display(parse(example))

# A beam descends downwards from S. Whenever it reaches a splitter, ^,
# a new beam starts from the left and the right of the beam.  It continues
# downwards until it reaches another splitter or exits. Count the number of
# times the beam is split (aka the number of splitters that were reached).

down = (0, 1)
left = (-1, 0)
right = (1, 0)


def jcvd(grid: dict[tuple[int, int], str], start: tuple[int, int]):
    """
    Does the splits.

    A beam continues downwards from start. If it reaches a splitter (^),
    two new beams continue from the left and right of the ^.

    Mutate grid, adding | for beams and changing visited splitters to -.
    """
    # skip off-the-grid or already-contains-beam
    if start not in grid or grid[start] == "|":
        return 0

    grid[start] = "|"

    next = start[0] + down[0], start[1] + down[1]
    if next in grid and grid[next] == "^":
        grid[next] = "-"
        return 1 + sum(
            jcvd(grid, (start[0] + step[0], start[1] + step[1]))
            for step in (left, right)
        )

    else:
        return jcvd(grid, next)


grid = parse(example)


def find_start(grid: dict[tuple[int, int], str]):
    for k, v in grid.items():
        if v == "S":
            return k
    raise ValueError("No S in grid")


print(jcvd(grid, find_start(grid)))

print(sum(v == "-" for v in grid.values()))

grid = parse(aocd.data)
wrong = jcvd(grid, find_start(grid))

display(grid)

print("Part 1:", sum(v == "-" for v in grid.values()), wrong)


def jcvd_2(
    grid: dict[tuple[int, int], str],
    start: tuple[int, int],
    memo: dict[tuple[int, int], int],
):
    """
    Now count all possible paths to the exit.
    """
    if start in memo:
        return memo[start]

    if start not in grid:
        return 1

    here = grid[start]

    if here == "^":
        sides = (left, right)
    else:
        sides = (down,)

    total = sum(
        jcvd_2(grid, tuple(starmap(add, zip(start, side))), memo) for side in sides
    )
    memo[start] = total
    return total


# will be fast even without memoization
memo = {}
example_grid = parse(example)
ans_2 = jcvd_2(example_grid, find_start(example_grid), memo)
print("Example Part 2", ans_2)

# will take more time if we don't use memoization
memo = {}
grid = parse(aocd.data)
ans_2_real = jcvd_2(grid, find_start(grid), memo)
print(f"Part 2 {ans_2_real}; {ans_2_real.bit_length()} bits")

part_2_for_part_1 = sum(grid[pos] == "^" for pos in memo)
print(f"Part 1 answer from part 2 data {part_2_for_part_1}")
print(f"{len(memo)} entries in memoization structure")

def line_by_line(data: str):
    lines = data.splitlines()
    values = [int(c=="S") for c in lines[0]]
    for line in lines[1:]:
        for i in range(len(values)):
            if line[i] == "^":
                values[i-1] += values[i]
                values[i+1] += values[i]
                values[i] = 0

    return values

print("Line-by-line attempt", line_by_line(example), sum(line_by_line(example)))

print(sum(line_by_line(aocd.data)))