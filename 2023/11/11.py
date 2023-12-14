#!/usr/bin/env python

import aocd
from rich.console import Console
from itertools import combinations

console = Console()


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


def load(lines):
    board: dict[tuple, str] = {}

    for i, line in enumerate(lines, start=1):
        for j, char in enumerate(line, start=1):
            board[V(j, i)] = char

    return board


def display(board_grid, visited, marked={}):
    for y, line in enumerate(board_grid, start=1):
        colorized = []
        for x, c in enumerate(line, start=1):
            if c == "#":
                color = "bright_cyan"
            elif (x, y) in visited:
                color = "green"
            elif (x, y) in marked:
                color = ("red", "blue")[marked[(x, y)]]
            else:
                color = "grey"
            colorized.append(f"[{color}]{c}[/]")
        console.print("".join(colorized))
    print("Red is outside, green is circuit, blue is inside")

example = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

if True:
    DATA = aocd.data.splitlines()
else:
    DATA = example.splitlines()

grid = DATA

board = load(grid)

# display(grid, {})

stars = dict(filter(lambda item: item[1] == "#", board.items()))
print(stars)

columns_with_stars = set(x for x, y in stars)
rows_with_stars = set(y for x, y in stars)

print(columns_with_stars)
print(rows_with_stars)

no_stars_cols = []
for i in range(1, len(grid[0]) + 1):
    if not i in columns_with_stars:
        no_stars_cols.append(i)

no_stars_rows = []
for i in range(1, len(grid[0]) + 1):
    if not i in rows_with_stars:
        no_stars_rows.append(i)

print(no_stars_cols)
print(no_stars_rows)

print(len(stars))
print(len(list(combinations(stars, 2))))


all_distance = 0
EXPANSION = int(1e6)-1
print("Expand by", EXPANSION)
for a, b in list(combinations(stars, 2)):
    distance = (b - a).taxi()
    assert (a - b).taxi() == distance

    min_x = min(a[0], b[0])
    max_x = max(a[0], b[0])
    extra_x = len(list(s for s in no_stars_cols if min_x < s < max_x)) * EXPANSION

    min_y = min(a[1], b[1])
    max_y = max(a[1], b[1])
    extra_y = len(list(s for s in no_stars_rows if min_y < s < max_y)) * EXPANSION

    # because existing column is already included in the count
    distance += extra_x + extra_y

    all_distance += distance

print("Ans", all_distance)
aocd.submit(all_distance, part=2)
