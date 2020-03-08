import os
import time
import hashlib
import hmac

HEADER_SLACK_TIMESTAMP = 'X-Slack-Request-Timestamp'
HEADER_SLACK_SIGNATURE = 'X-Slack-Signature'
BYTES_ENCODING = 'latin-1'

def is_verified_request(event):
    signing_secret = os.environ['SLACK_SIGNING_SECRET']
    signature = event['headers'][HEADER_SLACK_SIGNATURE]
    timestamp = event['headers'][HEADER_SLACK_TIMESTAMP]

    if abs(time.time() - int(timestamp)) > 60 * 5:
        print('Replay attack check failed. Time out by 5+ minutes')
        return False

    calculated_signature = generate_signature(signing_secret, timestamp, event['body'])

    if not hmac.compare_digest(signature, calculated_signature):
        print('Invalid signature. Does not match X-Slack-Signature')
        return False

    return True

def generate_signature(signing_secret, timestamp, body):
    calculated_basestring = 'v0:{}:{}'.format(timestamp, body)
    return 'v0=' + hmac.new(
        bytes(signing_secret, BYTES_ENCODING),
        msg=bytes(calculated_basestring, BYTES_ENCODING),
        digestmod=hashlib.sha256
    ).hexdigest()
