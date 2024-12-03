#!/usr/bin/env python
# Elf gardener walks from S


import aocd
from rich.console import Console
from itertools import product

print = Console().print

EMOJI = str.maketrans({"#": "🪨", ".": "\N{FULLWIDTH FULL STOP}", "S":"\N{Chequered FLAG}"})

directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

# column, row
N = (0, -1)
S = (0, 1)
E = (1, 0)
W = (-1, 0)

example = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""".splitlines()


def adjacent(board, coord):
    """
    Neighbors according to N, S, E, W
    """
    for x, y in (N, S, E, W):
        neighbor = (coord[0] + x, coord[1] + y)
        if not board.get(neighbor):
            continue
        yield neighbor


def load(lines, exclude="#"):
    board: dict[tuple, str] = {}

    for i, line in enumerate(lines, start=1):
        for j, char in enumerate(line, start=1):
            if char not in exclude:
                board[(j, i)] = char

    return board


board_grid = aocd.data.splitlines()
regular_board = load(board_grid)


def step(starts, neighbors=adjacent, board={}):
    visited = set()
    for here in starts:
        for neighbor in neighbors(board, here):
            visited.add(neighbor)
    return visited


def display(visited, marked={}, board_grid=""):
    for y, line in enumerate(board_grid, start=1):
        row = []
        for x, c in enumerate(line, start=1):
            if (x, y) in visited:
                color = "red"
                c = "\N{ELF}"
            elif c == "S":
                color = "bright_cyan"
            elif (x, y) in marked:
                color = ("red", "blue")[marked[(x, y)]]
            else:
                color = "grey"
            row.append(f"[{color}]{c.translate(EMOJI)}")
        print("".join(row))
    print("Red is outside, green is circuit, blue is inside")


def go(lines, distance=64):
    board = load(lines)

    coord = (0, 0)
    for coord, char in board.items():
        if char == "S":
            break

    reachable = set()
    reachable.add(coord)
    for i in range(distance):
        reachable = step(reachable, board=board)
        if (i % 32) == 0:
            display(reachable, board_grid=lines)
            input()

    print(len(reachable))
    return len(reachable)


# result = go(aocd.data.splitlines(), distance=64)


example2 = """.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##...####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##..S####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##...####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
................................."""


# example2 = aocd.data


def double_example(example):
    return [
        "".join((line.replace("S", "."), line, line.replace("S", ".")))
        for line in example
    ]


# extra_example = double_example(example2.replace("S", ".").splitlines())

# result = go(
#     extra_example + double_example(example2.splitlines()) + extra_example, distance=1000
# )

ELF_STEPS = 26501365

full_data = aocd.data.splitlines()

print(f"{len(full_data)}x{len(full_data[0])}; {ELF_STEPS/len(full_data)} blocks wide")