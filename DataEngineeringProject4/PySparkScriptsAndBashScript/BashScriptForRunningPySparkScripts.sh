pip install --upgrade pip | tr -d '\r'
pip install -r requirements.txt | tr -d '\r'
spark-submit --master local[2] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,com.datastax.spark:spark-cassandra-connector_2.12:3.4.1 LoadingConversionRateChangePercentageToTable.py | tr -d '\r'
spark-submit --master local[2] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,com.datastax.spark:spark-cassandra-connector_2.12:3.4.1 LoadingExchangeCurrencyDataToTable.py | tr -d '\r'