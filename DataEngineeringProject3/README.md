# MAIN GOAL OF PROJECT
<br /> The main goal of this project was to extract data from websites that holds Currency Exchange Rates for selected currencies where the base currency is Euro every day. 
<br />In addition, symbols for selected currencies were also extracted.
<br /> Next, data was transformed and loaded to a database in order to show the current exchange rate for selected currencies.

## **SHORT DESCRIPTION OF PROJECT**
<br /> To start with, it is necessary to copy this repository in your local driver by typing:
<br /> _git clone https://github.com/Longwinter93/DataEngineeringProjects/tree/main/DataEngineeringProject3_
<br /> [A Docker Desktop](https://www.docker.com/products/docker-desktop/) is used to build and run container applications. To run create and start these containers, it is necessery to execute a `docker compose up` command on the terminal.
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
<br /> As we can see, data is successfully loaded to tables in a Postgresql database
1. ![Currency](https://github.com/Longwinter93/DataEngineeringProjects/blob/main/DataEngineeringProject3/currency.jpg)
2. ![Symbol](https://github.com/Longwinter93/DataEngineeringProjects/blob/main/DataEngineeringProject3/symbol.jpg)

### MANUAL INSTRUCTION
<br /> It is also possible to run this project manually without adding bash scripts.
<br />To start with, it is necessary to run _docker compose up_ on the terminal in order to create and start containers in a  Docker.
<br />DAGs needs to be executed in a Apache Airflow webserver. We can also do it by running it by bash commands:
1. _docker ps_ (looking at running containers and finding a **airflow-triggerer** container)
2. _docker exec -it nameofairflowtriggerontainer  /bin/bash_ (it opens an **airflow-triggerer** container to run bash commands) 
3. _airflow dags list_ (it look for available a dag)
4. _airflow dags trigger Extracting_data_ (it triggers a dag)

<br /> Then, it is necessary to execute and run bash commands in a spark container:

1) _docker exec -it nameofsparkcontainer /bin/bash_
5) _pip install --upgrade pip_ (upgrading pip)
6) _pip install -r requirements.txt_ (installing packages)

<br /> Running PySpark scripts

1) _spark-submit --master local[2] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 LoadingExchangeRateDataToDWH.py_
2) _spark-submit --master local[2] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 LoadingSymbolDataToDWH.py_


###### To create this project, these sites were used [Apache Kafka](https://kafka.apache.org/),[Apache Airflow](https://airflow.apache.org/), [Kafka-Python](https://kafka-python.readthedocs.io/en/master/), [Docker Desktop](https://www.docker.com/products/docker-desktop/), [Apache Spark](https://spark.apache.org/),  [Structured Streaming + Kafka Integration Guide](https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html) & [PostgreSQL](https://www.postgresql.org/).