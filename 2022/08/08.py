#!/usr/bin/env python
import aocd
import operator
import time
from functools import reduce
from itertools import repeat, chain

example = """\
30373
25512
65332
33549
35390
""".splitlines()

import contextlib


@contextlib.contextmanager
def timeme():
    start = time.time()
    yield
    end = time.time()
    print(end - start)


def identity(fn):
    return fn


def visible(input, reverse=False):
    width = len(input[0])
    height = len(input)

    width_range = range(width)
    height_range = range(height)

    reverser = reversed if reverse else identity

    max_x = [-1] * width
    max_y = [-1] * height

    visibles = set()

    for i in reverser(width_range):  # x
        for j in reverser(height_range):  # y
            height = int(input[j][i])
            print(i, j, f"={height}")
            if height > max_x[i] or height > max_y[j]:
                visibles.add((i, j))

            for arr, index in (max_x, i), (max_y, j):
                arr[index] = max(arr[index], height)

    return visibles


a = visible(example)
print("---")
b = visible(example, reverse=True)

answer = len(a.union(b))
print(answer)

assert answer == 21

with timeme():
    p1 = len(visible(aocd.lines).union(visible(aocd.lines, reverse=True)))
    print("Part 1", p1)


def takewhile_plus(predicate, iterable):
    """
    Also return first failing item.
    """
    for item in iterable:
        yield item
        if not predicate(item):
            break


def scenic_score(input, x, y):
    width = len(input[0])
    height = len(input)

    # given i, j four iterators both alike in dignity going in whatever
    # direction
    candidate_height = int(input[y][x])

    def go_left():
        j = y
        for i in range(x - 1, -1, -1):
            yield int(input[j][i])

    def go_right():
        j = y
        for i in range(x + 1, width):
            yield int(input[j][i])

    def go_up():
        i = x
        for j in range(y - 1, -1, -1):
            yield int(input[j][i])

    def go_down():
        i = x
        for j in range(y + 1, height):
            yield int(input[j][i])

    directions = (go_left, go_right, go_up, go_down)
    scores = [
        len([*takewhile_plus(lambda h: h < candidate_height, direction())])
        for direction in directions
    ]

    return reduce(operator.mul, scores)


scenic_score(example, 2, 3)
scenic_score(example, 2, 1)
scenic_score(example, 0, 3)


def scenic_max(input):
    """
    Scenic scores for all points in input.
    """
    width = len(input[0])
    height = len(input)

    width_range = range(width)
    height_range = range(height)

    for i in width_range:  # x
        for j in height_range:  # y
            yield scenic_score(input, i, j)


print(max(scenic_max(example)))

with timeme():
    print("Part 2", max(scenic_max(aocd.lines)))

# What could be more scenic than code golf


def scenic_iterator(input, x, y):
    width = len(input[0])
    height = len(input)

    # iterate over coordinates from given point to outside
    LEFT_RIGHT_UP_DOWN = [
        (range(x - 1, -1, -1), repeat(y)),
        (range(x + 1, width), repeat(y)),
        (repeat(x), range(y - 1, -1, -1)),
        (repeat(x), range(y + 1, height)),
    ]

    def coords_values(iterator):
        for i, j in iterator:
            yield int(input[j][i])

    directions = (coords_values(zip(*d)) for d in LEFT_RIGHT_UP_DOWN)

    return directions


def scenic_look(input, x, y, end=(99,)):
    # given i, j four iterators both alike in dignity going in whatever
    # direction
    candidate_height = int(input[y][x])

    directions = scenic_iterator(input, x, y)
    scores = [
        [*takewhile_plus(lambda h: h < candidate_height, chain(direction, end))]
        for direction in directions
    ]

    return scores


def scenic_every(input, operation):
    """
    Call operation for all points in input.
    """
    for i in range(len(input[0])):  # x
        for j in range(len(input)):  # y
            yield operation(input, i, j)


def part1(input, i, j):
    return any(view[-1] == 99 for view in scenic_look(input, i, j, end=(99,)))


def part2(input, x, y):
    return reduce(operator.mul, map(len, scenic_look(input, x, y, end=())))


print("Part 2b")

with timeme():
    print("p1", sum(scenic_every(aocd.lines, part1)))

with timeme():
    print("p2", max(scenic_every(aocd.lines, part2)))
