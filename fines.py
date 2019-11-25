import json
import os
from urllib.parse import parse_qs
import boto3
from auth import is_verified_request

def handle(event, _):
    if not is_verified_request(event):
        return {"statusCode": 401}

    params = parse_qs(event['body'])
    team_id = params['team_id'][0]

    print('Team ID -> ', team_id)

    dynamodb = boto3.client('dynamodb')
    table_name = os.environ['DYNAMODB_TABLE']
    dynamo_response = dynamodb.get_item(
        TableName=table_name,
        Key={'teamId': {'S': team_id}}
    )

    team_fines = dynamo_response['Item']['teamFines']

    return {
        "statusCode": 200,
        "body": json.dumps(generate_response_body(team_fines)),
        "headers": {
            "Content-Type": "application/json"
        }
    }

def generate_response_body(team_fines):
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
