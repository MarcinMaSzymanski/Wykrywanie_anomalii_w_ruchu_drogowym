#biblioteki zew

#import plikow wew
import main as m
import preProcessingController as ppc
import Queries.ridesQueries as rq
import Queries.accelerationsQueries as aq
import Queries.accelerationsPreProcessedQueries as appq


def startThread(d):
    rides = rq.findAccelerations()
    if len(rides.index) == 0:
        d["PreProcessing"] = False
        return

    m.addLog("ThreadPreProcessing start")

    for ride in rides.values:
        accelerations = aq.findByRide(ride[0])
        if len(accelerations.index) < 1:
            rq.setIncorrect(ride[0])
            continue

        preProcessed = ppc.preProcessing(accelerations)
        result = appq.addAccelerations(preProcessed)
        if not result:
            rq.setIncorrect(ride[0])
            continue
        rq.setPreProcessed(ride[0])

    d["PreProcessing"] = False