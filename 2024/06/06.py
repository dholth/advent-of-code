#!/usr/bin/env python


import sys
import time
from collections import defaultdict

import aocd

sys.setrecursionlimit(10000)

FILLER = "\N{FULLWIDTH FULL STOP}"
PRETTY = {
    " ": "\N{FULLWIDTH FULL STOP}",
    ".": "\N{FULLWIDTH FULL STOP}",
    "#": "🧱",
    ">": "👉",
    "<": "👈",
    "^": "👆",
    "v": "👇",
}


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

    def __repr__(self):
        return f"V{str((*self,))}"


# no diagonals
directions = [V(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if abs(sum((i, j))) == 1]

# winds up being [V(-1, 0), V(0, -1), V(0, 1), V(1, 0)]


# # in the order initially considered
compass = [V(0, -1), V(1, 0), V(0, 1), V(-1, 0)]  # in rotation direction

N, E, S, W = compass

print(compass)


def parse(data, ignore=""):
    board: dict[tuple, str] = {}
    for i, line in enumerate(data.splitlines(), start=1):
        for j, char in enumerate(line.strip(), start=1):
            if char not in ignore:
                board[V(j, i)] = char
    return board


def display(grid, overlay={}):
    grid = dict(grid)
    grid.update(overlay)

    x0, y0, x1, y1 = 1, 1, 1, 1
    for x, y in grid:
        x0 = min(x0, x)
        x1 = max(x1, x)
        y0 = min(y0, y)
        y1 = max(y1, y)
    x0, x1, y0, y1 = map(int, (x0, x1, y0, y1))
    for y in range(y0, y1 + 1):
        print(
            "".join(
                PRETTY.get(
                    grid.get(V(x, y), FILLER),
                    grid.get(V(x, y), FILLER),
                )
                for x in range(x0, x1 + 1)
            )
        )


example = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

board = parse(aocd.data)

display(board)

visited = set()


def patrol(pos, direction, depth=0):
    if board.get(pos + direction) == "#":
        # print("Turn", direction, end="")
        direction = compass[(compass.index(direction) + 1) % len(compass)]
    if board.get(pos) is None:
        return depth
    visited.add(pos)
    return patrol(pos + direction, direction, depth=depth + 1)


start = None
for coord in board:
    if board[coord] == "^":
        start = coord

print(start)

print(patrol(start, N))

print(len(visited))

# Brute force determine loop

# Keep track of all (visited, direction)
# If (pos + direction) != #
#  Add a # in (pos + direction)
#    Patrol
#    If (pos + direction) of wherever we are is in visited:
#      we found a loop


class FindLoops:
    visited: dict[tuple, int]

    def __init__(self):
        self.visited = defaultdict(int)
        self.loop_blocks = {}

    def find_loops(self, pos, direction, depth=0, loopy=False):
        ans = 0
        if not loopy and board.get(pos + direction) == ".":
            board[pos + direction] = "#"
            ans += self.find_loops(
                pos, direction, depth=depth + 1, loopy=(pos + direction)
            )
            board[pos + direction] = "."

        while board.get(pos + direction) == "#":
            direction = compass[(compass.index(direction) + 1) % len(compass)]

        if board.get(pos) is None:
            return ans

        self.visited[(pos, direction)] = self.visited[(pos, direction)] + 1
        if self.visited[(pos, direction)] == 2:
            ans += 1
            self.loop_blocks[loopy] = True
        else:
            ans += self.find_loops(
                pos + direction, direction, depth=depth + 1, loopy=loopy
            )
        self.visited[(pos, direction)] = self.visited[(pos, direction)] - 1
        return ans

    def find_loop_dumb(self, pos, direction, depth=0):
        """
        Slower way to find loops.
        """
        while board.get(pos + direction) == "#":
            direction = compass[(compass.index(direction) + 1) % len(compass)]

        if board.get(pos) is None:
            return False

        self.visited[(pos, direction)] = self.visited[(pos, direction)] + 1
        if self.visited[(pos, direction)] == 2:
            return True

        return self.find_loop_dumb(pos + direction, direction, depth=depth + 1)


loop_find = FindLoops()

begin = time.time_ns()
no_loop = loop_find.find_loop_dumb(start, N)
end = time.time_ns()

initial_visited = loop_find.visited

print(
    no_loop,
    len(set(a for a, _ in initial_visited)),
    len(initial_visited),
    (end - begin) / 1e9,
)

ans2 = 0
blockers = set()
for i, position in enumerate(set(a for a, _ in initial_visited)):
    if i % 100 == 0:
        print(i)
    if position == start:
        print("Skip starting position")
        continue
    loop_find.visited = defaultdict(int)
    assert board[position] == "."
    board[position] = "#"
    if loop_find.find_loop_dumb(start, N):
        blockers.add(position)
    board[position] = "."

print("brute force method", ans2, len(blockers))

loop_find = FindLoops()
print(loop_find.find_loops(start, N))  # still buggy
