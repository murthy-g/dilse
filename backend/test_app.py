import pytest
from app import app  # Replace 'app' with the name of your app's Python file
import json
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello_world(client):
    response = client.get('/')
    assert response.data == b'Hello, World!'

@patch('app.users_table')
def test_register_existing_email(mocked_table, client):
    mocked_table.query.return_value = {'Items': [{'email': 'test@example.com'}]}
    data = {
        'name': 'John Doe',
        'email': 'test@example.com',
        'password': 'password123',
        'age': 25,
        'gender': 'male',
        'location': 'NYC',
        'phone_number': '123-456-7890'
    }
    response = client.post('/register', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    assert b'Email already exists' in response.data

@patch('app.users_table')
def test_login_success(mocked_table, client):
    mocked_table.scan.return_value = {'Items': [{'user_id': 'user123', 'email': 'test@example.com', 'password': 'password123'}]}
    data = {
        'email': 'test@example.com',
        'password': 'password123'
    }
    response = client.post('/login', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert b'Login successful!' in response.data

#... add test_login_failure with 401 response ...

@patch('app.matches_table')
def test_get_matches(mocked_table, client):
    mocked_table.query.return_value = {'Items': []}
    response = client.get('/get_matches/user123')
    assert response.status_code == 200
    assert b'[]' in response.data

@patch('app.matches_table')
def test_like_user_match(mocked_table, client):
    mocked_table.get_item.return_value = {'Item': {'user_id': 'user123', 'liked_user_id': 'user456'}}
    data = {
        'current_user_id': 'user456',
        'liked_user_id': 'user123'
    }
    response = client.post('/like_user', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert b"It's a match!" in response.data

# @patch('app.matches_table')
# def test_like_user_not_matched(mocked_table, client):
#     # The scenario here is user123 likes user456, but user456 hasn't liked user123 back yet.
#     # Hence, we assume the `get_item` method returns no matching item for this pair.
#     mocked_table.get_item.return_value = None
    
#     data = {
#         'current_user_id': 'user123',
#         'liked_user_id': 'user456'
#     }
    
#     response = client.post('/like_user', data=json.dumps(data), content_type='application/json')
    
#     assert response.status_code == 200
#     # This message depends on what your service actually returns in this scenario.
#     assert b'User liked, but not a match yet.' in response.data


#... add test_like_user_not_matched ...

# @patch('app.users_table')
# @patch('app.upload_to_s3')
# def test_upload_file(mocked_upload, mocked_table, client):
#     mocked_table.query.return_value = {'Items': [{'user_id': 'user123'}]}
#     mocked_upload.return_value = True
#     with open('./friends.png', 'rb') as f:  # replace with a real path to a test file
#         response = client.post('/upload_file/user123', data={'file': f})

#     assert response.status_code == 200
#     assert b'File uploaded successfully!' in response.data

#... add other scenarios for test_upload_file ...

# @patch('app.dynamodb.Table')
# def test_get_photos(mocked_table, client):
#     mocked_table.return_value.query.return_value = {'Items': [{'photo_url': 'url1'}, {'photo_url': 'url2'}]}

# @patch('app.photos_table')
# def test_get_photos(mocked_table, client):
#     mocked_table.query.return_value = {'Items': [{'photo_url': 'url1'}, {'photo_url': 'url2'}]}
#     response = client.get('/getphotos/user123')
#     assert response.status_code == 200
#     assert b'url1' in response.data
#     assert b'url2' in response.data

# @patch('app.users_table')
# @patch('app.matches_table')
# def test_get_recommendations(mocked_matches_table, mocked_users_table, client):
#     #... mock your database returns ...
#     response = client.get('/recommendations/user123')
#     assert response.status_code == 200
#     #... assertions based on mocked return ...

# Continue with more test cases for edge cases and different scenarios.
