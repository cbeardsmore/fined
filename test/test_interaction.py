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
def event_pb(mock_os):
    event_payload = []
    with open('local/pay_button.json') as file:
        event_payload = json.load(file)
    return utils.update_signature(event_payload)


@pytest.fixture(scope="function")
def event_vs(mock_os):
    event_payload = []
    with open('local/view_submission.json') as file:
        event_payload = json.load(file)
    return utils.update_signature(event_payload)


def test_handle_with_unverified_request_returns_401(event_pb):
    event_pb['headers'][const.HEADER_SLACK_SIGNATURE] = 'invalid'
    result = interaction.handle(event_pb, {})
    assert result['statusCode'] == 401


def test_handle_returns_empty_response(event_pb):
    result = interaction.handle(event_pb, {})
    assert result['statusCode'] == 200
    assert result['headers']['Content-Type'] == 'application/json'
    assert result['body'] == ''


def test_handle_with_unknown_action_does_nothing(requests_mock, event_pb):
    event_pb['body'] = utils.set_interaction_action_id(event_pb['body'], 'random_action_id')
    event_pb = utils.update_signature(event_pb)
    requests_mock.post(interaction.OPEN_VIEW_POST_URL)

    interaction.handle(event_pb, {})
    assert requests_mock.call_count == 0

def test_handle_with_pay_action_calls_slack_view_open(requests_mock, event_pb):
    event_pb['body'] = utils.set_interaction_action_id(event_pb['body'], interaction.ACTION_PAY_FINE)
    event_pb = utils.update_signature(event_pb)
    requests_mock.post(interaction.OPEN_VIEW_POST_URL)

    interaction.handle(event_pb, {})
    last_request = requests_mock.last_request

    assert requests_mock.call_count == 1
    assert last_request.json() == response.create_pay_model(const.TRIGGER_ID)
    assert last_request.headers['Content-Type'] == interaction.CONTENT_TYPE
    assert last_request.headers['Authorization'] == 'Bearer {}'.format(const.BOT_ACCESS_TOKEN)


def test_handle_with_view_submission_does_nothing(requests_mock, event_vs):
    requests_mock.post(interaction.OPEN_VIEW_POST_URL)
    interaction.handle(event_vs, {})
    assert requests_mock.call_count == 0
