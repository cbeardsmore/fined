from urllib.parse import parse_qs
import json
import auth
import response

def handle(event, _):
    if not auth.is_verified_request(event):
        return {'statusCode': 401}

    payload = json.loads(parse_qs(event['body'])['payload'][0])
    print(payload)
    return response.wrap_response_body(response.create_help_response())
