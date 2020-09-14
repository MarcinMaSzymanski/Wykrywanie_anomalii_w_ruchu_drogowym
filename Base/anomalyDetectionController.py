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
    result = accelerations.loc[accelerations['accelerationValue'] <= local_min]
    return result