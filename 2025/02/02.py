#!/usr/bin/env python
import re

import aocd

data = aocd.data

ranges = list(re.findall(r"(\d+)-(\d+)", data))
# print(ranges)


def print_ranges(ranges):
    for a, b in ranges:
        print(
            len(a),
            len(b),
            int(b) - int(a),
            a,
            a[: -len(a) // 2],
            a[len(a) // 2 :],
            b,
            b[: -len(b) // 2],
            b[len(b) // 2 :],
        )


def brute_a(ranges: list[tuple[str, str]]):
    for start, end in ranges:
        print(start, end)
        for i in range(int(start), int(end) + 1):
            a = str(i)
            if a[: -len(a) // 2] == a[len(a) // 2 :]:
                yield i


print(sum(brute_a(ranges)))


def split_all_ways(s):
    len_s = len(s)
    for i in range(1, len_s // 2 + 1):
        print(i)
        print(len_s, i)
        if len_s % i == 0:
            group = []
            for j in range(len_s // i):
                group.append(s[j * i : j * i + i])
            yield group


def repeating_sequence(s):
    """
    Return True if any evenly-divisible number of characters in "s" repeats
    through the whole string.
    """
    len_s = len(s)
    # not faster forwards or backwards
    for i in range(1, len_s // 2 + 1):
        if len_s % i == 0:
            group = []
            for j in range(len_s // i):
                group.append(s[j * i : j * i + i])
            if all(group[0] == n for n in group[1:]):
                return True
    return False


print(repeating_sequence("jimmyjimmy"))


def brute_b(ranges: list[tuple[str, str]]):
    for start, end in ranges:
        print(start, end)
        for i in range(int(start), int(end) + 1):
            a = str(i)
            if repeating_sequence(a):
                yield i


print(sum(brute_b(ranges)))

print("How many?", len(list(brute_b(ranges))))
