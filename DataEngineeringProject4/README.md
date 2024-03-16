# MAIN GOAL OF PROJECT
<img src="https://github.com/Longwinter93/DataEngineeringProjects/blob/main/DataEngineeringProject3/Architecture.jpg" width="1000" height="400">
The main goal of this project was to extract **US Dollar Exchange Rates Table** & **Percentage Change in the Last 24 Hours** tables from a website. <br />Data is saved as CSV and JSON files and load into Object Storage. <br />Next, data is emitted in a continuous incremental manner with the goal of low-latency processing in every fifth minute.
<br />Finally, data is transformed and loaded then into tables. <br />In addition, each step is recorded in databases by inserting records to tables.

## SHORT DESCRIPTION OF PROJECT
<br /> To start with, it is necessary to copy this repository in your local driver by typing:
<br /> ```git clone https://github.com/Longwinter93/DataEngineeringProjects```. 
<br /> A **DataEngineeringProject4** folder belongs to this project. It is necessery to open this folder in your explorer to see _docker-compose.yaml_.
<br /> [A Docker Desktop](https://www.docker.com/products/docker-desktop/) is used to build and run container applications.
<br /> To run create and start these containers, it is necessery to execute a `docker compose up` command on the terminal.
<br />Data is extracted from a website. <br />Next, data is saved as JSON and CSV files that are located in a [AirflowFolders](https://github.com/Longwinter93/DataEngineeringProjects/tree/main/DataEngineeringProject4/AirflowFolders) and placed in buckets in [MinIO Object Storage](https://min.io/) to organize objects. Before this step, it is essential to create access key in MinIO and implement it on Python scripts.<br />Tables, where data will populate, are created in an [Apache Cassandra database](https://cassandra.apache.org/_/index.html).
<br />Then, data is written to [Kafka](https://kafka.apache.org/) Topic. <br />Finally, all steps are recorded and this information is inserted in tables in an Apache Cassandra database. <br />This workflow is represented as a **DAG** (a Directed Acyclic Graph) as well as is triggered by [Apache Airflow](https://airflow.apache.org/). <br />These steps are written by Python scripts that are located in a [dags folder](https://github.com/Longwinter93/DataEngineeringProjects/tree/main/DataEngineeringProject4/dags). 
<img src="https://github.com/Longwinter93/DataEngineeringProjects/blob/main/DataEngineeringProject4/ApacheAirflowDAG.jpg" width="600" height="400">
<br /> To run this DAG, it is necessary to open Airflow Webserver that is the User Interface of Airflow and run this DAG.
<br />[Spark](https://spark.apache.org/) reads data from Apache Kafka and saves it as a DataFrame that is a distributed collection of data grouped into named columns. These PySpark and Bash scripts are located in a [PySparkScriptsAndBashScript folder](https://github.com/Longwinter93/DataEngineeringProjects/tree/main/DataEngineeringProject4/PySparkScriptsAndBashScript). 
<br />To run this step, it is mandatory to run a bash script in a Spark container by using these bash commands in terminal:
- ```docker ps``` _to show all running containers and find a spark container_
- ```docker exec -it nameofsparkcontainer /bin/bash``` _to get a bash shell in the container_.
- ```bash BashScriptForRunningPySparkScripts.sh ``` _to run this script to update pip, install packages with respect to [configuration file](https://github.com/Longwinter93/DataEngineeringProjects/blob/main/DataEngineeringProject4/requirements.txt), then run PySparkScripts_.

<br />After a few transformations, a DataFrame is loaded to tables in Apache Cassandra.
<br />This step is also recorded in a table in Apache Cassandra.
<br />All steps are also described in all Python scripts.

## FINAL RESULT OF PROJECT
- US Dollar Exchange Rates Tables and Percent Change in the Last 24 Hours are successfully saved as JSON and csv files in a [AirflowFolders folder](https://github.com/Longwinter93/DataEngineeringProjects/tree/main/DataEngineeringProject4/AirflowFolders).
- CSV files are stored in MinIO Object Storage:
<img src="https://github.com/Longwinter93/DataEngineeringProjects/blob/main/DataEngineeringProject4/MinIOObjectStorage.jpg" width="600" height="400">.
- DataFrames are also successfully loaded to tables in Apache Cassandra:
<img src="https://github.com/Longwinter93/DataEngineeringProjects/blob/main/DataEngineeringProject4/ExchangeCurrencyTables.jpg" width="600" height="400">
- All steps are recorded and inserted in a table in Apache Cassandra:
<img src="https://github.com/Longwinter93/DataEngineeringProjects/blob/main/DataEngineeringProject4/RecordTables.jpg" width="600" height="400">
## RUNNING THIS PROJECT MANUALLY
<br />Instead of using a Bash script, it is feasible to run these commands in a bash shell in the Spark container:
- ```pip install --upgrade pip```
- ```pip install -r requirements.txt```
- ```spark-submit --master local[2] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,com.datastax.spark:spark-cassandra-connector_2.12:3.4.1 LoadingConversionRateChangePercentageToTable.py```
- ```spark-submit --master local[2] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,com.datastax.spark:spark-cassandra-connector_2.12:3.4.1 LoadingExchangeCurrencyDataToTable.py```

###### To create this project, these sites were used [Apache Kafka](https://kafka.apache.org/), [Apache Airflow](https://airflow.apache.org/), [Kafka-Python](https://kafka-python.readthedocs.io/en/master/), [Docker Desktop](https://www.docker.com/products/docker-desktop/),  [Apache Spark](https://spark.apache.org/), [MinIO](https://min.io/), [Structured Streaming + Kafka Integration Guide](https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html) & [Apache Cassandra database](https://cassandra.apache.org/_/index.html).
