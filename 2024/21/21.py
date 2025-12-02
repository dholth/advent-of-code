#!/usr/bin/env python
"""
Two layers of directional keypads control a robot typing on a numerical pad.
They all start on the "A" key. Show the sequence of motions required to input
codes.
"""

import functools
import itertools
import sys
from dataclasses import dataclass
from typing import Iterable

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

# may be A029A "starts at A"
example = """\
029A
980A
179A
456A
379A
""".splitlines()

PRETTY = {}
PRETTY.update((chr(i), chr(0xFEE0 + i)) for i in range(ord("0"), ord("{")))
PRETTY.update({"v": "👇", ">": "👉", "^": "👆", "<": "👈"})
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

    def __str__(self):
        return f"{self.__class__.__name__}({self.letter})"


class NodeList(list):
    def __str__(self):
        return ",".join(el.letter for el in self)


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
        pending=(),
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

    def distinct_paths(self, start: Node, connected, goal: str, path: list):
        """
        Distinct paths to goal from start using 'connected' function to find neighbors.
        """
        if start.letter == goal:
            yield path
        for next, _ in connected(start):
            if next in path:
                continue
            yield from self.distinct_paths(next, connected, goal, path + [next])

    def paths_between(self, start: str, goal: str):
        """
        Distinct paths, easy version using letters not Node()
        """
        begin = next(n for n in self.nodes if n.letter == start)
        yield from self.distinct_paths(begin, self.neighbors, goal, [begin])

    def shortest_paths_between(self, start: str, goal: str):
        # TODO rank by minimum exploded * 2 length
        # OR favor consecutive same-button presses
        all_paths_between = list(self.paths_between(start, goal))
        shortest = min(len(p) for p in all_paths_between)
        return [NodeList(p) for p in all_paths_between if len(p) == shortest]

    @functools.cache
    def direction_between(self, start: str, goal: str):
        """
        Return arrow direction between two adjacent characters on the pad.
        """
        if isinstance(start, Node):
            start = start.letter
        if isinstance(goal, Node):
            goal = goal.letter
        begin = next(n for n in self.nodes if n.letter == start)
        for n, direction in self.neighbors(begin):
            if n.letter == goal:
                return direction
        raise ValueError(f"{start},{goal} not adjacent")

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


example_sequences = """\
029A: <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
980A: <v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A
179A: <v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
456A: <v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A
379A: <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
"""

"""
The complexity of a single code (like 029A) is equal to the result of multiplying these two values:

    The length of the shortest sequence of button presses you need to type on your directional keypad in order to cause the code to be typed on the numeric keypad; for 029A, this would be 68.
    The numeric part of the code (ignoring leading zeroes); for 029A, this would be 29.
"""

arrowpad = Grid(arrows)


# Need to enumerate every explode * 2 path between each pair of symbols on
# numeric keypad
def explode(code, keypad: Grid):
    """
    Arrow instructions for keypad entry of code
    """
    exploded = []
    for a, b in itertools.pairwise(code):
        shortest2 = []
        for shortest in keypad.shortest_paths_between(a, b):
            # may need to go deeper
            shortest2.append([])
            for c, d in zip(shortest, shortest[1:]):
                d = keypad.direction_between(c, d)
                shortest2[-1].append(DIRECTIONS[d])
            min_length = min(len(s2) for s2 in shortest2)
        exploded.extend(next(s2 for s2 in shortest2 if len(s2) == min_length))
        exploded.append("A")
    return "".join(exploded).replace("<v<A", "v<<A")


def explodeN(start, next, keypads):
    paths = keypad.paths_between(start, next[0])
    for path in paths:
        for c, d in zip(path, path[1:]):
            pass


def distinct_paths(self, start: Node, connected, goal: str, path: list):
    """
    Distinct paths to goal from start using 'connected' function to find neighbors.
    """
    if start.letter == goal:
        yield path
    for next, _ in connected(start):
        if next in path:
            continue
        yield from self.distinct_paths(next, connected, goal, path + [next])


def part1(codes: list[str]):
    total = 0
    for i in range(len(codes)):
        # to start at A
        code0 = "A" + codes[i]

        print("Type", code0)
        explode0 = explode(code0, keypad)
        # A to 1 avoiding empty space
        explode0 = explode0.replace("<^<A", "^<<A")
        explode0 = explode0.replace("<^<^A", "^^<<A")
        # the shortest path on explode0 may not be the shortest path on explode1
        # unfortunately (or is it only between 1 and 2)
        explode1 = explode("A" + explode0, arrowpad)
        explode2 = explode("A" + explode1, arrowpad)
        print(len(explode0), explode0)
        print(len(explode1), explode1)
        print(len(explode2), explode2)

        code = int(codes[i][:-1])
        length = len(explode2)
        print(f"Score {code} * {length} = {code*length}")
        total += code * length
    return total


keypad.display()
arrowpad.display()

print("Example")
print(part1(aocd.data.splitlines()))

# For example, to type 029A,
#
#     < to move the arm from A (its initial position) to 0.
#     A to push the 0 button.
#     ^A to move the arm to the 2 button and push it.
#     >^^A to move the arm to the 9 button and push it.
#     vvvA to move the arm to the A button and push it.


# For each pair of symbols on the main keyboard, find the shortest path between them.

# 1. Check all paths between the symbols
# 2. Explode 1 all paths
# 3. Explode 2 all paths

# Tricky since Explode 1 and Explode 2 generate additional segments... Maybe the
# number of segments is predictable, and we can string together [segment 1
# paths] [segment 2 paths] [segment 3 paths] to iterate through all possible
# combined paths...