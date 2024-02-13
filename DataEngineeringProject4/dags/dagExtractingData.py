from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator 
from WebScrapingPythonExchangeCurrency import finalExecutionOfExchangeRate
from WebScrapingPythonConversionRateChangePercentage import finalExecutionOfRateChangePercentage
from airflow.providers.postgres.operators.postgres import PostgresOperator
#from CassandraTablesDollarExchangeRates import ConnectionToCassandra

default_args = {
        'owner' : 'Lukasz',
        'retries': 5,
        'retry_delay': timedelta(minutes=5)

}


with DAG(
    default_args=default_args,
    dag_id='PullingCurrencyExchangeRateData',
    description='Extracting Currency Exchange Rates and Conversion Rate Change Percentage ',
    start_date=datetime(2024,2, 1),
    schedule_interval='30 4 * * *'
) as dag:
    CurrencyExchangeRate= PythonOperator(
    task_id='Extracing_data_CurrencyExchangeRates',
    python_callable=finalExecutionOfExchangeRate
    )
    ConversionRateChangePercentage= PythonOperator(
    task_id='Extracing_data_Conversion_Rate_Change_Percentage',
    python_callable=finalExecutionOfRateChangePercentage
    )

    
    
     
    CurrencyExchangeRate >> ConversionRateChangePercentage 
    
  
    
