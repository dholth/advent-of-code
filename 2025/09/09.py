#!/usr/bin/env python
"""
Day 9: Movie Theater
"""

import math
import re
from pathlib import Path

import aocd

example = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""


def parse(data: str):
    for line in data.splitlines():
        yield tuple(int(n) for n in re.findall(r"\d+", line))


def rectangle(v0, v1):
    return tuple((abs(x0 - x1) + 1) for x0, x1 in zip(v0, v1))


def largest_pair(coords):
    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            yield (math.prod(rectangle(coords[i], coords[j])))


coords = list(parse(aocd.data))

print("Part 1", max(largest_pair(coords)))


def svg(coords):
    path = []
    for x, y in coords:
        path.append(f"L {x} {y}")
    template = f"""<svg width="98065" height="98065" xmlns="http://www.w3.org/2000/svg">
    <path d="{" ".join(path)} Z" fill="black" stroke="green" />
    </svg>"""
    return template

Path("debug.svg").write_text(svg(coords))

print(max(coords))
