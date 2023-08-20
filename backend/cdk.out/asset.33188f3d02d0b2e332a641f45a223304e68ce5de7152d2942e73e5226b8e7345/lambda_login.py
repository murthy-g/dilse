import boto3
import json
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
users_table = dynamodb.Table('users')

def lambda_login(event, context):
    data = json.loads(event['body'])

    email = data.get('email')
    password = data.get('password')  # Note: in real-world apps, hash and compare passwords!

    # Assuming 'EmailIndex' is the name of the GSI on the 'users' table with 'email' as the partition key
    response = users_table.query(
        IndexName='EmailIndex',
        KeyConditionExpression=Key('email').eq(email)
    )
    
    # Here, we're checking if the user exists and the password matches. 
    # In real-world scenarios, make sure to store hashed passwords in the DB and compare against the hashed value.
    if 'Items' in response and len(response['Items']) > 0 and response['Items'][0]['password'] == password:
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Login successful!",
                "user_id": response['Items'][0]['user_id']
            })
        }
    else:
        return {
            "statusCode": 401,
            "body": json.dumps({
                "message": "Invalid credentials"
            })
        }
