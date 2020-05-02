import json
import auth
import response

def handle(event, _):
    if not auth.is_verified_request(event):
        return {'statusCode': 401}

    print(json.dumps(event))
    return response.create_empty_response()
