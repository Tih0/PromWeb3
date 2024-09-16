from web3 import Web3
from typing import Optional, Union
import requests
from web3.middleware import geth_poa_middleware
from decimal import Decimal
from utils.networks import Network
from config import useProxy
from utils.tg import send_message_error, send_message_success

class TokenAmount:
    Wei: int
    Ether: Decimal
    decimals: int

    def __init__(self, amount: Union[int, float, str, Decimal], decimals: int = 18, wei: bool = False) -> None:
        if wei:
            self.Wei: int = amount
            self.Ether: Decimal = Decimal(amount) / 10 ** decimals
        else:
            self.Wei: int = int(Decimal(amount) * 10 ** decimals)
            self.Ether: Decimal = Decimal(amount)

        self.decimals = decimals
class Client:

    def __init__(
            self,
            private_key: str,
            network: Network,
            proxy: Optional[str] = None,
            abi: Optional[str] = None
    ):
        self.private_key = private_key
        self.network = network
        self.rpc = self.network.rpc
        if useProxy == True:
            self.proxyline = f'http://vNuNjA5W:HmxyeHtB@{proxy}'
            self.w3 = Web3(Web3.HTTPProvider(endpoint_uri=self.rpc, request_kwargs= {'proxies' : {'http': self.proxyline, 'https': self.proxyline}}))
        else:
            self.w3 = Web3(Web3.HTTPProvider(endpoint_uri=self.rpc))

        self.address = Web3.to_checksum_address(self.w3.eth.account.from_key(private_key=private_key).address)
        self.explorer = network.explorer



    @staticmethod
    def get_max_priority_fee_per_gas(w3: Web3, block: dict) -> int:
        block_number = block['number']
        latest_block_transaction_count = w3.eth.get_block_transaction_count(block_number)
        max_priority_fee_per_gas_lst = []
        for i in range(latest_block_transaction_count):
            try:
                transaction = w3.eth.get_transaction_by_block(block_number, i)
                if 'maxPriorityFeePerGas' in transaction:
                    max_priority_fee_per_gas_lst.append(transaction['maxPriorityFeePerGas'])
            except Exception:
                continue

        if not max_priority_fee_per_gas_lst:
            max_priority_fee_per_gas = w3.eth.max_priority_fee
        else:
            max_priority_fee_per_gas_lst.sort()
            max_priority_fee_per_gas = max_priority_fee_per_gas_lst[len(max_priority_fee_per_gas_lst) // 2]
        return max_priority_fee_per_gas

    def send_transaction(
            self,
            to,
            data=None,
            from_=None,
            increase_gas=1.2,
            value=None,
            eip1559: Optional[bool] = False,
            max_priority_fee_per_gas: Optional[int] = None,
            max_fee_per_gas: Optional[int] = None
    ):
        if not from_:
            from_ = self.address

        tx_params = {
            'chainId': self.w3.eth.chain_id,
            'nonce': self.w3.eth.get_transaction_count(self.address),
            'from': Web3.to_checksum_address(from_),
            'to': Web3.to_checksum_address(to),
        }
        if data:
            tx_params['data'] = data


        if eip1559 == True:
            if useProxy == True:
                w3 = Web3(Web3.HTTPProvider(endpoint_uri=self.rpc, request_kwargs= {'proxies' : {'http': self.proxyline, 'https': self.proxyline}}))
            else:
                w3 = Web3(Web3.HTTPProvider(endpoint_uri=self.rpc))
            w3.middleware_onion.inject(geth_poa_middleware, layer=0)

            last_block = w3.eth.get_block('latest')
            if not max_priority_fee_per_gas:
                max_priority_fee_per_gas = Client.get_max_priority_fee_per_gas(w3=w3, block=last_block)
            if not max_fee_per_gas:
                base_fee = int(last_block['baseFeePerGas'] * increase_gas)
                max_fee_per_gas = base_fee + max_priority_fee_per_gas
            tx_params['maxPriorityFeePerGas'] = max_priority_fee_per_gas
            tx_params['maxFeePerGas'] = max_fee_per_gas

        else:
            tx_params['gasPrice'] = self.w3.eth.gas_price

        if value:
            tx_params['value'] = value

        try:
            tx_params['gas'] = int(self.w3.eth.estimate_gas(tx_params) * increase_gas)

        except Exception as err:
            print(f'{self.address} | Transaction failed | {err}')
            txt = f'{self.address} | Transaction failed | {err}'
            send_message_error(self.address, txt)
            return None
        sign = self.w3.eth.account.sign_transaction(tx_params, self.private_key)
        return self.w3.eth.send_raw_transaction(sign.rawTransaction)

    def verif_tx(self, tx_hash) -> bool:
        try:
            data = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=200)
            if 'status' in data and data['status'] == 1:
                print(f'{self.address} | transaction was successful: ')
                print(f'{self.network.explorer}{tx_hash.hex()}')
                send_message_success(self.address, f'{self.network.explorer}{tx_hash.hex()}')
                return True
            else:
                print(f'{self.address} | transaction failed {data["transactionHash"].hex()}')
                txt = f'{self.address} | transaction failed {data["transactionHash"].hex()}'
                send_message_error(self.address, txt)
                return False
        except Exception as err:
            print(f'{self.address} | unexpected error in <verif_tx> function: {err}')
            txt = f'{self.address} | unexpected error in <verif_tx> function: {err}'
            send_message_error(self.address, txt)
            return False


    def get_eth_price(self, token='ETH'):
        token = token.upper()
        print(f'{self.address} | getting {token} price')
        response = requests.get(f'https://api.binance.com/api/v3/depth?limit=1&symbol={token}USDT')
        if response.status_code != 200:
            print(f'code: {response.status_code} | json: {response.json()}')
            return None
        result_dict = response.json()
        if 'asks' not in result_dict:
            print(f'code: {response.status} | json: {response.json()}')
            return None
        return float(result_dict['asks'][0][0])
