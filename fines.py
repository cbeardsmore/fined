import re
from urllib.parse import parse_qs
import auth
import dynamo
import response

HELP_REGEX = r'help'

def handle(event, _):
    if not auth.is_verified_request(event):
        return {"statusCode": 401}

    params = parse_qs(event['body'])
    text = params.get('text', 'help')[0].strip()

    if re.match(HELP_REGEX, text):
        response_body = response.create_help_response()
    else:
        response_body = handle_fines_request(params)

    return response.wrap_response_body(response_body)


def handle_fines_request(params):
    team_id = params['team_id'][0]
    channel_id = None
    team_fines = dynamo.get_fines(team_id, channel_id)

    if team_fines is None:
        return response.create_no_fines_response()

    return response.create_fines_response(team_fines)
