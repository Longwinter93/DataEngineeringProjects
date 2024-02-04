from dataclasses import dataclass, asdict
from typing import List
import requests
import json 
import time
import os.path
import os
import logging
from kafka import KafkaProducer 
from kafka.errors import KafkaError


@dataclass
class CurrencySymbol:
    EUR: str
    SymbolEuro: str
    USD: str
    SymbolUSD: str
    GBP: str
    SymbolGBP: str
    PLN: str
    SymbolPLN: str
    SEK: str
    SymbolSEK: str
    CHF: str
    SymbolCHF: str
    INR: str
    SymbolINR: str
    CNY: str
    SymbolCNY: str
    
    


def make_request_symbol(url: str="https://api.vatcomply.com/currencies") -> dict:
    request = requests.get(url)
    CurrencySymbol = request.json()
    
    if request.status_code != 200:
        print("Error")
        return 
    
    return CurrencySymbol


        
def create_final_json_symbol(json_data) -> dict:
    symbol = CurrencySymbol(
        EUR=json_data['EUR']['name'],
        SymbolEuro=json_data['EUR']['symbol'],
        USD=json_data['USD']['name'],
        SymbolUSD=json_data['USD']['symbol'],
        GBP=json_data['GBP']['name'],
        SymbolGBP=json_data['GBP']['symbol'],
        PLN=json_data['PLN']['name'],
        SymbolPLN=json_data['PLN']['symbol'],
        SEK=json_data['SEK']['name'],
        SymbolSEK=json_data['SEK']['symbol'],
        CHF=json_data['CHF']['name'],
        SymbolCHF=json_data['CHF']['symbol'],
        INR=json_data['INR']['name'],
        SymbolINR=json_data['INR']['symbol'],
        CNY=json_data['CNY']['name'],
        SymbolCNY=json_data['CNY']['symbol']     
    )
    return symbol 

def save_to_file_symbol(symbol: CurrencySymbol):
    try:
        with open('symbol.json', 'w') as file:
            json.dump(asdict(symbol), file)
    except FileNotFoundError as ex:
        print(ex)



def CurrencySymbolJSON():
    data = make_request_symbol()
    symbol = create_final_json_symbol(data)
    save_to_file_symbol(symbol)
    return symbol

def CreateKafkaProducer():
    localhost = 'host.docker.internal:29092' 
    return KafkaProducer(bootstrap_servers=[localhost])


        
def PublishingMessageSymbolToTopic():
    producer = CreateKafkaProducer()
    topic_name = 'Symbol' # topic where the message will be published
    StreamingDataSymbol = CurrencySymbolJSON()   
    StreamingDataDictSymbol = asdict(StreamingDataSymbol)
    end_time = time.time() + 30 # the script will run for 120 seconds
    while True:
        if time.time() > end_time:
            break  
        producer.send(topic_name, json.dumps(StreamingDataDictSymbol).encode('utf-8'))
        time.sleep(10)

def finalExecutionSymbol():
    CurrencySymbolJSON()
    PublishingMessageSymbolToTopic()
    logging.info("Extracting symbols was successfully done")
    print("Publishing Symbol Data To Topics")



if __name__ == "__main__":
    finalExecutionSymbol()
