#biblioteki zew
from google.cloud import storage

#import plikow wew
import connections as c
import main as m
import processController as pc
import Queries.ridesQueries as rq

def getBlobs(bucketName):
    client = storage.Client()
    blobs = client.list_blobs(bucketName)
    return blobs


def checkFiles(blobs):
    for blob in blobs:
        if blob.name.startswith("files-processed") and blob.name.endswith(".gpx"):
            return True
    return False

def startThread(d):
    bucketName = c.bucketName
    blobs = getBlobs(bucketName)

    if blobs == None:
        d["Process"] = False
        return

    check=checkFiles(blobs)

    if not check:
        m.addLog("No files to process in storage. End of thread.")
        d["Process"] = False
        return

    m.addLog("ThreadProcess start")

    newBlobs=getBlobs(bucketName)
    id = rq.getLastRideId() + 1
    for blob in newBlobs:
        if blob.name.startswith("files-processed") and blob.name.endswith(".gpx"):
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
            try:
                if result:
                    id += 1
                    c.setFileAsProcessed(bucketName, blob)
                else:
                    c.setFileAsIncorrect(bucketName, blob)
            except Exception as e:
                m.addLog("Error in moving file, error: " + str(e))
                d["Process"] = False
                return


    d["allFilesProcessedFlag"] = True
    d["Process"] = False