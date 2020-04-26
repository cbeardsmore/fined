from urllib.parse import parse_qs, urlencode
import time
import json
import auth
import const


def update_signature(event):
    timestamp = time.time()
    signature = auth.generate_signature(
        const.SIGNING_SECRET, timestamp, event['body'])
    event['headers'][const.HEADER_SLACK_SIGNATURE] = signature
    event['headers'][const.HEADER_SLACK_TIMESTAMP] = timestamp
    return event


def set_body_text(body, text):
    params = parse_qs(body)
    params['text'] = text
    params['user_name'] = const.USERNAME
    params['team_id'] = const.TEAM_ID
    return urlencode(params)


def set_interaction_payload_field(body, field, value):
    params = parse_qs(body)
    payload = json.loads(params['payload'][0])
    payload[field] = value
    params['payload'] = json.dumps(payload)
    return urlencode(params)


def set_interaction_action_id(body, value):
    params = parse_qs(body)
    payload = json.loads(params['payload'][0])
    payload['actions'][0]['action_id'] = value
    params['payload'] = json.dumps(payload)
    return urlencode(params)
