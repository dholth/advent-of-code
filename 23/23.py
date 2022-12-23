#!/usr/bin/env python

from collections import Counter
from itertools import chain, cycle, islice

import aocd

example = """\
.....
..##.
..#..
.....
..##.
.....
"""

example1 = """\
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
"""

ELF = "#"

# using (1, 1) as top left
def parse(lines):
    grid = {}

    lines = iter(lines)
    for y, line in enumerate(lines, 1):
        if not line:
            break
        for x, char in enumerate(line, 1):
            if char == ELF:
                grid[x + y * 1j] = char
    return grid


PRETTY = {" ": "\N{FULLWIDTH MACRON}", "#": "🧝", ".": "\N{FULLWIDTH FULL STOP}"}

dir_num = {1 + 0j: 0, 1j: 1, -1: 2, -1j: 3}
num_dir = {v: k for k, v in dir_num.items()}
# directions: 0 right, 1 down, 2 left, 3 up
# directions: 0 east, 1 south, 2 west, 3 north

# in the order initially considered
compass = {"N": num_dir[3], "S": num_dir[1], "W": num_dir[2], "E": num_dir[0]}


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
                    grid.get(x + y * 1j, "\N{FULLWIDTH MACRON}"),
                    grid.get(x + y * 1j, "\N{FULLWIDTH MACRON}"),
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


grid = parse(example1.splitlines())

# grid = parse(aocd.lines)

# If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north one step.
# If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south one step.
# If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west one step.
# If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east one step.

# If no other Elves are in one of those eight positions, the Elf does not do anything during this round.

MUST_BE_EMPTY = {
    "N": (-1j, -1 - 1j, +1 - 1j),
    "S": (1j, -1 + 1j, 1 + 1j),
    "E": (1, 1 + 1j, 1 - 1j),
    "W": (-1, -1 + 1j, -1 - 1j),
}

ALL_NEIGHBORS = set(chain(*MUST_BE_EMPTY.values()))

# yield current, proposed positions for all elves
def proposals(grid, priority: list):
    for coord in grid:
        if not any(grid.get(coord + c) == ELF for c in ALL_NEIGHBORS):
            continue
        for d in priority:
            if not any(grid.get(coord + c) == ELF for c in MUST_BE_EMPTY[d]):
                yield coord, coord + compass[d]
                break


def move(grid, ps, counts=None):
    motion = 0
    if not counts:
        counts = Counter(ps.values())
    for k, v in ps.items():
        if counts[v] == 1:
            motion += 1
            del grid[k]
            grid[v] = ELF
    return motion


priority = cycle(compass)

turn = 0
for turn in range(1, 10000):  # 1-index for the win?
    consider = list(islice(priority, 4))
    next(priority)  # so first direction chosen will cycle around
    print(f"{consider}")
    ps = dict(proposals(grid, consider))
    counts = Counter(ps.values())
    print("🌳")
    display(
        grid, {v: ("❌" if counts[v] == 1 else f"{counts[v]:02d}") for v in ps.values()}
    )
    moves = move(grid, ps, counts)
    if moves == 0:
        print(f"Stopped at {turn}")
        break

    # input()

print("🌳")
display(grid)

print(f"Stopped at {turn}")

x0, x1, y0, y1 = limits(grid)
area = (x1 - x0) * (y1 - y0)
print(area)
area_without_elves = area - sum(bool(x == ELF) for x in grid.values())
print("Area without elves", area_without_elves)
