#!/usr/bin/env python

from pathlib import Path
import re

from aocd import submit

here = Path(__file__).parent
input = Path(here, "input.txt").read_text().splitlines()

sample = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""".splitlines()


def all_numbers(line):
    return [int(x) for x in re.findall(r"\d+", line)]


def numbers_from_line(line):
    not_card = line.partition(":")[-1]
    want, have = not_card.split("|")
    return all_numbers(want), all_numbers(have)


def allmatch(lines):
    for line in lines:
        winning, rest = numbers_from_line(line)
        winners = set(winning).intersection(set(rest))
        if winners:
            points = 2 ** (len(winners) - 1)
            yield points


print("Part 1")
print(sum(allmatch(sample)))

answer = sum(allmatch(input))
print(answer)

print("Part 2")


def cards_win_copies(sample):
    # extra past the end to avoid range checks
    repeat = [1] * len(sample) * 2
    for i, line in enumerate(sample):
        winning, rest = numbers_from_line(line)
        winners = set(winning).intersection(set(rest))
        for j in range(len(winners)):
            repeat[i + 1 + j] += repeat[i]
    return sum(repeat[0 : len(sample)])


print(cards_win_copies(input))
