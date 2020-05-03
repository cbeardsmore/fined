import os
import boto3
from boto3.dynamodb.types import TypeDeserializer

AWS_REGION = 'us-east-1'
DYNAMO_ENV_KEY = 'DYNAMODB_TABLE_FINES'


def add_fine(team_id, channel_id, user_name, text, id):
    dynamodb = boto3.client('dynamodb', region_name=AWS_REGION)
    table_name = os.environ[DYNAMO_ENV_KEY]
    team_channel_id = get_team_channel_id(team_id, channel_id)
    dynamodb.update_item(
        TableName=table_name,
        Key={'teamChannelId': {'S': team_channel_id}},
        UpdateExpression='SET teamFines = list_append(if_not_exists(teamFines, :emptyList), :fine)',
        ExpressionAttributeValues={
            ':emptyList': {'L': []},
            ':fine': {'L': [{'M': {
                'finedBy': {'S': user_name},
                'text': {'S': text},
                'id': {'S': id}
            }}]}
        }
    )


def update_access_token(team_id, access_token):
    dynamodb = boto3.client('dynamodb', region_name=AWS_REGION)
    table_name = os.environ[DYNAMO_ENV_KEY]
    print(team_id, access_token)


def delete_fine(team_id, channel_id, fine_id):
    team_fines = get_fines(team_id, channel_id)
    fine_index_list = [x for x in range(len(team_fines)) if team_fines[x]['id'] == fine_id]
    fine_index = str(fine_index_list[0])

    dynamodb = boto3.client('dynamodb', region_name=AWS_REGION)
    table_name = os.environ[DYNAMO_ENV_KEY]
    team_channel_id = get_team_channel_id(team_id, channel_id)

    dynamodb.update_item(
        TableName=table_name,
        Key={'teamChannelId': {'S': team_channel_id}},
        UpdateExpression='REMOVE teamFines[' + fine_index + ']',
        ConditionExpression='teamFines[' + fine_index + '].id = :fineId',
        ExpressionAttributeValues={
            ':fineId': {'S': fine_id}
        }
    )


def get_fines(team_id, channel_id):
    dynamodb = boto3.client('dynamodb', region_name=AWS_REGION)
    table_name = os.environ[DYNAMO_ENV_KEY]
    team_channel_id = get_team_channel_id(team_id, channel_id)

    dynamo_response = dynamodb.get_item(
        TableName=table_name,
        Key={'teamChannelId': {'S': team_channel_id}}
    )

    if (dynamo_response.get('Item') is None or dynamo_response['Item']['teamFines'] is None):
        return None

    team_fines = dynamo_response['Item']['teamFines']
    return TypeDeserializer().deserialize(team_fines)


def create_table():
    dynamodb = boto3.client('dynamodb', region_name=AWS_REGION)
    table_name = os.environ[DYNAMO_ENV_KEY]
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{
            'AttributeName': 'teamChannelId',
            'KeyType': 'HASH'
        }],
        AttributeDefinitions=[
            {
                'AttributeName': 'teamChannelId',
                'AttributeType': 'S'
            }
        ],
    )


def get_team_channel_id(team_id, channel_id):
    print('teamId: {}, channelId: {}'.format(team_id, channel_id))
    return '{}-{}'.format(team_id, channel_id)
