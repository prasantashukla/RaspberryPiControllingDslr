import boto3
import sys
import time
import os
import json
import captureImage as c
from time import sleep
from datetime import datetime

from flask import Flask, request, render_template
from flask import jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


BUCKET_NAME = "aft-offsite-us-west-2" 
PHOTO_BOOTH_FOLDER="photobooth-pics/"
PARTICIPANTS_FOLDER="participants/"

PIC_ID = "PiShots"

s3 = boto3.client('s3')

@app.route('/takepicture', methods=['GET', 'POST'])
def takePicture():
    print("Taking picture")
    shot_date = datetime.now().strftime("%Y-%m-%d")
    shot_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    folderName1 = c.createSaveFolder(shot_date)
    folderName2 = c.captureImages(folderName1)
    fileName = c.renameFiles(folderName2, shot_time + PIC_ID)

    response = jsonify({"userId":"avidubey", "picName":fileName})
    response.headers.add('Access-Control-Allow-Origin', '*')

    print("returning response after successful photo capture")
    return response


    
def uploadGroupPicAndEmail():
    print("recovered")
    userId = request.form["userId"]
    print("req_data is ",userId)
    response = jsonify({"userId":"avidubey", "picName":"123.jpg"})
    response.headers.add('Access-Control-Allow-Origin', '*')

    #cars = request.form
    print("returning response")
    return response
    # on return, we can show local copy of picture on the screen
    #s3.upload_file(Key,bucketName,Key)
    print("Uploaded to s3 successfully")
    #s3.upload_file(Key,BUCKET_NAME,Key)
    print("Call a lambda function that detects the faces in picture and sends email to the users")
    print("Function returns the list of users the email was sent to")

def uploadIndividualPicAndUpdateDatabase(fileName, username):
    print("upload to S3 in participants folder and replace the existing username")
    uploadKeyName = PARTICIPANTS_FOLDER + username + ".jpg"
    s3.upload_file(fileName, BUCKET_NAME, uploadKeyName)

if __name__ == "__main__":
    app.run()