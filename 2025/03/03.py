#!/usr/bin/env python
"""
Calculate joltage.
"""

import aocd

data = aocd.data.splitlines()


sample = """987654321111111
811111111111119
234234234234278
818181911112111""".splitlines()


def joltage(line):
    values = [int(n) for n in line]
    m = max(values[:-1])
    n = max(values[values.index(m) + 1 :])
    return m * 10 + n


def joltages(lines):
    return sum(joltage(line) for line in lines)


print("Part A", joltages(sample))


def joltage2(values: list[int], place, quiet=True):
    def out(*args):
        pass

    if not quiet:
        out = print

    if place == 0:
        return ()

    seek_in = values[: len(values) - place + 1]
    n = max(seek_in)
    index = seek_in.index(n)
    remain = values[index + 1 :]
    out(
        "P",
        place,
        "N",
        n,
        "<",
        seek_in,
        "|",
        values[index],
        ">Remain",
        remain,
    )
    return (n,) + joltage2(remain, place - 1, quiet=quiet)


def joltages2(lines, quiet=True):
    values = []
    for i, line in enumerate(lines):
        j = joltage2([int(n) for n in line], 12, quiet=quiet)
        assert len(j) == 12
        if not quiet:
            print(f"Joltage {i}, {line}, {j}")
        values.append(int("".join(str(n) for n in j)))
    return values


ex2 = joltages2(sample, quiet=True)

for expected, computed in zip(
    [987654321111, 811111111119, 434234234278, 888911112111], ex2
):
    assert expected == computed, list(zip(str(expected), str(computed)))

print("Example OK")

print("Part B", sum(joltages2(data)))
