from urllib.parse import parse_qs
from urllib.parse import urlencode
import json
import time
import os
import pytest
import auth
import fine
import response

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
    with open('local/fine.json') as file:
        event_payload = json.load(file)
    return update_signature(event_payload)

def test_handle_with_unverified_request_returns_401(event):
    event['headers'][HEADER_SLACK_SIGNATURE] = 'invalid'
    result = fine.handle(event, {})
    assert result['statusCode'] == 401

def test_handle_sets_headers_and_status_code(event):
    result = fine.handle(event, {})
    assert result['statusCode'] == 200
    assert result['headers']['Content-Type'] == 'application/json'

def test_handle_with_no_text_returns_fallback(event):
    event['body'] = set_body_text(event['body'], 'invalid_text')
    event = update_signature(event)
    result = fine.handle(event, {})
    assert result['body'] == json.dumps(response.create_fallback_response())

def test_handle_with_help_text_returns_help(event):
    event['body'] = set_body_text(event['body'], 'help')
    event = update_signature(event)
    result = fine.handle(event, {})
    assert result['body'] == json.dumps(response.create_help_response())


# HELPER METHODS
def update_signature(event):
    timestamp = time.time()
    signature = auth.generate_signature(SIGNING_SECRET, timestamp, event['body'])
    event['headers'][HEADER_SLACK_SIGNATURE] = signature
    event['headers'][HEADER_SLACK_TIMESTAMP] = timestamp
    return event

def set_body_text(body, text):
    params = parse_qs(body)
    params['text'] = text
    return urlencode(params)
