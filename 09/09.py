import aocd
import operator
from operator import add

example = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
""".splitlines()

#     U
# <- L R ->
#     D
directions = {"R": (1, 0), "L": (-1, 0), "U": (0, -1), "D": (0, 1)}


def parse(lines):
    for line in lines:
        d, c = line.split()
        yield d, int(c)


print([*parse(example)])

# head, tail
rope = [(0, 0), (0, 0)]


def display(rope, width=20, height=20):
    # (0, 0) in bottom left
    row = ["."] * width
    grid = [row.copy() for _ in range(height)]
    grid[0 + 5][0 + 5] = "+"
    print(rope)
    for i, (x, y) in enumerate(rope):
        grid[y + 5][x + 5] = str(i)
    return "\n".join(reversed(list("".join(row) for row in grid)))


print(display(rope))


def follow(head, tail):
    # return new tail position
    distance = tuple(map(operator.sub, head, tail))
    if max(abs(d) for d in distance) < 2:
        return tail
    if distance[0] == 0:
        tail = tail[0], tail[1] + distance[1] // abs(distance[1])
    elif distance[1] == 0:
        tail = tail[0] + distance[0] // abs(distance[0]), tail[1]
    else:
        tail = tail[0] + distance[0] // abs(distance[0]), tail[1] + distance[1] // abs(
            distance[1]
        )
    return tail


def dragaround(lines):
    history = []
    for d, count in parse(lines):
        for _ in range(count):
            rope[0] = tuple(map(add, rope[0], directions[d]))
            for i in range(1, len(rope)):
                rope[i] = follow(rope[i - 1], rope[i])
            history.append(rope[-1])
            # print(display(rope))
        #     print("\N{RIGHTWARDS ARROW}")
        # print("\N{LEFTWARDS ARROW}")
    return history


assert len(set(dragaround(example))) == 13

rope = [(0, 0)] * 2
print(len(set(dragaround(aocd.lines))))

rope = [(0, 0)] * 10
print(len(set(dragaround(aocd.lines))))
