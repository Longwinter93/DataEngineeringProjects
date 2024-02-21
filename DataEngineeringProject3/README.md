# **SHORT DESCRIPTION OF PROJECT**
Data was extracting from a webiste using Python scripts that are located in a [dags folder]( https://github.com/Longwinter93/DataEngineeringProjects/tree/main/DataEngineeringProject3/dags).
It holds data values by using [dataclasses](https://docs.python.org/3/library/dataclasses.html), then data was saved as JSON files.
This task is run by Apache Airflow. 
A project contains a bash script (scripts/ApacheAirflowTrigger.sh). It triggers automatically a new DAG after creating a  **airflow-triggerer** container
Apache Kafka Producer was used to publish records to the Kafka Cluster. Then, a Kafka Consumer (client) consumes records from a Kafka Cluster. Then this data source was read by Structured Steaming Spark (PySpark)
Then, data was transformed and loaded to postgresql tables by using pyspark scripts  

## MANUAL INSTRUCTION
-- running 
1) docker compose up (creating and starting containers)
2) executing tasks in Apache Airflow
-- 
Airflow trigger
docker exec -it nameofcontainer  /bin/bash 
airflow dags list
airflow dags trigger Extracting_data
3) docker ps
4) docker exec -it nameofsparkcontainer /bin/bash
-- Installing requirements
5) pip install --upgrade pip
6) pip install -r requirements.txt
-- Running PySpark scripts
7) spark-submit --master local[2] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 LoadingExchangeRateDataToDWH.py

8) spark-submit --master local[2] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 LoadingSymbolDataToDWH.py

