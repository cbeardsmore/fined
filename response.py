import json


def wrap_response_body(response_body):
    return {
        "statusCode": 200,
        "body": json.dumps(response_body),
        "headers": {
            "Content-Type": "application/json"
        }
    }


def create_fallback_response():
    return {
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


def create_no_fines_response():
    return {
        "response_type": "ephermeral",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "There are no fines for this channel! Use the /fine command to fine a teammate."
                }
            }
        ]
    }


def create_fine_response(user_name):
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


def create_fines_response(team_fines):
    response_template = {
        "response_type": "in_channel",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "\U0001F4B0 *Current Team Fines:* \U0001F4B0"
                }
            },
            {
                "type": "divider"
            }
        ]
    }

    for fine in team_fines:
        response_template['blocks'].append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "\u2022 {} ".format(fine)
                },
                "accessory": {
                    "type": "button",
                    "style": "primary",
                    "text": {
                        "type": "plain_text",
                        "text": "Pay",
                        "emoji": True
                    },
                    "value": "Pay"
                }
            }
        )

    response_template['blocks'].append(
        {
            "type": "divider"
        }
    )

    return response_template


def create_help_response():
    return {
        "response_type": "ephermeral",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Hey there 👋 I'm FinedBot and I'm here to help. 🤖"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*1️⃣ Use the `/fine` command*. 🤔 Someone on your team deserves a fine? Type `/fine` followed by the victims alias, the cost and the reason. Here's some examples:\n • `/fine @Tim $5 for messing up the CSS...again`\n• `/fine @Sam $10 for wearing Activewear after 9am`\n• `/fine Jack $10 for being late to standup for the 5th time this week`\n\n Make sure you always follow the required format of: \n • `/fine @user $cost for reason`"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*2️⃣ Use the `/fines` command.* 👮‍♀️ Get a list of your teams biggest offenders and who needs to pay up. They'll be prompted to remind them of their outstanding fines:"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*3️⃣ Pay up!* 💰Users can mark their fines as paid. Shout a teammate a coffee, pay for the next group lunch, or donate to your favourite charity. It's up to you to keep people honest. Here's a few of our favourite:\n• http://www.americanhumane.org/\n• https://www.hopeforthewarriors.org/\n• https://www.beyondblue.org.au/ "
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": " 💻Check out the code at https://github.com/cbeardsmore/fined\n ❓Get help at any time with `/fine help\n"
                    }
                ]
            }
        ]
    }
