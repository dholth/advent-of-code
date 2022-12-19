#!/usr/bin/env python
from __future__ import annotations

from itertools import product
from dataclasses import dataclass

import aocd


example = """\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
""".splitlines()


@dataclass(order=True)
class Node:
    coord: tuple
    visited: bool = False
    anti: bool = False

    def __hash__(self):
        return hash(self.coord)


SIDES = [c for c in product(*[(-1, 0, 1)] * 3) if sum(map(abs, c)) == 1]


@dataclass
class Grid:
    nodes: set[Node]
    by_coord: dict[tuple, Node]

    def __init__(self, rows):
        self.by_coord = {}
        self.probes = {}
        for row in rows:
            node = Node(coord=(tuple(map(int, row.split(",")))))
            self.by_coord[node.coord] = node
            # self.nodes.add(node)

    def get(self, node: Node):
        return self.by_coord.get(node.coord)

    def add(self, node: Node):
        self.by_coord[node.coord] = node

    def neighbors(self, node: Node):
        """
        All neighbors for node.
        """
        for side in SIDES:
            next_coord = (*map(int.__add__, node.coord, side),)
            n = self.by_coord.get(next_coord)
            if n is None:
                self.probes[next_coord] = self.probes.get(next_coord, 0) + 1
            yield n

    def antineighbors(self, node: Node):
        """
        All neighbors for node (return coordinates if missing)
        """
        sides = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]
        for side in sides:
            next_coord = (*map(int.__add__, node.coord, side),)
            n = self.by_coord.get(next_coord)
            if n is None:
                yield next_coord
            yield n

    def surface_area(self):
        surface_area = 0
        self.probes = {}
        for node in self.by_coord.values():
            if node.anti:
                continue
            node.visited = True
            for n in self.neighbors(node):
                if n is None:
                    surface_area += 1
        return surface_area

    def surface_area_2(self):
        surface_area = 0
        self.probes = {}
        for node in self.by_coord.values():
            if node.anti:
                continue
            node.visited = True
            neighbors = list(self.neighbors(node))
            for n in neighbors:
                if n and n.anti:
                    surface_area += 1
        return surface_area

    def dim(self):
        big = [0, 0, 0]
        small = [0, 0, 0]
        for node in self.by_coord.values():
            big = [max(c, d) for c, d in zip(big, node.coord)]
            small = [min(c, d) for c, d in zip(small, node.coord)]

        return small, big


grid = Grid(aocd.data.splitlines())

print(f"{grid.surface_area()=}")
print(f"All sides", len(grid.by_coord) * 6)

grid = Grid(aocd.data.splitlines())
p1 = grid.surface_area()

print("Hot pockets!")
probes = dict(grid.probes)  # copy
# oh, maybe there are multiple air pockets
for p, c in probes.items():
    if c != 6:
        continue
    node = Node(p)
    print(p, all(n for n in grid.neighbors(node)))
    grid.add(node)

print("Surface area 2", grid.surface_area())

print("Hot pockets!")
probes = dict(grid.probes)  # copy
# oh, maybe there are multiple air pockets
for p, c in probes.items():
    if c != 6:
        continue
    node = Node(p)
    print(p, all(n for n in grid.neighbors(node)))
    grid.add(node)

# lower than 3254
print("Surface area 2b", grid.surface_area())

print("Dim", grid.dim())

grid = Grid(aocd.data.splitlines())


def show(grid):
    for z in range(-1, 21):
        for y in range(-1, 21):

            def as_char(n):
                if n:
                    return "-" if n.anti else "#"
                else:
                    return "."

            print("".join(as_char(grid.by_coord.get((x, y, z))) for x in range(-1, 21)))


# between 0,0,0 and 20, 20, 20
antinode = Node((0, 0, 0), anti=True)
grid.add(antinode)

show(grid)

frontier = [antinode]

while frontier:
    a = frontier.pop()
    for n in grid.antineighbors(a):
        if isinstance(n, tuple):
            if all((-1 <= c <= 20) for c in n):
                anti = Node(n, anti=True)
                frontier.append(anti)
                grid.add(anti)

show(grid)

after = grid.surface_area()
print(p1, after, p1 - after)

print(grid.surface_area_2())

with open("hollow.txt", "w") as hollow:
    for i, j, k in product(*[range(20)] * 3):
        if grid.by_coord.get((i, j, k)) is None:
            print(f"{i},{j},{k}", file=hollow)
