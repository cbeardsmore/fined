import json


def wrap_response_body(response_body):
    return {
        "statusCode": 200,
        "body": json.dumps(response_body),
        "headers": {
            "Content-Type": "application/json"
        }
    }

def create_empty_response():
    return {
        "statusCode": 200,
        "body": "",
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
                    "text": "\u2022 {} ".format(fine['text'])
                },
                "accessory": {
                    "type": "button",
                    "style": "primary",
                    "action_id": "pay_fine_button",
                    "text": {
                        "type": "plain_text",
                        "text": "Pay",
                        "emoji": True
                    },
                    "value": fine['id']
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


def create_pay_modal(trigger_id, channel_id, fine_id):
    return {
        "trigger_id": trigger_id,
        "view": {
            "type": "modal",
            "callback_id": channel_id,
            "private_metadata": fine_id,
            "title": {
                "type": "plain_text",
                "text": "Pay Your Fine!",
                "emoji": True
            },
            "submit": {
                "type": "plain_text",
                "text": "Mark as Paid",
                "emoji": True
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "💵 Time to pay up. You have 2 choices"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*🙆‍♂️ Pay the Team*"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "It's up to you how you payback the team. Our favourites include:\n\n     • Shout a coffee ☕️\n     • Pay for team lunch 🍔\n     • Buy the next round 🍻"
                    }

                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*❤️ Donate to Charity*"
                    }

                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Pay it forward to a charity of your choice and give back to the community Here's some popular choices:\n\n     • <http://www.americanhumane.org/|American Humane>\n     • <https://www.hopeforthewarriors.org/| Hope for the Warriors>\n     • <https://www.beyondblue.org.au/|Beyond Blue>"
                    }

                }
            ]
        }
    }
