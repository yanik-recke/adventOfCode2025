from pathlib import Path
from dataclasses import dataclass


ranges = [[int(x.split("-")[0]), (int(x.split("-")[1]))] for x in Path("in5.txt").read_text().splitlines()]

total = 0
added = []

def extend(r) -> int:
    if r[0] > r[1]: return 0

    for a in added:
        if r[0] >= a[0] and r[0] <= a[1] and r[1] >= a[1]:
            r[0] = a[1] + 1
            return extend(r)
        elif r[0] < a[0] and r[1] <= a[1] and r[1] >= a[0]:
            r[1] = a[0] - 1
            return extend(r)
        elif r[0] < a[0] and r[1] > a[1]:
            return extend([r[0], a[0] - 1]) + extend([a[1] + 1, r[1]])
        elif (r[0] == a[0] and r[1] == a[1]) or (r[0] >= a[0] and r[1] <= a[1]):
            return 0

    added.append(r)
    return r[1] - r[0] + 1

for r in ranges:
    total += extend(r)

# too hgih: 376531652668485
# too high: 366548846582317
# too high: 352509891817888
print(total)