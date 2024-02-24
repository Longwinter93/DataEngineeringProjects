from bs4 import BeautifulSoup
import requests
import json
import time
import pandas as pd
import logging
import io  
from minio import Minio 

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
    



def SelectingData():
    soup = PullingDataFromWebsite()
    for Currency in soup.find_all('td'):
        print(Currency.text)
        
    currencies=soup.find_all('td')
    ListComprehension = [title.text for title in currencies]

    print(ListComprehension)
    
def SavingDataToListComprehensionCurrency(currency: list) -> list:
    return [title.text for title in currency[::3]]



def SavingDataToListComprehensionValues(ValuesOfCurrency: list) -> list:
    return [title.text for title in ValuesOfCurrency[1::3]]



def ConvertingListComprehensionToDictionary(Currency: list, Value: list) -> dict:
    my_dict = {Currency[i]: Value[i] for i in range(len(Currency))}
    return my_dict

def ConvertingListComprehensionToDicionary():
    soup = PullingDataFromWebsite()
    currencies=soup.find_all('td')
    SavingDataToListComprehensionCurrency(currencies)
    ListComprehensionCurrency = SavingDataToListComprehensionCurrency(currencies)
    Values = soup.find_all('td')
    ListComprehensionValuesOfCurrency = SavingDataToListComprehensionValues(Values)
    
    DictionaryDataCurrencyValues = ConvertingListComprehensionToDictionary(ListComprehensionCurrency,ListComprehensionValuesOfCurrency)
    ConvertingListComprehensionToDictionary(ListComprehensionCurrency,ListComprehensionValuesOfCurrency)

    return print(f"\033[94m'Dictionary of ExchangeRate: \n {ConvertingListComprehensionToDictionary(ListComprehensionCurrency,ListComprehensionValuesOfCurrency)}")
    
def DictionaryOfExchangeRate():
    soup = PullingDataFromWebsite()
    currencies=soup.find_all('td')
    SavingDataToListComprehensionCurrency(currencies)
    ListComprehensionCurrency = SavingDataToListComprehensionCurrency(currencies)
    Values = soup.find_all('td')
    ListComprehensionValuesOfCurrency = SavingDataToListComprehensionValues(Values)
    
    DictionaryDataCurrencyValues = ConvertingListComprehensionToDictionary(ListComprehensionCurrency,ListComprehensionValuesOfCurrency)
    return DictionaryDataCurrencyValues

def SaveToJSONfile(data: dict) -> json:
    timestr = time.strftime("%d-%m-%Y")
    try:
        with open(timestr + '-' +'US_DOLLAR_EXCHANGE_RATES_TABLE.json', 'w') as file:
                json.dump(data, file)
    except FileNotFoundError as ex:
        print(ex)
        
def ConvertingDictToJSON(datadict: dict) -> json:
    JSONUSDollarExchangeRatesTable = json.dumps(datadict)
    JSONUSDollarExchangeRatesTable
    dataUSDollarExchangeRatesTable = json.loads(JSONUSDollarExchangeRatesTable) 
    return dataUSDollarExchangeRatesTable

def CreateDataFrameFromJSON(json):
    dfUSDollarExchangeRates = pd.DataFrame.from_dict(json, orient="index")
    dfUSDollarExchangeRates.reset_index(inplace=True)
    dfUSDollarExchangeRates = dfUSDollarExchangeRates.set_axis(['Currency', 'Rate'], axis=1)
    USDollar =pd.DataFrame([{'Currency':'US Dollar', 'Rate':'1.0'}]) 
    dfUSDollarExchangeRates = pd.concat([USDollar, dfUSDollarExchangeRates], ignore_index=True)
    today_ts = pd.Timestamp.today()
    dfUSDollarExchangeRates['LOADINGDATA'] = today_ts
    
    return dfUSDollarExchangeRates
        
