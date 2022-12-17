import aocd
import itertools

print(sum(int(line.strip("+")) for line in aocd.lines))

freqy = set()

current = 0
for change in itertools.cycle(int(line.strip("+")) for line in aocd.lines):
    current += change
    if current in freqy:
        print(current)
        break
    freqy.add(current)
