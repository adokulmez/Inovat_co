# -*- coding: utf-8 -*-

import requests
import csv
import os


cwd = os.getcwd()
try:
    os.mkdir(cwd+"/data")
except OSError as error: 
    print(error)

BASE_URL = 'https://fakestoreapi.com'

response = requests.get(f"{BASE_URL}/users")
with open('data/users.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(response.json())
file.close()

response = requests.get(f"{BASE_URL}/products")
with open('data/products.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(response.json())
file.close()