def PrintingDataFrameOfExchangeRate(): 
    DictionaryDataCurrencyValues = DictionaryOfExchangeRate()
    JSONCurrencyValues = ConvertingDictToJSON(DictionaryDataCurrencyValues)
    dfUSDollarExchangeRates = CreateDataFrameFromJSON(JSONCurrencyValues)
    df = CreateDataFrameFromJSON(JSONCurrencyValues) 
    return print(f"'\033[95m'DataFrame Of ExchangeRate: \n {df}")
        
def DataFrameOfExchangeRate(): 
    DictionaryDataCurrencyValues = DictionaryOfExchangeRate()
    JSONCurrencyValues = ConvertingDictToJSON(DictionaryDataCurrencyValues)
    dfUSDollarExchangeRates = CreateDataFrameFromJSON(JSONCurrencyValues)
    return CreateDataFrameFromJSON(JSONCurrencyValues)  

def SaveToCSVFile(dataframe):
    timestr = time.strftime("%d-%m-%Y")
    CSV = dataframe.to_csv(timestr + '-' + 'USDollarExchangeRates.csv')
    return CSV
    
    
def finalExecutionOfExchangeRate():
    URL = 'https://www.x-rates.com/table/?from=USD&amount=1'
    MakingRequest(URL)
    ConvertingListComprehensionToDicionary()
    DictionaryDataCurrencyValues = DictionaryOfExchangeRate()
    SaveToJSONfile(DictionaryDataCurrencyValues)
    dfUSDollarExchangeRates = DataFrameOfExchangeRate()
    PrintingDataFrameOfExchangeRate()
    SaveToCSVFile(dfUSDollarExchangeRates)

def UploadDataMinioExchangeCurrency():
    timestr = time.strftime("%d-%m-%Y")
    URL = 'https://www.x-rates.com/table/?from=USD&amount=1'
    MakingRequest(URL)
    DictionaryDataCurrencyValues = DictionaryOfExchangeRate()
    JSONCurrencyValues = ConvertingDictToJSON(DictionaryDataCurrencyValues)
    dfUSDollarExchangeRates = CreateDataFrameFromJSON(JSONCurrencyValues)
    df =  dfUSDollarExchangeRates
    try: 
        client = Minio(endpoint='host.docker.internal:9000', 
                access_key='VshGY8lcAXJbUs0c1FOD',  
                secret_key='9aGFZCb6P9ONsasQigboPzUYgF4Us3RP8J4Iu0uf', 
                    secure=False)  
        if not client.bucket_exists("usdollarexchangerates"):
            client.make_bucket("usdollarexchangerates")
            print("\033[92m Bucket usdollarexchangerates created successfully.")
              
    except Exception as err:
        print(f"Error occurred: {err}")
        
    ListOfAllAccessibleBuckets = print(f"\033[94m Total buckets:  {len(client.list_buckets())}"),  
    csv_bytes = df.to_csv().encode('utf-8')
    csv_buffer = io.BytesIO(csv_bytes)
    try: 
        UploadCSVFileToObject = client.put_object("usdollarexchangerates", 
                        timestr + '-' + 'RawDataUSDollarExchangeRates.csv',  
                        data=csv_buffer, 
                        length=len(csv_bytes), 
                        content_type='application/csv')
        
        objects = client.list_objects("conversionrateexchange")
        for obj in objects:
            ListObjectInformationOfBucket = print(f"\033[95m List of Bucket Object {obj}")
        return  UploadCSVFileToObject , ListObjectInformationOfBucket, ListOfAllAccessibleBuckets
    except Exception as err:
        print(f"Error occurred: {err}")


    
if __name__ == "__main__":
    finalExecutionOfExchangeRate()
    print("\033[92m Data ExchangeCurrency was successfully saved as a CSV and JSON files")
    UploadDataMinioExchangeCurrency()
    print("\033[92m Data ExchangeCurrency was successfully loaded to an object in a bucket")

    
    

    
    
