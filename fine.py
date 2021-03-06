import re
from urllib.parse import parse_qs
import uuid
import auth
import response
import dynamo

HELP_REGEX = r'help'
FINE_REGEX = r'@(.+) \$?[0-9]+ for .+'

def handle(event, _):
    if not auth.is_verified_request(event):
        return {'statusCode': 401}

    params = parse_qs(event['body'])
    text = params.get('text', 'help')[0].strip()
    print('FINE request -> ', text)

    if re.match(HELP_REGEX, text):
        response_body = response.create_help_response()
    elif re.match(FINE_REGEX, text):
        response_body = handle_fine_request(params, text)
    else:
        response_body = response.create_fallback_response()

    return response.wrap_response_body(response_body)


def handle_fine_request(params, text):
    user_name = params['user_name'][0]
    team_id = params['team_id'][0]
    # TODO: figure out why parse_qs is wrapping certain values, move to using parse_sql
    channel_id = params['channel_id'][0].strip("['']")
    user_name_fined = re.search(FINE_REGEX, text).group(1).strip()
    fine_id = str(uuid.uuid4())

    print('FINE writing to Dynamo -> {}, {}, {}'.format(team_id, channel_id, fine_id))
    dynamo.add_fine(team_id, channel_id, user_name, text, fine_id)
    return response.create_fine_response(user_name_fined)
    