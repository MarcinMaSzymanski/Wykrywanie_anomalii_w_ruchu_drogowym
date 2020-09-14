#biblioteki zew

#import plikow wew
import main as m
import preProcessingController as ppc
import Queries.ridesQueries as rq
import Queries.accelerationsQueries as aq
import Queries.accelerationsPreProcessedQueries as appq


def startThread(d):
    result=rq.checkAccelerations()
    if not result:
        d["PreProcessing"] = False
        return

    m.addLog("PreProcessing start")

    accelerations= aq.findNegativeValues()
    min = ppc.findOutliers(accelerations)
    print(min)
    result = appq.addAccelerations(min)
    if result:
        rq.setPreProcessed()
    d["PreProcessing"] = False
