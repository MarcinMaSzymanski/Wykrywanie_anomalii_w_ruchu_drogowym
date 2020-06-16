import gpxpy.gpx
from sqlalchemy import create_engine
from sklearn.covariance import EllipticEnvelope
import mysql.connector
import pandas as pd
import threading
import schedule
import time
from datetime import datetime

ThreadName="Acceleration"
flag_run=False
run=True
logs="Main log" + str(datetime.now()) + ".txt"
logfile=open(logs,"w+")
logfile.write("Program main.py started at: " + str(datetime.now()) + "\n")
logfile.close()
print("Program started, " + str(datetime.now()))


db_connection_str = 'mysql+pymysql://root:cvMs_990@34.89.143.164:3306/Anomaly_detection'


def handleException(exp):
    string=str(datetime.now()) + exp
    print(string)
    logfile = open(logs, "a+")
    logfile.write(string + "\n")
    logfile.close()

def connectToMySqlWithPandas():
    global flag_run
    sqlEngine = create_engine(db_connection_str)
    try:
        dbConnection = sqlEngine.connect()
        return dbConnection
    except Exception as e:
        handleException(" Exception in method sqlEngine.connetct: " + str(e))
        flag_run = False
        return False

def connectToDatabaseWithCursor():
    global flag_run
    try:
        mydb = mysql.connector.connect(
            host="34.89.143.164",
            user="root",
            passwd="cvMs_990",
            database="Anomaly_detection"
        )

        return mydb
    except Exception as e:
        handleException(" Exception in method mydb.cursor: " + str(e))
        flag_run = False
        return False


def Acceleration():
    global flag_run
    sqlEngine = create_engine(db_connection_str)
    dbConnection = connectToMySqlWithPandas()
    mydb = connectToDatabaseWithCursor()
    cursor = mydb.cursor(buffered=True)
    try:
        rides = pd.read_sql("select Ride_ID FROM Rides WHERE Acceleration=FALSE AND InvalidData=FALSE ", dbConnection)
    except Exception as e:
        handleException("Exception in method pd.read_sql: " + str(e))
        flag_run = False
        return

    for row in rides.Ride_ID.values:
        try:
            points = pd.read_sql("select Point_ID, Latitude, Longitude, Date FROM Points WHERE Ride_ID=" + str(row), dbConnection)
        except Exception as e:
            handleException("Exception in method pd.read_sql: " + str(e))
        queryAcceleration=""
        firstPoint = None
        firstSpeed = None
        secondSpeed = None
        firstTime = None
        secondTime = None
        count = 0

        for point in points.values:
            count+=1
            p=gpxpy.gpx.GPXTrackPoint(point[1], point[2])
            p.time=point[3]
            if firstPoint == None:
                firstPoint = p
            else:
                secondPoint = firstPoint
                firstPoint = p
                if firstSpeed == None:
                    firstSpeed = firstPoint.speed_between(secondPoint)
                    firstTime = firstPoint.time_difference(secondPoint)
                    if firstSpeed == None:
                        firstPoint = secondPoint
                        firstTime = secondTime
                        firstSpeed = secondSpeed
                        continue
                else:
                    secondSpeed = firstSpeed
                    secondTime = firstTime
                    firstSpeed = firstPoint.speed_between(secondPoint)
                    firstTime = firstPoint.time_difference(secondPoint)
                    if firstSpeed == None:
                        firstPoint = secondPoint
                        firstTime = secondTime
                        firstSpeed = secondSpeed
                        continue
                    try:
                        acceleration = (firstSpeed - secondSpeed) / (firstTime + secondTime)
                    except:
                        firstPoint = secondPoint
                        firstTime = secondTime
                        firstSpeed = secondSpeed
                        continue
                    if count == 3:
                        queryAcceleration = "(" + str(row) + ", " + str(point[0] - 2) + ", " + str(point[0]) + ", '" + str(round(acceleration, 2)) + "')"
                    else:
                        queryAcceleration = queryAcceleration + ", (" + str(row) + ", " + str(point[0] - 2) + ", " + str(point[0]) + ", '" + str(round(acceleration, 2)) + "')"
        try:
            query = ("INSERT INTO Accelerations (Ride_ID, StartPoint_ID, EndPoint_ID, Acceleration) VALUES " + queryAcceleration)
            cursor.execute(query)
            mydb.commit()
            try:
                query = ("UPDATE Rides SET Acceleration=TRUE WHERE Ride_ID=" + str(row))
                cursor.execute(query)
                mydb.commit()
            except:
                handleException("Exception in change processed status, Ride_ID: " + str(row))
        except Exception as e:
            handleException("Exception in cursor.execute, Ride_ID: " + str(row) +  ", " + str(e))
            try:
                query = ("UPDATE Rides SET InvalidData=TRUE WHERE Ride_ID=" + str(row))
                cursor.execute(query)
                mydb.commit()
            except:
                handleException("Exception in change processed status, Ride_ID: " + str(row))
    cursor.close()
    dbConnection.close()

    flag_run=False
    print("Thread anomalies has ended. "  + str(datetime.now()))


