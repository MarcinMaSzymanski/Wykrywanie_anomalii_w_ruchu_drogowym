#biblioteki zew
from sklearn.covariance import EllipticEnvelope
import pandas as pd

#pliki wew

def findOutliers(accelerations):
    elliptic = EllipticEnvelope(contamination=0.0005)
    elliptic.fit(accelerations.accelerationValue.values.reshape(-1, 1))
    ell = pd.DataFrame({'Acceleration': accelerations.accelerationValue.values,
                            'Outliers': elliptic.predict(accelerations.accelerationValue.values.reshape(-1, 1))})
    result = (ell.loc[ell['Outliers'] == -1])
    local_min = result.loc[result['Acceleration'] < 0, 'Acceleration'].max()
    return local_min
