from urllib.parse import parse_qs
from boto3.dynamodb.types import TypeDeserializer
from auth import is_verified_request
from dynamo import get_item
import response

def handle(event, _):
    if not is_verified_request(event):
        return {"statusCode": 401}

    params = parse_qs(event['body'])
    team_id = params['team_id'][0]
    dynamo_response = get_item(team_id)

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
