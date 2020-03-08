import os
from urllib.parse import parse_qs
import boto3
from boto3.dynamodb.types import TypeDeserializer
from auth import is_verified_request
import response

def handle(event, _):
    if not is_verified_request(event):
        return {"statusCode": 401}

    params = parse_qs(event['body'])
    team_id = params['team_id'][0]

    dynamodb = boto3.client('dynamodb', region_name='us-east-1')
    table_name = os.environ['DYNAMODB_TABLE']
    dynamo_response = dynamodb.get_item(
        TableName=table_name,
        Key={'teamId': {'S': team_id}}
    )

    if (dynamo_response.get('Item') is None or dynamo_response['Item']['teamFines'] is None):
        return response.create_no_fines_response()

    team_fines = dynamo_response['Item']['teamFines']
    team_fines_deserialized = from_dynamodb_to_json(team_fines)
    body = response.create_fines_response(team_fines_deserialized)
    return response.wrap_response_body(body)

def from_dynamodb_to_json(item):
    d = TypeDeserializer()
    items = d.deserialize(item)
    items = [x['text'] for x in items]
    items = "\n \u2022 ".join(items)
    return items
