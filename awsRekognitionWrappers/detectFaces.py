# Detects all the faces in a target image
# Look for response.FaceDetails array
# FaceDetail.BoundingBox
# FaceDetail.Confidence >=95
# FaceDetail.Smile.(Value as true/false and Confidence)
import boto3
client=boto3.client('rekognition', region_name='us-east-1')

targetBucket = "aft-offsite"

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

'''
print("Detecting all the faces")

response = detectfaces(targetBucket, "1549588233.jpg")
print(response)
'''