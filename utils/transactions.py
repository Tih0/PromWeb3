import random
import time
from utils.client import Client
from web3.exceptions import TransactionNotFound
import asyncio, string

def string_to_bytes32(text):
    if len(text) > 128:
        raise ValueError("String too long to convert to bytes32")
    bytes_text = text.encode('utf-8')
    bytes32_text = bytes_text.ljust(64, b'\0')
    return '3' + bytes32_text.hex()[:127:]

def generate_random_letters():
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    return letters
class Transactions:
    def __init__(self, client: Client):
        self.client = client

    async def txYourself(self, k, delay_min, delay_max, start_delay_min, start_delay_max, low_prom, high_prom, retry = 0):
        if k != 0 and k != -1:
            delay = random.randint(delay_min, delay_max)
            print(f'Delay: {delay}')
            await asyncio.sleep(delay)

        elif k == 0:
            delay = random.randint(start_delay_min, start_delay_max)
            print(f'Start delay:{delay}')
            await asyncio.sleep(delay)

        print(f'{self.client.address} | txYourself')
        try:
            tx = self.client.send_transaction(
                to=self.client.address,
                # value = random.randint(low_prom, high_prom) * (10 ** 17)
                value= self.client.w3.eth.get_balance(self.client.address) - (random.randint(1, 3) * 10**17)
            )
            await asyncio.sleep(5)
            verify = self.client.verif_tx(tx)
            if verify == False:
                retry += 1
                if retry < 5:
                    print(f"{self.client.address} | Error. Try one more time {retry} / 5")
                    print('Time sleep 20 seconds')
                    await asyncio.sleep(20)
                    k = -1
                    await self.txYourself(k, delay_min, delay_max, start_delay_min, start_delay_max, low_prom, high_prom, retry=retry)
                else:
                    print(f"ERROR txYourself")
                    return 0

        except TransactionNotFound:
            print(f'{self.client.address} | The transaction has not been remembered for a long period of time, trying again')
            print('Time sleep 120 seconds')
            await asyncio.sleep(120)
            retry += 1
            if retry > 5:
                return 0
            k = -1
            await self.txYourself(k, delay_min, delay_max, start_delay_min, start_delay_max, low_prom, high_prom, retry=retry)

        except ConnectionError:
            print(f'{self.client.address} | Internet connection error or problems with the RPC')
            await asyncio.sleep(120)
            print('Time sleep 120 seconds')
            retry += 1
            if retry > 5:
                return 0
            k = -1
            await self.txYourself(k, delay_min, delay_max, start_delay_min, start_delay_max, low_prom, high_prom, retry=retry)

        except Exception as error:
            print(f"{self.client.address} | Unknown Error:  {error}")
            print('Time sleep 120 seconds')
            await asyncio.sleep(120)
            retry += 1
            if retry > 5:
                return 0
            k = -1
            await self.txYourself(k, delay_min, delay_max, start_delay_min, start_delay_max, low_prom, high_prom, retry=retry)


    async def createToken(self, k, delay_min, delay_max, start_delay_min, start_delay_max, retry = 0):
        if k != 0 and k != -1:
            delay = random.randint(delay_min, delay_max)
            print(f'Delay: {delay}')
            await asyncio.sleep(delay)


        elif k == 0:
            delay = random.randint(start_delay_min, start_delay_max)
            print(f'Start delay:{delay}')
            await asyncio.sleep(delay)

        print(f'{self.client.address} | Create Token')
        contract_address = '0x1612b92eb16A8966ddC3bAcd05EB517183Dd9A98'
        myToken = string_to_bytes32(generate_random_letters())
        data = f'0x4fde2bc200000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000000000000012000000000000000000000000000000000000000000000000000000000000000120000000000000000000000000000000000000000000000000000000000000160000000000000000000000000000000000000000000000000000000000000271000000000000000000000000000000000000000000000000000000000000027100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000{myToken}{myToken}0'
        try:
            tx = self.client.send_transaction(
                to=contract_address,
                value=0,
                data=data,
            )
            await asyncio.sleep(5)
            verify = self.client.verif_tx(tx)
            if verify == False:
                retry += 1
                if retry < 5:
                    print(f"{self.client.address} | Error. Try one more time {retry} / 5")
                    print('Time sleep 20 seconds')
                    await asyncio.sleep(20)
                    k = -1
                    await self.createToken(k, delay_min, delay_max, start_delay_min, start_delay_max, retry=retry)
                else:
                    print(f"ERROR Create Token")
                    return 0

        except TransactionNotFound:
            print(f'{self.client.address} | The transaction has not been remembered for a long period of time, trying again')
            print('Time sleep 120 seconds')
            await asyncio.sleep(120)
            retry += 1
            if retry > 5:
                return 0
            k = -1
            await self.createToken(k, delay_min, delay_max, start_delay_min, start_delay_max, retry=retry)
        except ConnectionError:
            print(f'{self.client.address} | Internet connection error or problems with the RPC')
            await asyncio.sleep(120)
            print('Time sleep 120 seconds')
            retry += 1
            if retry > 5:
                return 0
            k = -1
            await self.createToken(k, delay_min, delay_max, start_delay_min, start_delay_max, retry=retry)
        except Exception as error:
            print(f"{self.client.address} | Unknown Error:  {error}")
            print('Time sleep 120 seconds')
            await asyncio.sleep(120)
            retry += 1
            if retry > 5:
                return 0
            k = -1
            await self.createToken(k, delay_min, delay_max, start_delay_min, start_delay_max, retry=retry)
    async def createNFT(self, k, delay_min, delay_max, start_delay_min, start_delay_max, retry=0):
        if k > 0 and k != -1:
            delay = random.randint(delay_min, delay_max)
            print(f'Delay: {delay}')
            await asyncio.sleep(delay)

        elif k == 0:
            delay = random.randint(start_delay_min, start_delay_max)
            print(f'Start delay:{delay}')
            await asyncio.sleep(delay)
        print(f'{self.client.address} | Create NFT')
        contract_address = '0x1612b92eb16a8966ddc3bacd05eb517183dd9a98'
        myNFT = string_to_bytes32(generate_random_letters())
        data = f'0x40bfac6500000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000000000000012000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000005000000000000000000000000000000000000000000000000000000000000000{myNFT}{myNFT}0'
        try:
            tx = self.client.send_transaction(
                to=contract_address,
                value=0,
                data=data,
            )
            await asyncio.sleep(5)
            verify = self.client.verif_tx(tx)
            if verify == False:
                retry += 1
                if retry < 5:
                    print(f"{self.client.address} | Error. Try one more time {retry} / 5")
                    print('Time sleep 20 seconds')
                    await asyncio.sleep(20)
                    k = -1
                    await self.createNFT(k, delay_min, delay_max, start_delay_min, start_delay_max, retry=retry)
                else:
                    print(f"ERROR Create NFT")
                    return 0

        except TransactionNotFound:
            print(f'{self.client.address} | The transaction has not been remembered for a long period of time, trying again')
            print('Time sleep 120 seconds')
            await asyncio.sleep(120)
            retry += 1
            if retry > 5:
                return 0
            k = -1
            await self.createNFT(k, delay_min, delay_max, start_delay_min, start_delay_max, retry=retry)

        except ConnectionError:
            print(f'{self.client.address} | Internet connection error or problems with the RPC')
            await asyncio.sleep(120)
            print('Time sleep 120 seconds')
            retry += 1
            if retry > 5:
                return 0
            k = -1
            await self.createNFT(k, delay_min, delay_max, start_delay_min, start_delay_max, retry=retry)

        except Exception as error:
            print(f"{self.client.address} | Unknown Error:  {error}")
            print('Time sleep 120 seconds')
            await asyncio.sleep(120)
            retry += 1
            if retry > 5:
                return 0
            k = -1
            await self.createNFT(k, delay_min, delay_max, start_delay_min, start_delay_max, retry=retry)

