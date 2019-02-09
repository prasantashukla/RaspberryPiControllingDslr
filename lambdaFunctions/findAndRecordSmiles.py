import boto3
rekognition_client=boto3.client('rekognition', region_name='us-east-1')


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