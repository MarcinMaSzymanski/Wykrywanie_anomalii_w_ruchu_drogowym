#biblioteki zew

#pliki wew
import connections as c

def addAnomalies(anomalies):
    result = c.executeQuery(anomalies, 'Anomalies')

def findPointsByRide(ride):
    query = "SELECT point FROM Anomalies WHERE ride=" + str(ride)
    result = c.readQuery(query)
    return result