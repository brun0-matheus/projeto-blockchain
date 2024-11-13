import json
from bitcoinlib.wallets import wallet_create_or_open
from bitcoinlib.keys import HDKey 
from tqdm import tqdm

NUM_PEOPLE = 500
# Parâmetros da curva elíptica
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


with open('leaked.json') as f:
    leaked = json.load(f)

print('Verificando chaves...')
cor = 0
for i in tqdm(range(1, NUM_PEOPLE+1)):
    nome = f'cara{i}'
    wallet = wallet_create_or_open(nome)

    key = wallet.get_key().key()
    pub = key.address()
    if pub in leaked:
        real_priv = key.secret        
        for leaked_priv in leaked[pub]:
            if int(leaked_priv) == real_priv:
                print('Verificação de chave privada bem-sucedida')
                cor += 1
                break
        else:
            print('Deu ruim! As candidatas a chave privada estão incorretas!')

tot = len(leaked)

if cor == tot:
    print(f'No total, {tot} chaves foram vazadas, e todas estavam corretas.')
else:
    print(f'No total, {tot} chaves foram vazadas, sendo que {cor} estavam corretas e {tot-cor} erradas.')
