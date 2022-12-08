#!/usr/bin/env python
import aocd
import pprint
import random

# To begin, find all of the directories with a total size of at most 100000,
# then calculate the sum of their total sizes. In the example above, these
# directories are a and e; the sum of their total sizes is 95437 (94853 + 584).
# (As in this example, this process can count files more than once!)

ornaments = """\
👶 Baby
👼 Baby Angel
🎅 Santa Claus
🤶 Mrs. Claus
🧑‍🎄 Mx Claus
🧝 Elf
🧝‍♂️ Man Elf
🧝‍♀️ Woman Elf
👪 Family
🦌 Deer
🍪 Cookie
🥛 Glass of Milk
🍷 Wine Glass
🍴 Fork and Knife
⛪ Church
🌟 Glowing Star
❄️ Snowflake
☃️ Snowman
⛄ Snowman Without Snow
🔥 Fire
🎄 Christmas Tree
🎁 Wrapped Gift
🧦 Socks
🔔 Bell
🎶 Musical Notes
🕯️ Candle
""".splitlines()

example = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
""".splitlines()

visually = """\
- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)
"""

if False:

    def fmt(dir):
        assert dir[0] == "/"
        return "/" + "/".join(dir[1:])

    def attempt(lines):
        dirs = {}
        cwd = []
        for line in lines:
            if line == "$ cd ..":
                cwd.pop()
            elif line.startswith("$ cd "):
                cwd.append(line[5:])
            elif line.split()[0].isnumeric():
                a, b = line.split()
                dirs[tuple(cwd)] = dirs.get(tuple(cwd), []) + [(int(a), b)]
            else:
                print("ignore", line)

        # pprint.pprint(dirs)

        def size(somedir):
            total = 0
            for dir in dirs:
                # "tuple startswith"
                if dir[: len(somedir)] == somedir:
                    # print(fmt(somedir), "contains", fmt(dir))
                    total += sum(size for size, name in dirs[dir])
            return total

        deleteme = 0
        deleted = set()
        for dir in dirs:
            if False and any(dir == x[: len(dir)] for x in deleted):
                print("skip already totaled", dir)
                continue
            totsize = size(dir)
            print(fmt(dir), totsize)
            if totsize <= 100000:
                print("delete", fmt(dir))
                deleted.add(dir)
                deleteme += totsize
            # print("/".join(dir), totsize)

        pprint.pprint(sorted(fmt(x) for x in deleted))

        print("deleteme", deleteme)

        return deleteme

    attempt(example)

    pa = attempt(aocd.lines)

    total = 0
    for line in aocd.lines:
        size = line.split()[0]
        if size.isnumeric():
            total += int(size)

    print("total B", total)

    print("guess", pa)


class ElfDir:
    def __init__(self, name, parent=None):
        self.parent = parent
        self.name = name
        self.files = []
        self.subdirs = []

    def __str__(self, level=1):
        ornament = random.choice(ornaments)[0]
        indent = "  " * level
        files = f"\n{indent}- ".join((f"{size} {name}" for size, name in self.files))
        repr = f"{self.name} (dir) {ornament}"
        if self.files:
            repr += f"\n{indent}- " + files
        if self.subdirs:
            repr += f"\n{indent}- " + f"\n{indent}- ".join(
                subdir.__str__(level=level + 1) for subdir in self.subdirs
            )
        return repr

    def __repr__(self):
        return self.name

    def size(self):
        return sum(subdir.size() for subdir in self.subdirs) + sum(
            f[0] for f in self.files
        )

    def discard(self):
        discarded = 0
        mysize = self.size()
        if self.size() < 100000:
            discarded += mysize
        for subdir in self.subdirs:
            discarded += subdir.discard()
        return discarded

    def discard2(self, sizes):
        sizes.append(self.size())
        for subdir in self.subdirs:
            subdir.discard2(sizes)


def parse_recursive(cwd, lines):
    for line in lines:
        if line == "$ cd ..":
            return
        elif line.startswith("$ cd "):
            newdir = ElfDir(line[5:], parent=cwd)
            cwd.subdirs.append(newdir)
            parse_recursive(newdir, lines)
        elif line.split()[0].isnumeric():
            size, name = line.split()
            cwd.files.append((int(size), name))

    return cwd


lines = iter(example)

exampletree = parse_recursive(ElfDir(""), lines)

print(exampletree)
print(exampletree.size())
print(exampletree.discard())

assert exampletree.size() == 48381165
assert exampletree.discard() == 95437

realtree = parse_recursive(ElfDir(""), iter(aocd.lines))
assert realtree
print(realtree.size())
print(realtree.discard())
# aocd.submit(realtree.discard(), part="a", day=7, year=2022)

total_size = 70000000  # on filesystem
necessary = 30000000
available = total_size - realtree.size()
free_me = necessary - available
all_sizes = []
realtree.discard2(all_sizes)
print(all_sizes)

p2 = min(s for s in all_sizes if s >= free_me)
# aocd.submit(p2, part="b", day=7, year=2022)

print(realtree)
