# Find the distribution of the correlation NS between the input and output bits for each of the 8 S-boxes
from constants import substitution_boxes
from prettytable import PrettyTable, ALL

for n in range(7):
    print(f"Substitution Box {n+1}:\n")
    table = PrettyTable(["alpha|beta"] + [str(i) for i in range(1, 16)])
    table.hrules=ALL
    for i in range(1,64):
        cts=[]
        for j in range(1,16):
            ct=0
            a=bin(i)[2:].zfill(6)
            b=bin(j)[2:].zfill(4)
            for x in range(64):
                inbin = bin(x)[2:].zfill(6)
                outbin = substitution_boxes[n][int(inbin[0] + inbin[5] + inbin[1:5], base=2)]
                xor_a = sum((ord(inbin[i])-ord('0')) for i in range(6) if a[i]=='1')%2
                xor_b = sum((ord(outbin[i])-ord('0'))for i in range(4) if b[i]=='1')%2
                ct += xor_a==xor_b
            cts.append(ct-32)
        table.add_row([i] + cts)
    print(table)