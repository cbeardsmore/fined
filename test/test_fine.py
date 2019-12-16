import fine
import time
import json


def test_is_verified_request_for_valid_request():
    event = []
    with open('local/fine.json') as file:
        event = json.load(file)

    print(event)

    fine.handle(event, {})
    assert 1 == 2

