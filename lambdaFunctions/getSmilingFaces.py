import boto3
import json

rekognition_client=boto3.client('rekognition', region_name='us-west-2')
lambda_client=boto3.client('lambda', region_name='us-west-2')
s3 = boto3.client('s3', region_name='us-west-2')

TARGET_BUCKET = "aft-offsite-us-west-2"
PARTIPANTS_FOLDER = "participants/"
FACE_CONFIDENCE_THRESHOLD = 95

def lambda_handler(event, context):
    targetImageFileName = event["Records"][0]["s3"]["object"]["key"]
    detectFacesResponse = detectfaces(TARGET_BUCKET, targetImageFileName)
    # Get Bounding Box list having smiles
    noOfPeopleInPhoto, smilingUserBoundingBoxes = getSmilingUserBoundingBoxes(detectFacesResponse)
    print("Total ", len(smilingUserBoundingBoxes), " smiles detected among total ", noOfPeopleInPhoto, "people detected")
        
    # For all the files in participants folder call another separate lambda to recordSmileScore
    # pass above list and participant bucket and fileName

    participants = getListOfParticipants()
    for participant in participants:
        recordSmileScore(participant, targetImageFileName, smilingUserBoundingBoxes, noOfPeopleInPhoto)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def recordSmileScore(participant, targetImageFileName, smilingUserBoundingBoxes, noOfPeopleInPhoto):
    
    event = {"target_bucket" : TARGET_BUCKET ,
                "participant" : participant, 
                "noOfPeopleInPhoto" : noOfPeopleInPhoto,
                "targetImageFileName" : targetImageFileName,
                "smilingUserBoundingBoxes" : smilingUserBoundingBoxes}
    lambda_client.invoke(FunctionName="recordParticipantSmile", 
                            InvocationType='Event', 
                            Payload=json.dumps(event, default=lambda o: o.__dict__))
                        
def isSmileOnFace(faceDetail):
    smile = faceDetail["Smile"]
    if (smile["Value"] == True):
        return True
    else:
        return False

def getSmilingUserBoundingBoxes(detectFacesResponse):
    faceDetails = detectFacesResponse["FaceDetails"]
    totalFaceCount = 0
    smilingUserBoundingBoxes = []
    for faceDetail in faceDetails:
        if (faceDetail["Confidence"] > FACE_CONFIDENCE_THRESHOLD):
            totalFaceCount+=1
            if isSmileOnFace(faceDetail): #Face Confidence check
                boundingBox = faceDetail["BoundingBox"]
                #boundingBox = BoundingBox(bb["Left"], bb["Top"], bb["Height"], bb["Width"])
                smileConfidence = faceDetail["Smile"]["Confidence"]
                userBoundingBox = UserBoundingBox(boundingBox, None, smileConfidence)
                smilingUserBoundingBoxes.append(userBoundingBox)
    return totalFaceCount, smilingUserBoundingBoxes


def getListOfParticipants():
    startAfter = PARTIPANTS_FOLDER
    """Get a list of all keys in an S3 bucket."""
    keys = []

    theobjects = s3.list_objects_v2(Bucket=TARGET_BUCKET, Prefix=startAfter, Delimiter='/' )
    for object in theobjects['Contents']:
        key = object['Key']
        if(key.endswith(".jpeg")):
            keys.append(key)

    return keys

def detectfaces(targetBucket, imageName):
    response = rekognition_client.detect_faces(
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


class BoundingBox(object):
    def __init__(self, Left, Top, Height, Weight):
        self.Left = Left
        self.Top = Top
        self.Height = Height
        self.Weight = Weight

class UserBoundingBox(object):
    def __init__(self, boundingBox, username, smileConfidence):
        self.boundingBox = boundingBox
        self.username = username
        self.smileConfidence = smileConfidence
