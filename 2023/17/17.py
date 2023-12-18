#!/usr/bin/env python

import networkx as nx
from networkx.algorithms import shortest_path_length

import aocd
from rich.console import Console

print = Console().print

data = aocd.data.splitlines()

example = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""".splitlines()


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


# column, row
N = V(0, -1)
S = V(0, 1)
E = V(1, 0)
W = V(-1, 0)

cardinals = [N, E, S, W]

t = str.maketrans({})


def display(board, message=""):
    print(f"--- {message}")
    print("\n".join([n.translate(t) for n in board]))


def load(lines):
    board: dict[tuple, str] = {}

    for i, line in enumerate(lines, start=0):
        for j, char in enumerate(line, start=0):
            board[V(j, i)] = int(char)

    return board


display(example)


board = load(data)

# horizontal and vertical nodes
# each cell explodes to several nodes with accumulated costs, then linking to the other direction:
#
# 123
# 456
# 789

# you only incur cost by entering a block, not by leaving it
# ... can only move 3 blocks in a single direction before turning 90 degrees left or right
# ... a bit like a knight

# 1

# store (coord, direction) ->(cost) -> (coord', direction')

#
#     yyy
#    x>
#     zzz

# (x, east) links to 3 y N's and 3 Z S's or maybe 4 "move forward zero before turning"

# rinse repeat

# special-case the goal so it is one node

MAX_TRAVEL = 10
MIN_TRAVEL = 4


class Board:
    def __init__(self, data):
        self.data = data

    def edges(self, coord, direction, part2=True):
        index = cardinals.index(direction)
        left = cardinals[(index - 1) % len(cardinals)]
        right = cardinals[(index + 1) % len(cardinals)]

        here = coord
        cost = 0
        for i in range(MAX_TRAVEL):
            here += direction
            if here in self.data:
                cost += self.data[here]
                if part2 and i < (MIN_TRAVEL - 1):
                    continue
                yield (here, left), cost
                yield (here, right), cost


b = Board(board)

print("Edges from zero")
for c in cardinals:
    # 1-indexed
    print(list(b.edges(V(0, 0), c)))

dg = nx.DiGraph()

for coord in b.data:
    for direction in cardinals:
        dg.add_node((coord, direction))

for coord in b.data:
    for direction in cardinals:
        new_edges = [
            ((coord, direction), n, weight)
            for n, weight in b.edges(coord, direction, part2=True)
        ]
        dg.add_weighted_edges_from(new_edges)

start = (V(0, 0), E)
alt_start = (V(0, 0), S)

max_x = max(x for x, y in board)
max_y = max(y for x, y in board)
goal = (V(max_x, max_y), S)
alt_goal = (V(max_x, max_y), E)

lengths = []
for s in (start, alt_start):
    for g in (goal, alt_goal):
        lengths.append(shortest_path_length(dg, source=s, target=g, weight="weight"))
        print(f"{s}->{g}", lengths[-1])


def show(graph):
    import matplotlib.pyplot as plt

    subax1 = plt.subplot()
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos=pos, with_labels=True, ax=subax1)

    plt.show()
