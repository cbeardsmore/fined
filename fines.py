import boto3
import json
import os

from urllib.parse import parse_qs
from auth import isVerifiedRequest

def handle(event, context):
    if not isVerifiedRequest(event):
        return { "statusCode": 401 }

    params = parse_qs(event['body'])
    team_id = params['team_id'][0]

    print('Team ID -> ', team_id)

    dynamodb = boto3.client('dynamodb')
    tableName = os.environ['DYNAMODB_TABLE']
    dynamo_response = dynamodb.get_item(
        TableName=tableName,
        Key={ 'teamId': { 'S': team_id } }
    )

    team_fines = dynamo_response['Item']['teamFines']
    
    return {
        "statusCode": 200,
        "body": json.dumps(generateResponseBody(team_fines)),
        "headers": {
            "Content-Type": "application/json"
        }
    }

def generateResponseBody(team_fines):
    return  {
        "response_type": "in_channel",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Current Team Fines: {}".format(team_fines)
                }
            }
        ]
    }