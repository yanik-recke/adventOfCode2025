import math

ranges: list[tuple[int, int]] = []

with open("in2.txt", "r") as f:
    for line in f: 
        ranges_str = line.split(",")
        for x in ranges_str:
            split = x.split("-")
            ranges.append((int(split[0]), int(split[1])))

invalid: list[int] = []
total = 0

digits = set()

# math.floor(x / pow(10, n)) % 10

for lo, hi in ranges:
    for curr in range(lo, hi + 1):
        s = str(curr)
        for inner in range(1, len(s)):
            j = inner
            pre_idx = 0
            prefix = s[:inner]
            while j < len(s) and prefix[pre_idx] == s[j]:
                pre_idx = (pre_idx + 1) % inner
                j += 1
            if pre_idx == 0 and j == len(s):
                invalid.append(curr)
                total += curr
                break

# too low: 34089559199
# too low: 34089559244
print(invalid)
print(total)
