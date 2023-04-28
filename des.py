import numpy as np
from des_constants import *

# convert_to_bitstring(substitution_boxes)
def expand(half_block: str):
    return np.array(list(half_block[expansion_table[i]] for i in range(48)))

def xor(str1: str, str2: str):
    return "".join(map(lambda c: '0' if c[0] == c[1] else '1', zip(str1, str2)))

def feistel_fn(half_block: str, subkey: str):
    
    # expand the half-block EXPANSION
    expanded = expand(half_block)

    # key mixing KEY SIMULATES THE SBOXES BEING RANDOM PERMUTATIONS
    result = xor(expanded, subkey); #print(result)

    # apply the S-boxes. RANDOM PERMUTATION
    # print(list(int(result[i] + result[i+5] + result[i+1:i+5], base=2) for i in range(0, 48, 6)))
    res = "".join(substitution_boxes[i//6][int(result[i] + result[i+5] + result[i+1:i+5], base=2)] for i in range(0, 48, 6))
    #print(res)
    # permute the result
    
    # permute the concat of the sbox results DIFFUSION
    final_ans = "".join(res[feistel_permutation[i]] for i in range(32))

    return final_ans

# def generate_subkeys(key: str, rounds: int):
#     ans = [None]*rounds
#     for i in range(rounds):
#         if i in [0, 1, 8, 15]: # the list can be arbitrary
#             key = ans[i] = key[1:28] + key[0] + key[29:] + key[28]
#         else:
#             key = ans[i] = key[2:28] + key[0:2] + key[30:] + key[28:30]
#         ans[i] = "".join(ans[i][elem] for elem in pc2)[:48]
#     return ans
    
def generate_subkeys(key: str, rounds: int):
    # returns the array of positions of each subkey
    ans = [None]*rounds
    rotated = 0
    for i in range(rounds):
        if i in [5, 1, 8, 15]: # the list can be arbitrary
            rotated += 1
        else:
            rotated += 2
        ans[i] = [(rotated+k)%28 for k in range(27)] + [(rotated-1)%28] + [28+(rotated+k)%28 for k in range(27)] + [28+(rotated-1)%28]
        ans[i] = [ans[i][elem] for elem in pc2][:48]
    # with open('subkey-indices-des3.txt', 'w') as f:
    #     f.write(str(ans))
    return ans

def des(block: str, key: str, rounds, subkey_table):
    """
    Essentially, apply 16 round of Feistel mainly. One round of permuting the block before and after the feistel network. 
    One round of Feistel: (a, b) -> (a', b') with a' = b, b' = a xor f_i(b). f_i(b) = feistel_fn(b, key_i)
    """

    # first, permute the block
    # block = "".join(block[elem] for elem in permutation1)
    
    # generate the sub keys for the feistel network
    subkeys = []
    for subkey in subkey_table:
        ans = "".join(key[idx] for idx in subkey)
        subkeys.append(ans)

    # perform the rounds
    left = block[:32]; right = block[32:]
    for i in range(rounds):
        tmp = right
        right = xor(left, feistel_fn(right, subkeys[i]))
        left = tmp
    block = right + left
    
    # apply an inverse permutation to the block and return it
    ciphertext = block
    # ciphertext = "".join(block[elem] for elem in inv_permutation1)
    return ciphertext

def edcrypt(plain_or_cipher: str, key: str, rounds: int=16, decrypt=False):
    """
    Encrypting arbitrary length messages using 64-bit blocks
    """
    floor = (len(plain_or_cipher)>>6)<<6
    if len(plain_or_cipher) != floor:
        plain_or_cipher = plain_or_cipher + '1' + '0'*(floor + 63 - len(plain_or_cipher))
        floor += 64

    key = "".join(key[elem] for elem in pc1)[:56]
    subkey_table = generate_subkeys(key, rounds)
    return "".join(des(block=plain_or_cipher[i:i+64], key=key, rounds=rounds, subkey_table=list(reversed(subkey_table)) if decrypt else subkey_table) for i in range(0, floor, 64))

def encrypt(plaintext: str, key: str, rounds: int=16): return edcrypt(plaintext, key, rounds=rounds, decrypt=False)
def decrypt(ciphertext: str, key: str, rounds: int=16): return edcrypt(ciphertext, key, rounds=rounds, decrypt=True)

# simple driver code
if __name__ == "__main__":
    plaintext = "1010101111001101111001101010101111001101000100110010010100110110"
    key =       "1010101010111011000010010001100000100111001101101100110011011101"

    cipher = encrypt(plaintext, key, 3)
    decrypted = decrypt(cipher, key, 3)
    print(cipher)
    print(decrypted)
    expected_output = "1001111000100110100111110101101011111010010011011011101101110000"
    print(cipher == expected_output)
    print(plaintext == decrypted)