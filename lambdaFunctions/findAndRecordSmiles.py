import boto3
import json
rekognition_client=boto3.client('rekognition', region_name='us-west-2')

FACE_DETECTION_CONFIDENCE_THRESHOLD = 95
FACE_SIMILARITY_THRESHOLD = 90
BOUNDING_BOX_OVERLAP_AREA_THRESHOLD = 90

def lambda_handler(event, context):
    print(json.dumps(event))
    # Inputs are participant and UserBoundingBoxes with Confirmed Smiles
    smilingUserBoundingBoxes = event["smilingUserBoundingBoxes"]
    participant = event["participant"]
    targetImageFileName = event["targetImageFileName"]

    compareFacesResponse = compare_faces(participant, event["target_bucket"], targetImageFileName)
    faceMatchMaxSimilarity, boundingBox = getFaceMatchBoundingBox(compareFacesResponse)

    if faceMatchMaxSimilarity > FACE_SIMILARITY_THRESHOLD:
        print("Found a match for participant ", participant)
    
    matchingBoundingBoxOverlapPercentage, smilingUserBoundingBox = getMatchingUserBoundingBox(boundingBox, smilingUserBoundingBoxes)
    
    if(matchingBoundingBoxOverlapPercentage > BOUNDING_BOX_OVERLAP_AREA_THRESHOLD):
        recordUserSmileConfidence(participant, smilingUserBoundingBox["smileConfidence"])

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def recordUserSmileConfidence(participant, smileConfidence):
    print("participant ",participant," is smiling with smile Confidence score of ", smileConfidence)

def getMatchingUserBoundingBox(boundingBox, smilingUserBoundingBoxes):
    overlapPercentage = 0
    returnSmilingUserBoundingBox = None
    for smilingUserBoundingBox in smilingUserBoundingBoxes:
            smilingBoundingBoxOverlapPercentage = getOverlapAreaPercentage(boundingBox, smilingUserBoundingBox["boundingBox"])
            if(smilingBoundingBoxOverlapPercentage > overlapPercentage):
                overlapPercentage = smilingBoundingBoxOverlapPercentage
                returnSmilingUserBoundingBox = smilingUserBoundingBox
    
    return overlapPercentage, returnSmilingUserBoundingBox
        

def getFaceMatchBoundingBox(compareFacesResponse):
    faceMatches = compareFacesResponse["FaceMatches"]
    faceMatchMaxSimilarity = 0
    boundingBox = None
    for faceMatch in faceMatches:
        if faceMatch["Similarity"] > faceMatchMaxSimilarity and faceMatch["Face"]["Confidence"] > FACE_DETECTION_CONFIDENCE_THRESHOLD:
            faceMatchMaxSimilarity = faceMatch["Similarity"]
            boundingBox = faceMatch["Face"]["BoundingBox"]

    return faceMatchMaxSimilarity, boundingBox

def compare_faces(participant, targetBucket, targetImageName):
    response = rekognition_client.compare_faces(
        SourceImage={
            'S3Object': {
                'Bucket': targetBucket,
                'Name': participant
            }
        },
        TargetImage={
            'S3Object': {
                'Bucket': targetBucket,
                'Name': targetImageName
            }
        }
    )

    return response   


def getArea(boundingBox):
    return boundingBox["Height"] * boundingBox["Width"]

def getOverlapAreaPercentage(boundingBox1, boundingBox2):
    # boundingBox1 Variables
    l1 = boundingBox1["Left"]
    t1 = boundingBox1["Top"]
    w1 = boundingBox1["Width"]
    h1 = boundingBox1["Height"]

    # boundingBox2 Variables
    l2 = boundingBox2["Left"]
    t2 = boundingBox2["Top"]
    w2 = boundingBox2["Width"]
    h2 = boundingBox2["Height"]

    # Check if the boxes are overlapping or not
    # Horizontal Overlapping Check
    horizontal_overlapping = False
    vertical_overlapping = False

    if( ( (l1 <= l2) and ((l1 + w1) >= l2) )  or ( (l2 <= l1) and ((l2 + w2) >= l1) ) ):
        horizontal_overlapping = True

    # Vertical Overlapping Check
    if( (t1 <= t2 and t1 + h1 >= t2) or (t2 <= t1 and t2 + h2 >= t1) ):
        vertical_overlapping = True

    area_of_intersection = 0
    if (horizontal_overlapping and vertical_overlapping):     
        length = abs ((l1 + w1) - (l2))
        
        width = abs((t1 + h1) - (t2))
        
        area_of_intersection = length * width

    area_of_union = getArea(boundingBox1) + getArea(boundingBox2) - area_of_intersection

    overlapAreaPercentage = 100 * area_of_intersection / area_of_union
    print ("overlapArea% = ", overlapAreaPercentage)
    return overlapAreaPercentage