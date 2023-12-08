#!/usr/bin/env python

from functools import total_ordering
import pathlib
import itertools
import math

input = pathlib.Path("13/input.txt").read_text().splitlines()

sample = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
""".splitlines()


def pairs(lines):
    lines = iter(lines)
    for line in lines:
        if not line:
            line = next(lines)
        yield [Specialist(eval(line)), Specialist(eval(next(lines)))]


def devils_compare(l, r):
    if isinstance(l, int) and isinstance(r, int):
        return l < r
    if isinstance(l, int):
        l = [l]
    if isinstance(r, int):
        r = [r]
    il = iter(l)
    ir = iter(r)
    for a, b in zip(il, ir):
        if devils_compare(a, b):
            return True
        elif devils_compare(b, a):
            return False
    try:
        next(ir)
        return True
    except StopIteration:
        return False


@total_ordering
class Specialist(list):
    def __init__(self, items):
        for item in items:
            if isinstance(item, list):
                self.append(Specialist(item))
            else:
                assert isinstance(item, int)
                self.append(item)

    def __lt__(self, other):
        return devils_compare(self, other)

    def __gt__(self, other):
        return NotImplemented


for pair in pairs(sample):
    print(pair)
    l, r = pair
    print(l < r)

result = [(i, l < r) for i, (l, r) in enumerate(pairs(sample), 1)]
print(result)
print("example p1", sum(i for i, less in result if less))

result = [(i, l < r) for i, (l, r) in enumerate(pairs(input), 1)]
# print(result)
print("p1", sum(i for i, less in result if less))

dividers = Specialist([[2]]), Specialist([[6]])

chained = list(itertools.chain.from_iterable(pairs(input)))
chained.append(Specialist([[2]]))
chained.append(Specialist([[6]]))
pathlib.Path("13/unsorted.txt").write_text("\n".join(repr(c) for c in chained) + "\n")
chained.sort()
pathlib.Path("13/sorted.txt").write_text("\n".join(repr(c) for c in chained) + "\n")

print("p2", math.prod(chained.index(d) + 1 for d in dividers))


def sample_p2():
    chained = list(itertools.chain.from_iterable(pairs(sample)))
    chained.append(Specialist([[2]]))
    chained.append(Specialist([[6]]))
    chained.sort()
    pathlib.Path("13/sampled.txt").write_text(
        "\n".join(repr(c) for c in chained) + "\n"
    )
    print("Sample p2", math.prod(chained.index(d) + 1 for d in dividers))


sample_p2()

try:
    assert not Specialist([[1], 4]) < Specialist([1, [2, [3, [4, [5, 6, 0]]]], 8, 9])
    assert Specialist([1, [2, [3, [4, [5, 6, 0]]]], 8, 9]) < Specialist([[1], 4])
except AssertionError:
    print("oops")

a = Specialist([[1], 4])
b = Specialist([1, [2, [3, [4, [5, 6, 0]]]], 8, 9])
print(a < b)

print("all the misordered ones")
# python 3.10
for i, (l, r) in enumerate(itertools.pairwise(chained)):
    if not l < r:
        print(i, l, "!<", r)


print("next")
print(devils_compare(a, b))
print(devils_compare(b, a))
