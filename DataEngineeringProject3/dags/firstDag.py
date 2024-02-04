from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator 
from symbolData import finalExecutionSymbol
from exchangeRate import finalExecutionExchangeRate


default_args = {
        'owner' : 'Lukasz',
        'retries': 5,
        'retry_delay': timedelta(minutes=5)

}


with DAG(
    default_args=default_args,
    dag_id='Extracting_data',
    description='Extracting currency data Exchange Rate and Symbol  from website and save it on a JSON file',
    start_date=datetime(2024,2, 1),
    schedule_interval='30 4 * * *'
) as dag:
    ExchangeRate= PythonOperator(
    task_id='Extracing_data_ExchangeRate',
    python_callable=finalExecutionExchangeRate
    )
    Symbol= PythonOperator(
    task_id='Extracing_data_Symbol',
    python_callable=finalExecutionSymbol
    )
    
    
     
    ExchangeRate >> Symbol

