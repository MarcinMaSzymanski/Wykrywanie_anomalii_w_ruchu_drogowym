# biblioteki zew
import gpxpy.gpx
import pandas as pd

# import plikow wew
import main as m
import globals


def getAccelerations(ride, points):
    firstPoint = None
    firstSpeed = None
    secondSpeed = None
    firstTime = None
    secondTime = None

    i=1
    dictionaryAccelerations=dict()

    lastPoint = None
    lastSpeed = None
    lastTime = None

    for point in points:
        p = gpxpy.gpx.GPXTrackPoint(point[1], point[2])
        p.time = point[3]
        if lastPoint == None:
            lastPoint = p
            continue
        elif lastPoint.latitude == p.latitude and lastPoint.longitude == p.longitude:
            continue
        else:
            speed = p.speed_between(lastPoint)
            time = p.time_difference(lastPoint)
            if lastSpeed == None:
                lastPoint = p
                lastSpeed = speed
                lastTime = time
                continue
            else:
                try:
                    acceleration = (speed - lastSpeed) / (lastTime + time)
                    lastPoint = p
                    lastSpeed = speed
                    lastTime = time
                except:
                    continue
                try:
                    dictionaryAccelerations.update({i: [str(ride), str(point[0]), str(round(acceleration, 2))]})
                    i += 1
                except Exception as e:
                    m.addLog("Error in adding dictionary to dataframe, ride: " + str(ride) + ", exception: " + str(e))

    columnsAccelerations = ["ride", "endPoint", "accelerationValue"]
    try:
        dfAccelerations = pd.DataFrame.from_dict(dictionaryAccelerations, orient='index', columns=columnsAccelerations)
    except Exception as e:
        m.addLog("Error in adding dictonary to dataframe, ride: " + str(ride) + ", exception: " + str(e))
        return False
    return dfAccelerations



