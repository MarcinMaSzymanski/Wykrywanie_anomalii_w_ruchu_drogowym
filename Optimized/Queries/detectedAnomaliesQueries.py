#pliki wew
import connections as c

def addAnomalies(anomalies):
    result = c.executeQuery(anomalies, 'DetectedAnomalies')