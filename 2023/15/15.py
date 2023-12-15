#!/usr/bin/env python

import aocd
from collections import defaultdict
import re

"""
So, to find the result of running the HASH algorithm on the string HASH:

    The current value starts at 0.
    The first character is H; its ASCII code is 72.
    The current value increases to 72.
    The current value is multiplied by 17 to become 1224.
    The current value becomes 200 (the remainder of 1224 divided by 256).
    The next character is A; its ASCII code is 65.
    The current value increases to 265.
    The current value is multiplied by 17 to become 4505.
    The current value becomes 153 (the remainder of 4505 divided by 256).
    The next character is S; its ASCII code is 83.
    The current value increases to 236.
    The current value is multiplied by 17 to become 4012.
    The current value becomes 172 (the remainder of 4012 divided by 256).
    The next character is H; its ASCII code is 72.
    The current value increases to 244.
    The current value is multiplied by 17 to become 4148.
    The current value becomes 52 (the remainder of 4148 divided by 256).

So, the result of running the HASH algorithm on the string HASH is 52.
"""


def hash(string):
    """
    The HASH algorithm is a way to turn any string of characters into a single
    number in the range 0 to 255. To run the HASH algorithm on a string, start with
    a current value of 0. Then, for each character in the string starting from the
    beginning:

        Determine the ASCII code for the current character of the string. Increase
        the current value by the ASCII code you just determined. Set the current
        value to itself multiplied by 17. Set the current value to the remainder of
        dividing itself by 256.

    After following these steps for each character in the string in order, the
    current value is the output of the HASH algorithm.
    """
    value = 0
    for byte in string.encode("ascii"):
        # print("byte", byte)
        value += byte
        # print(value)
        value *= 17
        # print("*17", value)
        value = value % 256
        # print("%256", value)
    return value


assert hash("HASH") == 52

initialization_sequence = aocd.data.split(",")

example = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7".split(",")
print(sum(hash(ex) for ex in example))

ans = sum(hash(x) for x in initialization_sequence)
print("Part 1", ans)


def part2(instructions):
    boxes = defaultdict(list)
    for instruction in instructions:
        label, op, value = re.split("([-=])", instruction)
        h = hash(label)
        match op:
            case "-":
                boxes[h] = [(l, v) for l, v in boxes[h] if l != label]
            case "=":
                current = boxes[h]
                for i, (l, v) in enumerate(current):
                    if l == label:
                        current[i] = (label, value)
                        break
                else:
                    current.append((label, value))
    return boxes


def score(boxes):
    """
    At the end of the above example, the focusing power of each lens is as follows:

    rn: 1 (box 0) * 1 (first slot) * 1 (focal length) = 1
    cm: 1 (box 0) * 2 (second slot) * 2 (focal length) = 4
    ot: 4 (box 3) * 1 (first slot) * 7 (focal length) = 28
    ab: 4 (box 3) * 2 (second slot) * 5 (focal length) = 40
    pc: 4 (box 3) * 3 (third slot) * 6 (focal length) = 72
    """
    score = 0
    for k, box in boxes.items():
        for i, (l, v) in enumerate(box, start=1):
            # print(f"Score {l} = {k} * {i} + {v}")
            score += (k + 1) * i * int(v)
    return score


boxes = part2(example)
s = score(boxes)
print(s)

boxes2 = part2(initialization_sequence)
s2 = score(boxes2)
print("Part 2", s2)
