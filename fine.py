import boto3

from urllib.parse import parse_qs
from auth import isVerifiedRequest

STATUS_CODE_KEY = "statusCode"
DYNAMO_TABLE_NAME = "fines"

def handle(event, context):
    if not isVerifiedRequest(event):
        return { STATUS_CODE_KEY: 401 }

    params = parse_qs(event['body'])
    text = params['text'][0]
    user_name = params['user_name'][0]
    team_id = params['team_id'][0]

    print('Text -> ', text)
    print('User Name -> ', user_name)
    print('Team ID -> ', team_id)

    dynamodb = boto3.client('dynamodb')
    response = dynamodb.put_item(
        TableName=DYNAMO_TABLE_NAME,
        Item={ 
            'teamId': { 'S': team_id }, 
            'teamFines': { 'M': 
                { 'username': { 'S': user_name,}, 'text': {'S': text} }
            }
        }
    )
        
    print(response)
    return { STATUS_CODE_KEY: 200 }
