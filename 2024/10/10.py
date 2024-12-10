#!/usr/bin/env python

import heapq
import sys
import time
from dataclasses import dataclass
from typing import Iterable

import aocd


def height(letter):
    return int(letter)


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
            if letter == "0":
                self.start = node
            elif letter == "9":
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

    # Rule is "can only go up exactly one level"
    def incoming(self, node: Node):
        """
        All nodes that can reach this node.
        """
        incoming_height = node.height - 1
        for n in self.neighbors(node):
            if n.height == incoming_height:
                yield n

    def outgoing(self, node: Node):
        """
        All nodes that can be reached by this node.
        """
        outgoing_height = node.height + 1
        for n in self.neighbors(node):
            if n.height == outgoing_height:
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
                if col == self.end:
                    char = "\N{SNOWMAN}"
                elif col == self.start:
                    char = "\N{WORLD MAP}"
                elif col.coord in pathset0:
                    char = "\N{CANDLE}"
                elif col in pathset:
                    char = "\N{SLEUTH OR SPY}"
                elif col in pending:
                    char = "+"
                elif col.visited:
                    # print(" ", end="")
                    char = chr(ord("0") + col.distance % 10)
                else:
                    char = col.letter
                print(char, end="")
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
            # if node == goal:
            #     break

            for next in connected(node):
                if not next.visited:
                    next.distance = min(node.distance + 1, next.distance)
                    heapq.heappush(unvisited, (next.distance, next))

    def distinct_paths(self, start: Node, connected):
        """
        Distinct paths to "9" from start using 'connected' function to find neighbors.
        """
        if start.letter == "9":
            return 1
        return sum(self.distinct_paths(next, connected) for next in connected(start))

    def reset(self):
        for node in self.nodes:
            node.reset()


example = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
""".splitlines()


def part1(data: list[str]):
    grid = Grid(data)
    grid.display(set())
    print(grid.start, grid.end)

    assert grid.array[3][4].coord == (4, 3)

    grid.shortest(grid.start, grid.end, grid.outgoing)

    grid.display(set())

    score = 0
    scores = []
    for start in [n for n in grid.nodes if n.letter == "0"]:
        grid.reset()
        start.distance = 0
        grid.start = start
        grid.shortest(grid.start, grid.end, grid.outgoing)
        score += sum(n.distance < sys.maxsize for n in grid.nodes if n.letter == "9")
        scores.append(
            (
                start.coord,
                sum(n.distance < sys.maxsize for n in grid.nodes if n.letter == "9"),
            )
        )

    scores.sort()
    return sum(score for _, score in scores)


print("Part 1", part1(aocd.data.splitlines()))

## Part 2

# For part 2, find all distinct paths between 0's and 9's for each 0.


def part2(data: list[str]):
    gridx = Grid(data)
    total = 0
    for start in sorted(
        (n for n in gridx.nodes if n.letter == "0"), key=lambda n: n.coord
    ):
        score = gridx.distinct_paths(start, gridx.outgoing)
        total += score
    return total


print("Part 2", part2(aocd.data.splitlines()))
