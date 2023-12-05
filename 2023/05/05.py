#!/usr/bin/env python
"""
Any (multi-digit) number adjacent to a symbol is a "part number" and should be
summed.
"""

import itertools
import math
import pprint
import re
from dataclasses import dataclass
from pathlib import Path

from aocd import submit
from rich.console import Console

console = Console()

INPUT = Path("input.txt")

# destination, source, range size
# seed-to-soil
# 50 is destination "soil"
# 98 is source "seed"
SAMPLE = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
""".splitlines()


def all_numbers(line):
    return [int(x) for x in re.findall(r"\d+", line)]


@dataclass
class RangeMap:
    source: str
    dest: str
    ranges: list[list[int]]

    def __init__(self, lines):
        self.source, self.dest = lines[0].split(" ")[0].split("-to-")
        self.ranges = list(all_numbers(line) for line in lines[1:])

    def __getitem__(self, n):
        for dest, source, size in self.ranges:
            if source <= n < (source + size):
                return dest + (n - source)
        # none match
        return n


def parse(lines) -> tuple[list[int], list[RangeMap]]:
    initer = iter(lines)

    def n():
        return next(initer).strip()

    def grouping():
        return list(iter(n, ""))

    seeds = all_numbers("".join(grouping()))
    ranges = []
    while group := grouping():
        ranges.append(RangeMap(group))

    return seeds, ranges


if __name__ == "__main__":
    seeds, ranges = parse(SAMPLE)
    pprint.pprint(seeds)
    pprint.pprint(ranges)

    for seed in seeds:
        n = seed
        for range in ranges:
            n = range[n]
        print(n)

    seeds, ranges = parse(Path("input.txt").open())

    print("Seeds", seeds)

    answers = []
    for seed in seeds:
        n = seed
        for range in ranges:
            n = range[n]
        answers.append(n)
    print(list(zip(seeds, answers)), min(answers))
