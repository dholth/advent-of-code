import pprint
from pathlib import Path

input = Path(__file__).parents[0] / "05.txt"

def stacks_moves():
    lines = input.read_text().splitlines()
    lines = iter(lines)

    stacks = [[] for _ in range(9)]

    for line in lines:
        if not line:
            break

        for i, element in enumerate(line[1::4]):
            if element != " ":
                stacks[i].append(element)

    for stack in stacks:
        stack.pop()
        stack.reverse()

    pprint.pprint(stacks)

    stacks = [None] + stacks

    def parse_moves():
        for move in lines:
            _, count, _, src, _, dst = move.split()
            count = int(count)
            src = int(src)
            dst = int(dst)
            yield (count, src, dst)

    moves = list(parse_moves())

    return stacks, moves

# part 1

stacks, moves = stacks_moves()

for count, src, dst in moves:
    for _ in range(count):
        stacks[dst].append(stacks[src].pop())

print("".join(stack[-1] for stack in stacks[1:]))

# part 2

stacks, moves = stacks_moves()

for count, src, dst in moves:
    leave = stacks[src][-count:]
    remain = stacks[src][:-count]
    assert len(leave) + len(remain) == len(stacks[src])
    stacks[src] = remain
    stacks[dst].extend(leave)
    # pprint.pprint(stacks)

print("".join(stack[-1] for stack in stacks[1:]))

# part 2 golf

stacks, moves = stacks_moves()

for count, src, dst in moves:
    floor = []
    for _ in range(count):
        floor.append(stacks[src].pop())
    while floor:
        stacks[dst].append(floor.pop())

print("".join(stack[-1] for stack in stacks[1:]))