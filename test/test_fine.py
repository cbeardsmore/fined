import json
import os
from moto import mock_dynamodb2
import pytest
import fine
import response
import dynamo
import utils
import const

@pytest.fixture(scope="function")
def mock_os(monkeypatch):
    monkeypatch.setitem(os.environ, 'SLACK_SIGNING_SECRET', const.SIGNING_SECRET)
    monkeypatch.setitem(os.environ, 'DYNAMODB_TABLE', const.DYNAMO_DB_TABLE)


@pytest.fixture(scope="function")
def event(mock_os):
    event_payload = []
    with open('local/fine.json') as file:
        event_payload = json.load(file)
    return utils.update_signature(event_payload)


def test_handle_with_unverified_request_returns_401(event):
    event['headers'][const.HEADER_SLACK_SIGNATURE] = 'invalid'
    result = fine.handle(event, {})
    assert result['statusCode'] == 401


def test_handle_sets_headers_and_status_code(event):
    result = fine.handle(event, {})
    assert result['statusCode'] == 200
    assert result['headers']['Content-Type'] == 'application/json'


def test_handle_with_no_text_returns_fallback(event):
    event['body'] = utils.set_body_text(event['body'], 'invalid_text')
    event = utils.update_signature(event)
    result = fine.handle(event, {})
    assert result['body'] == json.dumps(response.create_fallback_response())


def test_handle_with_help_text_returns_help(event):
    event['body'] = utils.set_body_text(event['body'], 'help')
    event = utils.update_signature(event)
    result = fine.handle(event, {})
    assert result['body'] == json.dumps(response.create_help_response())


@mock_dynamodb2
def test_handle_with_fine_text_returns_valid_response(event):
    body_text = '@{} $50 for reason'.format(const.USERNAME_FINED)
    event['body'] = utils.set_body_text(event['body'], body_text)
    event = utils.update_signature(event)
    dynamo.create_table()
    result = fine.handle(event, {})
    assert result['body'] == json.dumps(response.create_fine_response(const.USERNAME_FINED))


@mock_dynamodb2
def test_handle_with_fine_text_saves_dynamo_item(event):
    text = '@fake_user_2 $50 for reason'
    event['body'] = utils.set_body_text(event['body'], text)
    event = utils.update_signature(event)
    dynamo.create_table()
    fine.handle(event, {})
    print(event)
    fine_item = dynamo.get_fines(const.TEAM_ID, const.CHANNEL_ID)[0]
    assert fine_item['finedBy'] == const.USERNAME
    assert fine_item['text'] == text
    assert fine_item['id'] is not None
    