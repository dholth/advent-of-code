#!/usr/bin/env python
import itertools
import sys
import time

import aocd
import numpy as np
import skimage.draw


example = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
""".splitlines()

EMPTY = 0
WALL = 1
SOURCE = 2
SAND = 3

SOURCE_COORD = (500, 0)


def parse(input):
    for line in input:
        yield [tuple(map(int, coord.split(","))) for coord in line.split("->")]


if sys.argv[1:2] == ["example"]:
    scan = list(parse(example))
else:
    scan = list(parse(aocd.lines))

xmin = min(x for x, y in itertools.chain.from_iterable(scan))
ymin = min(y for x, y in itertools.chain.from_iterable(scan))
xmax = max(x for x, y in itertools.chain.from_iterable(scan))
ymax = max(y for x, y in itertools.chain.from_iterable(scan))

print("Lines", len(aocd.lines))
print("Min", (xmin, ymin))
print("Size", (xmax, ymax))

# puzzles are 1-indexed, and leave room for falling off the edge
array = np.zeros((xmax + ymax, ymax + 2), np.byte)

array[SOURCE_COORD] = SOURCE

for path in scan:
    for start, end in itertools.pairwise(path):
        x0, y0 = start
        x1, y1 = end
        assert x0 == x1 or y0 == y1

        # rows, columns
        (
            rr,
            cc,
        ) = skimage.draw.line(x0, y0, x1, y1)

        array[rr, cc] = WALL


def asstr(array, xmin=xmin, xmax=None):
    return "\n".join(
        reversed(
            list(
                "".join("\N{FULLWIDTH FULL STOP}\N{ROCK}⏳🟡"[val] for val in row)
                for row in array[xmin - 1 : xmax]
            )
        )
    )


def display(array, xmin=xmin, xmax=None):
    """
    Show in terminal.
    """
    print(asstr(array, xmin, xmax))


def plot(array):
    # this works well
    import matplotlib.pyplot as plt

    plt.imshow(array, interpolation="none")
    plt.show()


# A unit of sand always falls down one step if possible. If the tile immediately
# below is blocked (by rock or sand), the unit of sand attempts to instead move
# diagonally one step down and to the left. If that tile is blocked, the unit of
# sand attempts to instead move diagonally one step down and to the right. Sand
# keeps moving as long as it is able to do so, at each step trying to move down,
# then down-left, then down-right. If all three possible destinations are
# blocked, the unit of sand comes to rest and no longer moves, at which point
# the next unit of sand is created back at the source.


def next_positions(position: np.ndarray):
    next = [(0, 1), (-1, 1), (1, 1)]
    for n in next:
        yield position + n


rested = []


def fall():
    total_steps = 0
    firstfall = False
    step = 0
    total_steps = 0

    for grains in range(1, 30000):  # size of dune above cave
        position = np.array(SOURCE_COORD, np.int32)
        for step in range(ymax + 1):
            total_steps += 1

            for p1 in next_positions(position):
                if array[tuple(p1)] == EMPTY:
                    if position[1] != 0:  # keep hourglass
                        array[tuple(position)] = EMPTY
                    position = p1
                    array[tuple(position)] = SAND
                    break
            else:
                break

        # catch those on floor
        rested.append(np.array(position))

        if step == ymax:
            display(array, xmin, xmax + 2)
            print("Fell off end! Iterations:", total_steps)
            print("Rested array length", len(rested))
            print("How many are sand?", np.count_nonzero(array == SAND))
            print("Grains dropped", grains)
            print()
            if not firstfall:
                time.sleep(2)
                firstfall = True
        elif np.all(position == SOURCE_COORD):
            # get rid of hourglass
            array[tuple(position)] = SAND
            print("Grains dropped", grains)
            return total_steps


total_steps = fall()

display(array, xmin, xmax + 2)
print("Iterations:", total_steps)
print("'rested' array length:", len(rested))
print("How many are sand?", np.count_nonzero(array == SAND))

has_sand = [np.count_nonzero(row == SAND) for row in array]
xmin_real = min(i for i, val in enumerate(has_sand) if val)
xmax_real = max(i for i, val in enumerate(has_sand) if val)
print("limits are -x, x, y:", xmin_real, xmax_real, ymax)
print("array size", array.shape)

plot(array[xmin_real : xmax_real + 1])
