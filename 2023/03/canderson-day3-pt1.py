#!/usr/bin/env python
"""--- Day 3: Gear Ratios ---
You and the Elf eventually reach a gondola lift station; he says the gondola
lift will take you up to the water source, but this is as far as he can bring
you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem:
they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of
surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working
right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine,
but nobody can figure out which one. If you can add up all the part numbers in
the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation
of the engine. There are lots of numbers and symbols you don't really
understand, but apparently any number adjacent to a symbol, even diagonally,
is a "part number" and should be included in your sum. (Periods (.) do not
count as a symbol.)

In this schematic, two numbers are not part numbers because they are not
adjacent to a symbol: 114 (top right) and 58 (middle right). Every other
number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all
of the part numbers in the engine schematic?
"""

from pathlib import Path

EX1 = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

EX2 = """
"""

DIGITS = "0,1,2,3,4,5,6,7,8,9".split(",")


def eat_digits(schematic, x, y):
    i = x
    if not schematic[y][i] in DIGITS:
        return
    while schematic[y][i] in DIGITS:
        schematic[y][i] = "Z"
        i += 1
        if i >= len(schematic[0]):
            break
    i = x - 1
    while schematic[y][i] in DIGITS:
        schematic[y][i] = "Z"
        i -= 1
        if i < 0:
            break


def scrub(schematic, x, y):
    # if schematic[y][x] == "#":
    #     breakpoint()
    schematic[y][x] = "S"
    for j in range(y - 1, y + 2):
        for i in range(x - 1, x + 2):
            eat_digits(schematic, i, j)


def show(schematic):
    for row in schematic:
        print("".join(row))


def get_numbers(schematic):
    numbers = []
    total = 0
    for row in schematic:
        line = "".join(row)
        n = [int(x) for x in line.split(".") if x]
        numbers.extend(n)
        total += sum(n)
    return total, numbers


def pt1(input):
    numbers = [list(line) for line in input.split("\n")]
    for y in range(len(numbers)):
        for x in range(len(numbers[y])):
            if numbers[y][x] not in DIGITS:
                numbers[y][x] = "."
    omitted = [list(line) for line in input.split("\n")]
    ignored = "0,1,2,3,4,5,6,7,8,9,.,Z,S".split(",")
    for y in range(len(omitted)):
        for x in range(len(omitted[y])):
            if omitted[y][x] not in ignored:
                scrub(omitted, x, y)
    for y in range(len(omitted)):
        for x in range(len(omitted[y])):
            if omitted[y][x] in DIGITS:
                numbers[y][x] = "0"
    show(omitted)
    print(get_numbers(numbers))


def pt2(input):
    print("TODO")


if __name__ == "__main__":
    with open(Path(__file__).parent / "input.txt") as fd:
        input = fd.read().strip()

    # pt1(EX1.strip())  # 172
    pt1(input)  # NOT: 554313, 496369, 494380, 419253, 419297, 338988, 303797
#    pt2(EX2.strip())  #
#    pt2(input)  #
