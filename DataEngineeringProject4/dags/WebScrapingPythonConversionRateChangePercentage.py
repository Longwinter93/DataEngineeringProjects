from bs4 import BeautifulSoup
import requests
import json
import time
import pandas as pd
import logging
import io  
from minio import Minio 
from kafka import KafkaProducer 
from kafka.errors import KafkaError

def MakingRequest(url: str) -> str:
    URL = 'https://www.x-rates.com/table/?from=USD&amount=1'
    r = requests.get(URL)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        print("\033[92m Request was successfully done. The status code: {}".format(r.status_code))
        USDollarExchangeRateTable = soup.find_all('td')
        Time = soup.find_all('span', class_="ratesTimestamp")[0].text
        USDollar = soup.find_all('th', class_='rtHeader rtHeaderCurr')[0].text
        ValueUSDollar = soup.find_all('th', class_='rtHeader rtHeaderValues')[0].text
        return USDollarExchangeRateTable, Time, USDollar, ValueUSDollar
    else:   
        print(f"\033[91m Request wasn't successfully done. The status code: {r.status_code}")

def PullingDataFromWebsite():
    URL = 'https://www.x-rates.com/table/?from=USD&amount=1'
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def ConvertingListComprehensionToDictionary(Currency: list, Value: list) -> dict:
    my_dict = {Currency[i]: Value[i] for i in range(len(Currency))}
    return my_dict
  
def ExtractingDataAndSaveItToListComprehension(data: str) -> list:
    return [PercentageCurrencyValue.text for PercentageCurrencyValue in data]

def ExtractingConversionCurrency(conversioncurrency: str) -> list:
    return [str(ConversionCurrency)[:7:] for ConversionCurrency in conversioncurrency]

def ExtractingChangePercentage(changepercentage: str) -> list:
    return [PercentageValue.text for PercentageValue in changepercentage]

def DictionaryConversionRateChangePercentage():
    soup = PullingDataFromWebsite()
    PercentageChangeCurrency = soup.find_all(class_="currencyPairUL")[0].find_all('li')
    ConversionCurrencyPercentageChange = ExtractingDataAndSaveItToListComprehension(PercentageChangeCurrency)
    ConversionCurrency = ExtractingConversionCurrency(ConversionCurrencyPercentageChange)
    PercentageChange  = soup.find_all('span', {'class':['down','up']})
    ChangePercentage = ExtractingChangePercentage(PercentageChange) 
    RateChangePercentage = ConvertingListComprehensionToDictionary(ConversionCurrency,ChangePercentage) 
    return RateChangePercentage

def SaveToJSONfile(data: dict) -> json:
    timestr = time.strftime("%d-%m-%Y")
    try:
        with open(timestr + '-' +'PERCENT_CHANGE_IN_THE_LAST_24_HOURS.json', 'w') as file:
                json.dump(data, file)
    except FileNotFoundError as ex:
        print(ex)
       
def ConvertingDictToJSON(datadict: dict) -> json:
    JSONUSDollarExchangeRatesTable = json.dumps(datadict)
    JSONUSDollarExchangeRatesTable
    dataUSDollarExchangeRatesTable = json.loads(JSONUSDollarExchangeRatesTable) 
    return dataUSDollarExchangeRatesTable    

  
def CreateDataFrameFromJSONPercentageChange(json):
    dfPercentChangeIntheLast24Hours = pd.DataFrame.from_dict(json, orient="index")
    dfPercentChangeIntheLast24Hours.reset_index(inplace=True)
    dfPercentChangeIntheLast24Hours = dfPercentChangeIntheLast24Hours.set_axis(['ConversionCurrency', 'PercentChange'], axis=1)
    today_ts = pd.Timestamp.today()
    dfPercentChangeIntheLast24Hours['LOADINGDATA'] = today_ts
    dfPercentChangeIntheLast24Hours     
    return dfPercentChangeIntheLast24Hours       

def SaveToCSVFile(dataframe):
    timestr = time.strftime("%d-%m-%Y")
    CSV = dataframe.to_csv(timestr + '-' + 'PercentChangeIntheLast24Hours.csv')
    return CSV        

