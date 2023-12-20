#!/usr/bin/env python

import math
import re
from itertools import groupby

import aocd
import networkx as nx
from rich.console import Console

print = Console().print

pattern = re.compile(r"^(?P<source>\w+)\{(?P<inner>.*)\}$", re.VERBOSE)
inner_pattern = re.compile(
    r"((?P<var>\w)(?P<op>[<>])(?P<val>\d+):)?(?P<next>\w+)(,|$)", re.VERBOSE
)

example = """\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
""".splitlines()


def sections(lines):
    """
    Split lines by blank lines.
    """
    return [[*g] for k, g in groupby(lines, bool) if k]


def parse_items(items):
    for item in items:
        yield dict(zip("xmas", map(int, re.findall(r"\d+", item))))


def parse_ops(ops):
    for op in ops:
        source, program = pattern.match(op).groups()

        yield (source, [m.groupdict() for m in inner_pattern.finditer(program)])


full_data = aocd.data.splitlines()
flows, items = sections(full_data)

items = list(parse_items(items))

flows = dict(parse_ops(flows))

# print(items)
# print(flows)


def interpret_one(item, flow):
    here = ""
    for ins in flow:
        op = ins["op"]
        next = ins["next"]
        var = ins["var"]
        val = int(ins["val"]) if ins["val"] is not None else None
        match op:
            case None:
                here = next
            case "<":
                if item[var] < val:
                    return next
            case ">":
                if item[var] > val:
                    return next
            case _:
                assert False
    return here


def interpret(item, flows):
    here = "in"
    while here not in ("R", "A"):
        try:
            here = interpret_one(item, flows[here])
        except KeyError:
            print("flow", here, "not found")
            raise
    return here


accepted = []
rejected = []

for item in items:
    status = interpret(item, flows)
    if status == "A":
        accepted.append(item)


def score(items):
    return sum(sum(v for v in item.values()) for item in items)


print("Score", score(accepted))


START = 1
END = 4001
XMAS = "xmas"


def show(graph):
    import matplotlib.pyplot as plt

    subax1 = plt.subplot()
    pos = nx.shell_layout(graph)
    nx.draw(graph, pos=pos, with_labels=True, ax=subax1)

    plt.show()


def display_part2(data):
    flows = dict(parse_ops(sections(data)[0]))

    digraph = nx.DiGraph()
    for k, v in flows.items():
        for step in v:
            digraph.add_edge(k, step["next"])

    try:
        nx.cycles.find_cycle(digraph)
        raise ValueError("Graph has cycles")
    except nx.exception.NetworkXNoCycle:
        print("Graph has no cycles")

    show(digraph)


# display_part2(aocd.data.splitlines())


def format_step(step):
    if step["op"]:
        return f"{step['var']}{step['op']}{step['val']}"
    return "."


def inverse_step(step):
    match step["op"]:
        case None:
            return "."
        case ">":
            return {**step, "op": "<="}
        case "<":
            return {**step, "op": ">="}
        case _:
            raise ValueError("Unexpected")


def step_to_range(step):
    r = None
    if op := step["op"]:
        value = int(step["val"])
        match op:
            case ">":
                r = range(value + 1, END)
            case "<":
                return range(START, value)
            case ">=":
                return range(value, END)
            case "<=":
                return range(START, value + 1)
            case _:
                raise ValueError("Unexpected")
    return r


def merge_ranges(r1: range, r2: range):
    return range(max(r1.start, r2.start), min(r1.stop, r2.stop))


def steps_to_ranges(steps):
    xmas = dict(zip("xmas", (range(START, END),) * 4))
    for step in steps:
        r = step_to_range(step)
        if r is not None:
            var = step["var"]
            xmas[var] = merge_ranges(xmas[var], r)
    return xmas


def traverse_graph(flows, here, previous=()):
    if here in "RA":
        # print(list(format_step(s) for s in previous), here)
        if here == "A":
            yield steps_to_ranges(previous)
        return

    for step in flows[here]:
        yield from traverse_graph(flows, step["next"], previous + (step,))
        # and inverse of step
        previous = previous + (inverse_step(step),)


flows = dict(parse_ops(sections(full_data)[0]))
traversals = list(traverse_graph(flows, "in"))
print(f"Found {len(traversals)} accepted paths")

all = 0
for t in traversals:
    all += sum([math.prod(len(r) for r in t.values())])

print("Accepted", all)
