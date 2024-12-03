#!/usr/bin/env python

import aocd
from rich.console import Console

print = Console().print

from dataclasses import dataclass
from collections import deque

# --- Day 20: Pulse Propagation ---
example = """\
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
""".splitlines()
# ---------------------------------
# answer_a: 1000
# answer_b: -


# Conjunction modules (prefix &) remember the type of the most recent pulse
# received from each of their connected input modules; they initially default to
# remembering a low pulse for each input. When a pulse is received, the
# conjunction module first updates its memory for that input. Then, if it
# remembers high pulses for all inputs, it sends a low pulse; otherwise, it
# sends a high pulse.

# There is a single broadcast module (named broadcaster). When it receives a
# pulse, it sends the same pulse to all of its destination modules.


@dataclass
class Pulse:
    src: str
    dest: list[str]
    high: bool

    @property
    def low(self):
        return not self.high


@dataclass
class Node:
    name: str
    kind: str
    on: bool
    inputs: list[str]
    outputs: list[str]

    def __init__(self, name):
        self.name = name
        self.inputs = []
        self.outputs = []
        self.kind = ""
        self.last_inputs = {}
        self.on = False

    def pulse(self, p: Pulse) -> list[Pulse]:
        self.last_inputs[p.src] = p
        match self:
            case Node(kind=""):
                return [Pulse(self.name, self.outputs, p.high)]
            case Node(kind="%"):
                # Flip-flop modules (prefix %) are either on or off; they are
                # initially off. If a flip-flop module receives a high pulse, it
                # is ignored and nothing happens. However, if a flip-flop module
                # receives a low pulse, it flips between on and off. If it was
                # off, it turns on and sends a high pulse. If it was on, it
                # turns off and sends a low pulse.
                if p.low:
                    self.on = not self.on
                    return [Pulse(self.name, self.outputs, self.on)]
            case Node(kind="&"):
                # Conjunction modules (prefix &) remember the type of the most recent pulse
                # received from each of their connected input modules; they initially default to
                # remembering a low pulse for each input. When a pulse is received, the
                # conjunction module first updates its memory for that input. Then, if it
                # remembers high pulses for all inputs, it sends a low pulse; otherwise, it
                # sends a high pulse.
                values = [
                    self.last_inputs[n].high if n in self.last_inputs else False
                    for n in self.inputs
                ]
                if all(values):
                    return [Pulse(self.name, self.outputs, False)]
                return [Pulse(self.name, self.outputs, True)]
            case _:
                raise ValueError(f"Unsupported node kind {self.kind}")
        return []


def parse(lines):
    system = {}
    for line in lines:
        l, r = line.split(" -> ")
        outputs = r.split(", ")
        kind = ""
        if not l[0].isalpha():
            kind = l[0]
            l = l[1:]

        node = system.get(l)
        if not node:
            node = Node(l)
        node.kind = kind

        for output in outputs:
            out_node = system.get(output, Node(output))
            out_node.inputs.append(l)
            system[output] = out_node
            node.outputs.append(out_node.name)

        system[l] = node

    return system


def simulate(system, times=1, part2=False):
    pulses = []
    for i in range(1, times):
        q: deque[Pulse] = deque()
        # When you push the button, a single low pulse is sent directly to the broadcaster module.
        q.append(Pulse(dest=["broadcaster"], src="button", high=False))
        while q:
            pulse = q.popleft()
            if not part2:
                pulses.append(pulse)
            for d in pulse.dest:
                if part2 and d == "zp" and pulse.high:
                    print(i, pulse, system[d])
                output = system[d].pulse(pulse)
                # print(pulse, "to", system[d], "produced", output)
                q.extend(output)
    if part2:
        raise ValueError(f"Too slow, {i}")
    return pulses


def tryme(lines, part2=False):
    system = parse(lines)
    pulses = simulate(system, 1000)
    print("Pulsed this many times", sum(len(p.dest) for p in pulses))

    high_pulses = sum(len(p.dest) for p in pulses if p.high)
    low_pulses = sum(len(p.dest) for p in pulses if p.low)
    print(high_pulses, low_pulses)

    return high_pulses * low_pulses


def p2(lines, part2=False):
    system = parse(lines)
    presses = simulate(system, 1000 + (10000000 * part2), part2=part2)
    return presses


print("Example 1")
tryme(example)

print("Example 2")
tryme(
    """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output""".splitlines()
)


# aocd.submit(tryme(aocd.data.splitlines()), part=1)

# aocd.submit(p2(aocd.data.splitlines(), True), part=2)

system = parse(aocd.data.splitlines())

with open("dot.txt", "w") as out:
    out.write("digraph {\n")
    for node in system.values():
        out.write(f"{node.name} -> {{ {' '.join(node.outputs)} }}\n")
    out.write("}\n")


import timeit

k100 = timeit.timeit(lambda: simulate(system, 100001), number=1)

print(
    "Brute force answer in",
    (215252378794009 / 100000) * k100 / 3600 / 24 / 365,
    "years",
)
