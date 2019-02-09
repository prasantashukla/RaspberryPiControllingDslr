import boto3
import json

s3 = boto3.client('s3', region_name='us-west-2')

def lambda_handler(event, context):
    # userId = event["userId"]
    # smileConfidencePercentage = event["smileConfidence"]
    # noOfPeopleInPhoto = event["noOfPeopleInPhoto"]
    
    # Shuklaji : algo for scoring, storing in ddb, api for retrieving
    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }
