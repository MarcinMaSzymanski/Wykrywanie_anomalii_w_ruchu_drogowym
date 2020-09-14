#biblioteki zew
from sklearn.covariance import EllipticEnvelope
import pandas as pd

#pliki wew
import globals

def preProcessing(dfAccelerations):
    rows_to_delete = []
    lastAcceleration = None
    i = -1
    for acceleration in dfAccelerations.values:
        i += 1
        if lastAcceleration == None:
            lastAcceleration = float(acceleration[2])
            if float(acceleration[2]) >= 0 or float(acceleration[2]) <= -6:
                rows_to_delete.append(i)
            continue
        # globals.errorValue = 2, globals.maximumBreakValue = -6
        if (float(acceleration[2]) > globals.errorValue and lastAcceleration < -globals.errorValue) or (
                float(acceleration[2]) < -globals.errorValue and lastAcceleration > globals.errorValue):
            rows_to_delete.append(i - 1)
            rows_to_delete.append(i)
            lastAcceleration = float(acceleration[2])
            continue
        if float(acceleration[2]) >= 0 or float(acceleration[2]) <= globals.maximumBreakValue:
            rows_to_delete.append(i)
        lastAcceleration = float(acceleration[2])

    rows_to_delete = list(dict.fromkeys(rows_to_delete))
    result = dfAccelerations.drop(rows_to_delete)

    return result

