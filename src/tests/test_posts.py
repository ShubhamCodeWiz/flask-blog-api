# tests/test_posts.py
from src.models import User
from src import db
from flask_jwt_extended import create_access_token

def test_get_posts_empty(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/posts' page is requested (GET)
    THEN check that the response is valid and the database is empty
    """
    response = test_client.get('/posts')
    assert response.status_code == 200
    assert response.json == []

def test_create_post(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/posts' page is posted to (POST) with valid data and auth
    THEN check that the response is valid and the post is in the database
    """
    # 1. Setup: Create a user and a token for them
    test_user = User(username='testuser')
    test_user.set_password('password123')
    db.session.add(test_user)
    db.session.commit()
    
    # We need an app context to create a token
    with test_client.application.app_context():
        access_token = create_access_token(identity=str(test_user.id))

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    # 2. Action: Make the POST request
    new_post_data = {
        'title': 'Test Post',
        'content': 'This is a test.'
    }
    response = test_client.post('/posts', json=new_post_data, headers=headers)

    # 3. Assertion: Check the outcome
    assert response.status_code == 201
    assert response.json['title'] == 'Test Post'
    assert response.json['author']['username'] == 'testuser'