import os
import requests
import response
import dynamo

ADD_TO_SLACK_STATE = 'magic_state_parameter'
OAUTH_ACCESS_POST_URL = 'https://slack.com/api/oauth.v2.access'
CONTENT_TYPE = 'application/x-www-form-urlencoded'

def handle(event, _):
    query_parameters = event['queryStringParameters']

    if query_parameters['state'] != ADD_TO_SLACK_STATE:
        return {'statusCode': 401}

    team, access_token = exchange_auth_code(query_parameters['code'])
    dynamo.update_access_token(team, access_token)

    return response.create_redirect_response()


def exchange_auth_code(code):
    headers = {'Content-Type': CONTENT_TYPE}
    data = {
        'client_id': os.environ['CLIENT_ID'],
        'client_secret': os.environ['CLIENT_SECRET'],
        'code': code
    }

    access_token_payload = requests.post(OAUTH_ACCESS_POST_URL, headers=headers, data=data)
    body = access_token_payload.json()
    return body['team'], body['access_token']
