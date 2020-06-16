from google.cloud import storage
import re
import gpxpy.gpx
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime
import mysql.connector
import numpy as np

bucket_name='storage-gpx-files'

logs="Main log" + str(datetime.now()) + ".txt"
logfile=open(logs,"w+")
logfile.write("Program GC_FileTransfer started at: " + str(datetime.now()) + "\n")
logfile.close()
print("Program started, " + str(datetime.now()))

def handleException(exp):
    string = str(datetime.now()) + exp
    print(string)
    logfile = open(logs, "a+")
    logfile.write(string + "\n")
    logfile.close()

def connectToDatabaseWithConnector():
    global flag_run
    try:
        mydb = mysql.connector.connect(
            host="34.89.143.164",
            user="root",
            passwd="cvMs_990",
            database="db_AnomalyDetection"
        )
        return mydb
    except Exception as e:
        handleException(" Exception in method mydb.cursor: " + str(e))
        flag_run = False
        return False

def executeQuery(query,cursor):
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        handleException("Exception in method cursor.execute: " + str(e))
        return False

def sendQuery(query,cursor):
    try:
        cursor.execute(query)
    except Exception as e:
        handleException("Exception in method cursor.execute: " + str(e))
        return False

client = storage.Client()

bucket = client.get_bucket(bucket_name)
blobs=client.list_blobs(bucket_name)

mydb=connectToDatabaseWithConnector()
if mydb==False:
    print("Exite...")
    exit()

cursor = mydb.cursor(buffered=True)
query = ("SELECT MAX(Ride_ID) as ID_MAX FROM Rides")
result=executeQuery(query,cursor)
Ride_ID = result[0][0]
if (Ride_ID == None): Ride_ID = 0

for blob in blobs:
    if blob.name.startswith("files-to-processed") and blob.name.endswith(".gpx"):
        print(blob.name)
        Age=""
        Gender=""
        if blob.name.startswith("files-to-processed/UNDEFINED"):
            pattern = "RANGE(.*?)/"
            Age = re.search(pattern, blob.name).group(1)
            if Age==None: Age="UNDEFINED"
            Gender="UNDEFINED"
        if blob.name.startswith("files-to-processed/MALE"):
            pattern = "RANGE(.*?)/"
            Age = re.search(pattern, blob.name).group(1)
            if Age==None: Age="UNDEFINED"
            Gender="MALE"
        if blob.name.startswith("files-to-processed/FEMALE"):
            pattern = "RANGE(.*?)/"
            Age = re.search(pattern, blob.name).group(1)
            if Age==None: Age="UNDEFINED"
            Gender="FEMALE"
        text=blob.download_as_string()
        t=str(text).split("b'",1)
        try:
            gpx = gpxpy.parse(t[1].rsplit("'",1)[0])
        except Exception as e:
            handleException("Exception in gpxParse, filename: " + blob.name + " " + str(e))
            continue
        columnsRides=["Gender","Age"]
        dfRide=pd.DataFrame([[Gender,Age]], columns=columnsRides)
        for track in gpx.tracks:
            for segment in track.segments:
                point_count=len(segment.points)
                if point_count>2:
                    Ride_ID += 1
                    count = 0
                    queryPoint=""

                    for point in segment.points:

                        time = str(point.time).split("+", 1)
                        count += 1
                        if count == 1:
                            queryPoint = "(" + str(Ride_ID) + ", " + str(point.latitude) + ", " + str(
                                point.longitude) + ", '" + time[0] + "')"
                        else:
                            queryPoint = queryPoint + ", (" + str(Ride_ID) + ", " + str(point.latitude) + ", " + str(
                                point.longitude) + ", '" + time[0] + "')"
                    queryRide = ("INSERT INTO Rides (Gender, Age) VALUES ('" + Gender + "', '" + Age + "')")
                    queryPoints=("INSERT INTO Points (Ride_ID, Latitude, Longitude, Date) "
                                   "VALUES " + queryPoint)
                    sendQuery(queryRide,cursor)
                    if sendQuery(queryPoints,cursor)==False:
                        query=("DELETE FROM Rides WHERE Ride_ID=" + str(Ride_ID))
                        sendQuery(query,cursor)
                        try:
                            source_bucket = client.bucket(bucket_name)
                            source_blob = source_bucket.blob(blob.name)
                            destinationBlobName = blob.name.replace("files-to-processed", "files-processed")
                            bucket.rename_blob(source_blob, destinationBlobName)
                        except Exception as e:
                            handleException(
                                "Error in method: rename blob, file_name: " + blob.name + ", error: " + str(e))
                    else:
                        try:
                            source_bucket = client.bucket(bucket_name)
                            source_blob = source_bucket.blob(blob.name)
                            destinationBlobName=blob.name.replace("files-to-processed","invalid-files")
                            bucket.rename_blob(source_blob,destinationBlobName)
                        except Exception as e:
                            handleException("Error in method: rename blob, file_name: " + blob.name + ", error: " + str(e))
                    mydb.commit()
cursor.close()


