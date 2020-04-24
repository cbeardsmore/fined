from urllib.parse import parse_qs
import auth
import response
import json

def handle(event, _):
    if not auth.is_verified_request(event):
        return {'statusCode': 401}

    print(json.dumps(event))
    return response.wrap_response_body(response.create_help_response())
