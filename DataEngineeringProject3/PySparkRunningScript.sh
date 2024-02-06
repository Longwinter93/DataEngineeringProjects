sleep 90
pip install --upgrade pip
pip install -r requirements.txt
spark-submit --master local[2] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 LoadingExchangeRateDataToDWH.py
spark-submit --master local[2] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 LoadingSymbolDataToDWH.py