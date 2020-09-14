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


bucketName = c.bucketName
blobs = getBlobs(bucketName)

for blob in blobs:
    client = storage.Client()
    bucket = client.get_bucket(bucketName)
    sourceBucket = client.bucket(bucketName)
    sourceBlob = sourceBucket.blob(blob.name)
    if blob.name.startswith("files-incorrect") and blob.name.endswith(".gpx"):
        destinationBlobName = blob.name.replace("files-incorrect", "files-to-processed")
        bucket.rename_blob(sourceBlob, destinationBlobName)
    if blob.name.startswith("files-processed") and blob.name.endswith(".gpx"):
        destinationBlobName = blob.name.replace("files-processed", "files-to-processed")
        bucket.rename_blob(sourceBlob, destinationBlobName)