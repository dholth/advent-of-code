#!/usr/bin/env python

import heapq
import sys
import time
from dataclasses import dataclass
from typing import Any, Generator, Iterable

import aocd

sys.setrecursionlimit(10000)

PRETTY = {
    ".": "\N{FULLWIDTH FULL STOP}",
    "#": "🧱",
    "S": "\N{DEER}",
    "E": "\N{PANCAKES}",
}

example = """\
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""

HORIZONTAL = 0
VERTICAL = 1


@dataclass(order=True)
class Node:
    distance: int = sys.maxsize
    coord: tuple = (0, 0, 0)
    visited: bool = False
    letter: str = ""

    def __hash__(self):
        return hash(self.coord)

    def reset(self):
        self.visited = False
        self.distance = sys.maxsize


@dataclass
class Grid:
    nodes: dict[tuple, Node]
    array: list[list[Node]]
    start: Node
    end: Node
    prev: Node | None = None

    def __init__(self, rows):
        self.nodes = {}
        self.array = []

        def build(coord=(), letter="", **args):
            horizontal = Node(coord=coord + (HORIZONTAL,), **args, letter=letter)
            vertical = Node(coord=coord + (VERTICAL,), **args, letter=letter)
            if letter != "#":
                self.nodes[horizontal.coord] = horizontal
                self.nodes[vertical.coord] = vertical
            if letter == "S":
                self.start = horizontal  # facing East
            elif letter == "E":
                self.end = horizontal  # or vertical
            return horizontal

        self.array = [
            [build(coord=(x, y), letter=c) for (x, c) in enumerate(row)]
            for (y, row) in enumerate(rows)
        ]

        self.start.distance = 0

    def neighbors(self, node: Node):
        """
        All neighbors for node.
        """
        x, y, z = node.coord
        for dx, dy, dz in (
            (-1, 0, 0),
            (1, 0, 0),
            (0, -1, 0),
            (0, 1, 0),
            (0, 0, -1),
            (0, 0, 1),
        ):
            nx, ny, nz = x + dx, y + dy, z + dz
            if (nx, ny, nz) in self.nodes:
                yield self.nodes[(nx, ny, nz)]

    def outgoing(self, node: Node):
        """
        All nodes that can be reached by this node.

        Plus cost.
        """
        # or a difference in X coordinates
        horizontal = node.coord[-1] == HORIZONTAL
        for n in self.neighbors(node):
            if horizontal and n.coord[1] != node.coord[1]:
                continue
            if not horizontal and n.coord[0] != node.coord[0]:
                continue

            if n.letter in ".SE":
                cost = 1 if n.coord[-1] == node.coord[-1] else 1000
                if n.letter == "E" and node.letter == "E":
                    cost = 0
                yield n, cost

    def outgoing_down_only(self, node: Node):
        for n, cost in self.outgoing(node):
            if n.distance > node.distance:
                yield n

    def display(
        self,
        pending,
        pathset0: Iterable[tuple[int, int]] = (),
        pathset: Iterable[Node] = (),
    ):
        pathset0 = set(pathset0)
        pathset = set(pathset)
        pending = set(pending)
        print("\N{MOUNTAIN}")
        for row in self.array:
            for col in row:
                print(PRETTY.get(col.letter), end="")
            print()

    def shortest(
        self,
        start,
        goal,
        connected: Generator[tuple[Node, int], Any, None],
        show=False,
    ):
        # nodes.visited and nodes.distance should be reset before calling
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

            # Find distance for all
            # if node == self.end:
            #     break

            for next, cost in connected(node):
                if not next.visited:
                    next.distance = min(node.distance + cost, next.distance)
                    heapq.heappush(unvisited, (next.distance, next))

    def distinct_paths(self, start: Node, connected):
        """
        Distinct paths to "9" from start using 'connected' function to find neighbors.
        """
        if start.letter == "E":
            return 1
        paths = sum(self.distinct_paths(next, connected) for next in connected(start))
        if paths > 0:
            start.in_path = True
        return paths

    def reset(self):
        for node in self.nodes.values():
            node.reset()


def part1(data: list[str]):
    grid = Grid(data)
    grid.display(set())
    print(grid.start, grid.end)

    grid.shortest(grid.start, grid.end, grid.outgoing)

    grid.display(set())

    print(grid.end.distance)

    return grid.end.distance


print("Part 1", part1(example.splitlines()))

## For part 2, find all of the shortest paths through the maze.

# Should be able to go downwards in distance along all the nodes


def part2(data):
    grid = Grid(data.splitlines())
    grid.display(set())
    print(grid.start, grid.end)

    grid.shortest(grid.start, grid.end, grid.outgoing)

    grid.display(set())

    print(grid.distinct_paths(grid.start, grid.outgoing_down_only))

    return 1 + len(
        set(n.coord[:2] for n in grid.nodes.values() if hasattr(n, "in_path"))
    )


print("Nodes in best paths (example)", part2(example))
print("Nodes in best paths", part2(aocd.data))
