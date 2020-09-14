#biblioteki zew
import gpxpy.gpx
import re
from google.cloud import storage
import pandas as pd

#biblioteki wew
import Queries.ridesQueries as rq
import Queries.pointsQueries as pq
import main as m

def processFile(blob, file, rideId):


    text = str(file).split("b'", 1)

    Age = ""
    Gender = ""
    if blob.name.startswith("files-to-processed/UNDEFINED"):
        pattern = "RANGE(.*?)/"
        # try:
        #     Age = re.search(pattern, blob.name).group(1)
        # except:
        #     Age = None
        # if Age == None: Age = "UNDEFINED"
        Gender = "UNDEFINED"
    if blob.name.startswith("files-to-processed/MALE"):
        pattern = "RANGE(.*?)/"
        try:
            Age = re.search(pattern, blob.name).group(1)
        except:
            Age = None
        if Age == None: Age = "UNDEFINED"
        Gender = "MALE"
    if blob.name.startswith("files-to-processed/FEMALE"):
        pattern = "RANGE(.*?)/"
        try:
            Age = re.search(pattern, blob.name).group(1)
        except:
            Age = None
        if Age == None: Age = "UNDEFINED"
        Gender = "FEMALE"

    try:
        gpx = gpxpy.parse(text[1].rsplit("'", 1)[0])
    except Exception as e:
        m.addLog("Error in parsing, filename: " + blob.name + ", exception: " + str(e))
        return False

    dictionaryPoints=dict()
    i=1
    for track in gpx.tracks:
        for segment in track.segments:
            if len(segment.points) > 0:
                for point in segment.points:
                    time = str(point.time).split("+", 1)
                    dictionaryPoints.update({ i : [str(rideId), str(point.latitude), str(point.longitude), time[0]]})
                    i+=1
    columnsPoints = ["ride", "latitude", "longitude", "date"]
    try:
        dfPoints = pd.DataFrame.from_dict(dictionaryPoints,orient='index',columns=columnsPoints)
    except Exception as e:
        m.addLog("Error in adding dictonary to dataframe, filename: " + blob.name + ", exception: " + str(e))
        return False

    columnsRides = ["gender", "age"]
    dfRide = pd.DataFrame([[Gender, Age]], columns=columnsRides)
    result = rq.addRide(dfRide)
    result = pq.addPoints(dfPoints)
    if not result:
        m.addLog("Error in adding points, filename: " + blob.name)
        return False
    else:
        return True
