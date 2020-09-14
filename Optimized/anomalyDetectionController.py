#biblioteki zew
from sklearn.covariance import EllipticEnvelope
import pandas as pd

#pliki wew

def anomalyDetection(accelerations):
    contam=0.005
    elliptic = EllipticEnvelope(contamination=contam)
    try:
        elliptic.fit(accelerations.accelerationValue.values.reshape(-1, 1))
        ell = pd.DataFrame({'Acceleration': accelerations.accelerationValue.values,
                            'Outliers': elliptic.predict(accelerations.accelerationValue.values.reshape(-1, 1))})
    except:
        return pd.DataFrame()
    result = ell.loc[ell['Outliers'] == -1]
    local_min = result.loc[result['Acceleration'] < 0, 'Acceleration'].max()
    if local_min >= -0.2:
        result=pd.DataFrame()
        return result
    result = accelerations.loc[accelerations['accelerationValue'] <= local_min]

    rows_to_delete = []

    i = -1
    lastRide = None
    # 0 - ride, 1 - endpoint 2 - accelerationValue
    result = result.reset_index(drop=True)
    for row in result.values:
        i += 1
        if lastRide is None:
            lastRide = row[1]
            continue
        if (lastRide + 1) == row[1]:
            rows_to_delete.append(i - 1)
        lastRide = row[1]

    rows_to_delete = list(dict.fromkeys(rows_to_delete))
    result = result.drop(rows_to_delete)

    return result