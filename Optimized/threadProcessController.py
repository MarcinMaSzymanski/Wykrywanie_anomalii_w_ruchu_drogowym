#biblioteki zew
from google.cloud import storage

#import plikow wew
import connections as c
import main as m
import processController as pc
import Queries.ridesQueries as rq


def checkFiles(blobs):
    for blob in blobs:
        if blob.name.startswith("files-to-processed") and blob.name.endswith(".gpx"):
            return True
    return False

def startThread(d):
    blobs = c.getBlobs()

    if blobs == None:
        d["Process"] = False
        return

    check=checkFiles(blobs)

    if not check:
        d["Process"] = True
        return

    m.addLog("ThreadProcess start")

    newBlobs=c.getBlobs()
    id = rq.getLastRideId() + 1
    for blob in newBlobs:
        if blob.name.startswith("files-to-processed") and blob.name.endswith(".gpx"):
            try:
                file = blob.download_as_string()
            except:
                try:
                    file = blob.download_as_string()
                except Exception as e:
                    m.addLog("Error in downloading file, filename: " + blob.name + ", exception: " + str(e))
                    d["Process"] = False
                    return
            result = pc.processFile(blob, file, id)
            if result:
                id += 1
                # result = c.setFileAsProcessed(blob)
            # else:
                # result = c.setFileAsIncorrect(blob)
            # if not result:
            #     d["Process"] = False
            #     return

    d["allFilesProcessedFlag"] = True
    d["Process"] = False