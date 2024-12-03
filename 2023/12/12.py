#!/usr/bin/env python

"""
On the twelvth day of Christmas
"""

import time
import aocd
from rich.console import Console
import re
from functools import cache
from itertools import combinations

console = Console()


def load(lines):
    board = []
    for line in lines:
        springs, numbers = line.split()
        board.append((springs, tuple(map(int, re.findall(r"\d+", numbers)))))

    return board


# Looking for strings of # (damaged) springs separated by . (operational)
# springs, by replacing some ? with # or .
example = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

expected = [1, 4, 1, 1, 4, 10]

REAL_INPUT = False

if REAL_INPUT:
    DATA = aocd.data.splitlines()
else:
    DATA = example.splitlines()

board = load(DATA)

# console.print(board)

if False:
    for line, counts in board:
        line = f".{line}."
        for c in counts:
            for i in range(1, len(line) - 1):
                window = line[i - 1 : i + c + 1]
                replace = "." + "#" * c + "."
                pattern = rf"[\?\.][\?#]{{{c}}}[\?\.]"
                match = re.match(pattern, window)
                print(pattern, window, match)
                if match:
                    proposal = line[0 : i - 1] + replace + line[i + c + 1 :]
                    assert len(proposal) == len(line)
                    print(line, "->", proposal, proposal[i + c :])
            break
        break


def count_possible(line, c, next, level=0, debug=False):
    assert line.startswith(".") and line.endswith(".")
    # try to fit this in #'s and ?'s
    replace = "." + "#" * c + "."
    if debug:
        print("line", line)
    for i in range(len(replace), len(line) - len(replace)):
        window = line[i - len(replace) : i]
        past = line[: i - len(replace)]
        if "#" in past:
            continue

        if debug:
            print("window", window)
            print("past", line[: i - len(replace)])

        # if "#" in line[:i]:
        #     print("Look for", replace, "in", window)
        #     print("reject", i, line[:i])
        #     continue

        pattern = rf"[\?\.][\?#]{{{c}}}[\?\.]"
        match = re.match(pattern, window)
        # print(pattern, window, match)
        if match:
            proposal = line[0 : i - 1].replace("?", ".") + replace + line[i + c + 1 :]
            assert len(proposal) == len(line)
            if debug:
                print("Propose", line, "->", proposal, proposal[i + c :])
            if next:
                for submatch in count_possible(
                    proposal[i + c :], next[0], next[1:], level + 1
                ):
                    yield proposal[: i + c] + submatch
            else:
                yield proposal.replace("?", ".")


@cache
def sliding_window(line, span, next, level=0, debug=False):
    # assert line.startswith(".")
    # try to fit this in #'s and ?'s
    replace = "." + "#" * span
    solutions = 0

    hash_or_question = sum(c in "#?" for c in line)
    necessary_space = sum(next) + len(next) - 1
    if hash_or_question < sum(next) or len(line) < necessary_space:
        return 0

    pattern = re.compile(rf"(^|[\.\?])[\?\.][\?#]{{{span}}}([\.\?]|$)")

    for i in range(len(line) - len(replace)):
        past = line[:i]
        if "#" in past:
            continue

        match = pattern.match(line, i)

        if match:
            proposal = f"{past}{replace}{line[i+len(replace):]}"
            next_line = proposal[i + len(replace) :]
            assert len(proposal) == len(line)
            if debug:
                console.print(
                    f"{' '*(level)}[grey]{past}[/][green]{replace}[/][blue]{line[i+len(replace):]}[/]"
                )
            if next:
                next_level = 0
                if debug:
                    next_level = level + i + len(replace)

                solutions += sliding_window(
                    next_line, next[0], next[1:], next_level, debug=debug
                )
            else:
                solutions += 1

    return solutions

    # if not match and debug:
    #     print("not match", pattern, window)


def doublecheck(line, counts):
    lengths = tuple(len(hashes) for hashes in re.findall("#+", line))
    # if lengths != counts:
    #     print("Reject", counts, line)
    # else:
    #     print("Accept", counts, line)
    return lengths == counts


def non_bruteforce(board, debug=False):
    answer = []
    for i, (line, counts) in enumerate(board):
        solutions = list(
            soln
            for soln in count_possible(f".{line}.", counts[0], counts[1:], debug=debug)
            # if doublecheck(soln, counts)
        )
        # console.print(list(solutions))
        # console.print([len(s) for s in solutions])
        a, b = len(solutions), len(set(solutions))
        if a != b or line == "#??..??#.?#?":
            console.print(len(solutions), len(set(solutions)))
            console.print(line, counts, solutions)
        if debug:
            print("Line", i, len(solutions))
        answer.append(len(solutions))
    return answer


smart_answer = non_bruteforce(board)

# console.print(answer)
# if not REAL_INPUT:
#     assert smart_answer == expected

print("Part 1", sum(smart_answer))


# if REAL_INPUT:
#     aocd.submit(sum(answer), part=1)


def bruteforce(line, counts):
    line = bytearray(line.encode("utf-8"))
    existing_hashes = sum(len(hashes) for hashes in re.findall(b"#+", line))
    new_hashes = sum(counts) - existing_hashes
    questions = list(i for i, c in enumerate(line) if c == ord("?"))
    for i in range(2 ** len(questions)):
        bit_count = i.bit_count()
        if bit_count != new_hashes:
            continue

        for bit, q in enumerate(questions):
            line[q] = b".#"[bool(i & 1 << bit)]

        lengths = tuple(len(hashes) for hashes in re.findall(b"#+", line))
        if lengths == counts:
            yield line.decode("ascii")


