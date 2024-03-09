Adding a new Data Engineering Project ;) 
The project is in the process of doing!

-- Writing descriptions what was done in each python scripts!!
--Trigger DAGs in Apache Airflow
-- how to do it : 
-- spark container ->
docker exec -it nameofcontainer /bin/bash
-- running bash script 
bash BashScriptForRunningPySparkScripts.sh 

pip install --upgrade pip
pip install -r requirements.txt
spark-submit --master local[2] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,com.datastax.spark:spark-cassandra-connector_2.12:3.4.1 LoadingConversionRateChangePercentageToTable.py
spark-submit --master local[2] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,com.datastax.spark:spark-cassandra-connector_2.12:3.4.1 LoadingExchangeCurrencyDataToTable.py