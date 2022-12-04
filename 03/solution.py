#!/usr/bin/env python
from pathlib import Path


def priority(letter: str):
    if letter.islower():
        return ord(letter) - ord("a") + 1
    else:
        return ord(letter) - ord("A") + 27


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
        a, b, c, *sacks = sacks
        yield set(a) & set(b) & set(c)


def go():
    print(sum(priority(naughty.pop()) for naughty in inboth()))
    print(sum(priority(three.pop()) for three in inthree()))


if __name__ == "__main__":
    go()