# about 2/3rds the time of bruteforce1
def bruteforce2(line, counts):
    line = bytearray(line.encode("utf-8"))
    existing_hashes = sum(len(hashes) for hashes in re.findall(b"#+", line))
    new_hashes = sum(counts) - existing_hashes
    questions = list(i for i, c in enumerate(line) if c == ord("?"))
    for combo in combinations(questions, new_hashes):
        combo = set(combo)
        for q in questions:
            line[q] = b".#"[q in combo]

        lengths = tuple(len(hashes) for hashes in re.findall(b"#+", line))
        if lengths == counts:
            yield line.decode("ascii")


start = time.time()
answer = []
if True:
    for line, counts in board:
        # print(sum(s == "?" for s in line))
        # print("Found a solution", "From", line, "To", bruteforce(line, counts))
        answer.append(len(list(s for s in bruteforce(line, counts))))
        # print(answer[-1], line)

# if REAL_INPUT:
#     aocd.submit(sum(answer), part=1)
end = time.time()

print("Part 1 Bruteforce", sum(answer), end - start)
start = time.time()
answer = []
if True:
    for line, counts in board:
        # print(sum(s == "?" for s in line))
        # print("Found a solution", "From", line, "To", bruteforce(line, counts))
        answer.append(len(list(s for s in bruteforce2(line, counts))))
        # print(answer[-1], line)
end = time.time()
print("Part 1 Bruteforce2", sum(answer), end - start)
print("Part 1 Not Bruteforce", sum(smart_answer))

# Number five is alive
"""
As you look out at the field of springs, you feel like there are way more
springs than the condition records list. When you examine the records, you
discover that they were actually folded up this whole time!

To unfold the records, on each row, replace the list of spring conditions with
five copies of itself (separated by ?) and replace the list of contiguous groups
of damaged springs with five copies of itself (separated by ,).

So, this row:

.# 1

Would become:

.#?.#?.#?.#?.# 1,1,1,1,1

The first line of the above example would become:

???.###????.###????.###????.###????.### 1,1,3,1,1,3,1,1,3,1,1,3,1,1,3
"""

fiveboard = [("?".join([line] * 5), counts * 5) for line, counts in board]

# console.print(fiveboard)

print("\nPart 2")
# smart_answer2 = sliding_window(fiveboard[0:1], debug=True)
# console.print(smart_answer2)

print("Part 1")
# for i, (line, counts) in enumerate(board):
#     console.print(
#         "Ans",
#         i,
#         line,
#         counts,
#         sliding_window(f".{line}.", counts[0], counts[1:], debug=False)
#         # len(
#         #     list(
#         #         soln
#         #         for soln in sliding_window(
#         #             f".{line}.", counts[0], counts[1:], debug=False
#         #         )
#         #     )
#         # ),
#     )

print("\nPart 2")
if not REAL_INPUT:
    assert fiveboard[0][0] == "???.###????.###????.###????.###????.###", fiveboard[0][0]


def count_iter(i):
    result = 0
    for x in i:
        result += 1
    return result


answers = []
for i, (line, counts) in enumerate(board):
    # console.print("Q", line, counts)
    answers.append(sliding_window(f".{line}.", counts[0], counts[1:], debug=False))
    # console.print("Ans", i, line, counts, answers[-1])

console.print("Part 1 sliding window sum", sum(answers))
print("Part 1 Not Bruteforce", sum(smart_answer))
if REAL_INPUT:
    if sum(answers) != 7541:
        console.print("[red]!= 7541[/]")

if False:
    answers = []
    for i, (line, counts) in enumerate(fiveboard):
        # console.print("Q", line, counts)
        no_double_dots = re.sub(r"\.+", ".", f".{line}.")
        answers.append(
            sliding_window(no_double_dots, counts[0], counts[1:], debug=False)
        )
        # console.print(count_iter(bruteforce2(line, counts)))
        console.print("Ans", i, answers[-1], no_double_dots)

    console.print("Sum", sum(answers))

    if REAL_INPUT:
        aocd.submit(sum(answers), part=2)
    else:
        assert sum(answers) == 525152
        print("Correct on sample input")

""" 1,1,3 repeat
???.###????.###????.###????.###????.###
#.#.###
"""


@cache
def sliding2(line: str, next, debug=False):
    """
    This time, respect boundaries...

    Count anything where "past" has no #'s
    """
    if not next:
        return int(not "#" in line)
    span = next[0]
    solutions = 0
    replace = "#" * span
    if debug:
        console.print(span, next)
    for i in range(len(line)):
        past = line[:i]
        if "#" in past:
            break
        window = line[i : i + span]
        future = line[i + span :]
        if future and future[0] not in ("?."):
            continue
        if debug:
            console.print(f"{past}[blue]{window}[/]{future}")
            proposed = f"{'.'*i}[green]{replace}[/].{future[1:]}"
            console.print(proposed)
        next_part = future[1:].lstrip(".")
        solutions += sliding2(next_part, next[1:])
        if debug:
            console.print()
    return solutions


example2 = [1, 16384, 1, 16, 2500, 506250]

line, count = fiveboard[0]
print("Part 2, nth try")
console.print(line)
for expected, (line, count) in zip(example2, fiveboard):
    line = re.sub(r"\.+", ".", line).strip(".")
    ans = sliding2(line, count)
    print(f"{ans:8} {ans==expected}\t", line)
