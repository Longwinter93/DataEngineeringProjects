from time import sleep
from json import dumps, loads 
import json 
from kafka import KafkaConsumer
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField,FloatType,IntegerType,StringType
from pyspark.sql.functions import from_json,col,current_timestamp
from pyspark import SparkContext
import logging

#Defining SparkSession - the entry point to programming Spark with the Dataset and DataFrame API
#Adding required packages to read data from Apache Kafka and postgresql drivers to save a table there.
def SparkSessionStreamingData():
    try:
        spark = SparkSession \
        .builder \
        .appName("Streaming from Kafka") \
        .config("spark.streaming.stopGracefullyOnShutdown", True) \
        .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0') \
        .config("spark.sql.shuffle.partitions", 4) \
        .config("spark.jars", "/opt/spark/jars/postgresql-42.2.5.jar") \
        .master("local[*]") \
        .getOrCreate()
        print("\033[92m Spark Session was successfully created")
    except  Exception:
        print("\033[91m Spark Session wasn't successfully created")
    return spark 

#Creating a Kafka Source for Batch Queries
def ReadingDataFromKafkaSymbol():
    topic_name = 'Symbol'
    localhost = 'host.docker.internal:29092'
    spark = SparkSessionStreamingData()
    try:
        df = spark.read\
            .format("kafka") \
            .option("kafka.bootstrap.servers", localhost) \
            .option("subscribe", topic_name) \
            .option("delimeter",",") \
            .option("startingOffsets", "earliest") \
            .load()
        print("\033[92m a Kafka Source for Streaming queries was successfully created")
    except Exception:
        print("\033[91m a Kafka Source for Streaming queries wasn't successfully created")
    return df  

#Creating schema to read the JSON data and put it to DataFrame.
def CreateDataFrameSymbol():
    df = ReadingDataFromKafkaSymbol()
    schema = StructType([
        StructField("EUR", StringType(),True),
        StructField("SymbolEuro", StringType(),True),
        StructField("USD", StringType(),True),
        StructField("SymbolUSD", StringType(),True),
        StructField("GBP", StringType(),True),
        StructField("SymbolGBP", StringType(),True),
        StructField("PLN", StringType(),True),
        StructField("SymbolPLN", StringType(),True),
        StructField("SEK", StringType(),True),
        StructField("SymbolSEK", StringType(),True),
        StructField("CHF", StringType(),True),
        StructField("SymbolCHF", StringType(),True),
        StructField("INR", StringType(),True),
        StructField("SymbolINR", StringType(),True),
        StructField("CNY", StringType(),True),
         StructField("SymbolCNY", StringType(),True),
    ])
    df = df.selectExpr("CAST(value AS STRING) value").select(from_json(col("value"),schema).alias("data")).select("data.*")
    df = df.withColumn("LoadingDate", current_timestamp())
    print(df.show(truncate=False))
    return df 

#Saving DataFrame to a postgresql table
def LoadingDataSymbolToDWH():
    df = CreateDataFrameSymbol()
    dfSymbol = df.select("EUR", "SymbolEuro",
                           "USD", "SymbolUSD",
                           "GBP","SymbolGBP",
                           "PLN","SymbolPLN",
                           "SEK","SymbolSEK",
                           "CHF","SymbolCHF",
                           "INR","SymbolINR",
                           "CNY","SymbolCNY","LoadingDate").write.format("jdbc") \
    .option("url", "jdbc:postgresql://host.docker.internal:5432/postgres") \
    .option("driver", "org.postgresql.Driver").option("dbtable", "Symbol") \
    .option("user", "airflow").option("password", "airflow").mode("append").save()
    return dfSymbol

#Putting all functions to one function to easily execute it    
def finalexecutionDWH():
    LoadingDataSymbolToDWH()
    logging.info("LoadingDataToDWH")
    print("Loading Symbol Data To DWH was successfully done")

# a finalexecutionDWH() function will be executed only if the script is the main program
if __name__ == "__main__":
    finalexecutionDWH()