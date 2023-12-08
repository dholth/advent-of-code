#!/usr/bin/env python

from __future__ import annotations

import collections as c
from dataclasses import dataclass

import aocd.utils

# contains one zero
nums = [*map(int, aocd.lines)]
counts = c.Counter(nums)
assert counts[0] == 1

print(f"Length is {len(nums)}")
print(min(nums), max(nums))


@dataclass
class DN:
    i: int
    v: int
    i0: int

    def __init__(self, i, v):
        self.i = i  # original index
        self.v = v  # value
        self.i0 = i  # new index


def track_indexes(ex):
    return elfcrypt(ex)


def elfcrypt(ex, repeat=1, key=1):
    values = list(DN(*v) for v in enumerate(ex))
    for value in values:
        value.v *= key

    new = list(values)
    l = len(ex)

    for _ in range(repeat):
        for val in values:
            forward_amount = val.v % (l - 1)  # is this 0 vs 1 indexing
            new_index = val.i0 + forward_amount
            for i in range(val.i0, new_index):
                new[i % l] = new[(i + 1) % l]
                new[i % l].i0 = i % l
            new[new_index % l] = val
            val.i0 = new_index % l

    return new


# if always moving ahead, doesn't affect anything behind...

result = track_indexes(nums)
zero = [r for r in result if r.v == 0][0]
p1 = (
    result[zero.i0 + 1000].v
    + result[zero.i0 + 2000].v
    + result[(zero.i0 + 3000) % len(result)].v
)
print("Part 1", p1)

result = elfcrypt(nums, repeat=10, key=811589153)
zero = [r for r in result if r.v == 0][0]
p2 = sum(result[(zero.i0 + n) % len(result)].v for n in (1000, 2000, 3000))
print("Part 2", p2)
