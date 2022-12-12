#!/usr/bin/env python

import math
import pprint
from dataclasses import dataclass
from itertools import chain
from typing import Callable, Iterator

import aocd

example = """\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
""".splitlines()


@dataclass
class Monkey:
    items: list[int]
    op: Callable[[int], int]
    test: Callable[[int], int]
    modulo: int
    activity: int = 0

    def __init__(self, lines: Iterator[str]):
        assert next(lines).startswith("Monkey")
        self.items = list(map(int, next(lines).split(":")[-1].split(",")))

        operation = next(lines).split("=")[-1]

        def op(old):
            return eval(operation)

        self.op = op

        modulo = int(next(lines).rsplit(" ", 1)[-1])
        self.modulo = modulo
        monkey_true = int(next(lines).split("monkey")[-1])
        monkey_false = int(next(lines).split("monkey")[-1])

        def test(item):
            return monkey_true if item % modulo == 0 else monkey_false

        self.test = test


Monkey.__name__ = "\N{MONKEY}"

lines = iter(example)


def parse(lines):
    print("\N{BANANA}")
    lines = iter(lines)
    for line in lines:
        if not line:
            continue
        # monkey does not consume whole iterable
        yield Monkey(chain((line,), lines))


monkeys = list(parse(example))


def round(monkeys, divide=3, modulo=0, show=False):
    for monkey in monkeys:
        items = [monkey.op(item) // divide for item in monkey.items]
        if modulo:
            items = [item % modulo for item in items]
        monkey.activity += len(items)
        monkey.items = []
        for item in items:
            n = monkey.test(item)
            monkeys[n].items.append(item)
        if show:
            print("\N{MONKEY}")
            pprint.pprint(monkeys)


round(monkeys, show=True)
assert monkeys[0].items == [20, 23, 27, 26], monkeys[0].items
assert monkeys[1].items == [2080, 25, 167, 207, 401, 1046]


for i in range(19):
    round(monkeys)

print("\N{MONKEY}")
pprint.pprint(monkeys)


monkeys = list(parse(aocd.lines))
for i in range(20):
    round(monkeys)

print("\N{MONKEY}")
pprint.pprint(monkeys)

monkeys.sort(key=lambda m: m.activity)

part1 = monkeys[-1].activity * monkeys[-2].activity

print(f"\N{MONKEY}\N{OFFICE BUILDING} {part1}")


monkeys = list(parse(aocd.lines))

modulo = int(math.prod(monkey.modulo for monkey in monkeys))
for i in range(10000):
    round(monkeys, divide=1, modulo=modulo)

pprint.pprint(monkeys)

monkeys.sort(key=lambda m: m.activity)

part2 = monkeys[-1].activity * monkeys[-2].activity

print(f"\N{MONKEY}\N{OFFICE BUILDING} {part2}")
