#biblioteki zew
from google.cloud import storage

#import plikow wew
import connections as c
import main as m
import processControler as pc
import Queries.ridesQueries as rq

def getBlobs(bucketName):
    client = storage.Client()
    blobs = client.list_blobs(bucketName)
    return blobs


bucketName = c.bucketName
blobs = getBlobs(bucketName)

i=0
j=0
k=0
for blob in blobs:
    if blob.name.startswith("files-to-processed/FEMALE") and blob.name.endswith(".gpx"):
        i += 1
    if blob.name.startswith("files-to-processed/MALE") and blob.name.endswith(".gpx"):
        j += 1
    if blob.name.startswith("files-to-processed/UNDEFINED") and blob.name.endswith(".gpx"):
        k += 1
    print("i = " + str(i))
    print("j = " + str(j))
    print("k = " + str(k))