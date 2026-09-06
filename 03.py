
total = 0

with open("in3.txt", "r") as f:
    for line in f:
        l = [int(x) for x in line.strip()]

        fst_max = (-1, -1)
        for i, x in enumerate(l):
            fst_max = fst_max if fst_max[1] >= x else (i, x)

        temp = fst_max
        if fst_max[0] == len(l) - 1:
            fst_max = (-1, -1)
            for i, x in enumerate(l[:len(l) - 1]):
                fst_max = fst_max if fst_max[1] > x else (i, x)

            # print(l, fst_max[1], temp[1])
            total += int(str(fst_max[1]) + str(temp[1]))
        else:
            fst_max = (-1, -1)
            for i, x in enumerate(l[temp[0] + 1:]):
                fst_max = fst_max if fst_max[1] > x else (i, x)

            # print(l, temp[1], fst_max[1])
            total += int(str(temp[1]) + str(fst_max[1]))

print(total)


    

        
