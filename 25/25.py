#!/usr/bin/env python

import aocd

example = """\
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
""".splitlines()

examples = """\
        1              1
        2              2
        3             1=
        4             1-
        5             10
        6             11
        7             12
        8             2=
        9             2-
       10             20
       15            1=0
       20            1-0
     2022         1=11-2
    12345        1-0---0
314159265  1121-1110-1=0
""".splitlines()


def parsnafu(line):
    value = 0
    for i, sym in enumerate(reversed(line)):
        # print(i, sym, 5**i)
        place = 5**i
        if sym in "012":
            value += place * int(sym)
        elif sym == "-":
            value -= place
        elif sym == "=":
            value -= 2 * place
    return value


s0 = sum(parsnafu(line) for line in example)
assert s0 == 4890
s = sum(parsnafu(line) for line in aocd.lines)

print(s0, s)


def fivits(num, base=5):
    def div():
        nonlocal num
        while num:
            yield num % base
            num //= base

    return tuple(reversed(tuple(div())))


def snaprint(diggy):
    result = []
    # diggy: base 5 digits (normal)
    carry = 0
    for num in reversed(diggy):
        num += carry
        carry = 0
        while num > 2:
            carry += 1
            num -= 5
        if num in (0, 1, 2):
            result += str(num)
        elif num in (-1, -2):
            result += {-1: "-", -2: "="}[num]
        else:
            raise ValueError()
    # deal with last carry
    if carry == 0:
        pass
    elif carry >= 5:
        result += reversed(snaprint(fivits(carry)))
    elif carry <= 2:
        result += str(carry)
    elif carry == 3:
        result += ["-", "1"]
    elif carry == 4:
        result += ["=", "1"]
    else:
        raise ValueError(carry)

    result.reverse()
    return result


for n, expected in (l.split() for l in examples):
    n = int(n)
    assert parsnafu(expected) == n
    result = "".join(snaprint(fivits(int(n))))
    print(
        expected == result,
        n,
        expected,
        result,
    )

print("Reparse")

print("".join(snaprint(fivits(s))))
