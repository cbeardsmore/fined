import json
import os
from moto import mock_dynamodb2
import pytest
import response
import fines
import utils
import const
import dynamo

@pytest.fixture(scope="function")
def mock_os(monkeypatch):
    monkeypatch.setitem(os.environ, 'SLACK_SIGNING_SECRET', const.SIGNING_SECRET)
    monkeypatch.setitem(os.environ, 'DYNAMODB_TABLE_FINES', const.DYNAMODB_TABLE_FINES)


@pytest.fixture(scope="function")
def event(mock_os):
    event_payload = []
    with open('test/payloads/fines.json') as file:
        event_payload = json.load(file)
    return utils.update_signature(event_payload)


def test_handle_with_unverified_request_returns_401(event):
    event['headers'][const.HEADER_SLACK_SIGNATURE] = 'invalid'
    result = fines.handle(event, {})
    assert result['statusCode'] == 401


def test_handle_with_help_text_returns_help(event):
    event['body'] = utils.set_body_text(event['body'], 'help')
    event = utils.update_signature(event)
    result = fines.handle(event, {})
    assert result['body'] == json.dumps(response.create_help_response())


@mock_dynamodb2
def test_handle_with_no_fines_returns_no_fines_response(event):
    event = utils.update_signature(event)
    dynamo.create_fine_table()
    result = fines.handle(event, {})
    assert result['body'] == json.dumps(response.create_no_fines_response())


@mock_dynamodb2
def test_handle_with_fine_text_returns_valid_response(event):
    text = '@fake_user_2 $50 for reason'
    event['body'] = utils.set_body_text(event['body'], '')
    event = utils.update_signature(event)

    dynamo.create_fine_table()
    dynamo.add_fine(const.TEAM_ID, const.CHANNEL_ID, const.USERNAME, text, const.FINE_ID)
    result = fines.handle(event, {})

    expected_fine = [{'finedBy': const.USERNAME, 'text': text, 'id': const.FINE_ID}]
    assert result['body'] == json.dumps(response.create_fines_response(expected_fine))
    