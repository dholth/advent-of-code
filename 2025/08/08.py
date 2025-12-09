#!/usr/bin/env python
"""
Day 8: Playground.
"""

import math
import re
from collections import defaultdict

import aocd

# Connect pairs of 3d-coordinates that are closest together and
# not already directly connected.

# distance = √((x2-x1)²+(y2-y1)²+(z2-z1)²


def d_squared(a: tuple[int, ...], b: tuple[int, ...]):
    """
    Return square of the distance between a, b.
    """
    return sum((x0 - x1) ** 2 for x0, x1 in zip(a, b))


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


def part_2(coords):
    """
    yield connections, v0, v1 (indexes into coords)
    """
    # all distances betwee n, m but not all distances between m, n
    # stored as squared distance
    distances: dict[tuple[int, int], int] = {}
    for n in range(len(coords)):
        for m in range(n + 1, len(coords)):
            distances[(n, m)] = d_squared(coords[n], coords[m])

    # all distances unique?
    assert len(set(distances.values())) == len(distances)

    closest_first = sorted((v, k) for k, v in distances.items())

    # map node to outgoing nodes
    connections = defaultdict(set)

    for distance, (v0, v1) in closest_first:
        #       print(distance, v0, v1, coords[v0], coords[v1])
        connections[v0].add(v1)
        connections[v1].add(v0)

        yield connections, v0, v1


def part_1(coords, pairs=1000):
    for i, (connections, *_) in enumerate(part_2(coords)):
        if i == pairs:
            return connections


connections = part_1(coords, 10)


def assign_clique(connections: dict[int, set[int]], v0, clique: set[int]):
    """
    Recursively add elements to clique if not in clique.
    """
    if v0 in clique:
        return
    clique.add(v0)
    for v1 in connections[v0]:
        assign_clique(connections, v1, clique)
    return clique


def circuits(connections):
    # now call it, add to "big set of visited things", and keep going.
    visited = set()
    for v0 in connections:
        if v0 in visited:
            continue
        circuit = assign_clique(connections, v0, set())
        yield len(circuit)
        visited.update(circuit)


coords2 = list(parse(aocd.data))
connections = part_1(coords2, 1000)
print("Part 1", math.prod(sorted(circuits(connections))[-3:]))

# Now keep going until there is one circuit


for i, (connections, v0, v1) in enumerate(part_2(coords2)):
    cc = list(circuits(connections))
    # print(i, len(cc))
    if len(cc) == 1 and cc[0] == len(coords2):
        print("Part 2", coords2[v0][0] * coords2[v1][0])
        break
