import boto3
import json
import sys
from UserBoundingBox import UserBoundingBox

client=boto3.client('rekognition', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')

TARGET_BUCKET = "aft-offsite"
PARTIPANTS_FOLDER = "participants"
SMILE_CONFIDENCE_THRESHOLD = 90
FACE_CONFIDENCE_THRESHOLD = 95

def lambda_handler(event, context):
    detectFacesResponse = detectfaces(TARGET_BUCKET, event["imageFileName"])
    # Get Bounding Box list having smiles
    userBoundingBoxes = getSmilingUserBoundingBoxes(detectFacesResponse)
    print("Total ", len(userBoundingBoxes), " smiles detected")
        
    # For all the files in participants folder call another separate lambda to recordSmileScore
    # pass above list and participant bucket and fileName

    participants = getListOfParticipants()
    for participant in participants:
        recordSmileScore(participant, userBoundingBoxes)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def recordSmileScore(participant, UserBoundingBox):
    print(participant)

def isSmileOnFace(faceDetail):
    smile = faceDetail["Smile"]
    if (smile["Value"] == True):
        return True
    else:
        return False

def getSmilingUserBoundingBoxes(detectFacesResponse):
    faceDetails = detectFacesResponse["FaceDetails"]
    smilingUserBoundingBoxes = []
    for faceDetail in faceDetails:
        if (faceDetail["Confidence"] > FACE_CONFIDENCE_THRESHOLD and isSmileOnFace(faceDetail)): #Face Confidence check
            print("Smile detected")
            boundingBox = faceDetail["BoundingBox"]
            smileConfidence = faceDetail["Smile"]["Confidence"]
            userBoundingBox = UserBoundingBox(boundingBox, None, smileConfidence)
            smilingUserBoundingBoxes.append(userBoundingBox)
    return smilingUserBoundingBoxes


def getListOfParticipants():
    startAfter = PARTIPANTS_FOLDER+"/"
    """Get a list of all keys in an S3 bucket."""
    keys = []

    theobjects = s3.list_objects_v2(Bucket=TARGET_BUCKET, StartAfter=startAfter )
    for object in theobjects['Contents']:
        keys.append(object['Key'])

    return keys

def detectfaces(targetBucket, imageName):
    response = client.detect_faces(
        Image={
            'S3Object': {
                'Bucket': targetBucket,
                'Name': imageName
            }
        },
        Attributes=[
            'ALL'
        ]
    )
    return response
    

#u = UserBoundingBox("sdfdf", None, 99)
#print(u.BoundingBox)
event = {"imageFileName":"1549588233.jpg"}
response = lambda_handler(event, None)