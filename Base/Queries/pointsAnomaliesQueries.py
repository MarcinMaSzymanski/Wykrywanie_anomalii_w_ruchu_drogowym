#pliki wew
import connections as c

def addAnomalies(anomalies):
    result = c.executeQuery(anomalies, 'PointsAnomalies')
    return result

def getCo_ordinates():
    query = "select latitude, longitude FROM PointsAnomalies"
    result = c.readQuery(query)
    return result