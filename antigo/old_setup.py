import subprocess
import json
from tqdm import tqdm

# Garanta que o bitcoind esteja rodando
# bitcoind -regtest -fallbackfee=0.00001

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
        
        print(f"Error: Command failed with status code {e.returncode}")
        print(e.stderr)
        exit(1)


def create_or_open(wallet_name, generate_to=False) -> str:
    # Returns the main address
    
    if run_command('loadwallet', wallet_name, crash_on_error=False):
        lst = json.loads(run_command('listaddressgroupings', wallet=wallet_name))
        if len(lst[0]) == 0:
            addr = run_command('getnewaddress', wallet=wallet_name)
            return addr
        
        return lst[0][0][0]
    else:
        run_command('createwallet', wallet_name)
        addr = run_command('getnewaddress', wallet=wallet_name)
        if generate_to:
            run_command('generatetoaddress', 171, addr)
        return addr 
        

# Cria carteira original e minera os primeiros satoshis
print('Criando carteira pai...')
addr_pai = create_or_open('pai', generate_to=True)

dinheiro = float(run_command('getbalance'))

print(f'Carteira criada e primeiros blocos minerados! Balança atual: {dinheiro}')
assert dinheiro > 0, 'Deveria ter alguns bitcoins na carteira'

print(f'Criando (ou abrindo) {NUM_PESSOAS} carteiras e mandando dinheiro...')
x = 450
print(f'Fazendo em blocos de {x} para nao sobrecerragar a mempool')
for i in range(1, NUM_PESSOAS+1, x):
    print(f'Bloco {i}-{i+x}...')
    for j in tqdm(range(i, min(i+x, NUM_PESSOAS+1))):
        wallet_name = f'cara{j}'
        
        addr_cara = create_or_open(wallet_name)

        run_command('sendtoaddress', addr_cara, 0.1, wallet='pai')
        run_command('unloadwallet', wallet_name)
        
    run_command('-generate', 1, wallet='pai')
    
print('Dinheiro enviado! Agora vamos minerar alguns blocos para confirmar as transações e ver o saldo')
run_command('-generate', 6, wallet='pai')

for i in range(1, NUM_PESSOAS+1):
    wallet_name = f'cara{i}'
    run_command('loadwallet', wallet_name)
    saldo = float(run_command('getbalance', wallet=wallet_name))
    run_command('unloadwallet', wallet_name)
    
    if saldo < 0.1:        
        print(f'Saldo incorreto da pessoa {i}: {saldo}')

print('Todos saldos verificados!')


