from pyspark import SparkContext
from pyspark.sql import SparkSession,functions, Window
from pyspark.sql.functions import *
from pyspark.sql.types import IntegerType,BooleanType,DateType, TimestampType,LongType,DecimalType,  DoubleType, StringType, ArrayType, LongType,StructField, StructType
from pyspark.sql.types import StructType,StructField,FloatType,IntegerType,StringType
from pyspark.sql.functions import from_json,col,current_timestamp
import logging


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
    topic_name = 'exchangecurrency'
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
        StructField("Euro", DecimalType(38,2),True),
        StructField("British Pound", DecimalType(38,2),True),
        StructField("Indian Rupee", DecimalType(38,2),True),
        StructField("Australian Dollar", DecimalType(38,2),True),
        StructField("Canadian Dollar", DecimalType(38,2),True),
        StructField("Singapore Dollar", DecimalType(38,2),True),
        StructField("Swiss Franc", DecimalType(38,2),True),
        StructField("Malaysian Ringgit", DecimalType(38,2),True),
        StructField("Japanese Yen", DecimalType(38,2),True),
        StructField("Chinese Yuan Renminbi", DecimalType(38,2),True),
        StructField("Argentine Peso", DecimalType(38,2),True),
        StructField("Bahraini Dinar", DecimalType(38,2),True),
        StructField("Botswana Pula", DecimalType(38,2),True),
        StructField("Brazilian Real", DecimalType(38,2),True),
        StructField("Bruneian Dollar", DecimalType(38,2),True),
        StructField("Bulgarian Lev", DecimalType(38,2),True),
        StructField("Chilean Peso", DecimalType(38,2),True),
        StructField("Colombian Peso", DecimalType(38,2),True),
        StructField("Czech Koruna", DecimalType(38,2),True),
        StructField("Danish Krone", DecimalType(38,2),True),
        StructField("Hong Kong Dollar", DecimalType(38,2),True),
        StructField("Hungarian Forint", DecimalType(38,2),True),
        StructField("Icelandic Krona", DecimalType(38,2),True),
        StructField("Indonesian Rupiah", DecimalType(38,2),True),
        StructField("Iranian Rial", DecimalType(38,2),True),
        StructField("Israeli Shekel", DecimalType(38,2),True),
        StructField("Kazakhstani Tenge", DecimalType(38,2),True),
        StructField("South Korean Won", DecimalType(38,2),True),
        StructField("Kuwaiti Dinar", DecimalType(38,2),True),
        StructField("Libyan Dinar", DecimalType(38,2),True),
        StructField("Mauritian Rupee", DecimalType(38,2),True),
        StructField("Mexican Peso", DecimalType(38,2),True),
        StructField("Nepalese Rupee", DecimalType(38,2),True),
        StructField("New Zealand Dollar", DecimalType(38,2),True),
        StructField("Norwegian Krone", DecimalType(38,2),True),
        StructField("Omani Rial", DecimalType(38,2),True),
        StructField("Pakistani Rupee", DecimalType(38,2),True),
        StructField("Philippine Peso", DecimalType(38,2),True),
        StructField("Polish Zloty", DecimalType(38,2),True),
        StructField("Qatari Riyal", DecimalType(38,2),True),
        StructField("Romanian New Leu", DecimalType(38,2),True),
        StructField("Russian Ruble", DecimalType(38,2),True),
        StructField("Saudi Arabian Riyal", DecimalType(38,2),True),
        StructField("South African Rand", DecimalType(38,2),True),
        StructField("Sri Lankan Rupee", DecimalType(38,2),True),
        StructField("Swedish Krona", DecimalType(38,2),True),
        StructField("Taiwan New Dollar", DecimalType(38,2),True),
        StructField("Thai Baht", DecimalType(38,2),True),
        StructField("Trinidadian Dollar", DecimalType(38,2),True),
        StructField("Turkish Lira", DecimalType(38,2),True),
        StructField("Emirati Dirham", DecimalType(38,2),True),
        StructField("Venezuelan Bolivar", DecimalType(38,2),True)
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
        variableColumnName="currency", 
        valueColumnName="exchangerate"
    ).filter(df['id'] == 0)
    
    df3 = df2.withColumn("id", monotonically_increasing_id()) \
    .withColumn("loadingtimedata", current_timestamp())
    
    return df3
    
def LoadingDataToDWH():
    df3 = TransposeColumnsToRows()
    LoadingDataToTable = df3.write\
        .format("org.apache.spark.sql.cassandra")\
        .mode('append')\
        .options(table="usdollarexchangeratestable", keyspace="exchangecurrency").save()
    return LoadingDataToTable

if __name__ == "__main__":
    LoadingDataToDWH()
    logging.info("A usdollarexchangeratestable was successfully populated.")
    print("Loading Exchange Currency Data To DWH was successfully done")