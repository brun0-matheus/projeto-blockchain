from bitcoinlib.services.bitcoind import *
import subprocess 
import json
from bitcoinlib.wallets import wallet_create_or_open
from bitcoinlib.transactions import Transaction
from bitcoinlib.keys import Signature
from tqdm import tqdm
from random import randint, randbytes 

NUM_PEOPLE = 500
NUM_TRANS_PER_PERSON = 50
satoshi_per_btc = 10**8
bdc = BitcoindClient(base_url='http://rpcuser:ok3n2ri2j4gq90nbqununb50gi4ni4u23jf043g093jg904jg09q4@localhost:18443', network='regtest')

wallets = [None] * (NUM_PEOPLE + 1)


def run_command(*options, wallet=None, crash_on_error=True):
    command = 'bitcoin-cli -regtest '
    if wallet:
        command += f'-rpcwallet={wallet} '
    command += ' '.join(map(str, options))
    try:
        result = subprocess.run(
            command, shell=True, check=True, text=True, 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        
        output = result.stdout
        error = result.stderr

        return output.strip() 
    except subprocess.CalledProcessError as e:
        if not crash_on_error:
            return False
        
        print(f"Error: Command failed with status code {e.returncode}")
        print(e.stderr)
        exit(1)


def get_tx_id(address):
    res = run_command('listunspent', 1, 9999999, f'"[\\"{address}\\"]"')
    lst = json.loads(res)

    # pega o primeiro msm
    return lst[0]['txid']
    

def main(f, first_addr, origem_id):
    #origem = wallet_create_or_open(f'cara{origem_id}', network='regtest')
    origem = wallets[origem_id]

    key = origem.get_key().key()
    addr_origem = key.address()

    #print(f'{addr_origem = }')

    #print(f'Pegando tx id...')
    prev_txid = randbytes(32).hex()
    #tx_id = get_tx_id(addr_origem)
    #print(f'{tx_id = }')

    f.write(('' if first_addr else ',') + f'"{addr_origem}": [')

    first = True
    for _ in range(NUM_TRANS_PER_PERSON):
        idx = origem_id
        while idx == origem_id:
            idx = randint(1, NUM_PEOPLE)
            
        #destino = wallet_create_or_open(f'cara{idx}', network='regtest')
        destino = wallets[idx]
        addr_destino = destino.get_key().address
        #print(f'{addr_destino = }')

        #print('Fazendo transação...')
        t = Transaction(network='regtest')    
        t.add_input(prev_txid=prev_txid, output_n=1, keys=key.public_hex, compressed=False)
        t.add_output(int(0.001 * satoshi_per_btc), addr_destino)
        t.sign(key.private_byte)

        sig = t.inputs[0].signatures[0] 
        f.write(('' if first else ',') + f'["{t.txid}", "{hex(sig.r)}", "{hex(sig.s)}"]')
        first = False

    f.write("]")
        

if __name__ == '__main__':
    print('Abrindo carteiras...')
    for i in tqdm(range(1, NUM_PEOPLE+1)):
        wallets[i] = wallet_create_or_open(f'cara{i}')
        
    with open('transcations.json', 'w') as f:
        f.write('{')
        for i in tqdm(range(1, NUM_PEOPLE+1)):
            main(f, i==1, i)
        
        f.write('}')
        
