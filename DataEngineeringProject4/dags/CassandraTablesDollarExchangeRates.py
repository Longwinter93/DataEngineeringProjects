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
        return session.execute("""CREATE KEYSPACE IF NOT EXISTS exchangecurrency WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '1' };""")
    except Exception as e:
        print(e)

def CreateTable():
    session = ConnectionToCassandra()
    session.set_keyspace('exchangecurrency')
    query = """CREATE TABLE IF NOT EXISTS exchangecurrency.USDollarExchangeRatesTable (
        id int PRIMARY KEY, 
        Currency text,
        ExchangeRate float,
        LoadingTimeData timestamp
        );"""
    try:
        return session.execute(query)
    except Exception as e:
        print(e)
        
def FinalCreateTableDollarExchangeRates():
    ConnectionToCassandra()
    Execution()
    CreateTable()


if __name__ == "__main__":
    FinalCreateTableDollarExchangeRates()


    

   