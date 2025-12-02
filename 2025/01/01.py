#!/usr/bin/env python
import math

import aocd

sample = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""

actual = aocd.data
# actual = sample

directions = {"R": 1, "L": -1}


def parse(data):
    return [(n[0], int(n[1:])) for n in data.split()]


def part_a(rotations):
    place = 50
    zeroes = 0

    for d, amt in rotations:
        place = place + directions[d] * amt
        place %= 100
        if place == 0:
            zeroes += 1

    return zeroes


print("A", part_a(parse(data)))


def parse_b(data):
    return [(directions[n[0]] * int(n[1:])) for n in data.split()]


def part_b(rotations):
    place = 50
    zeroes = 0
    for amt in rotations:
        if abs(amt) >= 100:
            zeroes += abs(amt // 100)
            if amt < 0:
                amt_ = -(amt % 100)
            else:
                amt_ = amt % 100
            print(f"Amount {amt} becomes {amt_}")
            amt = amt_
        place = place + amt
        place %= 100
        if place == 0:
            zeroes += 1

    return zeroes


def part_b_simple(rotations):
    place = 50
    zeroes = 0
    for amt in rotations:
        place += amt
        zeroes += abs(place // 100)
        place %= 100
    return zeroes


def part_b_brute(rotations):
    place = 50
    zeroes = 0
    for amt in rotations:
        magnitude = math.copysign(1, amt)
        for _ in range(abs(amt)):
            place += magnitude
            place %= 100
            if place == 0:
                zeroes += 1

    return zeroes


# print("Part B (example)", part_b(parse_b(sample)))

print("Answer B (too low)", part_b(parse_b(data)))

print("B (simple)", part_b_simple(parse_b(data)))

print("B (brute)", part_b_brute(parse_b(data)))
