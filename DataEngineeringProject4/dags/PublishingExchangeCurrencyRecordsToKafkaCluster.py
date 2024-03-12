from WebScrapingPythonExchangeCurrency import DictionaryOfExchangeRate, ConvertingDictToJSON
import time
import json
from kafka import KafkaProducer 
from kafka.errors import KafkaError

#Making a connection between Producer and Bootstrap initial cluster metadata (broker)
#A Kafka publishes records to the Kafka cluster
def CreateKafkaProducer():
    localhost = 'host.docker.internal:29092' 
    return KafkaProducer(bootstrap_servers=[localhost])

#Defining a topic where the message will be published
#Message value that is converted to a JSON formatted string that is encoded to the UTF-8 encoded version of the string 
def PublishingUSDollarExchangeRatesRecordsToTopic():
    producer = CreateKafkaProducer()
    topic_name = 'exchangecurrency' # topic where the message will be published
    DictionaryDataCurrencyValues = DictionaryOfExchangeRate()
    JSONCurrencyValues = ConvertingDictToJSON(DictionaryDataCurrencyValues)
    StreamingDataDictUSDollarExchangeRates = JSONCurrencyValues
    end_time = time.time() + 30 # the script will run for 30 seconds
    while True:
        if time.time() > end_time:
            break  
        producer.send(topic_name, json.dumps(StreamingDataDictUSDollarExchangeRates).encode('utf-8'))
        time.sleep(10)
    print("\033[92m Publishing USDollarExchangeRates events to Kafka Cluster")
  
#Running this function if this file is run as a script from the command line. 
#However, if the file is imported from another file, this will not be executed.        
if __name__ == "__main__":
    PublishingUSDollarExchangeRatesRecordsToTopic() 