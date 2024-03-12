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

#Using decorator dataclass to modify the behaviour of class
#Defining class CurrencySymbol with class attributes to hold data types
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
    
#Making a request to web page to obtain a response called request and convert it to JSON  
def make_request_symbol(url: str="https://api.vatcomply.com/currencies") -> dict:
    request = requests.get(url)
    CurrencySymbol = request.json()
    
    if request.status_code != 200:
        print("Error")
        return 
    
    return CurrencySymbol

#Using a CurrencySymbol class to store data in a JSON format. Then, a JSON key-value pairs were selected   
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

#Fetching data in a JSON file
def save_to_file_symbol(symbol: CurrencySymbol):
    try:
        with open('symbol.json', 'w') as file:
            json.dump(asdict(symbol), file)
    except FileNotFoundError as ex:
        print(ex)

#Creating one function that holds all functions to obtain desired results        
def CurrencySymbolJSON():
    data = make_request_symbol()
    symbol = create_final_json_symbol(data)
    save_to_file_symbol(symbol)
    return symbol

#Making a connection between Producer and Bootstrap initial cluster metadata (broker)
def CreateKafkaProducer():
    localhost = 'host.docker.internal:29092' 
    return KafkaProducer(bootstrap_servers=[localhost])

#Defining a topic where the message will be published
#Message value that is converted to a JSON formatted string that is encoded to the UTF-8 encoded version of the string 
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
        
#Putting all functions in one function
def finalExecutionSymbol():
    CurrencySymbolJSON()
    PublishingMessageSymbolToTopic()
    logging.info("Extracting symbols was successfully done")
    print("Publishing Symbol Data To Topics")

# a finalExecutionSymbol() function will be executed only if the script is the main program, but when it is imported as a module
if __name__ == "__main__":
    finalExecutionSymbol()