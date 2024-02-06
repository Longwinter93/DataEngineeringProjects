Data was extracting from a webiste using Python scripts (holding data values using dataclasses) and was saved in a JSON file.
This task is run by Apache Airflow. 
Apache Kafka Producer was used to publish records to the Kafka Cluster. Then, a Kafka Consumer (client) consumes records from a Kafka Cluster. Then this data source was read by Structured Steaming Spark (PySpark)
Then, data was transformed and loaded to postgresql tables by using pyspark scripts  

-- running 
1) docker compose up
2) executing tasks in Apache Airflow
3) docker ps
4) docker exec -it nameofsparkcontainer /bin/bash

5) pip install --upgrade pip
6) pip install -r requirements.txt
7) spark-submit --master local[2] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 LoadingExchangeRateDataToDWH.py

8) spark-submit --master local[2] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 LoadingSymbolDataToDWH.py


-- Apache airflow 
Airflow trigger
docker exec -it nameofcontainer  /bin/bash 
airflow dags list
airflow dags trigger Extracting_data
--
bash PySparkRunningScript.sh 