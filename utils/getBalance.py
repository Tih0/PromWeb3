from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from utils.client import Client

def getBalanceForOne(client: Client, count):
    count_tx = client.w3.eth.get_transaction_count(client.address)
    eth = format(client.w3.eth.get_balance(client.address) / 10 ** 18, '.6f')
    res = (f'{client.address} |-->   PROM: {eth}')
    if count == False:
        return res
    else:
        res2 = (f"                                           |-->   Count TXs: {count_tx}")
        return res, res2

def getBalance(client_list: list[Client], num_clients: int, count=False):
    print('BALANCE: \n------------------------------------------')
    threads = []
    mas = []
    with ThreadPoolExecutor(max_workers=num_clients) as executor:
        futures = [executor.submit(getBalanceForOne, client_list[i], True) for i in range(num_clients)]
        for future in futures:
            result = future.result()
            mas.append(result)

    for i in range(num_clients):
        print(mas[i][0])
        print(mas[i][1])
    print('\n\n\n')