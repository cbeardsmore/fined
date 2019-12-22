import json

def wrap_response_body(response_body):
    return {
        "statusCode": 200,
        "body": json.dumps(response_body),
        "headers": {
            "Content-Type": "application/json"
        }
    }

def handle_help_request():
    return  {
        "response_type": "ephermeral",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "/fine user $amount for ...."
                }
            }
        ]
    }

def handle_fallback():
    return  {
        "response_type": "ephermeral",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Oops! I didn't quite catch that...try /fine help for how to use Fined!"
                }
            }
        ]
    }

def handle_fine_response(user_name):
    return {
        "response_type": "in_channel",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "@{} has been fined. Shame on them!".format(user_name)
                }
            }
        ]
    }
