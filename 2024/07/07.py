#!/usr/bin/env python

import aocd
import re

example = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""


def parse(data: str):
    return (list(map(int, re.findall(r"\d+", line))) for line in data.splitlines())


def operate(car, cdr, part2=False):
    if cdr and car:
        yield from operate(car + cdr[0], cdr[1:], part2)
        yield from operate(car * cdr[0], cdr[1:], part2)
        if part2:
            yield from operate(int(f"{car}{cdr[0]}"), cdr[1:], part2)
    else:
        yield car


def combine(data: str, part2=False):
    for equation in parse(data):
        answer, *numbers = equation
        possible = operate(numbers[0], numbers[1:], part2=part2)
        yield answer * (any(answer == x for x in possible))


answer = sum(combine(aocd.data))
print(answer)

answer2 = sum(combine(aocd.data, True))
print(answer2)
