from pathlib import Path

input = (Path(__file__).parents[0] / "input").read_text()


def marker(input, size=4):
    for i, character in enumerate(input):
        if len(set(input[i - size : i])) == size:
            return i


example = [
    ["mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7, 19],
    ["bvwbjplbgvbhsrlpgdmjqwftvncz", 5, 23],
    ["nppdvjthqldpwncqszvftbrmjlhg", 6, 23],
    ["nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10, 29],
    ["zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11, 26],
]

for data, expected, expected2 in example:
    assert marker(data) == expected
    assert marker(data, 14) == expected2

print(marker(input))

print(marker(input, 14))
