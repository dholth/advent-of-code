#!/usr/bin/env python

from collections import UserList
from itertools import product
import time
from networkx import DiGraph
from functools import cache

import aocd

example = """\
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
""".splitlines()

WALL = "#"
STORM = "><^v"
STORM_EAST, STORM_WEST, STORM_NORTH, STORM_SOUTH = STORM

# using (1, 1) as top left
def parse(lines):
    grid = {}

    lines = iter(lines)
    for y, line in enumerate(lines, 1):
        if not line:
            break
        for x, char in enumerate(line, 1):
            if char == WALL or char in STORM:
                grid[x + y * 1j] = char
    return grid


FILLER = "\N{FULLWIDTH FULL STOP}"
PRETTY = {
    " ": "\N{FULLWIDTH FULL STOP}",
    "#": "🧱",
    ">": "👉",
    "<": "👈",
    "^": "👆",
    "v": "👇",
}

dir_num = {1 + 0j: 0, 1j: 1, -1: 2, -1j: 3}
num_dir = {v: k for k, v in dir_num.items()}
# directions: 0 right, 1 down, 2 left, 3 up
# directions: 0 east, 1 south, 2 west, 3 north

# in the order initially considered
compass = {"N": num_dir[3], "S": num_dir[1], "W": num_dir[2], "E": num_dir[0]}
compass_index = {k: i for i, k in enumerate(compass)}
blizz = {
    ">": compass_index["E"],
    "<": compass_index["W"],
    "^": compass_index["N"],
    "v": compass_index["S"],
}


def display(grid, overlay={}):
    grid = dict(grid)
    grid.update(overlay)

    x0, y0, x1, y1 = 1, 1, 1, 1
    for k in grid:
        x0 = min(x0, k.real)
        x1 = max(x1, k.real)
        y0 = min(y0, k.imag)
        y1 = max(y1, k.imag)
    x0, x1, y0, y1 = map(int, (x0, x1, y0, y1))
    for y in range(y0, y1 + 1):
        print(
            "".join(
                PRETTY.get(
                    grid.get(x + y * 1j, FILLER),
                    grid.get(x + y * 1j, FILLER),
                )
                for x in range(x0, x1 + 1)
            )
        )


def limits(grid):
    x0, y0, x1, y1 = 1, 1, 1, 1
    for k in grid:
        x0 = min(x0, k.real)
        x1 = max(x1, k.real + 1)
        y0 = min(y0, k.imag)
        y1 = max(y1, k.imag + 1)
    x0, x1, y0, y1 = map(int, (x0, x1, y0, y1))
    return x0, x1, y0, y1


grid = parse(aocd.lines)

display(grid)

print(limits(grid))

x0, x1, y0, y1 = limits(grid)
print(f"active area: {x1-x0-2}\u0078{y1-y0-2}")


class ShiftList(UserList):
    def __init__(self, data, offset: int):
        offset %= len(data)
        super().__init__(data)
        self.offset = offset

    def __getitem__(self, i):
        if 0 <= i < len(self):
            return super().__getitem__((i + self.offset) % len(self))
        raise IndexError(i)


SHIFT_DIRECTION = {
    blizz[STORM_EAST]: -1,
    blizz[STORM_WEST]: 1,
    blizz[STORM_NORTH]: 1,
    blizz[STORM_SOUTH]: -1,
}

# 4 neighbors plus self
SIDES = [
    (c[0] + 1j * c[1]) for c in product(*[(-1, 0, 1)] * 2) if sum(map(abs, c)) in (0, 1)
]


