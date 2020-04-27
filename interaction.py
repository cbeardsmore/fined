from urllib.parse import parse_qs
import json
import os
import requests
import auth
import response

OPEN_VIEW_POST_URL = 'https://slack.com/api/views.open'
CONTENT_TYPE = 'application/json; charset=utf-8'

ACTION_PAY_FINE = 'pay_fine_button'
VIEW_SUBMISSION_TYPE = 'view_submission'
BLOCK_INTERACTION_TYPE = 'block_actions'


def handle(event, _):
    if not auth.is_verified_request(event):
        return {'statusCode': 401}

    payload = json.loads(parse_qs(event['body'])['payload'][0])
    payload_type = payload['type']

    if payload_type == BLOCK_INTERACTION_TYPE:
        handle_block_interaction(payload)
    elif payload_type == VIEW_SUBMISSION_TYPE:
        handle_view_submission(payload)

    return response.create_empty_response()


def handle_block_interaction(payload):
    trigger_action = payload['actions'][0]
    action_id = trigger_action['action_id']

    if action_id == ACTION_PAY_FINE:
        open_modal(payload['trigger_id'])


def open_modal(trigger_id):
    bot_access_token = os.environ['BOT_ACCESS_TOKEN']
    data = response.create_pay_model(trigger_id)

    headers = {
        'Content-Type': CONTENT_TYPE,
        'Authorization': 'Bearer {}'.format(bot_access_token)
    }
    return requests.post(OPEN_VIEW_POST_URL, headers=headers, data=json.dumps(data))


def handle_view_submission(payload):
    # todo: handle modal submissions via DynamoDB deletion
    print(payload)
    