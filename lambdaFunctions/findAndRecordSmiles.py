import boto3
import json
rekognition_client=boto3.client('rekognition', region_name='us-east-1')

def lambda_handler(event, context):
    # Inputs are participant and UserBoundingBoxes with Confirmed Smiles
    compareFacesResponse = compare_faces(event["participant"], event["target_bucket"], event["smilingUserBoundingBoxes"])
    


    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


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