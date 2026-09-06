from pathlib import Path

x = Path("in7.txt").read_text().splitlines()

grid = {
    (col, row): v 
    for row, line in enumerate(x)
    for col, v in enumerate(line) if v == "^" or v == "S"
}

# width and height of input
w = len(x[0])
h = len(x)

def find_start() -> tuple[int, int]:
    for p in grid:
        if grid[p] == "S": return p

    raise Exception("Huhu")

s = find_start()

counter = 0

q = [s]

split = set()
spikes = set()

while len(q) > 0:
    curr = q.pop(0)

    x = curr[0]
    y = curr[1] + 1
    while (x, y) not in grid and y < h:
        split.add((x, y))
        y += 1

    if y == h:
        continue
    else:
        if (x, y) not in spikes:
            spikes.add((x, y))
            counter += 1

    if x - 1 >= 0 and (x - 1, y) not in split and (x - 1,y) not in grid:
        q.append((x - 1, y))
        split.add((x - 1, y))

    if x + 1 < w and (x + 1, y) not in split and (x + 1, y) not in grid:
        q.append((x + 1, y))
        split.add((x + 1, y))

built = {}
built[s] = "S"

for r in range(h):
    row = ""
    for c in range(w):
        if (c, r) in spikes:
            built[(c, r)] = "^"
        elif (c, r) in split:
            built[(c, r)] = "|"

q = [x for x in built if x[1] == h - 2 and built[x] == "|"]

timelines = 0

def rec(curr: tuple[int, int], mem: dict[tuple[int, int], int]) -> int:
    if curr in mem:
        return mem[curr]

    x = curr[0]
    y = curr[1]

    sym = built[curr]
    if sym == "|":
        total = 0
        if (x - 1, y) in built and built[x - 1, y] == "^":
            tmp = rec((x - 1, y), mem)
            mem[(x - 1, y)] = tmp
            total += tmp
        if (x + 1, y) in built and built[x + 1, y] == "^":
            tmp = rec((x + 1, y), mem)
            mem[(x + 1, y)] = tmp
            total += tmp
        if (x, y - 1) in built and (built[x, y - 1] == "|" or built[x, y - 1] == "S"):
            tmp = rec((x, y - 1), mem)
            mem[(x, y - 1)] = tmp
            total += tmp

        return total
    elif sym == "^":
        if (x, y - 1) in built and built[x, y - 1] == "|":
            return rec((x, y - 1), mem)
    elif sym == "S":
        mem[curr] = mem.get(curr, 0) + 1
        return 1

    return 0

mem = {}
for p in q:
    timelines += rec(p, mem)

print(timelines)

# print_grid()

# while len(q) > 0:
#     curr = q.pop(0)
#     x = curr[0]
#     y = curr[1]

#     sym = built[curr]
#     if sym == "|":
#         if (x - 1, y) in built and built[x - 1, y] == "^":
#             q.append((x - 1, y))
#         if (x + 1, y) in built and built[x + 1, y] == "^":
#             q.append((x + 1, y))
#         if (x, y - 1) in built and (built[x, y - 1] == "|" or built[x, y - 1] == "S"):
#             q.append((x, y - 1))
#     elif sym == "^":
#         if (x, y - 1) in built and built[x, y - 1] == "|":
#             q.append((x, y - 1))
#     elif sym == "S":
#         timelines += 1

def print_grid():
    for r in range(h):
        row_tmp = ""
        for c in range(w):
            if (c, r) in spikes:
                row_tmp += "^"
            elif (c, r) in split:
                row_tmp += "|"
            else:
                row_tmp += "."

        print(row_tmp)


