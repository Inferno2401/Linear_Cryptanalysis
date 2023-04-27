import numpy as np
from constants import *

# convert_to_bitstring(substitution_boxes)
def expand(half_block: str):
    return np.array(list(half_block[expansion_table[i]] for i in range(48)))


def xor(str1: str, str2: str):
    return "".join(map(lambda c: '0' if c[0] == c[1] else '1', zip(str1, str2)))


def feistel_fn(half_block: str, subkey: str):
    
    # expand the half-block
    expanded = expand(half_block)

    # key mixing
    result = xor(expanded, subkey); #print(result)

    # apply the S-boxes.
    # print(list(int(result[i] + result[i+5] + result[i+1:i+5], base=2) for i in range(0, 48, 6)))
    res = "".join(substitution_boxes[i//6][int(result[i] + result[i+5] + result[i+1:i+5], base=2)] for i in range(0, 48, 6))
    #print(res)
    # permute the result
    
    final_ans = "".join(res[feistel_permutation[i]] for i in range(32))

    return final_ans

def generate_subkeys(key: str):
    key = "".join(key[elem] for elem in pc1)[:56]
    ans = [None]*16
    for i in range(16):
        if i in [0, 1, 8, 9, 11, 15]: 
            key = ans[i] = key[1:28] + key[0] + key[29:] + key[28]
        else:
            key = ans[i] = key[2:28] + key[0:2] + key[30:] + key[28:30]
        ans[i] = "".join(ans[i][elem] for elem in pc2)[:48]
    # print("ans: ", ans)
    return ans
    
def des(block: str, key: str, round_table=None):
    """
    Essentially, apply 16 round of Feistel mainly. One round of permuting the block before and after the feistel network. 
    One round of Feistel: (a, b) -> (a', b') with a' = b, b' = a xor f_i(b). f_i(b) = feistel_fn(b, key_i)
    """

    # first, permute the block
    block = "".join(block[elem] for elem in permutation1)
    
    # generate the sub keys for the feistel network
    subkeys = generate_subkeys(key) if round_table is None else round_table

    left = block[:32]; right = block[32:]
    for i in range(16):
        tmp = right
        right = xor(left, feistel_fn(right, subkeys[i]))
        left = tmp
    
    # apply an inverse permutation to the block and return it
    block = right + left
    ciphertext = "".join(block[elem] for elem in inv_permutation1)
    return ciphertext

def edcrypt(plaintext: str, key: str, iv: str='0'*64, decrypt=False):
    """
    Encrypting arbitrary length messages using 64-bit blocks
    """
    floor = (len(plaintext)>>6)<<6
    if len(plaintext) != floor:
        plaintext = plaintext + '1' + '0'*(floor + 63 - len(plaintext))
        floor += 64
    round_table = generate_subkeys(key)
    return "".join(des(block=plaintext[i:i+64], key=key, round_table=list(reversed(round_table)) if decrypt else round_table) for i in range(0, floor, 64))

# simple driver code
if __name__ == "__main__":
    plaintext = "1010101111001101111001101010101111001101000100110010010100110110"
    key =       "1010101010111011000010010001100000100111001101101100110011011101"

    cipher = edcrypt(plaintext, key)
    decrypted = edcrypt(cipher, key, decrypt=True)
    print(cipher)
    print(decrypted)
    expected_output = "1001111000100110100111110101101011111010010011011011101101110000"
    print(cipher == expected_output)
    print(plaintext == decrypted)
    