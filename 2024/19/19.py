#!/usr/bin/env python
"""
Arranging towels.
"""

import aocd
import dataclasses
import functools

example = """\
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""


def search(pattern, towels: frozenset[str]):
    if pattern == "":
        return True

    possible = False
    for towel in towels:
        if pattern.startswith(towel):
            next = pattern[len(towel) :]
            if search(next, towels):
                return True

    return possible


# The first line indicates the available towel patterns; in this example, the
# onsen has unlimited towels with a single red stripe (r), unlimited towels with
# a white stripe and then a red stripe (wr), and so on.


@functools.cache
def count(pattern, towels: frozenset[str], debug=False):
    if pattern == "":
        return 1

    possibilities = 0
    for towel in towels:
        if pattern.startswith(towel):
            next = pattern[len(towel) :]
            if debug:
                print(f"{towel}|{next}")
            possibilities += count(next, towels, debug=debug)

    return possibilities


@dataclasses.dataclass
class Puzzle:
    towels: frozenset[str]
    patterns: list[str]


def parse(data: str):
    lines = data.splitlines()
    towels = lines[0].split(", ")
    assert not lines[1]  # blank line
    patterns = lines[2:]

    return Puzzle(towels=frozenset(towels), patterns=patterns)


def partExample():
    ex = parse(example)
    print(ex)

    for pattern in ex.patterns:
        print(pattern, search(pattern, ex.towels))


def part1():
    print("Part 1")
    p = parse(aocd.data)
    ans = 0
    for i, pattern in enumerate(p.patterns):
        print(
            f"{i} of {len(p.patterns)}", pattern, possible := search(pattern, p.towels)
        )
        ans += possible
    print("Answer", ans)
    return ans


def part2(data, debug=True):
    p = parse(data)
    print(p)
    ans = 0
    for i, pattern in enumerate(p.patterns):
        print(
            f"{i} of {len(p.patterns)}",
            pattern,
            ans1 := count(pattern, p.towels, debug=debug),
        )
        ans += ans1

    return ans


part1()
print()

ans2 = part2(example)
print(f"{ans2} ways")
print()

print("Part 2, full input")
ans2 = part2(aocd.data, debug=False)
print(f"{ans2} ways")
