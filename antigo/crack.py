from bitcoinlib.wallets import wallet_create_or_open
from bitcoinlib.keys import Signature 
from fastecdsa.curve import secp256k1
import json

G = secp256k1.G
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


def my_sign(wallet_name, txid):
    wallet = wallet_create_or_open(wallet_name)
    d = wallet.get_key().key().private_byte
    d = int.from_bytes(d)

    z = int(txid, 16)
    k = 7
    pt = k * G
    r = pt.x % n
    s = (pow(k, -1, n) * (z + (r * d) % n)) % n
    if s > n / 2:
        s = n - s
    return r, s


def test_sign(wallet_name, txid):
    wallet = wallet_create_or_open(wallet_name)
    sig = Signature.create(txid, wallet.get_key().key().private_byte, k=7)
    return sig.r, sig.s 


def load_precalc():
    with open('precalc.json') as f:
        return json.load(f)
            

def load_transcations():
    with open('transcations.json') as f:
        return json.load(f)

    
print('Carregando transacoes...')
trans = load_transcations()
print('Carregado!')

print('Carregando precalc...')
mapa = load_precalc()
print('Carregado!')

found_keys = {}

for pub_key, sigs in trans.items():
    for txid, r, s in sigs:
        r = int(r, 16)
        if str(r) in mapa:
            k = mapa[r]
        else:
            continue

        print('Achou!')

        z = int(txid, 16)
        s = int(s, 16)

        d = ((((s*k) % n) - z) * pow(r, -1, n)) % n
        print(f'{pub_key = }, {d = }')

        found_keys = {pub_key: d}

        break


with open('leaked.json', 'w') as f:
    json.dump(f)
        

