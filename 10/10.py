#!/usr/bin/env python
import pathlib
import sys

# add ornaments to path
sys.path.append(str(pathlib.Path(__file__).parents[1]))

from typing import Iterator
import aocd
import random
import heapq
import dataclasses
import ornaments
import random

example0 = """\
noop
addx 3
addx -5
""".splitlines()

example = """\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop""".splitlines()


@dataclasses.dataclass
class Instruction:
    name: str
    arg: int
    cycles: int = 1

    def __init__(self, name, arg):
        self.name = name
        self.arg = arg

    def __call__(self, x) -> int:
        return self.op(x)

    def op(self, x):
        return x


class AddX(Instruction):
    cycles = 2

    def op(self, x):
        return x + self.arg


@dataclasses.dataclass(order=True)
class InPipeline:
    retires: int  # cycle executed
    pc: int  # cycle added
    instruction: Instruction


instructions = {"noop": Instruction, "addx": AddX}


def parse(lines) -> Iterator[Instruction]:
    for line in lines:
        name, *args = line.split()
        yield instructions[name](name, *([int(a) for a in args] or (None,)))


def execute(lines):

    heap: list[InPipeline] = []

    retires = 0
    for pc, inst in enumerate(parse(lines)):
        retires += inst.cycles
        heapq.heappush(heap, InPipeline(retires, pc, inst))

    cycle = 1
    x = 1

    for cycle in range(1, 1000):
        yield (cycle, x)
        while heap and heap[0].retires == cycle:
            inst = heapq.heappop(heap)
            # print(inst)
            x = inst.instruction(x)
        if not heap:
            yield (cycle + 1, x)
            break


execute(example0)
print("〜", random.choice(ornaments.ornaments)[0])
execute(example)

result = list(execute(example))

print(result[19::40])

result = list(execute(aocd.lines))

ans = sum((a * b) for a, b in result[19::40])

print("Part 1", ans)

print("〜", random.choice(ornaments.ornaments)[0])

for i in range(0, len(result), 40):
    row = result[i : i + 40]
    for i, (clock, value) in enumerate(row, 0):
        if i - 1 <= value <= i + 1:
            print("\N{CHRISTMAS TREE}", end="")
        else:
            print("\N{FULLWIDTH FULL STOP}", end="")
    print()
