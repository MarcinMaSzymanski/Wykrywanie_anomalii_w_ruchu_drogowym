#biblioteki zew

#pliki wew
import connections as c


def addAccelerations(df):
    result = c.executeQuery(df, 'Accelerations')
    if result: return True
    else: return False

def findNegativeValues():
    query = "select accelerationValue FROM Accelerations WHERE accelerationValue<0"
    result = c.readQuery(query)
    return result