import json
import os
import pytest
import oauth
import const


@pytest.fixture(scope="function")
def mock_os(monkeypatch):
    monkeypatch.setitem(os.environ, 'SLACK_SIGNING_SECRET',
                        const.SIGNING_SECRET)
    monkeypatch.setitem(os.environ, 'DYNAMODB_TABLE_FINES',
                        const.DYNAMO_DB_TABLE)
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


def test_handle_with_valid_state_returns_empty_response(requests_mock, event):
    requests_mock.post(oauth.OAUTH_ACCESS_POST_URL, text=json.dumps({
        'team': {'id': 'fake_team_id'},
        'access_token': 'fake_access_token'
    }))
    result = oauth.handle(event, {})
    assert result['statusCode'] == 200
    assert result['headers']['Content-Type'] == 'application/json'
    assert result['body'] == ''


def test_handle_with_valid_state_exchanges_access_token(requests_mock, event):
    requests_mock.post(oauth.OAUTH_ACCESS_POST_URL, text=json.dumps({
        'team': {'id': 'fake_team_id'},
        'access_token': 'fake_access_token'
    }))

    oauth.handle(event, {})

    expected_text = 'client_id={}&client_secret={}&code={}'.format(
        const.CLIENT_ID, const.CLIENT_SECRET, const.AUTH_CODE)
    assert requests_mock.call_count == 1
    assert requests_mock.last_request.text == expected_text
