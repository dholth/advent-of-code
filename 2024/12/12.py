#!/usr/bin/env python

import heapq
import pathlib
import sys
import time
from dataclasses import dataclass
from itertools import cycle

import aocd
import shapely

DEBUG = False

PRETTY = {}
PRETTY.update((chr(i), chr(0xFEE0 + i)) for i in range(ord("0"), ord("{")))


def height(letter):
    return ord(letter) - ord("A")


@dataclass(order=True)
class Node:
    distance: int = sys.maxsize
    coord: tuple = (0, 0)
    height: int = 0
    visited: bool = False
    letter: str = ""

    def __hash__(self):
        return hash(self.coord)

    def reset(self):
        self.visited = False
        self.distance = sys.maxsize


@dataclass
class Grid:
    nodes: set[Node]
    array: list[list[Node]]
    start: Node
    end: Node
    prev: Node | None = None

    def __init__(self, rows):
        self.nodes = set()
        self.array = []

        def build(letter="", **args):
            node = Node(**args, letter=letter)
            self.nodes.add(node)
            return node

        self.array = [
            [
                build(coord=(x, y), height=height(c), letter=c)
                for (x, c) in enumerate(row)
            ]
            for (y, row) in enumerate(rows)
        ]

    def neighbors(self, node: Node):
        """
        All neighbors for node.
        """
        x, y = node.coord
        for dx, dy in (-1, 0), (1, 0), (0, -1), (0, 1):
            nx, ny = x + dx, y + dy
            if nx < 0 or ny < 0:
                continue
            try:
                yield self.array[y + dy][x + dx]
            except IndexError:
                pass

    def same_letter(self, node: Node):
        for n in self.neighbors(node):
            if n.letter == node.letter:
                yield n

    def display(
        self,
        highlight,
    ):
        highlight = set(highlight)
        print("\N{RED APPLE}")
        for row in self.array:
            for col in row:
                if col in highlight:
                    char = "\N{GLOWING STAR}"
                else:
                    char = col.letter
                print(PRETTY.get(char, char), end="")
            print()

    def flood(self, start, connected, show=False):
        display_distance = 0
        unvisited = [(start.distance, start)]
        while unvisited:
            original_priority, node = heapq.heappop(unvisited)
            if original_priority != node.distance:
                continue
            if node.visited:
                continue
            if display_distance < node.distance:
                display_distance = node.distance
                if show:
                    print("\033[2J\033[H")  # clear screen and move to home
                    self.display(n for _, n in unvisited)
                    sys.stdout.flush()

                    time.sleep(0.01)

            node.visited = True

            for next in connected(node):
                if not next.visited:
                    next.distance = min(node.distance + 1, next.distance)
                    heapq.heappush(unvisited, (next.distance, next))

    def reset(self):
        for node in self.nodes:
            node.reset()


example = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
""".splitlines()


def is_corner(point1, point2, point3):
    # if point 2 is a corner
    x0, y0 = point1
    x1, y1 = point2
    x2, y2 = point3

    return abs(x0 - x2) == 1 and abs(y0 - y2) == 1


def count_sides(points, letter=None, number=None):
    points = list(points)[:-1]
    # print("sides p", points)
    p0 = cycle(points)
    p1 = cycle(points)
    p2 = cycle(points)

    next(p1)

    next(p2)
    next(p2)

    corners = []
    for a, b, c in zip(p0, p1, p2):
        if is_corner(a, b, c):
            if b in corners:
                break
            corners.append(b)

    if letter and DEBUG:
        pathlib.Path(f"corners-{number}-{letter}.svg").write_text(
            shapely.Polygon(corners)._repr_svg_()
        )

    return corners


def fence_costs(data: list[str], show=False):
    grid = Grid(data)
    grid.end = next(n for n in grid.nodes)  # not needed for this puzzle

    all_regions = set()
    regions = []
    region_number = 0
    for n in grid.nodes:
        if n in all_regions:
            continue

        grid.start = n
        grid.start.distance = 0

        grid.flood(grid.start, connected=grid.same_letter)

        regions.append({n for n in grid.nodes if n.visited})
        all_regions.update(regions[-1])

        if show:
            grid.display(regions[-1])
            print("Region", region_number)

        grid.reset()

        region_number += 1

    # Compute score
    print(f"{len(regions)} regions")
    score = 0
    score2 = 0
    for i, region in enumerate(regions):
        area = len(region)
        perimeter = 0

        polygons = []
        for node in region:
            x, y = node.coord
            polygon = shapely.Polygon(((x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)))
            polygons.append(polygon)
            perimeter += 4 - len(list(grid.same_letter(node)))

        polys = shapely.GeometryCollection(polygons)
        p2: shapely.Polygon = shapely.union_all(polys)  # type: ignore

        if DEBUG:
            print(
                f"{i} {node.letter} Old score {area * perimeter:4d}",
                f"\ta={area} boundary coords={len(count_sides(p2.exterior.coords))}",
            )

            pathlib.Path(f"{i}-{node.letter}.svg").write_text(p2._repr_svg_())

        score += area * perimeter
        score2 += len(count_sides(p2.exterior.coords, node.letter, i)) * area
        for interior in p2.interiors:
            score2 += len(count_sides(interior.coords, node.letter, i)) * area

    return score, score2


print("Example")
print("Part 1, 2", fence_costs(example, show=True))

## Part 2

# Find number of sides of region * area for all

example_sides = [
    (4.0, 1.0),
    (4.0, 2.0),
    (5.0, 2.0),
    (6.0, 2.0),
    (6.0, 1.0),
    (6.0, 0.0),
    (5.0, 0.0),
    (4.0, 0.0),
    (4.0, 1.0),
]

assert len(count_sides(example_sides)) == 4

print("Full")
print("Part 1, 2", fence_costs(aocd.data.splitlines()))
