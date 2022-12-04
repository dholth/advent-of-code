#!/usr/bin/env python
from functools import reduce
from itertools import islice
from pathlib import Path
from typing import Iterable


def priority(letter: str):
    if letter.islower():
        return ord(letter) - ord("a") + 1
    else:
        return ord(letter) - ord("A") + 27


def sacks_halves():
    sacks = Path("03/input").read_text().splitlines()
    for sack in sacks:
        yield sack[: len(sack) // 2]
        yield sack[len(sack) // 2 :]


def sacks_wholes():
    return Path("03/input").read_text().splitlines()


def inboth():
    sacks = Path("03/input").read_text().splitlines()
    for sack in sacks:
        left, right = sack[: len(sack) // 2], sack[len(sack) // 2 :]
        assert len(left) == len(right)
        print(set(left) & set(right))
        yield set(left) & set(right)


def inthree():
    sacks = Path("03/input").read_text().splitlines()
    while sacks:
        a, b, c = (sacks.pop() for _ in range(3))
        yield set(a) & set(b) & set(c)


def inany(sacks: Iterable[set[str]], count=2):
    # doesn't assert len(sacks) is divisible by count
    for group in iter(lambda: list(islice(sacks, 0, count)), []):
        yield reduce(set.intersection, group)


def go():
    print(sum(priority(naughty.pop()) for naughty in inboth()))
    print(sum(priority(three.pop()) for three in inthree()))

    print(
        sum(
            priority(naughty.pop())
            for naughty in inany(set(sack) for sack in sacks_halves())
        )
    )

    print(
        sum(
            priority(naughty.pop())
            for naughty in inany((set(sack) for sack in sacks_wholes()), count=3)
        )
    )


if __name__ == "__main__":
    go()
