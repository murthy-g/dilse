import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
users_table = dynamodb.Table('users')
matches_table = dynamodb.Table('matches')

def get_recommendations(event, context):
    user_id = event['pathParameters']['user_id']

    # 1. Find mutual likes
    mutual_matches = matches_table.query(
        IndexName="LikedUserIndex",  # Assuming you've a GSI on liked_user_id
        KeyConditionExpression=Key('liked_user_id').eq(user_id) & Key('status').eq('matched')
    )

    mutual_likes = [item['user_id'] for item in mutual_matches.get('Items', [])]

    # 2. Find users liked by the current user but haven't responded yet
    liked_users = matches_table.query(
        KeyConditionExpression=Key('user_id').eq(user_id) & Attr('status').eq('liked')
    )

    liked_user_ids = [item['liked_user_id'] for item in liked_users.get('Items', []) if item['liked_user_id'] not in mutual_likes]

    # Fetch profiles for mutual likes and liked users
    profiles = []

    for uid in mutual_likes + liked_user_ids:
        user = users_table.get_item(Key={'user_id': uid})
        if 'Item' in user:
            profiles.append(user['Item'])

    # Note: For simplicity, we're not fetching new user recommendations in this example

    return {
        'statusCode': 200,
        'body': json.dumps(profiles)
    }
