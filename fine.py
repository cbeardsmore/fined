import os
import re
from urllib.parse import parse_qs
import boto3
from auth import is_verified_request
import response

HELP_REGEX = r'help'
FINE_REGEX = r'@.*\$.*for.*'

def handle(event, _):
    if not is_verified_request(event):
        return {'statusCode': 401}

    params = parse_qs(event['body'])
    text = params.get('text', 'help')[0].strip()

    if re.match(HELP_REGEX, text):
        response_body = response.create_help_response()
    elif re.match(FINE_REGEX, text):
        response_body = handle_fine_request(params)
    else:
        response_body = response.create_fallback_response()

    return response.wrap_response_body(response_body)


def handle_fine_request(params):
    text = params['text'][0].strip()
    user_name = params['user_name'][0]
    team_id = params['team_id'][0]

    dynamodb = boto3.client('dynamodb', region_name='us-east-1')
    table_name = os.environ['DYNAMODB_TABLE']
    dynamodb.update_item(
        TableName=table_name,
        Key={'teamId': {'S': team_id}},
        UpdateExpression='SET teamFines = list_append(if_not_exists(teamFines, :emptyList), :fine)',
        ExpressionAttributeValues={
            ':emptyList': {'L':[]},
            ':fine': {'L': [{'M': {'finedBy': {'S': user_name}, 'text': {'S': text}}}]}
        }
    )

    return response.create_fine_response(user_name)