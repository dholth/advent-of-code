#!/usr/bin/env python

from collections import defaultdict

import aocd
import functools
import itertools
import time
import timeit


def parse(data):
    return tuple(map(int, data.split()))


example = "0 1 10 99 999"

print(parse(example))


@functools.cache
def blink(stone):
    """
    If the stone is engraved with the number 0, it is replaced by
    a stone engraved with the number 1.

    If the stone is engraved with a number that has an even number
    of digits, it is replaced by two stones. The left half of the
    digits are engraved on the new left stone, and the right half
    of the digits are engraved on the new right stone. (The new
    numbers don't keep extra leading zeroes: 1000 would become
    stones 10 and 0.)

    If none of the other rules apply, the stone is replaced by a
    new stone; the old stone's number multiplied by 2024 is engraved
    on the new stone.
    """

    if stone == 0:
        return (1,)

    digits = str(stone)
    length = len(digits)
    if length % 2 == 0:
        return (int(digits[: length // 2]), int(digits[length // 2 :]))

    return (stone * 2024,)


stones = parse(aocd.data)

for i in range(25):
    print(i)
    stones = (*itertools.chain.from_iterable(blink(stone) for stone in stones),)

print(len(stones))


@functools.cache
def blink_remains(stones, splits):
    if splits == 0:
        return len(stones)
    return sum(blink_remains(blink(stone), splits - 1) for stone in stones)


begin = time.time_ns()
print(blink_remains(parse(aocd.data), 75))
end = time.time_ns()
print(f"75 blinks in {(end-begin)/1e9:.02f}s")


def blink_iterative(turns):
    stones = defaultdict(int)
    for stone in parse(aocd.data):
        stones[stone] += 1

    for i in range(turns):
        for stone, amount in list(stones.items()):
            stones[stone] -= amount
            for new_stone in blink(stone):
                stones[new_stone] += amount

    return sum(stones.values())

begin = time.time_ns()
print(blink_iterative(75))
end = time.time_ns()
print(f"75 non-recursive blinks in {(end-begin)/1e9:.02f}s")

print("Dict method %0.4f" % timeit.timeit('blink_iterative(75)', number=100, globals=globals()))
print("Memo method %0.4f" % timeit.timeit('blink_remains(parse(aocd.data), 75)', 'blink_remains.cache_clear()', number=100, globals=globals()))

