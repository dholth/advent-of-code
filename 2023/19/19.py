#!/usr/bin/env python

import aocd
from itertools import groupby
from rich.console import Console
import re

print = Console().print

pattern = re.compile(r"^(?P<source>\w+)\{(?P<inner>.*)\}$", re.VERBOSE)
inner_pattern = re.compile(
    r"(?P<var>\w)(?P<op>[<>])(?P<num>\d+):(?P<next>\w+)(,$)", re.VERBOSE
)
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


def splitblank(lines):
    return [[*g] for k, g in groupby(lines, bool) if k]


def parse_items(items):
    for item in items:
        yield dict(zip("xmas", map(int, re.findall(r"\d+", item))))


def parse_ops(ops):
    for op in ops:
        source, program = pattern.match(op).groups()

        yield (source, [m.groupdict() for m in inner_pattern.finditer(program)])


data = aocd.data.splitlines()
flows, items = splitblank(data)

items = list(parse_items(items))

flows = dict(parse_ops(flows))

print(items)
print(flows)


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
