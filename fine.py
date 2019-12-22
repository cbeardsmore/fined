import os
import re
from urllib.parse import parse_qs
import boto3
from auth import is_verified_request
import handlers

HELP_REGEX = r'help'
FINE_REGEX = r'@.*\$.*for.*'

def handle(event, _):
    if not is_verified_request(event):
        return {'statusCode': 401}

    params = parse_qs(event['body'])
    text = params.get('text', 'help')[0].strip()

    if re.match(HELP_REGEX, text):
        response_body = handlers.handle_help_request()
    elif re.match(FINE_REGEX, text):
        response_body = handle_fine_request(params)
    else:
        response_body = handlers.handle_fallback()

    return handlers.wrap_response_body(response_body)


def handle_fine_request(params):
    text = params['text'][0].strip()
    user_name = params['user_name'][0]
    team_id = params['team_id'][0]

    dynamodb = boto3.client('dynamodb')
    table_name = os.environ['DYNAMODB_TABLE']
    dynamodb.update_item(
        TableName=table_name,
        Key={'teamId': {'S': team_id}},
        UpdateExpression='SET teamFines = list_append(if_not_exists(teamFines, :emptyList), :fine)',
        ExpressionAttributeValues={
            ':fine': {'L': [{'M': {'finedBy': {'S': user_name}, 'text': {'S': text}}}]},
            ':emptyList': {'L':[]}
        }
    )

    return handlers.handle_fine_response(user_name)