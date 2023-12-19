#!/usr/bin/env python

import sys
from collections import defaultdict
import numpy as np
import aocd
from rich.console import Console

print = Console().print

t = str.maketrans({"O": "🪨", "#": "🧱", ".": "\N{FULLWIDTH FULL STOP}", "$": "💦"})

BIGGISH_NUMBER = sys.maxsize


def display(board, message=""):
    print(f"--- {message}")
    min_x = BIGGISH_NUMBER
    min_y = BIGGISH_NUMBER
    max_x = -BIGGISH_NUMBER
    max_y = -BIGGISH_NUMBER

    for x, y in board:
        min_x = min(x, min_x)
        min_y = min(y, min_y)
        max_x = max(x, max_x)
        max_y = max(y, max_y)

    for y in range(min_y, max_y + 1):
        outside = True
        line = []
        for x in range(min_x, max_x + 1):
            value = board[(x, y)]
            if not value:
                if line and line[-1] == "#":
                    outside = not outside
                value = "$."[outside]
            line.append(value)
        print("".join(line).translate(t))


print = Console().print

data = aocd.data.splitlines()

example = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)""".splitlines()


class V(tuple):
    def __new__(cls, *args):
        return super(V, cls).__new__(cls, args)

    def __add__(self, other):
        return self.__class__(*(a + b for a, b in zip(self, other)))

    def __sub__(self, other):
        return self.__class__(*(a - b for a, b in zip(self, other)))

    def taxi(self):
        a, b = self
        return int(abs(a) + abs(b))


# column, row
U = V(0, -1)
D = V(0, 1)
R = V(1, 0)
L = V(-1, 0)

dirs = dict(zip("UDRL", (U, D, R, L)))

print(dirs)

board = defaultdict(str)


def dig(board, lines):
    here = V(0, 0)
    for line in lines:
        dir, count, color = line.split()
        count = int(count)
        for _ in range(count):
            here += dirs[dir]
            board[here] = "#"


dig(board, example)

display(board)


board2 = defaultdict(str)
dig(board2, data)
# display(board2)


def adjacent(board, coord):
    """
    Neighbors according to N, S, E, W
    """
    for x, y in dirs.values():
        neighbor = (coord[0] + x, coord[1] + y)
        nval = board.get(neighbor)
        if not nval or nval == "#":
            continue
        yield neighbor


def flood(board, start) -> tuple[int, dict[tuple[int, int], int]]:
    visited = {start: 0}
    todo = [start]
    next = []

    for distance in range(10000):
        for here in todo:
            visited[here] = distance
            board[here] = "."
            next_to = set(adjacent(board, here))
            for n in next_to:
                if not n in visited:
                    next.append(n)
        if not next:
            print("Done at", distance)
            return distance, visited
        todo = set(next)
        next = []
    assert False


def corners(board):
    min_x = BIGGISH_NUMBER
    min_y = BIGGISH_NUMBER
    max_x = -BIGGISH_NUMBER
    max_y = -BIGGISH_NUMBER

    for x, y in board:
        min_x = min(x, min_x)
        min_y = min(y, min_y)
        max_x = max(x, max_x)
        max_y = max(y, max_y)

    return (min_x, min_y), (max_x, max_y)


def border(board):
    # fill in board plus 1 all around
    (min_x, min_y), (max_x, max_y) = corners(board)

    for y in range(min_y - 1, max_y + 2):
        for x in range(min_x - 1, max_x + 2):
            if not board[(x, y)]:
                board[(x, y)] = "$"


border(board)

flood(board, corners(board)[0])

display(board)

border(board2)
flood(board2, corners(board2)[0])
# display(board2)

print(sum(b in "$#" for b in board.values()))

ans = sum(b in "$#" for b in board2.values())
print("Part 1", ans)


def dig2(lines):
    here = np.array((16526865, 16526865))
    yield here
    for line in lines:
        dir, count, color = line.split()
        count = int(count)
        # print(color, color[2:-2], color[-2])
        distance = int(color[2:-2], 16)
        # The last hexadecimal digit encodes the direction to dig: 0 means R, 1 means D, 2 means L, and 3 means U.
        direction = np.array(dirs["RDLU"[int(color[-2])]])
        # print(direction * distance)
        here = here + (direction * distance)
        yield here


perimeter = list(dig2(example))
print(perimeter)

area = 0
for (a0, a1), (b0, b1) in zip(perimeter, perimeter[1:]):
    # if (b0, b1) == (0, 0):
    #     break
    # print(f"{(a0,a1)}->{(b0,b1)}")
    section = np.linalg.det(np.array([[a0, b0], [a1, b1]]))
    area += section
print(area)

print(952408144115 == int(area))

from shapely.geometry import Polygon

p0 = Polygon(perimeter)
print("Example area", p0.area, 952408144115 == int(p0.area))
p = Polygon(dig2(data))
print("Data area", p.area)

import shapely

print(shapely.area(p0) - 952408144115)


def Area(corners):
    # from stackoverflow
    n = len(corners)  # of corners
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0
    return area


def area(points):
    # a = 1/2 sum(i=1..n) x[i] * (y[i+1] - y[i-1])

    s = 0
    for i in range(len(perimeter)):
        x = points[i][0]
        y0 = points[(i - 1) % len(points)][1]
        y1 = points[(i + 1) % len(points)][1]
        s += x * (y1 - y0)
    return s / 2


print("Shoe", area(perimeter))
# 952408144115

print("Missing", 952408144115 - area(perimeter))


def sump(lines):
    "sum of perimeter sizes"
    for line in lines:
        dir, count, color = line.split()
        count = int(count)
        # print(color, color[2:-2], color[-2])
        distance = int(color[2:-2], 16)
        yield distance


print(sum(sump(example)))

border = sum(sump(example)) / 2 + 1
print(border)

print("Example", 952408144115 - (border + area(perimeter)))

points2 = list(dig2(data))
# print(points2)
border2 = sum(sump(data)) // 2 + 1
