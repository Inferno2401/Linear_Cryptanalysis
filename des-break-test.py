import des
import numpy as np
import des_constants
import tqdm

# an attempt to find K1[22] xor K3[22] using the linear equation
# PH[a]+PL[15]+CH[a]+CL[15] = K1[22]+K3[22] holding wp 0.70

def multi_xor(string: str, indices: list):
    return sum(string[index] == '1' for index in indices)&1 # not a string, notice

# set up variables
ROUNDS = 3
p0 = 0.70
N = 2000 # for probability of success 99.8%
good = []; bad = []

def test(KEY):
    KEY_56BIT = "".join(KEY[elem] for elem in des_constants.pc1)[:56]
    # print(KEY_56BIT[:5])
    random_ptexts = zip(np.random.randint(1<<32, size=(N,)), np.random.randint(1<<32, size=(N,)))
    P = list(map(lambda x: (bin(x[0])[2:].zfill(32) + bin(x[1])[2:].zfill(32)), random_ptexts))
    C = list(des.encrypt(p, KEY, ROUNDS) for p in P)
    # print("\n".join(str((p,c)) for p,c in zip(P, C)))
    T = 0
    prob = 0
    for p,c in zip(P, C): # turn into sum
        prob += (multi_xor(p, [2, 7, 13, 24, 48])^multi_xor(c, [2, 7, 13, 24, 48]) == multi_xor(KEY_56BIT, [0,3]))
        T += (multi_xor(p, [2, 7, 13, 24, 48])^multi_xor(c, [2, 7, 13, 24, 48]))
        # prob += (multi_xor(p, [2, 7, 13, 24, 48])^multi_xor(c, [2, 7, 13, 24]) == multi_xor(KEY_56BIT, [3]))
        # T += (multi_xor(p, [2, 7, 13, 24, 48])^multi_xor(c, [2, 7, 13, 24]))
    # print(prob/N)
    if prob/N > 0.5: good.append(KEY_56BIT[:5])
    else: bad.append(KEY_56BIT[:5])
    return int((p0<0.5) if T<N/2 else (p0>0.5)), prob/N

def solve(KEY):
    # print(KEY)
    while True:
        ans, prob = test(KEY)
        print(prob/N)
        # if abs(p0 - prob) < 0.01: 
        return ans
    
def test2(n: int):
    succ = crct = 0
    for i in tqdm.tqdm(range(n)):
        KEY = bin(np.random.randint(1<<32))[2:].zfill(32) + bin(np.random.randint(1<<32))[2:].zfill(32)
        KEY_56BIT = "".join(KEY[elem] for elem in des_constants.pc1)[:56]
        # print(KEY_56BIT)
        ans, prob = test(KEY)
        if (prob > 0.5):
            succ += 1
            crct += (ans == multi_xor(KEY_56BIT, [0, 3]))
            # print("You're in luck! Here's the predicted xor of the red bits:", int(ans))
        else:
            # print("Welp, failed to cryptanalyse key, try again.")
            pass
    print(n, succ, crct, sep=", ")

test2(100)
# for i in range(10):
#     KEY = bin(np.random.randint(1<<32))[2:].zfill(32) + bin(np.random.randint(1<<32))[2:].zfill(32)
#     KEY_56BIT = "".join(KEY[elem] for elem in des_constants.pc1)[:56]
#     print(KEY_56BIT)
#     ans = solve(KEY)
#     print(KEY)
#     print("K[0,3]:", multi_xor(KEY_56BIT, [0,3]))
#     print("Ours:", ans)
#     print()
print(set(good))
print(set(bad))
# print(des.ct)
# print(sum(des.ct))
# print({i:val for i,val in enumerate(des.ct)})
# print(max(des.ct), min(des.ct))