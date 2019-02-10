import boto3
import sys
import time
import os

BUCKET_NAME = "aft-offsite-us-west-2" 
FOLDER="photobooth-pics/"

s3 = boto3.client('s3')

def takePicture():
    # Logic to take picture using gphoto2
    print()

def uploadToS3():
    #s3.upload_file(Key,bucketName,Key)