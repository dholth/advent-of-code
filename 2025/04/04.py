#!/usr/bin/env python
"""
Paper rolls and forklifts.

Count adjacent grid locations.
"""

import aocd

sample = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

PRETTY = {
    ".": "\N{FULLWIDTH FULL STOP}",
    "@": "🧻",
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
        row = "".join([PRETTY[parsed.get((x, y), ".")] for x in range(max_x + 1)])
        print(row)


display(parse(sample))

surrounds = [(x, y) for y in range(-1, 2) for x in range(-1, 2) if (x, y) != (0, 0)]

print(surrounds)


def neighbors(grid: dict[tuple[int, int], str], seek):
    """
    Count how many neighbors of any cell in grid that contains "seek" equal "seek" (and not None or .), yield True if less than 4.
    """
    for place in grid:
        if grid[place] != seek:
            continue
        yield (
            sum(grid.get((place[0] + x, place[1] + y)) == seek for (x, y) in surrounds)
            < 4
        )


def neighbors2(grid: dict[tuple[int, int], str], seek):
    """
    Count how many neighbors of any cell in grid that contains "seek" equal "seek" (and not None or .), yield coordinate if less than 4.
    """
    for place in grid:
        if grid[place] != seek:
            continue
        if (
            sum(grid.get((place[0] + x, place[1] + y)) == seek for (x, y) in surrounds)
            < 4
        ):
            yield place


print(sum(neighbors(parse(sample), "@")))

part1 = sum(neighbors(parse(aocd.data), "@"))
print(f"Reachable rolls: {part1}")

grid = parse(aocd.data, ignore=".")
# display(grid)

before = len(grid)
while remove := list(neighbors2(grid, "@")):
    print(len(remove))
    for element in remove:
        del grid[element]
after = len(grid)

print(f"Removed {before - after} rolls of paper")
