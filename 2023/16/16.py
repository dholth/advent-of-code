#!/usr/bin/env python

import sys
import time
from collections import defaultdict

import aocd
from rich.console import Console

print = Console().print

sys.setrecursionlimit(32768)

data = aocd.data.splitlines()

t = str.maketrans(
    {
        "/": "\N{FULLWIDTH SOLIDUS}",
        "\\": "\N{FULLWIDTH REVERSE SOLIDUS}",
        ".": "\N{FULLWIDTH FULL STOP}",
        "-": "\N{FULLWIDTH HYPHEN-MINUS}",
        "|": "\N{FULLWIDTH VERTICAL LINE}",
    }
)


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
N = V(0, -1)
S = V(0, 1)
E = V(1, 0)
W = V(-1, 0)


def display(board, message=""):
    print(f"--- {message}")
    print("\n".join([n.translate(t) for n in board]))


def load(lines):
    board: dict[tuple, str] = {}

    for i, line in enumerate(lines, start=1):
        for j, char in enumerate(line, start=1):
            board[(j, i)] = char

    return board


display(data)


#   N
# W   E
#   S


visited = defaultdict(set)


def display_visited(lines, visited):
    for i, line in enumerate(lines, start=1):
        show = []
        for j, char in enumerate(line, start=1):
            pos = (j, i)
            if char == "." and (j, i) in visited:
                show.append("\N{SUN WITH FACE}")
            else:
                show.append(char)
        print("".join(show).translate(t))


def raycast(board, position, direction):
    try:
        here = board[position]
    except KeyError:
        return

    if direction in visited[position]:
        return

    visited[position].add(direction)

    # display_visited(data, visited)
    # print()
    # time.sleep(0.01)
    # input()

    match here:
        case ".":
            raycast(board, position + direction, direction)
        case "\\":
            direction = {N: W, S: E, E: S, W: N}[direction]
            raycast(board, position + direction, direction)
        case "/":
            direction = {N: E, S: W, E: N, W: S}[direction]
            raycast(board, position + direction, direction)
        case "|":
            if direction in (N, S):
                raycast(board, position + direction, direction)
            else:
                raycast(board, position + N, N)
                raycast(board, position + S, S)
        case "-":
            if direction in (E, W):
                raycast(board, position + direction, direction)
            else:
                raycast(board, position + E, E)
                raycast(board, position + W, W)


board = load(data)

try:
    raycast(board, V(1, 1), V(1, 0))
except RecursionError:
    print("End with recursion error")
    pass

display_visited(data, visited)
print(len(visited))
print(len(board))
