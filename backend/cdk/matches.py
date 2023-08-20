import boto3

dynamodb = boto3.resource('dynamodb')

matches_table = dynamodb.create_table(
    TableName='matches',
    KeySchema=[
        {
            'AttributeName': 'user_id',
            'KeyType': 'HASH'  # Partition key
        },
        {
            'AttributeName': 'liked_user_id',
            'KeyType': 'RANGE'  # Sort key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'user_id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'liked_user_id',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

matches_table.meta.client.get_waiter('table_exists').wait(TableName='matches')
