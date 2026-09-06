import math

ranges: list[tuple[int, int]] = []

with open("in2.txt", "r") as f:
    for line in f: 
        ranges_str = line.split(",")
        for range in ranges_str:
            split = range.split("-")
            ranges.append((int(split[0]), int(split[1])))

invalid: list[int] = []
sum = 0

for range in ranges:
    curr = range[0]
    while curr <= range[1]:
        num_digits = math.floor(math.log10(curr)) + 1
        if num_digits % 2 == 0:
            mid = num_digits // 2
            num_str = str(curr)
            if num_str[:mid] == num_str[mid:]:
                invalid.append(curr)
                sum += curr

        curr += 1
        

print(invalid)
print(sum)
