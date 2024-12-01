#!/usr/bin/env python
from collections import Counter

import aocd

from aocd import data

numbers = [
    [int(n) for n in line.split()]
    for line in data.splitlines()
]

left, right = list(zip(*numbers))

ans = sum(abs(l - r) for l, r in zip(sorted(left), sorted(right)))

print(ans)

frequency = Counter(right)

ans2 = sum(n*frequency.get(n, 0) for n in left)

print(ans2)
