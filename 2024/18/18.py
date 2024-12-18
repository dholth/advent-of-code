#!/usr/bin/env python

import bisect
import heapq
import sys
import time
from dataclasses import dataclass
from typing import Any, Callable, Generator, Iterable

import aocd

sys.setrecursionlimit(10000)

PRETTY = {
    ".": "\N{FULLWIDTH FULL STOP}",
    "#": "🧱",
    "S": "\N{DEER}",
    "E": "\N{PANCAKES}",
}

example = """\
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""

# Your memory space is a two-dimensional grid with coordinates that
# range from 0 to 70 both horizontally and vertically. However, for
# the sake of example, suppose you're on a smaller grid with coordinates
# that range from 0 to 6 and the following list of incoming byte
# positions:


def parse(data):
    return list((*map(int, line.split(",")),) for line in data.splitlines())


HORIZONTAL = 0
VERTICAL = 1


@dataclass(order=True)
class Node:
    distance: int = sys.maxsize
    coord: tuple = (0, 0)
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
            node = Node(coord=coord, **args, letter=letter)
            if letter == "S":
                self.start = node
            elif letter == "E":
                self.end = node
            self.nodes[node.coord] = node
            return node

        self.array = [
            [build(coord=(x, y), letter=c) for (x, c) in enumerate(row)]
            for (y, row) in enumerate(rows)
        ]

        # self.start.distance = 0

    def neighbors(self, node: Node):
        """
        All neighbors for node.
        """
        x, y = node.coord
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = x + dx, y + dy
            if (nx, ny) in self.nodes:
                yield self.nodes[(nx, ny)]

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
                print(PRETTY.get(col.letter), end="")
            print()

    def shortest(
        self,
        start,
        goal,
        connected: Callable[[Node], Generator[tuple[Node, int], Any, None]],
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
            if node == goal:
                break

            for next, cost in connected(node):
                if not next.visited:
                    next.distance = min(node.distance + cost, next.distance)
                    heapq.heappush(unvisited, (next.distance, next))

    def reset(self):
        for node in self.nodes.values():
            node.reset()
        self.start.distance = 0


def ex():
    size = 7  # from 0 to 6 inclusive

    def grid():
        for y in range(size):
            yield "." * size

    g = Grid(grid())
    print(g.nodes)
    g.start = g.nodes[(0, 0)]
    g.end = g.nodes[(5, 5)]
    g.start.distance = 0

    g.display()
    g.shortest(g.start, g.end, g.outgoing)
    g.display()

    print(g.end.distance)

    g.reset()

    for coord in list(parse(example))[:12]:
        g.nodes[coord].letter = "#"

    g.display()

    g.shortest(g.start, g.end, g.outgoing)

    print(g.end.distance)


ex()


def pt1(input, corruption, size=71):
    def grid():
        for _ in range(size):
            yield "." * size

    g = Grid(grid())
    # print(g.nodes)

    g.start = g.nodes[(0, 0)]
    g.end = g.nodes[(size - 1, size - 1)]
    g.start.distance = 0

    # g.display()
    # g.shortest(g.start, g.end, g.outgoing)
    # g.display()

    # print(g.end.distance)

    # g.reset()

    for coord in input[:corruption]:
        g.nodes[coord].letter = "#"

    # g.display()

    g.shortest(g.start, g.end, g.outgoing)

    return g.end.distance


def pt2(start=1024):
    input = parse(aocd.data)
    for i in range(start, len(input)):
        print(i)
        distance = pt1(input, i, size=71)
        if distance == sys.maxsize:
            a, b = input[i - 1]
            print("Answer is", f"{a},{b}")
            # aocd.submit()
            break


def pt2ex():
    input = parse(example)
    for i in range(len(input)):
        print(i)
        distance = pt1(input, i, size=7)
        if distance == sys.maxsize:
            a, b = input[i - 1]
            print("Answer is", f"{a},{b}")
            break


class Pt2List:
    """
    Use builtin binary search.
    """

    def __init__(self, input="", size=71):
        self.input = parse(input or aocd.data)
        self.size = size

    def __getitem__(self, i):
        """
        Return 0 if destination is reachable after dropping i blocks, else
        return 1.
        """
        print("try", i)
        input = self.input
        distance = pt1(input, i, size=self.size)
        if distance == sys.maxsize:
            return 1
        return 0

    def __len__(self):
        return len(self.input)


pt2list = Pt2List()

begin = time.time_ns()
pt2(start=1024)
end = time.time_ns()
print(f"Brute force answer in {(end-begin)/1e9:.02f}s")

begin = time.time_ns()
print(ans2 := bisect.bisect_left(pt2list, 1))
end = time.time_ns()
print(f"Find {pt2list.input[ans2-1]} using bisect_left in {(end-begin)/1e9:.02f}s")

begin = time.time_ns()
print(ans3 := bisect.bisect_right(pt2list, 0))  # bisect() is bisect_right()
end = time.time_ns()
print(f"Find {pt2list.input[ans3-1]} using bisect_right in {(end-begin)/1e9:.02f}s")
