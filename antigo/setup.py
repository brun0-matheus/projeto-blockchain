import subprocess
import json
from tqdm import tqdm
from bitcoinlib.keys import Key
from bitcoinlib.wallets import wallet_create_or_open 

# Garanta que o bitcoind esteja rodando
# bitcoind -regtest -fallbackfee=0.00001 -deprecatedrpc=create_bdb
# Cria uma wallet legacy e deixa como padrao
# bitcoin-cli -regtest -named createwallet wallet_name="pai" descriptors=false

# Para 10k pessoas leva um tempinho...
NUM_PESSOAS = 10000

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
        
        print(f"Error: Command '{command}' failed with status code {e.returncode}")
        print(e.stderr)
        exit(1)


print('Criando carteiras e minerando para elas...')
for i in tqdm(range(1, NUM_PESSOAS+1)):
    name = f'cara{i}'
    wallet = wallet_create_or_open(name, network='regtest')

    address = wallet.get_key().address
    balance = wallet.balance()

    run_command('importaddress', address, name, 'false')
    run_command('generatetoaddress', 1, address)

print('Minerando blocos extras para todo mundo receber o dinheiro')
run_command('-generate', 100)

    
