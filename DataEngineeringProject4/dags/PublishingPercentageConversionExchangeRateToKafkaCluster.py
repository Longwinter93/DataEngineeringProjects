from WebScrapingPythonPercentageConversionExchangeRate import DictionaryConversionRateChangePercentage, ConvertingDictToJSON 
from kafka import KafkaProducer 
from kafka.errors import KafkaError
import time
import json

#A Kafka publishes records to the Kafka cluster
def CreateKafkaProducer():
    localhost = 'host.docker.internal:29092' 
    return KafkaProducer(bootstrap_servers=[localhost])

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
    