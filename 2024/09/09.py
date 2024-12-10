#!/usr/bin/env python

import aocd
import time
from itertools import groupby


def parse(data: str):
    return [*map(int, data)]


def expand(data: list[int]):
    for i, blocks in enumerate(data):
        if i % 2:
            yield from [-1] * blocks
        else:
            yield from [i // 2] * blocks


def checksum(blocks):
    return sum(i * block for i, block in enumerate(blocks) if block >= 0)


example = "2333133121414131402"

disk = parse(example)

print(example)
print(list(expand(disk)))


def take_from_end(disk):
    backwards = reversed(list(enumerate(disk)))
    for i, block in backwards:
        if block >= 0:
            yield i, block


def compact(disk):
    end = take_from_end(disk)
    for i, block in enumerate(disk):
        if block < 0:
            j, block2 = next(end)
            if j < i:
                break
            disk[i] = block2
            disk[j] = -1


disk = list(expand(disk))

print()
print("Initial", disk)
print()

print(list(take_from_end(disk)))

compact(disk)

print()
print(disk)

expected = list(map(int, "0099811188827773336446555566"))

assert disk[: len(expected)] == expected
print("Matches example")

print("Example checksum", checksum(disk))

print("The real thing", len(aocd.data))

disk = list(expand(parse(aocd.data)))
print("Length", len(disk))
begin = time.time_ns()
compact(disk)
end = time.time_ns()
print("Took", (end - begin) / 1e9, len(disk))

print("Part 1", checksum(disk))


## Part 2


def spans(disk: list[int], key=lambda item: item[1] == -1):
    """
    Generate (index, length) tuple of runs of -1 in disk.
    """
    return (
        (next(g)[0], 1 + len(list(g))) for k, g in groupby(enumerate(disk), key) if k
    )


def freelist(disk: list[int]):
    return spans(disk)


def usedlist(disk: list[int]):
    for index, value in spans(disk, key=lambda item: item[1]):
        if disk[index] != -1:
            yield index, value


def compact2(disk):
    for i, length in reversed(list(usedlist(disk))):
        for j, available in freelist(disk):
            if j > i:
                break
            if available >= length:
                disk[j : j + length] = disk[i : i + length]
                disk[i : i + length] = [-1] * length
                break


disk2 = list(expand(parse(example)))

print(example)
print(disk2)

print(list(freelist(disk2)))
print(list(usedlist(disk2)))

compact2(disk2)
print(disk2)
print(checksum(disk2))

if False:
    disk3 = list(expand(parse(aocd.data)))
    begin = time.time_ns()
    compact2(disk3)
    end = time.time_ns()
    ans2 = checksum(disk3)
    print(f"{ans2} in {(end-begin)/1e9:.2f}s")


def compact4(disk):
    free = list(freelist(disk))
    for i, length in reversed(list(usedlist(disk))):
        # print(disk)
        # print(free)
        # input()
        for ij, (j, available) in enumerate(free):
            if j > i:
                break
            if available >= length:
                disk[j : j + length] = disk[i : i + length]
                disk[i : i + length] = [-1] * length

                remains = (j + length, available - length)
                if remains[1]:
                    free[ij] = remains
                else:
                    del free[ij]
                break

    return disk


print()
compact4(list(expand(parse(example))))

print("\ncompact4() on full data")
begin = time.time_ns()
print(checksum(compact4(list(expand(parse(aocd.data))))), end="")
end = time.time_ns()
print(f" in {(end-begin)/1e9:.2f}s")
