#!/usr/bin/env python
"""
Any (multi-digit) number adjacent to a symbol is a "part number" and should be
summed.
"""

import pprint
import re
from dataclasses import dataclass
from itertools import groupby
from pathlib import Path

from aocd import submit
from rich.console import Console

console = Console()

INPUT = Path(__file__).parent / "input.txt"

BIG_NUMBER = 2**33

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

    def reverse(self, n):
        # return increment to reach end of range
        for source, dest, size in self.ranges:
            source_end = source + size
            source_offset = n - source
            if source <= n < source_end:
                return dest + source_offset, source_end - n
        # none match
        return n, BIG_NUMBER


@dataclass
class SeedRange:
    ranges: list[list[int]]
    source = "seed"
    dest = "seed"

    def __init__(self, seeds):
        self.ranges = [[start, size] for start, size in zip(seeds[0::2], seeds[1::2])]

    def reverse(self, n):
        # return increment to reach end of range
        for source, size in self.ranges:
            if source <= n < (source + size):
                return n, BIG_NUMBER
        # not a valid seed
        return -1, BIG_NUMBER


def parse(lines) -> tuple[list[int], list[RangeMap]]:
    sections = [[*g] for k, g in groupby((line.strip() for line in lines), bool) if k]
    seeds = all_numbers("".join(sections[0]))
    ranges = [RangeMap(section) for section in sections[1:]]

    return seeds, ranges


def solve(input):
    seeds, ranges = parse(input)

    print("Seeds", seeds)

    answers = []
    for seed in seeds:
        n = seed
        for range in ranges:
            n = range[n]
        answers.append(n)
    print(list(zip(seeds, answers)), "\nSmallest:", min(answers))


def part_2(seeds, ranges):
    sr = SeedRange(seeds)
    print(sr)

    backwards = ranges[-1::-1] + [sr]

    i = 0
    while i < BIG_NUMBER:
        iprime = i
        steps = []
        for range in backwards:
            # print(range.dest, iprime, end="")
            iprime, step = range.reverse(iprime)
            # print(" to", range.source, iprime)
            steps.append(step)
        print(i, iprime, steps)
        i += min(steps)


if __name__ == "__main__":
    seeds, ranges = parse(SAMPLE)
    pprint.pprint(seeds)
    pprint.pprint(ranges)

    print("Example")
    solve(SAMPLE)

    print("\nPart 1")
    solve(INPUT.open())

    # Part the 2

    # Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.

    # The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:

    # seeds: 79 14 55 13

    # This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

    print("\nPart the 2")

    part_2(seeds, ranges)

    seeds2, ranges2 = parse(INPUT.open())
    part_2(seeds2, ranges2)
