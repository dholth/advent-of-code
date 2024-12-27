#!/usr/bin/env python

import collections
import heapq
import pprint
import sys
import time
from dataclasses import dataclass
from typing import Any, Callable, Generator, Iterable

import aocd

PRETTY = {
    ".": "\N{FULLWIDTH FULL STOP}",
    "#": "🧱",
    "S": "\N{DEER}",
    "E": "\N{PANCAKES}",
    "*": "\N{GLOWING STAR}",
}


def parse(data):
    return list((*map(int, line.split(",")),) for line in data.splitlines())


HORIZONTAL = 0
VERTICAL = 1


class V(tuple):
    def __new__(cls, *args):
        return super(V, cls).__new__(cls, args)

    def __add__(self, other):
        return self.__class__(*(a + b for a, b in zip(self, other)))

    def __sub__(self, other):
        return self.__class__(*(a - b for a, b in zip(self, other)))

    def taxi(self):
        a, b = self
        return int(abs(a) + abs(b))

    def __repr__(self):
        return f"V{str((*self,))}"


@dataclass(order=True)
class Node:
    distance: int = sys.maxsize
    coord: V = V(0, 0)
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

    def __init__(self, rows: str | list[str]):
        self.nodes = {}
        self.array = []

        if isinstance(rows, str):
            rows = rows.splitlines()

        def build(coord=(), letter="", **args):
            node = Node(coord=coord, **args, letter=letter)
            if letter == "S":
                self.start = node
            elif letter == "E":
                self.end = node
            self.nodes[node.coord] = node
            return node

        self.array = [
            [build(coord=V(x, y), letter=c) for (x, c) in enumerate(row)]
            for (y, row) in enumerate(rows)
        ]

    def neighbors(self, node: Node):
        """
        All neighbors for node.
        """
        x, y = node.coord
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = x + dx, y + dy
            if (nx, ny) in self.nodes:
                yield self.nodes[(nx, ny)]

    def taxis(self, node: Node, radius: int = 1):
        radius += 1
        x, y = node.coord
        for dy in range(-radius, radius):
            sideways = radius - abs(dy)
            for dx in range(-sideways + 1, sideways):
                x1, y1 = x + dx, y + dy
                if (x1, y1) in self.nodes:
                    yield self.nodes[(x1, y1)]

    def outgoing(self, node: Node):
        """
        All nodes that can be reached by this node, plus cost.
        """
        for n in self.neighbors(node):
            if n.letter != "#":
                yield n, 1

    def display(
        self,
        pending=(),
        pathset0: Iterable[tuple[int, int]] = (),
        pathset: Iterable[Node] = (),
    ):
        pathset0 = set(pathset0)
        pathset = set(pathset)
        pending = set(pending)
        print("\N{MOUNTAIN}")
        for row in self.array:
            for col in row:
                letter = col.letter
                if col.coord in pending:
                    letter = "*"
                print(PRETTY.get(letter), end="")
            print()

    def shortest(
        self,
        start,
        goal,
        connected: Callable[[Node], Generator[tuple[Node, int], Any, None]],
        show=False,
        stop_at_goal=False,
    ):
        # nodes.visited and nodes.distance should be reset before calling
        display_distance = 0
        start.distance = 0
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
            if stop_at_goal and node == goal:
                break

            for next, cost in connected(node):
                if not next.visited:
                    next.distance = min(node.distance + cost, next.distance)
                    heapq.heappush(unvisited, (next.distance, next))

    def reset(self):
        for node in self.nodes.values():
            node.reset()


example = """\
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""


def part1():
    grid = Grid(aocd.data.splitlines())
    grid.display()

    # the forwards version
    # there is only one path through the maze, so we don't need both forward and reverse!
    grid.shortest(grid.start, grid.end, grid.outgoing)

    counter = collections.Counter()

    for node in grid.nodes.values():
        if node.letter != "#":
            continue

        if node.coord == (4, 1):
            # import pdb; pdb.set_trace()
            pass

        try:
            left, right, above, below = (*grid.neighbors(node),)
        except ValueError:
            # print("Skip", node)
            continue

        for a, b in (left, right), (above, below):
            # (right, left), (above, below), (below, above):
            if a.letter == "#" or b.letter == "#":
                continue  # watch out for sys.maxint
            # Subtract 2 steps taken to cross the shortcut, Buckaroo Banzai style
            shortcut = abs(a.distance - b.distance) - 2
            if (
                shortcut > 0 and shortcut.bit_length() < 16
            ):  # supre long shortcuts still?
                counter.update((shortcut,))
                # ex.display((a.coord, b.coord))
                # input(f"Saves {shortcut}")

    grid.display(set(((8, 8),)))

    pprint.pprint(dict(counter))

    ans = sum(v for k, v in counter.items() if k >= 100)
    print("P1 answer", ans)
    return ans


## Part 2


def part2():
    # Cheats can last up to 20 units.
    # We will start from the dots now.
    # If a cheat has the same start and end coordinates, it is the same cheat.
    # Horizontal AND vertical movement is allowed during the cheat. (A diamond shape)

    grid = Grid(example)
    for radius in range(3):
        nodes = set(x.coord for x in grid.taxis(grid.nodes[(8, 8)], radius))
        grid.display(nodes)
        input(f"Radius {radius}")

    ## Part 2 (real data)

    grid = Grid(aocd.data)
    grid.display()

    # the forwards version
    grid.shortest(grid.start, grid.end, grid.outgoing)

    counter = collections.Counter()
    seen = set()
    for node in grid.nodes.values():
        if node.letter not in ".SE":
            continue

        for cheat_end in grid.taxis(node, radius=20):
            cheat_id = frozenset((node.coord, cheat_end.coord))
            if cheat_end.letter == "#" or cheat_end == node or cheat_id in seen:
                continue
            # print("Consider", node.coord, cheat_end.coord)
            seen.add(cheat_id)

            shortcut = abs(node.distance - cheat_end.distance)
            shortcut_penalty = (node.coord - cheat_end.coord).taxi()
            shortcut -= shortcut_penalty
            # print("Shortcut", shortcut, "Penalty", shortcut_penalty)

            # ex.display((node.coord, cheat_end.coord))

            if (
                shortcut > 0 and shortcut.bit_length() < 16
            ):  # supre long shortcuts still?
                counter.update((shortcut,))
                # ex.display((a.coord, b.coord))
                # input(f"Saves {shortcut}")

    # pprint.pprint(dict(counter))

    print("P2 answer", sum(v for k, v in counter.items() if k >= 100))

# ## Combinations version (not used)

# ex = Grid(example)
# ex.shortest(ex.start, ex.end, ex.outgoing)
# counter = collections.Counter()
# interesting = [node for node in ex.nodes.values() if node.letter in ".SE"]
# for start, end in combinations(interesting, 2):
#     distance = (start.coord - end.coord).taxi()
#     if distance > 2:
#         continue
#     shortcut = abs(start.distance - cheat_end.distance)
#     ...


if __name__ == "__main__":
    part1()
    part2()
