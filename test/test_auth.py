import auth
import fine
import json
import time
import pytest

SIGNING_SECRET = 'fake_secret'
HEADER_SLACK_TIMESTAMP = 'X-Slack-Request-Timestamp'
HEADER_SLACK_SIGNATURE = 'X-Slack-Signature'

@pytest.fixture(scope="session")
def event():
    with open('local/fine.json') as file:
        return json.load(file)

def test_is_verified_request_for_valid_request(event):
    timestamp = time.time()
    signature = auth.generate_signature(SIGNING_SECRET, timestamp, event['body'])
    event['headers'][HEADER_SLACK_SIGNATURE] = signature
    event['headers'][HEADER_SLACK_TIMESTAMP] = timestamp

    result = fine.handle(event, {})
    assert result['statusCode'] == 200

def test_is_verified_request_for_expired_request(event):
    timestamp = time.time() - 60 * 6
    signature = auth.generate_signature(SIGNING_SECRET, timestamp, event['body'])
    event['headers'][HEADER_SLACK_SIGNATURE] = signature
    event['headers'][HEADER_SLACK_TIMESTAMP] = timestamp

    result = fine.handle(event, {})
    assert result['statusCode'] == 401

def test_is_verified_request_for_invalid_secret(event):
    timestamp = time.time() - 60 * 6
    signature = auth.generate_signature('this_secret_is_wrong', timestamp, event['body'])
    event['headers'][HEADER_SLACK_SIGNATURE] = signature
    event['headers'][HEADER_SLACK_TIMESTAMP] = timestamp

    result = fine.handle(event, {})
    assert result['statusCode'] == 401