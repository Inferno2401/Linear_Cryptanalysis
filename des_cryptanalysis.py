import des
import numpy as np
import des_constants


RED = "\x1b[0;31m"
RESET = "\x1b[0m"

# Linear Cryptanalysis of 3-round DES (can generalize, see Matsui's paper)

# an attempt to find K1[22] xor K3[22] using the linear equation
# PH[a]+PL[15]+CH[a]+CL[15] = K1[22]+K3[22] holding wp 0.70.

def multi_xor(string: str, indices: list):
    return sum(string[index] == '1' for index in indices)&1 # not a string, notice

# set up variables
ROUNDS = 3
p0 = 0.7
N = 300 # increasing it increases probability of success


def analyse(KEY):
    KEY_56BIT = "".join(KEY[elem] for elem in des_constants.pc1)[:56]
    random_ptexts = zip(np.random.randint(1<<32, size=(N,)), np.random.randint(1<<32, size=(N,)))
    P = list(map(lambda x: (bin(x[0])[2:].zfill(32) + bin(x[1])[2:].zfill(32)), random_ptexts))
    C = list(des.encrypt(p, KEY, ROUNDS) for p in P)
    T = 0
    prob = 0
    for p,c in zip(P, C): # turn into sum
        prob += (multi_xor(p, [2, 7, 13, 24, 48])^multi_xor(c, [2, 7, 13, 24, 48]) == multi_xor(KEY_56BIT, [0,3,8,9]))
        T += (multi_xor(p, [2, 7, 13, 24, 48])^multi_xor(c, [2, 7, 13, 24, 48]))
        # prob += (multi_xor(p, [2, 7, 13, 24, 48])^multi_xor(c, [2, 7, 13, 24]) == multi_xor(KEY_56BIT, [3]))
        # T += (multi_xor(p, [2, 7, 13, 24, 48])^multi_xor(c, [2, 7, 13, 24]))
    return int((p0<0.5) if T<N/2 else (p0>0.5)), prob/N

def auto_test(n: int):
    import tqdm
    succ = crct = 0
    for i in (range(n)):
        KEY = bin(np.random.randint(1<<32))[2:].zfill(32) + bin(np.random.randint(1<<32))[2:].zfill(32)
        KEY_56BIT = "".join(KEY[elem] for elem in des_constants.pc1)[:56]
        # print(KEY_56BIT)
        ans, prob = analyse(KEY)
        if (prob > 0.5):
            succ += 1
            crct += (ans == multi_xor(KEY_56BIT, [0, 3,8,9]))
            print("key (56-bit):", RED + KEY_56BIT[0] + RESET + KEY_56BIT[1:3] + RED + KEY_56BIT[3] + RESET + KEY_56BIT[4:], "| Predicted xor:", int(ans))
            # print("You're in luck! Here's the predicted xor of the red bits:", int(ans))
        else:
            # print("Welp, failed to cryptanalyse key, try again.")
            pass
    print("total tests:", n, "\nsuccessful analysis:", succ, "\ncorrectly predicted:", crct)

def manual_test():
    inp = input("Key please: ")
    KEY = bin(np.random.randint(1<<32))[2:].zfill(32) + bin(np.random.randint(1<<32))[2:].zfill(32) if inp in ['', 'random'] else inp.zfill(64)
    KEY_56BIT = "".join(KEY[elem] for elem in des_constants.pc1)[:56]

    print("Your key (56-bit):", RED + KEY_56BIT[0] + RESET + KEY_56BIT[1:3] + RED + KEY_56BIT[3] + RESET + KEY_56BIT[4:])
    ans, prob = analyse(KEY)
    if (prob > 0.5):
        print("You're in luck! Here's the predicted xor of the red bits:", int(ans))
    else:
        print("Welp, failed to cryptanalyse key, try again.")

if __name__ == '__main__':
    from sys import argv
    if len(argv)>1:
        auto_test(int(argv[1]))
    else:
        while True:
            manual_test()