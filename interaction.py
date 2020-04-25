from urllib.parse import parse_qs
import json
import os
import requests
import auth
import response

OPEN_VIEW_POST_URL = 'https://slack.com/api/views.open'
CONTENT_TYPE = 'application/json; charset=utf-8'

def handle(event, _):
    if not auth.is_verified_request(event):
        return {'statusCode': 401}

    payload = json.loads(parse_qs(event['body'])['payload'][0])
    open_modal_response = open_modal(payload['trigger_id'])
    
    print(open_modal_response.content)
    return response.wrap_response_body('')


def open_modal(trigger_id):
    bot_access_token = os.environ['BOT_ACCESS_TOKEN']
    data = response.create_pay_model(trigger_id)
    headers = {
        'Content-Type': CONTENT_TYPE,
        'Authorization': 'Bearer {}'.format(bot_access_token)
    }
    return requests.post(OPEN_VIEW_POST_URL, headers=headers, data=json.dumps(data))
