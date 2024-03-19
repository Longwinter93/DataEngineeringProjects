# MAIN GOAL OF PROJECT
<br /><img src="https://github.com/Longwinter93/DataEngineeringProjects/blob/main/DataEngineeringProject2/Architecture.jpg" width="1000" height="300">
<br />The main goal of ***IoT Smoke Detection project*** is to monitor presence of smoke of fire based on the data collected from sensors. 
<br />Data is emitted at high volume in a continuous, incremental manner with the goal of low-latency processing.

## SHORT DESCRIPTION OF PROJECT
<br />Data was extracted from sensors and saved as CSV files. 
<br />**Pandas** was used to read csv files into DataFrame.
<br />Then, this DataFrame was converted to a JSON format in order to publish records to the **Kafka** Cluster.
<br />**Spark** was used to read data from Kafka. Data was also saved as a streaming DataFrame.
<br />Finally, these DataFrames were loaded to Data warehouse and saved as tables in **SQL Server**.

<br />In-depth analysis with detailed information is included in **KafkaProducerSmokeDetection.ipynb**, **KafkaConsumerSmokeDetection.ipynb** and **SparkStreamingSmokeDetectionData.ipynb**

## FINAL RESULT OF PROJECT
<br /> IoT Smoke Detection data was successfully load to SQL Server:
<br /><img src="https://github.com/Longwinter93/DataEngineeringProjects/blob/main/DataEngineeringProject2/DataSmokeDetection.jpg" width="1000" height="400">

###### To create this project, these sites were used [Apache Kafka](https://kafka.apache.org/), [Kafka-Python](https://kafka-python.readthedocs.io/en/master/), [Apache Spark](https://spark.apache.org/), [Structured Streaming + Kafka Integration Guide](https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html), [pandas](https://pandas.pydata.org/)
