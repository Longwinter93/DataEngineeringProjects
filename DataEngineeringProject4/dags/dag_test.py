from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator 
from WebScrapingPythonExchangeCurrency_test import UploadDataMinioExchangeCurrency


default_args = {
        'owner' : 'Lukasz',
        'retries': 5,
        'retry_delay': timedelta(minutes=5)

}


with DAG(
    default_args=default_args,
    dag_id='Test',
    description='Extracting Currency Exchange Rates and Conversion Rate Change Percentage. Creating Apache Cassandra Tables. Uploading Data in a Bucket ',
    start_date=datetime(2024,2, 17),
    schedule_interval='30 4 * * *'
) as dag:
   UploadingDataExchangeCurrencyInBucket= PythonOperator(
   task_id='Uploads_data_from_a_file_ExchangeCurrencyUSD_to_bucket',
   python_callable=UploadDataMinioExchangeCurrency
   )
    
        
    
     
   UploadingDataExchangeCurrencyInBucket
    
  
    
