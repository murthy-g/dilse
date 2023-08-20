import boto3
import json
from models.Match import Match

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
users_table = dynamodb.Table('users')
matches_table = dynamodb.Table('matches')

def lambda_like(event, context):
    data = json.loads(event['body'])

    current_user_id = data.json.get('current_user_id')
    liked_user_id = data.json.get('liked_user_id')
    
    # Check if the liked user has also liked the current user
    response = matches_table.get_item(Key={'user_id': liked_user_id, 'liked_user_id': current_user_id})

    match = None
    if 'Item' in response:
        match = Match(current_user_id, liked_user_id, 'matched')
    else:
        match = Match(current_user_id, liked_user_id)

    matches_table.put_item(Item=match.to_dynamo_item())

    return {
            "statusCode": 200,
            "body": json.dumps({'message': match.status == 'matched' and 'It\'s a match!' or 'Like registered!'}),
            'headers': {
                'Content-Type': 'application/json',
            }
        }