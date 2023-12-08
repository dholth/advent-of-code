#!/usr/bin/env python

import re
from itertools import cycle, groupby

import aocd
from numpy import lcm


def splits(line):
    here, left, right = list(re.findall("\w+", line))

    ["".join(g) for x, g in groupby(line, str.isalpha) if x]
    return here, (left, right)


def desertgraph(data):
    data = iter(data)
    path = cycle(next(data))
    assert next(data) == ""
    graph = dict(splits(line) for line in data)
    return path, graph


def part1(path, graph, start="AAA", win=lambda x: x == "ZZZ"):
    steps = 0
    here = start
    while not win(here):
        rl = next(path)
        there = graph[here][rl == "R"]
        # print(here, there)
        here = there
        steps += 1

    return steps


# part 2
# start at all nodes that end with A
# end at all nodes that end with Z


aocd.submit(part1(*desertgraph(aocd.data.splitlines())), part=1)

path, graph = desertgraph(aocd.data.splitlines())

if False:
    path, graph = desertgraph(
        """LR

    11A = (11B, XXX)
    11B = (XXX, 11Z)
    11Z = (11B, XXX)
    22A = (22B, XXX)
    22B = (22C, 22C)
    22C = (22Z, 22Z)
    22Z = (22B, 22B)
    XXX = (XXX, XXX)""".splitlines()
    )

starts = [g for g in graph if g.endswith("A")]
# ['GSA', 'DLA', 'MLA', 'MQA', 'AAA', 'JGA']
ends = [g for g in graph if g.endswith("Z")]
# ['ZZZ', 'PXZ', 'TFZ', 'QLZ', 'XJZ', 'DXZ']

# steps = 0
# while not all(s.endswith('Z') for s in starts):
#     rl = next(path)
#     nexts = [graph[here][rl == "R"] for here in starts]
#     steps += 1
#     # print(starts, nexts)
#     if steps % 1024 == 0:
#         print(steps, nexts)
#     starts = nexts

# need to find the cycle length for each of starts and multiply?
print("Starting from", starts)
steps = []
for s in starts:
    # need fresh path
    path, graph = desertgraph(aocd.data.splitlines())
    ans = part1(path, graph, start=s, win=lambda x: x.endswith("Z"))
    print(s, ans)
    steps.append(ans)

print(steps)

# the fast way
print(lcm.reduce(steps))

# slow but it worked
increment = min(steps)

howfar = increment
while not all(howfar % x == 0 for x in steps):
    howfar += increment
print(howfar)
