import os
import boto3
from boto3.dynamodb.types import TypeDeserializer

AWS_REGION = 'us-east-1'
DYNAMO_ENV_KEY = 'DYNAMODB_TABLE'

def update_item(team_id, user_name, text):
    dynamodb = boto3.client('dynamodb', region_name=AWS_REGION)
    table_name = os.environ[DYNAMO_ENV_KEY]
    dynamodb.update_item(
        TableName=table_name,
        Key={'teamId': {'S': team_id}},
        UpdateExpression='SET teamFines = list_append(if_not_exists(teamFines, :emptyList), :fine)',
        ExpressionAttributeValues={
            ':emptyList': {'L':[]},
            ':fine': {'L': [{'M': {'finedBy': {'S': user_name}, 'text': {'S': text}}}]}
        }
    )

def get_item(team_id):
    dynamodb = boto3.client('dynamodb', region_name=AWS_REGION)
    table_name = os.environ[DYNAMO_ENV_KEY]
    dynamo_response = dynamodb.get_item(
        TableName=table_name,
        Key={'teamId': {'S': team_id}}
    )

    if (dynamo_response.get('Item') is None or dynamo_response['Item']['teamFines'] is None):
        return None

    team_fines = dynamo_response['Item']['teamFines']
    return TypeDeserializer().deserialize(team_fines)
