#!/usr/bin/env python

import aocd
import ast
from graphlib import TopologicalSorter


def parse(lines, fp=True):
    allowed = (
        ast.Assign,
        ast.Name,
        ast.BinOp,
        ast.operator,
        ast.Load,
        ast.Store,
        ast.Constant,
    )
    for line in lines:
        line = line.replace(":", "=")
        if not fp:
            line = line.replace("/", "//")

        parsed = ast.parse(line, mode="exec").body[0]

        assert all(isinstance(n, allowed) for n in ast.walk(parsed)), list(
            ast.walk(parsed)
        )

        node = {}
        deps = set()

        for i, (name, nodes) in enumerate(ast.iter_fields(parsed)):
            if name == "targets":
                node[nodes[0].id] = deps

            if name == "value":
                deps.update(
                    m.id for _, m in ast.iter_fields(nodes) if isinstance(m, ast.Name)
                )

        yield node, parsed


asts = {}
graph = {}

# part b gives different answer for fp=True; don't know if advent of code would
# accept both
for node, parsed in parse(aocd.lines, fp=True):
    target = list(node.keys())[0]
    # stablize the toposort
    node[target] = sorted(node[target])
    graph.update(node)
    asts[target] = parsed

ts = TopologicalSorter(graph)
module = ast.parse("")
module.body = [asts[name] for name in ts.static_order()]
# print(ast.dump(module))

scope = {}
eval(compile(module, "", "exec"), scope)

print("Part the first", scope["root"])

a, b = graph["root"]
monkey = ast.parse(f"def monkey(humn): return {a}, {b}")
monkey_fn = monkey.body[0]

ts = TopologicalSorter(graph)
monkey_fn.body = [
    asts[name] for name in ts.static_order() if name not in ("humn", "root")
] + [monkey_fn.body[0]]

scope = {}
eval(compile(monkey, "", "exec"), scope)
monkey = scope["monkey"]

guesses = range(-1024000, 1024000, 1024000 // 1024)

vals = [monkey(guess)[0] for guess in guesses]
vals2 = [monkey(guess)[1] for guess in guesses]

# this one is constant
assert all(v == vals2[0] for v in vals2)

a0, b0 = monkey(0)
a1, b1 = monkey(1)
assert b0 == b1

# math fails me, try guessing
# is between 0 and 72950437237489 for my input
guess = 72950437237489
a0, b0 = monkey(0)
a1, b1 = monkey(guess)

assert a0 > b0


def find(min_guess=0, max_guess=guess):
    for n in range(64):
        for x in range(min_guess, max_guess, (max_guess - min_guess) // 2):
            a0, b0 = monkey(x)
            if a0 < b0:
                min_guess = x
            elif a0 == b0:
                print(f"Guess in {n}", x, a0, b0)
                return x
            else:
                max_guess = x


g = find()
print("guess", g)

a0, b0 = monkey(0)
a1, b1 = monkey(1)
assert b0 == b1
print(a0, a1, b1 + (a0 / (a0 / a1)))

# genius idea from the internet
a, b = monkey(0 + 1j)
genius = int((b - a.real) / a.imag)
print("Imagine", genius, g, genius == g)

