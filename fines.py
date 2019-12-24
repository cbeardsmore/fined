import os
from urllib.parse import parse_qs
import boto3
from auth import is_verified_request
import response

def handle(event, _):
    if not is_verified_request(event):
        return {"statusCode": 401}

    params = parse_qs(event['body'])
    team_id = params['team_id'][0]

    dynamodb = boto3.client('dynamodb')
    table_name = os.environ['DYNAMODB_TABLE']
    dynamo_response = dynamodb.get_item(
        TableName=table_name,
        Key={'teamId': {'S': team_id}}
    )

    team_fines = dynamo_response['Item']['teamFines']
    body = response.create_fines_response(team_fines)
    return response.wrap_response_body(body)
