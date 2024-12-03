#!/usr/bin/env python
from aocd import data
from itertools import pairwise

if False:
    data = """7 6 4 2 1
    1 2 7 8 9
    9 7 6 2 1
    1 3 2 4 5
    8 6 4 4 1
    1 3 6 7 9"""


def part1():
    for line in data.splitlines():
        nums = list(map(int, line.split()))
        yield score(nums)


def score(nums):
    # The levels are either all increasing or all decreasing.
    # Any two adjacent levels differ by at least one and at most three.

    safety = list(a - b for a, b in pairwise(nums))
    all_negative = all(x < 0 for x in safety)
    all_positive = all(x > 0 for x in safety)
    monotonous = all_negative or all_positive
    gradual = all(0 < abs(x) <= 3 for x in safety)
    return monotonous and gradual


print(sum(part1()))


def score2(nums):
    # The Problem Dampener is a reactor-mounted module that lets the reactor safety
    # systems tolerate a single bad level in what would otherwise be a safe report.
    # It's like the bad level never happened!

    easy = score(nums)
    if easy:
        return True
    for n in range(len(nums)):
        damped = nums[:n] + nums[n + 1 :]
        if score(damped):
            return True
    return False


def part2():
    for line in data.splitlines():
        nums = list(map(int, line.split()))
        yield score2(nums)


print(sum(part2()))
