#biblioteki zew

#pliki wew
import connections as c

def getLastRideId():
    query = "SELECT MAX(iRide) as ID_MAX FROM Rides"
    result = c.readQuery(query)
    id = result['ID_MAX'].iloc[0]
    if id is None: id=0
    return id

def addRide(ride):
    result = c.executeQuery(ride, 'Rides')
    if result==False: return False
    else: return True

def findUnprocessed():
    query = "SELECT iRide FROM Rides WHERE processedState=\"Unprocessed\""
    result = c.readQuery(query)
    return result

def setIncorrect(ride):
    query = "UPDATE Rides Set processedState=\"Incorrect\" Where iRide=" + str(ride)
    result = c.updateQuery(query)

def setAccelerations(ride):
    query = "UPDATE Rides Set processedState=\"Accelerations\" Where iRide=" + str(ride)
    result = c.updateQuery(query)

def checkAccelerations():
    query = "SELECT COUNT(*) as unprocessed FROM Rides WHERE processedState=\"Unprocessed\""
    result = c.readQuery(query)
    unprocessed = result['unprocessed'].iloc[0]
    query = "SELECT COUNT(*) as accelerations FROM Rides WHERE processedState=\"Accelerations\""
    result = c.readQuery(query)
    accelerations = result['accelerations'].iloc[0]
    if unprocessed == 0 and accelerations>0: return True
    else: return False

def setPreProcessed():
    query = "UPDATE Rides Set processedState=\"PreProcessed\" WHERE processedState=\"Accelerations\""
    result = c.updateQuery(query)

def findPreProcessed():
    query = "SELECT iRide FROM Rides WHERE processedState=\"PreProcessed\""
    result = c.readQuery(query)
    return result

def setNoAnomalies(ride):
    query = "UPDATE Rides Set processedState=\"NoAnomalies\" Where iRide=" + str(ride)
    result = c.updateQuery(query)

def setAnomalies(ride):
    query = "UPDATE Rides Set processedState=\"Anomalies\" Where iRide=" + str(ride)
    result = c.updateQuery(query)

def findAnomalies():
    query = "SELECT iRide FROM Rides WHERE processedState=\"Anomalies\""
    result = c.readQuery(query)
    return result

def setRoundAnomalies(ride):
    query = "UPDATE Rides Set processedState=\"RoundAnomalies\" Where iRide=" + str(ride)
    result = c.updateQuery(query)

def checkRoundAnomalies():
    query = "SELECT COUNT(*) as anomalies FROM Rides WHERE processedState=\"Anomalies\""
    result = c.readQuery(query)
    anomalies = result['anomalies'].iloc[0]
    query = "SELECT COUNT(*) as roundAnomalies FROM Rides WHERE processedState=\"RoundAnomalies\""
    result = c.readQuery(query)
    roundAnomalies = result['roundAnomalies'].iloc[0]
    if anomalies == 0 and roundAnomalies>0: return True
    else: return False

def setCountAnomalies():
    query = "UPDATE Rides Set processedState=\"CountAnomalies\" WHERE processedState=\"RoundAnomalies\""
    result = c.updateQuery(query)
