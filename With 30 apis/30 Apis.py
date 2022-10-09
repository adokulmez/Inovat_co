import concurrent.futures
import requests
import threading
import time
import pandas as pd, numpy as np
from pandas.core.frame import DataFrame
import threading, queue
import os
import csv
import asyncio
import aiohttp




df=[]
results=[]
failed_requests = []

thread_local = threading.local()


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_API(url) -> DataFrame:
    session = get_session()
    response = session.get(url)
    if response.ok:
        results.append(response.json())
    else:
        failed_requests.append() 
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")
    download_API.task_done()
    return pd.DataFrame(results)

def download_all_APIs(APIs) :
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_API, APIs)
        

if __name__ == "__main__":
    APIs = [
        'https://fakestoreapi.com/products/1',
        'https://fakestoreapi.com/products/2',
        'https://fakestoreapi.com/products/3',
        'https://fakestoreapi.com/products/4',
        'https://fakestoreapi.com/products/5',
        'https://fakestoreapi.com/products/6',
        'https://fakestoreapi.com/products/7',
        'https://fakestoreapi.com/products/8',
        'https://fakestoreapi.com/products/9',
        'https://fakestoreapi.com/products/10',
        'https://fakestoreapi.com/products/11',
        'https://fakestoreapi.com/products/12',
        'https://fakestoreapi.com/products/13',
        'https://fakestoreapi.com/products/14',
        'https://fakestoreapi.com/products/15',
        'https://fakestoreapi.com/products/16',
        'https://fakestoreapi.com/products/17',
        'https://fakestoreapi.com/products/18',
        'https://fakestoreapi.com/products/19',
        
        'https://fakestoreapi.com/users/1',
        'https://fakestoreapi.com/users/2',
        'https://fakestoreapi.com/users/3',
        'https://fakestoreapi.com/users/4',
        'https://fakestoreapi.com/users/5',
        'https://fakestoreapi.com/users/6',
        'https://fakestoreapi.com/users/7',
        'https://fakestoreapi.com/users/8',
        'https://fakestoreapi.com/users/9',
        'https://fakestoreapi.com/users/10'
        
    ]
    start_time = time.time()
    download_all_APIs(APIs)
    
    myFile = open('demo_file.csv', 'w')
    writer = csv.writer(myFile)
    writer.writerow(['id','title','price','description','category','image','rating'])
    for data_list in results:
        writer.writerow(data_list)
    myFile.close()
    
    myFile = open('demo_file.csv', 'r')
    print("The content of the csv file is:")
    print(myFile.read())
    myFile.close()
    
    duration = time.time() - start_time
    print(f"Downloaded {len(APIs)} in {duration} seconds")