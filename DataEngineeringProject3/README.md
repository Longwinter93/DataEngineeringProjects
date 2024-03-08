# To be added:
<br /> DataFrame will be changed in order to load data in different ways (columns to rows)
<br />Adding JSON files to the description to show all steps of doing


# MAIN GOAL OF PROJECT
<img src="https://github.com/Longwinter93/DataEngineeringProjects/blob/main/DataEngineeringProject3/Architecture.jpg" width="1000" height="400">
<br /> The main goal of this project was to extract data from websites that holds Currency Exchange Rates for selected currencies where the base currency is Euro. Data is emitted in a continuous incremental manner with the goal of low-latency processing in every fifth minute.
<br />In addition, symbols for selected currencies were also extracted.
<br /> Next, data was transformed and loaded to a database in order to show the current exchange rate for selected currencies.

## **SHORT DESCRIPTION OF PROJECT**
<br /> To start with, it is necessary to copy this repository in your local driver by typing:
<br /> ```git clone https://github.com/Longwinter93/DataEngineeringProjects```. 
<br /> A DataEngineeringProject3 folder belongs to this project. It is necessery to open this folder in your explorer to see _docker-compose.yaml_.
<br /> [A Docker Desktop](https://www.docker.com/products/docker-desktop/) is used to build and run container applications.
<br /> To run create and start these containers, it is necessery to execute a `docker compose up` command on the terminal.
<br /> Data was extracting from a webiste using Python scripts that are located in a [dags folder](https://github.com/Longwinter93/DataEngineeringProjects/tree/main/DataEngineeringProject3/dags).
<br /> Python scripts are written to hold data values by using [dataclasses](https://docs.python.org/3/library/dataclasses.html), then data was saved as JSON files in a [AirflowFolders](https://github.com/Longwinter93/DataEngineeringProjects/tree/main/DataEngineeringProject3/AirflowFolders) folder.
<br />  This task is triggered by [Apache Airflow](https://airflow.apache.org/). 
<br />  This project contains a [ApacheAirflowTrigger](https://github.com/Longwinter93/DataEngineeringProjects/tree/main/DataEngineeringProject3/AirflowFolders) bash script.
<br /> This script triggers automatically a new DAG after creating a  **airflow-triggerer** container. 
<br /> [A Kafka client](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html) publishes records (Exchange Rate and Symbol data) to the Kafka Cluster at the same time.
<br /> Then, [PySpark](https://github.com/Longwinter93/DataEngineeringProjects/tree/main/DataEngineeringProject3/PySparkScripts) scripts are executed. It project also contains a [PySparkRunningScript](https://github.com/Longwinter93/DataEngineeringProjects/tree/main/DataEngineeringProject3) bash script. This script is executed automatically after creating a  **spark** container.
<br /> As a result, [A Kafka Consumer (client)](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html) consumes records (Exchange Rate and Symbol data) from a Kafka Cluster.
<br /> These records are read by [Structured Steaming Spark (PySpark)](https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html). Tables are created in a [Postgresql](https://www.postgresql.org/)  database in the meanwhile.
<br /> Finally, data was transformed and loaded to Postgresql tables by mentioned-above Pyspark scripts  

## **FINAL RESULT OF PROJECT**
<br /> Thanks to bash scripts, the whole process is automatically done.
<br /> Currency and symbol data is successfully saved as JSON files in a [AirflowFolders](https://github.com/Longwinter93/DataEngineeringProjects/tree/main/DataEngineeringProject3/AirflowFolders) folder 
<br /> As we can see, data is successfully loaded to tables in a Postgresql database
1. ![Currency](https://github.com/Longwinter93/DataEngineeringProjects/blob/main/DataEngineeringProject3/currency.jpg)
2. ![Symbol](https://github.com/Longwinter93/DataEngineeringProjects/blob/main/DataEngineeringProject3/symbol.jpg)

### MANUAL INSTRUCTION
<br /> It is also possible to run this project manually without adding bash scripts.
<br />To start with, it is necessary to run _docker compose up_ on the terminal in order to create and start containers in a  Docker.
<br />DAGs needs to be executed in a Apache Airflow webserver. We can also do it by running it by bash commands:

<br />1. ```docker ps``` (looking at running containers and finding a **airflow-triggerer** container)
<br />2. ```docker exec -it nameofairflowtriggerontainer  /bin/bash``` (it opens an **airflow-triggerer** container to run bash commands) 
<br />3. ```airflow dags list``` (it look for available a dag)
<br />4. ```airflow dags trigger Extracting_data``` (it triggers a dag)

<br /> Then, it is necessary to execute and run bash commands in a spark container:

<br />1. ```docker exec -it nameofsparkcontainer /bin/bash```
<br />2. ```pip install --upgrade pip``` (upgrading pip)
<br />3. ```pip install -r requirements.txt``` (installing packages)

<br /> Running PySpark scripts

<br />1. ```spark-submit --master local[2] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 LoadingExchangeRateDataToDWH.py```
<br />2. ```spark-submit --master local[2] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 LoadingSymbolDataToDWH.py```


###### To create this project, these sites were used [Apache Kafka](https://kafka.apache.org/),[Apache Airflow](https://airflow.apache.org/), [Kafka-Python](https://kafka-python.readthedocs.io/en/master/), [Docker Desktop](https://www.docker.com/products/docker-desktop/), [Apache Spark](https://spark.apache.org/),  [Structured Streaming + Kafka Integration Guide](https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html) & [PostgreSQL](https://www.postgresql.org/).