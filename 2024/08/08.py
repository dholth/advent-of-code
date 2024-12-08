#!/usr/bin/env python

import itertools
from collections import defaultdict, deque

import aocd

FILLER = "\uff03"
PRETTY = {
    " ": "\N{FULLWIDTH FULL STOP}",
    ".": "\N{FULLWIDTH FULL STOP}",
    "#": "🧱",
    ">": "👉",
    "<": "👈",
    "^": "👆",
    "v": "👇",
}

# fullwidth letters = 0xfee0 + ord(ascii letter)

PRETTY.update((chr(i), chr(0xFEE0 + i)) for i in range(ord("0"), ord("{")))


class V(tuple):
    def __new__(cls, *args):
        return super(V, cls).__new__(cls, args)

    def __add__(self, other):
        return self.__class__(*(a + b for a, b in zip(self, other)))

    def __sub__(self, other):
        return self.__class__(*(a - b for a, b in zip(self, other)))

    def __mul__(self, scale):
        return self.__class__(*(a * scale for a in self))

    def taxi(self):
        a, b = self
        return int(abs(a) + abs(b))

    def __repr__(self):
        return f"V{str((*self,))}"


def parse(data, ignore="") -> dict[V, str]:
    board = {}
    for i, line in enumerate(data.splitlines(), start=1):
        for j, char in enumerate(line.strip(), start=1):
            if char not in ignore:
                board[V(j, i)] = char
    return board


def bounds(grid):
    """
    Bounds for a 1-indexed grid.
    """
    x0, y0, x1, y1 = 1, 1, 1, 1
    for x, y in grid:
        x0 = min(x0, x)
        x1 = max(x1, x)
        y0 = min(y0, y)
        y1 = max(y1, y)
    x0, x1, y0, y1 = map(int, (x0, x1, y0, y1))
    return x0, x1, y0, y1


def display(grid, overlay={}):
    grid = dict(grid)
    grid.update(overlay)
    x0, x1, y0, y1 = bounds(grid)
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
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

example1 = """\
..........
...#......
..........
....a.....
..........
.....a....
..........
......#...
..........
..........
"""

board = parse(aocd.data)

display(board)
print()


def group_by_frequency(board, ignore="."):
    by_frequency: dict[str, list[tuple[V, str]]] = {
        f: [v for v in board.items() if v[1] == f]
        for f in set((board.values()))
        if f not in ignore
    }
    return by_frequency


def group_by_frequency_2(board, ignore="."):
    by_frequency: dict[str, list[tuple[V, str]]] = {
        f: [v for v in board.items() if v[1] == f]
        for f in set((board.values()))
        if f not in ignore
    }

    by_frequency = {}
    for v, f in board.items():
        if f in ignore:
            continue
        group = by_frequency.get(f, [])
        group.append(v)
        by_frequency[f] = v

    return by_frequency


def consume(it):
    return deque(it, maxlen=0)


def group_by_frequency_3(board, ignore="."):
    by_frequency = defaultdict(list)
    consume(by_frequency[v[1]].append(v) for v in board.items() if v[1] not in ignore)
    return dict(by_frequency)


by_frequency = group_by_frequency_3(board)

antinodes = {}
for frequency, nodes in by_frequency.items():
    for first, second in itertools.combinations(nodes, 2):
        antinodes[(first[0] - second[0]) + first[0]] = "b"
        antinodes[(second[0] - first[0]) + second[0]] = "c"

display(board, antinodes)

# OOB = (new location not in board)

print("Part 1", len(set(k for k in antinodes if k in board)))

exampleT = """\
T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
..........
"""

boardT = parse(exampleT)

by_frequency = group_by_frequency_3(boardT, ignore=".#")


def more_antinodes(board, by_frequency):
    antinodes = {}
    for frequency, nodes in by_frequency.items():
        for first, second in itertools.combinations(nodes, 2):
            for a, b in (first, second), (second, first):
                for i in range(100):
                    candidate = (a[0] - b[0]) * i + a[0]
                    if candidate not in board:
                        # out of bounds
                        break
                    antinodes[candidate] = "#"
                else:
                    raise RuntimeError("too many iterations")

    return antinodes


ma = more_antinodes(boardT, by_frequency)

display(boardT, ma)

print(len(ma))

part2 = more_antinodes(board, group_by_frequency(board))

display(board, part2)

print(len(part2))
