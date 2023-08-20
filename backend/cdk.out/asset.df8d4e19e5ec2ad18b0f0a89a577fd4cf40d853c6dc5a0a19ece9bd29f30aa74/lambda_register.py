from models.User import User
from models.Match import Match
from boto3.dynamodb.conditions import Key, Attr
import json
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
users_table = dynamodb.Table('users')
matches_table = dynamodb.Table('matches')
photos_table = dynamodb.Table('user_photos')

def lambda_register(event, context):
    data = json.loads(event['body'])

    # Check if email already exists using GSI
    email_check = users_table.query(
        IndexName='EmailIndex',  # Replace with your GSI name
        KeyConditionExpression=Key('email').eq(data['email'])
    )
    
    if 'Items' in email_check and len(email_check['Items']) > 0:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Email already exists"}),
            'headers': {
                'Content-Type': 'application/json',
            }
        }
    
    user = User(
        name=data['name'],
        email=data['email'],
        password=data['password'],  # Reminder: Store hashed password!
        age=data['age'],
        gender=data['gender'],
        location=data['location'],
        phone_number=data['phone_number']  # Add phone number here
    )

    response = users_table.put_item(Item=user.to_dynamo_item())

    return {
        'statusCode': 201,
        'body': json.dumps(response),
        'headers': {
            'Content-Type': 'application/json',
        }
    }
