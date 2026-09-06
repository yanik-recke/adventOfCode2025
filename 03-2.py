from sortedcontainers import SortedKeyList

# tuple where the first value is the index
def key(x: tuple[int, int]) -> int:
    return x[0]

total = 0

def just_do_it(lo : int, hi : int, l: list[int]) -> tuple[int, int]:
    highest = (-1, -1) 

    for i, x in enumerate(l[lo:hi + 1]):
       highest = highest if highest[1] >= x else (i, x)

    return highest

def rec(result: SortedKeyList, lo: int, hi: int):
    if len(result) == 12 or lo > hi:
        return
    else:
        index, highest = just_do_it(lo, hi, l)
        result.add((index + lo, highest))

        if (index + lo) >= hi:
            rec(result, lo, index + lo - 1)
        else:
            rec(result, index + lo + 1, hi)
            rec(result, lo, index + lo - 1) 


with open("in3.txt", "r") as f:
    for line in f:
        l = [int(x) for x in line.strip()]

        result = SortedKeyList(key=key)

        hi = len(l) - 1
        lo = 0

        rec(result, lo, hi)

        tmp = ""
        for x in result: tmp += str(x[1])
        total += int(tmp)


print(total)
