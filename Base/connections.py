#biblioteki zew
from configparser import ConfigParser
import pandas as pd
from sqlalchemy import create_engine
import pymysql

#moduly wew
import main as m

parser = ConfigParser()
parser.read('config.ini')

mySqlServer = {
        "host": parser.get('MySQLConnector', 'host'),
        "port": parser.get('MySQLConnector', 'port'),
        "user": parser.get('MySQLConnector', 'user'),
        "password": parser.get('MySQLConnector', 'password'),
        "dbname": parser.get('MySQLConnector', 'dbname')
    }

mySqlConnectionString = 'mysql+pymysql://' + mySqlServer["user"] + ':' + mySqlServer["password"] + '@' + mySqlServer["host"] + '/' + mySqlServer["dbname"]

mySqlEngine = create_engine(mySqlConnectionString)

bucketName = parser.get('StorageConnector', 'bucketName')



def readQuery(query):
    mySqlConnention = mySqlEngine.connect()
    try:
        result = pd.read_sql(query, mySqlConnention)
    except:
        result = None
    mySqlConnention.close()
    return result

def executeQuery(df, table):
    try:
        df.to_sql(table, con=mySqlEngine, if_exists='append', index=False)
        result = True
    except Exception as e:
        print(e)
        result = False
    return result

def updateQuery(query):
    try:
        mySqlEngine.execute(query)
        result = True
    except Exception as e:
        result = False
        print(str(e))
    return result

def setFileAsIncorrect(blob):
    sourceBlob = sourceBucket.blob(blob.name)
    destinationBlobName = blob.name.replace("files-to-processed", "files-incorrect")
    try:
        bucket.rename_blob(sourceBlob, destinationBlobName)
    except Exception as e:
        m.addLog("Error in moving file: " + str(e))
        bucket.rename_blob(sourceBlob, destinationBlobName)
        try:
            bucket.rename_blob(sourceBlob, destinationBlobName)
        except Exception as e:
            m.addLog("Error in moving file: " + str(e))
            return False
    return True

def setFileAsProcessed(blob):
    sourceBlob = sourceBucket.blob(blob.name)
    destinationBlobName = blob.name.replace("files-to-processed", "files-processed")
    try:
        bucket.rename_blob(sourceBlob, destinationBlobName)
    except Exception as e:
        m.addLog("Error in moving file: " + str(e))
        bucket.rename_blob(sourceBlob, destinationBlobName)
        try:
            bucket.rename_blob(sourceBlob, destinationBlobName)
        except Exception as e:
            m.addLog("Error in moving file: " + str(e))
            return False
    return True