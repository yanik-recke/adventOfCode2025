from z3 import Solver, Int, Or
from pathlib import Path
from dataclasses import dataclass
from itertools import combinations, product

lines = [l for l in Path("areas.txt").read_text().splitlines()]
areas: list[tuple[int, int, list[int]]] = []

for l in lines: 
    dim, i = l.split(":")
    h, w = map(int, dim.split("x"))
    indeces = list(map(int, i.strip().split(" ")))
    areas.append((h, w, indeces))

# shapes are always 3x3

@dataclass
class Shape:
    h = w = 3
    recs: list[tuple[int, int]]


lines = Path("in12.txt").read_text().splitlines()

shape_idx = -1
rowidx = 0
shapes: list[Shape] = []
coords: list[tuple[int, int]] = []

for l in lines[1:]:
    if ":" in l:
        shapes.append(Shape(coords))
        coords = []
        rowidx = 0
    elif l == "":
        continue
    else:
        for i, c in enumerate(l):
            if c == "#": coords.append((i, rowidx))

        rowidx += 1

shapes.append(Shape(coords))

for area in areas:
    s = Solver()
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

    for sidx, shape in enumerate(ishapes):
        for ridx, (rx, ry) in enumerate(shape.recs):
            s.add(p[sidx][ridx] == (x[sidx] + rx))
            s.add(q[sidx][ridx] == (y[sidx] + ry))
    
    # none of the coordinates must overlap, so if 2,2 is occupied by shape 1
    # shapes 2, ..., i must not have any coordinate that is there
    pairs = list(combinations(range(0, len(ishapes)), 2))

    for li, ri in combinations(range(len(ishapes)), 2):
        for a, b in product(range(len(ishapes[li].recs)), range(len(ishapes[ri].recs))):
            s.add(Or(p[li][a] != p[ri][b], q[li][a] != q[ri][b]))

    # rotation and flipping???
    
