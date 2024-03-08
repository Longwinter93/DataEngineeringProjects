Adding a new Data Engineering Project ;) 
The project is in the process of doing!


-- implementing kafka - learning about it and it creates topic
-- correcting code and putting corrections on it
-- running automatically all script codes and download jar drivers automatically
-- Apache Airflow  - changes dag to make it different
-- write bash scrips to run in in command. 
-- try to extract these python scripts
-- taking data from minio automatically
-- adding records to postgresql that data was loaded etc to keep track of it
-- store data in Minio (docker compose)
-- putting json files in Minio
--putting data from spark to Minio
-- try to load this data to apache cassandra


-- how to do it : 
-- spark container ->
docker exec -it nameofcontainer /bin/bash
pip install --upgrade pip
pip install -r requirements.txt
spark-submit --master local[2] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,com.datastax.spark:spark-cassandra-connector_2.12:3.4.1 LoadingConversionRateChangePercentageToTable.py
spark-submit --master local[2] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,com.datastax.spark:spark-cassandra-connector_2.12:3.4.1 LoadingExchangeCurrencyDataToTable.py