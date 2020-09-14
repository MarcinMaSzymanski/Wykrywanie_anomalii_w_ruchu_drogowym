#biblioteki zew
#import plikow wew
import main as m
import accelerationController as ac
import Queries.ridesQueries as rq
import Queries.pointsQueries as pq
import Queries.accelerationsQueries as aq
import Queries.accelerationsPreProcessedQueries as appq

def startThread(d):
    rides=rq.findUnprocessed()
    if len(rides.index) == 0:
        d["Acceleration"] = False
        return

    m.addLog("ThreadAcceleration start")

    for ride in rides.values:
        points=pq.findByRide(ride[0])
        if len(points.index)<3:
            rq.setIncorrect(ride[0])
            continue

        accelerations = ac.getAccelerations(ride[0], points.values)
        result = aq.addAccelerations(accelerations)
        if not result:
            rq.setIncorrect(ride[0])
            continue
        rq.setAccelerations(ride[0])

    d["Acceleration"] = False