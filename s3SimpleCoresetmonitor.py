#!/usr/bin/env python

import boto3
import os

def get_new_uploads(bucketname, file_set):
	s3 = boto3.resource('s3')
	bucket = s3.Bucket(bucketname)
	files = [o.key for o in bucket.objects.all()]
	new_uploads = [f for f in files if f not in file_set]
	return new_uploads

if __name__ == "__main__":
	client = boto3.client('s3')
	path = "/home/ubuntu/data/simple_coresets/"
	bucketname = "ryankelly-superurop-simplecoreset"
	file_set = set(os.listdir(path))
	while True:
		file_names = get_new_uploads(bucketname, file_set)
		for f in file_names:
			client.download_file(bucketname,f,path+f)



