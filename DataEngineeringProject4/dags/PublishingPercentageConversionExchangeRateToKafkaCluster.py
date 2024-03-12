from WebScrapingPythonPercentageConversionExchangeRate import DictionaryConversionRateChangePercentage, ConvertingDictToJSON 
from kafka import KafkaProducer 
from kafka.errors import KafkaError
import time
import json

#Making a connection between Producer and Bootstrap initial cluster metadata (broker)
#A Kafka publishes records to the Kafka cluster
def CreateKafkaProducer():
    localhost = 'host.docker.internal:29092' 
    return KafkaProducer(bootstrap_servers=[localhost])

#Defining a topic where the message will be published
#Message value that is converted to a JSON formatted string that is encoded to the UTF-8 encoded version of the string 
def PublishingPercentageChangeExchangeRateRecordsToTopic():
    producer = CreateKafkaProducer()
    topic_name = 'percentageexchangerate' # topic where the message will be published
    RateChangePercentage = DictionaryConversionRateChangePercentage()
    JSONConversionRateChangePercentage = ConvertingDictToJSON(RateChangePercentage)
    StreamingDataDictPercentageChangeExchangeRate = JSONConversionRateChangePercentage
    end_time = time.time() + 30 # the script will run for 30 seconds
    while True:
        if time.time() > end_time:
            break  
        producer.send(topic_name, json.dumps(StreamingDataDictPercentageChangeExchangeRate).encode('utf-8'))
        time.sleep(10)
    print("\033[92m Publishing PercentageChangeExchangeRate events to Kafka Cluster")
     
#Running this function if this file is run as a script from the command line. 
#However, if the file is imported from another file, this will not be executed.       
if __name__ == "__main__":
    PublishingPercentageChangeExchangeRateRecordsToTopic()