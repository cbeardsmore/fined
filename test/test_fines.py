from urllib.parse import parse_qs
from urllib.parse import urlencode
import json
import time
import os
import pytest
import auth
import fines

SIGNING_SECRET = 'fake_secret'
HEADER_SLACK_TIMESTAMP = 'X-Slack-Request-Timestamp'
HEADER_SLACK_SIGNATURE = 'X-Slack-Signature'


@pytest.fixture(scope="function")
def mock_os(monkeypatch):
    monkeypatch.setitem(os.environ, 'SLACK_SIGNING_SECRET', 'fake_secret')
    monkeypatch.setitem(os.environ, 'DYNAMODB_TABLE', 'table_name')


@pytest.fixture(scope="function")
def event(mock_os):
    event_payload = []
    with open('local/fines.json') as file:
        event_payload = json.load(file)
    return update_signature(event_payload)


def test_handle_with_unverified_request_returns_401(event):
    event['headers'][HEADER_SLACK_SIGNATURE] = 'invalid'
    result = fines.handle(event, {})
    assert result['statusCode'] == 401


def update_signature(event):
    timestamp = time.time()
    signature = auth.generate_signature(
        SIGNING_SECRET, timestamp, event['body'])
    event['headers'][HEADER_SLACK_SIGNATURE] = signature
    event['headers'][HEADER_SLACK_TIMESTAMP] = timestamp
    return event


def set_body_text(body, text):
    params = parse_qs(body)
    params['text'] = text
    params['user_name'] = 'fake_user'
    params['team_id'] = 'fake_team_id'
    return urlencode(params)
