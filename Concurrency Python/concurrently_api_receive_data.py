import threading, queue
import os
import requests
import pandas as pd, numpy as np
import time
import csv
from pandas.core.frame import DataFrame

base_url = 'https://fakestoreapi.com'
num_workers = 2
records = 1

results = []
failed_requests = []

def worker(worker_num:int, q:queue) -> None:
    with requests.Session() as session:
        while True:
            i=0
            i=i+1
            set().add(f'Worker: {worker_num}, PID: {os.getpid()}, TID: {threading.get_ident()}')
            category, id = q.get()
            endpoint = f'/{category}?id={id}'
            print(f'WORKER {worker_num}: API request for cat: {category}, id: {id} started ...')
            response = session.get(url=base_url+endpoint)
            if response.ok:
                results.append(response.json())
            else:
                failed_requests.append((category, id))
            q.task_done() 

def main() -> DataFrame:
    # Create queue and add items
    q = queue.Queue()
    for category in ('users', 'products'):
        for id in range(records):
            q.put((category,id))

    # turn-on the worker thread(s)
    # daemon: runs without blocking the main program from exiting
    for i in range(num_workers):
        threading.Thread(target=worker, args=(i, q), daemon=True).start()

    # block until all tasks are done
    q.join()

    # make dataframe of results
    return pd.DataFrame(results)



if __name__ == "__main__":
    print('THREADING')
    cwd = os.getcwd()
    try:
        os.mkdir(cwd+"/ApiExport")
    except OSError as error: 
        print(error)
    start_time = time.time()
    df = main()
    l = [1,2]
    l_mod = [0] + l + [max(l)+1]

    list_of_dfs = [df.iloc[l_mod[n]:l_mod[n+1]] for n in range(len(l_mod)-1)]
    list_of_dfs[0].to_csv('ApiExport/product.csv')
    list_of_dfs[1].to_csv('ApiExport/users.csv')
    print(f'\nDataframe ({len(failed_requests)} failed requests, {len(results)} successful requests)\n {df.head()}')
    print("\n--- %s seconds ---" % (time.time() - start_time))
    print(list(set()))
    