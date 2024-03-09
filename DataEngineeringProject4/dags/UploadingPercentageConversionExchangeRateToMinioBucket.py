from WebScrapingPythonPercentageConversionExchangeRate import MakingRequest, DictionaryConversionRateChangePercentage,ConvertingDictToJSON, CreateDataFrameFromJSONPercentageChange 
from minio import Minio 
import time
import io  
import pandas as pd

#Uploading .csv files to a Minio bucket
def UploadDataMinioExchangeRatePercentageChange():
    timestr = time.strftime("%d-%m-%Y")
    URL = 'https://www.x-rates.com/table/?from=USD&amount=1'
    MakingRequest(URL)
    RateChangePercentage = DictionaryConversionRateChangePercentage()
    JSONConversionRateChangePercentage = ConvertingDictToJSON(RateChangePercentage)
    df = CreateDataFrameFromJSONPercentageChange(JSONConversionRateChangePercentage)
    try: 
        client = Minio(endpoint='host.docker.internal:9000', 
                access_key='PhMH2hUV5UZBbxpCXM6B',  
                secret_key='el3GZ80XG6pjjRhCKBLW5rnZFdyVJteQzlHNMGbR', 
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
        print("\033[92m Data Conversion Rate Change Percentage was successfully loaded to an object in a bucket")
        return  UploadCSVFileToObject , ListObjectInformationOfBucket, ListOfAllAccessibleBuckets
    except Exception as err:
        print(f"Error occurred: {err}")
        
        
#Running this function if this file is run as a script from the command line. 
#However, if the file is imported from another file, this will not be executed.               
if __name__ == "__main__":
    UploadDataMinioExchangeRatePercentageChange()
