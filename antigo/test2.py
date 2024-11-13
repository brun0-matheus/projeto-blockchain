from bitcoinlib.services.bitcoind import *
import subprocess 
import json
from bitcoinlib.wallets import wallet_create_or_open
from bitcoinlib.transactions import Transaction 
from tqdm import tqdm
from random import randint 

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


w = wallet_create_or_open('cara1', network='regtest')

print(w.balance())
        
