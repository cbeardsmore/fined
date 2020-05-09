OAUTH_AUTHORIZE_URL = 'https://slack.com/oauth/v2/authorize?client_id=839622902965.1103591322370&scope=commands&state=magic_state_parameter'

def handle(event, _):
    return {
        "statusCode": 302,
        "headers": {
            "Location": OAUTH_AUTHORIZE_URL
        }
    }
