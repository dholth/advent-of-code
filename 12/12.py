#!/usr/bin/env python

import heapq
import sys
from dataclasses import dataclass
from typing import Iterable

import aocd


def height(letter):
    if letter == "S":
        letter = "a"
    elif letter == "E":
        letter = "z"
    return ord(letter) - ord("a")


@dataclass(order=True)
class Node:
    distance: int = sys.maxsize
    coord: tuple = (0, 0)
    height: int = 0
    visited: bool = False

    def __hash__(self):
        return hash(self.coord)


@dataclass
class Grid:
    nodes: set[Node]
    array: list[list[Node]]
    start: Node
    end: Node
    prev: Node = None

    def __init__(self, rows):
        self.nodes = set()
        self.array = []

        def build(letter="", **args):
            node = Node(**args)
            if letter == "S":
                self.start = node
            elif letter == "E":
                self.end = node
            self.nodes.add(node)
            return node

        self.array = [
            [
                build(coord=(x, y), height=height(c), letter=c)
                for (x, c) in enumerate(row)
            ]
            for (y, row) in enumerate(rows)
        ]

        self.start.distance = 0

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

    def incoming(self, node: Node):
        """
        All nodes that can reach this node.
        """
        for n in self.neighbors(node):
            if node.height <= n.height + 1:
                yield n

    def outgoing(self, node: Node):
        """
        All nodes that can be reached by this node.
        """
        max_height = node.height + 1
        for n in self.neighbors(node):
            if n.height <= max_height:
                yield n

    def display(self, pending, pathset0: Iterable = (), pathset: Iterable[Node] = ()):
        pathset0 = set(pathset0)
        pathset = set(pathset)
        print("\N{MOUNTAIN}")
        for row in grid.array:
            for col in row:
                if col == grid.end:
                    char = "\N{SNOWMAN}"
                elif col == grid.start:
                    char = "\N{WORLD MAP}"
                elif col.coord in pathset0:
                    char = "\N{CANDLE}"
                elif col in pathset:
                    char = "\N{SLEUTH OR SPY}"
                elif col in pending:
                    char = "x"
                elif col.visited:
                    # print(" ", end="")
                    char = chr(ord("0") + col.distance % 10)
                else:
                    char = "."
                print(char, end="")
            print()

    def shortest(self, start, goal, connected):
        # nodes.visited and nodes.distance should be reset before calling
        unvisited = [start]
        while unvisited:
            node = heapq.heappop(unvisited)
            if node.visited:
                continue
            node.visited = True
            if node == goal:
                break

            for next in connected(node):
                if not next.visited:
                    next.distance = min(node.distance + 1, next.distance)
                    heapq.heappush(unvisited, next)

    def climbdown(self, start: Node, goal: Node):
        """
        After calling shortest, traverse backwards from goal.
        """
        path = [goal]
        current = goal
        i = 0
        while current != start and i < 600:
            try:
                current = sorted(
                    n
                    for n in grid.incoming(current)
                    if n.distance == current.distance - 1
                )[-1]
                path.append(current)
            except IndexError:
                break
            i += 1

        return path


# is 181x41 grid
example = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
""".splitlines()

grid = Grid(example)
grid.display(set())
print(grid.start, grid.end)

assert grid.array[3][4].coord == (4, 3)

print("\n".join(aocd.lines))

grid = Grid(aocd.lines)

grid.shortest(grid.start, grid.end, grid.outgoing)
path = grid.climbdown(grid.start, grid.end)
pathset0 = set(p.coord for p in path)

grid.display(set(), pathset0, set())
print()
print("Steps to summit:", grid.end.distance, grid.end)

# Part 1: shortest path from starting point to end
# aocd.submit(grid.end.distance)

# part 2: shortest path from any a to end
grid = Grid(aocd.lines)

grid.end.distance = 0
grid.start.distance = sys.maxsize

grid.shortest(grid.end, grid.start, grid.incoming)

all_as = sorted(n for n in grid.nodes if n.height == 0)

print("Target:", grid.end)
print("Original starting point:", grid.start)
print("Best starting points:", all_as[:10])

pathset = set(grid.climbdown(grid.end, all_as[0]))

grid.display(set(), pathset0, pathset)
