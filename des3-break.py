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
p0 = 0.19
N = 2000 # for probability of success 99.8%


def test():
    KEY = bin(np.random.randint(1<<32))[2:].zfill(32) + bin(np.random.randint(1<<32))[2:].zfill(32)
    KEY_56BIT = "".join(KEY[elem] for elem in des_constants.pc1)[:56]
    # print(KEY_56BIT)
    random_ptexts = zip(np.random.randint(1<<32, size=(N,)), np.random.randint(1<<32, size=(N,)))
    P = list(map(lambda x: (bin(x[0])[2:].zfill(32) + bin(x[1])[2:].zfill(32)), random_ptexts))
    C = list(des.encrypt(p, KEY, ROUNDS) for p in P)
    # print("\n".join(str((p,c)) for p,c in zip(P, C)))
    T = 0
    prob = 0
    for p,c in zip(P, C): # turn into sum
        # prob += (multi_xor(p, [2, 7, 13, 24, 48])^multi_xor(c, [2, 7, 13, 24, 48]) == multi_xor(KEY_56BIT, [0,3]))
        # T += (1 - (multi_xor(p, [2, 7, 13, 24, 48])^multi_xor(c, [2, 7, 13, 24, 48])))
        prob += (multi_xor(p, [2, 7, 13, 24, 48])^multi_xor(c, [2, 7, 13, 24]) == multi_xor(KEY_56BIT, [1, 2, 3]))
        T += (1 - (multi_xor(p, [2, 7, 13, 24, 48])^multi_xor(c, [2, 7, 13, 24])))
    print(prob/N)
    return ((p0<0.5) if T>N/2 else (p0>0.5)) == multi_xor(KEY_56BIT, [1, 2, 3]),prob

ntests = 100
# print(sum(test() for i in (range(ntests)) if crct < 0.5))
tot = s = t = 0
for i in range(ntests):
    val,crct = test(); #print("ans:", ans)
    if crct/N>0.5: continue
    tot += 1; s += val 
print(s, tot)