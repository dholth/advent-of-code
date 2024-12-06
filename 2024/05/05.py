#!/usr/bin/env python

import re
from itertools import groupby, takewhile

import aocd
from rich.console import Console

console = Console()

example = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""


def parse(data: str):
    idata = iter(list(map(int, re.findall(r"\d+", line))) for line in data.splitlines())
    while part := list(takewhile(bool, idata)):
        yield part


first_part, second_part = parse(aocd.data)

must_after = {}
must_before = {}
for a, b in first_part:
    must_after[a] = must_after.get(a, []) + [b]
    must_before[b] = must_before.get(b, []) + [a]


def follows_rules(pages: list[int]):
    for i in range(len(pages)):
        page = pages[i]
        after = set(pages[i + 1 :])
        before = set(pages[:i])

        if not (after.issubset(set(must_after.get(page, [])))) and (
            before.issubset(set(must_before.get(page, [])))
        ):
            return False
    return True


ans = 0
for pages in second_part:
    if follows_rules(pages):
        ans += pages[len(pages) // 2]


print("Part 1", ans)
print()


def insertion_point(pages, misfit: int):
    """
    Return list with misfit inserted, following rules.
    """
    for i in range(len(pages) + 1):
        after = pages[i:]
        before = pages[:i]

        test = before + [misfit] + after
        if follows_rules(test):
            return test

    return pages


def remove_misfits(pages):
    misfits = []
    okay = []
    for i in range(len(pages)):
        page = pages[i]
        after = set(pages[i + 1 :])
        before = set(pages[:i])

        if not (after.issubset(set(must_after.get(page, [])))) and (
            before.issubset(set(must_before.get(page, [])))
        ):
            misfits.append(page)
        else:
            okay.append(page)

    return okay, misfits


ans2 = 0
for pages in second_part:
    misfits = []
    okay = pages

    while True:
        okay, misfits_n = remove_misfits(okay)
        if not misfits_n:
            break
        misfits.extend(misfits_n)

    if misfits:
        print("broken", okay, misfits)
        print("okay?", follows_rules(okay))

        for m in misfits:
            okay = insertion_point(okay, m)

        print("fixed?", okay)
        ans2 += okay[len(okay) // 2]

    print()

print("Part 2", ans2)
