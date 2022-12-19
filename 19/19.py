#!/usr/bin/env python

from __future__ import annotations
from typing import Any
import sys
import aocd
import re
import pprint
from functools import partial

try:
    from functools import cache
except:
    from functools import lru_cache

    cache = lru_cache(maxsize=None)


# print(aocd.data)

example = """\
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
"""

BLUEPRINT = r"Blueprint (\d+):"
EACH = r"Each (?P<KIND>\w+) robot costs ((?P<A>\d+) (?P<R>\w+))( and (?P<A2>\d+) (?P<R2>\w+))?\."


def blueprints(lines):
    """
    Yield strings with all text for a particular blueprint.
    """
    bp_id = 0
    accum = []
    lines = iter(lines)
    for line in lines:
        match = re.match(BLUEPRINT, line)
        if match:
            if accum:
                yield bp_id, "".join(accum)
                accum = []
            bp_id = int(match[1])
        accum += [line]
    if accum:
        yield bp_id, "".join(accum)


def parse(lines):
    for i, blueprint in blueprints(lines):
        bp: dict[str, Any] = {}
        m = re.finditer(EACH, blueprint)
        for z in m:
            group = z.groupdict()
            recipe = {group["R"]: int(group["A"])}
            if group["R2"]:
                recipe[group["R2"]] = int(group["A2"])
            bp[group["KIND"]] = recipe
        yield (i, bp)


BLUEPRINTS = []


@cache
def max_spend(b_idx, turn):
    """
    How much can we usefully spend with :turn: remaining turns?
    """
    resources = {}
    blueprint = BLUEPRINTS[b_idx][1]
    for robot, reqs in blueprint.items():
        for req in reqs:
            resources[req] = max(resources.get(req, 0), turn * reqs[req])
    return resources


@cache
def search(
    b_idx: int,
    robots: tuple[str],
    resources: frozenset[tuple[str, int]],
    turns=24,
    choices: tuple = (),
):
    """
    Return how many geodes can be collected in remaining turns.

    Rules:

    Each robot can collect 1 of its resource type per minute. It also takes one
    minute for the robot factory (also conveniently from your pack) to construct
    any type of robot, although it consumes the necessary resources available
    when construction begins.

    So we just have to choose which robot (if any) to construct per turn.
    """
    geodes = 0
    blueprint = BLUEPRINTS[b_idx][1]

    # to calculate which robots we can build
    rdict = dict(resources)
    if choices:
        print(
            f"\nTurns remaining {turns} {24-turns}, resources {rdict}, robots {robots}"
        )

    # maximum we could possibly spend building robots
    overproduction = None
    if not choices:
        overproduction = max_spend(b_idx, turns)

    # resources available in next turn
    rnext = rdict.copy()
    for robot in robots:
        if robot == "geode":
            geodes += 1
        else:
            if overproduction:
                rnext[robot] = min(overproduction[robot], rnext[robot] + 1)
            else:
                rnext[robot] = rnext[robot] + 1

    possibles = []

    if turns:
        # print(f"{turns} Can build nothing")
        if not choices or choices[0] == None:
            possibles.append(
                partial(
                    search,
                    b_idx,
                    robots,
                    frozenset(rnext.items()),
                    turns=turns - 1,
                    choices=choices[1:],
                )
            )
            if choices:
                print(f"Minute {24-turns} end :{robots}: collecting {geodes=} {rnext=}")

        for robot, reqs in blueprint.items():
            # can we build it?
            # include "don't build"
            # print(f"{turns} Try to build {robot}:{reqs} with {rdict}")

            if False or turns == 1 and robot != "geode":
                # non-geode robot can do nothing useful in 1 turn
                # other ways to skip building extra robots?
                continue

            if all(
                rdict.get(resource, 0) >= amount for resource, amount in reqs.items()
            ):
                if choices and choices[0] != robot:
                    continue

                if choices:
                    print(f"{turns} Can build {robot}")

                rnext_rob = rnext.copy()
                for resource, amount in reqs.items():
                    rnext_rob[resource] -= amount
                possibles.append(
                    partial(
                        search,
                        b_idx,
                        tuple(sorted(robots + (robot,))),
                        frozenset(rnext_rob.items()),
                        turns=turns - 1,
                        choices=choices[1:],
                    )
                )
                if choices:
                    print(
                        f"Minute {24-turns} end :{robots}: collecting {geodes=} {rnext_rob=}"
                    )

    else:
        if choices:
            print(f"Minute {24-turns} end :{robots}: collecting {geodes=} {rnext=}")

    if possibles:
        geodes += max(p() for p in possibles)

    return geodes


initial = set((("ore", 0), ("clay", 0), ("obsidian", 0)))


# full input
if sys.argv[1:2] == ["x"]:
    text = example
else:
    print(sys.argv)
    text = aocd.data

BLUEPRINTS = list(parse(text.splitlines()))


def search_all(bp_id, min_turns=1, max_turns=24):
    best = 0
    for turns in range(min_turns, max_turns):
        best = search(bp_id, robots=("ore",), resources=frozenset(initial), turns=turns)

        print(f"{BLUEPRINTS[bp_id][0]}, Turns {turns}", best)

    search.cache_clear()

    return BLUEPRINTS[bp_id][0], best


pprint.pprint(BLUEPRINTS)

if True:
    scores = [(a, b) for a, b in (search_all(n, 23) for n in range(len(BLUEPRINTS)))]
    print(scores)
    print(sum(a * b for a, b in scores))

example_choices = (
    None,  # 1
    None,  # 2
    "clay",  # 3
    None,  # 4
    "clay",  # 5
    None,  # 6
    "clay",  # 7
    None,  # 8
    None,  # 9
    None,  # 10
    "obsidian",  # 11
    "clay",  # 12
    None,  # 13
    None,  # 14
    "obsidian",  # 15
    None,
    None,
    "geode",  # 18
    None,
    None,
    "geode",  # 21
    None,
    None,
    None,
)

# best = search(
#     0, robots=("ore",), resources=frozenset(initial), turns=23, choices=example_choices
# )
# print(best)


# lines = aocd.data.splitlines()

# for line, (idx, recipe) in zip(lines, parse(lines)):
#     print("\n".join(line.split(".")), idx, recipe, "\n")
