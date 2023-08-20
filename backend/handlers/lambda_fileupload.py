import json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import NoCredentialsError

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
users_table = dynamodb.Table('users')
s3 = boto3.client('s3')

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])  # Define your allowed file extensions here
S3_BUCKET = "dilse_bucket"  # Replace with your bucket name

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_to_s3(file, bucket, filename):
    try:
        s3.upload_fileobj(file, bucket, filename)
        return True
    except NoCredentialsError:
        print("Credentials not available")
        return False

def upload_file(event, context):
    user_id = event['pathParameters']['user_id']

    # Check if the user_id exists
    user_response = users_table.query(
        KeyConditionExpression=Key('user_id').eq(user_id)
    )
    
    # If no items matched the user_id, return error
    if 'Items' not in user_response or len(user_response['Items']) == 0:
        return {
            'statusCode': 400,
            'body': json.dumps({"error": "User ID does not exist"})
        }

    # The file will be part of the event body, decoded from base64
    file_content = base64.b64decode(event['body']).decode('utf-8')  
    filename = event['headers']['filename']

    if not filename or filename == '':
        return {
            'statusCode': 400,
            'body': json.dumps({"error": "No selected file"})
        }

    if allowed_file(filename):
        if upload_to_s3(file_content, S3_BUCKET, filename):
            files_table = dynamodb.Table('user_files')
            file_item = {
                'user_id': user_id,
                'filename': filename,
                's3_bucket': S3_BUCKET,
                's3_key': filename
            }
            files_table.put_item(Item=file_item)
            return {
                'statusCode': 200,
                'body': json.dumps({"success": True, "message": "File uploaded successfully!"})
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": "Upload failed"})
            }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({"error": "File type not allowed"})
        }
