#biblioteki zew

#pliki wew
import connections as c


def addAccelerations(df):
    result = c.executeQuery(df, 'Accelerations')
    if result: return True
    else: return False

def findByRide(ride):
    query = "SELECT ride, endPoint, accelerationValue FROM Accelerations WHERE ride=" + str(ride)
    result = c.readQuery(query)
    return result