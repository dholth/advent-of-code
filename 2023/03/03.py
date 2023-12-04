#!/usr/bin/env python
"""
Any (multi-digit) number adjacent to a symbol is a "part number" and should be
summed.
"""

import itertools
import pprint
import re
from pathlib import Path

from aocd import submit
from rich.console import Console

console = Console()

mode = 2

if mode == 0:
    INPUT = Path("input-google.txt")
elif mode == 1:
    INPUT = Path("input.txt")
else:
    INPUT = Path("sample.txt")

directions = [
    offset for offset in itertools.product((-1, 0, 1), (-1, 0, 1)) if offset != (0, 0)
]

print(directions)

board: dict[tuple, str] = {}

for i, line in enumerate(INPUT.open(), start=1):
    for j, char in enumerate(line.strip(), start=1):
        if char != ".":
            board[(i, j)] = char


pprint.pprint(board)

adjacent_to_symbol = set()

for coord, char in board.items():
    if not char.isdigit():
        # check diagonals
        print(f"Check neighbors of {coord}={char}")
        for i, j in directions:
            neighbor_coord = (coord[0] + i, coord[1] + j)
            neighbor = board.get(neighbor_coord)
            if not neighbor:
                continue
            adjacent_to_symbol.add(neighbor_coord)
            # print(neighbor)
    print()


print("Find numbers adjacent to symbols")
valid_numbers = []
invalid_numbers = []
valid_numbers_coords = set()

all_numbers_2 = []

for i, line in enumerate(INPUT.open(), start=1):
    current_number = []
    current_number_coords = set()
    for j, char in enumerate(line.strip() + ".", start=1):
        if char.isdigit():
            current_number.append(char)
            current_number_coords.add((i, j))
        else:
            joined_number = "".join(current_number)
            if current_number:
                all_numbers_2.append(int(joined_number))
            if current_number and not current_number_coords.isdisjoint(
                adjacent_to_symbol
            ):
                valid_numbers.append(int(joined_number))
                valid_numbers_coords.update(current_number_coords)
            elif current_number:
                invalid_numbers.append(int(joined_number))
            current_number = []
            current_number_coords = set()
    # console.print()


for i, line in enumerate(INPUT.open(), start=1):
    current_number = []
    current_number_coords = set()
    for j, char in enumerate(line.strip(), start=1):
        if (i, j) in valid_numbers_coords:
            console.print(f"[red]{char}", end="")
        elif char == "." or char.isdigit():
            console.print(f"[grey]{char}", end="")
        else:
            console.print(f"[blue]{char}", end="")
    console.print()

print()

# print("Places adjacent to symbol", adjacent_to_symbol)
print("Valid numbers", valid_numbers)
print("Ineligible numbers", invalid_numbers)
print("Answer", sum(valid_numbers))


all_numbers = [int(x) for x in re.findall(r"\d+", INPUT.read_text())]

print("All numbers", all_numbers)
print("All numbers minus invalid ones", sum(all_numbers) - sum(invalid_numbers))

Path("all_numbers.txt").write_text("\n".join(str(n) for n in all_numbers))
Path("all_numbers_2.txt").write_text("\n".join(str(n) for n in all_numbers_2))
