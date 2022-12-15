#!/usr/bin/env python
from __future__ import annotations

from dataclasses import dataclass
import aocd
from itertools import *


try:
    pairwise
except:

    def pairwise(iterable):
        # pairwise('ABCDEFG') --> AB BC CD DE EF FG
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)


example = """\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
""".splitlines()


def parse(lines):
    for line in lines:
        line = iter(line)
        vals = [
            int("".join(group))
            for k, group in groupby(line, lambda c: (c == "-" or c.isdigit()))
            if k
        ]
        yield vals


def manhattan(coord):
    return int(abs(coord.real) + abs(coord.imag))


@dataclass
class Sensor:
    coord: int
    beacon: int

    def __init__(self, x, y, bx, by):
        self.coord = x + y * 1j
        self.beacon = bx + by * 1j
        self.influence = manhattan(self.coord - self.beacon)

    @property
    def x(self):
        return int(self.coord.real)

    @property
    def y(self):
        return int(self.coord.imag)

    @property
    def ymin(self):
        return int(self.coord.imag - self.influence)

    @property
    def ymax(self):
        """
        End y coordinate (exclusive)
        """
        return int(self.coord.imag + self.influence + 1)

    def span(self, y):
        # [start and end coordinate) of influence at y
        ydist = abs(self.y - y)
        influence = self.influence
        if ydist > influence:
            return range(0, 0)
        else:
            return range(
                int(self.coord.real - influence + ydist),
                int(self.coord.real + influence - ydist + 1),
            )

    def spans(self):
        for y in range(self.y - self.influence, self.y + self.influence):
            yield y, self.span(y)


sensors = [Sensor(*l) for l in parse(example)]
for s in sensors:
    print(s.coord - s.beacon, manhattan(s.coord - s.beacon))

    if s.coord == 8 + 7j:
        print("special", s)

        for y in range(-3, 17):
            print(y, s.span(y))

sensors = [Sensor(*l) for l in parse(aocd.lines)]

interest = set()
SPECIAL_LINE = 2000000
for s in sensors:
    print(s.span(SPECIAL_LINE))
    # goodbye RAM
    interest.update(s.span(SPECIAL_LINE))

for s in sensors:
    if s.beacon.imag == SPECIAL_LINE:
        print("Oh hoho")
        interest.discard(int(s.beacon.real))

print("Part 1", len(interest))

# Your handheld device indicates that the distress signal is coming from a
# beacon nearby. The distress beacon is not detected by any sensor, but the
# distress beacon must have x and y coordinates each no lower than 0 and no
# larger than 4000000.

# To isolate the distress beacon's signal, you need to determine its tuning
# frequency, which can be found by multiplying its x coordinate by 4000000 and
# then adding its y coordinate.

# In the example above, the search space is smaller: instead, the x and y
# coordinates can each be at most 20. With this reduced search area, there is
# only a single position that could have a beacon: x=14, y=11. The tuning
# frequency for this distress beacon is 56000011.

# Find the only possible position for the distress beacon. What is its tuning
# frequency?

sensors = [Sensor(*l) for l in parse(example)]
grid = dict()
for s in sensors:
    for y, span in s.spans():
        grid.update({(x + y * 1j): "#" for x in span})

for s in sensors:
    grid[s.coord] = "S"
    grid[s.beacon] = "B"


def display(grid, x0=494, x1=508, y0=0, y1=14):
    print("🕳")
    for y in range(y0, y1):
        print("".join(grid.get(x + y * 1j, ".") for x in range(x0, x1)))


grid[14 + 11j] = "X"

display(grid, 0, 21, 0, 20)

y = 11


def get_ranges(sensors, y=11):
    return sorted(
        (sp for sp in (s.span(y) for s in sensors) if sp), key=lambda r: r.start
    )


ranges = get_ranges(sensors)


# several broken merge functions
def merge(r1: range, r2: range):
    if r2 is None:
        return r1
    if r1.stop > r2.start:
        return range(r1.start, max(r1.stop, r2.stop))


for r1, r2 in pairwise(ranges):
    print(r1, r2, merge(r1, r2))

print("ranges", ranges)
merged = [ranges.pop()]

while ranges:
    smaller = ranges.pop()
    bigger = merged[-1]
    m = merge(smaller, bigger)
    if m:
        merged[-1] = m
    else:
        merged.append(smaller)

merged = []
ranges = iter(get_ranges(sensors))
for something in ranges:
    for s2 in ranges:
        print("try to merge", something, s2)
        m = merge(something, s2)
        if m:
            something = m
        else:
            break
    merged.append(something)

print("merged 2", merged)


ranges = get_ranges(sensors)


# from github.com/dholth/httpfile
def merge_4(ranges: list[range]):
    merged: list[range] = []
    for r in ranges:
        if merged and r.start < merged[-1].stop:
            last = merged[-1]
            merged[-1] = range(last.start, max(last.stop, r.stop))
        else:
            merged.append(r)
    return merged


print(merge_4(ranges))

import time

begin = last = time.time()

sensors = [Sensor(*l) for l in parse(aocd.lines)]

# track which sensors are within the y range?

ystarts = sorted(s.ymin for s in sensors)
print(ystarts)


SEARCH_MAX = 4000000
all_sensors = sensors
for y0, y1 in pairwise(ystarts):
    if y1 < 0 or y0 > SEARCH_MAX:
        continue

    # limit to sensors overlapping current y coordinates
    sensors = [
        s
        for s in all_sensors
        if merge(*sorted([range(y0, y1), range(s.ymin, s.ymax)], key=lambda r: r.start))
    ]

    # approximately doubles speed
    print(f"⛰ Range {y0}-{y1} with {len(sensors)}")

    for y in range(max(y0, 0), min(y1, SEARCH_MAX)):
        ranges = get_ranges(sensors, y)
        # allranges = get_ranges(all_sensors, y)
        # if ranges != allranges:
        # print("oops", ranges, allranges, y)
        for l, r in pairwise(merge_4(ranges)):
            if 0 < l.stop < r.start < SEARCH_MAX:
                print("Ranges:", ranges)
                print("Found", l, r, y * 1j)
                print("Part 2", l.stop * 4000000 + y)
        if y % 1000 == 0:
            now = int(time.time())
            if now > last:
                last = int(time.time())
                print(y, "%0.2f/s" % (y / (now - begin)))
