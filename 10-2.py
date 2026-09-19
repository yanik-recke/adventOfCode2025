from pathlib import Path
from dataclasses import dataclass
from z3 import Optimize, Int, Sum, sat


@dataclass
class Instr:
    buttons: list[tuple[int, ...]]
    joltages: list[int]

    def __init__(self, line: str):
        parts = line.split(" ")[1:]
        self.buttons = [eval(x) if len(x) > 3 else eval(x.replace(")", ",)")) for x in parts[:len(parts) - 1]]
        self.joltages = eval(parts[len(parts) - 1].replace("{", "[").replace("}", "]"))

    def __str__(self) -> str:
        return str(self.buttons) + " - " + str(self.joltages)

instrs = [Instr(x) for x in Path("in10.txt").read_text().splitlines()]

result = 0

for instr in instrs:
    target = instr.joltages
    options = instr.buttons

    opt = Optimize()
    x = [Int(f"x{j}") for j in range(len(options))]

    for xj in x:
        opt.add(xj >= 0)

    for i, t in enumerate(target):
        opt.add(Sum([x[j] for j, o in enumerate(options) if i in o]) == t)

    opt.minimize(Sum(x))

    if opt.check() == sat:
        m = opt.model()
        result += sum([m[xj].as_long() for xj in x])
    else:
        print("No solution")

print(result)