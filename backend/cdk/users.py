import boto3

dynamodb = boto3.resource('dynamodb')

users_table = dynamodb.create_table(
    TableName='users',
    KeySchema=[
        {
            'AttributeName': 'user_id',
            'KeyType': 'HASH'  # Partition key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'user_id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'email',   # Additional attribute definition for GSI
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'phone_number',
            'AttributeType': 'S'
        }
    ],
    GlobalSecondaryIndexes=[
        {
            'IndexName': 'EmailIndex',  # Name for the GSI
            'KeySchema': [
                {
                    'AttributeName': 'email',
                    'KeyType': 'HASH'
                }
            ],
            'Projection': {
                'ProjectionType': 'ALL'  # Can be KEYS_ONLY, INCLUDE, or ALL
            },
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        },
        {
            'IndexName': 'PhoneNumberIndex',  # Name for the GSI
            'KeySchema': [
                {
                    'AttributeName': 'phone_number',
                    'KeyType': 'HASH'
                }
            ],
            'Projection': {
                'ProjectionType': 'ALL'
            },
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

users_table.meta.client.get_waiter('table_exists').wait(TableName='users')
