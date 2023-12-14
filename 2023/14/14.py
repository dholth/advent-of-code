#!/usr/bin/env python
import aocd
from itertools import groupby, chain

data = aocd.data.splitlines()

t = str.maketrans({"O": "🪨", "#": "🧱", ".": "\N{FULLWIDTH FULL STOP}"})

example = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""".splitlines()

# data = example


def columns(board):
    for i in range(len(board[0])):
        yield "".join(row[i] for row in board)


def score(column):
    """
    The amount of load caused by a single rounded rock (O) is equal to the
    number of rows from the rock to the south edge of the platform, including
    the row the rock is on. (Cube-shaped rocks (#) don't contribute to load.)
    """
    return sum((element == "O") * i for i, element in enumerate(column[::-1], start=1))


ans = 0
for column in columns(data):
    shifted = [sorted(g, reverse=True) for k, g in groupby(column, lambda k: k == "#")]
    joined = "".join(chain(*shifted))
    ans += score(joined)

print("Part 1", ans)

cycles = 1000000000

"""
The parabolic reflector dish deforms, but not in a way that focuses the beam. To
do that, you'll need to move the rocks to the edges of the platform.
Fortunately, a button on the side of the control panel labeled "spin cycle"
attempts to do just that!

Each cycle tilts the platform four times so that the rounded rocks roll north,
then west, then south, then east. After each tilt, the rounded rocks roll as far
as they can before the platform tilts in the next direction. After one cycle,
the platform will have finished rolling the rounded rocks in those four
directions in that order.
"""


def tilt(data, reverse=True):
    for column in reversed(list(columns(data))):
        shifted = [
            sorted(g, reverse=reverse) for k, g in groupby(column, lambda k: k == "#")
        ]
        joined = "".join(chain(*shifted))
        yield joined


new_data = data


def display(board, message=""):
    print(f"--- {message}")
    print("\n".join([n.translate(t) for n in board]))


if False:
    print("No rotation 👆")
    display(data)
    # Roll North
    new_data = list(tilt(new_data))
    display(new_data, "First 👈")
    # Roll West
    new_data = list(tilt(new_data, reverse=False))
    display(new_data, "Second 👇")
    # Roll South
    new_data = list(tilt(new_data, reverse=True))
    display(new_data, "Third 👉")
    # Roll East
    new_data = list(tilt(new_data, reverse=False))
    display(new_data, "Fourth 👆")


def cycle(data):
    data = list(tilt(data))
    # Roll West
    data = list(tilt(data, reverse=False))
    # Roll South
    data = list(tilt(data, reverse=True))
    # Roll East
    data = list(tilt(data, reverse=False))
    return data


# display(cycle(data))
# display(cycle(cycle(cycle(data))))

import time

seen = {}

begin = time.time_ns()
i = 0
while i < cycles:
    data = cycle(data)
    key = "\n".join(data)
    if key in seen:
        print(f"{i} seen again, first seen at {seen[key]}")
        cycle_length = i - seen[key]
        print(f"{cycle_length} cycle length")
        skip = ((cycles - i) // cycle_length) * cycle_length
        i += skip + 1
        print(f"Skip ahead {skip} to {i}")
        seen.clear()
    else:
        seen[key] = i
    i += 1

end = time.time_ns()

print(f"1000 cycles took {(end-begin)/1e9:0.2f}s")
print(f"{cycles} cycles would take {(end-begin)/1e9*(cycles/1000)}s")

ans = 0
for column in columns(data):
    ans += score(column)

print("Part 2", ans)

display(data)
