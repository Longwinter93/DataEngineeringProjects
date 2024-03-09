from pyspark import SparkContext
from pyspark.sql import SparkSession,functions, Window, Row
from pyspark.sql.functions import *
from pyspark.sql.types import IntegerType,BooleanType,DateType, TimestampType,LongType,DecimalType,  DoubleType, StringType, ArrayType, LongType,StructField, StructType
from pyspark.sql.types import StructType,StructField,FloatType,IntegerType,StringType
from pyspark.sql.functions import from_json,col,current_timestamp
from cassandra.cluster import Cluster



def SparkSessionStreamingData():
    try:
        spark = SparkSession \
        .builder \
        .appName("Streaming from Kafka") \
        .config("spark.streaming.stopGracefullyOnShutdown", True) \
        .config("spark.sql.shuffle.partitions", 4) \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,com.datastax.spark:spark-cassandra-connector_2.12:3.4.1") \
        .config("spark.cassandra.connection.host", "cassandra").config("spark.cassandra.connection.port","9042")\
        .config("spark.cassandra.auth.username", "cassandra") \
        .config("spark.cassandra.auth.password", "cassandra") \
        .config("spark.sql.extensions", "com.datastax.spark.connector.CassandraSparkExtensions") \
        .master("local[*]") \
        .getOrCreate()
        print("\033[92m Spark Session was successfully created")
    except  Exception:
        print("\033[91m Spark Session wasn't successfully created")
    return spark 

def ReadingDataFromKafka():
    topic_name = 'percentageexchangerate'
    localhost = 'host.docker.internal:29092'
    spark = SparkSessionStreamingData()
    try:
        df = spark \
            .read \
            .format("kafka") \
            .option("kafka.bootstrap.servers", localhost) \
            .option("subscribe", topic_name) \
            .load()
        print("\033[92m a Kafka Source for Streaming queries was successfully created")
    except Exception:
        print("\033[91m a Kafka Source for Streaming queries wasn't successfully created")
    return df  


def CreateDataFrameCurrency():
    df =ReadingDataFromKafka()
    schema = StructType([
        StructField("EUR/USD", StringType(),True),
        StructField("USD/JPY", StringType(),True),
        StructField("GBP/USD", StringType(),True),
        StructField("USD/CHF", StringType(),True),
        StructField("USD/CAD", StringType(),True),
        StructField("EUR/JPY", StringType(),True),
        StructField("AUD/USD", StringType(),True),
        StructField("CNY/USD", StringType(),True)
    ])
    df = df.selectExpr("CAST(value AS STRING) value").select(from_json(col("value"),schema).alias("data")).select("data.*")
    df = df.withColumn("id", monotonically_increasing_id())
    return df


def TransposeColumnsToRows():
    df = CreateDataFrameCurrency()
    columns = df.columns[:-1]
    df2 = df.melt(
        ids=["id"], 
        values=[columns],
        variableColumnName="conversionrate", 
        valueColumnName="percentagechange"
    ).filter(df['id'] == 0)
    
    df3 = df2.withColumn("id", monotonically_increasing_id()) \
    .withColumn("loadingtimedata", current_timestamp()) 
    
    return df3


def LoadingDataToDWH():
    df3 = TransposeColumnsToRows()
    LoadingDataFrameToTable = df3.write\
        .format("org.apache.spark.sql.cassandra")\
        .mode('append')\
        .options(table="percentagechangelast24hours", keyspace="exchangecurrency").save()
    return LoadingDataFrameToTable

def LoadingDataToRecordsTable():
    try:
        cluster = Cluster(['cassandra'],port=9042)
        session = cluster.connect() 
        session.set_keyspace('exchangecurrency')
        query = """INSERT INTO exchangecurrency.recordtable
        (id, nameoftransaction, timeofloadingdata)
        VALUES (5, 'A percentagechangelast24hours table was populated', toTimeStamp(now()));"""
        return session.execute(query)
    except Exception as e:
        print(e)       
    
if __name__ == "__main__":
    LoadingDataToDWH()
    print("Loading Conversion Rate Change Percentage Data To DWH was successfully done")
    LoadingDataToRecordsTable()
    print("Record Table was successfully populated")

    
    