def finalExecutionOfRateChangePercentage():
    URL = 'https://www.x-rates.com/table/?from=USD&amount=1'
    MakingRequest(URL)
    RateChangePercentage = DictionaryConversionRateChangePercentage()
    SaveToJSONfile(RateChangePercentage)
    print(f"\033[93m the Dictionary of the Percetange of the Rate Change: \n {RateChangePercentage}")
    JSONConversionRateChangePercentage = ConvertingDictToJSON(RateChangePercentage)
    df = CreateDataFrameFromJSONPercentageChange(JSONConversionRateChangePercentage)
    print(f"'\033[96m' DataFrame of of the Percetange of the Rate Change: \n {df}")
    SaveToCSVFile(df)
    
def UploadDataMinioExchangeRatePercentageChange():
    timestr = time.strftime("%d-%m-%Y")
    URL = 'https://www.x-rates.com/table/?from=USD&amount=1'
    MakingRequest(URL)
    RateChangePercentage = DictionaryConversionRateChangePercentage()
    JSONConversionRateChangePercentage = ConvertingDictToJSON(RateChangePercentage)
    df = CreateDataFrameFromJSONPercentageChange(JSONConversionRateChangePercentage)
    try: 
        client = Minio(endpoint='host.docker.internal:9000', 
                access_key='kj4Ud2U786iqb8pI8IH9',  
                secret_key='ea4Cv2J0H7g0kpYqsNXNdT6QcuQlx24DfqL8Xxxq', 
                    secure=False)  
        if not client.bucket_exists("conversionrateexchange"):
            client.make_bucket("conversionrateexchange")
            print("\033[92m Bucket conversionrateexchange created successfully.")
              
    except Exception as err:
        print(f"Error occurred: {err}")   
    ListOfAllAccessibleBuckets = print(f"\033[94m Total buckets:  {len(client.list_buckets())}"),  
    csv_bytes = df.to_csv().encode('utf-8')
    csv_buffer = io.BytesIO(csv_bytes)
    try: 
        UploadCSVFileToObject = client.put_object("conversionrateexchange", 
                        timestr + '-' + 'RawDataPercentChangeIntheLast24Hours.csv',  
                        data=csv_buffer, 
                        length=len(csv_bytes), 
                        content_type='application/csv')
        
        objects = client.list_objects("conversionrateexchange")
        for obj in objects:
            ListObjectInformationOfBucket = print(f"\033[95m List of Bucket Object {obj}")
        return  UploadCSVFileToObject , ListObjectInformationOfBucket, ListOfAllAccessibleBuckets
    except Exception as err:
        print(f"Error occurred: {err}")


def CreateKafkaProducer():
    localhost = 'host.docker.internal:29092' 
    return KafkaProducer(bootstrap_servers=[localhost])

def PublishingPercentageChangeExchangeRateRecordsToTopic():
    producer = CreateKafkaProducer()
    topic_name = 'percentageexchangerate' # topic where the message will be published
    RateChangePercentage = DictionaryConversionRateChangePercentage()
    JSONConversionRateChangePercentage = ConvertingDictToJSON(RateChangePercentage)
 
    StreamingDataDictPercentageChangeExchangeRate = JSONConversionRateChangePercentage
    end_time = time.time() + 30 # the script will run for 120 seconds
    while True:
        if time.time() > end_time:
            break  
        producer.send(topic_name, json.dumps(StreamingDataDictPercentageChangeExchangeRate).encode('utf-8'))
        time.sleep(10)
        
    
if __name__ == "__main__":
    finalExecutionOfRateChangePercentage()
    print("\033[92m Data Conversion Rate Change Percentage was successfully saved as a CSV and JSON files")
    UploadDataMinioExchangeRatePercentageChange()
    print("\033[92m Data Conversion Rate Change Percentage was successfully loaded to an object in a bucket")
    PublishingPercentageChangeExchangeRateRecordsToTopic()
    print("\033[92m Publishing PercentageChangeExchangeRate events to Kafka Cluster")
    