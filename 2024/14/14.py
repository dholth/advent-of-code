#!/usr/bin/env python

import operator
import re
from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
import statistics

import aocd

FILLER = "\uff03"
PRETTY = {
    " ": "\N{FULLWIDTH FULL STOP}",
    ".": "\N{FULLWIDTH FULL STOP}",
    "#": "🧱",
    "R": "🤖",
}


class V(tuple):
    def __new__(cls, *args):
        return super(V, cls).__new__(cls, args)

    def __add__(self, other):
        return self.__class__(*(a + b for a, b in zip(self, other)))

    def __sub__(self, other):
        return self.__class__(*(a - b for a, b in zip(self, other)))

    def __mul__(self, scale):
        return self.__class__(*(a * scale for a in self))

    def __mod__(self, other):
        return self.__class__(*(a % b for a, b in zip(self, other)))

    def taxi(self):
        a, b = self
        return int(abs(a) + abs(b))

    def __repr__(self):
        return f"V{str((*self,))}"


@dataclass
class Robot:
    p: V
    v: V


def parse(data: str):
    for line in data.splitlines():
        a, b, c, d = map(int, re.findall(r"-?\d+", line))
        yield Robot(p=V(a, b), v=V(c, d))


def display(robots, size: tuple, show_quadrants=False):
    grid = {robot.p: robot for robot in robots}
    width, height = size

    midpoint = size[0] // 2, size[1] // 2

    for y in range(height):
        row = []
        for x in range(width):
            if (x, y) in grid:
                row.append("\N{ROBOT FACE}")
            else:
                # row.append("\N{FULLWIDTH FULL STOP}")
                row.append("  ")  # double space as fullwidth

            if show_quadrants and (x == midpoint[0] or y == midpoint[1]):
                row[-1] = PRETTY.get("#")

        print("".join(row))


def by_quadrant(robots, size: tuple):
    width, height = size
    midpoint = width // 2, height // 2
    mw, mh = midpoint

    by_quadrant = defaultdict(list)

    for robot in robots:
        x, y = robot.p
        quadrant = (x > mw) - (x < mw), (y > mh) - (y < mh)
        if not any(c == 0 for c in quadrant):
            by_quadrant[quadrant].append(robot)

    return dict(by_quadrant)


def triangularity(q):
    # express many more on one side of the chart

    # V(17, 7) (-1, -1) Top Left
    # V(92, 46) (1, -1) Top Right
    # (-1, 1) Bottom left
    # (1, 1) Bottom right

    tl = len(q[(-1, -1)])
    tr = len(q[(1, -1)])
    bl = len(q[(-1, 1)])
    br = len(q[(1, 1)])

    top_bottom = abs((tl + tr) - (bl + br))

    left_right = abs((tl + bl) - (tr + br))

    return max(top_bottom, left_right)


example = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

robots = list(parse(example))


def simulate(robots: list[Robot], seconds: int, size: tuple):
    for robot in robots:
        robot.p = (robot.p + robot.v * seconds) % size


print("Initial state")
display(robots, (11, 7))

simulate(robots, 100, (11, 7))

print("After 100 seconds")
display(robots, (11, 7), show_quadrants=True)

print(
    "Example",
    reduce(operator.mul, (len(v) for v in by_quadrant(robots, (11, 7)).values())),
)

full_size = (101, 103)
robots = list(parse(aocd.data))
assert len(robots) == len(aocd.data.splitlines())
simulate(robots, 100, full_size)
display(robots, full_size, show_quadrants=True)

print(
    "Part 1",
    reduce(operator.mul, (len(v) for v in by_quadrant(robots, full_size).values())),
)

## Part 2 (look for christmas tree)


def count_top_left(robots):
    return sum((1 < robot.p[0] < 32 and 1 < robot.p[1] < 32) for robot in robots)


def spreadness(robots):
    x, y = list(zip(*(robot.p for robot in robots)))
    return statistics.pstdev(x) * statistics.pstdev(y)


robots = list(parse(aocd.data))
max_tri = 1
min_spread = 1e9
frame_displayed = 0
for i in range(1, 6476):
    simulate(robots, 1, full_size)
    # winning implementation showed frames matching tri * .9, but

    # tri = triangularity(by_quadrant(robots, full_size))
    spread = spreadness(robots)
    if spread < min_spread:
        frame_displayed += 1
        # print("\033[2J\033[H")  # clear screen and move to home
        # max_tri = max(tri, max_tri)
        min_spread = min(spread, min_spread)
        display(robots, full_size)
        print(f"{i} seconds elapsed\n")
        # print("Triangularity", tri, "Max", max_tri, "Ratio", tri / max_tri)
        print("pstdev X", statistics.pstdev(robot.p[0] for robot in robots))
        print("pstdev Y", statistics.pstdev(robot.p[1] for robot in robots))
        print("f(X) * f(Y)", spread)
        print(f"Showed {frame_displayed} frames")

    if i % 1000 == 0:
        print(f"{i} steps")

# >>> unicodedata.name('\u3000')
# 'IDEOGRAPHIC SPACE'
