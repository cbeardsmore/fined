import json
import os
from urllib.parse import parse_qs
import boto3
from auth import is_verified_request

def handle(event, _):
    if not is_verified_request(event):
        return {'statusCode': 401}

    params = parse_qs(event['body'])
    text = params['text'][0]
    user_name = params['user_name'][0]
    team_id = params['team_id'][0]

    print('Text -> ', text)
    print('User Name -> ', user_name)
    print('Team ID -> ', team_id)

    dynamodb = boto3.client('dynamodb')
    table_name = os.environ['DYNAMODB_TABLE']
    dynamodb.put_item(
        TableName=table_name,
        Item={
            'teamId': {'S': team_id},
            'teamFines': {'M':
                {'username': {'S': user_name,}, 'text': {'S': text}}
            }
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps(generate_response_body(user_name)),
        "headers": {
            "Content-Type": "application/json"
        }
    }


def generate_response_body(user_name):
    return  {
        "response_type": "in_channel",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "@{} has been fined. Shame on them!".format(user_name)
                }
            }
        ]
    }
