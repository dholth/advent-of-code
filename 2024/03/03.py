#!/usr/bin/env python

import operator
import re

import aocd

example = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
dodont = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

VALID = re.compile(r"mul\(\d+,\d+\)", re.UNICODE)
VALID_DODONT = re.compile(VALID.pattern + r"|do\(\)|don't\(\)")


def uncorrupt(data):
    answer = 0
    for expr in VALID.findall(data):
        print(expr)
        term = operator.mul(*map(int, re.findall(r"\d+", expr)))
        print(term)
        answer += term
    return answer


def part2(data):
    answer = 0
    do = True
    for expr in VALID_DODONT.findall(data):
        if expr == "do()":
            do = True
        elif expr == "don't()":
            do = False
        else:
            term = operator.mul(*map(int, re.findall("\d+", expr)))
            answer += do * term
    return answer


if __name__ == "__main__":
    print(uncorrupt(example))
    print(VALID_DODONT.findall(dodont))
    print(part2(aocd.data))
