import re
from urllib.parse import parse_qs
from auth import is_verified_request
from dynamo import update_item
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

    update_item(team_id, user_name, text)
    return response.create_fine_response(user_name)