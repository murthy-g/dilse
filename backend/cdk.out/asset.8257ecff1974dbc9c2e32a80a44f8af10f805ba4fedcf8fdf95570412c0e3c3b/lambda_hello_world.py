def lambda_hello_world(event, context):
    return {
        'statusCode': 200,
        'body': 'Hello, World!',
        'headers': {
            'Content-Type': 'text/plain',
        }
    }
