import des
import subprocess
import secrets
import time

n = 500
for _ in range(n):
    key = bin(secrets.randbits(64))[2:].zfill(64)
    msg = bin(secrets.randbits(64))[2:].zfill(64)
    t1 = time.time()
    expected_output = subprocess.check_output(['./a.out', key, msg]).decode()
    t2 = time.time()
    ciphertext_test = des.edcrypt(msg, key)
    t3 = time.time()
    print(_, ("passed" if expected_output==ciphertext_test else "failed") + f"; time taken = {(t3-t1)/(t2-t1):.2f}")