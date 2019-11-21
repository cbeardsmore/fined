import json
import urllib.parse

def handle(event, context):
    print(event)
    return { "statusCode": 200 }