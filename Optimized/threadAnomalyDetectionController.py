#biblioteki zew

#import plikow wew
import main as m
import anomalyDetectionController as adc
import roundAnomaliesController as rac
import Queries.ridesQueries as rq
import Queries.accelerationsPreProcessedQueries as appq
import Queries.anomaliesQueries as aq
import Queries.pointsQueries as pq
import Queries.pointsAnomaliesQueries as paq

def startThread(d):
    rides = rq.findPreProcessed()
    if len(rides.index) == 0:
        d["AnomalyDetection"] = False
        return

    m.addLog("ThreadAnomalyDetection start")

    for ride in rides.values:
        accelerations=appq.findByRide(ride[0])
        if len(accelerations.index) == 0:
            rq.setNoAnomalies(ride[0])
            continue
        result = adc.anomalyDetection(accelerations)
        if result.empty:
            rq.setNoAnomalies(ride[0])
            continue
        if len(result.index) == 0:
            rq.setNoAnomalies(ride[0])
            continue
        aq.addAnomalies(result)
        rq.setAnomalies(ride[0])
        co_ordinates = pq.getCo_ordinates(result)
        result = rac.roundCo_ordinates(co_ordinates)
        paq.addAnomalies(result)
        rq.setRoundAnomalies(ride[0])
    d["AnomalyDetection"] = False
