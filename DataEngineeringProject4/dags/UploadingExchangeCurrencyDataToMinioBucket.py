from WebScrapingPythonExchangeCurrency import MakingRequest, DictionaryOfExchangeRate, ConvertingDictToJSON, CreateDataFrameFromJSON
import io  
import time
from minio import Minio 

#Creating a usdollarexchangerates bucket in Minio
#Uploading Exchange Currency .csv files to a Minio bucket
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
                access_key='jgvFHXbh8XJZUGZ13BL3',  
                secret_key='Q21MSxEIlnC6PZCkqYyuPX8BM7k2Mksd6h6GyuKs', 
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
        print("\033[92m Data ExchangeCurrency was successfully loaded to an object in a bucket")
        return  UploadCSVFileToObject , ListObjectInformationOfBucket, ListOfAllAccessibleBuckets
    except Exception as err:
        print(f"Error occurred: {err}")
        
#Running this function if this file is run as a script from the command line. 
#However, if the file is imported from another file, this will not be executed.        
if __name__ == "__main__":
    UploadDataMinioExchangeCurrency()
