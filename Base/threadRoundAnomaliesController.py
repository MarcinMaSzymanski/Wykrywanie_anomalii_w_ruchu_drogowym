#biblioteki zew

#import plikow wew
import main as m
import roundAnomaliesController as rac
import Queries.ridesQueries as rq
import Queries.anomaliesQueries as aq
import Queries.pointsQueries as pq
import Queries.pointsAnomaliesQueries as paq

def startThread(d):
    rides = rq.findAnomalies()
    if len(rides.index) == 0:
        d["RoundAnomalies"] = False
        return
    m.addLog("ThreadRoundAnomalies start")
    for ride in rides.values:
        points = aq.findPointsByRide(ride[0])
        co_ordinates = pq.getCo_ordinates(points)
        result = rac.roundCo_ordinates(co_ordinates)
        paq.addAnomalies(result)
        rq.setRoundAnomalies(ride[0])
    d["RoundAnomalies"] = False