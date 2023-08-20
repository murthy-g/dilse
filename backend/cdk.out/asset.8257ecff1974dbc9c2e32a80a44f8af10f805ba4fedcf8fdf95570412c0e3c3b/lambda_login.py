import jsonify
import boto3
import json
from boto3.dynamodb.conditions import Key, Attr


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
users_table = dynamodb.Table('users')
matches_table = dynamodb.Table('matches')
photos_table = dynamodb.Table('user_photos')

def lambda_login(event, context):
    data = json.loads(event['body'])

    email = data.json.get('email')
    password = data.json.get('password')  # Note: in real-world apps, compare hashed passwords!

    # For simplicity, we're fetching by user_id. In real apps, you'll likely fetch by email.
    response = users_table.scan(FilterExpression=Attr('email').eq(email) & Attr('password').eq(password))
    
    if 'Items' in response and len(response['Items']) > 0:
        return jsonify({'message': 'Login successful!', 'user_id': response['Items'][0]['user_id']}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

