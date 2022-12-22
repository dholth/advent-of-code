#!/usr/bin/env python
# Wraparound grid

from functools import partial
from itertools import groupby
import time

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


PRETTY = {" ": "\N{FULLWIDTH MACRON}", "#": "🟦", ".": "\N{FULLWIDTH FULL STOP}"}

# emoji presentation selector \uFE0F
# extra space might not be necessary in better terminals?
directions = {1 + 0j: "➡\uFE0F ", 1j: "⬇\uFE0F ", -1: "⬅\uFE0F ", -1j: "⬆\uFE0F "}
dir_num = {1 + 0j: 0, 1j: 1, -1: 2, -1j: 3}
num_dir = {v: k for k, v in dir_num.items()}
# directions: 0 right, 1 down, 2 left, 3 up
rotations = {"L": -1j, "R": 1j, "8": -1}  # 1-8-0


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
    for y in range(y0, y1 + 2):
        print(
            "".join(
                PRETTY.get(
                    grid.get(x + y * 1j, "\N{FULLWIDTH MACRON}"),
                    grid.get(x + y * 1j, "\N{FULLWIDTH MACRON}"),
                )
                for x in range(x0, x1 + 1)
            )
        )


import aocd

grid, path = parse(example.splitlines())

grid, path = parse(aocd.lines)

display(grid)

print(directions)

# multiply by 1j or -1j to rotate


def initial(grid):
    for x in range(100):
        x = x + 1j
        if x in grid:
            print("Start is", x, grid[x])
            return x


# +x 👉
direction = 1
position = initial(grid)
display(grid, {position: directions[direction]})

# return next coordinate if walking in direction from position, wrapping around
# wall=(honor walls)
def walk(grid, position, direction, wall=True):
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
            position = walk(grid, position, direction)
            history[position] = "🍞"
    else:
        assert text in ("L", "R")
        direction *= rotations[text]

    # display(grid, history | {position: directions[direction]})
    # input()

display(grid, history | {position: directions[direction]})

print("Coord", position, "Dir", direction)

# directions: 0 right, 1 down, 2 left, 3 up
print("P1", position.real, "P2", position.imag, "P3", dir_num[direction])


def password(position, direction):
    # advent of code won't strip the ".0" from a floating point answer
    return int(position.imag * 1000 + position.real * 4 + dir_num[direction])


print(password(position, direction))
input()

## Part 2


def boundary(grid):
    x0, y0, x1, y1 = 1, 1, 1, 1
    for k in grid:
        x0 = min(x0, k.real)
        x1 = max(x1, k.real)
        y0 = min(y0, k.imag)
        y1 = max(y1, k.imag)
    return x0, y0, x1, y1


