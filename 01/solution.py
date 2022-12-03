#!/usr/bin/env python
from pathlib import Path


def go():
    elves = []
    elf = []
    for line in Path("01/input").open():
        try:
            elf.append(int(line))
        except ValueError:
            elves.append(elf)
            elf = []
    print(elves)
    print("greatest sum", max(sum(elf) for elf in elves))
    elfsum = sorted(sum(elf) for elf in elves)
    print("sum of greatest 3", sum(elfsum[-3:]))


if __name__ == "__main__":
    go()
