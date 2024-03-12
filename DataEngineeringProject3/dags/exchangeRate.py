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
#Defining class ExchangeRate with class attributes to hold data types
@dataclass
class ExchangeRate:
    date: str
    base: str
    EUR: float
    USD: float 
    GBP: float
    PLN: float
    SEK: float
    CHF: float
    INR: float
    CNY: float
    
#Making a request to web page to obtain a response called request and convert it to JSON
def make_request_currency(url: str="https://api.vatcomply.com/rates?base=EUR") -> dict:
    request = requests.get(url)
    CurrencyData = request.json()
    
    if request.status_code != 200:
        print("Error")
        return 
    
    return CurrencyData

#Using a ExchangeRate class to store data in a JSON format. Then, a JSON key-value pairs were selected
def create_final_json_currency(json_data) -> dict:
    currency = ExchangeRate(
        date=json_data['date'],
        base=json_data['base'],
        EUR=json_data['rates']['EUR'],
        USD=json_data['rates']['USD'],
        GBP=json_data['rates']['GBP'],
        PLN=json_data['rates']['PLN'],
        SEK=json_data['rates']['SEK'],
        CHF=json_data['rates']['CHF'],
        INR=json_data['rates']['INR'],
        CNY=json_data['rates']['CNY']     
    )
    return currency 

#Fetching data in a JSON file
def save_to_file_currency(currency: ExchangeRate):
    timestr = time.strftime("%d-%m-%Y")
    try: 
        with open(timestr + '-' + 'currency.json', 'w') as file:
            json.dump(asdict(currency), file)
    except FileNotFoundError as ex:
        print(ex)
        
#Creating one function that holds all functions to obtain desired results        
def CurrencyExchangeJSON():
    data = make_request_currency()
    currency = create_final_json_currency(data)
    save_to_file_currency(currency)
    return currency

#Making a connection between Producer and Bootstrap initial cluster metadata (broker)
def CreateKafkaProducer():
    localhost = 'host.docker.internal:29092' 
    return KafkaProducer(bootstrap_servers=[localhost])

#Defining a topic where the message will be published
#Message value that is converted to a JSON formatted string that is encoded to the UTF-8 encoded version of the string
def PublishingMessageCurrencyToTopic():
    producer = CreateKafkaProducer()
    topic_name = 'Currency' # topic where the message will be published
    StreamingDataCurrency = CurrencyExchangeJSON()   
    StreamingDataDictCurrency = asdict(StreamingDataCurrency)
    end_time = time.time() + 30 # the script will run for 30 seconds
    while True:
        if time.time() > end_time:
            break  
        producer.send(topic_name, json.dumps(StreamingDataDictCurrency).encode('utf-8'))
        time.sleep(10)
        
#Putting all functions in one function
def finalExecutionExchangeRate():
    CurrencyExchangeJSON()
    PublishingMessageCurrencyToTopic()
    logging.info("Extracting Exchange Rate was successfully done")
    print("Publishing Exchange Rate Data To Topics")
    
# a finalExecutionExchangeRate() function will be executed only if the script is the main program, but when it is imported as a module
if __name__ == "__main__":
    finalExecutionExchangeRate()