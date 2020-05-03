import json
import os
from moto import mock_dynamodb2
import pytest
import oauth
import const
import dynamo


@pytest.fixture(scope="function")
def mock_os(monkeypatch):
    monkeypatch.setitem(os.environ, 'SLACK_SIGNING_SECRET', const.SIGNING_SECRET)
    monkeypatch.setitem(os.environ, 'DYNAMODB_TABLE_FINES', const.DYNAMODB_TABLE_FINES)
    monkeypatch.setitem(os.environ, 'DYNAMODB_TABLE_TOKENS', const.DYNAMODB_TABLE_TOKENS)
    monkeypatch.setitem(os.environ, 'CLIENT_ID', const.CLIENT_ID)
    monkeypatch.setitem(os.environ, 'CLIENT_SECRET', const.CLIENT_SECRET)


@pytest.fixture(scope="function")
def event(mock_os):
    with open('test/payloads/oauth.json') as file:
        return json.load(file)


def test_handle_with_invalid_state_returns_401(event):
    event['queryStringParameters']['state'] = 'invalid_state'
    result = oauth.handle(event, {})
    assert result['statusCode'] == 401


@mock_dynamodb2
def test_handle_with_valid_state_returns_empty_response(requests_mock, event):
    dynamo.create_token_table()
    requests_mock.post(oauth.OAUTH_ACCESS_POST_URL, text=json.dumps({
        'team': {'id': const.TEAM_ID, 'name': const.TEAM_NAME},
        'access_token': const.BOT_ACCESS_TOKEN
    }))

    result = oauth.handle(event, {})
    assert result['statusCode'] == 200
    assert result['headers']['Content-Type'] == 'application/json'
    assert result['body'] == ''


@mock_dynamodb2
def test_handle_with_valid_state_exchanges_access_token(requests_mock, event):
    dynamo.create_token_table()
    requests_mock.post(oauth.OAUTH_ACCESS_POST_URL, text=json.dumps({
        'team': {'id': const.TEAM_ID, 'name': const.TEAM_NAME},
        'access_token': const.BOT_ACCESS_TOKEN
    }))

    oauth.handle(event, {})

    expected_text = 'client_id={}&client_secret={}&code={}'.format(
        const.CLIENT_ID, const.CLIENT_SECRET, const.AUTH_CODE)
    assert requests_mock.call_count == 1
    assert requests_mock.last_request.text != expected_text


@mock_dynamodb2
def test_handle_with_valid_state_updates_dynamo(requests_mock, event):
    dynamo.create_token_table()
    requests_mock.post(oauth.OAUTH_ACCESS_POST_URL, text=json.dumps({
        'team': {'id': const.TEAM_ID, 'name': const.TEAM_NAME},
        'access_token': const.BOT_ACCESS_TOKEN
    }))

    oauth.handle(event, {})
    assert dynamo.get_access_token(const.TEAM_ID) == const.BOT_ACCESS_TOKEN