def PreProcessing():
    global flag_run
    dbConnection = connectToMySqlWithPandas()
    mydb = connectToDatabaseWithCursor()
    cursor = mydb.cursor(buffered=True)
    try:
        rides = pd.read_sql("select Ride_ID FROM Rides WHERE Acceleration=True and PreProcessed=FALSE and InvalidData=False", dbConnection)
    except Exception as e:
        handleException(" Exception in method read_sql: " + str(e))
    for row in rides.Ride_ID.values:
        try:
            accelerations = pd.read_sql("select StartPoint_ID, EndPoint_ID, Acceleration FROM Accelerations WHERE Ride_ID=" + str(row), dbConnection)
        except Exception as e:
            handleException(" Exception in method read_sql, Ride_ID: "+ str(row) + str(e))
        queryAcceleration=""

        count = 0
        for acceleration in accelerations.values:
            if acceleration[2]<5 and acceleration[2]>-5:
                count+=1
                if count==1:
                    queryAcceleration = "(" + str(row) + ", " + str(acceleration[0]) + ", " + str(acceleration[1]) + ", '" + str(acceleration[2]) + "')"
                else:
                    queryAcceleration = queryAcceleration + ", (" + str(row) + ", " + str(acceleration[0]) + ", " + str(acceleration[1]) + ", '" + str(acceleration[2]) + "')"
        try:
            query = ("INSERT INTO Accelerations_PreProcessed (Ride_ID, StartPoint_ID, EndPoint_ID, Acceleration) VALUES " + queryAcceleration)
            cursor.execute(query)
            mydb.commit()
            try:
                query = ("UPDATE Rides SET PreProcessed=TRUE WHERE Ride_ID=" + str(row))
                cursor.execute(query)
                mydb.commit()
            except:
                handleException("Exception in change processed status, Ride_ID: " + str(row))
        except Exception as e:
            handleException("Exception in cursor.execute, Ride_ID: " + str(row) + ", " + str(e))
            try:
                query = ("UPDATE Rides SET InvalidData=TRUE WHERE Ride_ID=" + str(row))
                cursor.execute(query)
                mydb.commit()
            except:
                handleException("Exception in change processed status, Ride_ID: " + str(row))
    cursor.close()
    dbConnection.close()
    flag_run = False
    print("Thread anomalies has ended. "  + str(datetime.now()))


