# Simulação de PRNG vulnerável em carteiras bitcoin 

Inspirado no caso de carteiras Android de bitcoin que foram quebradas em 2013 devido a uma falha no gerador de números pseudo-aleatórios, como explicado nesse [artigo](https://dl.acm.org/doi/abs/10.1007/978-3-642-36095-4_9). 

## Instalação 

Baixe a biblioteca [bitcoinlib](https://github.com/1200wd/bitcoinlib/tree/48e9984791e0ede99141610483725b2e30f57ee9) (apenas a pasta chamada bitcoinlib que está no repositório), e substituia o arquivo `keys.py` pelo o que está aqui (ele contém o código vulnerável do PRNG).

## Uso 

Rode o script `pre_calc.py`, que vai gerar um .json com seeds e seus valores r correspondentes. Leva 1 hora no meu computador, mas ele é bem lento.

Depois, execute `make_transactions.py`, que vai criar as carteiras bitcoin se não existirem, ou abri-las caso já existam. Após isso, ele vai fazer as transações e salvar as informações em `transactions.json`.

Finalmente, rode `crack.py`, que vai conseguir descobrir as chaves privadas de algumas carteiras. Para conseguir taxas de sucessos melhores, basta aumentar o tamanho do precalculo, mas fazer isso vai aumentar o consumo de memória e CPU. As chaves descobertas são salvas no arquivo `leaked.json`.

Caso queira verificar se as chaves estão corretas, basta executar `verify.py`.

Para apagar as chaves e transações salvas que a biblioteca mantém, basta apagar a basta .bitcoinlib na sua home (pelo menos no linux ela fica lá).

