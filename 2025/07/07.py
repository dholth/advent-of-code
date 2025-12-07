#!/usr/bin/env python
"""
Day 7: Laboratories
"""

# The jcvd algorithm: does the splits

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
    "S": "\N{Glowing Star}",
    "^": "🌲",
    "-": "\N{Christmas Tree}",
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
    if not start in grid or grid[start] == "|":
        return 0

    grid[start] = "|"

    # display(grid)

    next = start[0]+down[0], start[1]+down[1]
    if next in grid and grid[next] == '^':
        grid[next] = "-"
        return 2 + sum(jcvd(grid, (start[0]+step[0], start[1]+step[1])) for step in (left, right))

    else:
        return jcvd(grid, next)

grid = parse(example)
def find_start(grid):
    for k, v in grid.items():
        if v == "S":
            return k

print(jcvd(grid, find_start(grid)))

print(sum(v=='-' for v in grid.values()))

grid = parse(aocd.data)
jcvd(grid, find_start(grid))
aocd.submit(sum(v=='-' for v in grid.values()))

display(grid)
