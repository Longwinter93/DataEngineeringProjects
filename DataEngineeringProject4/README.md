# MAIN GOAL OF PROJECT
The main goal of this project was to extract **US Dollar Exchange Rates Table** & **Percentage Change in the Last 24 Hours** tables from a website. Data is saved as CSV and JSON files and load into Object Storage. Next, data is emitted in a continuous incremental manner with the goal of low-latency processing in every fifth minute.
Finally, data is transformed and loaded then into tables. In addition, each step is recorded in databases by inserting records to tables.

## SHORT DESCRIPTION OF PROJECT
<br /> To start with, it is necessary to copy this repository in your local driver by typing:
<br /> ```git clone https://github.com/Longwinter93/DataEngineeringProjects```. 
<br /> A DataEngineeringProject4 folder belongs to this project. It is necessery to open this folder in your explorer to see _docker-compose.yaml_.
<br /> [A Docker Desktop](https://www.docker.com/products/docker-desktop/) is used to build and run container applications.
<br /> To run create and start these containers, it is necessery to execute a `docker compose up` command on the terminal.
<br />Data is extracted from a website. Next, data is saved as JSON and CSV files that are located in a [AirflowFolders](https://github.com/Longwinter93/DataEngineeringProjects/tree/main/DataEngineeringProject4/AirflowFolders)  and placed in buckets in MinIO Object Storage to organize objects. Before this step, it is essential to create access key in MinIO. Tables, where data will populate, are created in an Apache Cassandra database.
Then, data is written to Kafka Topic. Finally, all steps are recorded and this information is inserted in tables in an Apache Cassandra database. This workflow is represented as a DAG (a Directed Acyclic Graph) as well as is triggered by Apache Airflow. These steps are written by Python scripts that are located in a [dags folder](https://github.com/Longwinter93/DataEngineeringProjects/tree/main/DataEngineeringProject4/dags). 
_picture of it_
<br /> To run this DAG, it is necessary to open Airflow Webserver that is the User Interface of Airflow and run this DAG.
_picture of it_
<br />Spark reads data from Apache Kafka and saves it as a DataFrame that is a distributed collection of data grouped into named columns. These PySpark and Bash scripts are located in a [PySparkScriptsAndBashScript folder](https://github.com/Longwinter93/DataEngineeringProjects/tree/main/DataEngineeringProject4/PySparkScriptsAndBashScript). 
<br />To run this step, it is mandatory to run a bash script in a Spark container by using these bash commands in terminal:
+ ```docker ps``` _to show all running containers and find a spark container_
+ ```docker exec -it nameofsparkcontainer /bin/bash``` _to get a bash shell in the container_.
+ ```bash BashScriptForRunningPySparkScripts.sh ``` _to run this script to update pip, install packages with respect to [configuration file](https://github.com/Longwinter93/DataEngineeringProjects/blob/main/DataEngineeringProject4/requirements.txt), then run PySparkScripts_.
<br /> After a few transformations, a DataFrame is loaded to tables in Apache Cassandra.
<br /> This step is also recoreded in a table in Apache Cassandra.

## FINAL RESULT OF PROJECT
US Dollar Exchange Rates Tables and Percent Change in the Last 24 Hours are successfully saved as JSON and csv files in a [AirflowFolders folder](https://github.com/Longwinter93/DataEngineeringProjects/tree/main/DataEngineeringProject4/AirflowFolders).
CSV files are stored in MinIO Object Storage:.
DataFrames are also successfully loaded to tables in Apache Cassandra:
All steps are recorded and inserted in a table in Apache Cassandra:

### RUNNING THIS PROJECT MANUALLY
Instead of using a Bash script, it is feasible to run these commands in a bash shell in the Spark container:
```pip install --upgrade pip```
```pip install -r requirements.txt```
```spark-submit --master local[2] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,com.datastax.spark:spark-cassandra-connector_2.12:3.4.1 LoadingConversionRateChangePercentageToTable.py```
```spark-submit --master local[2] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,com.datastax.spark:spark-cassandra-connector_2.12:3.4.1 LoadingExchangeCurrencyDataToTable.py```


Adding a new Data Engineering Project ;) 
The project is in the process of doing!

-- Writing descriptions what was done in each python scripts!!
-- Making description in README then make a graph of this architecture
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