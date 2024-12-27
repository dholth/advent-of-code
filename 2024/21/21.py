#!/usr/bin/env python
"""
Two layers of directional keypads control a robot typing on a numerical pad.
They all start on the "A" key. Show the sequence of motions required to input
codes.
"""

import heapq
import sys
import time
from dataclasses import dataclass
from typing import Iterable

import functools
import itertools
import aocd

numbers = """\
789
456
123
 0A
""".splitlines()

arrows = """\
 ^A
<v>
""".splitlines()

example = """\
029A
980A
179A
456A
379A
""".splitlines()

PRETTY = {}
PRETTY.update((chr(i), chr(0xFEE0 + i)) for i in range(ord("0"), ord("{")))
FILLER = "\N{FULLWIDTH FULL STOP}"

# 0,0 is top left; coordinates increase going right, and going down.
DIRECTIONS = {(-1, 0): "<", (1, 0): ">", (0, -1): "^", (0, 1): "v"}

# bottom keypad pathfinding to next keypad...
# graphs...
# problem segments...
# shortest options per segment ala day 10...
# paths between pairs given in example?
# annotate edges with directions?

# Were you to choose this sequence of button presses, here are all of the
# buttons that would be pressed on your directional keypad, the two robots'
# directional keypads, and the numeric keypad

# Your keypad
# Robot 3 directional keypad
# Robot 2 directional keypad
# Robot 1 numeric keypad


@dataclass(order=True)
class Node:
    coord: tuple = (0, 0)
    letter: str = ""
    visited: bool = False
    distance: int = sys.maxsize

    def __hash__(self):
        return hash(self.coord)

    def reset(self):
        self.visited = False
        self.distance = sys.maxsize


@dataclass
class Grid:
    nodes: frozenset[Node]
    array: list[list[Node]]
    start: Node
    end: Node
    prev: Node | None = None

    def __init__(self, rows):
        nodes = set()
        self.array = []

        def build(letter="", **args):
            node = Node(**args, letter=letter)
            if letter == "A":
                self.start = node
            nodes.add(node)
            return node

        self.array = [
            [build(coord=(x, y), letter=c) for (x, c) in enumerate(row)]
            for (y, row) in enumerate(rows)
        ]

        self.start.distance = 0

        self.nodes = frozenset(nodes)

    def __hash__(self):
        return hash(self.nodes)

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
                candidate = self.array[y + dy][x + dx]
                if candidate.letter == " ":
                    continue
                yield candidate, (dx, dy)
            except IndexError:
                pass

    def display(
        self,
        pending,
        pathset0: Iterable[tuple[int, int]] = (),
        pathset: Iterable[Node] = (),
    ):
        pathset0 = set(pathset0)
        pathset = set(pathset)
        pending = set(pending)
        print("\N{CHEESE WEDGE}")
        for row in self.array:
            for col in row:
                if col in pending:
                    char = "+"
                elif col.visited:
                    # print(" ", end="")
                    char = chr(ord("0") + col.distance % 10)
                else:
                    char = col.letter
                print(PRETTY.get(char, FILLER), end="")
            print()

    def shortest(self, start, goal, connected, show=False):
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

            if node == goal:
                break

            for next in connected(node):
                if not next.visited:
                    next.distance = min(node.distance + 1, next.distance)
                    heapq.heappush(unvisited, (next.distance, next))

    def _distinct_paths(self, start: Node, connected, goal: str, path: list):
        """
        Distinct paths to goal from start using 'connected' function to find neighbors.
        """
        # XXX will also need directions between them, or, come up with a lookup.
        if start.letter == goal:
            yield path
        for next, _ in connected(start):
            if next in path:
                continue
            yield from self._distinct_paths(next, connected, goal, path + [next])

    def paths_between(self, start: str, goal: str):
        begin = next(n for n in self.nodes if n.letter == start)
        yield from self._distinct_paths(begin, self.neighbors, goal, [begin])

    def shortest_paths_between(self, start: str, goal: str):
        all_paths_between = list(self.paths_between(start, goal))
        shortest = min(len(p) for p in all_paths_between)
        return [p for p in all_paths_between if len(p) == shortest]

    @functools.cache
    def direction_between(self, start: str, goal: str):
        """
        Return arrow direction between two adjacent characters on the pad.
        """
        begin = next(n for n in self.nodes if n.letter == start)
        for n, direction in self.neighbors(begin):
            if n.letter == goal:
                return direction
        raise ValueError("Not adjacent")

    def reset(self):
        for node in self.nodes:
            node.reset()


keypad = Grid(numbers)
keypad.display(())
print("\nPaths between A and 9:")
for path in keypad.paths_between("A", "9"):
    print(",".join(n.letter for n in path))

print(f"\nCode {example[0]}")
for a, b in zip(example[0], example[0][1:]):
    print(f"Shortest paths between {a} and {b}")
    for path in keypad.shortest_paths_between(a, b):
        print(",".join(n.letter for n in path))
    print()

example_path = "987412563A"
print(f"\nBetween {example_path}")
for a, b in zip(example_path, example_path[1:]):
    print(a, b)
    d = keypad.direction_between(a, b)
    print(d, DIRECTIONS[d])
