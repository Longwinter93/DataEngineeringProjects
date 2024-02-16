from bs4 import BeautifulSoup
import requests
import json
import time
import pandas as pd
import logging
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
    
def UploadDataMinio():
    URL = 'https://www.x-rates.com/table/?from=USD&amount=1'
    MakingRequest(URL)
    RateChangePercentage = DictionaryConversionRateChangePercentage()
    JSONConversionRateChangePercentage = ConvertingDictToJSON(RateChangePercentage)
    df = CreateDataFrameFromJSONPercentageChange(JSONConversionRateChangePercentage)
    client = Minio(endpoint='localhost:9000', 
               access_key='b7Cfjwg7tnHB9AQU2FaA',  
               secret_key='Yk6QhHX0Y4HQPvvZFLvvg6gm07MYA6yAXULKssQ2', 
                secure=False)    
    return print("Total buckets: ", len(client.list_buckets())),client.fput_object("bucketname","data.csv" ,SaveToCSVFile(df))

    
if __name__ == "__main__":
    finalExecutionOfRateChangePercentage()
    UploadDataMinio()
    
