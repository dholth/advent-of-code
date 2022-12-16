#!/usr/bin/env python
from __future__ import annotations

import contextlib
import re
from dataclasses import dataclass

import aocd
import networkx as nx
import time


@contextlib.contextmanager
def timeme(message=""):
    start = time.time()
    yield
    end = time.time()
    print(f"{message} {end - start:0.2f}s")


SHOW = False

# start at AA
example = """\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
""".splitlines()


@dataclass(order=True)
class Node:
    name: str
    index: int
    rate: int  # pressure released
    neighbors: list[str]

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return f"{self.name} {self.rate or ''}"


parse_re = re.compile(
    r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)"
)


def parse(lines):
    for i, line in enumerate(lines):
        match = parse_re.match(line)
        assert match
        name, rate, neighbors = match.groups()
        yield Node(
            name=name,
            index=i,
            rate=int(rate),
            neighbors=neighbors.split(", "),
        )


import aocd

print(len(aocd.lines))
print(
    "How many have a nonzero flow rate in the full puzzle?",
    sum(n.rate > 0 for n in parse(aocd.lines)),
)
print(
    "... in the example?",
    sum(n.rate > 0 for n in parse(example)),
)


def go(lines, show=False):
    nodes: dict[str, Node] = {}

    for i, node in enumerate(parse(lines)):
        nodes[node.name] = node

    graph = nx.DiGraph()
    for node in nodes.values():
        for neighbor in node.neighbors:
            # # no mr. graph, I expect you to di!
            # if neighbor > node.name:
            graph.add_edge(node, nodes[neighbor])

    return graph, nodes


def show(graph):
    import matplotlib.pyplot as plt

    subax1 = plt.subplot()
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos=pos, with_labels=True, ax=subax1)

    plt.show()


graph, nodes = go(example, show=False)

from networkx.algorithms import floyd_warshall_numpy


def distance(graph, nodes):
    # distance matrix with original node order, otherwise graph.nodes()
    return floyd_warshall_numpy(graph, nodelist=nodes.values())


print(distance(graph, nodes))

if SHOW:
    show(graph)

graph, nodes = go(aocd.lines)
dist = distance(graph, nodes)

if SHOW:
    show(graph)

all_scores = []
total_scores = 0


def score(sequence):
    global total_scores
    total_scores += 1
    current_score = sum(node.rate * t for node, t in sequence)
    all_scores.append((current_score, set(node for node, _ in sequence)))
    return current_score


opened: list = []
max_score = 0
max_solution = []
total_searches = 0


def search(here, valves: set[Node], distance, remaining=30):
    global max_score, max_solution, total_searches
    total_searches += 1

    to_next = distance[here.index]

    for valve in valves:
        walking = to_next[valve.index]
        if walking >= remaining:
            continue

        open_time = int(remaining - walking - 1)
        opened.append((valve, open_time))
        search(valve, valves - {valve}, distance, remaining=open_time)
        opened.pop()

    else:
        s = score(opened)
        if max_score < s:
            max_score = s
            names = " ".join(f"{node.name}" for node, t in opened)
            # if names == "DD BB JJ HH EE CC":
            #     assert s == 1651
            # print(f"{s} {names} {remaining}")


valves = [n for n in nodes.values() if n.rate]

with timeme("Part A traverse"):
    search(nodes["AA"], set(valves), dist)

print("30 seconds")

all_scores.sort(key=lambda s: s[0], reverse=True)
print("Best", max(all_scores))
print("searches:", total_searches)
print("scores:", total_scores)


opened: list = []
max_score = 0
max_solution = []
total_searches = 0
total_scores = 0
all_scores = []


with timeme("Part B traverse"):
    search(nodes["AA"], set(valves), dist, remaining=30 - 4)

print("24 seconds, two workers")
print("searches:", total_searches)
print("scores:", total_scores)

# this produces a correct guess fast
all_scores.sort(key=lambda s: s[0], reverse=True)

# what if instead of searching the whole triangle, we searched all solutions
# smaller than an index into this array?
with timeme("Create scores by length array"):
    # above sort already keeps these sorted by score
    scores_by_length = [[]] * len(valves)
    for i, scores in enumerate(
        [[s for s in all_scores if len(s[1]) < k] for k in range(len(valves))]
    ):
        scores_by_length[i] = scores

# none of scores_by_length happen to be longer than 8 valves


def cross_search(time_limit=1):
    max_cross = 0

    begin = time.time()
    for i in range(len(all_scores)):
        score0, valves0 = all_scores[i]
        for j in range(i, len(all_scores)):
            score1, valves1 = all_scores[j]
            if score0 + score1 > max_cross and valves0.isdisjoint(valves1):
                max_cross = score0 + score1
                print(
                    i,
                    j,
                    max_cross,
                    tuple(v.name for v in valves0),
                    tuple(v.name for v in valves1),
                )

        if time.time() - begin > time_limit:
            return


def cross_search_2(time_limit=1):
    max_cross = 0

    total_valves = len(valves)
    begin = time.time()
    for i in range(len(all_scores)):
        score0, valves0 = all_scores[i]
        remaining_valves = total_valves - len(valves0)
        try:
            for score1, valves1 in scores_by_length[remaining_valves]:
                if score0 + score1 > max_cross and valves0.isdisjoint(valves1):
                    max_cross = score0 + score1
                    print(
                        i,
                        max_cross,
                        tuple(v.name for v in valves0),
                        tuple(v.name for v in valves1),
                    )
        except IndexError:
            print(tuple(v.name for v in valves0), remaining_valves, total_valves)
            print("IndexError")
        if time.time() - begin > time_limit:
            return


# index to first result with a certain score
points = []
for i, (score, nodes) in enumerate(all_scores):
    if not points or score < points[-1][0]:
        points.append((score, i))

# skip parts of all_scores if part a score + part b score < max_score
# since all_scores is sorted by score descending
def cross_search_by_scores(time_limit=1):
    max_cross = 0

    begin = time.time()
    for i in range(len(all_scores)):
        score0, valves0 = all_scores[i]
        for j in range(i, len(all_scores)):
            score1, valves1 = all_scores[j]
            potential_score = score0 + score1
            if potential_score < max_cross:
                break
            elif potential_score > max_cross and valves0.isdisjoint(valves1):
                max_cross = score0 + score1
                print(
                    i,
                    j,
                    max_cross,
                    tuple(v.name for v in valves0),
                    tuple(v.name for v in valves1),
                )

        if time.time() - begin > time_limit:
            return


# ~170s to run to completion (prints answer immediately)
time_limit = 1
with timeme(f"Cross i*j method with {time_limit}s time limit"):
    cross_search(time_limit=time_limit)

# ~62.5s to run to completion (prints answer immediately)
# possibly against buggy set of scores to check
# with timeme("Cross shorter-sets-only method."):
#     cross_search(200)

with timeme("Cross, skipping if bigger score not possible."):
    cross_search_by_scores(200)
