from z3 import Solver, Int, Or, And, sat
from pathlib import Path
from dataclasses import dataclass
from itertools import combinations, product, batched

@dataclass
class Shape:
    h = w = 3
    recs: list[tuple[int, int]]

areas: list[tuple[tuple[int, ...], list[int]]] = [(tuple(map(int, l.split(":")[0].split("x"))), list(map(int, l.split(":")[1].strip().split(" ")))) for l in Path("areas.txt").read_text().splitlines()]
shapes: list[Shape] = [Shape([(j, i) for j, c in enumerate(l) for _, x in enumerate(c) if x == "#"]) for i, l in enumerate(batched([l for l in Path("in12.txt").read_text().splitlines() if l != "" and ":" not in l], 3))]

fits = 0
for area in areas:
    if (sum(area[1]) * 9) <= area[0][0] * area[0][1]: fits += 1

to_calc = [area for area in areas if sum(len(shapes[idx].recs) * rec for idx, rec in enumerate(area[1])) < area[0][0] * area[0][1] and not ((sum(area[1]) * 9) <= area[0][0] * area[0][1])]

print(len(to_calc)) # = 0, proof that no further calulcations are needed
print(fits)

exit(0)

areas = to_calc

# turns out the solver was not needed, I am leaving it here anyways because it 
# was a lot of work
for area in areas:
    s = Solver()
    s.set("timeout", 10000)
    h_area, w_area = area[0], area[1]
    indeces = area[2]

    ishapes: list[Shape] = []

    for idx, c in enumerate(indeces):
        for _ in range(0, c):
            ishapes.append(shapes[idx])

    # shape coordinates are top-left corner of each rectangle, this will not work with any input
    # top row and left most row must have at least one # in each shape so this works
    # for 2 shapes this would give x1, x2, y1 and y2 where (x1, y1) and (x2, y2) represent
    # the coordinates for the top left corner of the rectangle
    x = [Int(f"x_{i}") for i in range(len(ishapes))]
    y = [Int(f"y_{i}") for i in range(len(ishapes))]

    # the shapes must be placed inside the defined area
    # all shapes are 3x3, since the coordinates from above 
    # are for the top left corner they have to be >= 0 and +3 must
    # not be larger than the area's limits (w_area, h_area)
    for i, _ in enumerate(ishapes):
        s.add(x[i] >= 0, x[i] + 3 <= w_area)
        s.add(y[i] >= 0, y[i] + 3 <= h_area)

    # for each shape its other coordinates need to be set dependent on
    # the coordinate of the top-left corner
    # that they do not exceed the area's boundaries is ensured by the constraints above
    # each shape has coordinates following the schema: (p11, q11), p(12, q12), etc. with the first 
    # number being the index of the shape and the second number being the index of the coordinate of the shape
    p = [[Int(f"p_{i}{j}") for j in range(len(ishapes[i].recs))] for i in range(len(ishapes))]
    q = [[Int(f"q_{i}{j}") for j in range(len(ishapes[i].recs))] for i in range(len(ishapes))]

    for i, _ in enumerate(ishapes):
        for j, _ in enumerate(p[i]):
            s.add(p[i][j] >= 0, p[i][j] <= w_area)

        for j, _ in enumerate(q[i]):
            s.add(q[i][j] >= 0, q[i][j] <= h_area)
    
    # for sidx, shape in enumerate(ishapes):
    #     for ridx, (rx, ry) in enumerate(shape.recs):
    #         s.add(p[sidx][ridx] == (x[sidx] + rx))
    #         s.add(q[sidx][ridx] == (y[sidx] + ry))

    # rotation and flipping???
    rotation_cheat_sheet_90 = {
        (0,0): (2,0),
        (1,0): (2,1),
        (2,0): (2,2),
        (0,1): (1,0),
        (1,1): (1,1),
        (2,1): (1,2),
        (0,2): (0,0),
        (1,2): (0,1),
        (2,2): (0,2), 
    }

    def rotate(d: int, p: tuple[int, int]) -> tuple[int, int]:
        if d == 90:
            return rotation_cheat_sheet_90[p]
        elif d == 180:
            return rotation_cheat_sheet_90[rotation_cheat_sheet_90[p]]
        elif d == 270:
            return rotation_cheat_sheet_90[rotation_cheat_sheet_90[rotation_cheat_sheet_90[p]]]

        raise Exception("Call only with 90, 180 or 270")

    for sidx, _ in enumerate(ishapes):
        # for x (p)
        s.add(Or(
                    And([(p[sidx][i] == (x[sidx] + ishapes[sidx].recs[i][0])) for i in range(len(ishapes[sidx].recs))] + [(q[sidx][i] == (y[sidx] + ishapes[sidx].recs[i][1])) for i in range(len(ishapes[sidx].recs))]),
                    And([(p[sidx][i] == (x[sidx] + rotate(90, ishapes[sidx].recs[i])[0])) for i in range(len(ishapes[sidx].recs))] + [(q[sidx][i] == (y[sidx] + rotate(90, ishapes[sidx].recs[i])[1])) for i in range(len(ishapes[sidx].recs))]),
                    And([(p[sidx][i] == (x[sidx] + rotate(180, ishapes[sidx].recs[i])[0])) for i in range(len(ishapes[sidx].recs))] + [(q[sidx][i] == (y[sidx] + rotate(180, ishapes[sidx].recs[i])[1])) for i in range(len(ishapes[sidx].recs))]),
                    And([(p[sidx][i] == (x[sidx] + rotate(270, ishapes[sidx].recs[i])[0])) for i in range(len(ishapes[sidx].recs))] + [(q[sidx][i] == (y[sidx] + rotate(270, ishapes[sidx].recs[i])[1])) for i in range(len(ishapes[sidx].recs))])
                )
            )
    
    # none of the coordinates must overlap, so if 2,2 is occupied by shape 1
    # shapes 2, ..., i must not have any coordinate that is there
    pairs = list(combinations(range(0, len(ishapes)), 2))

    for li, ri in combinations(range(len(ishapes)), 2):
        for a, b in product(range(len(ishapes[li].recs)), range(len(ishapes[ri].recs))):
            s.add(Or(p[li][a] != p[ri][b], q[li][a] != q[ri][b]))

    if s.check() == sat:
        fits += 1
        m = s.model()
        print("Yippie")
        for i in range(len(ishapes)):
            print(
                f"Rect {i}: x={m[x[i]]}, y={m[y[i]]}"
            )
    else:
        print("No valid packing found.")