#!/usr/bin/env python
# An animal scurries around a grid of pipes.

import itertools
import math
import pprint
import re
from pathlib import Path

import aocd

from aocd import submit
from rich.console import Console

console = Console()

directions = [(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if (i, j) != (0, 0)]

directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

print(directions)

"""
| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
"""

# column, row
N = (0, -1)
S = (0, 1)
E = (1, 0)
W = (-1, 0)

tubes = {
    "|": (N, S),
    "-": (E, W),
    "L": (N, E),
    "J": (N, W),
    "7": (S, W),
    "F": (S, E),
    "S": (N, S, E, W),
    ".": (),
}


def neighbors(board, coord):
    """
    Neighbors according to tubes rules.
    """
    here = board[coord]
    for x, y in tubes[here]:
        neighbor = (coord[0] + x, coord[1] + y)
        if not board.get(neighbor):
            continue
        yield neighbor


def adjacent(board, coord):
    """
    Neighbors according to N, S, E, W
    """
    for x, y in (N, S, E, W):
        neighbor = (coord[0] + x, coord[1] + y)
        if not board.get(neighbor):
            continue
        yield neighbor


def load(lines):
    board: dict[tuple, str] = {}

    for i, line in enumerate(lines, start=1):
        for j, char in enumerate(line, start=1):
            board[(j, i)] = char

    return board


board_grid = aocd.data.splitlines()
regular_board = load(board_grid)


def flood(start) -> tuple[int, dict[tuple[int, int], int]]:
    visited = {start: 0}
    todo = [start]
    next = []

    for distance in range(10000):
        for here in todo:
            visited[here] = distance
            next_to = set(neighbors(regular_board, here))
            for n in next_to:
                if here in set(neighbors(regular_board, n)):
                    if not n in visited:
                        next.append(n)
        if not next:
            print("Done at", distance)
            return distance, visited
        todo = set(next)
        next = []
    assert False


def part2(start, visited) -> tuple[int, dict[tuple[int, int], int]]:
    """
    Now all are connected; include dots in the board.
    """
    todo = [start]
    next = []

    for distance in range(1000):
        print(distance, len(todo))
        for here in todo:
            visited[here] = distance
            next_to = set(adjacent(regular_board, here))
            for n in next_to:
                if not n in visited:
                    next.append(n)
        if not next:
            print("Done at", distance)
            return distance, visited
        todo = set(next)
        next = []
    return -1, visited


def display(visited, marked={}):
    for y, line in enumerate(board_grid, start=1):
        for x, c in enumerate(line, start=1):
            if c == "S":
                color = "bright_cyan"
            elif (x, y) in visited:
                color = "green"
            elif (x, y) in marked:
                color = ("red", "blue")[marked[(x, y)]]
            else:
                color = "grey"
            console.print(f"[{color}]{c}", end="")
        print()
    print("Red is outside, green is circuit, blue is inside")


coord = (0, 0)
for coord, char in regular_board.items():
    if char == "S":
        break

print("Start at", coord)

distance, visited = flood(coord)

# display(visited)

print("Part 1", distance)

visited1 = visited.copy()

# wrong solution
# visited2 will be the same object as visited
# distance2, visited2 = part2((1, 1), visited)

# display(visited2)

# print("Part 2", distance2, len(visited2), len(board) - len(visited2))

# print(sum(x not in visited2 for x in board))


def part2b(visited, board, board_grid):
    """even-odd rule part2 but incorrect"""
    marked = {}
    for y, line in enumerate(board_grid, start=1):
        inside = False
        previous_visited = False
        for x, char in enumerate(line, start=1):
            if char == "-":
                continue
            if (x, y) in visited and board[(x, y)] == "|":
                inside = not inside
            if not (x, y) in visited:
                marked[(x, y)] = inside

            # here_visited = (x, y) in visited
            # if here_visited and not previous_visited:
            #     inside = True
            # if previous_visited and not here_visited:
            #     inside = False
            # previous_visited = here_visited
            # if not here_visited:
            #     marked[(x, y)] = inside
    return marked


marked = part2b(visited1, regular_board, board_grid)

# display(visited1, marked)

print("Inside", sum(v for v in marked.values() if v is True))
# aocd.submit(sum(v for v in marked.values() if v is True), part=2)
print("Outside", sum(v for v in marked.values() if v is False))
print(len(marked))
# print(marked)

silly_method = {
    "|": [
        " * ",
        " * ",
        " * ",
    ],
    "-": [
        "   ",
        "***",
        "   ",
    ],
    "L": [
        " * ",
        " **",
        "   ",
    ],
    "J": [
        " * ",
        "** ",
        "   ",
    ],
    "7": [
        "   ",
        "** ",
        " * ",
    ],
    "F": [
        "   ",
        " **",
        " * ",
    ],
    "S": [
        " * ",
        "***",
        " * ",
    ],
    ".": [
        "   ",
        "   ",
        "   ",
    ],
}

grid2 = [[" "] * len(board_grid[0]) * 3 for _ in range(len(board_grid) * 3)]

for y, line in enumerate(board_grid):
    for x, char in enumerate(line):
        v = (x + 1, y + 1) in visited
        if v:
            sprite = silly_method[char]
            for j, s in enumerate(sprite):
                grid2[y * 3 + j][x * 3 : x * 3 + len(s)] = list(s)

# for line in grid2:
#     print("".join(line))


def silly_flood(board, start, visited) -> tuple[int, dict[tuple[int, int], int]]:
    """
    Now only *'s block the flow.
    """
    todo = [start]
    next = []

    for distance in range(1000):
        for here in todo:
            visited[here] = distance
            next_to = set(adjacent(board, here))
            for n in next_to:
                if not n in visited:
                    if board[n] != "*":
                        next.append(n)
        if not next:
            print("Done at", distance)
            return distance, visited
        todo = set(next)
        next = []
    return -1, visited


silly_board = load("".join(line) for line in grid2)

assert (1, 1) in silly_board

silly_visited = {}
distance, visited = silly_flood(silly_board, (1, 1), silly_visited)

assert (1, 1) in silly_board


for line in grid2:
    print("".join(line))


print()
print()
print()

for i, j in visited:
    grid2[j - 1][i - 1] = "."

thespot = 0

for j in range(len(board_grid)):
    y = 1 + 3 * j
    for i in range(len(board_grid[0])):
        x = 1 + 3 * i
        if grid2[y][x] == " ":
            grid2[y][x] = "X"
            thespot += 1

for line in grid2:
    print("".join(line))

print(thespot, "spaces inside the curve.")
