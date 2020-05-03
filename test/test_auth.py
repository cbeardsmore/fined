import json
import time
import os
import pytest
import auth
import const

@pytest.fixture(scope="function")
def event(monkeypatch):
    monkeypatch.setitem(os.environ, 'SLACK_SIGNING_SECRET', const.SIGNING_SECRET)
    with open('test/payloads/fine.json') as file:
        return json.load(file)

def test_is_verified_request_for_valid_request(event):
    timestamp = time.time()
    signature = auth.generate_signature(const.SIGNING_SECRET, timestamp, event['body'])
    event['headers'][const.HEADER_SLACK_SIGNATURE] = signature
    event['headers'][const.HEADER_SLACK_TIMESTAMP] = timestamp

    assert auth.is_verified_request(event)

def test_is_verified_request_for_expired_request(event):
    timestamp = time.time() - 60 * 6
    signature = auth.generate_signature(const.SIGNING_SECRET, timestamp, event['body'])
    event['headers'][const.HEADER_SLACK_SIGNATURE] = signature
    event['headers'][const.HEADER_SLACK_TIMESTAMP] = timestamp

    assert not auth.is_verified_request(event)

def test_is_verified_request_for_invalid_secret(event):
    timestamp = time.time()
    signature = auth.generate_signature('this_secret_is_wrong', timestamp, event['body'])
    event['headers'][const.HEADER_SLACK_SIGNATURE] = signature
    event['headers'][const.HEADER_SLACK_TIMESTAMP] = timestamp

    assert not auth.is_verified_request(event)
