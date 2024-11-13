import json
from bitcoinlib.wallets import wallet_create_or_open
from bitcoinlib.transactions import Transaction
from bitcoinlib.keys import Signature
from tqdm import tqdm
from random import randint, randbytes 

NUM_PEOPLE = 500
NUM_TRANS_PER_PERSON = 50
satoshi_per_btc = 10**8

wallets = [None] * (NUM_PEOPLE + 1)
    

def send_random_transactions(f, first_addr, origem_id):
    origem = wallets[origem_id]

    key = origem.get_key().key()
    addr_origem = key.address()

    # deveria pegar da blockchain
    prev_txid = randbytes(32).hex()

    # Escreve "addr_origem": [
    # Ou seja, comeco de uma lista para a chave addr_origem
    f.write(('' if first_addr else ',') + f'"{addr_origem}": [')

    first = True
    for _ in range(NUM_TRANS_PER_PERSON):
        idx = origem_id
        while idx == origem_id:
            idx = randint(1, NUM_PEOPLE)
            
        destino = wallets[idx]
        addr_destino = destino.get_key().address

        t = Transaction(network='regtest')    
        t.add_input(prev_txid=prev_txid, output_n=1, keys=key.public_hex, compressed=False)
        t.add_output(int(0.001 * satoshi_per_btc), addr_destino)
        t.sign(key)

        sig = t.inputs[0].signatures[0]
        # Salva a assinatura (é uma lista de 3 elementos: [txid, r, s])
        f.write(('' if first else ',') + f'["{sig.txid}", "{hex(sig.r)}", "{hex(sig.s)}"]')
        first = False

    f.write("]")
        

if __name__ == '__main__':
    print('Abrindo (ou criando) carteiras...')
    for i in tqdm(range(1, NUM_PEOPLE+1)):
        wallets[i] = wallet_create_or_open(f'cara{i}')

    print('Fazendo transações...')
    with open('transcations.json', 'w') as f:
        f.write('{')
        for i in tqdm(range(1, NUM_PEOPLE+1)):
            send_random_transactions(f, i==1, i)
        
        f.write('}')
        
