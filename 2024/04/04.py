#!/usr/bin/env python

import aocd


directions = [(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if (i, j) != (0, 0)]


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


directions = [V(*d) for d in directions]

print(directions)


def parse(data, ignore=""):
    board: dict[tuple, str] = {}
    for i, line in enumerate(data.splitlines(), start=1):
        for j, char in enumerate(line.strip(), start=1):
            if char not in ignore:
                board[V(i, j)] = char
    return board


example = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

board = parse(aocd.data)


def isxmas(pos, direction, depth=0, pattern="XMAS"):
    if depth == len(pattern):
        return True
    if board.get(pos) == pattern[depth]:
        return isxmas(pos + direction, direction, depth=depth + 1)
    return False


def search():
    for direction in directions:
        for coord in board:
            yield isxmas(coord, direction)


## Part 2

board = parse("""\
.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........""")


def isx_mas(pos):
    NE = V(-1, -1)
    SW = V(1, 1)

    NW = V(-1, 1)
    SE = V(1, -1)

    ms = set("MS")

    return (
        board.get(pos) == "A"
        and set((board.get(pos + NE), board.get(pos + SW))) == ms
        and set((board.get(pos + NW), board.get(pos + SE))) == ms
    )


def search2():
    for pos in board:
        yield isx_mas(pos)


isx_mas(V(2, 3))

board = parse(aocd.data)

print(sum(search2()))
