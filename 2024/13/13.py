#!/usr/bin/env python

import aocd
import re
import functools

DEBUG = False

example = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""


def parse(data: str):
    groups = data.split("\n\n")
    return (map(int, re.findall("\d+", group)) for group in groups)


def parse_offset(data: str, offset: int):
    for nums in parse(data):
        *nums, a, b = nums
        yield (*nums, a + offset, b + offset)


def search(ax, ay, bx, by, px, py, range_min=0, range_max=100):
    for b in reversed(range(range_min, range_max)):
        if result := search_1(ax, ay, bx, by, px, py, b):
            yield result


def search_1(ax, ay, bx, by, px, py, b):
    if (px - (bx * b)) % ax == 0 and (py - (by * b)) % ay == 0:
        result = {"B": b, "A": ((px - (bx * b)) // ax, (py - (by * b)) // ay)}
        if result["A"][0] > 0 and result["A"][0] == result["A"][1]:
            return result


tokens = 0
correct_part1 = {}
for i, nums in enumerate(parse(aocd.data)):
    for result in search(*nums):
        tokens += result["A"][0] * 3 + result["B"] * 1
        correct_part1[i] = result

print("Part 1", tokens)

part1_answer = tokens

## Part 2

# Add 10000000000000 to the X and Y locations of each prize.
# Unfortunately, it will take many more than 100 presses to win.

PART2_OFFSET = 10000000000000


def do_algebra(bx, by, ax, ay, px, py, a):
    # find b given a but the variable names might be wrong?
    b1 = (py - ay * a) // by
    b2 = (px - ax * a) // bx
    return b1 - b2


for nums in parse(example):
    nums = tuple(nums)
    for result in search(*nums):
        print(result)
        print(do_algebra(*nums, result["A"][0]))

part2 = list(parse_offset(example, offset=PART2_OFFSET))

# Now, it is only possible to win a prize on the second and fourth claw
# machines. Unfortunately, it will take many more than 100 presses to do so.


def guess_bisect(piece, up=True, index=-1):
    guesser = functools.partial(do_algebra, *piece)

    upper_bound = PART2_OFFSET
    lower_bound = 0

    index_str = f"{index} " if index >= 0 else ""

    for _ in range(64):
        guess = lower_bound + (upper_bound - lower_bound) // 2
        result = guesser(guess)
        if abs(result) < 100 and DEBUG:
            print(
                f"{index_str}guess:",
                guess,
                "result:",
                result,
                "range",
                (lower_bound, upper_bound),
            )
        if result == 0:
            print(f"{index_str}Range at 0", (lower_bound, upper_bound), "guess", guess)
            found = list(search(*piece, range_min=lower_bound, range_max=upper_bound))
            if len(found) != 1:
                print(f"{index_str}No solution")
                return None
            return found[0]["B"]

        if up:
            # need to adjust in both directions however
            if result > 0:
                lower_bound = guess
            if result < 0:
                upper_bound = guess

        else:
            if result < 0:
                lower_bound = guess
            if result > 0:
                upper_bound = guess

        if upper_bound == lower_bound:
            break


results = []
for i, piece in enumerate(part2):
    for g in (guess_bisect(piece, True), guess_bisect(piece, False)):
        if g:
            results.append((i, search_1(*piece, g)))

print(results)


def part2_method(offset, compare_with_part1=False):
    results = []
    for i, piece in enumerate(list(parse_offset(aocd.data, offset=offset))):
        # this is not enough information to allow us to guess_bisect once
        # guesser = functools.partial(do_algebra, *piece)
        # polarity = guesser(0) - guesser(1)

        for g in (
            guess_bisect(piece, True, index=i),
            guess_bisect(piece, False, index=i),
        ):
            if g:
                results.append((i, search_1(*piece, g)))

    tokens = 0
    for i, result in results:
        if compare_with_part1:
            correct = correct_part1.get(i)
            if correct != result:
                print(
                    i,
                    "\N{DUCK} Original result",
                    correct_part1.get(i),
                    "Binary guess result",
                    result,
                )
        if result is None:
            continue
        tokens += result["A"][0] * 3 + result["B"] * 1

    return tokens


print("Part 1 with part 2 method", part2_method(0, True))
print("Original answer", part1_answer)
print()
print("Part 2", part2_method(PART2_OFFSET))
