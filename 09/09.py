#!/usr/bin/env python
import aocd
from operator import add, sub

example = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
""".splitlines()

#     U
# <- L R ->
#     D
directions = {"R": (1, 0), "L": (-1, 0), "U": (0, -1), "D": (0, 1)}


def parse(lines):
    for line in lines:
        d, c = line.split()
        yield d, int(c)


print([*parse(example)])

# head, tail
rope = [(0, 0), (0, 0)]


def display(rope, width=20, height=20):
    # (0, 0) in bottom left
    lower = tuple(map(min, *rope))
    upper = tuple(map(max, *rope))
    size = tuple(map(sub, upper, lower))
    row = ["."] * (size[0] + 1)
    grid = [row.copy() for _ in range(size[1] + 1)]
    # 0, 0 not necessarily in lower / upper window
    # grid[0 - lower[1]][0 - lower[0]] = "+"
    for i, (x, y) in enumerate(rope):
        grid[y - lower[1]][x - lower[0]] = str(i)
    return "\n".join(reversed(list("".join(row) for row in grid)))


print(display(rope))


def cmp(a, b):
    return (a > b) - (a < b)


def follow(head, tail):
    # return new tail position
    distance = tuple(map(sub, head, tail))
    if max(abs(d) for d in distance) < 2:
        return tail
    delta = tuple(map(cmp, head, tail))
    tail = tuple(map(add, tail, delta))
    return tail


def dragaround(lines):
    history = []
    for d, count in parse(lines):
        for _ in range(count):
            rope[0] = tuple(map(add, rope[0], directions[d]))
            for i in range(1, len(rope)):
                rope[i] = follow(rope[i - 1], rope[i])
            history.append(rope[-1])
        print(display(rope) + "\n")
    return history


assert len(set(dragaround(example))) == 13

rope = [(0, 0)] * 2
print(len(set(dragaround(aocd.lines))))

rope = [(0, 0)] * 10
print(len(set(dragaround(aocd.lines))))
