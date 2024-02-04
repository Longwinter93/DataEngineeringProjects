FROM apache/airflow:2.8.0


COPY requirements.txt .
#COPY requirements.txt /opt/bitnami/spark/ 
#COPY postgresqldriver/postgresql-42.2.5.jar /opt/bitnami/spark/jars/ 
#COPY PySparkScripts/LoadingExchangeRateDataToDWH.py /opt/bitnami/spark/
#COPY PySparkScripts/LoadingSymbolDataToDWH.py /opt/bitnami/spark/ 

RUN pip install --upgrade pip
RUN pip install -r requirements.txt