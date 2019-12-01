import json
import os
import re
from urllib.parse import parse_qs
import boto3
from auth import is_verified_request
import handlers

HELP_REGEX = 'help'
FINE_REGEX = r'@.*\$.*for.*'

def handle(event, _):
    if not is_verified_request(event):
        return {'statusCode': 401}

    params = parse_qs(event['body'])
    text = params['text'][0].strip()

    if re.match(HELP_REGEX, text):
        response_body = handlers.handle_help_request()
    elif re.match(FINE_REGEX, text):
        response_body = handle_fine_request(params)
    else:
        response_body = handlers.handle_fallback()

    return {
        "statusCode": 200,
        "body": json.dumps(response_body),
        "headers": {
            "Content-Type": "application/json"
        }
    }

def handle_fine_request(params):
    text = params['text'][0].strip()
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

    return generate_response_body(user_name)

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
