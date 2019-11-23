from auth import isVerifiedRequest

def handle(event, context):
    if not isVerifiedRequest(event):
        return { "statusCode": 401 }
    print("Valid Fines request")
    return { "statusCode": 200 }