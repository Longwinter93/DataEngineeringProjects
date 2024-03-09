from cassandra.cluster import Cluster
#Connection to Apache Cassandra
def ConnectionToCassandra():
    try:
        cluster = Cluster(['cassandra'],port=9042)
        session = cluster.connect() 
        return session
    except Exception as e:
        print(e)
    

def Execution():
    session = ConnectionToCassandra()
    try:
        return session.execute("""CREATE KEYSPACE IF NOT EXISTS exchangecurrency WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '1' };""")
    except Exception as e:
        print(e)
#Creating a record table that holds all information related to the process
def CreateRecordTable():
    session = ConnectionToCassandra()
    session.set_keyspace('exchangecurrency')
    query = """CREATE TABLE IF NOT EXISTS exchangecurrency.recordtable (
        id int,
        nameoftransaction text,
        timeofloadingdata timestamp,
        PRIMARY KEY (timeofloadingdata ,id ))
        WITH CLUSTERING ORDER BY (id ASC);"""
    try:
        return session.execute(query)
    except Exception as e:
        print(e)
        
#Inserting data that what was done       
def RegisteringFetchingData():
    session = ConnectionToCassandra()
    session.set_keyspace('exchangecurrency')
    query = """INSERT INTO exchangecurrency.recordtable
    (id, nameoftransaction, timeofloadingdata)
    VALUES (1, 'Exchange Currency and Percentage Conversion Exchange Rate were extracted from website', toTimeStamp(now()));"""
    try:
        session.execute(query)
    except Exception as e:
        print(e)  
        
              
def RegisteringMinioBucketWasCreated():
    session = ConnectionToCassandra()
    session.set_keyspace('exchangecurrency')
    query = """INSERT INTO exchangecurrency.recordtable
    (id, nameoftransaction, timeofloadingdata)
    VALUES (2, 'Buckets were created. JSON and CSV files were upload to Minio Buckets', toTimeStamp(now()));"""
    try:
        session.execute(query)
    except Exception as e:
        print(e)
        
        
def RegisteringTableWasCreated():
    session = ConnectionToCassandra()
    session.set_keyspace('exchangecurrency')
    query = """INSERT INTO exchangecurrency.recordtable
    (id, nameoftransaction, timeofloadingdata)
    VALUES (3, 'percentagechangelast24hours and usdollarexchangeratestable tables were created', toTimeStamp(now()));"""
    try:
        session.execute(query)
    except Exception as e:
        print(e)

def RegisteringKafkaPublishesRecordsToKafkaCluster():
    session = ConnectionToCassandra()
    session.set_keyspace('exchangecurrency')
    query = """INSERT INTO exchangecurrency.recordtable
    (id, nameoftransaction, timeofloadingdata)
    VALUES (4, 'Kafka Producer publishes events to Kafka', toTimeStamp(now()));"""
    try:
        session.execute(query)
    except Exception as e:
        print(e)

      
def FinalCreateTableRecordTableAndRegisteringRecords():
    ConnectionToCassandra()
    Execution()
    CreateRecordTable()
    print("\033[92m A RecordTable table was successfully created")
    RegisteringFetchingData()
    RegisteringMinioBucketWasCreated()
    RegisteringTableWasCreated()
    RegisteringKafkaPublishesRecordsToKafkaCluster()
    print("\033[92m Directed Acyclic Graph for these tasks were recorded in the table")
    
#Running this function if this file is run as a script from the command line. 
#However, if the file is imported from another file, this will not be executed.      
if __name__ == "__main__":
    FinalCreateTableRecordTableAndRegisteringRecords()
   


    

   