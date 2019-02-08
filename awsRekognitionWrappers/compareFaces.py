# Compare a source image face with top 100 largest faces in the target image
# Gives FaceMatches and UnmatchedFaces with scores
# Look at FaceMatches and anythign above 80% can be termed as a match
# Look for FaceMatch.Similarity Object
# Look for FaceMatch.Face.BoudingBox.(Width, Height, Left, Top)
# In order to match face, bounding box has to overlap so we need some function called 
# areaOfOverlap(BoundingBox1, BoundingBox2)

import boto3
client=boto3.client('rekognition', region_name='us-east-1')

targetBucket = "aft-offsite"

def compare_faces(login, targetImageName):
    response = client.compare_faces(
        SourceImage={
            'S3Object': {
                'Bucket': targetBucket,
                'Name': 'participants/'+login+'.jpeg'
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

# Testing the function
print("Comparing faces")
login = "shravana"
targetImageName = "1549588233.jpg"
response = compare_faces(login, targetImageName)
print(response)