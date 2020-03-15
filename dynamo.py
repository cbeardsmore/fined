import os
import boto3

def update_item(team_id, user_name, text):
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')
    table_name = os.environ['DYNAMODB_TABLE']
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
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')
    table_name = os.environ['DYNAMODB_TABLE']
    return dynamodb.get_item(
        TableName=table_name,
        Key={'teamId': {'S': team_id}}
    )
