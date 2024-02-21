# MAIN GOAL OF PROJECT
<br /> The main goal of this project was to extract data from websites that holds Currency Exchange Rates for selected currencies where the base currency is Euro. In addition, symbols for selected currencies were also extracted.
<br /> Next, data was transformed and loaded to a database in order to show the current exchange rate for selected currencies.

## **SHORT DESCRIPTION OF PROJECT**

<br /> Data was extracting from a webiste using Python scripts that are located in a [dags folder](https://github.com/Longwinter93/DataEngineeringProjects/tree/main/DataEngineeringProject3/dags).
<br /> It holds data values by using [dataclasses](https://docs.python.org/3/library/dataclasses.html), then data was saved as JSON files.
<br />  This task is run by [Apache Airflow](https://airflow.apache.org/). 
<br />  This project contains  [ApacheAirflowTrigger](https://github.com/Longwinter93/DataEngineeringProjects/tree/main/DataEngineeringProject3/AirflowFolders) bash script.
<br /> It triggers automatically a new DAG after creating a  **airflow-triggerer** container. 
<br /> A Kafka client publishes records (Exchange Rate and Symbol data) to the Kafka Cluster at the same time.
<br /> Then, [PySpark](https://github.com/Longwinter93/DataEngineeringProjects/tree/main/DataEngineeringProject3/PySparkScripts) scripts are executed. It project also contains a [PySparkRunningScript] bash script(https://github.com/Longwinter93/DataEngineeringProjects/tree/main/DataEngineeringProject3). This script is executed automatically after creating a  **spark** container.
<br /> As a result, A Kafka Consumer (client) consumes records (Exchange Rate and Symbol data) from a Kafka Cluster.
<br /> These records were read by Structured Steaming Spark (PySpark). Tables are created in a Postgresql database in the meanwhile.
<br /> Finally, data was transformed and loaded to Postgresql tables by mentioned-above Pyspark scripts  

### MANUAL INSTRUCTION
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

