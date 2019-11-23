from urllib.parse import parse_qs
from auth import isVerifiedRequest

def handle(event, context):
    if not isVerifiedRequest(event):
        return { "statusCode": 401 }

    params = parse_qs(event['body'])
    text = params['text'][0]
    user_name = params['user_name'][0]

    print('Text -> ', text)
    print('User Name -> ', user_name)
    return { "statusCode": 200 }

