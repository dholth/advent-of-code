#!/usr/bin/env python

import pprint
from collections import Counter
from enum import Enum
from pathlib import Path

DEBUG = False

INPUT = (Path(__file__).parent / "input.txt").read_text().splitlines()
SAMPLE = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""".splitlines()

# for hand, bid in (line.split() for line in INPUT):
#     print(hand, bid, Counter(hand))

CARD_STRENGTH = "AKQJT98765432"
CARD_LEX = {k: -v for v, k in enumerate(CARD_STRENGTH)}
CARD_STRENGTH_JOKER = "AKQT98765432J"
CARD_JOKE = {k: -v for v, k in enumerate(CARD_STRENGTH_JOKER)}


class Hand(Enum):
    FIVE = 7
    FOUR = 6
    FULL = 5
    THREE = 4
    PAIR2 = 3
    PAIR1 = 2
    HIGH = 1


def rank(hand, joker=False):
    """
    Every hand is exactly one type. From strongest to weakest, they are:

    7 Five of a kind, where all five cards have the same label: AAAAA
    6 Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    5 Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    4 Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    3 Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    2 One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    1 High card, where all cards' labels are distinct: 23456

    Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.
    """
    counter = Counter(hand)
    counts = counter.most_common()

    # incorrect method
    # if joker and "J" in hand:
    #     jokers = counter.pop("J")
    #     counter += Counter({counts[0][0]:jokers})
    #     counts = counter.most_common()

    if DEBUG:
        print(len(counts), counts)

    if len(counts) == 1:
        return Hand.FIVE
    elif len(counts) == 2:
        if counts[0][1] == 4:
            return Hand.FOUR
        elif counts[0][1] == 3:
            return Hand.FULL
        assert False
    elif len(counts) == 3:
        if counts[0][1] == 3:
            return Hand.THREE
        elif counts[0][1] == 2 and counts[1][1] == 2:
            return Hand.PAIR2
        assert False
    elif len(counts) == 4:
        return Hand.PAIR1
    elif len(counts) == 5:
        return Hand.HIGH

    assert False, "Should not get here"


def jokerank(hand):
    if "J" in hand:
        return max(rank(hand.replace("J", letter)).value for letter in set(hand))
    return rank(hand).value


splits = (line.split() for line in SAMPLE)

hand, bid = next(splits)
print(hand, rank(hand))

hand, bid = next(splits)
print(hand, rank(hand))

hand, bid = next(splits)
print(hand, rank(hand))

hand, bid = next(splits)
print(hand, rank(hand))

hand, bid = next(splits)
print(hand, rank(hand))

print(rank("ABCDE"))

# Example hands
assert rank("AAAAA") == Hand.FIVE
assert rank("AA8AA") == Hand.FOUR
assert rank("23332") == Hand.FULL
assert rank("TTT98") == Hand.THREE
assert rank("23432") == Hand.PAIR2
assert rank("A23A4") == Hand.PAIR1
assert rank("23456") == Hand.HIGH

print("\nPart 1")

decorated = sorted(
    [
        (rank(hand).value, tuple(CARD_LEX[c] for c in hand), hand, bid)
        for hand, bid in (line.split() for line in INPUT)
    ]
)


if DEBUG:
    pprint.pprint(decorated)

# pprint.pprint([(r, d) for r, d in enumerate(decorated, start=1)])
answer = sum((r * int(d[-1])) for r, d in enumerate(decorated, start=1))
print("Answer A", answer)


decorated = sorted(
    [
        (rank(hand, joker=True).value, tuple(CARD_JOKE[c] for c in hand), hand, bid)
        for hand, bid in (line.split() for line in SAMPLE)
    ]
)

# pprint.pprint(decorated)

# pprint.pprint([(r, d) for r, d in enumerate(decorated, start=1)])
answer = sum((r * int(d[-1])) for r, d in enumerate(decorated, start=1))
print("Sample B", answer)


decorated = sorted(
    [
        (jokerank(hand), tuple(CARD_JOKE[c] for c in hand), hand, bid)
        for hand, bid in (line.split() for line in INPUT)
    ]
)

answer = sum((r * int(d[-1])) for r, d in enumerate(decorated, start=1))
print("Answer B", answer)

print(CARD_JOKE)

# 1st wrong answer 251117811
