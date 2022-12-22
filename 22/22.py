#!/usr/bin/env python
# Wraparound grid

from itertools import groupby

example = """\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""

# using (1, 1) as top left
def parse(lines):
    grid = {}
    path = ""

    lines = iter(lines)
    for y, line in enumerate(lines, 1):
        if not line:
            break
        for x, char in enumerate(line, 1):
            if not char.isspace():
                grid[x + y * 1j] = char

    path = next(lines)
    return grid, path


PRETTY = {" ": "\N{FULLWIDTH MACRON}", "#": "🌋", ".": "\N{FULLWIDTH FULL STOP}"}

# emoji presentation selector \uFE0F
# extra space might not be necessary in better terminals?
directions = {1 + 0j: "➡\uFE0F ", 1j: "⬇\uFE0F ", -1: "⬅\uFE0F ", -1j: "⬆\uFE0F "}
dir_num = {1+0j: 0, 1j: 1, -1:2, -1j: 3}
# directions: 0 right, 1 down, 2 left, 3 up
rotations = {"L": -1j, "R": 1j}


def display(grid, overlay={}):
    grid = dict(grid)
    grid.update(overlay)

    x0, y0, x1, y1 = 0, 0, 0, 0
    for k in grid:
        x0 = min(x0, k.real)
        x1 = max(x1, k.real)
        y0 = min(y0, k.imag)
        y1 = max(y1, k.imag)
    x0, x1, y0, y1 = map(int, (x0, x1, y0, y1))
    for y in range(y0, y1 + 1):
        print(
            "".join(
                PRETTY.get(grid.get(x + y * 1j, " "), grid.get(x + y * 1j, " "))
                for x in range(x0, x1 + 1)
            )
        )


import aocd

grid, path = parse(example.splitlines())

grid, path = parse(aocd.lines)

display(grid)

print(directions)

# multiply by 1j or -1j to rotate

for x in range(100):
    x = x+1j
    if x in grid:
        print("Start is", x, grid[x])
        position = x
        break

# +x 👉
direction = 1
display(grid, {position: directions[direction]})

# return next coordinate if walking in direction from position, wrapping around
# wall=(honor walls)
def next(grid, position, direction, wall=True):
    new = position + direction
    if not new in grid:
        for i in range(1000):
            new -= direction
            if not new in grid:
                new += direction
                break
        else:
            raise RuntimeError("Failed to wraparound")
    if grid[new] == ".":
        return new
    elif grid[new] == "#":
        return position
    else:
        raise RuntimeError("Unexpected at", new)


history = {position: "🍞"}
for number, text in groupby(path, str.isnumeric):
    text = "".join(text)
    print(text)
    if number:
        distance = int(text)
        for _ in range(distance):
            position = next(grid, position, direction)
            history[position] = "🍞"
    else:
        assert text in ("L", "R")
        direction *= rotations[text]

    # display(grid, history | {position: directions[direction]})
    # input()

display(grid, history | {position:directions[direction]})

print("Coord", position, "Dir", direction)

# directions: 0 right, 1 down, 2 left, 3 up
print("P1", position.real, "P2", position.imag, "P3", dir_num[direction])

def password(position, direction):
    return position.imag*1000+position.real*4+dir_num[direction]

print(password(position, direction))