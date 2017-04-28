#!/usr/bin/env python

import boto3
import os
import time

def get_new_uploads(bucketname):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucketname)
    files = [o.key for o in bucket.objects.all()]
    return files

if __name__ == "__main__":
    client = boto3.client('s3')
    paths = ["results","simple"]
    bucketnames = ["ryankelly-superurop-coreset","ryankelly-superurop-simplecoreset"]
    files = [os.listdir(path) for path in paths]
    while True:
        for i in range(len(bucketnames)):
            bucketname = bucketnames[i]
            file_set = get_uploads(bucketname)
            for f in files:
                if f not in fileset:
                    client.upload_file(paths[i]+f,bucketname,f)
        time.sleep(5)
