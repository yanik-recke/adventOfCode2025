import math
from sortedcontainers import SortedKeyList
from dataclasses import dataclass

@dataclass
class Point:
    xyz: tuple[int, int, int]
    index: int

    def __eq__(self, value):
        if isinstance(value, Point):
            return self.xyz == value.xyz and self.index == value.index
        else:
            return False

    def __hash__(self):
        x, y, z = self.xyz
        return ((x * 73856093) ^ (y * 19349663) ^ (z * 83492791))

    def __str__(self):
        x, y, z = self.xyz
        index = self.index
        return "(" + str(x) + ", " +  str(y) + ", " + str(z) + ", index = " + str(index) + ")"

def key(x: tuple[int, Point, Point]) -> int:
    return x[0]

all_points = []

with open("in8.txt", "r") as f:
    index = 0
    for line in f:
        s = line.split(",")
        all_points.append(Point((int(s[0]), int(s[1]), int(s[2])), int(index)))
        index += 1

visited = set()
ordered = SortedKeyList(key=key)

for p in all_points:
    for j in all_points: 
        if p.index != j.index and not (p.index,j.index) in visited and not (j.index, p.index) in visited:
            visited.add((p.index, j.index))
            distance = math.dist(p.xyz, j.xyz)
            ordered.add((distance, p, j))

# for p in ordered:
    # print(str(p[0]) + " - " + str(p[1]) + " - " + str(p[2]))

# stores tuple in form of (parent, height)
# indeces are the elements!
class UnionFind:

    def __init__(self, len: int):
        self.ds: list[tuple[int, int]] = [(None, None)] * len # type: ignore
        i = 0
        while i < len:
            self.ds[i] = (i, 0)
            i += 1

    def union(self, n, m) -> None:
        assert not self.ds[n] is None
        self.ds[self.find(m)] = (self.find(self.ds[n][0]), self.ds[n][1] + 1) # type: ignore

    # returns the parent index
    def find(self, n) -> int | None:
        t: tuple[int, int] = self.ds[n]
        parent_index = t[0]

        while parent_index != n:
            nxt = self.ds[parent_index]
            if nxt is None: return None
            n = parent_index
            parent_index = nxt[0]

        return parent_index

uf = UnionFind(len(all_points))

i = 0
counter = 0

while counter < 1000:
    t: tuple[int, Point, Point] = ordered[i] # type: ignore

    if uf.find(t[1].index) != uf.find(t[2].index):
        uf.union(t[1].index, t[2].index)

    counter += 1
    i += 1

circuits = {}

x = 0
while x < len(uf.ds):
    circuits[uf.find(x)] = circuits.get(uf.find(x), 0) + 1
    x += 1

# print("{" + "\n".join("{!r}: {!r},".format(k, v) for k, v in circuits.items()) + "}")

l = sorted(circuits.values(), reverse=True)
print(l[0] * l[1] * l[2])