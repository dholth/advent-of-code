#!/usr/bin/env python

import aocd
import re
from dataclasses import dataclass, replace

example = """\
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""

OUTPUT = []


@dataclass
class VM:
    a: int = 0
    b: int = 0
    c: int = 0
    instructions: tuple[int, ...] = tuple()
    pc: int = 0

    def combo(self, op):
        if op <= 3:
            return op
        elif op in (4, 5, 6):
            return getattr(self, "abc"[op - 4])
        else:
            raise NotImplementedError(f"combo op {op}")

    def step(self):
        def cbo():
            return self.combo(self.instructions[self.pc + 1])

        def lit():
            return self.instructions[self.pc + 1]

        op = self.instructions[self.pc]
        if op == 0:
            # adv
            self.a = self.a // 2 ** cbo()
        elif op == 1:
            # bxl
            self.b = self.b ^ lit()
        elif op == 2:
            # bst
            self.b = cbo() % 8
        elif op == 3:
            # jnz
            if self.a != 0:
                self.pc = lit()
                return  # don't increment by 2 at end
        elif op == 4:
            # bxc
            self.b = self.b ^ self.c
        elif op == 5:
            # out
            OUTPUT.append(cbo() % 8)
        elif op == 6:
            # bdv
            self.b = self.a // 2 ** cbo()
        elif op == 7:
            # cdv
            self.c = self.a // 2 ** cbo()
        else:
            raise NotImplementedError(f"{self.instructions[self.pc]} @ {self.pc}")

        self.pc += 2

    def dis(self):
        for instruction, op in zip(self.instructions[0::2], self.instructions[1::2]):
            if instruction in (0, 2, 5, 6, 7):
                # interpret combo op
                if op > 3:
                    op = "abc"[op - 4]

            print(
                ["adv", "bxl", "bst", "jnz", "bxc", "out", "bdv", "cdv"][instruction],
                op,
            )

    def run(self):
        OUTPUT.clear()
        while self.pc < len(self.instructions):
            self.step()
        return ",".join(str(o) for o in OUTPUT)


def parse(data):
    a, b, c, *instructions = map(int, re.findall(r"\d+", data))
    return VM(a, b, c, tuple(instructions))


small_examples = """\
If register C contains 9, the program 2,6 would set register B to 1.
If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
If register B contains 29, the program 1,7 would set register B to 26.
If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
""".splitlines()


print(small_examples[0])
ex0 = VM(c=9, instructions=(2, 6))
print(ex0)
ex0.step()
print(ex0)

print()
print(small_examples[1])
ex1 = VM(a=10, instructions=(5, 0, 5, 1, 5, 4))
while ex1.pc < len(ex1.instructions):
    ex1.step()
print(ex1, ",".join(str(o) for o in OUTPUT))

print()
print(small_examples[2])
ex2 = VM(2024, instructions=(0, 1, 5, 4, 3, 0))
print(ex2.run(), ex2)

print()
print(small_examples[3])
ex3 = VM(b=29, instructions=(1, 7))
print(ex3.run(), ex3)

print()
print(small_examples[4])
ex4 = VM(b=2024, c=43690, instructions=(4, 0))
print(ex4.run(), ex4)

print("""
Your first task is to determine what the program is trying to output. To do this, initialize the registers to the given values, then run the given program, collecting any output produced by out instructions. (Always join the values produced by out instructions with commas.) After the above program halts, its final output will be 4,6,3,5,6,3,5,2,1,0.
""")
vm = parse(example)
print(vm)
print(vm.run(), vm)

print("Part 1", parse(aocd.data).run())

vmP = parse(aocd.data)  # the one to keep the same
maxPC = len(vmP.instructions)
lInstructions = list(vmP.instructions)

if False:  #
    # TODO write a VM that operates in reverse?
    for try_a in range(1000000000, 3 * 1000000000):
        vmTry = replace(vmP, a=try_a)
        if try_a % 1000000 == 0:
            print("Try a", try_a, vmTry)

        OUTPUT.clear()

        while lInstructions[: len(OUTPUT)] == OUTPUT and vmTry.pc < maxPC:
            vmTry.step()

        if vmTry.pc >= maxPC and vmTry.instructions == OUTPUT:
            print("Victory at", try_a)

print()
print(vmP)
vmP.dis()

"""
VM(a=62769524, b=0, c=0, instructions=(2, 4, 1, 7, 7, 5, 0, 3, 4, 0, 1, 7, 5, 5, 3, 0), pc=0)
bst a
bxl 7
cdv b
adv 3
bxc 0
bxl 7
out b
jnz 0
"""


def search(aprime):
    for i in range(8):
        aTry = (aprime << 3) + i
        vmTry = replace(vmP, a=aTry)
        vmTry.run()
        if OUTPUT and OUTPUT == lInstructions[-len(OUTPUT) :]:
            print(oct(aTry), OUTPUT)
            if OUTPUT == lInstructions:
                print("Amazing")
                return aTry
            if result := search(aTry):
                return result


print("\nPart 2")
for i in range(1, 8):
    print(i)
    if search(i):
        break
