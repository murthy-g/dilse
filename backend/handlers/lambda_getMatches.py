
import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
users_table = dynamodb.Table('users')
matches_table = dynamodb.Table('matches')


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
matches_table = dynamodb.Table('matches')

def get_matches(event, context):
    user_id = event['pathParameters']['user_id']  # Assuming you have defined 'user_id' as a path parameter in API Gateway
    
    response = matches_table.query(KeyConditionExpression=Key('user_id').eq(user_id))

    # Return results in the format AWS Lambda expects for API Gateway
    return {
        'statusCode': 200,
        'body': json.dumps(response.get('Items', [])),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  # If needed
        }
    }
