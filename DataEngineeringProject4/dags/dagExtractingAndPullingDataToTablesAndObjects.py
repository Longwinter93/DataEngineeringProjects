from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator 
from WebScrapingPythonExchangeCurrency import finalExecutionOfExchangeRate
from UploadingExchangeCurrencyDataToMinioBucket import UploadDataMinioExchangeCurrency
from PublishingExchangeCurrencyRecordsToKafkaCluster import PublishingUSDollarExchangeRatesRecordsToTopic
from WebScrapingPythonPercentageConversionExchangeRate import finalExecutionOfRateChangePercentage
from UploadingPercentageConversionExchangeRateToMinioBucket import UploadDataMinioExchangeRatePercentageChange
from PublishingPercentageConversionExchangeRateToKafkaCluster import PublishingPercentageChangeExchangeRateRecordsToTopic
from CassandraTablePercentageChangeLast24Hours import FinalCreateTablePercentacheChangeCassandra
from CassandraTablesDollarExchangeRates import  FinalCreateTableDollarExchangeRates
from CassandraRecordsTable import FinalCreateTableRecordTableAndRegisteringRecords

#Creating a basic pipeline:
#A dictionary of default parameters were defined to use to create tasks
default_args = {
        'owner' : 'Lukasz',
        'retries': 5,
        'retry_delay': timedelta(minutes=5)
        }

#Declaring DAG (directed acyclic graph) with a collection of operators, tasks with directional dependencies
with DAG(
    default_args=default_args,
    dag_id='PullingCurrencyExchangeRateDataCreatingApacheCassandraTablesUploadingDataInBucket',
    description='Extracting Currency Exchange Rates and Conversion Rate Change Percentage. Creating Apache Cassandra Tables. Uploading Data in a Bucket ',
    start_date=datetime(2024,3, 16),
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
   CreateTablePercentacheChangeCassandra= PythonOperator(
   task_id='Create_Table_Percentage_Change_Cassandra',
   python_callable=FinalCreateTablePercentacheChangeCassandra
   )
   CreateTableDollarExchangeRates= PythonOperator(
   task_id='Create_Table_Dollar_Exchange_Rates',
   python_callable=FinalCreateTableDollarExchangeRates
   )
   UploadingDataExchangeRatePercentageChangeInBucket= PythonOperator(
   task_id='Uploads_data_from_a_file_ExchangeRatePercentageChange24h_to_bucket',
   python_callable=UploadDataMinioExchangeRatePercentageChange
   )
   UploadingDataExchangeCurrencyInBucket= PythonOperator(
   task_id='Uploads_data_from_a_file_ExchangeCurrencyUSD_to_bucket',
   python_callable=UploadDataMinioExchangeCurrency
   )
   PublishingRecordsToTheKafkaClusterConversionRateExchange= PythonOperator(
   task_id='Publishing_ConversionExchangeRate_Data_To_Kafka_Cluster',
   python_callable=PublishingPercentageChangeExchangeRateRecordsToTopic
   )
   PublishingRecordsToTheKafkaClusterExchangeCurrency= PythonOperator(
   task_id='Publishing_Exchange_Curerncy_Data_To_Kafka_Cluster',
   python_callable=PublishingUSDollarExchangeRatesRecordsToTopic
   )
   RecordingDAGs= PythonOperator(
   task_id='RecordingDAGSInATable',
   python_callable=FinalCreateTableRecordTableAndRegisteringRecords
   )
    
   [UploadingDataExchangeCurrencyInBucket,  CurrencyExchangeRate] >> CreateTableDollarExchangeRates >> PublishingRecordsToTheKafkaClusterExchangeCurrency  >> RecordingDAGs
   [UploadingDataExchangeRatePercentageChangeInBucket,  ConversionRateChangePercentage ] >>  CreateTablePercentacheChangeCassandra  >> PublishingRecordsToTheKafkaClusterConversionRateExchange >> RecordingDAGs