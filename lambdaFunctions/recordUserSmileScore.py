import boto3
import json
import decimal

s3 = boto3.client('dynamodb', region_name='us-west-2')
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

table = dynamodb.Table('UserSmileScore')

def lambda_handler(event, context):
    userId = event["userId"]
    smileConfidencePercentage = event["smileConfidence"]
    noOfPeopleInPhoto = event["noOfPeopleInPhoto"]
    
    response = table.update_item(
    Key={
        'UserId': userId
    },
    UpdateExpression="add score :s, numberOfTimeSeen :c, seenWithPeople :p",
    ExpressionAttributeValues={
        ':s': decimal.Decimal(noOfPeopleInPhoto * decimal.Decimal(smileConfidencePercentage/100)).quantize(decimal.Decimal('1.00')),
        ':c': decimal.Decimal(1),
        ':p': decimal.Decimal(noOfPeopleInPhoto),
    })
    

    
    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }
