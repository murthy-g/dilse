
from flask import Flask, request, jsonify
import boto3
import uuid
from helpers.file import S3_BUCKET, allowed_file, upload_to_s3
from models.User import User
from models.Match import Match
from boto3.dynamodb.conditions import Key, Attr
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)



dynamodb = boto3.resource('dynamodb', aws_access_key_id='AKIA5B6GM6M7NNHMUQNU',
                  aws_secret_access_key='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', region_name='us-east-1')
users_table = dynamodb.Table('users')
matches_table = dynamodb.Table('matches')
photos_table = dynamodb.Table('user_photos')

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/register', methods=['POST'])
def register():
    data = request.json

    # Check if email already exists using GSI
    email_check = users_table.query(
        IndexName='EmailIndex',  # Replace with your GSI name
        KeyConditionExpression=Key('email').eq(data['email'])
    )
    
    if 'Items' in email_check and len(email_check['Items']) > 0:
        return jsonify({"error": "Email already exists"}), 400

    
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
    return jsonify(response), 201


@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')  # Note: in real-world apps, compare hashed passwords!

    # For simplicity, we're fetching by user_id. In real apps, you'll likely fetch by email.
    response = users_table.scan(FilterExpression=Attr('email').eq(email) & Attr('password').eq(password))
    
    if 'Items' in response and len(response['Items']) > 0:
        return jsonify({'message': 'Login successful!', 'user_id': response['Items'][0]['user_id']}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/get_matches/<user_id>', methods=['GET'])
def get_matches(user_id):
    # Note: You'll need to import Key from boto3.dynamodb.conditions for the below line to work
    response = matches_table.query(KeyConditionExpression=Key('user_id').eq(user_id))
    return jsonify(response.get('Items', []))

@app.route('/like_user', methods=['POST'])
def like_user():
    current_user_id = request.json.get('current_user_id')
    liked_user_id = request.json.get('liked_user_id')
    
    # Check if the liked user has also liked the current user
    response = matches_table.get_item(Key={'user_id': liked_user_id, 'liked_user_id': current_user_id})

    match = None
    if 'Item' in response:
        match = Match(current_user_id, liked_user_id, 'matched')
    else:
        match = Match(current_user_id, liked_user_id)

    matches_table.put_item(Item=match.to_dynamo_item())

    return jsonify({'message': match.status == 'matched' and 'It\'s a match!' or 'Like registered!'}), 200

@app.route('/upload_file/<user_id>', methods=['POST'])
def upload_file(user_id):
    # Check if the user_id exists
    user_response = users_table.query(
        KeyConditionExpression=Key('user_id').eq(user_id)
    )
    
    # If no items matched the user_id, return error
    if 'Items' not in user_response or len(user_response['Items']) == 0:
        return jsonify({"error": "User ID does not exist"}), 400

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if upload_to_s3(file, S3_BUCKET):
            # After successful upload, save the filename to your DynamoDB
            files_table = dynamodb.Table('user_files')  # Assuming you have a table called 'user_files'
            file_item = {
                'user_id': user_id,
                'filename': filename,
                's3_bucket': S3_BUCKET,
                's3_key': filename
            }
            files_table.put_item(Item=file_item)
            return jsonify({"success": True, "message": "File uploaded successfully!"}), 200
        else:
            return jsonify({"error": "Upload failed"}), 500
    else:
        return jsonify({"error": "File type not allowed"}), 400

@app.route('/getphotos/<user_id>', methods=['GET'])
def get_photos(user_id):
    # photos_table = dynamodb.Table('user_photos')  # Assuming you have a table named 'user_photos'

    # Query the photos table based on the user_id
    response = photos_table.query(
        KeyConditionExpression=Key('user_id').eq(user_id)
    )

    # Extract photo URLs or references
    photo_urls = [item['photo_url'] for item in response.get('Items', [])]

    return jsonify(photo_urls)

@app.route('/recommendations/<user_id>', methods=['GET'])
def get_recommendations(user_id):

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

    return jsonify(profiles)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
