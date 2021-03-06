from urllib.parse import parse_qs
import json
import os
import requests
import auth
import response
import dynamo

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
    print('INTERACTION payload received -> ', payload_type)

    if payload_type == BLOCK_INTERACTION_TYPE:
        handle_block_interaction(payload)
    elif payload_type == VIEW_SUBMISSION_TYPE:
        handle_view_submission(payload)

    return response.create_empty_response()


def handle_block_interaction(payload):
    trigger_action = payload['actions'][0]
    action_id = trigger_action['action_id']
    action_value = trigger_action['value']
    channel_id = payload['channel']['id']
    team_id = payload['team']['id']

    if action_id == ACTION_PAY_FINE:
        print('INTERACTION modal opened -> {}, {}, {}'.format(team_id, channel_id, action_value))
        open_modal(payload['trigger_id'], team_id, channel_id, action_value)


def open_modal(trigger_id, team_id, channel_id, fine_id):
    bot_access_token = dynamo.get_access_token(team_id)
    data = response.create_pay_modal(trigger_id, channel_id, fine_id)

    headers = {
        'Content-Type': CONTENT_TYPE,
        'Authorization': 'Bearer {}'.format(bot_access_token)
    }
    return requests.post(OPEN_VIEW_POST_URL, headers=headers, data=json.dumps(data))


def handle_view_submission(payload):
    team_id = payload['team']['id']
    channel_id = payload['view']['callback_id']
    fine_id = payload['view']['private_metadata']
    
    print('INTERACTION deleting fine -> {}, {}, {}'.format(team_id, channel_id, fine_id))
    dynamo.delete_fine(team_id, channel_id, fine_id)
