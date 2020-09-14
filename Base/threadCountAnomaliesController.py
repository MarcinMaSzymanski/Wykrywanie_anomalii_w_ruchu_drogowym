#biblioteki zew
import sys
#import plikow wew
import main as m
import countAnomaliesController as cac
import Queries.ridesQueries as rq
import Queries.pointsAnomaliesQueries as paq
import Queries.detectedAnomaliesQueries as daq

def startThread(d):
    result = rq.checkRoundAnomalies()
    if not result:
        d["CountAnomalies"] = False
        return

    m.addLog("ThreadCountAnomalies start")

    co_ordinates=paq.getCo_ordinates()
    result = cac.countAnomalies(co_ordinates)
    daq.addAnomalies(result)
    rq.setCountAnomalies()
    d["CountAnomalies"] = False
    m.addLog("This is end.")
    sys.exit()
