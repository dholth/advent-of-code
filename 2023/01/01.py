#!/usr/bin/env python

import sys

words = "one, two, three, four, five, six, seven, eight, nine".split(", ")
print(words)


def sums(inputs):
    for line in inputs:
        digis = "".join(x for x in line if x.isdigit())
        calibration = int(digis[0] + digis[-1])
        yield calibration


print(sum(sums(open("input.txt"))))


def overlappingwords(word):
    for i in range(len(word)):
        for j, num in enumerate(words, start=1):
            if word[i:].startswith(num):
                yield str(j)
                break
        else:
            yield word[i]


def part2(inputs):
    for line in inputs:
        original = line
        line = "".join(overlappingwords(line))
        yield line


print(sum(sums(part2(open("input.txt")))))
