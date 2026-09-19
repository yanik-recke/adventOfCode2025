from pathlib import Path
reds = [tuple(map(int, x.split(","))) for x in Path("in9.txt").read_text().splitlines()]
reds.append(reds[0])

edges: list[tuple[tuple[int, int], tuple[int, int]]] = []

for idx, _ in enumerate(reds):
    if idx + 1 < len(reds): 
        edges.append(((reds[idx][0], reds[idx][1]), (reds[idx + 1][0], reds[idx + 1][1])))

def edge_enters_interior(e: tuple[tuple[int, int], tuple[int, int]], minx, maxx, miny, maxy) -> bool:

    # vertical edge
    if e[0][0] == e[1][0]:
        x = e[0][0]
        lowery = min(e[0][1], e[1][1])
        highery = max(e[0][1], e[1][1])

        if lowery == miny and highery == maxy and x == minx and x == maxx: return False

        if minx < x and x < maxx:
            if lowery <= miny and highery > miny:
                return True

            if lowery >= miny and lowery < maxy and highery > maxy:
                return True

            if lowery >= miny and lowery <= maxy and highery > miny and highery <= maxy:
                return True
            
    # horizontal edge
    else:
        y = e[0][1]
        lowerx = min(e[0][0], e[1][0])
        higherx = max(e[0][0], e[1][0])

        if lowerx == minx and higherx == maxx and y == miny and y == maxy: return False

        if miny < y and y < maxy:
            if lowerx <= minx and higherx > minx:
                return True

            if lowerx >= minx and lowerx < maxx and higherx > maxx:
                return True

            if lowerx >= minx and lowerx <= maxx and higherx > minx and higherx <= maxx:
                return True

    return False

largest = -1

for p0 in reds:
    for p1 in reds:
        if p0 != p1 and largest < ((abs(p0[0] - p1[0]) + 1) * (abs(p0[1] - p1[1]) + 1)):
            minx = min(p0[0], p1[0])
            maxx = max(p0[0], p1[0])
            miny = min(p0[1], p1[1])
            maxy = max(p0[1], p1[1])

            valid = True
            for e in edges:
                if edge_enters_interior(e, minx, maxx, miny, maxy):
                    valid = False
                    break

            if valid:
                largest = max(largest, (maxx - minx + 1) * (maxy - miny + 1))

# wrong: 2507949948
print(largest)
