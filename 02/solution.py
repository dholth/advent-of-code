#!/usr/bin/env python
from pathlib import Path

names = ["rock", "paper", "scissors"]


def go():
    score = 0
    # round 1, fight
    for line in Path("02/input").open():
        parts = line.strip().split()
        a = ord(parts[0]) - ord("A")
        b = ord(parts[1]) - ord("X")

        print(a, b)
        print(names[a], "vs", names[b])
        win = (a + 1) % 3
        lose = (a - 1) % 3
        score += b + 1
        if b == win:
            print("p2 win")
            score += 6
        elif b == lose:
            print("p2 lose")
            score += 0
        else:
            print("draw")
            score += 3

    print("round 1", score)

    score = 0
    # round 2, fight
    for line in Path("02/input").open():
        parts = line.strip().split()
        a = ord(parts[0]) - ord("A")
        b = ord(parts[1]) - ord("X")

        outcomes = ["lose", "draw", "win"]

        print(a, b)
        print(names[a], "get", outcomes[b])
        win = (a + 1) % 3
        lose = (a - 1) % 3

        responses = [lose, a, win]
        b = responses[b]

        score += b + 1
        if b == win:
            print("p2 win")
            score += 6
        elif b == lose:
            print("p2 lose")
            score += 0
        else:
            print("draw")
            score += 3

    print("round 2", score)


if __name__ == "__main__":
    go()
