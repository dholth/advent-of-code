#!/usr/bin/env python

import bisect
import re
import sys

import aocd

data = aocd.get_data(day=2, year=2025)

ranges = list(re.findall(r"(\d+)-(\d+)", data))
print("Longest number", max(len(num) for num in re.findall(r"\d+", data)))

# generate all repeating numbers less than or equal to 10 (or n) digits long


def repeatsies(length):
    for i in range(length // 2):
        repeating_digits = i + 1
        # print(f"{digits} sub-digits")
        if length % repeating_digits == 0:
            for j in range(10**i, (10 ** (i + 1))):
                yield (str(j) * (length // repeating_digits))


invalid_elf_ids = []
for digits in range(2, 11):
    repeatable = list(repeatsies(digits))
    # for example, 11 11 (pairs) is also 1 1 1 1 (four singles)
    print("Digits", digits, "r", len(repeatable), "set(r)", len(set(repeatable)))
    invalid_elf_ids.extend(repeatable)

print(f"{len(invalid_elf_ids)} invalid id's <= 10 digits long")

invalid_elf_ids = sorted(set(int(id) for id in invalid_elf_ids))

print(f"{len(invalid_elf_ids)} unique invalid id's <= 10 digits long")

RANGE_BEGIN = True
RANGE_END = False

# Convert ranges into bisectable array. They don't overlap in this (day 2) problem.
flat_ranges = (
    [(int(r[0]), RANGE_BEGIN) for r in ranges]
    + [(int(r[1]), RANGE_END) for r in ranges]
    + [
        (0, False),
        (sys.maxsize, True),
    ]  # plus a range that "ended" after 0 and another that "began" after a very large number
)
flat_ranges.sort()

results = {True: 0, False: 0}
ans = 0
for elf_id in invalid_elf_ids:
    insert_point = bisect.bisect(flat_ranges, (elf_id - 0.5, True))
    try:
        nearby_range_boundary = flat_ranges[insert_point]
        results[nearby_range_boundary[1]] += 1
        if nearby_range_boundary[1] is RANGE_END:
            ans += int(elf_id)
    except IndexError:
        pass  # at end of all possible ranges?

print(results)
print(ans)
assert ans == 50857215650  # my correct answer from the slow method
