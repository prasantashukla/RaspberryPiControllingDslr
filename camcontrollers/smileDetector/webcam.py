import boto3
import sys
import time
import os
 
FOLDER="smileCandidates/"
epoch=int(time.time())
Key=FOLDER + str(epoch)+".jpg"
cmd='fswebcam -r 1920x1080 --no-banner  ' + Key
 
os.system(cmd)
 
bucketName = "aft-offsite-us-west-2"
 
s3 = boto3.client('s3')
s3.upload_file(Key,bucketName,Key)
print("file uploaded to s3 successfully with key " + Key)
cmd='rm ' + Key
os.system(cmd)