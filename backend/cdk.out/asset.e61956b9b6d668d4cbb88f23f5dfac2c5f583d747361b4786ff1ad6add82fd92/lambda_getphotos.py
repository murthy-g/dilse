import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
photos_table = dynamodb.Table('user_photos')

def get_photos(event, context):
    user_id = event['pathParameters']['user_id']

    # Query the photos table based on the user_id
    response = photos_table.query(
        KeyConditionExpression=Key('user_id').eq(user_id)
    )

    # Extract photo URLs or references
    photo_urls = [item['photo_url'] for item in response.get('Items', [])]

    return {
        'statusCode': 200,
        'body': json.dumps(photo_urls)
    }
