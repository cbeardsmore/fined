import json
import os
import pytest
import interaction
import utils
import const
import response

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


def test_handle_returns_empty_response(event):
    result = interaction.handle(event, {})
    assert result['statusCode'] == 200
    assert result['headers']['Content-Type'] == 'application/json'
    assert result['body'] == json.dumps('')


def test_handle_with_unknown_action_does_nothing(requests_mock, event):
    event['body'] = utils.set_interaction_action_id(event['body'], 'random_action_id')
    event = utils.update_signature(event)
    requests_mock.post(interaction.OPEN_VIEW_POST_URL)

    interaction.handle(event, {})
    assert requests_mock.call_count == 0

def test_handle_with_pay_action_calls_slack_view_open(requests_mock, event):
    event['body'] = utils.set_interaction_action_id(event['body'], interaction.ACTION_PAY_FINE)
    event = utils.update_signature(event)
    requests_mock.post(interaction.OPEN_VIEW_POST_URL)

    interaction.handle(event, {})
    last_request = requests_mock.last_request

    assert requests_mock.call_count == 1
    assert last_request.json() == response.create_pay_model(const.TRIGGER_ID)
    assert last_request.headers['Content-Type'] == interaction.CONTENT_TYPE
    assert last_request.headers['Authorization'] == 'Bearer {}'.format(const.BOT_ACCESS_TOKEN)
