#!/usr/bin/env python

from dataclasses import dataclass

import aocd

example = """\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""

WALL = "#"
BOX = "O"
GRID_CHARACTERS = "#O@[]"
STORM = "><^v"
STORM_EAST, STORM_WEST, STORM_NORTH, STORM_SOUTH = STORM


FILLER = "\N{FULLWIDTH FULL STOP}"
# FILLER = "\N{IDEOGRAPHIC SPACE}"

PRETTY = dict((chr(i), chr(0xFEE0 + i)) for i in range(ord("0"), ord("{")))

PRETTY.update(
    {
        " ": "\N{FULLWIDTH FULL STOP}",
        "#": "🧱",
        ">": "👉",
        "<": "👈",
        "^": "👆",
        "v": "👇",
        "@": "🤖",
        "O": "📦",  # or present
        "[": "＜",  # fullwidth brackets are too close to the edge of their squares
        "]": "＞",
    }
)


dir_num = {1 + 0j: 0, 1j: 1, -1: 2, -1j: 3}
num_dir = {v: k for k, v in dir_num.items()}
# directions: 0 right, 1 down, 2 left, 3 up
# directions: 0 east, 1 south, 2 west, 3 north

# in the order initially considered
compass = {"N": num_dir[3], "S": num_dir[1], "W": num_dir[2], "E": num_dir[0]}
compass_index = {k: i for i, k in enumerate(compass)}
directions = {
    ">": (1 + 0j),
    "<": (-1 + 0j),
    "^": (0 - 1j),
    "v": (0 + 1j),
}

PUSHABLE = "@O[]"
WALL = "#"


@dataclass
class Game:
    grid: dict[complex, str]
    moves: str

    def push(self, coord: complex, direction: complex):
        """
        Find first empty space and shift all in that direction; or find wall and
        don't.
        """
        assert coord in self.grid

        for i in range(100):
            probe = self.grid.get(coord + direction * i)
            if probe is None:
                break
            if probe == WALL:
                return coord
        else:
            raise RecursionError("Lost in space")

        for j in range(i, 0, -1):
            assert coord + direction * j not in self.grid
            self.grid[coord + direction * j] = self.grid.pop(
                coord + direction * (j - 1)
            )

        return coord + direction

    def pushWide(self, coord: complex, direction: complex, debug=False):
        if debug:
            print("Push in ", direction, "from", coord)

        if direction in (1, -1):
            return self.push(coord, direction)

        assert coord in self.grid

        # discover everything we're trying to push
        front = set((coord,))
        pushed = {}
        while front:
            move = front.pop()
            if move in pushed:
                continue

            pushed[move] = self.grid[move]
            probe = self.grid.get(move + direction)
            if probe == WALL:
                # obviates later "not any" pushable check
                return coord
            if probe in (WALL, None):
                continue
            elif probe in "[]":
                # add second half of box
                front.add(move + direction + [-1, 1]["][".index(probe)])
            front.add(move + direction)

        if debug:
            display(
                self.grid, overlay={p: "\N{BANANA}" for p in pushed}, message="Pushing:"
            )

        # now erase pushed and replace it in direction
        pushable = not any(self.grid.get(coord + direction) == WALL for coord in pushed)
        if pushable:
            for move in pushed:
                del self.grid[move]
            for move in pushed:
                self.grid[move + direction] = pushed[move]

            return coord + direction

        return coord

    def score(self):
        """
        The lanternfish use their own custom Goods Positioning System (GPS for
        short) to track the locations of the boxes. The GPS coordinate of a box
        is equal to 100 times its distance from the top edge of the map plus its
        distance from the left edge of the map. (This process does not stop at
        wall tiles; measure all the way to the edges of the map.)

        So, the box shown below has a distance of 1 from the top edge of the map
        and 4 from the left edge of the map, resulting in a GPS coordinate of
        100 * 1 + 4 = 104.

        ...

        This warehouse also uses GPS to locate the boxes. For these larger
        boxes, distances are measured from the edge of the map to the closest
        edge of the box in question. So, the box shown below has a distance of 1
        from the top edge of the map and 5 from the left edge of the map,
        resulting in a GPS coordinate of 100 * 1 + 5 = 105.
        """
        return sum(
            int(k.real + 100 * k.imag) for k, v in self.grid.items() if v in (BOX, "[")
        )


def parse(lines, preprocess=None):
    if isinstance(lines, str):
        lines = lines.splitlines()
    grid = {}

    lines = iter(lines)
    for y, line in enumerate(lines):
        if not line:
            break
        if preprocess:
            line = preprocess(line)
        for x, char in enumerate(line):
            if char in GRID_CHARACTERS:
                grid[x + y * 1j] = char

    return Game(grid=grid, moves="".join(lines))


def display(grid, overlay={}, message=""):
    grid = dict(grid)
    grid.update(overlay)

    if message:
        print(message)

    x0, y0, x1, y1 = 1, 1, 1, 1
    for k in grid:
        x0 = min(x0, k.real)
        x1 = max(x1, k.real)
        y0 = min(y0, k.imag)
        y1 = max(y1, k.imag)
    x0, x1, y0, y1 = map(int, (x0, x1, y0, y1))
    for y in range(y0, y1 + 1):
        print(
            "".join(
                PRETTY.get(
                    grid.get(x + y * 1j, FILLER),
                    grid.get(x + y * 1j, FILLER),
                )
                for x in range(x0, x1 + 1)
            )
        )


def limits(grid):
    x0, y0, x1, y1 = 1, 1, 1, 1
    for k in grid:
        x0 = min(x0, k.real)
        x1 = max(x1, k.real + 1)
        y0 = min(y0, k.imag)
        y1 = max(y1, k.imag + 1)
    x0, x1, y0, y1 = map(int, (x0, x1, y0, y1))
    return x0, x1, y0, y1


def part1(data, debug=False):
    game = parse(data)

    print(game.moves.translate({ord(k): v for k, v in PRETTY.items()}))
    display(game.grid)

    player = next(c for c in game.grid if game.grid[c] == "@")

    for move in game.moves:
        direction = directions[move]
        if debug:
            print("Push in ", direction, move, PRETTY[move], "from", player)
        player = game.push(player, direction)
        if debug:
            display(game.grid)
            input("...")

    score = game.score()
    return score


print("Part 1", part1(aocd.data))

## Part 2, everything except the robot is twice as wide!


def widen(line: str):
    # If the tile is #, the new map contains ## instead.
    # If the tile is O, the new map contains [] instead.
    # If the tile is ., the new map contains .. instead.
    # If the tile is @, the new map contains @. instead.

    return line.translate(
        {ord(k): v for k, v in {"#": "##", "O": "[]", ".": "..", "@": "@."}.items()}
    )


def part2(data, debug=False):
    game = parse(data, preprocess=widen)

    print(game.moves.translate({ord(k): v for k, v in PRETTY.items()}))
    display(game.grid)

    player = next(c for c in game.grid if game.grid[c] == "@")

    for move in game.moves:
        direction = directions[move]
        player = game.pushWide(player, direction, debug=debug)

    score = game.score()
    return score


pushup = """\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<v<^
"""

part2(pushup, debug=True)

print("Part 2 example", part2(example, debug=False))

print("Part 2", part2(aocd.data))
