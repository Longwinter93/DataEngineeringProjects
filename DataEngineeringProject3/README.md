-- running 
1) docker compose up
2) executing tasks in Apache Airflow
3) docker ps
4) docker exec -it nameofsparkcontainer /bin/bash

5)  pip install --upgrade pip
6) pip install -r requirements.txt
7) spark-submit --master local[2] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 LoadingExchangeRateDataToDWH.py

8) spark-submit --master local[2] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 LoadingSymbolDataToDWH.py