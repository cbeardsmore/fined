import json
import os
import pytest
import fines
import utils
import const

@pytest.fixture(scope="function")
def mock_os(monkeypatch):
    monkeypatch.setitem(os.environ, 'SLACK_SIGNING_SECRET', const.SIGNING_SECRET)
    monkeypatch.setitem(os.environ, 'DYNAMODB_TABLE', const.DYNAMO_DB_TABLE)


@pytest.fixture(scope="function")
def event(mock_os):
    event_payload = []
    with open('local/fines.json') as file:
        event_payload = json.load(file)
    return utils.update_signature(event_payload)


def test_handle_with_unverified_request_returns_401(event):
    event['headers'][const.HEADER_SLACK_SIGNATURE] = 'invalid'
    result = fines.handle(event, {})
    assert result['statusCode'] == 401
