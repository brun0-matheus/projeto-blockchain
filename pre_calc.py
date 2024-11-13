from fastecdsa.curve import secp256k1
from hashlib import sha1
import random
from tqdm import tqdm
import time 


def broken_prng(time_seed):
    seed = bytearray(20)
    random.seed(time_seed)  # srandom(clock() * time() * malloc() % pow(2,31))
    for i in range(20):
        seed[i] = random.randint(1, 128)   # seed[i] = random() % 128 

    buf = bytearray(86)

    idx = 0
    cnt = 0 

    buf[idx:20] = seed
    # era para atualizar o idx aqui, mas a lib original esqueceu
    buf[idx:idx+8] = cnt.to_bytes(8, 'big')
    idx += 8
    buf[idx:idx+4] = b'\x80\x00\x00\x00'

    return int.from_bytes(sha1(buf).digest())
        


with open('precalc.json', 'w') as f:
    G = secp256k1.G
    f.write('{')

    try:
        for i in tqdm(range(2**21)):
            k = broken_prng(i)
            pt = k * G

            first = i==0
            f.write(('' if first else ',') + f'"{k}": {pt.x}')
    finally:            
        f.write('}')