def anomalyDetection():
    global flag_run
    contam=0.005
    dbConnection = connectToMySqlWithPandas()
    mydb = connectToDatabaseWithCursor()
    cursor = mydb.cursor(buffered=True)
    rides = pd.read_sql(
        "select Ride_ID FROM Rides WHERE Acceleration=True and PreProcessed=TRUE and AnomalyDetection=FALSE and InvalidData=False", dbConnection)
    for row in rides.Ride_ID.values:
        try:
            accelerations = pd.read_sql(
                "select Acceleration FROM Accelerations_PreProcessed WHERE Ride_ID=" + str(row), dbConnection)
        except Exception as e:
            handleException("Exception in method read_sql, Ride_ID: " + str(row) + str(e))
        elliptic = EllipticEnvelope(contamination=contam)
        try:
            elliptic.fit(accelerations.Acceleration.values.reshape(-1, 1))
            ell = pd.DataFrame({'Acceleration': accelerations.Acceleration.values,
                                   'Outliers': elliptic.predict(accelerations.Acceleration.values.reshape(-1, 1))})
            result = (ell.loc[ell['Outliers'] == -1])
            local_min = result.loc[result['Acceleration'] < 0, 'Acceleration'].max()
        except Exception as e:
            handleException("Exception in anomaly detecting, Ride_ID: " + str(row) + str(e))

        try:
            query = (
                     "INSERT INTO Anomalies (Ride_ID, StartPoint_ID, EndPoint_ID, Acceleration) select Ride_ID, StartPoint_ID, EndPoint_ID, Acceleration FROM Accelerations_PreProcessed WHERE Acceleration<" + str(
                local_min) + " AND Ride_ID=" + str(row))
            cursor.execute(query)
            mydb.commit()
            try:
                query = ("UPDATE Rides SET AnomalyDetection=TRUE WHERE Ride_ID=" + str(row))
                cursor.execute(query)
                mydb.commit()
            except:
                handleException("Exception in change processed status, Ride_ID: " + str(row))
        except Exception as e:
            handleException("Exception in cursor.execute, Ride_ID: " + str(row) + ", " + str(e))
            try:
                query = ("UPDATE Rides SET InvalidData=TRUE WHERE Ride_ID=" + str(row))
                cursor.execute(query)
                mydb.commit()
            except:
                    handleException("Exception in change processed status, Ride_ID: " + str(row))
        try:
            query = ("UPDATE Rides SET InvalidData=TRUE WHERE Ride_ID=" + str(row))
            cursor.execute(query)
            mydb.commit()
        except:
            handleException("Exception in change processed status, Ride_ID: " + str(row))
    cursor.close()
    dbConnection.close()
    flag_run = False
    print("Thread anomalies has ended. "  + str(datetime.now()))

def countAnomalies():
    global flag_run
    dbConnection=connectToMySqlWithPandas()
    if not dbConnection:
        return
    try:
        anomalies = pd.read_sql("select Longitude, Latitude FROM PointAnomalies", dbConnection)
    except Exception as e:
        handleException(" Exception in method read_sql: " + str(e))
    a=anomalies.astype(float).round(4)
    count=a.groupby(a.columns.tolist()).size().reset_index().\
            rename(columns={0:'Count'})
    try:
        count.to_sql('Anomalies_locations', con=dbConnection, if_exists='append', index=False)
    except Exception as e:
        handleException(" Exception in method to_sql: " + str(e))
    print("Done")
def itsTime():
    global flag_run
    global ThreadName
    dbConnection = connectToMySqlWithPandas()
    count=[]
    try:
        acceleration=pd.read_sql("SELECT COUNT(*) FROM Rides WHERE Acceleration=False and InvalidData=False", dbConnection)
        preProcessed=pd.read_sql("SELECT COUNT(*) FROM Rides WHERE Acceleration=True and PreProcessed=False and InvalidData=FALSE", dbConnection)
        anomalyDetection = pd.read_sql(
            "SELECT COUNT(*) FROM Rides WHERE Acceleration=True and PreProcessed=True and AnomalyDetection=False and InvalidData=FALSE",
            dbConnection)

        count.append(acceleration.values[0][0])
        count.append(preProcessed.values[0][0])
        count.append(anomalyDetection.values[0][0])
    except Exception as e:
        handleException(" Exception in method read_sql: " + str(e))
        flag_run = False
        return
    maxi=max(count)
    if maxi==0:
        flag_run = False
    elif count[0]==maxi:
        flag_run=True
        ThreadName="Acceleration"
    elif count[1]==maxi:
        flag_run=True
        ThreadName="PreProcessing"
    elif count[2]==maxi:
        flag_run=True
        ThreadName="AnomalyDetection"
    dbConnection.close()

def startThread(threadName):
    if threadName=="Acceleration":
        thread = threading.Thread(target=Acceleration(), args=())
        thread.start()

    if threadName=="PreProcessing":
        thread = threading.Thread(target=PreProcessing(), args=())
        thread.start()
    if threadName=="AnomalyDetection":
        thread = threading.Thread(target=anomalyDetection(), args=())
        thread.start()
    print("Running thread: " + threadName + " " + str(datetime.now()))
schedule.every(5).minutes.do(itsTime)

# while(run):
#     schedule.run_pending()
#     if threading.activeCount()==1 and flag_run==True:
#         startThread(ThreadName)
#     elif threading.activeCount()==1 and flag_run==False:
#         print("Nothing to do here, " + str(datetime.now()))
#     time.sleep(60)
countAnomalies()


