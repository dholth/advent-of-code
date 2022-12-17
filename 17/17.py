#!/usr/bin/env python
from __future__ import annotations

import contextlib
import itertools
from itertools import groupby

import aocd
import time

from aocd.models import Puzzle


@contextlib.contextmanager
def timeme(message=""):
    start = time.time()
    yield
    end = time.time()
    print(f"{message} {end - start:0.2f}s")


example = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

r_text = """\
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"""

ROCK = "💎"
BORDER = "🌴"

rocks = [[*g] for k, g in groupby(r_text.splitlines(), bool) if k]

rocks2 = []
for rock in rocks:
    r = {}
    for j in range(len(rock)):
        for i in range(len(rock[0])):
            # negative j so bottom of rock is 0
            if rock[-j - 1][i] == "#":
                r[i - j * 1j] = ROCK
    rocks2.append(r)


def display(grid):
    x0, y0, x1, y1 = 0, 0, 0, 0
    for k in grid:
        x0 = min(x0, k.real)
        x1 = max(x1, k.real)
        y0 = min(y0, k.imag)
        y1 = max(y1, k.imag)
    x0, x1, y0, y1 = map(int, (x0, x1, y0, y1))
    for y in range(y0, y1 + 1):
        print(
            "".join(
                grid.get(x + y * 1j, "\N{FULLWIDTH FULL STOP}")
                for x in range(x0, x1 + 1)
            )
        )


for r in rocks2:
    display(r)
    print()

# this must start repeating including on stackability
def pile(jets, limit=2022):
    jets = itertools.cycle(enumerate(jets))
    rocks = itertools.cycle(rocks2)

    tower = {i: BORDER for i in range(7)}

    highest = min(k.imag for k in tower) * 1j

    pattern = set()
    PERMANENT_MARK = None
    extra_height = 0
    cheat = 0  # steps

    for step, rock in enumerate(rocks, 1):
        offset = 2 + highest - 4j  # 3 blank rows

        newrock = {k + offset: v for k, v in rock.items()}

        def buffet():
            nonlocal newrock, highest

            # across
            ji, jet = next(jets)
            jet = {"<": -1, ">": +1}[jet]
            mayberock = {k + jet: v for k, v in newrock.items()}
            for k in mayberock:
                if tower.get(k) or k.real < 0 or k.real >= 7:
                    break
            else:
                newrock = mayberock

            # down
            mayberock = {k + 1j: v for k, v in newrock.items()}
            for k in mayberock:
                if tower.get(k) or k.real < 0 or k.real >= 7:
                    return ji
            else:
                newrock = mayberock

            return None

        for i in range(1024):
            ji = buffet()
            if ji is not None:
                break
        else:
            print("Too many buffets!")

        tower.update(newrock)

        highest = min(highest.imag, min(k.imag for k in newrock)) * 1j

        mark = (step % len(rocks2), ji)
        if not PERMANENT_MARK:
            if mark in pattern:
                print(f"step:{step} mark:{mark} h:{highest}")
                PERMANENT_MARK = mark
                last_mark_step = step
                last_height = highest
            pattern.add(mark)

        elif mark == PERMANENT_MARK:
            print(f"step:{step} delta:{step-last_mark_step} mark:{mark} h:{highest}")
            steps_per_cycle = step - last_mark_step
            last_mark_step = step
            height_per_cycle = -int(highest.imag - last_height.imag)
            last_height = highest
            print(height_per_cycle)

            if steps_per_cycle:  # not set soon enough
                skip_cycles = (limit - step) // steps_per_cycle
                extra_height = height_per_cycle * skip_cycles
                cheat = skip_cycles * steps_per_cycle

        if step >= (limit - cheat):
            height = -int(highest.imag)
            print("Height", height)
            print("Height + extra", height + extra_height)
            display(tower)
            break

        # how devious are they
        if step % 10000 == 0:
            byebye = set()
            for k in tower:
                if k.imag > highest.imag + 100:
                    byebye.add(k)
            for k in byebye:
                del tower[k]

        if step % 11017 == 0:
            print("At step %d, %0.2f%%" % (step, (step / limit) * 100))


puzzle = Puzzle(2022, 17)

print("Pile 'em high")
pile(puzzle.input_data)
print("END")

pile(puzzle.input_data, limit=1000000000000)
