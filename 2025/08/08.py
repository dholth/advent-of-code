#!/usr/bin/env python
"""
Day 8: Playground.
"""

import pprint
import re
from dataclasses import dataclass
from functools import reduce
from operator import mul

import aocd

# Connect pairs of 3d-coordinates that are closest together and
# not already directly connected.

# distance = √((x2-x1)²+(y2-y1)²+(z2-z1)²

@dataclass
class vector:
    x: int
    y: int
    z: int

def d_squared(a: tuple[int, ...], b: tuple[int, ...]):
    """
    Return square of the distance between a, b.
    """
    return sum((x0-x1)**2 for x0, x1 in zip(a, b))

example = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""

def parse(data: str):
    for line in data.splitlines():
        yield tuple(int(n) for n in re.findall(r"\d+", line))

coords = list(parse(example))

def part_1(coords, pairs=1001):
    # all distances betwee n, m but not all distances between m, n
    # stored as squared distance
    distances: dict[tuple[int, int], int] = {}
    for n in range(len(coords)):
        for m in range(n+1, len(coords)):
            distances[(n,m)] = d_squared(coords[n], coords[m])

    # all distances unique?
    assert len(set(distances.values())) == len(distances)

    closest_first = sorted((v, k) for k, v in distances.items())

    # circuits
    # assign coordinate indices to a circuit
    # if any of the indices are already in a circuit, that's the number;
    # else, a new number. or use sets.
    circuits: list[set[int]] = []
    for distance, (v0, v1) in closest_first[:pairs]: # off by one or just wrong?
        print(distance, v0, v1, coords[v0], coords[v1])
        for circuit in circuits:
            # doesn't account for circuits that are connected together
            if v0 in circuit or v1 in circuit:
                circuit.add(v0)
                circuit.add(v1)
                break
        else:
            circuits.append(set((v0, v1)))

    top_3 = sorted(len(circuit) for circuit in circuits)[-3:]
    print(top_3)
    pprint.pprint(circuits)
    return reduce(mul, top_3)

assert part_1(coords, 10) == 40

# aocd.submit(part_1(list(parse(aocd.data)), 1001))
