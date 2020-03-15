from urllib.parse import parse_qs
import auth
import dynamo
import response

def handle(event, _):
    if not auth.is_verified_request(event):
        return {"statusCode": 401}

    params = parse_qs(event['body'])
    team_id = params['team_id'][0]
    team_fines = dynamo.get_item(team_id)

    if team_fines is None:
        body = response.create_no_fines_response()
        return response.wrap_response_body(body)

    team_fines_formatted = format_team_fines(team_fines)
    body = response.create_fines_response(team_fines_formatted)
    return response.wrap_response_body(body)

def format_team_fines(fines):
    fines = [x['text'] for x in fines]
    fines = "\n \u2022 ".join(fines)
    return fines
