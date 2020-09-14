#biblioteki zew

#pliki wew
import connections as c

def addAccelerations(min):
    query = (
            "INSERT INTO AccelerationsPreProcessed (ride, endPoint, accelerationValue) select ride, endPoint, accelerationValue FROM Accelerations WHERE accelerationValue>" + str(min) + " and accelerationValue<0")
    result = c.updateQuery(query)
    return result

def findByRide(ride):
    query = "SELECT ride, endPoint as point, accelerationValue FROM AccelerationsPreProcessed WHERE ride=" + str(ride)
    result = c.readQuery(query)
    return result
