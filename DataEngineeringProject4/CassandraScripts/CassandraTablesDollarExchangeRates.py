from cassandra.cluster import Cluster

def ConnectionToCassandra():
    try:
        cluster = Cluster(['cassandra'],port=9042)
        session = cluster.connect() 
       
    except Exception as e:
        print(e)
        
    return session

def Execution():
    session = ConnectionToCassandra()
    try:
        session.execute("""CREATE KEYSPACE IF NOT EXISTS ExchangeCurrency WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '1' };""")
    except Exception as e:
        print(e)


    

if __name__ == "__main__":
    ConnectionToCassandra()
    Execution()

    

   