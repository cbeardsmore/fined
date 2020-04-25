import json
import os
import pytest
import interaction
import response
import utils
import const

@pytest.fixture(scope="function")
def mock_os(monkeypatch):
    monkeypatch.setitem(os.environ, 'SLACK_SIGNING_SECRET', const.SIGNING_SECRET)
    monkeypatch.setitem(os.environ, 'BOT_ACCESS_TOKEN', const.BOT_ACCESS_TOKEN)
    monkeypatch.setitem(os.environ, 'DYNAMODB_TABLE', const.DYNAMO_DB_TABLE)


@pytest.fixture(scope="function")
def event(mock_os):
    event_payload = []
    with open('local/interaction.json') as file:
        event_payload = json.load(file)
    return utils.update_signature(event_payload)


def test_handle_with_unverified_request_returns_401(event):
    event['headers'][const.HEADER_SLACK_SIGNATURE] = 'invalid'
    result = interaction.handle(event, {})
    assert result['statusCode'] == 401


def test_handle_sets_headers_and_status_code(event):
    result = interaction.handle(event, {})
    assert result['statusCode'] == 200
    assert result['headers']['Content-Type'] == 'application/json'


def test_handle_returns_empty_response(event):
    event = utils.update_signature(event)
    result = interaction.handle(event, {})
    assert result['body'] == json.dumps('')
