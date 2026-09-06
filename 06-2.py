from pathlib import Path
from dataclasses import dataclass
from math import prod

lines = [l for l in Path("in6.txt").read_text().splitlines()]

@dataclass
class Problem:
    numbers: list[str]
    op: str

problems: dict[int, Problem] = {}

problems_idx = 0
c = len(lines[0]) - 1

while c >= 0:
    only_spaces = True
    num, op, r = "", "", 0

    while r < len(lines):
        if lines[r][c] == "*" or lines[r][c] == "+":
            op = lines[r][c]
            only_spaces = False
        elif lines[r][c] == " ":
            num += " "
        else:
            num += lines[r][c]
            only_spaces = False

        r += 1

    if only_spaces:
        problems_idx += 1
    else:
        if problems_idx not in problems:
            problems[problems_idx] = Problem([], op)

        if op != "":
            problems[problems_idx].op = op

        problems[problems_idx].numbers.append(num)
        
    c -= 1

result = 0

for i in problems:
    p = problems[i]
    nums = [int(x) for x in p.numbers]
    result += prod(nums) if p.op == "*" else sum(nums)

print(result)
