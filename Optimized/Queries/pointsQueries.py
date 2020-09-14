#biblioteki zew
import pandas as pd
#pliki wew
import connections as c

def addPoints(points):
    result = c.executeQuery(points, 'Points')
    if result==False: return False
    else: return True

def findByRide(ride):
    query = "SELECT iPoint, latitude, longitude, date FROM Points WHERE ride=" + str(ride)
    result = c.readQuery(query)
    return result

def getCo_ordinates(points):
    columnsCo_ordinates = ["latitude", "longitude"]
    dfCo_ordinates = pd.DataFrame(columns=columnsCo_ordinates)
    for point in points.values:
        query = "SELECT latitude, longitude FROM Points WHERE iPoint=" + str(point[1])
        result = c.readQuery(query)
        dfCo_ordinates = dfCo_ordinates.append(result)
    return dfCo_ordinates