import json
import urllib.parse

def handle(event, context):
    print(event['body'])
    params = parse_qs(event['body'])

    text = params['text'][0]
    user_name = params['user_name'][0]

    print('Text -> ', text)
    print('User Name -> ', user_name)

    return { "statusCode": 200 }