def dcube(grid):
    # 2d cube unfolded
    x0, y0, x1, y1 = boundary(grid)
    print(x0, y0, x1, y1)
    square_size = max((x1 - x0 + 1) // 4, (y1 - y0 + 1) // 4)
    return square_size, (x1 - x0 + 1) / square_size, (y1 - y0 + 1) / square_size


grid, path = parse(aocd.lines)
direction = 1
position = initial(grid)

display(grid)
region_size, gx, gy = dcube(grid)
print(region_size, gx, gy)


def edge(grid, region_size, gx, gy, direction, rev=False):
    # display right (0), down, left, or up (3) edge of grid with given region
    # size, square identified by gx, gy going around clockwise
    coords = {}

    # whoops
    direction = (direction + 1) % 4

    dir_corner = {1: (50 + 1j), 2: 50 + 50j, 3: 1 + 50j, 0: 1 + 1j}
    origin = (gx * region_size + gy * region_size * 1j) + dir_corner[direction]

    span = range(50)
    if rev:
        span = reversed(span)

    for j in span:
        new = origin + j * num_dir[direction]
        dj = j  # display j
        if rev:
            dj = 49 - j
        coords[new] = f"{dj:02d}"

    # usefully ordered
    return coords


# display(grid, wraps)

if False:
    for n in range(4):
        display(grid, edge(grid, region_size, 0, 3, n))
        print({0: "right", 1: "down", 2: "left", 3: "top"}[n])
        input()

RIGHT = 0
DOWN = 1
LEFT = 2
TOP = 3

# our edge
oe = partial(edge, grid, region_size)
# def oe(gx, gy, direction, rev=False):
#     return _oe(gx, gy, direction, rev=rev)

# (grid x, grid y, side, reversed)
# still need rotation direction
correspondence = {
    (0, 3, RIGHT): (1, 2, DOWN, True),  # turn left
    (0, 3, DOWN): (2, 0, TOP, True),  # no turn
    (0, 3, LEFT): (1, 0, TOP, True),  # turn left
    (1, 2, RIGHT): (2, 0, RIGHT, True),  # turn 180
    (0, 2, LEFT): (1, 0, LEFT, True),  # turn 180
    (0, 2, TOP): (1, 1, LEFT, True),  # turn right
    (1, 1, RIGHT): (2, 0, DOWN, True),  # turn left
}

reverse_correspondence = {v: k for k, v in correspondence.items()}
correspondence.update(reverse_correspondence)

L = rotations["L"]
R = rotations["R"]
o8 = rotations["8"]
edge_turns = [L, 1, L, -1, -1, R, L]
# inverse if a turn, same if a flip
edge_twons = [R, 1, R, -1, -1, L, R]
cor_turn = dict(zip(correspondence, edge_turns + edge_twons, strict=True))

if False:
    for a, b in reversed(correspondence.items()):
        display(grid, oe(*a))
        print(a, b)
        input()
        display(grid, oe(*b))
        print(a, b)
        input()


# return next coordinate if walking in direction from position, wrapping around
# wall=(honor walls)
def cubewalk(grid, position, direction, wall=True):
    new = position + direction
    new_direction = direction
    if not new in grid:
        for edg in correspondence:
            current_edge = oe(*edg)
            if position in current_edge and edg[2] == dir_num[direction]:
                new = dict(zip(current_edge.keys(), oe(*correspondence[edg]).keys()))[
                    position
                ]
                new_direction = direction * cor_turn[edg]
                break
        else:
            print("missing edge", position, new)
            display(grid, overlay={position: "X", new: "Y"})
    if grid[new] == "." or (not wall and grid[new] == "#"):
        return new, new_direction
    elif grid[new] == "#":
        return position, direction
    else:
        raise RuntimeError("Unexpected at", new)


# walk around edges of the 2d map (clockwise)
def edgewalk(grid, position, direction):
    new = position + direction
    new_direction = direction
    if not new in grid:
        # right turn: new not in grid; repeat position
        new = position
        new_direction = direction * rotations["R"]
    # left turn: if there is a square to our left, go there
    elif new + direction * rotations["L"] in grid:
        new = new + direction * rotations["L"]
        new_direction = direction * rotations["L"]
    return new, new_direction


p0, d0 = position, direction
edges = [(position, direction)]

# do need to append the last one though
while len(edges) <= 1 or position != p0 and len(edges) < (50 * 15):
    position, direction = edgewalk(grid, position, direction)
    edges.append((position, direction))

    # if len(edges) % 50 == 0:
    #     display(grid, {p: directions[d] for p, d in edges})
    #     input()

# 1. detect first left turn (inside corner)
# 2. split final list in half
# 3. zip from inside corner going backwards, with inside corner going forwards

assert edges[-1] == (p0, num_dir[3])
display(grid, {p: directions[d] for p, d in edges})
input()

recent_positions = [position] * 20
while True:
    for _ in range(1):
        # position, direction = cubewalk(grid, position, direction, wall=True)
        position, direction = edgewalk(grid, position, direction)
        recent_positions.pop(0)
        recent_positions.append(position)
    display(
        grid, {p: "🍞" for p in recent_positions} | {position: directions[direction]}
    )
    turn = input().upper()
    if turn in ("L", "R"):
        direction *= rotations[turn]
    if turn == "Q":
        break

grid, path = parse(aocd.lines)
direction = 1
position = initial(grid)

DEBUG = True

recent_positions = [position] * 20
for number, text in groupby(path, str.isnumeric):
    text = "".join(text)
    # print(text)
    if number:
        distance = int(text)
        for _ in range(distance):
            position, direction = cubewalk(grid, position, direction)

            if position != recent_positions[-1]:
                recent_positions.pop(0)
                recent_positions.append(position)

                if DEBUG:
                    display(
                        grid,
                        {p: "🍞" for p in recent_positions}
                        | {position: directions[direction]},
                    )

                    print(text, directions[direction])
                    time.sleep(0.01)
    else:
        assert text in ("L", "R")
        direction *= rotations[text]

        if DEBUG:
            display(
                grid,
                {p: "🍞" for p in recent_positions} | {position: directions[direction]},
            )

            print(text, directions[direction])
            time.sleep(0.01)
    # input()

display(grid, {p: "🍞" for p in recent_positions} | {position: directions[direction]})

print(position, direction)

# directions: 0 right, 1 down, 2 left, 3 up
print("P1", position.real, "P2", position.imag, "P3", dir_num[direction])
