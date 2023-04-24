import random
import pymongo
import configparser
import logging
import os
from colorama import Fore, Style, init
import pyfiglet
from datetime import date, datetime
import ctypes
from tqdm.auto import tqdm
import time
import json
import requests
import inquirer
import xmltodict

config = configparser.ConfigParser()
config.read('CONFIG.ini')
username = config['DATABASE']['USERNAME']
passwd = config['DATABASE']['PASSWORD']

init(convert=True)
init(autoreset=True)

logging.basicConfig(filename="Logs/Log_errors.txt",level=logging.ERROR)

def log(content):
    print(f'[{datetime.now()}] {content}'+Style.RESET_ALL)


####
# Proxy Connection
####

with open('proxy.txt','r') as x:     
    adresy_proxy = {
        'https' : "",
        'http':""
    }
    proxy_lista =[]
    for line in x:
        proxy_lista.append(line[:-1])

def get_proxy():
    element = random.choice(proxy_lista)
    ip = element.split(":")[0]
    port = element.split(":")[1]
    login = element.split(":")[2]
    passwd = element.split(":")[3]

    https_proxy_format = "https://" +login+":"+passwd+"@"+ip+":"+port
    http_proxy_format = "http://" +login+":"+passwd+"@"+ip+":"+port
    adresy_proxy['https'] = https_proxy_format
    adresy_proxy['http'] = http_proxy_format

    return adresy_proxy

#####
# MONGO DB 
####
def mongo_list_collections():
    client = pymongo.MongoClient(f"mongodb+srv://{username}:{passwd}@kurierzyaio.3p9sozk.mongodb.net/?retryWrites=true&w=majority")
    db = client.Parcels
    return db.list_collection_names()

def mongo_start_connection_parcels(author_id:str):
    client = pymongo.MongoClient(f"mongodb+srv://{username}:{passwd}@kurierzyaio.3p9sozk.mongodb.net/?retryWrites=true&w=majority")
    db = client.Parcels
    collection = db[author_id]

    return collection

def mongo_return_db():
    client = pymongo.MongoClient(f"mongodb+srv://{username}:{passwd}@kurierzyaio.3p9sozk.mongodb.net/?retryWrites=true&w=majority")
    db = client.Parcels

    return db


####
# Exception logging
####

def log_error(content:str):
    logging.basicConfig(filename='logs.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    logging.warning(content)

def checkWhopLicence(licence_whop):
    bear = ''
    whop_headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {bear}"}

    whop_r = requests.get(f'https://api.whop.com/api/v1/licenses/{licence_whop}',headers=whop_headers) 
    whop_response = whop_r.json()
    if whop_response['valid'] == True:
        isKeyValid = True
        current_user = whop_response['discord']['username']

        return {"current_user":current_user}
    
    else:
        isKeyValid = False
        if whop_response['banned'] == True:
            return isKeyValid
        return isKeyValid
    

def trackepaka(tracking) -> dict or str:
    data = {'parcelNumber': tracking}

    response = requests.post('https://www.epaka.pl/api/getTraceOfParcel.xml',data=data)
    response_json = xmltodict.parse(response.text)

    message = response_json['data']['message']

    status = {"AllSteps":[],"LastStep":"N/A"}

    if message == "Parcel found":
        for parcel in response_json['data']['trace']['step']:
            status['AllSteps'].append(parcel)

        try:
            status['LastStep'] = response_json['data']['trace']['step'][-1]
        except:
            pass
        
        if status.keys() == ['time','location','status_code','status_code_desc', 'status_code_generalized']:
            return "Not in transit"

        return status
    else:
        return "Not Found"



def PostNL_tracking(postCode,tracking):

    headers = {
        'authority': 'jouw.postnl.nl',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
        'dnt': '1',
        'referer': f'https://jouw.postnl.nl/track-and-trace/{tracking}-NL-{postCode}',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Opera";v="91", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.65',
    }

    params = {
        'language': 'en',
    }

    response = requests.get(f'https://jouw.postnl.nl/track-and-trace/api/trackAndTrace/{tracking}-NL-{postCode}', params=params, headers=headers)
    if response.status_code != 200:
        raise Exception
    else:
        print(response.json())
        latest_status = response.json()['colli'][tracking]['statusPhase']['message']
        try:
            delivery_date = response.json()['colli'][tracking]['deliveryDate']
        except ValueError:
            delivery_date = "N/A"
        shippedDate = response.json()['colli'][tracking]['observations'][-1]['observationDate']

        return latest_status,delivery_date,shippedDate
    