import asyncio, random
from utils.networks import Prom
from utils.getBalance import getBalance
from utils.client import Client
from utils.transactions import Transactions
from config import mode, delay_min, delay_max, start_delay_max, start_delay_min, low_prom, high_prom, group_accounts
from datetime import datetime, timezone, timedelta
from utils.tg import send_number, send_delay

address = []
clients = []
transactions = []
proxy = []
with open('proxy.txt') as f:
    proxy = f.readlines()

with open('addresses.txt') as f:
    address = f.readlines()


for i in range(len(address)):
    clients.append(Client(address[i].strip(), Prom, proxy[i].strip()))
    transactions.append(Transactions(client=clients[i]))

async def main(low_prom, high_prom):
    k = 0
    if mode == 'Balance':
        getBalance(client_list=clients, num_clients=len(clients))
        return 0

    elif mode == 'Random':
        b = 0
        while True:
            if b != 0:
                now = datetime.now(timezone.utc) + timedelta(hours=2)
                target_hour = random.randint(4, 15)
                target_time = datetime(now.year, now.month, now.day, target_hour, 0, 0, tzinfo=timezone.utc) - timedelta(hours=2)
                if now >= target_time:
                    target_time += timedelta(days=1)
                delay_seconds = (target_time - now).total_seconds()
                print(f'Next run at: {target_time} (UTC+2)')
                send_delay(f'⏰ Next run at: {target_time} (UTC+2)')
                await asyncio.sleep(delay_seconds)
                send_delay(f'🚀 Start transactions of group: {group_accounts}..')
            mas_counter = [0] * len(address)
            current_count = 0
            mas_count = [[0 for _ in range(3)] for _ in range(len(address))]
            while current_count <= max(mas_counter):
                tasks = []
                for i in range(len(address)):
                    if current_count == 0:
                        mas_counter[i] = random.randint(4, 7)

                    if current_count != mas_counter[i]:
                        nft = transactions[i].createNFT(k, delay_min, delay_max, start_delay_min, start_delay_max)
                        token = transactions[i].createToken(k, delay_min, delay_max, start_delay_min, start_delay_max)
                        yourself = transactions[i].txYourself(k, delay_min, delay_max, start_delay_min, start_delay_max, low_prom, high_prom)
                        mas_tx = [nft, token, yourself]
                        choice = random.choice(mas_tx)
                        while choice == nft and mas_count[i][0] == 0:
                            choice = random.choice(mas_tx)
                        while choice == token and mas_count[i][1] == 0:
                            choice = random.choice(mas_tx)
                        if choice == nft:
                            mas_count[i][0]+=1
                        elif choice == token:
                            mas_count[i][1]+=1
                        else:
                            mas_count[i][2]+=1
                        tasks.append(choice)
                await asyncio.gather(*tasks)
                current_count += 1
                k+=1
                print(f'Current Circle: {current_count}')
            low_prom += 5
            high_prom += 5
            b+=1

    elif mode == 'TxYourself':
        b = 0
        while True:
            if b != 0:
                now = datetime.now(timezone.utc) + timedelta(hours=2)
                target_hour = random.randint(4, 15)
                target_time = datetime(now.year, now.month, now.day, target_hour, 0, 0, tzinfo=timezone.utc) - timedelta(hours=2)
                if now >= target_time:
                    target_time += timedelta(days=1)
                delay_seconds = (target_time - now).total_seconds()
                print(f'Next run at: {target_time} (UTC+2)')
                send_delay(f'Next run at: {target_time} (UTC+2)')
                await asyncio.sleep(delay_seconds)
            mas_counter = [0] * len(address)
            current_count = 0
            while current_count <= max(mas_counter):
                tasks = []
                for i in range(len(address)):
                    if current_count == 0:
                        mas_counter[i] = random.randint(4, 7)
                    if current_count != mas_counter[i]:
                        tasks.append(transactions[i].txYourself(k, delay_min, delay_max, start_delay_min, start_delay_max, low_prom, high_prom))
                await asyncio.gather(*tasks)
                current_count += 1
                k+=1
                print(f'Current Circle: {current_count}')
            low_prom += 5
            high_prom += 5
            b+=1

    else:
        while True:
            tasks = []
            for i in range(len(address)):
                if mode == 'NFT':
                    tasks.append(transactions[i].createNFT(k, delay_min, delay_max, start_delay_min, start_delay_max))
                elif mode == 'Token':
                    tasks.append(transactions[i].createToken(k, delay_min, delay_max, start_delay_min, start_delay_max))
            await asyncio.gather(*tasks)
            k+=1

asyncio.run(main(low_prom, high_prom))
