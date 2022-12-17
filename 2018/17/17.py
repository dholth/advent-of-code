#!/usr/bin/env python
import sys
import time

sys.setrecursionlimit(10000)

cave = {}

source = 500 + 0j
print(source)

example = """\
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
""".splitlines()

WALL = "🧱"
WATER = "🌊"
FALL = "💧"
GONE = "🐳"
CLEANUP = "🔥"


def parse(lines):
    cave = {}
    for line in lines:
        x, y = (part.split("=")[-1] for part in line.split(", "))
        x = int(x)
        y0, y1 = tuple(map(int, y.split("..")))
        y = range(y0, y1 + 1)
        if line[0] == "x":
            cave.update({(x + (i * 1j)): WALL for i in y})
        else:
            cave.update({(i + (x * 1j)): WALL for i in y})
    return cave


cave = parse(open("input.txt").read().splitlines())

# minimum y in scan is important for answer
ymin = int(min(coord.imag for coord in cave))
ylimit = int(max(coord.imag for coord in cave))
x0 = int(min(coord.real for coord in cave) - 1)
x1 = int(max(coord.real for coord in cave) + 1)

dc = 0


def display(cave, overlay={}, x0=x0, x1=x1, y0=0, y1=ylimit, blank="．"):
    global dc
    dc += 1
    c = dict(cave)
    c.update(overlay)
    for y in range(y0, y1 + 1):
        print("".join(c.get(x + y * 1j, blank) for x in range(x0, x1)))


interest = True

maxcount = 0
ydisplayed = 0


def getwet(coord, step, count=0):
    global interest, maxcount, ydisplayed

    next = coord + step

    if coord.imag >= ylimit:
        cave[coord] = GONE
        return True

    if not cave.get(coord):
        cave[coord] = FALL

        # down
        if not cave.get(next):
            getwet(next, step, count=count + 1)

        cave[coord] = WATER

        if count > maxcount:
            y1 = max(0, int(coord.imag), ydisplayed)
            display(cave, y0=ydisplayed, y1=int(coord.imag))
            ydisplayed = y1
            maxcount = count
            time.sleep(0.01)

        # slide to the left
        if (
            cave.get(coord - 1) not in (WALL, FALL)
            and cave.get(coord + (-1 + 1j)) not in (FALL,)
            and cave.get(coord + 0 + 1j) != GONE
        ):
            # print("left bc", cave.get(coord + (-1)), cave.get(coord + -1 + 1j))
            # if slide != True:
            getwet(coord - 1, 0 + 1j, count=count + 1)
            if cave.get(coord - 1) == GONE:
                cave[coord] = GONE

        # slide to the right
        if (
            cave.get(coord + 1) not in (WALL, FALL)
            and cave.get(coord + (1 + 1j)) not in (FALL,)
            and cave.get(coord + 0 + 1j) != GONE
        ):
            # print("right bc", cave.get(coord + 1), cave.get(coord + (1 + 1j)))
            # if slide != True:
            getwet(coord + 1, 0 + 1j, count=count + 1)
            if cave.get(coord + 1) == GONE:
                cave[coord] = GONE

    # need to settle only if left and right are blocked
    if cave[coord + 1j] == GONE:
        cave[coord] = GONE
        cave[coord + 1j] = CLEANUP

        # cleanup improperly settled water (we took left, returned from right,
        # now revisit left)
        while cave.get(coord - 1) == WATER:
            coord -= 1
            cave[coord] = CLEANUP


print(
    f"Cave is {x0} {x1} by {ylimit} deep. Your console may need to be {(x1-x0) * 2} wide."
)
input("Press Enter")

getwet(source + 0 + 1j, 0 + 1j)

print("🧱" * 100)

if False:
    boring = {WALL: "#", GONE: "|", WATER: "~", FALL: "|"}
    for k in cave:
        cave[k] = boring.get(cave[k], cave[k])
display(cave)


# How many tiles can be reached by the water? To prevent counting forever,
# ignore tiles with a y coordinate smaller than the smallest y coordinate in
# your scan data or larger than the largest one. Any x coordinate is valid. In
# this example, the lowest y coordinate given is 1, and the highest is 13,
# causing the water spring (in row 0) and the water falling off the bottom of
# the render (in rows 14 through infinity) to be ignored.ß

# answer was originally too high (we counted from the source to the end, not
# from the smallest y to the end)

print(sum(cave[k] in (WATER, FALL, GONE, CLEANUP) for k in cave if k.imag >= ymin))

# part 2 (clean up unsettled water) we settle water to the left side of a whale,
# so that will be harder to clean

print(sum(cave[k] in (WATER,) for k in cave if k.imag >= ymin))
