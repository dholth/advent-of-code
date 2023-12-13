#!/usr/bin/env python

import aocd
from itertools import groupby, pairwise
from rich.console import Console

console = Console()
print = console.print

data: str = aocd.data  # type: ignore
boards = [[*g] for k, g in groupby(data.splitlines(), bool) if k]


def columns(board):
    for i in range(len(board[0])):
        yield "".join(row[i] for row in board)


def find_mirror(i, board):
    sames = 0
    mirrors = 0
    for j, (row1, row2) in enumerate(pairwise(board)):
        if row1 == row2:
            print(f"Board {i} {j}=={j+1}")
            ahead = board[j + 1 :]
            behind = board[j::-1]
            assert ahead[0] == behind[0]
            if all(a == b for a, b in zip(ahead, behind)):
                print(f"Mirror found at {i:2} {j:2}")
                return j + 1
                mirrors += 1
            sames += 1
    assert mirrors < 2
    print()
    return 0


def find_smudge(i, board):
    mirrors = 0
    for j, (row1, row2) in enumerate(pairwise(board)):
        ahead = board[j + 1 :]
        behind = board[j::-1]
        if sum(count_unequal(a, b) for a, b in zip(ahead, behind)) == 1:
            print(f"Smudge found at {i:2} {j:2}")
            return j + 1
            mirrors += 1
    assert mirrors < 2
    return 0


def count_unequal(a: str, b: str):
    return sum(a != b for a, b in zip(a, b))


def go():
    answer = 0
    for i, board in enumerate(boards):
        answer += find_mirror(i, board) * 100
        answer += find_mirror(i, list(columns(board)))

    console.print("Part 1", answer)

    smudge = 0
    for i, board in enumerate(boards):
        smudge_previous = smudge
        smudge += find_smudge(i, board) * 100
        smudge += find_smudge(i, list(columns(board)))
        if smudge_previous == smudge:
            console.print("Found no smudge on", i)

    console.print("Part 2", answer)


"""To summarize your pattern notes, add up the number of columns to the left of
each vertical line of reflection; to that, also add 100 multiplied by the number
of rows above each horizontal line of reflection. In the above example, the
first pattern's vertical line has 5 columns to its left and the second pattern's
horizontal line has 4 rows above it, a total of 405."""


if __name__ == "__main__":
    go()
