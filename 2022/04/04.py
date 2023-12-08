from pathlib import Path

input = Path(__file__).parents[0] / "04.txt"


class ElfRange:
    def __init__(self, text):
        l, r = text.split("-")
        self.l = int(l)
        self.r = int(r)

    def __contains__(self, other):
        return other.l >= self.l and other.r <= self.r

    def overlaps(self, other):
        return self.l <= other.l <= self.r or self.r >= other.r >= self.l


pairs = [line.split(",") for line in input.read_text().splitlines() if line.strip()]

ranges = [(ElfRange(a), ElfRange(b)) for a, b in pairs]

contains = [(a in b or b in a) for a, b in ranges]

print(sum(contains))

overlaps = [(a.overlaps(b) or b.overlaps(a)) for a, b in ranges]
print(sum(overlaps))