class Blizzard:
    def __init__(self, grid):
        self.grid = dict(grid)

        x0, x1, y0, y1 = limits(grid)

        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1

        x_active = x1 - x0 - 2
        y_active = y1 - y0 - 2

        # by direction
        self.bbd: list[list[list[str]]] = [[], [], [], []]
        self.bbd[blizz[STORM_EAST]] = [["."] * x_active for _ in range(y_active)]
        self.bbd[blizz[STORM_WEST]] = [["."] * x_active for _ in range(y_active)]
        self.bbd[blizz[STORM_NORTH]] = [["."] * y_active for _ in range(x_active)]
        self.bbd[blizz[STORM_SOUTH]] = [["."] * y_active for _ in range(x_active)]

        for y in range(y0 + 1, y1 - 1):
            for x in range(x0 + 1, x1 - 1):
                storm = self.grid.pop(x + y * 1j, None)
                if storm == None:
                    pass
                elif storm in (STORM_EAST, STORM_WEST):
                    self.bbd[blizz[storm]][y - x0 - 1][x - x0 - 1] = storm
                elif storm in (STORM_NORTH, STORM_SOUTH):
                    self.bbd[blizz[storm]][x - x0 - 1][y - y0 - 1] = storm
                else:
                    raise ValueError("Unexpected character", storm)

    def display(self, step=0):
        display(self.grid, self.overlay(step))

    def shift(self, step):
        shifted = []
        for i, rows in enumerate(self.bbd):
            shifted.append([ShiftList(row, step * SHIFT_DIRECTION[i]) for row in rows])
        return shifted

    @cache
    def overlay(self, step):
        """
        Storm overlay for step.
        """
        storms = {}
        bbd = self.shift(step)
        for y in range(y0 + 1, y1 - 1):
            for x in range(x0 + 1, x1 - 1):
                active = (
                    bbd[blizz[STORM_EAST]][y - x0 - 1][x - x0 - 1],
                    bbd[blizz[STORM_WEST]][y - x0 - 1][x - x0 - 1],
                    bbd[blizz[STORM_NORTH]][x - x0 - 1][y - y0 - 1],
                    bbd[blizz[STORM_SOUTH]][x - x0 - 1][y - y0 - 1],
                )
                active = tuple(a for a in active if a in STORM)
                if len(active) == 1:
                    storms[x + y * 1j] = active[0]
                elif len(active) > 1:
                    storms[x + y * 1j] = f"{len(active):02d}"
        return storms

    @cache
    def neighbors(self, step, coord):
        """
        Valid next locations for coord at step.
        """
        neighbors = []
        storms = self.overlay(step + 1)
        for side in SIDES:
            next = coord + side
            if self.grid.get(next) != WALL and storms.get(next) is None:
                neighbors.append((step + 1, next))
        return neighbors


b = Blizzard(grid)

start = 2 + 1j
goal = b.x1 - 2 + b.y1 * 1j - 1j

b.grid[start - 1j] = WALL
b.grid[goal + 1j] = WALL

display(b.grid, {start: "🧝", goal: "🥅"})


dg = DiGraph()


def bfs(start=start, t_start=0, goal=goal):
    # coord, step
    n = 0
    cur = [(t_start, n, start)]
    next_set = set()
    next = []
    for generation in range(1000):
        print("g", generation)
        while cur:
            here = cur.pop()
            # print(here)
            t, _, coord = here
            if coord == goal:
                print(f"Found {coord} at {t}, generation {generation}")
                return (t, coord)
            for neighbor in b.neighbors(t, coord):
                n += 1  # prevents < > against complex numbers
                tn, cn = neighbor
                if (tn, cn) not in next_set:
                    next_set.add((tn, cn))
                    next.append((neighbor[0], n, neighbor[1]))
                    # dg.add_edge((t, coord), (tn, cn))
        if not next_set:
            print("whoops")
            break
        display(b.grid, b.overlay(generation + 1) | {k[1]: "🟦" for k in next_set})
        time.sleep(0.1)
        cur = next
        next = []
        next_set = set()


t0, g0 = bfs()
assert g0 == goal
t1, g1 = bfs(goal, t0, start)
assert g1 == start
t2, g2 = bfs(start, t1, goal)
assert g2 == goal
