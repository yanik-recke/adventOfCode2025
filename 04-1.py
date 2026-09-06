from pathlib import Path


# grid[r][c]
# grid = Path("in4.txt").read_text().splitlines()
# h, w = len(grid), len(grid[0])

# grid = {
#     (r, c): ch
#     for r, line in enumerate(Path("in4.txt").read_text().splitlines())
#     for c, ch in enumerate(line)
# }

# for x, y in grid:
    
grid = {
    complex(r,c): ch
    for r, line in enumerate(Path("in4.txt").read_text().splitlines())
    for c, ch in enumerate(line) if ch == "@"
}

DIRS = [1, -1, 1j, -1j, complex(1,1), complex(-1, -1), complex(1, -1), complex(-1, 1)]

total = 0
for p in grid:
    neighbors = [p + d for d in DIRS if p + d in grid and grid[p + d] == "@"]

    if len(neighbors) < 4: total += 1

print(total)

    