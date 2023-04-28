import des
import numpy as np
import secrets
import des_constants
import tqdm

# an attempt to find K1[22] xor K3[22] using the linear equation
# PH[a]+PL[15]+CH[a]+CL[15] = K1[22]+K3[22] holding wp 0.70

def multi_xor(string: str, indices: list):
    return sum(string[index] == '1' for index in indices)&1 # not a string, notice

# set up variables
ROUNDS = 1
N = 200 # for probability of success 99.8%

def test():
    KEY = bin(1+np.random.randint(-1,1<<64-1))[2:].zfill(64)
    KEY_56BIT = "".join(KEY[elem] for elem in des_constants.pc1)[:56]
    P = list(map(lambda x: bin(x)[2:].zfill(64), 1+np.random.randint(-1,1<<64-1, size=(N,))))
    C = list(des.encrypt(p, KEY, ROUNDS) for p in P)
    # print(list(zip(P, C)))
    T = 0
    crct = 0
    for p,c in zip(P, C): # turn into sum
        # crct += (multi_xor(p, [2, 7, 13, 24, 48])^multi_xor(c, [2, 7, 13, 24, 48]) == multi_xor(KEY_56BIT, [0,3]))
        # T += (1 - (multi_xor(p, [2, 7, 13, 24, 48])^multi_xor(c, [2, 7, 13, 24, 48])))
        crct += (multi_xor(p, [2, 7, 13, 24, 48])^multi_xor(c, [2, 7, 13, 24]) == multi_xor(KEY_56BIT, [3]))
        T += (1 - (multi_xor(p, [2, 7, 13, 24, 48])^multi_xor(c, [2, 7, 13, 24])))
    print(crct/N)
    return (1 if T>N/2 else 0) == multi_xor(KEY_56BIT, [3]),crct,multi_xor(KEY_56BIT, [3])

ntests = 100
# print(sum(test() for i in (range(ntests)) if crct < 0.5))
tot = s = 0
for i in range(ntests):
    val,crct,ans = test(); print("ans:", ans)
    if crct/N>0.5: continue
    tot += 1; s += val; 
print(s, tot)