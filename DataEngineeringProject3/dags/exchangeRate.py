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
    
    
def make_request_currency(url: str="https://api.vatcomply.com/rates?base=EUR") -> dict:
    request = requests.get(url)
    CurrencyData = request.json()
    
    if request.status_code != 200:
        print("Error")
        return 
    
    return CurrencyData





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

def save_to_file_currency(currency: ExchangeRate):
    timestr = time.strftime("%d-%m-%Y")
    try: 
        with open(timestr + '-' + 'currency.json', 'w') as file:
            json.dump(asdict(currency), file)
    except FileNotFoundError as ex:
        print(ex)
        
        


def CurrencyExchangeJSON():
    data = make_request_currency()
    currency = create_final_json_currency(data)
    save_to_file_currency(currency)
    return currency


def CreateKafkaProducer():
    localhost = 'host.docker.internal:29092' 
    return KafkaProducer(bootstrap_servers=[localhost])


def PublishingMessageCurrencyToTopic():
    producer = CreateKafkaProducer()
    topic_name = 'Currency' # topic where the message will be published
    StreamingDataCurrency = CurrencyExchangeJSON()   
    StreamingDataDictCurrency = asdict(StreamingDataCurrency)
    end_time = time.time() + 30 # the script will run for 120 seconds
    while True:
        if time.time() > end_time:
            break  
        producer.send(topic_name, json.dumps(StreamingDataDictCurrency).encode('utf-8'))
        time.sleep(10)
        


def finalExecutionExchangeRate():
    CurrencyExchangeJSON()
    PublishingMessageCurrencyToTopic()
    logging.info("Extracting Exchange Rate was successfully done")
    print("Publishing Exchange Rate Data To Topics")



if __name__ == "__main__":
    finalExecutionExchangeRate()
