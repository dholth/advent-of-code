#!/usr/bin/env python
"""
Day 5: Cafeteria
"""

import itertools
import re
from dataclasses import dataclass

import aocd

data = aocd.data

sample = """3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""


@dataclass
class DB:
    fresh: list[range]
    ingredients: list[int]


def parse(data):
    lines = iter(data.splitlines())

    fresh = []
    for line in lines:
        if not line.strip():
            break
        start, stop = tuple(int(n) for n in re.findall(r"\d+", line))
        fresh.append(range(start, stop + 1))  # not sorted

    ingredients = []
    for line in lines:
        ingredients.append(int(line))

    return DB(fresh, ingredients)


db = parse(data)
db.fresh.sort(key=lambda r: r.start)

count = 0
for ingredient in db.ingredients:
    for r in db.fresh:
        if ingredient in r:
            count += 1
            break

print(f"{count} fresh ingredients")

# Now count all of the ingredient ID's that are considered to be fresh.


def show_issues(fresh: list[range]):
    for r1, r2 in itertools.pairwise(fresh):
        if r1.start == r2.start:
            print(f"Equal starts {r1} len1 {len(r1)} len2 {len(r2)}")
        if r1.stop > r2.stop:
            print("Complete overlap", r1, r2)


def remove_overlaps(fresh: list[range]):
    """
    Given a sorted list of ranges, yield new ranges that do not overlap or that
    have zero length.

    Broken.
    """
    for i, r in enumerate(fresh):
        if len(fresh) < i + 1 and r.stop > fresh[i + 1].start:
            yield range(r.start, fresh[i + 1].start)
        else:
            yield r


print("Remaining issues:")
show_issues(list(remove_overlaps(db.fresh)))


def merge_ranges(fresh: list[range]):
    """
    Split ranges into starts and stops.

    If we are in any range, number of ranges we are in is > 0.

    Otherwise, number of ranges we are in is 0.

    Yield a range when the number of ranges we are in drops to 0.
    """

    starts_stops = []
    for r in fresh:
        starts_stops.append((r.start, 1))
        starts_stops.append((r.stop, -1))

    starts_stops.sort()

    depth = 0
    start = 0
    for n, inc in starts_stops:
        depth += inc
        if depth == 1 and inc == 1:
            start = n
        if depth == 0 and inc == -1:
            stop = n
            print(f"Merged {start}-{stop}")
            yield range(start, stop)
        if depth < 0:
            print("Underwater", depth)
        else:
            print(depth)


db2 = parse(sample)

print("Sample part 2", sum(len(r) for r in merge_ranges(db2.fresh)))

print("Part 2", sum(len(r) for r in merge_ranges(db.fresh)))
