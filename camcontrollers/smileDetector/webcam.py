import boto3
import sys
import time
import os
 
BUCKET_NAME = "aft-offsite-us-west-2"
FOLDER="smileCandidates/"
s3 = boto3.client('s3')

epoch=int(time.time())
Key=FOLDER + str(epoch)+".jpg"
cmd='fswebcam -r 1920x1080 --no-banner  ' + Key
 
os.system(cmd)

s3.upload_file(Key,BUCKET_NAME,Key)
print("file uploaded to s3 successfully with key " + Key)
cmd='rm ' + Key
os.system(cmd)