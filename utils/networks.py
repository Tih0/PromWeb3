from decimal import Decimal
from typing import Union
class TokenAmount:
    Wei: int
    Ether: Decimal
    decimals: int

    def __init__(self, amount: Union[int, float, str, Decimal], decimals: int = 18, wei: bool = False) -> None:
        if wei:
            self.Wei: int = amount
            self.Ether: Decimal = Decimal(str(amount)) / 10 ** decimals

        else:
            self.Wei: int = int(Decimal(str(amount)) * 10 ** decimals)
            self.Ether: Decimal = Decimal(str(amount))

        self.decimals = decimals


class Network:
    def __init__(self,
                 name: str,
                 rpc: str,
                 chain_id: int,
                 eip1559_tx: bool,
                 coin_symbol: str,
                 explorer: str,
                 decimals: int = 18,
                 ):
        self.name = name
        self.rpc = rpc
        self.chain_id = chain_id
        self.eip1559_tx = eip1559_tx
        self.coin_symbol = coin_symbol
        self.decimals = decimals
        self.explorer = explorer

    def __str__(self):
        return f'{self.name}'

Prom = Network(
    name='Prom',
    rpc='https://testnet-rpc.prom.io',
    chain_id=97072271,
    eip1559_tx=True,
    coin_symbol='PROM',
    explorer='https://testnet.promscan.io/tx/',
)