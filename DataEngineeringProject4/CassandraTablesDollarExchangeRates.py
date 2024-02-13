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
        return session.execute("""CREATE KEYSPACE IF NOT EXISTS ExchangeCurrency WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '1' };""")
    except Exception as e:
        print(e)

def CreateTable():
    session = ConnectionToCassandra()
    session.set_keyspace('ExchangeCurrency')
    query = """CREATE TABLE IF NOT EXISTS ExchangeCurrency.USDollarExchangeRatesTable (
        id UUID  PRIMARY KEY,
        Currency text,
        ExchangeRate float,
        LoadingTimeData timestamp
        );"""
    try:
        return session.execute(query)
    except Exception as e:
        print(e)
        
def InsertData():
    session = ConnectionToCassandra()
    session.set_keyspace('ExchangeCurrency')
    query2 = """INSERT INTO ExchangeCurrency.USDollarExchangeRatesTable
    (Currency, ExchangeRate,LoadingTimeData )
    VALUES ("USD",82.23232, toTimeStamp(now()));"""
    try:
        return session.execute(query2)
    except Exception as e:
        print(e)
        

    
if __name__ == "__main__":
    ConnectionToCassandra()
    Execution()
    CreateTable()
    InsertData()

    

   