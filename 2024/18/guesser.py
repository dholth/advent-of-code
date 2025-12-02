#!/usr/bin/env python
"""
Binary search helper.
"""

import sys
import random

TOO_LOW = -1
TOO_HIGH = 1


def cmp(a, b):
    return (a > b) - (b > a)


def guesser(low=0, high=sys.maxsize):
    while low <= high:
        guess = (low + high) // 2
        feedback = yield guess
        if feedback <= TOO_LOW:
            low = guess + 1
        elif feedback >= TOO_HIGH:
            high = guess - 1
        else:
            break


if __name__ == "__main__":
    correct = random.randint(0, sys.maxsize >> 10)

    guess = guesser(high=sys.maxsize >> 10)
    feedback = None
    tries = 0
    while g := guess.send(feedback):
        tries += 1
        feedback = cmp(g, correct)

        print(tries, g, correct)
        if g == correct:
            print("Found in", tries)
            break

    guess = guesser(0, 1024)
    correct = 513
    g = next(guess)
    # inverse feedback won't find; raises StopIteration
    while g != correct:
        g = guess.send(cmp(correct, g))
        print(g, correct)
